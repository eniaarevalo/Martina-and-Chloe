"""Escenas del vídeo «¿Y si Estela Reynolds hubiera triunfado?» (IMAGINADO). Un solo mundo: camino en zigzag
(alfombra roja -> lo que sabemos -> 1 · culebrón -> 2 · villana -> 3 · Hollywood -> 4 · el premio -> la crítica -> encuesta)."""
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


def title_card(tid, x, y, w, top, title, col, z=8, fs=60):
    add(f'''<div id="{tid}" class="tcard" style="{css_box(x, y, w, None, z)}border-color:{col};opacity:0">
      <div class="tct" style="color:{col}">{top}</div><div class="tcn" style="font-size:{fs}px">{title}</div></div>''')


# ================================================================= GANCHO: la alfombra roja
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    add(f'<div id="cone" class="cone2" data-layout-ignore style="{css_box(fx + 230, fy + 150, 500, 930, 2)}opacity:0"></div>')
    add(f'<div id="rug" class="rug" data-layout-ignore style="{css_box(fx + 330, fl - 40, 300, 60, 3)}"></div>')
    add(character("es0", "estela", fx + 480, fl - 20, 1.25, z=6))
    for k, (x, y) in enumerate([(150, 330), (760, 380), (250, 640), (700, 680)]):
        ico(f"sp{k}", fx + x, fy + y, 90, "sparkles", "#fde047", z=7, fill="#fef08a")
    ico("str", fx + 400, fy + 180, 160, "star", "#facc15", z=9, fill="#fde047")
    add(f'<div id="img" class="stampbox" style="{css_box(fx + 220, fy + 360, 520, 140, 11)}opacity:0;font-size:78px">IMAGINADO</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: se enciende el foco, la alfombra roja se desenrolla y aparece Estela posando
    js('tl.fromTo("#cone", {opacity:0}, {opacity:1, duration:0.15}, 0.05);')
    sfx(0.05, "click", 0.5)
    js('tl.fromTo("#rug", {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:0.4, ease:"power3.out"}, 0.15);')
    js('tl.fromTo("#es0", {opacity:0, scale:0.6, transformOrigin:"50% 100%"}, {opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}, 0.3);')
    sfx(0.3, "whoosh", 0.35)
    js('tl.to(Q("es0","armR"), {rotation:-150, svgOrigin:PIV.armR, duration:0.3, ease:"back.out(2)"}, 0.7);')
    for k in range(4):
        js(f'tl.fromTo("#sp{k}", {{opacity:0, scale:0.3, rotation:-40}}, {{opacity:1, scale:1, rotation:0, duration:0.3, ease:"back.out(3)"}}, {0.5 + k * 0.1:.2f});')
        js(f'tl.to("#sp{k}", {{scale:0.7, duration:0.4, yoyo:true, repeat:5}}, {0.9 + k * 0.1:.2f});')
    sfx(0.5, "pop2", 0.3)
    life("es0", 0.8, G.DUR, 1)
    t_est, t_con = P("estrella"), P("conseguido")
    js(f'tl.fromTo("#str", {{opacity:0, scale:0.2, rotation:-90}}, {{opacity:1, scale:1, rotation:0, duration:0.45, ease:"back.out(2.5)"}}, {t_est - 0.2:.3f});')
    sfx(t_est, "check", 0.35)
    stamp("#img", t_con + 0.1, rot=-6)


# ================================================================= LO QUE SABEMOS
def scene_real():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h0", fx, fy, "✓", "LO QUE SABEMOS", color="#22c55e")
    building("mp", fx + 620, fy + 400, 300, 600, "MONTEPINAR", "#e2e8f0", "#38bdf8", "#0f766e", "#fff", z=3)
    add(character("es1", "estela", fx + 300, fl, 1.2, z=6))
    add(f'<div id="div" class="pill" style="{css_box(fx + 60, fy + 190, None, None, 9)}background:#ca8a04;color:#fff;font-size:50px;opacity:0">'
        f'{icon("crown", 48, "#fff", 2.6)} LA DIVA DEL EDIFICIO</div>')
    nq = bubble("sbq", fx + 40, fy + 300, 560, "ESTELA", "¡Qué ataque más gratuito!", "#ca8a04", "l", fs=56)
    t_pri, t_rea, t_mon, t_div, t_fra, t_que = P("primero"), P("real"), P("montepinar"), P("diva"), P("frase"), P("que", 2)
    travel(t_pri - 0.3, F(0, 1), 0, 1630, dur=0.6)
    header_in("h0", t_pri, t_rea)
    js(f'tl.fromTo("#mp", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_mon - 0.2:.3f});')
    js(f'tl.fromTo("#es1", {{opacity:0, x:-120}}, {{opacity:1, x:0, duration:0.4, ease:"back.out(2)"}}, {t_mon + 0.3:.3f});')
    life("es1", 0, G.DUR, 2)
    pop("#div", t_div - 0.1, sound="pop2")
    js(f'tl.to("#div", {{opacity:0, duration:0.25}}, {t_fra:.3f});')
    say("sbq", nq, "es1", t_que, E("gratuito"), from_x=-40)
    js(f'tl.to(Q("es1","armL"), {{rotation:70, svgOrigin:PIV.armL, duration:0.25, ease:"back.out(2)"}}, {t_que:.3f}); tl.to(Q("es1","armL"), {{rotation:0, svgOrigin:PIV.armL, duration:0.3}}, {E("gratuito") + 0.4:.3f});')
    js(f'tl.to(Q("es1","head"), {{rotation:-12, svgOrigin:PIV.head, duration:0.2, yoyo:true, repeat:1}}, {E("gratuito") - 0.2:.3f});')
    sfx(t_que, "golpe", 0.3)


# ================================================================= 1 · EL CULEBRÓN
def scene_culebron():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    header("h1", fx, fy, "1", "EL CULEBRÓN", color="#db2777", txt="#fff")
    add(f'''<div id="tv" class="tvset" style="{css_box(fx + 420, fy + 260, 500, 400, 4)}opacity:0">
      <div class="tvs"><div id="tvt" class="tvt">PASIÓN EN<br>TORREVIEJA</div></div><i class="tvl"></i><i class="tvr"></i></div>''')
    add(character("es2", "estela", fx + 220, fl, 1.15, z=6))
    for k, (x, y) in enumerate([(470, 300), (820, 330), (620, 250)]):
        ico(f"ht{k}", fx + x, fy + y, 80, "heart", "#ef4444", z=8, fill="#fca5a5")
    add(f'<div id="prt" class="pill" style="{css_box(fx + 450, fy + 700, None, None, 9)}background:#db2777;color:#fff;font-size:44px;opacity:0">PROTAGONISTA</div>')
    t_uno, t_pri, t_pro, t_cul, t_sob, t_pas, t_tor = P("uno"), P("primer"), P("protagonista"), P("culebron"), P("sobremesa"), P("pasion"), P("torrevieja")
    travel(t_uno - 0.3, F(1, 1), 1, 1630, dur=0.7)
    header_in("h1", t_uno, t_pri)
    js(f'tl.fromTo("#es2", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_pri:.3f});')
    life("es2", 0, G.DUR, 3)
    pop("#prt", t_pro - 0.1, sound="pop2")
    js(f'tl.fromTo("#tv", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_cul - 0.2:.3f});')
    js('tl.set("#tvt", {opacity:0}, 0);')
    js(f'tl.fromTo("#tvt", {{opacity:0, scale:1.4}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_pas - 0.1:.3f});')
    sfx(t_pas, "golpe", 0.3)
    for k in range(3):
        js(f'tl.fromTo("#ht{k}", {{opacity:0, scale:0.3, y:30}}, {{opacity:1, scale:1, y:-20, duration:0.4, ease:"back.out(2.5)"}}, {t_tor + k * 0.12:.3f});')
    js(f'tl.to(Q("es2","armR"), {{rotation:-120, svgOrigin:PIV.armR, duration:0.3, ease:"back.out(2)"}}, {t_tor:.3f}); tl.to(Q("es2","head"), {{rotation:-15, svgOrigin:PIV.head, duration:0.3}}, {t_tor:.3f});')


# ================================================================= 2 · LA VILLANA
def scene_villana():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    header("h2", fx, fy, "2", "LA VILLANA", color="#7c3aed", txt="#fff")
    title_card("ttm", fx + 400, fy + 220, 520, "SERIE DE ÉPOCA", "LA MARQUESA<br>DE MONTEPINAR", "#7c3aed", fs=54)
    add(character("es3", "estela", fx + 260, fl, 1.2, z=6))
    ico("crn", fx + 200, fl - 640, 130, "crown", "#facc15", z=8, fill="#fde047")
    add(f'<div id="fan" class="fan" data-layout-ignore style="{css_box(fx + 330, fl - 420, 220, 130, 8)}opacity:0"></div>')
    add(f'<div id="mal" class="stampbox" style="{css_box(fx + 470, fy + 560, 420, 140, 11)}opacity:0;font-size:80px">MALVADA</div>')
    t_dos, t_vil, t_epo, t_mar, t_aba, t_tod = P("dos"), P("villana"), P("epoca"), P("marquesa"), P("abanico"), P("todo")
    travel(t_dos - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h2", t_dos, t_vil)
    js(f'tl.fromTo("#es3", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_vil:.3f});')
    life("es3", 0, G.DUR, 4)
    slide_in("#ttm", t_epo - 0.2, dx=80, dy=0)
    js(f'tl.fromTo("#crn", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_mar - 0.1:.3f});')
    sfx(t_mar + 0.3, "check", 0.3)
    js(f'tl.fromTo("#fan", {{opacity:0, scaleX:0.1, transformOrigin:"0% 100%"}}, {{opacity:1, scaleX:1, duration:0.3, ease:"back.out(2)"}}, {t_aba - 0.1:.3f});')
    js(f'tl.to("#fan", {{rotation:-15, transformOrigin:"0% 100%", duration:0.15, yoyo:true, repeat:5}}, {t_aba + 0.25:.3f});')
    js(f'tl.to(Q("es3","armR"), {{rotation:-70, svgOrigin:PIV.armR, duration:0.25}}, {t_aba - 0.1:.3f});')
    sfx(t_aba, "whoosh-corto", 0.25)
    stamp("#mal", t_tod - 0.2, rot=-8)


# ================================================================= 3 · HOLLYWOOD
def scene_hollywood():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h3", fx, fy, "3", "HOLLYWOOD", color="#f59e0b")
    add(f'''<div id="hill" class="hill" data-layout-ignore style="{css_box(fx + 0, fy + 170, 960, 280, 2)}opacity:0">
      <div class="hws">{"".join(f'<b>{c}</b>' for c in "HOLLYWOOD")}</div></div>''')
    add(character("es4", "estela", fx + 200, fl, 1.2, z=6))
    for k, (x, y) in enumerate([(560, 830), (680, 760), (800, 830)]):
        ico(f"fl{k}", fx + x, fy + y, 130, "flame", "#f97316", z=5, fill="#fdba74")
    ico("clk", fx + 780, fy + 620, 140, "clapperboard", "#f8fafc", z=7)
    nb = bubble("sbh", fx + 360, fy + 470, 560, "ESTELA", "«Oh my God… ¡qué ataque!»", "#f59e0b", "l", fs=52)
    for k, (x, y) in enumerate([(380, 700), (480, 760)]):
        add(f'<div id="qm{k}" class="qmk" data-layout-ignore style="{css_box(fx + x, fy + y, 100, 120, 10)}opacity:0">?</div>')
    t_tre, t_sal, t_hol, t_acc, t_ing, t_nad = P("tres"), P("salto"), P("hollywood"), P("accion"), P("ingles"), P("nadie")
    travel(t_tre - 0.3, F(2, 0), 2, 570, dur=0.7)
    header_in("h3", t_tre, t_sal)
    js(f'tl.fromTo("#hill", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_hol - 0.3:.3f});')
    js(f'tl.fromTo(".hws b", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.2, stagger:0.05}}, {t_hol - 0.2:.3f});')
    js(f'tl.fromTo("#es4", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_hol:.3f});')
    life("es4", 0, G.DUR, 5)
    pop("#clk", t_acc - 0.3, sound="madera")
    for k in range(3):
        js(f'tl.fromTo("#fl{k}", {{opacity:0, scale:0.2}}, {{opacity:1, scale:1.1, duration:0.25, ease:"back.out(3)"}}, {t_acc + k * 0.08:.3f}); tl.to("#fl{k}", {{scaleY:1.25, duration:0.15, yoyo:true, repeat:5}}, {t_acc + 0.3:.3f});')
    sfx(t_acc, "golpe-climax", 0.4)
    shake(t_acc + 0.05, 18)
    js(f'tl.to("#fl0, #fl1, #fl2, #clk", {{opacity:0.25, duration:0.3}}, {t_ing - 0.4:.3f});')
    say("sbh", nb, "es4", t_ing - 0.3, t_nad, from_x=-40)
    for k in range(2):
        js(f'tl.fromTo("#qm{k}", {{opacity:0, scale:0.3, rotation:-20}}, {{opacity:1, scale:1, rotation:0, duration:0.3, ease:"back.out(3)"}}, {t_nad - 0.1 + k * 0.15:.3f});')
    sfx(t_nad, "pop", 0.3)


# ================================================================= 4 · EL PREMIO
def scene_premio():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h4", fx, fy, "4", "EL PREMIO", color="#facc15")
    add(character("es5", "estela", fx + 230, fl, 1.2, z=6))
    ico("tro", fx + 380, fy + 250, 220, "trophy", "#facc15", z=8, fill="#fde047")
    add(f'<div id="gpl" class="pill" style="{css_box(fx + 380, fy + 500, None, None, 9)}background:#facc15;color:{INK};font-size:52px;opacity:0">UN GOYA</div>')
    add(character("go5", "goya", fx + 760, fl, 1.1, z=5))
    add(f'<div id="gtag" class="ntag" style="{css_box(fx + 640, fl - 40, 240, 60, 8)}opacity:0">GOYA, LA VECINA</div>')
    add(f'<div id="gx" data-layout-ignore style="{css_box(fx + 680, fy + 520, 160, 160, 9)}opacity:0">{icon("x", 160, "#ef4444", 4)}</div>')
    t_cua, t_pre, t_gan, t_goy, t_ver, t_vec = P("cuatro"), P("premio"), P("ganaria"), P("goya"), P("verdad"), P("vecina")
    travel(t_cua - 0.3, F(2, 1), 2, 1630, dur=0.6)
    header_in("h4", t_cua, t_pre)
    js(f'tl.fromTo("#es5", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_pre:.3f});')
    life("es5", 0, G.DUR, 6)
    js(f'tl.fromTo("#tro", {{opacity:0, y:-300, rotation:-20}}, {{opacity:1, y:0, rotation:0, duration:0.5, ease:"bounce.out"}}, {t_gan - 0.2:.3f});')
    sfx(t_gan + 0.2, "check", 0.4)
    pop("#gpl", t_goy - 0.1, sound="pop2")
    js(f'tl.to(Q("es5","armR"), {{rotation:-150, svgOrigin:PIV.armR, duration:0.3, ease:"back.out(2)"}}, {t_goy:.3f}); jump("es5", {t_ver:.3f}, 40);')
    js(f'tl.fromTo("#go5", {{opacity:0, x:120}}, {{opacity:1, x:0, duration:0.35}}, {t_ver - 0.1:.3f}); tl.fromTo("#gtag", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_ver:.3f});')
    life("go5", 0, G.DUR, 7)
    js(f'tilt("go5", {t_vec:.3f});')
    js(f'tl.fromTo("#gx", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.25, ease:"back.out(3)"}}, {t_vec - 0.1:.3f});')
    sfx(t_vec, "golpe", 0.3)


# ================================================================= LA CRÍTICA
def scene_critica():
    fx, fy, fw, fh = F(3, 1)
    fl = floor(3)
    stars = "".join(f'<span style="color:{"#facc15" if k == 0 else "#cbd5e1"}">★</span>' for k in range(5))
    add(f'''<div id="np" class="news" style="{css_box(fx + 450, fy + 430, 480, 420, 5)}opacity:0">
      <div class="nph">{icon("newspaper", 54, INK, 2.6)} CRÍTICA</div><div class="nps">{stars}</div>
      <i class="nl" style="top:240px"></i><i class="nl" style="top:280px;width:70%"></i><i class="nl" style="top:320px"></i></div>''')
    add(character("es6", "estela", fx + 250, fl, 1.2, z=6))
    nq = bubble("sbc", fx + 40, fy + 180, 880, "ESTELA", "¡Qué ataque más gratuito!", "#ca8a04", "l", fs=54)
    t_y, t_cri, t_mal, t_res, t_que, t_gra = P("cada"), P("critica"), P("mala"), P("respuesta"), P("que", 4), P("gratuito", 2)
    travel(t_y - 0.4, F(3, 1), 3, 1630, dur=0.6)
    js(f'tl.fromTo("#es6", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_y:.3f});')
    life("es6", 0, G.DUR, 8)
    js(f'tl.fromTo("#np", {{opacity:0, rotation:-180, scale:0.2}}, {{opacity:1, rotation:-4, scale:1, duration:0.5, ease:"back.out(1.6)"}}, {t_cri - 0.2:.3f});')
    sfx(t_cri, "papel", 0.4)
    js(f'tl.to("#np .nps", {{scale:1.15, duration:0.12, yoyo:true, repeat:3}}, {t_mal:.3f});')
    js(f'tl.to(Q("es6","brows"), {{y:10, duration:0.2}}, {t_res:.3f});')
    say("sbc", nq, "es6", t_que, E("gratuito", 2), from_x=-40)
    js(f'tl.to(Q("es6","armL"), {{rotation:70, svgOrigin:PIV.armL, duration:0.25, ease:"back.out(2)"}}, {t_que:.3f});')
    js(f'tl.to("#np", {{x:300, rotation:30, opacity:0, duration:0.4, ease:"power2.in"}}, {t_gra:.3f});')
    sfx(t_que, "golpe", 0.35)
    shake(t_gra, 12)


# ================================================================= ENCUESTA
OPTS = [("CULEBRÓN", "#db2777"), ("VILLANA", "#7c3aed"), ("HOLLYWOOD", "#f59e0b")]


def scene_final():
    fx, fy, fw, fh = F(3, 0)
    rows = "".join(f'<div class="poll" style="top:{150 + k * 100}px"><span>{n}</span><i id="pb{k}" style="background:{c}"></i></div>'
                   for k, (n, c) in enumerate(OPTS))
    add(f'''<div id="pollc" class="card" style="{css_box(fx + 40, fy + 220, 880, 500, 6)}background:#fff;opacity:0">
      <div class="polh">{icon("message-circle", 54, INK, 2.6)} ¿QUÉ PAPEL LE DARÍAS?</div>{rows}</div>''')
    cta = "Yo la pondría de…"
    add(f'''<div id="cbx" class="card" style="{css_box(fx + 40, fy + 760, 880, 170, 6)}background:#fff;opacity:0">
      <div id="ctt" class="ctt">{chars(cta, "kc")}</div><div id="pub" class="pubb">Publicar</div></div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 800, fy + 880, 90, 90, 12)}opacity:0">{icon("mouse-pointer-2", 90, "#fff", 2.4).replace("<svg", "<svg fill=\"#0f1115\"")}</div>')
    t_pap, t_dar, t_leo, t_com = P("papel", 2), P("darias"), P("leo"), P("comentarios")
    travel(t_pap - 0.6, F(3, 0), 3, 570, dur=0.6)
    slide_in("#pollc", t_pap - 0.3, dy=-60)
    js('tl.set("[id^=pb]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    for k, w in enumerate([0.6, 0.85, 0.7]):
        js(f'tl.to("#pb{k}", {{scaleX:{w}, duration:0.35, ease:"back.out(1.6)"}}, {t_dar - 0.2 + k * 0.12:.3f});')
    sfx(t_dar, "pop2", 0.25)
    slide_in("#cbx", t_dar + 0.2, dy=60, sound=None)
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
.ntag {{ border-radius:14px; background:#0f172a; border:4px solid #fff; color:#fff; font:900 30px {FONT}; text-align:center; line-height:52px; white-space:nowrap; }}
.cone2 {{ clip-path:polygon(40% 0, 60% 0, 100% 100%, 0 100%); background:linear-gradient(rgba(254,240,138,0.55), rgba(254,240,138,0.05)); }}
.rug {{ border-radius:10px; background:linear-gradient(90deg,#991b1b,#dc2626,#991b1b); }}
.bld {{ border-radius:18px 18px 0 0; border:8px solid rgba(0,0,0,0.25); overflow:hidden; }}
.bsign {{ position:absolute; left:20px; right:20px; top:24px; height:70px; border-radius:14px; font:900 32px {FONT}; text-align:center; line-height:70px; white-space:nowrap; letter-spacing:-1px; }}
.win {{ position:absolute; width:56px; height:76px; border-radius:8px; opacity:0.9; }}
.bdoor {{ position:absolute; left:50%; bottom:0; width:110px; height:130px; margin-left:-55px; background:#0b0c10; border-radius:55px 55px 0 0; }}
.sb {{ background:#fff; border:7px solid; border-radius:36px; padding:54px 30px 26px; box-shadow:0 18px 40px rgba(0,0,0,0.45); }}
.sb:after {{ content:""; position:absolute; bottom:-34px; width:0; height:0; border-left:24px solid transparent; border-right:24px solid transparent; border-top:34px solid #fff; }}
.sb.l:after {{ left:90px; }} .sb.r:after {{ right:110px; }} .sb.c:after {{ left:50%; margin-left:-24px; }}
.who {{ position:absolute; left:26px; top:-30px; padding:4px 22px; border-radius:999px; color:#fff; font:900 38px {FONT}; white-space:nowrap; }}
.sbt {{ font-weight:900; color:{INK}; line-height:1.12; }}
.kc {{ opacity:0; }}
.tvset {{ border-radius:30px; background:#3f3f46; border:14px solid #27272a; }}
.tvs {{ position:absolute; left:20px; right:20px; top:20px; bottom:40px; border-radius:18px; background:radial-gradient(circle,#fbcfe8,#be185d); display:flex; align-items:center; justify-content:center; }}
.tvt {{ font:900 58px {FONT}; color:#fff; text-align:center; line-height:1.05; text-shadow:0 4px 0 #831843; }}
.tvset .tvl, .tvset .tvr {{ position:absolute; bottom:-60px; width:14px; height:60px; background:#27272a; }}
.tvset .tvl {{ left:120px; transform:rotate(20deg); }} .tvset .tvr {{ right:120px; transform:rotate(-20deg); }}
.tcard {{ background:#fff; border:8px solid; border-radius:30px; padding:26px 20px; text-align:center; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.tct {{ font:900 34px {FONT}; letter-spacing:2px; }}
.tcn {{ font-weight:900; color:{INK}; line-height:1.05; margin-top:10px; }}
.fan {{ border-radius:130px 130px 0 0; background:repeating-conic-gradient(from 270deg at 50% 100%, #7c3aed 0 10deg, #c4b5fd 10deg 20deg); }}
.hill {{ border-radius:50% 50% 0 0 / 100% 100% 0 0; background:linear-gradient(#57534e,#292524); }}
.hws {{ position:absolute; left:0; right:0; top:60px; display:flex; justify-content:center; gap:10px; }}
.hws b {{ font:900 86px {FONT}; color:#fff; display:inline-block; }}
.qmk {{ font:900 110px {FONT}; color:{ACC}; text-align:center; text-shadow:0 6px 0 #b45309; }}
.news {{ border-radius:10px; background:#f5f5f4; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.nph {{ position:absolute; left:0; right:0; top:30px; display:flex; align-items:center; justify-content:center; gap:14px; font:900 54px {FONT}; color:{INK}; }}
.nps {{ position:absolute; left:0; right:0; top:110px; text-align:center; font-size:84px; letter-spacing:6px; }}
.nl {{ position:absolute; left:40px; width:80%; height:16px; border-radius:8px; background:#d6d3d1; }}
.polh svg {{ flex:none; }}
.polh {{ position:absolute; left:40px; right:40px; top:40px; display:flex; align-items:center; gap:18px; font:900 48px {FONT}; color:{INK}; white-space:nowrap; }}
.poll {{ position:absolute; left:40px; right:40px; height:76px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:340px; flex:none; font:900 46px {FONT}; color:{INK}; white-space:nowrap; }}
.poll i {{ flex:1; height:44px; border-radius:22px; }}
.ctt {{ position:absolute; left:40px; top:52px; font:800 52px {FONT}; color:{INK}; white-space:nowrap; }}
.pubb {{ position:absolute; right:30px; top:40px; padding:12px 40px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 56px {FONT}; }}
"""


def build():
    world()
    scene_hook()
    scene_real()
    scene_culebron()
    scene_villana()
    scene_hollywood()
    scene_premio()
    scene_critica()
    scene_final()
