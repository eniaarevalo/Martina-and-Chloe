"""Corrige cómo escribe Whisper algunas palabras (no los tiempos): números de bloque,
nombres partidos... Guarda la original en transcript.raw.json.  Uso: python3 scripts/fix_transcript.py"""
import json, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
w = json.load(open("transcript.json"))
if any(x["text"] == "Merlo" or x["text"].endswith(":") for x in w):  # ya corregida: parte de la original
    w = json.load(open("transcript.raw.json"))
json.dump(w, open("transcript.raw.json", "w"), ensure_ascii=False, indent=1)
BLOQUE = {"1": "Uno", "2": "Dos", "3": "Tres", "4": "Cuatro"}
out = []
i = 0
while i < len(w):
    x = dict(w[i])
    m = re.fullmatch(r"(\d)\.", x["text"])
    prev = out[-1]["text"] if out else ""
    if m and m.group(1) in BLOQUE and re.search(r"[.]$", prev):
        x["text"] = BLOQUE[m.group(1)] + ":"
    if i + 1 < len(w) and x["text"] == "Mer" and w[i + 1]["text"].startswith("lo"):
        x["text"] = "Merlo" + w[i + 1]["text"][2:]
        x["end"] = w[i + 1]["end"]
        i += 1
    if x["text"].startswith("Ruedel"):
        x["text"] = "Rue del" + x["text"][6:]
    out.append(x)
    i += 1
for k, x in enumerate(out):
    x["id"] = f"w{k}"
json.dump(out, open("transcript.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(w)} -> {len(out)} palabras")
