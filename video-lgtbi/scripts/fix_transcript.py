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

BLOQUE = {"1": "Uno", "2": "Dos", "3": "Tres", "4": "Cuatro"}
SPELL = {"Zeki": "Zequi", "Zeki,": "Zequi,"}
out = []
for x in w:
    x = dict(x)
    m = re.fullmatch(r"(\d)\.", x["text"])
    if m and m.group(1) in BLOQUE and (not out or re.search(r"[.]$", out[-1]["text"])):
        x["text"] = BLOQUE[m.group(1)] + ":"
    x["text"] = SPELL.get(x["text"], x["text"])
    if x["text"] == "Yque":  # palabras pegadas: se reparte el tiempo
        mid = round(x["start"] + (x["end"] - x["start"]) * 0.35, 3)
        out.append(dict(text="Y", start=x["start"], end=mid))
        x = dict(text="que", start=mid, end=x["end"])
    out.append(x)
for k, x in enumerate(out):
    x["id"] = f"w{k}"
json.dump(out, open("transcript.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(w)} -> {len(out)} palabras")
