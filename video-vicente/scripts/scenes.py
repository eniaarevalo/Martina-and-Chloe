"""Escenas del vídeo «¿Y si Vicente Maroto entrenara al Atlético?» (IMAGINADO). Un solo mundo: camino en zigzag
(el sofá en el campo -> lo que sabemos -> 1 · entrenamiento -> 2 · táctica -> 3 · banquillo -> 4 · partidos -> rueda de prensa -> encuesta)."""
import math
import gen as G
from gen import (P, E, js, sfx, add, card, css_box, icon, chars, type_on, roller, roll_set, roll_to, cam, shake, pop,
                 slide_in, stamp, floaty, life, GOOD, GOOD_BG, BAD, ACC, INK, FONT)
from rig import character

COLX = [40, 1100]
CW, CH = 1060, 1300
ROWS = [0, 1300, 2600, 3900, 5200]
ROAD = [r + 1272 for r in ROWS]          # el camino va por el suelo de cada fila
PURPLE = "#7c3aed"


def F(row, col):
    """Encuadre de cada parada: 960x1080, con el camino justo abajo."""
    return (COLX[col] + 50, ROWS[row] + 205, 960, 1080)


def floor(row):
    return ROWS[row] + 1262


def ROW(row):
    return (COLX[0], ROWS[row] + 150, 2120, 1150)


# ---------------------------------------------------------------- el camino (línea de tiempo)
L_X, R_X = 70, 2130
PTS = [(L_X, ROAD[0]), (R_X, ROAD[0]), (R_X, ROAD[1]), (L_X, ROAD[1]), (L_X, ROAD[2]), (R_X, ROAD[2]),
       (R_X, ROAD[3]), (L_X, ROAD[3])]
SEG = [math.dist(PTS[i], PTS[i + 1]) for i in range(len(PTS) - 1)]
TOTAL = sum(SEG)


def s_at(row, x):
    """Distancia recorrida por el camino hasta el punto x de la fila `row`."""
    s = 0
    for i in range(len(PTS) - 1):
        (x0, y0), (x1, y1) = PTS[i], PTS[i + 1]
        if y0 == y1 == ROAD[row]:
            return s + abs(x - x0)
        s += SEG[i]
    return s


def road_to(t, row, x, dur):
    js(f'tl.to("#road", {{strokeDashoffset:{TOTAL - s_at(row, x):.1f}, duration:{dur:.2f}, ease:"power2.inOut"}}, {t:.3f});')


def travel(t, rect, row, x, dur=0.8):
    """Viaje de cámara + el camino se dibuja hasta la nueva parada."""
    cam(t, rect, dur=dur)
    road_to(t, row, x, dur)


def header(hid, x, y, num, title, color=ACC, year=None, txt=INK):
    yp = (f'<div id="{hid}-yr" class="ypill">{year}</div>' if year else "")
    add(f'''<div id="{hid}" style="{css_box(x, y, 960, 150, 6)}">
      <div id="{hid}-badge" class="badge" style="background:{color};color:{txt}">{num}</div>
      <div id="{hid}-title" class="htitle">{title}</div>{yp}</div>''')


def header_in(hid, t_num, t_title, year=False):
    pop(f"#{hid}-badge", t_num, sound="pop")
    js(f'tl.fromTo("#{hid}-title", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {t_title:.3f});')
    if year:
        pop(f"#{hid}-yr", t_title + 0.15, sound=None)


def flip(sel, t, hide, show, sound="whoosh-corto", bg=None):
    js(f'tl.to("{sel}", {{scaleY:0, duration:0.14, ease:"power2.in"}}, {t:.3f});')
    for h in hide:
        js(f'tl.set("{h}", {{opacity:0}}, {t + 0.14:.3f});')
    for s in show:
        js(f'tl.set("{s}", {{opacity:1}}, {t + 0.14:.3f});')
    if bg:
        js(f'tl.set("{sel}", {{backgroundColor:"{bg}"}}, {t + 0.14:.3f});')
    js(f'tl.to("{sel}", {{scaleY:1, duration:0.26, ease:"back.out(2.2)"}}, {t + 0.14:.3f});')
    if sound:
        sfx(t, sound, 0.2)


def avatar(cid, kind, size=170):
    return (f'<div class="avatar" style="width:{size}px;height:{size}px">'
            f'{character(cid, kind, size / 2, 470 * size / 220, size / 220, z=1)}</div>')


def hold_hands(left, right, t, dur=None):
    js(f'tl.to(Q("{left}","armR"), {{rotation:-42, svgOrigin:PIV.armR, duration:0.35, ease:"back.out(2)"}}, {t:.3f});')
    js(f'tl.to(Q("{right}","armL"), {{rotation:42, svgOrigin:PIV.armL, duration:0.35, ease:"back.out(2)"}}, {t:.3f});')
    if dur:
        js(f'tl.to(Q("{left}","armR"), {{rotation:0, svgOrigin:PIV.armR, duration:0.3}}, {t + dur:.3f});')
        js(f'tl.to(Q("{right}","armL"), {{rotation:0, svgOrigin:PIV.armL, duration:0.3}}, {t + dur:.3f});')


def hearts(prefix, x, y, n, t, spread=500, rise=520, z=9):
    cols = ["#ef4444", "#f97316", "#facc15", "#22c55e", "#3b82f6", "#a855f7"]
    for i in range(n):
        hx = x + (i - (n - 1) / 2) * spread / max(1, n - 1)
        add(f'<div id="{prefix}{i}" class="heart" data-layout-ignore style="{css_box(hx - 45, y, 90, 90, z)}">'
            f'{icon("heart", 90, cols[i % 6], 2.2).replace("<svg", f"<svg fill=\"{cols[i % 6]}\"")}</div>')
        tt = t + i * 0.09
        js(f'tl.fromTo("#{prefix}{i}", {{opacity:0, y:0, scale:0.4}}, {{opacity:1, y:{-rise * 0.5:.0f}, scale:1, duration:0.5, ease:"back.out(2)"}}, {tt:.3f});')
        js(f'tl.to("#{prefix}{i}", {{y:{-rise}, x:{(i % 3 - 1) * 40}, opacity:0, duration:1.2, ease:"power1.in"}}, {tt + 0.55:.3f});')
    sfx(t, "pop2", 0.25)


# ================================================================= PIEZAS
def bubble(bid, x, y, w, who, text, col, side="l", z=8, fs=40):
    """Bocadillo de diálogo con el nombre de quien habla. Devuelve el nº de letras (para escribirlo)."""
    add(f'''<div id="{bid}" class="sb {side}" style="{css_box(x, y, w, None, z)}border-color:{col};opacity:0">
      <div class="who" style="background:{col}">{who}</div><div class="sbt" style="font-size:{fs}px">{chars(text, "kc")}</div></div>''')
    return len(text.replace(" ", ""))


def talk(cid, t0, t1):
    n = max(1, 2 * int((t1 - t0) / 0.24) - 1)
    js(f'tl.fromTo(Q("{cid}","mouth"), {{scaleY:1}}, {{scaleY:2.4, svgOrigin:"120 134", duration:0.12, yoyo:true, repeat:{n}, immediateRender:false}}, {t0:.3f});')


def say(bid, n, cid, t0, t1, from_x=0):
    js(f'tl.fromTo("#{bid}", {{opacity:0, scale:0.5, x:{from_x}}}, {{opacity:1, scale:1, x:0, duration:0.3, ease:"back.out(2)"}}, {t0 - 0.3:.3f});')
    sfx(t0 - 0.3, "pop", 0.25)
    js(f'typeOn("#{bid} .kc", {t0:.3f}, {t1:.3f});')
    talk(cid, t0, t1)


def tag_imaginado(r, x):
    add(f'<div id="ti{r}{x}" class="mile" data-layout-ignore style="{css_box(x - 260, ROAD[r] + 34, 520, 70, 2)}">CRUCE IMAGINADO</div>')


def building(bid, x, y, w, h, name, wall, win, sign_bg, sign_col, z=3):
    wins = "".join(f'<i class="win" style="left:{40 + c * ((w - 80) // 3)}px;top:{120 + r * 110}px;background:{win}"></i>'
                   for r in range(4) for c in range(3))
    add(f'''<div id="{bid}" class="bld" style="{css_box(x, y, w, h, z)}background:{wall}">
      <div class="bsign" style="background:{sign_bg};color:{sign_col}">{name}</div>{wins}<div class="bdoor"></div></div>''')


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            if (r, c) == (3, 0):
                continue
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#f97316"/><stop offset="0.5" stop-color="#db2777"/><stop offset="1" stop-color="#7c3aed"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for r, x in [(0, 1630), (1, 1630), (1, 570), (2, 570)]:
        tag_imaginado(r, x)


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            if (r, c) == (3, 0):
                continue
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#facc15"/><stop offset="0.5" stop-color="#22c55e"/><stop offset="1" stop-color="#0ea5e9"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')


def chip(cid, x, y, ic, label, bg, col, z=8, fs=46):
    add(f'<div id="{cid}" class="pill" style="{css_box(x, y, None, None, z)}background:{bg};color:{col};font-size:{fs}px;opacity:0">'
        f'{icon(ic, fs, col, 2.6)} {label}</div>')


def coins(cid, x, base, n, z=6, w=150):
    """Montón de monedas (n monedas) apoyado en y=base."""
    html = "".join(f'<i class="coin" style="bottom:{k * 26}px"></i>' for k in range(n))
    add(f'<div id="{cid}" class="coins" data-layout-ignore style="{css_box(x, base - 26 * n - 40, w, 26 * n + 40, z)}">{html}</div>')


def pram(pid, x, y, z=6, sc=1.0):
    """Carrito de bebé con el bebé dentro (ojos grandes)."""
    add(f'''<div id="{pid}" class="pram" data-layout-ignore style="{css_box(x, y, 420 * sc, 380 * sc, z)}transform-origin:50% 100%">
      <svg viewBox="0 0 420 380" width="{420 * sc:.0f}" height="{380 * sc:.0f}" style="overflow:visible">
        <path d="M60 150 Q60 70 150 60 L150 170 Z" fill="#7c3aed"/>
        <rect x="50" y="160" width="300" height="120" rx="50" fill="#a78bfa"/>
        <circle cx="210" cy="150" r="56" fill="#f6d2b4"/>
        <circle cx="190" cy="146" r="13" fill="#fff"/><circle cx="232" cy="146" r="13" fill="#fff"/>
        <circle cx="192" cy="148" r="7" fill="#16161a"/><circle cx="234" cy="148" r="7" fill="#16161a"/>
        <path d="M198 174 Q210 182 222 174" stroke="#6a2e1e" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M350 180 L390 120" stroke="#475569" stroke-width="12" stroke-linecap="round"/>
        <circle cx="110" cy="320" r="40" fill="#1f2937" stroke="#94a3b8" stroke-width="10"/>
        <circle cx="290" cy="320" r="40" fill="#1f2937" stroke="#94a3b8" stroke-width="10"/>
      </svg></div>''')


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#ef4444"/><stop offset="0.5" stop-color="#f8fafc"/><stop offset="1" stop-color="#1d4ed8"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for r, x in [(1, 1630), (1, 570), (2, 570), (2, 1630), (3, 1630)]:
        tag_imaginado(r, x)


def sofa(sid, x, y, w=420, z=4, col="#7c2d12"):
    """Sofá en dos piezas: respaldo detrás del personaje (sid) y asiento + brazos delante (sid + 'f')."""
    add(f'''<div id="{sid}" class="sofa2" data-layout-ignore style="{css_box(x, y, w, 230, 3)}opacity:0">
      <i class="sb2" style="background:{col}"></i></div>''')
    add(f'''<div id="{sid}f" class="sofa2" data-layout-ignore style="{css_box(x, y, w, 230, 7)}opacity:0">
      <i class="ss" style="background:{col}"></i>
      <i class="sa l" style="background:{col}"></i><i class="sa r" style="background:{col}"></i></div>''')


def pitch(pid, x, y, w, h, z=1):
    add(f'''<div id="{pid}" class="pitch" data-layout-ignore style="{css_box(x, y, w, h, z)}">
      <i class="pl1"></i><i class="pl2"></i></div>''')


def stripes_pill(pid, x, y, text, z=9, fs=54):
    add(f'<div id="{pid}" class="spill" style="{css_box(x, y, None, None, z)}font-size:{fs}px;opacity:0"><span>{text}</span></div>')


def ico(iid, x, y, size, name, col, z=9, fill=None, sw=2.4):
    svg = icon(name, size, col, sw)
    if fill:
        svg = svg.replace("<svg", f'<svg fill="{fill}"')
    add(f'<div id="{iid}" data-layout-ignore style="{css_box(x, y, size, size, z)}opacity:0">{svg}</div>')


# ================================================================= GANCHO: el sofá en el campo
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    pitch("pt0", fx + 0, fy + 380, 960, 700)
    sofa("sf0", fx + 270, fl - 240, 420)
    add(character("vi0", "vicente", fx + 480, fl - 30, 1.15, z=5))
    add(f'<div id="coj" class="pill" style="{css_box(fx + 250, fy + 200, None, None, 9)}background:#fff;color:{INK};font-size:56px;opacity:0">EL HOMBRE COJÍN</div>')
    stripes_pill("atl", fx + 160, fy + 300, "ATLÉTICO DE MADRID", fs=56)
    add(f'<div id="img" class="stampbox" style="{css_box(fx + 220, fy + 470, 520, 140, 11)}opacity:0;font-size:78px">IMAGINADO</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: el sofá cae en mitad del campo y Vicente aterriza encima
    js('tl.fromTo("#sf0, #sf0f", {opacity:1, y:-900, rotation:-10}, {y:0, rotation:0, duration:0.4, ease:"power3.in"}, 0);')
    js('tl.to("#sf0, #sf0f", {keyframes:[{scaleY:0.85, scaleX:1.08, duration:0.08},{scaleY:1.04, scaleX:0.98, duration:0.12},{scaleY:1, scaleX:1, duration:0.1}], transformOrigin:"50% 100%"}, 0.4);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.4, "golpe-climax", 0.5)
    shake(0.4, 22)
    js('tl.fromTo("#vi0", {opacity:1, y:-700}, {y:0, duration:0.35, ease:"power2.in"}, 0.55);')
    js('tl.to("#vi0", {keyframes:[{scaleY:0.88, duration:0.08},{scaleY:1, duration:0.12}], transformOrigin:"50% 100%"}, 0.9);')
    sfx(0.9, "pop", 0.4)
    life("vi0", 1.1, G.DUR, 1)
    t_coj, t_ent, t_atl, t_mad = P("cojin"), P("entrenado"), P("atletico"), P("madrid")
    pop("#coj", t_coj - 0.3, sound="pop2")
    js(f'tl.to(Q("vi0","eyes"), {{scaleY:0.1, svgOrigin:PIV.eyes, duration:0.15, yoyo:true, repeat:1}}, {t_coj:.3f});')
    pop("#atl", t_atl - 0.1, sound="pop")
    js(f'tl.to("#atl", {{scale:1.08, duration:0.12, yoyo:true, repeat:1}}, {t_mad:.3f});')
    stamp("#img", t_mad + 0.05, rot=-6)


# ================================================================= LO QUE SABEMOS
def scene_real():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h0", fx, fy, "✓", "LO QUE SABEMOS", color="#22c55e")
    sofa("sf1", fx + 280, fl - 240, 400)
    add(character("go1", "goya", fx + 170, fl, 1.1, z=5))
    add(character("vi1", "vicente", fx + 480, fl - 30, 1.1, z=5))
    add(character("ja1", "javier", fx + 800, fl, 1.1, z=5))
    for k, (x, n) in enumerate([(fx + 50, "GOYA"), (fx + 360, "VICENTE"), (fx + 680, "JAVIER")]):
        add(f'<div id="nt{k}" class="ntag" style="{css_box(x, fl - 40, 240, 60, 8)}opacity:0">{n}</div>')
    ico("crw", fx + 420, fy + 300, 120, "crown", "#facc15", z=9, fill="#fde047")
    add(f'<div id="rey" class="pill" style="{css_box(fx + 200, fy + 200, None, None, 9)}background:{ACC};color:{INK};font-size:48px;opacity:0">EL REY DEL SOFÁ</div>')
    t_pri, t_rea, t_vic, t_pad, t_jav, t_mar, t_goy, t_rey, t_sof = (P("primero"), P("real"), P("vicente", 2), P("padre"), P("javier"),
                                                                     P("marido"), P("goya"), P("rey"), P("sofa"))
    travel(t_pri - 0.3, F(0, 1), 0, 1630, dur=0.6)
    header_in("h0", t_pri, t_rea)
    js(f'tl.fromTo("#sf1, #sf1f", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_vic - 0.3:.3f});')
    for k, (c, t) in enumerate([("go1", t_goy - 0.1), ("vi1", t_vic), ("ja1", t_jav - 0.1)]):
        life(c, 0, G.DUR, 2 + k)
        js(f'tl.fromTo("#{c}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t:.3f});')
        js(f'tl.fromTo("#nt{k}", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t + 0.1:.3f});')
    js(f'point("vi1", "R", {t_pad:.3f}, {t_jav + 0.6:.3f}, -60);')
    js(f'point("vi1", "L", {t_mar:.3f}, {t_goy + 0.6:.3f}, 60);')
    js(f'tl.fromTo("#crw", {{opacity:0, y:-160}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_rey - 0.1:.3f});')
    sfx(t_rey + 0.2, "check", 0.35)
    pop("#rey", t_sof - 0.1, sound=None)


# ================================================================= 1 · ENTRENAMIENTO
def scene_entreno():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    header("h1", fx, fy, "1", "ENTRENAMIENTO", color="#c8102e", txt="#fff")
    pitch("pt1", fx + 0, fy + 420, 960, 660)
    for k in range(4):
        add(f'<div id="cn{k}" class="cone" data-layout-ignore style="{css_box(fx + 120 + k * 200, fy + 470, 60, 70, 3)}opacity:0"></div>')
    sofa("sf2", fx + 520, fl - 240, 400)
    add(character("vi2", "vicente", fx + 720, fl - 30, 1.1, z=5))
    add(f'<div id="blk" class="blanket" data-layout-ignore style="{css_box(fx + 620, fl - 300, 200, 140, 7)}opacity:0"></div>')
    for k, (kind, x) in enumerate([("atm", 120), ("atm2", 330)]):
        add(f'<div id="pw{k}" data-layout-ignore style="{css_box(fx + x - 130, fl - 260, 260, 260, 5)}opacity:0">'
            f'<div class="lie">{character(f"pl{k}", kind, 130, 250, 0.55, z=1)}</div></div>')
    for k, (x, y) in enumerate([(120, 600), (330, 560), (700, 420)]):
        add(f'<div id="zz{k}" class="zz" data-layout-ignore style="{css_box(fx + x, fy + y, 140, 90, 10)}opacity:0">Zzz</div>')
    add(f'<div id="nor" class="stampbox" style="{css_box(fx + 140, fy + 250, 380, 120, 11)}opacity:0;font-size:64px">¿CORRER?</div>')
    t_uno, t_ent, t_cor, t_ses, t_man, t_sie = P("uno"), P("entrenamientos"), P("correr"), P("sesion"), P("mantita"), P("siesta")
    travel(t_uno - 0.3, F(1, 1), 1, 1630, dur=0.7)
    header_in("h1", t_uno, t_ent)
    for k in range(4):
        js(f'tl.fromTo("#cn{k}", {{opacity:0, y:-60}}, {{opacity:1, y:0, duration:0.3, ease:"bounce.out"}}, {t_ent + k * 0.1:.3f});')
    stamp("#nor", t_cor - 0.2, rot=-8)
    js(f'tl.to("#cn0, #cn1, #cn2, #cn3", {{rotation:90, y:30, duration:0.3, stagger:0.06}}, {t_cor + 0.3:.3f});')
    js(f'tl.to("#nor", {{opacity:0, duration:0.25}}, {t_ses - 0.2:.3f});')
    js(f'tl.fromTo("#sf2, #sf2f", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_ses - 0.1:.3f});')
    js(f'tl.fromTo("#vi2", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.35, ease:"power2.in"}}, {t_ses + 0.1:.3f});')
    life("vi2", 0, G.DUR, 5)
    sfx(t_ses + 0.45, "pop", 0.3)
    for k in range(2):
        js(f'tl.fromTo("#pw{k}", {{opacity:0, y:-40}}, {{opacity:1, y:0, duration:0.35}}, {t_man - 0.2 + k * 0.15:.3f});')
    js(f'tl.fromTo("#blk", {{opacity:0, scaleY:0.2, transformOrigin:"50% 0%"}}, {{opacity:1, scaleY:1, duration:0.35}}, {t_man:.3f});')
    sfx(t_man, "papel", 0.3)
    js(f'tl.to(Q("vi2","eyes"), {{scaleY:0.08, svgOrigin:PIV.eyes, duration:0.2}}, {t_sie:.3f}); tl.to(Q("vi2","head"), {{rotation:14, svgOrigin:PIV.head, duration:0.4}}, {t_sie:.3f});')
    for k in range(3):
        js(f'tl.fromTo("#zz{k}", {{opacity:0, y:30, scale:0.5}}, {{opacity:1, y:-40, scale:1, duration:0.7, repeat:1}}, {t_sie + k * 0.2:.3f});')


# ================================================================= 2 · LA TÁCTICA
def scene_tactica():
    fx, fy, fw, fh = F(1, 0)
    header("h2", fx, fy, "2", "LA TÁCTICA", color="#1d4ed8", txt="#fff")
    pos = [(150, 440), (330, 300), (330, 580), (540, 360), (540, 540), (720, 440)]
    dots = "".join(f'<i class="dot" id="dt{k}" style="left:{x - 30}px;top:{y - 30}px"></i>' for k, (x, y) in enumerate(pos))
    path = [0, 1, 3, 2, 4, 1, 3, 5]
    segs = "".join(f'<line id="ps{k}" x1="{pos[a][0]}" y1="{pos[a][1]}" x2="{pos[b][0]}" y2="{pos[b][1]}" stroke="#facc15" stroke-width="10" stroke-linecap="round" stroke-dasharray="14 12"/>'
                   for k, (a, b) in enumerate(zip(path, path[1:])))
    add(f'''<div id="brd" class="board" style="{css_box(fx + 40, fy + 300, 880, 720, 4)}opacity:0">
      <svg viewBox="0 0 880 720" width="880" height="720" style="position:absolute;left:0;top:0">{segs}</svg>{dots}
      <div id="bsf" class="bsofa">{icon("sofa", 110, "#fff", 2.4)}</div></div>''')
    add(f'<div id="sab" class="pill" style="{css_box(fx + 180, fy + 190, None, None, 10)}background:{GOOD_BG};color:#fff;font-size:52px;opacity:0">'
        f'{icon("check", 50, "#fff", 3)} SABE DE FÚTBOL</div>')
    stripes_pill("tt", fx + 280, fy + 190, "TIKI TAKA", z=11, fs=64)
    t_dos, t_tac, t_equ, t_sab, t_fut, t_tik, t_lev, t_sof = P("dos"), P("tactica"), P("equivoque"), P("sabe"), P("futbol"), P("tiki"), P("levantarse"), P("sofa", 3)
    travel(t_dos - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h2", t_dos, t_tac)
    slide_in("#brd", t_tac + 0.1, dy=60)
    js('tl.set(".dot", {scale:0}, 0);')
    js(f'tl.to(".dot", {{scale:1, duration:0.25, stagger:0.06, ease:"back.out(3)"}}, {t_equ:.3f});')
    pop("#sab", t_sab - 0.1, sound="check")
    js(f'tl.to("#sab", {{opacity:0, duration:0.25}}, {t_tik - 0.4:.3f});')
    stamp("#tt", t_tik - 0.2, rot=-4)
    n = len(path) - 1
    js('tl.set("[id^=ps]", {opacity:0}, 0);')
    for k in range(n):
        tt = t_tik + 0.2 + (t_lev - t_tik) * k / n
        js(f'tl.fromTo("#ps{k}", {{opacity:0}}, {{opacity:1, duration:0.12}}, {tt:.3f}); tl.to("#dt{path[k + 1]}", {{scale:1.3, duration:0.1, yoyo:true, repeat:1}}, {tt:.3f});')
        sfx(tt, "click", 0.15)
    js(f'tl.fromTo("#bsf", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2.5)"}}, {t_sof - 0.3:.3f});')
    js(f'tl.to("#tt", {{y:-10, duration:0.15, yoyo:true, repeat:1}}, {t_sof:.3f});')
    sfx(t_sof, "pop2", 0.3)


# ================================================================= 3 · EL BANQUILLO
def scene_banquillo():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h3", fx, fy, "3", "EL BANQUILLO", color="#c8102e", txt="#fff")
    add(f'''<div id="bnc" class="bench2" data-layout-ignore style="{css_box(fx + 180, fl - 330, 600, 320, 3)}opacity:0">
      <i class="roof"></i><i class="seat"></i><i class="lg l"></i><i class="lg r"></i></div>''')
    sofa("sf3", fx + 230, fl - 240, 500, col="#b91c1c")
    add(f'<div id="foot" class="footr" data-layout-ignore style="{css_box(fx + 740, fl - 110, 160, 100, 4)}opacity:0"></div>')
    add(character("vi3", "vicente", fx + 480, fl - 30, 1.15, z=5))
    add(f'<div id="rep" class="pill" style="{css_box(fx + 520, fy + 300, None, None, 10)}background:#fff;color:{INK};font-size:46px;opacity:0">+ REPOSAPIÉS</div>')
    t_tre, t_ban, t_ped, t_cam, t_sof, t_rep = P("tres"), P("banquillo"), P("pediria"), P("cambiarlo"), P("sofa", 4), P("reposapies")
    travel(t_tre - 0.3, F(2, 0), 2, 570, dur=0.7)
    header_in("h3", t_tre, t_ban)
    js(f'tl.fromTo("#bnc", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_ban:.3f});')
    js(f'tl.fromTo("#vi3", {{opacity:0, x:-300}}, {{opacity:1, x:0, duration:0.4}}, {t_ped - 0.2:.3f});')
    life("vi3", 0, G.DUR, 6)
    js(f'point("vi3", "R", {t_cam - 0.1:.3f}, {t_sof + 0.4:.3f}, -60);')
    # el banquillo se convierte en sofá
    js(f'tl.to("#bnc", {{scaleY:0, opacity:0, transformOrigin:"50% 100%", duration:0.3}}, {t_sof - 0.2:.3f});')
    js(f'tl.fromTo("#sf3, #sf3f", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_sof:.3f});')
    sfx(t_sof, "whoosh-corto", 0.3)
    js(f'tl.fromTo("#foot", {{opacity:0, x:120}}, {{opacity:1, x:0, duration:0.35, ease:"back.out(2)"}}, {t_rep - 0.1:.3f});')
    pop("#rep", t_rep, sound="check")
    js(f'jump("vi3", {t_rep + 0.2:.3f}, 30);')


# ================================================================= 4 · LOS PARTIDOS
def scene_partidos():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h4", fx, fy, "4", "LOS PARTIDOS", color="#1d4ed8", txt="#fff")
    pitch("pt4", fx + 0, fy + 420, 960, 660)
    add(f'<div id="gol" class="goal" data-layout-ignore style="{css_box(fx + 250, fl - 330, 460, 300, 3)}opacity:0"></div>')
    for k, (kind, x) in enumerate([("atm", 200), ("atm2", 420), ("atm", 640)]):
        add(f'<div id="dw{k}" data-layout-ignore style="{css_box(fx + x - 130, fl - 240, 260, 260, 5)}opacity:0">'
            f'<div class="lie">{character(f"df{k}", kind, 130, 250, 0.55, z=1)}</div></div>')
    rr1, h1 = roller("sr1", "1", 130, INK)
    rr2, h2 = roller("sr2", "1", 130, INK)
    add(f'''<div id="sco" class="card" style="{css_box(fx + 180, fy + 190, 600, 220, 8)}background:#fff;opacity:0">
      <div class="sct l">ATLÉTICO</div><div class="sct r">RIVAL</div>
      <div class="scn">{rr1}<span>–</span>{rr2}</div></div>''')
    add(f'<div id="cero" class="stampbox" style="{css_box(fx + 330, fy + 430, 300, 140, 11)}opacity:0;font-size:90px">0–0</div>')
    t_cua, t_par, t_fam, t_def, t_tum, t_emp, t_cer = P("cuatro"), P("partidos"), P("famoso"), P("defender"), P("tumbado"), P("empatar"), P("cero")
    travel(t_cua - 0.3, F(2, 1), 2, 1630, dur=0.6)
    header_in("h4", t_cua, t_par)
    js(f'tl.fromTo("#gol", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_par:.3f});')
    slide_in("#sco", t_fam - 0.2, dy=-60)
    roll_set("sr1", "1", h1)
    roll_set("sr2", "1", h2)
    for k in range(3):
        js(f'tl.fromTo("#dw{k}", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.35, ease:"bounce.out"}}, {t_def + k * 0.12:.3f});')
    sfx(t_def + 0.2, "golpe", 0.3)
    js(f'tl.to("[id^=dw]", {{x:8, duration:0.1, yoyo:true, repeat:5}}, {t_tum:.3f});')
    roll_to("sr1", "0", h1, t_emp, dur=0.5, spins=0)
    roll_to("sr2", "0", h2, t_emp + 0.1, dur=0.5, spins=0)
    stamp("#cero", t_cer - 0.1, rot=-8)


# ================================================================= RUEDA DE PRENSA
def scene_prensa():
    fx, fy, fw, fh = F(3, 1)
    fl = floor(3)
    add(f'<div id="bkdr" class="backdrop" data-layout-ignore style="{css_box(fx + 40, fy + 180, 880, 600, 2)}opacity:0"></div>')
    sofa("sf5", fx + 270, fl - 240, 420)
    add(character("vi5", "vicente", fx + 480, fl - 30, 1.15, z=5))
    add(f'<div id="tbl" class="ptable" data-layout-ignore style="{css_box(fx + 200, fl - 140, 560, 130, 7)}opacity:0"></div>')
    for k, x in enumerate([300, 430, 560]):
        ico(f"mc{k}", fx + x, fl - 240, 100, "mic", "#e2e8f0", z=8)
    for k, (x, y) in enumerate([(80, 240), (780, 300), (120, 520), (760, 560)]):
        add(f'<div id="fs{k}" class="flash" data-layout-ignore style="{css_box(fx + x, fy + y, 110, 110, 10)}opacity:0"></div>')
    nq = bubble("sbq", fx + 60, fy + 200, 840, "VICENTE", "«Tiki taka, toque y toque… y luego, una siesta».", "#c8102e", "c", fs=50)
    add(f'<div id="zq" class="zz" data-layout-ignore style="{css_box(fx + 640, fy + 520, 140, 90, 10)}opacity:0">Zzz</div>')
    t_rue, t_pre, t_cla, t_tik, t_toq, t_sie = P("rueda"), P("prensa"), P("claro"), P("tiki", 2), P("toque"), P("siesta", 2)
    travel(t_rue - 0.4, F(3, 1), 3, 1630, dur=0.6)
    js(f'tl.fromTo("#bkdr", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_rue - 0.1:.3f});')
    js(f'tl.fromTo("#sf5, #sf5f, #vi5", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_rue:.3f});')
    life("vi5", 0, G.DUR, 7)
    js(f'tl.fromTo("#tbl", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.3}}, {t_pre - 0.1:.3f});')
    for k in range(3):
        js(f'tl.fromTo("#mc{k}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.25, ease:"back.out(2)"}}, {t_pre + k * 0.08:.3f});')
    for k in range(4):
        js(f'tl.fromTo("#fs{k}", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1.2, duration:0.08, yoyo:true, repeat:1}}, {t_pre + 0.2 + k * 0.22:.3f});')
        js(f'tl.fromTo("#fs{k}", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1.2, duration:0.08, yoyo:true, repeat:1, immediateRender:false}}, {t_cla + 0.2 + k * 0.18:.3f});')
    sfx(t_pre + 0.2, "click", 0.3)
    sfx(t_cla + 0.2, "click", 0.3)
    say("sbq", nq, "vi5", t_tik, E("siesta", 2), from_x=0)
    js(f'tl.to(Q("vi5","armR"), {{rotation:-50, svgOrigin:PIV.armR, duration:0.2, yoyo:true, repeat:3}}, {t_toq:.3f});')
    js(f'tl.to(Q("vi5","eyes"), {{scaleY:0.08, svgOrigin:PIV.eyes, duration:0.2}}, {t_sie + 0.2:.3f}); tl.to(Q("vi5","head"), {{rotation:14, svgOrigin:PIV.head, duration:0.4}}, {t_sie + 0.2:.3f});')
    js(f'tl.fromTo("#zq", {{opacity:0, y:30}}, {{opacity:1, y:-40, duration:0.6}}, {t_sie + 0.3:.3f});')


# ================================================================= ENCUESTA
OPTS = [("SÍ", "#22c55e"), ("NO", "#ef4444"), ("SOLO PARA EL SOFÁ", "#f59e0b")]


def scene_final():
    fx, fy, fw, fh = F(3, 0)
    rows = "".join(f'<div class="poll" style="top:{150 + k * 100}px"><span>{n}</span><i id="pb{k}" style="background:{c}"></i></div>'
                   for k, (n, c) in enumerate(OPTS))
    add(f'''<div id="pollc" class="card" style="{css_box(fx + 40, fy + 220, 880, 500, 6)}background:#fff;opacity:0">
      <div class="polh">{icon("message-circle", 54, INK, 2.6)} ¿LO FICHARÍAS?</div>{rows}</div>''')
    cta = "Yo lo ficharía para…"
    add(f'''<div id="cbx" class="card" style="{css_box(fx + 40, fy + 760, 880, 170, 6)}background:#fff;opacity:0">
      <div id="ctt" class="ctt">{chars(cta, "kc")}</div><div id="pub" class="pubb">Publicar</div></div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 800, fy + 880, 90, 90, 12)}opacity:0">{icon("mouse-pointer-2", 90, "#fff", 2.4).replace("<svg", "<svg fill=\"#0f1115\"")}</div>')
    t_fic, t_equ, t_leo, t_com = P("ficharias"), P("equipo"), P("leo"), P("comentarios")
    travel(t_fic - 0.45, F(3, 0), 3, 570, dur=0.6)
    slide_in("#pollc", t_fic - 0.2, dy=-60)
    js('tl.set("[id^=pb]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    for k, w in enumerate([0.75, 0.3, 0.9]):
        js(f'tl.to("#pb{k}", {{scaleX:{w}, duration:0.35, ease:"back.out(1.6)"}}, {t_equ - 0.2 + k * 0.12:.3f});')
    sfx(t_equ, "pop2", 0.25)
    slide_in("#cbx", t_equ + 0.2, dy=60, sound=None)
    type_on("#ctt .kc", len(cta), t_leo - 0.2, t_com + 0.3)
    js(f'tl.fromTo("#cur", {{opacity:0, x:160, y:160}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.4:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.4:.3f});')
    sfx(t_com + 0.4, "click", 0.5)
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 42px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.htitle {{ font-size:80px; top:26px; }}
.stampbox {{ font:900 100px {FONT}; color:{BAD}; border:12px solid {BAD}; border-radius:26px; background:rgba(255,255,255,0.94);
  display:flex; align-items:center; justify-content:center; letter-spacing:-2px; white-space:nowrap; }}
.ntag {{ border-radius:14px; background:#0f172a; border:4px solid #fff; color:#fff; font:900 34px {FONT}; text-align:center; line-height:52px; white-space:nowrap; }}
.pitch {{ border-radius:30px; background:repeating-linear-gradient(90deg,#15803d 0 120px,#16a34a 120px 240px); opacity:0.55; }}
.pitch .pl1 {{ position:absolute; left:50%; top:0; bottom:0; width:8px; margin-left:-4px; background:rgba(255,255,255,0.7); }}
.pitch .pl2 {{ position:absolute; left:50%; top:50%; width:220px; height:220px; margin:-110px 0 0 -110px; border:8px solid rgba(255,255,255,0.7); border-radius:50%; }}
.sofa2 .sb2 {{ position:absolute; left:30px; right:30px; top:0; height:130px; border-radius:40px 40px 10px 10px; filter:brightness(1.15); }}
.sofa2 .ss {{ position:absolute; left:10px; right:10px; top:110px; height:90px; border-radius:24px; }}
.sofa2 .sa {{ position:absolute; top:70px; width:70px; height:140px; border-radius:30px; filter:brightness(0.85); }}
.sofa2 .sa.l {{ left:0; }} .sofa2 .sa.r {{ right:0; }}
.spill {{ border-radius:999px; padding:6px 30px; background:repeating-linear-gradient(90deg,#c8102e 0 40px,#ffffff 40px 80px); border:6px solid #1d4ed8; white-space:nowrap; }}
.spill span {{ font-weight:900; color:#fff; -webkit-text-stroke:3px #1d4ed8; paint-order:stroke fill; letter-spacing:-1px; }}
.cone {{ clip-path:polygon(50% 0, 100% 100%, 0 100%); background:linear-gradient(#fb923c,#ea580c); }}
.blanket {{ border-radius:20px; background:repeating-linear-gradient(45deg,#a78bfa 0 20px,#c4b5fd 20px 40px); }}
.lie {{ position:absolute; left:0; top:0; width:260px; height:260px; transform:rotate(-90deg); transform-origin:50% 50%; }}
.zz {{ font:900 70px {FONT}; color:#a5b4fc; text-align:center; }}
.board {{ border-radius:30px; background:#065f46; border:12px solid #e2e8f0; overflow:hidden; }}
.dot {{ position:absolute; width:60px; height:60px; border-radius:50%; background:#c8102e; border:6px solid #fff; }}
.bsofa {{ position:absolute; right:40px; bottom:40px; width:150px; height:150px; border-radius:30px; background:#7c2d12; display:flex; align-items:center; justify-content:center; opacity:0; }}
.bench2 .roof {{ position:absolute; left:0; right:0; top:0; height:150px; border-radius:30px 30px 0 0; background:rgba(186,230,253,0.35); border:8px solid #94a3b8; }}
.bench2 .seat {{ position:absolute; left:20px; right:20px; top:210px; height:40px; border-radius:12px; background:#64748b; }}
.bench2 .lg {{ position:absolute; top:150px; width:16px; height:170px; background:#94a3b8; }}
.bench2 .lg.l {{ left:20px; }} .bench2 .lg.r {{ right:20px; }}
.footr {{ border-radius:24px; background:#991b1b; }}
.goal {{ border:12px solid #f8fafc; border-bottom:none; border-radius:10px 10px 0 0;
  background:repeating-linear-gradient(0deg, rgba(255,255,255,0.15) 0 3px, transparent 3px 30px), repeating-linear-gradient(90deg, rgba(255,255,255,0.15) 0 3px, transparent 3px 30px); }}
.sct {{ position:absolute; top:20px; width:50%; text-align:center; font:900 40px {FONT}; color:#475569; }}
.sct.l {{ left:0; color:#c8102e; }} .sct.r {{ right:0; }}
.scn {{ position:absolute; left:0; right:0; top:70px; text-align:center; }}
.scn span {{ font:900 110px {FONT}; color:#94a3b8; margin:0 40px; vertical-align:top; }}
.backdrop {{ border-radius:24px; background:repeating-linear-gradient(45deg,#c8102e 0 60px,#b91c1c 60px 120px); opacity:0.35; }}
.ptable {{ border-radius:16px; background:#1e293b; border-top:10px solid #475569; }}
.flash {{ border-radius:50%; background:radial-gradient(circle,#fff,rgba(255,255,255,0) 70%); }}
.sb {{ background:#fff; border:7px solid; border-radius:36px; padding:54px 30px 26px; box-shadow:0 18px 40px rgba(0,0,0,0.45); }}
.sb:after {{ content:""; position:absolute; bottom:-34px; width:0; height:0; border-left:24px solid transparent; border-right:24px solid transparent; border-top:34px solid #fff; }}
.sb.l:after {{ left:90px; }} .sb.r:after {{ right:110px; }} .sb.c:after {{ left:50%; margin-left:-24px; }}
.who {{ position:absolute; left:26px; top:-30px; padding:4px 22px; border-radius:999px; color:#fff; font:900 38px {FONT}; white-space:nowrap; }}
.sbt {{ font-weight:900; color:{INK}; line-height:1.15; text-align:center; }}
.kc {{ opacity:0; }}
.polh svg {{ flex:none; }}
.polh {{ position:absolute; left:40px; right:40px; top:40px; display:flex; align-items:center; gap:18px; font:900 50px {FONT}; color:{INK}; white-space:nowrap; }}
.poll {{ position:absolute; left:40px; right:40px; height:76px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:420px; flex:none; font:900 42px {FONT}; color:{INK}; white-space:nowrap; }}
.poll i {{ flex:1; height:44px; border-radius:22px; }}
.ctt {{ position:absolute; left:40px; top:52px; font:800 50px {FONT}; color:{INK}; white-space:nowrap; }}
.pubb {{ position:absolute; right:30px; top:40px; padding:12px 40px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 56px {FONT}; }}
"""


def build():
    world()
    scene_hook()
    scene_real()
    scene_entreno()
    scene_tactica()
    scene_banquillo()
    scene_partidos()
    scene_prensa()
    scene_final()
