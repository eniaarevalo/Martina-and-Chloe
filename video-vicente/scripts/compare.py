"""Compara guion.txt con transcript.json palabra a palabra (números normalizados)."""
import json, re, difflib, unicodedata
NUM = {"mil novecientos noventa y nueve": "1999", "antena tres": "antena 3", "trece": "13", "dos mil tres": "2003",
       "siete coma tres": "7,3", "cuarenta por ciento": "40%", "cinco coma nueve": "5,9", "dos mil seis": "2006", "dos mil diez": "2010", "dos mil nueve": "2009", "veintiseis": "26", "ciento dieciseis": "116", "once de julio": "11 de julio", "dos mil veintiseis": "2026", "dos mil veinticinco": "2025", "trescientos": "300", "quince": "15", "doscientos ochenta y cinco mil": "285000", "dos mil veintiuno": "2021", "ciento cuarenta": "140", "dos o tres": "2 o 3", "treinta y siete por ciento": "37%", "dos mil siete": "2007", "dos mil doce": "2012", "quince por ciento": "15%", "tres millones": "3 millones", "dos mil metros": "2000 metros", "veintiuno": "21", "catorce": "14", "quinientos": "500"}
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"(\d)\.(\d{3})", r"\1\2", s)
    for k, v in NUM.items(): s = s.replace(k, v)
    return re.findall(r"[a-z0-9,%]+(?<!,)|\d+,\d+", s)
g = norm(open("guion.txt").read())
words = json.load(open("transcript.json"))
t = norm(" ".join(w["text"] for w in words))
ok = True
for op, a1, a2, b1, b2 in difflib.SequenceMatcher(a=g, b=t, autojunk=False).get_opcodes():
    if op != "equal":
        ok = False; print(f"{op}: guion={g[a1:a2]}  voz={t[b1:b2]}")
print(f"guion={len(g)} palabras, voz={len(t)} palabras ->", "IGUALES" if ok else "DIFERENCIAS")
