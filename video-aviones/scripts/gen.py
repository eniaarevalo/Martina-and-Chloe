"""Generador del vídeo «¿Por qué las ventanas de los aviones son redondas?».

Lee transcript.json (tiempos de cada palabra) y escribe:
  index.html, compositions/world.html, compositions/captions.html y assets/sfx-cues.json
Todo lo que se anima va enganchado a P("palabra", n): el momento en que EMPIEZA la
n-ésima vez que la voz dice esa palabra. Si cambia la voz o el guion, se vuelve a ejecutar
y todo se recoloca solo.

Uso: python3 scripts/gen.py [--sin-subtitulos] [--hasta SEGUNDOS]
"""
import json, math, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
from rig import character, PIVOT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SIN_SUBS = "--sin-subtitulos" in sys.argv
HASTA = float(sys.argv[sys.argv.index("--hasta") + 1]) if "--hasta" in sys.argv else None

# ---------------------------------------------------------------- tiempos de la voz
WORDS = json.load(open("transcript.json"))
VOZ_DUR = 49.313875
try:
    import subprocess
    VOZ_DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    "voz.wav"], capture_output=True, text=True).stdout)
except Exception:
    pass
DUR = HASTA or VOZ_DUR


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9%,]", "", s).strip(",")


NW = [norm(w["text"]) for w in WORDS]
SYNC = {}


def P(word, n=1):
    """Inicio de la n-ésima vez que se dice `word` (admite frases: P("antena 3"))."""
    seq = [norm(x) for x in word.split()]
    hits = [i for i in range(len(NW)) if NW[i:i + len(seq)] == seq]
    if len(hits) < n:
        raise SystemExit(f'P("{word}", {n}): solo aparece {len(hits)} veces en la voz')
    t = round(WORDS[hits[n - 1]]["start"], 3)
    SYNC.setdefault(f"{word}#{n}", dict(palabra=WORDS[hits[n - 1]]["text"], vez=n, empieza=t))
    return t


def E(word, n=1):
    """Final de esa palabra."""
    seq = [norm(x) for x in word.split()]
    hits = [i for i in range(len(NW)) if NW[i:i + len(seq)] == seq]
    t = round(WORDS[hits[n - 1] + len(seq) - 1]["end"], 3)
    SYNC.setdefault(f"E:{word}#{n}", dict(palabra=WORDS[hits[n - 1]]["text"] + " (final)", vez=n, empieza=t))
    return t


# ---------------------------------------------------------------- estilo
GOOD, BAD, ACC, INK = "#22c55e", "#ef4444", "#ffd43b", "#0f1115"
GOOD_BG = "#15803d"  # verde para fondos con texto blanco (contraste AA)
FONT = "Inter"

# ---------------------------------------------------------------- mundo (lienzo gigante)
COLX = [40, 1100]
CW, CH = 1060, 1300
ROWY = {"roof": 0, "3": 1300, "2": 2600, "1": 3900, "bajo": 5200}
FLOOR = {k: v + CH - 40 for k, v in ROWY.items()}  # donde pisan los personajes


def cell(row, col):
    return (COLX[col], ROWY[row], CW, CH)


def frame(row, col):
    """Zona de contenido (960x1080) de cada piso."""
    return (COLX[col] + 50, ROWY[row] + 110, 960, 1080)


# Caja de pantalla donde encuadra la cámara (fuera de subtítulos y zonas seguras)
SCR = dict(x=60, y=400, w=960, h=1080)


def cam_of(rect, box=SCR):
    x, y, w, h = rect
    s = min(box["w"] / w, box["h"] / h)
    cx, cy = x + w / 2, y + h / 2
    return dict(x=round(box["x"] + box["w"] / 2 - cx * s, 1), y=round(box["y"] + box["h"] / 2 - cy * s, 1), s=round(s, 4))


HTML = []      # piezas del mundo
JS = []        # tweens
SFX = []       # (t, archivo, volumen)


def js(s):
    JS.append(s)


def sfx(t, name, vol=0.5):
    if t < DUR:
        SFX.append(dict(t=round(t, 3), file=name, vol=vol))


def css_box(x, y, w=None, h=None, z=3, extra=""):
    s = f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;"
    if w is not None:
        s += f"width:{w:.0f}px;"
    if h is not None:
        s += f"height:{h:.0f}px;"
    return s + f"z-index:{z};" + extra


ICON_DIR = "node_modules/lucide-static/icons"


def icon(name, size, color="#111", sw=2.4):
    svg = open(f"{ICON_DIR}/{name}.svg").read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r'width="24"', f'width="{size}"', svg)
    svg = re.sub(r'height="24"', f'height="{size}"', svg)
    svg = svg.replace('stroke="currentColor"', f'stroke="{color}"').replace('stroke-width="2"', f'stroke-width="{sw}"')
    svg = re.sub(r'\sclass="[^"]*"', "", svg)
    return svg.strip()


def chars(text, cls="ch"):
    """Texto partido en letras para escribirlo letra a letra (las palabras siguen saltando de línea)."""
    words = []
    for w in text.split(" "):
        words.append('<span style="display:inline-block;white-space:nowrap">' +
                     "".join(f'<span class="{cls}">{c}</span>' for c in w) + "</span>")
    return " ".join(words)


def type_on(sel, n_chars, t0, t1):
    js(f'typeOn("{sel}", {t0:.3f}, {t1:.3f});')
    # teclas
    k = 0
    t = t0
    while t < t1:
        sfx(t, "teclado-tic", 0.18) if k % 3 == 0 else None
        t += (t1 - t0) / max(1, n_chars)
        k += 1


ROLL_N = 3  # vueltas del rodillo


def roller(rid, text, size, color=INK, weight=900):
    """Número que gira como un rodillo. Cada dígito es una tira 0-9 repetida."""
    h = round(size * 1.12)
    parts = []
    di = 0
    for c in text:
        if c.isdigit():
            strip = "".join(f'<span style="display:block;height:{h}px;line-height:{h}px">{d % 10}</span>'
                            for d in range(10 * ROLL_N))
            parts.append(f'<span class="dg" data-layout-ignore style="display:inline-block;height:{h}px;overflow:hidden;vertical-align:top">'
                         f'<span id="{rid}-d{di}" class="strip" data-layout-ignore style="display:block">{strip}</span></span>')
            di += 1
        else:
            parts.append(f'<span style="display:inline-block;height:{h}px;line-height:{h}px;vertical-align:top">{c}</span>')
    return (f'<span id="{rid}" class="roller" style="display:inline-block;font-size:{size}px;font-weight:{weight};'
            f'color:{color};font-variant-numeric:tabular-nums;line-height:{h}px;white-space:nowrap">{"".join(parts)}</span>'), h


def roll_to(rid, text, h, t, dur=0.8, spins=1, from_text=None, stagger=0.06):
    """Gira el rodillo hasta `text`. spins: vueltas completas extra."""
    digits = [c for c in text if c.isdigit()]
    for i, d in enumerate(digits):
        base = 10 * min(spins, ROLL_N - 1)
        idx = base + int(d)
        js(f'tl.to("#{rid}-d{i}", {{y:{-idx * h}, duration:{dur:.2f}, ease:"power3.out"}}, {t + i * stagger:.3f});')
    sfx(t, "tic-rodillo", 0.25)


def roll_set(rid, text, h):
    digits = [c for c in text if c.isdigit()]
    for i, d in enumerate(digits):
        js(f'tl.set("#{rid}-d{i}", {{y:{-int(d) * h}}}, 0);')


CAMS = []


def cam(t, rect, dur=0.7, ease="power3.inOut", box=SCR, whoosh=True):
    c = cam_of(rect, box)
    if CAMS:
        p = CAMS[-1]["c"]
        dist = math.hypot(c["x"] - p["x"], c["y"] - p["y"]) + abs(math.log(c["s"] / p["s"])) * 900
    else:
        dist = 0
    CAMS.append(dict(t=t, c=c, dur=dur, ease=ease))
    if not CAMS[:-1]:
        js(f'tl.set("#wd", {{x:{c["x"]}, y:{c["y"]}, scale:{c["s"]}, transformOrigin:"0 0"}}, 0);')
        js(f'tl.set("#grid", {{backgroundPosition:"{c["x"] * 0.25:.0f}px {c["y"] * 0.25:.0f}px"}}, 0);')
        return
    js(f'tl.to("#wd", {{x:{c["x"]}, y:{c["y"]}, scale:{c["s"]}, duration:{dur}, ease:"{ease}"}}, {t:.3f});')
    js(f'tl.to("#grid", {{backgroundPosition:"{c["x"] * 0.25:.0f}px {c["y"] * 0.25:.0f}px", duration:{dur}, ease:"{ease}"}}, {t:.3f});')
    if dist > 900 and t > 1:  # viaje largo: un poco de desenfoque
        js(f'tl.to("#wd", {{filter:"blur(5px)", duration:{dur * 0.4:.2f}, ease:"power1.in"}}, {t:.3f});')
        js(f'tl.to("#wd", {{filter:"blur(0px)", duration:{dur * 0.45:.2f}, ease:"power1.out"}}, {t + dur * 0.5:.3f});')
    if whoosh and dist > 250:
        sfx(t, "whoosh" if dist > 900 else "whoosh-corto", 0.35 if dist > 900 else 0.25)


def shake(t, amp=16):
    js(f'tl.to("#shake", {{keyframes:[{{x:{-amp},y:{amp * 0.6:.0f}}},{{x:{amp * 0.8:.0f},y:{-amp * 0.4:.0f}}},'
       f'{{x:{-amp * 0.5:.0f},y:{amp * 0.3:.0f}}},{{x:0,y:0}}], duration:0.36, ease:"power2.out"}}, {t:.3f});')


def pop(sel, t, sound="pop", vol=0.3, dur=0.42, from_scale=0.4, ease="back.out(2.2)"):
    js(f'tl.fromTo("{sel}", {{opacity:0, scale:{from_scale}}}, {{opacity:1, scale:1, duration:{dur}, ease:"{ease}"}}, {t:.3f});')
    if sound:
        sfx(t, sound, vol)


def slide_in(sel, t, dx=0, dy=60, dur=0.5, sound="pop2", vol=0.22):
    js(f'tl.fromTo("{sel}", {{opacity:0, x:{dx}, y:{dy}}}, {{opacity:1, x:0, y:0, duration:{dur}, ease:"power3.out"}}, {t:.3f});')
    if sound:
        sfx(t, sound, vol)


def stamp(sel, t, rot=-12):
    js(f'tl.fromTo("{sel}", {{opacity:0, scale:2.6, rotation:{rot - 14}}}, {{opacity:1, scale:1, rotation:{rot}, '
       f'duration:0.32, ease:"power4.in"}}, {t:.3f});')
    sfx(t + 0.28, "golpe", 0.35)


def floaty(sel, t0, t1, amp=7, period=2.4):
    n = max(1, int((t1 - t0) / period * 2))
    js(f'tl.to("{sel}", {{y:"-={amp}", duration:{period / 2:.2f}, ease:"sine.inOut", yoyo:true, repeat:{n - 1}}}, {t0:.3f});')


def add(html):
    HTML.append(html)


def card(cid, x, y, w, h, inner, z=6, extra="", bg="#ffffff"):
    add(f'<div id="{cid}" class="card" style="{css_box(x, y, w, h, z)}background:{bg};{extra}">{inner}</div>')


def life(cid, t0, t1, seed):
    js(f'life("{cid}", {t0:.3f}, {t1:.3f}, {seed});')


# ================================================================= HTML
STYLE = f"""
#root {{ position:absolute; inset:0; overflow:hidden; background:#07080b; font-family:{FONT}, sans-serif; }}
#grid {{ position:absolute; inset:-200px; background-color:#08090d;
  background-image: linear-gradient(rgba(255,255,255,0.045) 2px, transparent 2px),
                    linear-gradient(90deg, rgba(255,255,255,0.045) 2px, transparent 2px);
  background-size: 90px 90px; }}
#glow {{ position:absolute; left:-200px; right:-200px; bottom:-500px; height:1200px;
  background: radial-gradient(ellipse at 50% 70%, rgba(92,108,255,0.38), rgba(46,196,182,0.12) 45%, transparent 70%); }}
#scrim {{ position:absolute; left:0; right:0; top:0; height:520px; pointer-events:none;
  background:linear-gradient(rgba(7,8,11,0.97) 0%, rgba(7,8,11,0.94) 62%, rgba(7,8,11,0) 100%); }}
#shake {{ position:absolute; left:0; top:0; width:1080px; height:1920px; }}
#wd {{ position:absolute; left:0; top:0; width:2200px; height:6600px; }}
.room {{ background:linear-gradient(#13151c,#0f1117); border:6px solid rgba(255,255,255,0.10); border-bottom:14px solid rgba(255,255,255,0.16); border-radius:10px; }}
.ghost {{ font:900 140px {FONT}; color:rgba(255,255,255,0.055); letter-spacing:-4px; }}
.wall {{ border:10px solid rgba(255,255,255,0.12); border-radius:16px; }}
.parapet {{ background:#1a1d26; border-top:8px solid rgba(255,255,255,0.18); }}
.hut {{ background:#151821; border:6px solid rgba(255,255,255,0.12); border-radius:18px 18px 0 0; }}
.hutdoor {{ position:absolute; left:70px; bottom:0; width:140px; height:300px; background:#0b0c10; border-radius:70px 70px 0 0; }}
.street {{ background:linear-gradient(#14161d, #07080b); border-top:10px solid rgba(255,255,255,0.12); }}
#bb {{ background:#ffffff; border-radius:60px; box-shadow:0 40px 120px rgba(0,0,0,0.5); }}
#bb-posts {{ background:repeating-linear-gradient(90deg, transparent 0 250px, #2a2e3a 250px 290px); }}
.bbface {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.bbt1, .bbt2 {{ font:900 210px {FONT}; color:{INK}; line-height:0.95; letter-spacing:-6px; }}
.bbt2 {{ color:{BAD}; }}
.bbsub {{ font:700 90px {FONT}; color:#666; margin-top:20px; }}
.card {{ border-radius:40px; box-shadow:0 24px 60px rgba(0,0,0,0.45); overflow:visible; }}
.stamp {{ font:900 64px {FONT}; border:8px solid; border-radius:20px; padding:4px 22px; background:rgba(255,255,255,0.92); }}
.pill {{ font:900 50px {FONT}; padding:6px 24px; border-radius:999px; white-space:nowrap; }}
.badge {{ position:absolute; left:0; top:0; width:140px; height:140px; border-radius:50%; font:900 96px {FONT};
  color:{INK}; text-align:center; line-height:140px; }}
.htitle {{ position:absolute; left:170px; top:14px; font:900 100px {FONT}; color:#fff; letter-spacing:-2px; white-space:nowrap; }}
.doorframe {{ position:absolute; inset:0; background:#2a1c12; border-radius:200px 200px 0 0; border:14px solid #5a3b22; }}
.doorleaf {{ position:absolute; top:40px; bottom:0; left:24px; width:186px; background:linear-gradient(90deg,#8a5a34,#a06a3e);
  border-radius:150px 0 0 0; border:6px solid #5a3b22; }}
.doorleaf.r {{ left:auto; right:24px; border-radius:0 150px 0 0; }}
.counter {{ background:#d9d4c7; border-radius:16px 16px 0 0; }}
.counter-top {{ position:absolute; left:-20px; right:-20px; top:-26px; height:36px; background:#a58a5c; border-radius:12px; }}
.counter-sign {{ position:absolute; left:0; right:0; top:70px; text-align:center; font:900 72px {FONT}; color:{INK}; }}
.desktop {{ position:absolute; left:0; right:0; top:0; height:44px; background:#a07a4c; border-radius:14px; }}
.deskbody {{ position:absolute; left:30px; right:30px; top:44px; bottom:0; background:#6e5233; border-radius:0 0 12px 12px; }}
.drawer {{ position:absolute; left:80px; right:80px; top:90px; height:170px; background:#8b6840; border:6px solid #4e3a22; border-radius:12px; }}
.handle {{ position:absolute; left:50%; top:60px; width:120px; height:30px; margin-left:-60px; background:#e8d3a8; border-radius:15px; }}
.dust {{ border-radius:50%; background:#cfc7b8; opacity:0; }}
.chathead {{ height:120px; background:#1f2430; border-radius:40px 40px 0 0; display:flex; align-items:center; padding-left:40px; }}
.chathead .dot {{ width:26px; height:26px; border-radius:50%; background:{GOOD}; margin-right:20px; }}
.typing {{ position:absolute; left:40px; top:180px; background:#fff; border-radius:30px; padding:22px 30px; display:flex; gap:14px; opacity:0; }}
.typing span {{ width:22px; height:22px; border-radius:50%; background:#9aa3b2; display:block; }}
.bubble {{ position:absolute; background:#fff; border-radius:34px; padding:26px 34px; box-shadow:0 8px 24px rgba(0,0,0,0.08); }}
.ch, .qc, .pc, .cc {{ opacity:0; }}
.avatar {{ position:relative; border-radius:50%; overflow:hidden; background:#e8ecf4; }}
.over {{ position:absolute; left:0; top:0; }}
.badge .over {{ width:100%; text-align:center; }}
.ph {{ border:6px dashed rgba(255,255,255,0.25); border-radius:40px; }}
.sticker {{ border-radius:50%; background:#fff; box-shadow:0 14px 30px rgba(0,0,0,0.35); display:flex; flex-direction:column;
  align-items:center; justify-content:center; }}
.stlab {{ font:900 30px {FONT}; color:{INK}; margin-top:-4px; }}
.xdot {{ border-radius:50%; background:{BAD}; display:flex; align-items:center; justify-content:center; }}
.bubble.big {{ padding:30px 40px; box-shadow:0 20px 50px rgba(0,0,0,0.4); }}
.tail {{ position:absolute; left:120px; top:-28px; width:0; height:0; border-left:30px solid transparent; border-right:30px solid transparent; border-bottom:34px solid #fff; }}
.tail.l {{ left:-30px; top:auto; bottom:30px; border-left:none; border-bottom:24px solid transparent; border-top:24px solid transparent; border-right:34px solid #fff; }}
.sofa {{ background:#3b3f73; border-radius:60px 60px 20px 20px; border-top:60px solid #4b4f8a; }}
.lamp {{ border-left:10px solid #555a66; margin-left:40px; }}
#vc-sign {{ border-radius:30px; background:#141621; border:8px solid #3a3f55; text-align:center; font:900 96px {FONT}; line-height:114px; color:#7a809c; }}
#vc-on {{ width:100%; color:#ff4fd8; text-shadow:0 0 18px rgba(255,79,216,0.7); }}
.tape {{ position:absolute; width:48px; height:100px; border-radius:6px; box-shadow:inset 0 -18px 0 rgba(0,0,0,0.25); }}
#shelves {{ background:#3a2a1c; border-radius:16px; border:10px solid #5a4028; }}
#tv {{ background:#2a2e3a; border-radius:60px; box-shadow:0 30px 80px rgba(0,0,0,0.5); }}
#tv .screen {{ position:absolute; left:40px; top:40px; right:170px; bottom:40px; border-radius:40px; background:#0b0d14;
  display:flex; flex-direction:column; align-items:center; justify-content:center; }}
#tv .ant {{ position:absolute; top:-80px; width:10px; height:100px; background:#8b93a7; border-radius:5px; }}
#tv .a1 {{ left:330px; transform-origin:50% 100%; rotate:-25deg; }}
#tv .a2 {{ left:520px; transform-origin:50% 100%; rotate:25deg; }}
#tv .knob {{ position:absolute; right:50px; width:80px; height:80px; border-radius:50%; background:#8b93a7; }}
#tv .k1 {{ top:120px; }} #tv .k2 {{ top:260px; }}
.cbox {{ position:absolute; left:80px; right:80px; top:240px; height:250px; border-radius:40px; background:#f1f3f6;
  display:flex; align-items:center; gap:36px; padding-left:40px; }}
.cav {{ width:170px; height:170px; border-radius:50%; background:#6366f1; display:flex; align-items:center; justify-content:center; flex:none; }}
.caret {{ display:inline-block; width:10px; height:110px; background:{INK}; vertical-align:-14px; margin-left:8px; }}
.cbtn {{ position:absolute; right:80px; bottom:70px; padding:24px 70px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 100px {FONT}; }}
"""

LIB_JS = """
const tl = gsap.timeline({ paused: true });
const PIV = %s;
const Q = (id, part) => document.querySelector('#' + id + ' .' + part);
function life(id, t0, t1, seed) {
  const n = Math.max(1, Math.floor((t1 - t0) / 1.8));
  tl.fromTo(Q(id,'upper'), {scaleY:1}, {scaleY:1.03, svgOrigin:PIV.upper, duration:0.9, ease:'sine.inOut', yoyo:true, repeat:n*2-1, immediateRender:false}, t0);
  const m = Math.max(1, Math.floor((t1 - t0) / (1.4 + (seed %% 4) * 0.15)));
  tl.fromTo(Q(id,'head'), {rotation:-2.5}, {rotation:2.5, svgOrigin:PIV.head, duration:1.4 + (seed %% 4) * 0.15, ease:'sine.inOut', yoyo:true, repeat:m-1, immediateRender:false}, t0 + 0.1);
  let r = (seed * 7919) %% 997, t = t0 + 0.5 + (seed %% 5) * 0.23;
  const ey = Q(id,'eyes');
  while (t < t1 - 0.2) {
    tl.to(ey, {scaleY:0.08, svgOrigin:PIV.eyes, duration:0.06}, t);
    tl.to(ey, {scaleY:1, svgOrigin:PIV.eyes, duration:0.09}, t + 0.1);
    r = (r * 7919 + 13) %% 997; t += 2.1 + (r / 997) * 2.3;
  }
}
function walk(id, t0, t1, step) {
  const n = Math.max(2, Math.round((t1 - t0) / step));
  tl.fromTo(Q(id,'legL'), {rotation:-26}, {rotation:26, svgOrigin:PIV.legL, duration:step, ease:'sine.inOut', yoyo:true, repeat:n-1, immediateRender:false}, t0);
  tl.fromTo(Q(id,'legR'), {rotation:26}, {rotation:-26, svgOrigin:PIV.legR, duration:step, ease:'sine.inOut', yoyo:true, repeat:n-1, immediateRender:false}, t0);
  tl.fromTo(Q(id,'armL'), {rotation:24}, {rotation:-24, svgOrigin:PIV.armL, duration:step, ease:'sine.inOut', yoyo:true, repeat:n-1, immediateRender:false}, t0);
  tl.fromTo(Q(id,'armR'), {rotation:24}, {rotation:-24, svgOrigin:PIV.armR, duration:step, ease:'sine.inOut', yoyo:true, repeat:n-1, immediateRender:false}, t0);
  tl.fromTo(Q(id,'rig'), {y:0}, {y:-14, duration:step/2, ease:'sine.inOut', yoyo:true, repeat:n*2-1, immediateRender:false}, t0);
  const te = t0 + n * step;
  ['legL','legR','armL','armR'].forEach(p => tl.to(Q(id,p), {rotation:0, svgOrigin:PIV[p], duration:0.15}, te));
  tl.to(Q(id,'rig'), {y:0, duration:0.15}, te);
}
function face(id, dir, t) { tl.set(Q(id,'rig'), {scaleX:dir, svgOrigin:PIV.rig}, t); }
function jump(id, t, h) {
  tl.to(Q(id,'rig'), {keyframes:[{scaleY:0.9, y:0, duration:0.08},{scaleY:1.05, y:-h, duration:0.18, ease:'power2.out'},
    {scaleY:1, y:0, duration:0.18, ease:'power2.in'},{scaleY:0.95, duration:0.06},{scaleY:1, duration:0.08}], svgOrigin:PIV.rig}, t);
}
function point(id, side, t0, t1, ang) {
  const arm = Q(id, 'arm' + side);
  tl.to(arm, {rotation:ang, svgOrigin:PIV['arm' + side], duration:0.3, ease:'back.out(2)'}, t0);
  tl.to(arm, {rotation:0, svgOrigin:PIV['arm' + side], duration:0.35, ease:'power2.inOut'}, t1);
}
function wave(id, t0, t1) {
  const arm = Q(id, 'armR');
  tl.to(arm, {rotation:-150, svgOrigin:PIV.armR, duration:0.3, ease:'back.out(2)'}, t0);
  const n = Math.max(1, Math.floor((t1 - t0 - 0.3) / 0.28));
  tl.fromTo(arm, {rotation:-150}, {rotation:-118, svgOrigin:PIV.armR, duration:0.28, ease:'sine.inOut', yoyo:true, repeat:n-1, immediateRender:false}, t0 + 0.3);
}
function tilt(id, t) {
  tl.to(Q(id,'brows'), {y:-8, duration:0.2, ease:'back.out(3)'}, t);
  tl.to(Q(id,'brows'), {y:0, duration:0.3}, t + 1.2);
}
function typeOn(sel, t0, t1) {
  const els = document.querySelectorAll(sel);
  const dt = (t1 - t0) / Math.max(1, els.length);
  els.forEach((e, i) => tl.set(e, {opacity:1}, t0 + i * dt));
}
"""


def build_world():
    sys.modules["gen"] = sys.modules[__name__]
    import scenes
    scenes.build()
    extra_css = scenes.CSS.format(FONT=FONT, INK=INK, GOOD_BG=GOOD_BG, BAD=BAD, ACC=ACC, GOOD=GOOD)
    # partículas flotando (pantalla) para que nunca haya imagen congelada
    parts = "".join(
        f'<div class="pt" data-layout-ignore style="position:absolute;left:{(i * 137) % 1040 + 20}px;top:{(i * 263) % 1800 + 60}px;'
        f'width:{6 + i % 3 * 3}px;height:{6 + i % 3 * 3}px;border-radius:50%;background:rgba(255,255,255,{0.06 + (i % 4) * 0.03})"></div>'
        for i in range(26))
    for i in range(26):
        js(f'tl.fromTo(".pt:nth-child({i + 1})", {{y:0, x:0}}, {{y:{-120 - (i % 5) * 30}, x:{(i % 3 - 1) * 40}, '
           f'duration:{DUR:.2f}, ease:"none"}}, 0);')
    js(f'tl.fromTo("#glow", {{opacity:0.75}}, {{opacity:1, duration:2.5, ease:"sine.inOut", yoyo:true, repeat:{int(DUR / 2.5)}}}, 0);')

    html = f"""<template>
<style>{STYLE}{extra_css}</style>
<div id="root" data-composition-id="world" data-width="1080" data-height="1920" data-layout-allow-overlap data-layout-allow-overflow>
  <div id="grid" data-layout-ignore></div>
  <div id="glow" data-layout-ignore></div>
  <div id="particles" data-layout-ignore>{parts}</div>
  <div id="shake">
    <div id="wd">
      {chr(10).join(HTML)}
    </div>
  </div>
  <div id="scrim" data-layout-ignore></div>
</div>
<script>
{LIB_JS % json.dumps(PIVOT)}
{chr(10).join(JS)}
window.__timelines["world"] = tl;
</script>
</template>
"""
    os.makedirs("compositions", exist_ok=True)
    open("compositions/world.html", "w").write(html)


# ================================================================= SUBTÍTULOS
FIX = {"Ruedel": "Rue del", "guión": "guion", "que": None}
KEY_GOOD = {"curva", "reparte", "redondeadas", "solucion", "grueso", "comentarios", "igualar"}
KEY_BAD = {"rompieron", "esquina", "rompe", "rajo", "grieta", "fatiga", "concentra"}
KEY_ACC = {"1954", "comet", "reaccion", "presurizada", "globo", "infla", "desinfla", "clip", "metal", "tanque", "agua",
           "ventanita", "techo", "uno", "dos", "tres", "capas", "agujerito", "esquinas", "punto"}


def caption_groups():
    words = []
    for i, w in enumerate(WORDS):
        t = w["text"]
        if t == "Ruedel":
            t = "Rue del"
        t = t.replace("guión", "guion")
        if norm(t) == "que" and i > 0 and norm(WORDS[i - 1]["text"]) == "comenta":
            t = "qué"
        if t in ("Uno,", "Dos,", "Tres,", "Cuatro,"):
            t = t[:-1] + ":"
        words.append(dict(text=t, start=w["start"], end=w["end"], n=norm(w["text"])))
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        txt = " ".join(x["text"] for x in cur)
        brk = (nxt is None or re.search(r"[.,:;]$", w["text"]) and len(cur) >= 2 or len(cur) >= 4
               or (nxt and nxt["start"] - w["end"] > 0.3) or len(txt + " " + (nxt["text"] if nxt else "")) > 20)
        if brk:
            groups.append(cur)
            cur = []
    # agrupa sueltos de una palabra con el siguiente si caben
    out = []
    for g in groups:
        if out and len(g) == 1 and len(out[-1]) < 4 and len(" ".join(x["text"] for x in out[-1] + g)) <= 20 \
                and not re.search(r"[.:]$", out[-1][-1]["text"]):
            out[-1] = out[-1] + g
        else:
            out.append(g)
    return out


def build_captions():
    groups = caption_groups()
    items, js_ = [], []
    for gi, g in enumerate(groups):
        # palabra clave del grupo
        key = None
        for w in g:
            if w["n"] in KEY_BAD or w["n"] in KEY_GOOD or w["n"] in KEY_ACC:
                key = w
                break
        spans = []
        for wi, w in enumerate(g):
            cls = "w"
            style = ""
            if key is w:
                col = BAD if w["n"] in KEY_BAD else GOOD_BG if w["n"] in KEY_GOOD else ACC
                txtcol = "#fff" if col in (BAD, GOOD_BG) else INK
                style = f'background:{col};color:{txtcol};'
                cls += " key"
            spans.append(f'<span id="cw{gi}-{wi}" class="{cls}" style="{style}">{w["text"]}</span>')
        start = max(0.1, g[0]["start"] - 0.05)
        nxt = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else DUR
        end = min(nxt, g[-1]["end"] + 0.25)
        items.append(f'<div id="cg{gi}" class="cg">{" ".join(spans)}</div>')
        js_.append(f'tl.fromTo("#cg{gi}", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.12, ease:"power2.out"}}, {start:.3f});')
        for wi, w in enumerate(g):
            js_.append(f'tl.fromTo("#cw{gi}-{wi}", {{opacity:0.0, scale:0.7}}, {{opacity:1, scale:1, duration:0.14, '
                       f'ease:"back.out(3)"}}, {max(start, w["start"] - 0.03):.3f});')
        js_.append(f'tl.to("#cg{gi}", {{opacity:0, duration:0.1, ease:"power2.in"}}, {end - 0.1:.3f});')
        js_.append(f'tl.set("#cg{gi}", {{opacity:0, visibility:"hidden"}}, {end:.3f});')
    html = f"""<template>
<style>
#root {{ position:absolute; inset:0; }}
.cg {{ position:absolute; left:60px; right:60px; top:236px; text-align:center; font:900 72px {FONT}, sans-serif; color:#fff;
  line-height:1.25; opacity:0; text-shadow:0 6px 0 rgba(0,0,0,0.55), 0 0 30px rgba(0,0,0,0.6); }}
.w {{ display:inline-block; padding:0 6px; }}
.w.key {{ border-radius:16px; padding:0 18px; text-shadow:none; }}
</style>
<div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(items)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js_)}
window.__timelines["captions"] = tl;
</script>
</template>
"""
    open("compositions/captions.html", "w").write(html)


def build_index():
    dur = f"{DUR:.3f}"
    caps = "" if SIN_SUBS else f'''
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-start="0" data-duration="{dur}" data-track-index="2" data-track-kind="captions"
        data-width="1080" data-height="1920" style="z-index:5"></div>'''
    html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#07080b; }}
      #root {{ position:relative; width:1080px; height:1920px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
      <div id="world" data-composition-id="world" data-composition-src="compositions/world.html"
        data-start="0" data-duration="{dur}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920" style="z-index:1"></div>{caps}
      <audio id="mix" class="clip" src="assets/mezcla.wav" data-start="0" data-duration="{dur}" data-track-index="3" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open("index.html", "w").write(html)


if __name__ == "__main__":
    build_world()
    build_captions()
    build_index()
    json.dump(dict(duration=DUR, cues=sorted(SFX, key=lambda c: c["t"])), open("assets/sfx-cues.json", "w"), indent=1)
    js_all = open("compositions/world.html").read()
    rows = sorted(SYNC.values(), key=lambda r: r["empieza"])
    missing = [r for r in rows if f"{r['empieza']:.3f}" not in js_all and f"{r['empieza'] - 0.15:.3f}" not in js_all]
    json.dump(rows, open("assets/sync.json", "w"), ensure_ascii=False, indent=1)
    print(f"Sincronía: {len(rows)} anclajes a palabras · sin animación en su instante exacto: {len(missing)}")
    print(f"OK · {DUR:.2f}s · {len(JS)} tweens · {len(SFX)} efectos · subtítulos={'no' if SIN_SUBS else 'sí'}")
