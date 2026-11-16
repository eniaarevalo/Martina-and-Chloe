"""Escenas del vídeo «¿Cuánto cuesta un capítulo de La que se avecina?». Un solo mundo: un camino en zigzag
(el secreto -> el precio de la tele -> el tiempo -> los sueldos -> en qué se va -> la estimación -> encuesta)."""
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


# ================================================================= GANCHO: el secreto
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    add(f'<div id="lqsa" class="pill" style="{css_box(fx + 210, fy + 170, None, None, 9)}background:#0f766e;color:#fff;font-size:58px;opacity:0">'
        f'{icon("tv", 56, "#fff", 2.6)} LA QUE SE AVECINA</div>')
    add(f'<div id="clap" data-layout-ignore style="{css_box(fx + 50, fy + 380, 400, 400, 5)}">{icon("clapperboard", 400, "#f8fafc", 1.8)}</div>')
    keys = "".join(f'<i class="key" style="left:{30 + (k % 4) * 82}px;top:{220 + (k // 4) * 82}px"></i>' for k in range(16))
    add(f'''<div id="calc" class="calc" style="{css_box(fx + 520, fy + 320, 380, 580, 5)}">
      <div class="cdisp"><span id="cq">¿?</span></div>{keys}</div>''')
    add(f'<div id="sec" class="stampbox" style="{css_box(fx + 140, fy + 760, 520, 170, 10)}opacity:0">{icon("lock", 90, "#ef4444", 3)} SECRETO</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: la claqueta cae y se cierra, la calculadora entra
    js('tl.fromTo("#clap", {y:-500, rotation:-20, opacity:1}, {y:0, rotation:0, duration:0.5, ease:"back.out(1.6)"}, 0);')
    js('tl.fromTo("#calc", {x:500, opacity:1}, {x:0, duration:0.55, ease:"power3.out"}, 0.15);')
    js('tl.to("#clap", {rotation:-6, duration:0.08, yoyo:true, repeat:1}, 0.55);')
    sfx(0.0, "whoosh", 0.35)
    sfx(0.55, "madera", 0.45)
    t_cap, t_ave, t_nad, t_pub, t_ech, t_cue = P("capitulo"), P("avecina"), P("nadie"), P("publico"), P("echar"), P("cuentas")
    pop("#lqsa", t_cap, sound="pop2")
    js(f'tl.to("#cq", {{scale:1.3, duration:0.15, yoyo:true, repeat:3}}, {t_ave:.3f});')
    stamp("#sec", t_nad - 0.1, rot=-8)
    js(f'tl.to("#sec", {{opacity:0, duration:0.3}}, {t_ech - 0.3:.3f});')
    js(f'tl.to(".key", {{backgroundColor:"#facc15", duration:0.08, yoyo:true, repeat:1, stagger:{{each:0.06, from:"random"}}}}, {t_ech:.3f});')
    for k in range(5):
        sfx(t_ech + k * 0.13, "click", 0.18)
    js(f'tl.to("#calc", {{y:-14, duration:0.15, yoyo:true, repeat:1}}, {t_cue:.3f});')


# ================================================================= 1 · EL PRECIO DE LA TELE
def scene_tele():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "EL PRECIO DE LA TELE", color="#facc15")
    chip("tve", fx + 60, fy + 190, "tv", "SERIES DE PRIME TIME · TVE", "#fff", INK, fs=44)
    X0, X1 = 70, 760
    xs = lambda v: X0 + (X1 - X0) * v / 1_000_000
    ticks = "".join(f'<i class="tick" style="left:{xs(v) - 3:.0f}px"></i><span class="tl" style="left:{xs(v) - 100:.0f}px">{lab}</span>'
                    for v, lab in [(0, "0 €"), (500_000, "500.000"), (1_000_000, "1 MILLÓN")])
    add(f'''<div id="scl" class="card" style="{css_box(fx + 40, fy + 330, 880, 420, 6)}background:#fff;opacity:0">
      <div class="axis"></div>{ticks}
      <div id="band" class="band" style="left:{xs(600_000):.0f}px;width:{xs(800_000) - xs(600_000):.0f}px"></div>
      <div id="l6" class="bl6" style="left:{xs(600_000) - 250:.0f}px;text-align:right">600.000 €</div>
      <div id="l8" class="bl6" style="left:{xs(800_000) - 200:.0f}px;top:300px">800.000 €</div>
      <div id="pin" class="pin" style="left:{xs(760_000) - 45:.0f}px">{icon("map-pin", 90, "#ef4444", 2.6).replace("<svg", "<svg fill=\"#fecaca\"")}</div></div>''')
    add(f'<div id="cue" class="pill" style="{css_box(fx + 230, fy + 790, None, None, 9)}background:#ef4444;color:#fff;font-size:52px;opacity:0">CUÉNTAME ≈ 760.000 €</div>')
    add(f'<div id="pc" class="pill" style="{css_box(fx + 280, fy + 900, None, None, 9)}background:#1f2937;color:#fff;font-size:44px;opacity:0">POR CAPÍTULO</div>')
    t_uno, t_cue0, t_tve, t_ent, t_60, t_80, t_cap = P("uno"), P("cuesta", 2), P("tve"), P("entre"), P("600.000"), P("800.000"), P("capitulo", 2)
    travel(t_uno - 0.3, F(0, 1), 0, 1630, dur=0.7)
    header_in("h1", t_uno, t_cue0)
    pop("#tve", t_tve - 0.1, sound="pop2")
    slide_in("#scl", t_tve + 0.3, dy=60, sound=None)
    js('tl.set("#band", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to("#band", {{scaleX:1, duration:{t_80 - t_60 + 0.3:.2f}, ease:"power2.out"}}, {t_60:.3f});')
    pop("#l6", t_60, sound="pop")
    pop("#l8", t_80, sound="pop")
    pop("#pc", t_cap - 0.1, sound=None)
    t_cuen, t_760, t_ult = P("cuentame"), P("760.000"), P("ultima")
    js(f'tl.fromTo("#pin", {{opacity:0, y:-260}}, {{opacity:1, y:0, duration:0.5, ease:"bounce.out"}}, {t_cuen - 0.1:.3f});')
    sfx(t_cuen + 0.3, "golpe", 0.3)
    pop("#cue", t_760 - 0.1, sound="check")
    js(f'tl.to("#cue", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_ult:.3f});')


# ================================================================= 2 · EL TIEMPO
def scene_tiempo():
    fx, fy, fw, fh = F(1, 1)
    header("h2", fx, fy, "2", "EL TIEMPO", color="#38bdf8")
    chip("alb", fx + 60, fy + 190, "pen-line", "ALBERTO CABALLERO · CREADOR", "#fff", INK, fs=42)
    rr, hh = roller("mes", "01", 230, INK)
    add(f'''<div id="cal" class="calp" style="{css_box(fx + 250, fy + 320, 460, 470, 6)}opacity:0">
      <div class="calt">{icon("calendar", 54, "#fff", 2.6)} MES</div><div class="caln">{rr}</div></div>''')
    add(f'<div id="tem" class="pill" style="{css_box(fx + 150, fy + 840, None, None, 9)}background:#38bdf8;color:{INK};font-size:54px;opacity:0">1 TEMPORADA ≈ 10 MESES</div>')
    t_dos, t_tie, t_alb, t_sac, t_lle, t_die, t_mes = P("dos"), P("tiempo"), P("alberto"), P("sacar"), P("lleva"), P("diez"), P("meses")
    travel(t_dos - 0.3, F(1, 1), 1, 1630, dur=0.7)
    header_in("h2", t_dos, t_tie)
    pop("#alb", t_alb - 0.1, sound="pop2")
    slide_in("#cal", t_sac - 0.2, dy=-60)
    roll_set("mes", "01", hh)
    # pasan las hojas: 1, 2, 3 ... 10
    steps = ["02", "03", "04", "05", "06", "07", "08", "09"]
    t0, t1 = t_sac + 0.2, t_die - 0.1
    for k, v in enumerate(steps):
        tt = t0 + (t1 - t0) * k / len(steps)
        roll_to("mes", v, hh, tt, dur=0.2, spins=0, stagger=0)
        js(f'tl.fromTo("#cal", {{rotationX:0}}, {{rotationX:-12, duration:0.08, yoyo:true, repeat:1, immediateRender:false}}, {tt:.3f});')
    roll_to("mes", "10", hh, t_die, dur=0.4, spins=0, stagger=0)
    js(f'tl.to("#cal", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_die + 0.3:.3f});')
    stamp("#tem", t_mes - 0.1, rot=-4)


# ================================================================= 3 · LOS SUELDOS
def scene_sueldos():
    fx, fy, fw, fh = F(1, 0)
    header("h3", fx, fy, "3", "LOS SUELDOS", color="#ec4899", txt="#fff")
    add(f'''<div id="mac" class="card" style="{css_box(fx + 60, fy + 190, 840, 180, 7)}background:#fff;opacity:0">
      <div class="mq1">MACARENA GÓMEZ</div><div class="mq2">«Ridículo» comparado con la BBC</div></div>''')
    # balanza
    add(f'<div id="post" class="post" style="{css_box(fx + 465, fy + 520, 30, 470, 4)}opacity:0"></div>')
    add(f'<div id="foot" class="foot" style="{css_box(fx + 340, fy + 980, 280, 40, 4)}opacity:0"></div>')
    add(f'<div id="beam" class="beam" style="{css_box(fx + 140, fy + 520, 680, 26, 5)}opacity:0"></div>')
    for k, (x, lab, n) in enumerate([(fx + 60, "ESPAÑA", 2), (fx + 640, "BBC", 8)]):
        add(f'<div id="pan{k}" style="{css_box(x, fy + 540, 260, 380, 6)}opacity:0">'
            f'<i class="rope l"></i><i class="rope r"></i><div class="pan"></div><div class="panl">{lab}</div></div>')
        coins(f"cs{k}", x + 55, fy + 820, n, z=7)
    t_tre, t_act, t_mac, t_cob, t_rid, t_bbc = P("tres"), P("actores"), P("macarena"), P("cobra"), P("ridiculo"), P("bbc")
    travel(t_tre - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h3", t_tre, t_act)
    slide_in("#mac", t_mac - 0.2, dy=-60)
    for s_ in ("#post", "#foot", "#beam", "#pan0", "#pan1"):
        js(f'tl.fromTo("{s_}", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_cob - 0.4:.3f});')
    js('tl.set("[id^=cs] .coin", {opacity:0}, 0);')
    js(f'tl.to("#cs0 .coin", {{opacity:1, duration:0.1, stagger:0.1}}, {t_cob:.3f});')
    js(f'tl.to("#cs1 .coin", {{opacity:1, duration:0.08, stagger:0.07}}, {t_rid:.3f});')
    sfx(t_rid, "tic-rodillo", 0.3)
    # la balanza se inclina hacia la BBC
    js(f'tl.to("#beam", {{rotation:10, duration:0.6, ease:"back.out(1.6)"}}, {t_bbc - 0.2:.3f});')
    js(f'tl.to("#pan0, #cs0", {{y:-60, duration:0.6, ease:"back.out(1.6)"}}, {t_bbc - 0.2:.3f}); tl.to("#pan1, #cs1", {{y:60, duration:0.6, ease:"back.out(1.6)"}}, {t_bbc - 0.2:.3f});')
    sfx(t_bbc, "golpe", 0.3)


# ================================================================= ¿EN QUÉ SE VA EL DINERO?
def scene_gastos():
    fx, fy, fw, fh = F(2, 0)
    header("h4", fx, fy, "€", "¿EN QUÉ SE VA?", color="#22c55e")
    building("mp", fx + 330, fy + 500, 300, 530, "MONTEPINAR", "#e2e8f0", "#38bdf8", "#0f766e", "#fff", z=4)
    items = [("sue", "coins", "SUELDOS", fx + 20, fy + 230, "sueldos"), ("gui", "pen-line", "GUIONISTAS", fx + 620, fy + 230, "guionistas"),
             ("tec", "wrench", "TÉCNICOS", fx + 20, fy + 450, "tecnicos"), ("pla", "video", "PLATÓS", fx + 660, fy + 450, "platos"),
             ("ves", "shirt", "VESTUARIO", fx + 20, fy + 670, "vestuario")]
    for cid, ic, lab, x, y, w in items:
        chip(cid, x, y, ic, lab, "#fff", INK, z=8, fs=38)
    t_asi, t_din = P("asi"), P("dinero")
    travel(t_asi - 0.3, F(2, 0), 2, 570, dur=0.7)
    header_in("h4", t_asi, t_din)
    for cid, ic, lab, x, y, w in items:
        pop(f"#{cid}", P(w) - 0.1, sound="pop2", vol=0.22)
    js('tl.set("#mp", {scaleY:0, transformOrigin:"50% 100%", opacity:1}, 0);')
    js('tl.set("#mp .win", {opacity:0}, 0);')
    t_tod, t_mon, t_mon2 = P("todo"), P("montepinar"), P("montar")
    js(f'tl.to("#mp", {{scaleY:1, duration:0.6, ease:"back.out(1.4)"}}, {t_tod - 0.1:.3f});')
    js(f'tl.to("#mp .win", {{opacity:0.9, duration:0.05, stagger:0.04}}, {t_mon:.3f});')
    sfx(t_tod, "whoosh-corto", 0.25)
    js(f'tl.to("#mp", {{scale:1.05, duration:0.15, yoyo:true, repeat:1}}, {t_mon2:.3f});')
    sfx(t_mon2, "check", 0.3)


# ================================================================= LA ESTIMACIÓN
def scene_estimacion():
    fx, fy, fw, fh = F(2, 1)
    add(f'<div id="cim" class="bigc" style="{css_box(fx + 60, fy + 200, 840, 260, 7)}opacity:0">'
        f'<div class="b1">CIENTOS DE MILES</div><div class="b2">DE EUROS POR CAPÍTULO</div></div>')
    for k, n in enumerate([4, 7, 10, 7, 4]):
        coins(f"st{k}", fx + 90 + k * 160, fy + 1000, n, z=6, w=140)
    add(f'<div id="est" class="stampbox" style="{css_box(fx + 210, fy + 520, 540, 160, 11)}opacity:0;font-size:90px;line-height:136px">ESTIMACIÓN</div>')
    add(f'<div id="nof" class="pill" style="{css_box(fx + 220, fy + 720, None, None, 10)}background:#1f2937;color:#fff;font-size:46px;opacity:0">'
        f'{icon("lock", 44, "#fff", 2.6)} NO ES UN DATO OFICIAL</div>')
    t_si, t_res, t_cad, t_cie, t_eur, t_est, t_ofi = P("si"), P("resto"), P("cada"), P("cientos"), P("euros", 3), P("estimacion"), P("oficial")
    travel(t_si - 0.2, F(2, 1), 2, 1630, dur=0.6)
    js('tl.set("[id^=st] .coin", {opacity:0}, 0);')
    js(f'tl.to("[id^=st] .coin", {{opacity:1, duration:0.06, stagger:0.025}}, {t_res:.3f});')
    sfx(t_res, "tic-rodillo", 0.3)
    slide_in("#cim", t_cie - 0.2, dy=-60)
    js(f'tl.to("#cim", {{scale:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_eur:.3f});')
    stamp("#est", t_est - 0.25, rot=-8)
    pop("#nof", t_ofi - 0.2, sound="pop2")


# ================================================================= ENCUESTA FINAL
OPTS = [("MENOS DE 300.000 €", "#22c55e"), ("300.000 – 700.000 €", "#facc15"), ("MÁS DE 1 MILLÓN", "#ef4444")]


def scene_final():
    fx, fy, fw, fh = F(3, 1)
    rows = "".join(f'<div class="poll" style="top:{150 + k * 100}px"><span>{n}</span><i id="pb{k}" style="background:{c}"></i></div>'
                   for k, (n, c) in enumerate(OPTS))
    add(f'''<div id="pollc" class="card" style="{css_box(fx + 40, fy + 220, 880, 500, 6)}background:#fff;opacity:0">
      <div class="polh">{icon("message-circle", 54, INK, 2.6)} ¿CUÁNTO CREES QUE CUESTA?</div>{rows}</div>''')
    cta = "Yo creo que…"
    add(f'''<div id="cbx" class="card" style="{css_box(fx + 40, fy + 760, 880, 170, 6)}background:#fff;opacity:0">
      <div id="ctt" class="ctt">{chars(cta, "kc")}</div><div id="pub" class="pubb">Publicar</div></div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 800, fy + 880, 90, 90, 12)}opacity:0">{icon("mouse-pointer-2", 90, "#fff", 2.4).replace("<svg", "<svg fill=\"#0f1115\"")}</div>')
    t_tu, t_cre, t_cue, t_leo, t_com = P("tu"), P("crees"), P("cuesta", 3), P("leo"), P("comentarios")
    travel(t_tu - 0.35, F(3, 1), 3, 1630, dur=0.6)
    slide_in("#pollc", t_tu - 0.1, dy=-60)
    js('tl.set("[id^=pb]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    for k, w in enumerate([0.45, 0.85, 0.6]):
        js(f'tl.to("#pb{k}", {{scaleX:{w}, duration:0.4, ease:"back.out(1.6)"}}, {t_cre + k * 0.15:.3f});')
    sfx(t_cre, "pop2", 0.25)
    slide_in("#cbx", t_cue, dy=60, sound=None)
    type_on("#ctt .kc", len(cta), t_cue + 0.2, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:160, y:160}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    cam(E("comentarios") + 0.1, (0, 100, 2200, 3900), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.htitle {{ font-size:70px; top:30px; }}
.stampbox {{ font:900 100px {FONT}; color:{BAD}; border:12px solid {BAD}; border-radius:26px; background:rgba(255,255,255,0.94);
  display:flex; align-items:center; justify-content:center; gap:16px; letter-spacing:-2px; }}
.calc {{ border-radius:40px; background:#1f2937; border:8px solid #475569; box-shadow:0 30px 60px rgba(0,0,0,0.5); }}
.cdisp {{ position:absolute; left:28px; right:28px; top:28px; height:160px; border-radius:20px; background:#a3e635;
  font:900 120px {FONT}; color:#1a2e05; text-align:right; padding-right:30px; line-height:160px; }}
.cdisp span {{ display:inline-block; }}
.key {{ position:absolute; width:70px; height:70px; border-radius:16px; background:#64748b; }}
.axis {{ position:absolute; left:60px; right:60px; top:200px; height:14px; border-radius:7px; background:#cbd5e1; }}
.tick {{ position:absolute; top:186px; width:6px; height:42px; background:#94a3b8; border-radius:3px; }}
.tl {{ position:absolute; top:240px; width:200px; text-align:center; font:800 34px {FONT}; color:#64748b; white-space:nowrap; }}
.band {{ position:absolute; top:176px; height:62px; border-radius:16px; background:rgba(250,204,21,0.85); border:5px solid #ca8a04; }}
.bl6 {{ position:absolute; top:60px; width:240px; text-align:center; font:900 44px {FONT}; color:{INK}; white-space:nowrap; }}
.pin {{ position:absolute; top:96px; width:90px; height:90px; }}
.calp {{ border-radius:34px; background:#fff; overflow:hidden; box-shadow:0 30px 60px rgba(0,0,0,0.5); }}
.calt {{ height:110px; background:#ef4444; color:#fff; font:900 60px {FONT}; display:flex; align-items:center; justify-content:center; gap:16px; }}
.caln {{ position:absolute; left:0; right:0; top:150px; text-align:center; }}
.mq1 {{ position:absolute; left:0; right:0; top:22px; text-align:center; font:900 48px {FONT}; color:#db2777; }}
.mq2 {{ position:absolute; left:0; right:0; top:92px; text-align:center; font:900 46px {FONT}; color:{INK}; white-space:nowrap; }}
.post {{ border-radius:14px; background:#94a3b8; }}
.foot {{ border-radius:20px 20px 0 0; background:#64748b; }}
.beam {{ border-radius:13px; background:#cbd5e1; transform-origin:50% 50%; }}
.rope {{ position:absolute; top:0; width:6px; height:250px; background:#94a3b8; }}
.rope.l {{ left:30px; transform:rotate(-8deg); transform-origin:50% 0; }} .rope.r {{ right:30px; transform:rotate(8deg); transform-origin:50% 0; }}
.pan {{ position:absolute; left:0; right:0; top:240px; height:44px; border-radius:0 0 130px 130px; background:#e2e8f0; }}
.panl {{ position:absolute; left:0; right:0; top:300px; text-align:center; font:900 50px {FONT}; color:#fff; }}
.coins {{ }}
.coin {{ position:absolute; left:0; right:0; height:40px; border-radius:50%; background:radial-gradient(ellipse at 50% 40%, #fde68a, #f59e0b 70%);
  border:5px solid #b45309; }}
.bld {{ border-radius:18px 18px 0 0; border:8px solid rgba(0,0,0,0.25); overflow:hidden; }}
.bsign {{ position:absolute; left:24px; right:24px; top:24px; height:70px; border-radius:14px; font:900 34px {FONT}; text-align:center; line-height:70px; white-space:nowrap; letter-spacing:-1px; }}
.win {{ position:absolute; width:62px; height:76px; border-radius:8px; opacity:0.9; }}
.bdoor {{ position:absolute; left:50%; bottom:0; width:110px; height:130px; margin-left:-55px; background:#0b0c10; border-radius:55px 55px 0 0; }}
.bigc {{ border-radius:36px; background:{ACC}; box-shadow:0 30px 60px rgba(0,0,0,0.5); }}
.b1 {{ position:absolute; left:0; right:0; top:46px; text-align:center; font:900 84px {FONT}; color:{INK}; letter-spacing:-3px; white-space:nowrap; }}
.b2 {{ position:absolute; left:0; right:0; top:160px; text-align:center; font:900 52px {FONT}; color:#713f12; white-space:nowrap; }}
.polh svg {{ flex:none; }}
.polh {{ position:absolute; left:40px; right:40px; top:40px; display:flex; align-items:center; gap:18px; font:900 44px {FONT}; color:{INK}; white-space:nowrap; }}
.poll {{ position:absolute; left:40px; right:40px; height:76px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:470px; flex:none; font:900 38px {FONT}; color:{INK}; white-space:nowrap; }}
.poll i {{ flex:1; height:40px; border-radius:20px; }}
.ctt {{ position:absolute; left:40px; top:52px; font:800 54px {FONT}; color:{INK}; white-space:nowrap; }}
.pubb {{ position:absolute; right:30px; top:40px; padding:12px 40px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 56px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_tele()
    scene_tiempo()
    scene_sueldos()
    scene_gastos()
    scene_estimacion()
    scene_final()
