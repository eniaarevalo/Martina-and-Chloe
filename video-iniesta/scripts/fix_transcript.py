"""Corrige cómo escribe Whisper algunas palabras (no los tiempos) y quita palabras inventadas
sobre el silencio final. Guarda la original en transcript.raw.json.
Uso: python3 scripts/fix_transcript.py"""
import json, os, re, subprocess
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
w = json.load(open("transcript.json"))
if os.path.exists("transcript.raw.json") and json.load(open("transcript.raw.json"))[0]["start"] == w[0]["start"] \
        and len(json.load(open("transcript.raw.json"))) >= len(w):
    w = json.load(open("transcript.raw.json"))
json.dump(w, open("transcript.raw.json", "w"), ensure_ascii=False, indent=1)

# 1) silencio final: Whisper inventa palabras ahí («Gracias.»)
log = subprocess.run(["ffmpeg", "-i", "voz.wav", "-af", "silencedetect=noise=-35dB:d=0.6", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "voz.wav"],
                           capture_output=True, text=True).stdout)
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
tail = [s for s in starts if s > dur - 3]
if tail:
    w = [x for x in w if x["start"] < tail[-1]]

import unicodedata
def _plain(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
GUION = set(re.findall(r"\w+", _plain(open("guion.txt").read()))) if os.path.exists("guion.txt") else set()
# «costas.¿Y» -> «costas.» + «¿Y»: se parte donde empieza la pregunta, repartiendo el tiempo por letras
split = []
for x in w:
    i = x["text"].find("¿")
    if i > 0:
        a_, b_ = x["text"][:i], x["text"][i:]
        mid = round(x["start"] + (x["end"] - x["start"]) * len(a_) / len(x["text"]), 3)
        split += [dict(text=a_, start=x["start"], end=mid), dict(text=b_, start=mid, end=x["end"])]
    else:
        split.append(x)
w = split

BLOQUE = {"1": "Uno", "2": "Dos", "3": "Tres", "4": "Cuatro"}
SPELL = {"Zeki": "Zequi", "Zeki,": "Zequi,", "Español,": "Espanyol,", "Español": "Espanyol", "Zek.": "Cesc.", "Zek": "Cesc", "Zek,": "Cesc,"}
out = []
for x in w:
    x = dict(x)
    m = re.fullmatch(r"(\d)\.", x["text"])
    if m and m.group(1) in BLOQUE and (not out or re.search(r"[.]$", out[-1]["text"])):
        x["text"] = BLOQUE[m.group(1)] + ":"
    x["text"] = SPELL.get(x["text"], x["text"])
    m2 = re.fullmatch(r"(Maury)([.,:]?)", x["text"])
    if m2:
        x["text"] = "Mauri" + m2.group(2)
    m3 = re.fullmatch(r"([Pp])rimetime([.,:]?)", x["text"])
    if m3:  # «Primetime» -> «prime» + «time», repartiendo el tiempo
        mid = round((x["start"] + x["end"]) / 2, 3)
        out.append(dict(text=m3.group(1).lower() + "rime", start=x["start"], end=mid))
        x = dict(text="time" + m3.group(2), start=mid, end=x["end"])
    if x["text"] == "plato.":
        x["text"] = "plató."
    if x["text"] == "dama,":  # la «y» va pegada al final de «dama»
        mid = round(x["start"] + (x["end"] - x["start"]) * 0.7, 3)
        out.append(dict(text="dama", start=x["start"], end=mid))
        x = dict(text="y,", start=mid, end=x["end"])
    if x["text"] == "medio." and out and out[-1]["text"] == "en":
        prev = out.pop()
        x = dict(text="Enmedio.", start=prev["start"], end=x["end"])
    if out and out[-1]["text"].lower() == "moraleja":
        out[-1]["text"] = "Moraleja"
    if x["text"] == "Yabajo":
        x["text"] = "Yque"[:0] + "Y abajo"
        mid = round(x["start"] + (x["end"] - x["start"]) * 0.35, 3)
        out.append(dict(text="Y", start=x["start"], end=mid))
        x = dict(text="abajo", start=mid, end=x["end"])
    _w = re.sub(r"\W", "", _plain(x["text"]))
    if (x["text"][:1] == "Y" and len(_w) > 2 and _w not in GUION and _w[1:] in GUION) or x["text"] in ("Yde", "Yjusto"):
        x["text"] = "Yque" if False else x["text"]
        mid = round(x["start"] + (x["end"] - x["start"]) * 0.3, 3)
        out.append(dict(text="Y", start=x["start"], end=mid))
        x = dict(text=x["text"][1:].lstrip(), start=mid, end=x["end"])
    if x["text"] == "Yque":  # palabras pegadas: se reparte el tiempo
        mid = round(x["start"] + (x["end"] - x["start"]) * 0.35, 3)
        out.append(dict(text="Y", start=x["start"], end=mid))
        x = dict(text="que", start=mid, end=x["end"])
    out.append(x)
# Whisper a veces repite la última palabra (la parte en dos): se juntan
while len(out) > 1 and out[-1]["text"] == out[-2]["text"]:
    out[-2]["end"] = out[-1]["end"]
    out.pop()
for k, x in enumerate(out):
    x["id"] = f"w{k}"
json.dump(out, open("transcript.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(w)} -> {len(out)} palabras")

# Si hay las mismas palabras que en el guion, se usa la ortografía y puntuación del guion (los tiempos no cambian)
_w = json.load(open("transcript.json"))
_t = [t.replace("«", "").replace("»", "") for t in open("guion.txt").read().split()]
if len(_t) == len(_w):
    for x, t in zip(_w, _t):
        x["text"] = t
    json.dump(_w, open("transcript.json", "w"), ensure_ascii=False, indent=1)
    print("ortografía tomada del guion")
