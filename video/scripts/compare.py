"""Compara guion.txt con transcript.json palabra a palabra (números normalizados)."""
import json, re, difflib, unicodedata
NUM = {"mil novecientos noventa y nueve": "1999", "antena tres": "antena 3", "trece": "13", "dos mil tres": "2003",
       "siete coma tres": "7,3", "cuarenta por ciento": "40%", "cinco coma nueve": "5,9", "veintiuno": "21", "veinte": "20"}
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    for k, v in NUM.items(): s = s.replace(k, v)
    s = s.replace("rue del", "ruedel")
    return re.findall(r"[a-z0-9,%]+(?<!,)|\d+,\d+", s)
g = norm(open("guion.txt").read())
words = json.load(open("transcript.json"))
t = norm(" ".join(w["text"] for w in words))
ok = True
for op, a1, a2, b1, b2 in difflib.SequenceMatcher(a=g, b=t, autojunk=False).get_opcodes():
    if op != "equal":
        ok = False; print(f"{op}: guion={g[a1:a2]}  voz={t[b1:b2]}")
print(f"guion={len(g)} palabras, voz={len(t)} palabras ->", "IGUALES" if ok else "DIFERENCIAS")
