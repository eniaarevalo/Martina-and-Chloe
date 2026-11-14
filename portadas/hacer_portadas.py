"""Portadas (1080x1920) para TikTok, Reels y Shorts de cada vídeo.

Cada portada usa un fotograma del vídeo sin subtítulos (recortado a la zona de la animación)
y un título grande arriba, dentro de la zona que se ve en la cuadrícula del perfil (centro 3:4).

Uso:  python3 portadas/hacer_portadas.py            -> todas
      python3 portadas/hacer_portadas.py video-perro -> solo una
Salida: <carpeta>/entregas/portada.png y una copia en portadas/<carpeta>.png
"""
import base64, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# carpeta: (segundo del fotograma, [líneas del título], palabra resaltada, color del resaltado, etiqueta)
PORTADAS = {
    "video":            (2.2,  ["ASÍ EMPEZÓ", "AQUÍ NO HAY", "QUIEN VIVA"], "QUIEN VIVA", "#facc15", "LOS CASTINGS"),
    "video-edificio":   (33.8, ["EL EDIFICIO DE", "AQUÍ NO HAY QUIEN VIVA", "EXISTE"], "EXISTE", "#22c55e", "AQUÍ NO HAY QUIEN VIVA"),
    "video-lgtbi":      (35.3, ["MAURI Y FERNANDO", "CAMBIARON", "ESPAÑA"], "ESPAÑA", "#ec4899", "AQUÍ NO HAY QUIEN VIVA"),
    "video-lqsa":       (37.9, ["POR QUÉ ACABÓ", "AQUÍ NO HAY", "QUIEN VIVA"], "QUIEN VIVA", "#ef4444", "Y NACIÓ LQSA"),
    "video-recio":      (2.0,  ["¿POR QUÉ", "QUEREMOS A", "ANTONIO RECIO?"], "ANTONIO RECIO?", "#facc15", "PSICOLOGÍA"),
    "video-glucosa":    (25.1, ["ESE BAJÓN", "DESPUÉS DE COMER", "TIENE NOMBRE"], "TIENE NOMBRE", "#ef4444", "PICOS DE GLUCOSA"),
    "video-adopta":     (2.2,  ["ADOPTA,", "NO COMPRES"], "NO COMPRES", "#22c55e", "LO QUE NO TE CUENTAN"),
    "video-iniesta":    (17.1, ["LA HISTORIA", "DETRÁS DEL GOL", "DE INIESTA"], "DE INIESTA", "#ef4444", "MUNDIAL 2010"),
    "video-musica":     (26.7, ["¿POR QUÉ HAY", "MÚSICA EN", "EL SÚPER?"], "EL SÚPER?", "#facc15", "TE ESTÁN INFLUYENDO"),
    "video-aviones":    (2.3,  ["¿POR QUÉ LAS", "VENTANAS SON", "REDONDAS?"], "REDONDAS?", "#38bdf8", "AVIONES"),
    "video-perro":      (2.2,  ["LO QUE UN PERRO", "HACE EN", "TU CABEZA"], "TU CABEZA", "#ec4899", "PSICOLOGÍA"),
    "video-loteria":    (2.3,  ["¿POR QUÉ CANTAN", "NIÑOS", "LA LOTERÍA?"], "LA LOTERÍA?", "#facc15", "NAVIDAD"),
    "video-montepinar": (3.9,  ["¿EXISTE", "MONTEPINAR?"], "MONTEPINAR?", "#f97316", "LA QUE SE AVECINA"),
    "video-dedos":      (3.2,  ["¿POR QUÉ", "CRUZAMOS", "LOS DEDOS?"], "LOS DEDOS?", "#facc15", "SUPERSTICIONES"),
    "video-supernenas": (5.2,  ["MARISA, CONCHA", "Y VICENTA:", "LAS SUPERNENAS"], "LAS SUPERNENAS", "#a78bfa", "AQUÍ NO HAY QUIEN VIVA"),
    "video-terror":     (41.5, ["NUNCA RESPONDAS", "A SUS", "PREGUNTAS"], "PREGUNTAS", "#dc2626", "HISTORIA DE TERROR"),
    "video-belen":      (18.3, ["BELÉN Y EMILIO", "SEGÚN LA", "PSICOLOGÍA"], "PSICOLOGÍA", "#db2777", "AQUÍ NO HAY QUIEN VIVA"),
    "video-hora":       (31.2, ["¿CENAMOS TARDE", "POR CULPA", "DE HITLER?"], "DE HITLER?", "#ef4444", "MITO O VERDAD"),
}

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1080px;height:1920px;background:#07080b;overflow:hidden;font-family:Inter,sans-serif}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 80%, rgba(92,108,255,0.35), transparent 60%),
  linear-gradient(rgba(255,255,255,0.04) 2px, transparent 2px) 0 0/60px 60px,
  linear-gradient(90deg, rgba(255,255,255,0.04) 2px, transparent 2px) 0 0/60px 60px, #08090d}}
.wrap{{position:absolute;left:60px;right:60px;top:260px;bottom:240px;display:flex;flex-direction:column;align-items:center}}
.tag{{padding:10px 34px;border-radius:999px;background:#fff;color:#0f172a;
  font-weight:900;font-size:40px;letter-spacing:1px;white-space:nowrap}}
.title{{width:100%;text-align:center;margin-top:24px}}
.l{{display:block;font-weight:900;color:#fff;line-height:1.04;letter-spacing:-2px;white-space:nowrap;text-shadow:0 8px 30px rgba(0,0,0,0.6)}}
.hl{{display:inline-block;padding:0 22px;border-radius:22px;color:#0f172a;margin-top:10px}}
.shot{{flex:1;min-height:0;width:940px;margin-top:40px;border-radius:40px;overflow:hidden;border:8px solid rgba(255,255,255,0.9);
  box-shadow:0 30px 80px rgba(0,0,0,0.6), 0 0 60px {color}55}}
.shot img{{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 40%}}
</style></head><body><div class="bg"></div>
<div class="wrap"><div class="tag">{tag}</div>
<div class="title">{lines}</div>
<div class="shot"><img src="data:image/png;base64,{img}"></div></div>
<script>
// cada línea en una sola fila: se reduce el tamaño hasta que cabe en 960 px
document.querySelectorAll('.title .l').forEach(function(el){{
  var t = el.querySelector('.hl') || el;
  var s = parseFloat(getComputedStyle(t).fontSize);
  while (el.scrollWidth > 960 && s > 50) {{ s -= 2; t.style.fontSize = s + 'px'; }}
}});
</script>
</body></html>"""


def frame_png(video, t, out):
    # recorte de la zona animada (y 380..1480 del vídeo) para que se lea en pequeño
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1",
                    "-vf", "crop=1080:1100:0:380", out], check=True)


def build(name):
    t, lines, hl, color, tag = PORTADAS[name]
    video = os.path.join(ROOT, name, "entregas", "video-SIN-SUBTITULOS.mp4")
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, "f.png")
    frame_png(video, t, png)
    img = base64.b64encode(open(png, "rb").read()).decode()
    longest = max(len(l) for l in lines)
    size = 140
    html_lines = []
    for l in lines:
        if l == hl:
            html_lines.append(f'<span class="l"><span class="hl" style="background:{color};font-size:{size}px">{l}</span></span>')
        else:
            html_lines.append(f'<span class="l" style="font-size:{size}px">{l}</span>')
    html = HTML.format(tag=tag, lines="".join(html_lines), img=img, color=color)
    hp = os.path.join(tmp, "p.html")
    open(hp, "w").write(html)
    out1 = os.path.join(ROOT, name, "entregas", "portada.png")
    out2 = os.path.join(ROOT, "portadas", f"{name}.png")
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: 1080, height: 1920 }}, deviceScaleFactor: 1 }});
  await p.goto('file://{hp}');
  await p.waitForTimeout(300);
  await p.screenshot({{ path: '{out1}' }});
  await b.close();
}})();"""
    jp = os.path.join(tmp, "s.js")
    open(jp, "w").write(js)
    subprocess.run(["node", jp], check=True)
    subprocess.run(["cp", out1, out2], check=True)
    print("portada:", name)


if __name__ == "__main__":
    names = sys.argv[1:] or list(PORTADAS)
    for n in names:
        build(n)
