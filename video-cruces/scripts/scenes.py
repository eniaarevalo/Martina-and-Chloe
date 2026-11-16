"""Escenas del vídeo «4 cruces entre Aquí no hay quien viva y La que se avecina» (CRUCE IMAGINADO).
Un solo mundo: un camino en zigzag (los dos edificios -> Recio × Mauri -> Berta × Paloma -> Fina × Vicenta
-> Cuesta × Pastor -> mismo actor -> encuesta)."""
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


# ================================================================= GANCHO: los dos edificios
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    building("bA", fx + 40, fy + 400, 400, 600, "DESENGAÑO 21", "#8a4b2f", "#fcd34d", "#fef3c7", "#7c2d12")
    building("bB", fx + 520, fy + 400, 400, 600, "MONTEPINAR", "#e2e8f0", "#38bdf8", "#0f766e", "#fff")
    add(f'<div id="imag" class="pill" style="{css_box(fx + 230, fy + 160, None, None, 9)}background:#fff;color:{INK};font-size:54px;opacity:0">'
        f'{icon("drama", 52, INK, 2.6)} CRUCE IMAGINADO</div>')
    add(f'<div id="spk" data-layout-ignore style="{css_box(fx + 400, fy + 560, 160, 160, 9)}opacity:0">'
        f'{icon("zap", 160, ACC, 2.4).replace("<svg", "<svg fill=\"#ffd43b\"")}</div>')
    cols = ["#3b82c4", "#db2777", "#16a34a", "#7c3aed"]
    for k in range(4):
        add(f'<div id="nb{k}" class="nbad" style="{css_box(fx + 210 + k * 140, fy + 270, 110, 110, 9)}background:{cols[k]};opacity:0">{k + 1}</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: los dos edificios entran desde los lados
    js('tl.fromTo("#bA", {x:-420, opacity:1}, {x:-60, duration:0.7, ease:"power3.out"}, 0);')
    js('tl.fromTo("#bB", {x:420, opacity:1}, {x:60, duration:0.7, ease:"power3.out"}, 0);')
    sfx(0.0, "whoosh", 0.35)
    pop("#imag", 0.4, sound="pop2")
    t_cru, t_mon, t_cua, t_nun = P("cruzaran"), P("montepinar"), P("cuatro"), P("nunca")
    js(f'tl.to("#bA", {{x:0, duration:0.5, ease:"power2.in"}}, {t_cru:.3f}); tl.to("#bB", {{x:0, duration:0.5, ease:"power2.in"}}, {t_cru:.3f});')
    js(f'tl.fromTo("#spk", {{opacity:0, scale:0.3, rotation:-30}}, {{opacity:1, scale:1, rotation:0, duration:0.3, ease:"back.out(3)"}}, {t_cru + 0.5:.3f});')
    sfx(t_cru + 0.5, "golpe", 0.45)
    shake(t_cru + 0.5, 14)
    js(f'tl.to("#bA", {{rotation:-3, duration:0.2, yoyo:true, repeat:1}}, {t_mon:.3f}); tl.to("#bB", {{rotation:3, duration:0.2, yoyo:true, repeat:1}}, {t_mon:.3f});')
    for k in range(4):
        pop(f"#nb{k}", t_cua + k * 0.12, sound="pop" if k == 0 else None)
    js(f'tl.to("[id^=nb]", {{y:-16, duration:0.18, yoyo:true, repeat:1, stagger:0.08}}, {t_nun:.3f});')


# ================================================================= 1 · RECIO × MAURI
def scene_recio():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "1", "RECIO × MAURI", color="#3b82c4", txt="#fff")
    for k, (x, pl) in enumerate([(fx + 110, "1ºA"), (fx + 580, "1ºB")]):
        add(f'<div id="dr{k}" class="door3" style="{css_box(x, fl - 700, 280, 680, 2)}opacity:0"><b>{pl}</b></div>')
    add(character("rc1", "recio", fx + 250, fl, 1.2, z=5))
    add(character("ma1", "mauri", fx + 720, fl, 1.2, z=5))
    nr = bubble("sbr", fx + 10, fy + 180, 540, "RECIO", "Yo soy un empresario respetable y no quiero cosas raras en mi escalera.", "#ef4444", "l")
    nm = bubble("sbm", fx + 400, fy + 200, 550, "MAURI", "Tranquilo, Antonio, que lo mío no se pega. Lo que se pega es tu olor a marisco.", "#16a596", "r")
    add(f'<div id="fsh" data-layout-ignore style="{css_box(fx + 120, fl - 640, 130, 130, 9)}opacity:0">{icon("fish", 130, "#38bdf8", 2.6)}</div>')
    add(f'<div id="stk" data-layout-ignore style="{css_box(fx + 260, fl - 660, 130, 130, 9)}opacity:0">{icon("wind", 130, "#84cc16", 2.8)}</div>')
    add(f'<div id="sc1" class="pill" style="{css_box(fx + 250, fy + 560, None, None, 10)}background:{ACC};color:{INK};font-size:56px;opacity:0">MAURI 1 – 0 RECIO</div>')
    t_uno, t_ant, t_mau, t_rel = P("uno"), P("antonio"), P("mauri"), P("rellano")
    travel(t_uno - 0.3, F(0, 1), 0, 1630, dur=0.7)
    header_in("h1", t_uno, t_ant)
    for k in range(2):
        js(f'tl.fromTo("#dr{k}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_ant + k * 0.1:.3f});')
    life("rc1", 0, G.DUR, 1)
    life("ma1", 0, G.DUR, 2)
    js(f'tl.fromTo("#rc1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_ant + 0.2:.3f});')
    js(f'tl.fromTo("#ma1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_mau:.3f});')
    js(f'wave("ma1", {t_mau + 0.2:.3f}, {t_rel + 0.4:.3f}); tl.to(Q("ma1","armR"), {{rotation:0, svgOrigin:PIV.armR, duration:0.3}}, {t_rel + 0.5:.3f});')
    sfx(t_ant + 0.2, "puerta", 0.3)
    t_r2, t_emp, t_rar, t_esc = P("recio", 2), P("empresario"), P("raras"), E("escalera")
    say("sbr", nr, "rc1", t_r2 + 0.3, t_esc, from_x=-60)
    js(f'tl.to(Q("rc1","shirt"), {{fill:"#2563eb", duration:0.1}}, {t_emp:.3f});')
    js(f'point("rc1", "R", {t_rar - 0.2:.3f}, {t_esc + 0.3:.3f}, -70);')
    js(f'tl.to("#rc1", {{x:12, duration:0.07, yoyo:true, repeat:7}}, {t_rar:.3f});')
    sfx(t_rar, "golpe", 0.25)
    t_m2, t_tra, t_pe2, t_olo, t_mar = P("mauri", 2), P("tranquilo"), P("pega", 2), P("olor"), P("marisco")
    js(f'tl.to("#sbr", {{opacity:0.25, scale:0.92, duration:0.3}}, {t_m2 - 0.3:.3f});')
    say("sbm", nm, "ma1", t_m2 + 0.3, E("marisco"), from_x=60)
    js(f'tilt("ma1", {t_tra:.3f});')
    pop("#fsh", t_olo - 0.1, sound="pop2")
    js(f'tl.fromTo("#stk", {{opacity:0, y:20}}, {{opacity:1, y:-30, duration:0.6}}, {t_olo:.3f}); tl.to("#fsh", {{rotation:20, duration:0.2, yoyo:true, repeat:3}}, {t_olo + 0.2:.3f});')
    js(f'jump("rc1", {t_mar:.3f}, 40);')
    stamp("#sc1", E("marisco") - 0.25, rot=-4)


# ================================================================= 2 · BERTA × PALOMA
def scene_berta():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    header("h2", fx, fy, "2", "BERTA × PALOMA", color="#db2777", txt="#fff")
    for k, x in enumerate([fx + 260, fx + 700]):
        add(f'<div id="dp{k}" class="dpole" style="{css_box(x + 150, fl - 780, 26, 780, 3)}opacity:0"></div>')
        add(f'<div id="dh{k}" class="dryer" style="{css_box(x - 135, fl - 545, 270, 130, 7)}opacity:0"></div>')
    add(f'<div id="sci" data-layout-ignore style="{css_box(fx + 420, fy + 600, 120, 120, 4)}opacity:0">{icon("scissors", 120, "#94a3b8", 2.4)}</div>')
    add(character("pa1", "paloma", fx + 260, fl, 1.2, z=5))
    add(character("be1", "berta", fx + 700, fl, 1.2, z=5))
    np_ = bubble("sbp", fx + 10, fy + 180, 460, "PALOMA", "Mi marido es el presidente de la comunidad.", "#c2410c", "l")
    nb = bubble("sbb", fx + 490, fy + 260, 460, "BERTA", "Pues el mío tiene una empresa de mariscos.", "#0f766e", "r")
    nd = bubble("sbd", fx + 180, fy + 250, 600, "LAS DOS", "Y ninguno me hace ni caso.", "#db2777", "c", fs=50)
    add(f'<div id="pq" class="pill" style="{css_box(fx + 380, fy + 560, None, None, 9)}background:{BAD};color:#fff;font-size:50px;opacity:0">PIQUE</div>')
    add(f'<div id="hc" data-layout-ignore style="{css_box(fx + 410, fy + 560, 140, 140, 9)}opacity:0">'
        f'{icon("heart-crack", 140, "#ef4444", 2.4).replace("<svg", "<svg fill=\"#fecaca\"")}</div>')
    t_dos, t_ber, t_pal, t_pel = P("dos"), P("berta"), P("paloma"), P("peluqueria")
    travel(t_dos - 0.3, F(1, 1), 1, 1630, dur=0.7)
    header_in("h2", t_dos, t_ber)
    life("pa1", 0, G.DUR, 3)
    life("be1", 0, G.DUR, 4)
    js(f'tl.fromTo("#be1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_ber:.3f});')
    js(f'tl.fromTo("#pa1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_pal:.3f});')
    for k in range(2):
        js(f'tl.fromTo("#dp{k}, #dh{k}", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.4, ease:"back.out(2)"}}, {t_pel - 0.2 + k * 0.1:.3f});')
    pop("#sci", t_pel, sound="pop2")
    js(f'tl.to("#sci", {{rotation:-25, duration:0.15, yoyo:true, repeat:5}}, {t_pel + 0.3:.3f});')
    t_p2, t_pre, t_b2, t_mar = P("paloma", 2), P("presidente"), P("berta", 2), P("mariscos")
    say("sbp", np_, "pa1", t_p2 + 0.25, E("comunidad"), from_x=-60)
    js(f'tl.to("#pa1", {{y:-14, duration:0.15, yoyo:true, repeat:1}}, {t_pre:.3f});')
    say("sbb", nb, "be1", t_b2 + 0.25, E("mariscos"), from_x=60)
    js(f'tl.to("#be1", {{y:-14, duration:0.15, yoyo:true, repeat:1}}, {t_mar:.3f});')
    pop("#pq", t_mar + 0.1, sound="golpe", vol=0.3)
    js(f'tl.to("#pq", {{rotation:4, duration:0.08, yoyo:true, repeat:5}}, {t_mar + 0.4:.3f});')
    t_vez, t_nin, t_cas = P("vez"), P("ninguno"), P("caso")
    js(f'tl.to("#sbp, #sbb, #pq", {{opacity:0, duration:0.25}}, {t_vez - 0.3:.3f});')
    js(f'tl.fromTo("#sbd", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_vez:.3f});')
    sfx(t_vez, "pop", 0.25)
    js(f'typeOn("#sbd .kc", {t_nin - 0.1:.3f}, {E("caso"):.3f});')
    talk("pa1", t_nin - 0.1, E("caso"))
    talk("be1", t_nin - 0.1, E("caso"))
    for c in ("pa1", "be1"):
        js(f'tl.to(Q("{c}","head"), {{rotation:{-10 if c == "pa1" else 10}, y:10, svgOrigin:PIV.head, duration:0.4}}, {t_cas:.3f});')
    js(f'tl.to("#sbd", {{y:-80, duration:0.3}}, {t_cas:.3f});')
    pop("#hc", t_cas + 0.1, sound="pop2")


# ================================================================= 3 · FINA × MARISA
def scene_fina():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    header("h3", fx, fy, "3", "FINA × MARISA", color="#16a34a", txt="#fff")
    add(f'''<div id="bench" style="{css_box(fx + 110, fl - 230, 740, 230, 3)}opacity:0">
      <i class="bk" style="top:0"></i><i class="bk" style="top:46px"></i><i class="bk" style="top:110px"></i>
      <i class="bl" style="left:60px"></i><i class="bl" style="right:60px"></i></div>''')
    for k, x in enumerate([fx + 40, fx + 830]):
        add(f'<div id="pg{k}" data-layout-ignore style="{css_box(x, fl - 100, 90, 90, 6)}opacity:0">{icon("bird", 90, "#cbd5e1", 2.6)}</div>')
    add(character("fi1", "fina", fx + 290, fl, 1.2, z=5))
    add(character("vi1", "vecina1", fx + 680, fl, 1.2, z=5))
    nf = bubble("sbf", fx + 10, fy + 180, 520, "DOÑA FINA", "Mira esa, con la falda por aquí. Qué poca vergüenza.", "#64748b", "l", fs=44)
    nv = bubble("sbv", fx + 440, fy + 230, 510, "MARISA", "Pues la del quinto, peor. Y su marido, ni le cuento.", "#16a34a", "r", fs=44)
    rc, hc = roller("crit", "00", 130, BAD)
    add(f'''<div id="mtr" class="card" style="{css_box(fx + 130, fy + 200, 700, 300, 9)}background:#fff;opacity:0">
      <div class="mtt">VECINOS CRITICADOS</div><div class="crn">{rc}</div></div>''')
    add(f'<div id="zpb" data-layout-ignore style="{css_box(fx + 410, fl - 400, 140, 140, 9)}opacity:0">'
        f'{icon("zap", 140, ACC, 2.4).replace("<svg", "<svg fill=\"#ffd43b\"")}</div>')
    t_tre, t_fin, t_mar, t_ban, t_par = P("tres"), P("fina"), P("marisa"), P("banco"), P("parque")
    travel(t_tre - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h3", t_tre, t_fin)
    life("fi1", 0, G.DUR, 5)
    life("vi1", 0, G.DUR, 6)
    js(f'tl.fromTo("#fi1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_fin:.3f});')
    js(f'tl.fromTo("#vi1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_mar:.3f});')
    js(f'tl.fromTo("#bench", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_ban - 0.1:.3f});')
    sfx(t_ban, "madera", 0.3)
    for k in range(2):
        js(f'tl.fromTo("#pg{k}", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_par + k * 0.15:.3f});')
        js(f'tl.to("#pg{k}", {{y:-10, duration:0.18, yoyo:true, repeat:9}}, {t_par + 0.6 + k * 0.1:.3f});')
    t_f2, t_mir, t_fal, t_ver, t_m2, t_qui, t_mdo, t_cue = (P("fina", 2), P("mira"), P("falda"), P("verguenza"), P("marisa", 2),
                                                            P("quinto"), P("marido", 2), E("cuento"))
    say("sbf", nf, "fi1", t_f2 + 0.3, E("verguenza"), from_x=-60)
    js(f'point("fi1", "L", {t_mir - 0.1:.3f}, {t_ver + 0.3:.3f}, 70);')
    js(f'tl.to(Q("fi1","head"), {{rotation:-12, svgOrigin:PIV.head, duration:0.2, yoyo:true, repeat:3}}, {t_ver:.3f});')
    sfx(t_ver, "pop2", 0.2)
    js(f'tl.to("#sbf", {{opacity:0.25, scale:0.92, duration:0.3}}, {t_m2 - 0.3:.3f});')
    say("sbv", nv, "vi1", t_m2 + 0.3, t_cue, from_x=60)
    js(f'point("vi1", "R", {t_qui - 0.1:.3f}, {t_cue + 0.3:.3f}, -110);')
    js(f'tilt("vi1", {t_mdo:.3f});')
    js(f'tl.to(Q("fi1","head"), {{rotation:12, svgOrigin:PIV.head, duration:0.25}}, {t_mdo:.3f}); tl.to(Q("fi1","head"), {{rotation:0, svgOrigin:PIV.head, duration:0.3}}, {t_cue + 0.2:.3f});')
    t_med, t_cri, t_bar, t_pel, t_b2 = P("media"), P("criticado"), P("barrio"), P("pelean"), P("banco", 2)
    js(f'tl.to("#sbf, #sbv", {{opacity:0, duration:0.25}}, {t_med - 0.2:.3f});')
    slide_in("#mtr", t_med, dy=-60)
    roll_set("crit", "00", hc)
    roll_to("crit", "47", hc, t_cri, dur=0.8, spins=1)
    roll_to("crit", "99", hc, t_bar, dur=0.6, spins=2)
    js(f'tl.to("#mtr", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_bar + 0.6:.3f});')
    # se pelean por el banco: cada una tira hacia su lado
    js(f'tl.to("#mtr", {{opacity:0, y:-40, duration:0.25}}, {t_pel - 0.2:.3f});')
    js(f'point("fi1", "R", {t_pel:.3f}, {t_b2 + 0.8:.3f}, -60); point("vi1", "L", {t_pel:.3f}, {t_b2 + 0.8:.3f}, 60);')
    js(f'tl.to("#fi1", {{x:-30, duration:0.12, yoyo:true, repeat:9}}, {t_pel:.3f}); tl.to("#vi1", {{x:30, duration:0.12, yoyo:true, repeat:9}}, {t_pel:.3f});')
    js(f'tl.to("#bench", {{x:16, rotation:1.5, duration:0.1, yoyo:true, repeat:11}}, {t_pel:.3f});')
    js(f'tl.fromTo("#zpb", {{opacity:0, scale:0.3, rotation:-30}}, {{opacity:1, scale:1, rotation:0, duration:0.25, ease:"back.out(3)"}}, {t_b2 - 0.2:.3f});')
    sfx(t_b2 - 0.1, "golpe", 0.4)
    shake(t_b2, 12)


# ================================================================= 4 · CUESTA × PASTOR
def scene_cuesta():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h4", fx, fy, "4", "CUESTA × PASTOR", color="#7c3aed", txt="#fff")
    add(f'<div id="ele" class="pill" style="{css_box(fx + 300, fy + 175, None, None, 8)}background:#fff;color:{INK};font-size:52px;opacity:0">'
        f'{icon("vote", 52, INK, 2.6)} ELECCIONES</div>')
    add(f'<div id="urn" class="urn" style="{css_box(fx + 380, fl - 250, 200, 230, 4)}opacity:0"><i class="slot"></i><b>URNA</b></div>')
    for k, x in enumerate([fx + 230, fx + 700]):
        add(f'<div id="bal{k}" class="ballot" style="{css_box(x, fl - 300, 60, 76, 9)}opacity:0"></div>')
    add(character("cu1", "juan", fx + 190, fl, 1.2, z=5))
    add(character("ps1", "pastor", fx + 770, fl, 1.2, z=5))
    nc = bubble("sbc", fx + 10, fy + 280, 470, "CUESTA", "Como presidente, propongo votar.", "#5d6474", "l", fs=44)
    nps = bubble("sbps", fx + 440, fy + 280, 510, "PASTOR", "Perdone, el presidente soy yo. Pero voto, faltaría más.", "#1e3a8a", "r", fs=42)
    rc, hc = roller("vc", "0", 150, INK)
    rp, hp = roller("vp", "0", 150, INK)
    add(f'''<div id="sco" class="card" style="{css_box(fx + 160, fy + 230, 640, 300, 9)}background:#fff;opacity:0">
      <div class="scol" style="left:0"><div class="scn">CUESTA</div>{rc}</div>
      <div class="scol" style="right:0"><div class="scn">PASTOR</div>{rp}</div><div class="scdash">–</div></div>''')
    add(f'<div id="selfv" class="pill" style="{css_box(fx + 70, fy + 560, None, None, 10)}background:{ACC};color:{INK};font-size:44px;opacity:0">'
        f'{icon("repeat", 44, INK, 2.8)} CADA UNO SE VOTA A SÍ MISMO</div>')
    add(f'<div id="emp" class="stampbox" style="{css_box(fx + 260, fy + 300, 440, 170, 11)}opacity:0">EMPATE</div>')
    t_cua, t_jua, t_enr, t_ele = P("cuatro", 2), P("juan"), P("enrique"), P("elecciones")
    travel(t_cua - 0.3, F(2, 0), 2, 570, dur=0.7)
    header_in("h4", t_cua, t_jua)
    life("cu1", 0, G.DUR, 7)
    life("ps1", 0, G.DUR, 8)
    js(f'tl.fromTo("#cu1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_jua:.3f});')
    js(f'tl.fromTo("#ps1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_enr:.3f});')
    pop("#ele", t_ele - 0.1, sound="pop2")
    js(f'tl.fromTo("#urn", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4, ease:"back.out(2)"}}, {t_ele + 0.2:.3f});')
    t_c3, t_vot, t_p2, t_per, t_soy, t_vo1 = P("cuesta", 3), P("votar"), P("pastor", 2), P("perdone"), P("soy"), P("voto")
    say("sbc", nc, "cu1", t_c3 + 0.25, E("votar"), from_x=-60)
    js(f'point("cu1", "R", {t_vot - 0.2:.3f}, {t_vot + 0.8:.3f}, -60);')
    js(f'tl.to("#sbc", {{opacity:0.25, scale:0.92, duration:0.3}}, {t_p2 - 0.3:.3f});')
    say("sbps", nps, "ps1", t_p2 + 0.25, E("mas"), from_x=60)
    js(f'tl.to(Q("ps1","armL"), {{rotation:40, svgOrigin:PIV.armL, duration:0.3, ease:"back.out(2)"}}, {t_soy - 0.1:.3f}); tl.to(Q("ps1","armL"), {{rotation:0, svgOrigin:PIV.armL, duration:0.3}}, {t_soy + 0.7:.3f});')
    js(f'tl.to(Q("cu1","brows"), {{y:-10, duration:0.2}}, {t_per:.3f}); tl.to(Q("cu1","brows"), {{y:0, duration:0.3}}, {t_soy + 1:.3f});')
    # las dos papeletas a la urna
    for k in range(2):
        js(f'tl.fromTo("#bal{k}", {{opacity:1, x:0, y:0, rotation:0}}, {{immediateRender:false, opacity:1, x:{(480 - 260) if k == 0 else (480 - 730)}, y:-10, rotation:{180 if k == 0 else -180}, duration:0.55, ease:"power2.out"}}, {t_vo1 + k * 0.25:.3f});')
        js(f'tl.to("#bal{k}", {{y:60, opacity:0, duration:0.25, ease:"power2.in"}}, {t_vo1 + 0.55 + k * 0.25:.3f});')
        sfx(t_vo1 + 0.6 + k * 0.25, "papel", 0.3)
    t_rec, t_v2, t_v3, t_cad, t_emp = P("recuento"), P("voto", 2), P("voto", 3), P("cada"), P("empate")
    js(f'tl.to("#sbc, #sbps, #ele", {{opacity:0, duration:0.25}}, {t_rec - 0.3:.3f});')
    slide_in("#sco", t_rec - 0.2, dy=-60)
    roll_set("vc", "0", hc)
    roll_set("vp", "0", hp)
    roll_to("vc", "1", hc, t_v2, dur=0.6)
    roll_to("vp", "1", hp, t_v3, dur=0.6)
    js(f'jump("cu1", {t_v2 + 0.2:.3f}, 30); jump("ps1", {t_v3 + 0.2:.3f}, 30);')
    pop("#selfv", t_cad - 0.1, sound="pop2")
    js(f'point("cu1", "L", {t_cad:.3f}, {t_emp:.3f}, 40); point("ps1", "R", {t_cad:.3f}, {t_emp:.3f}, -40);')
    stamp("#emp", t_emp - 0.25, rot=-10)


# ================================================================= MISMO ACTOR
def scene_actor():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    add(f'<div id="spot" class="spot" data-layout-ignore style="{css_box(fx + 180, fy + 160, 600, 920, 2)}opacity:0"></div>')
    add(character("cu2", "juan", fx + 290, fl, 1.1, z=5))
    add(character("ps2", "pastor", fx + 670, fl, 1.1, z=5))
    add(f'<div id="mac" class="pill" style="{css_box(fx + 260, fy + 180, None, None, 9)}background:{ACC};color:{INK};font-size:64px;opacity:0">'
        f'{icon("drama", 60, INK, 2.6)} MISMO ACTOR</div>')
    add(f'<div id="jlg" class="namepl" style="{css_box(fx + 200, fy + 330, 560, 120, 9)}opacity:0">JOSÉ LUIS GIL</div>')
    t_mej, t_dos, t_int, t_mis, t_jos = P("mejor"), P("dos", 3), P("interpreta"), P("mismo", 3), P("jose")
    travel(t_mej - 0.1, F(2, 1), 2, 1630, dur=0.6)
    life("cu2", 0, G.DUR, 9)
    life("ps2", 0, G.DUR, 10)
    js(f'tl.fromTo("#cu2", {{opacity:0, x:-120}}, {{opacity:1, x:0, duration:0.35}}, {t_mej + 0.1:.3f});')
    js(f'tl.fromTo("#ps2", {{opacity:0, x:120}}, {{opacity:1, x:0, duration:0.35}}, {t_dos:.3f});')
    js(f'tl.to(Q("cu2","head"), {{rotation:10, svgOrigin:PIV.head, duration:0.25}}, {t_int:.3f}); tl.to(Q("ps2","head"), {{rotation:-10, svgOrigin:PIV.head, duration:0.25}}, {t_int:.3f});')
    # se juntan en el centro: son la misma persona
    js(f'tl.to("#cu2", {{x:190, duration:0.45, ease:"power3.inOut"}}, {t_mis - 0.1:.3f}); tl.to("#ps2", {{x:-190, duration:0.45, ease:"power3.inOut"}}, {t_mis - 0.1:.3f});')
    js(f'tl.to("#ps2", {{opacity:0, duration:0.25}}, {t_mis + 0.3:.3f});')
    js(f'tl.fromTo("#spot", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_mis:.3f});')
    sfx(t_mis + 0.3, "golpe-climax", 0.4)
    pop("#mac", t_mis + 0.05, sound=None)
    pop("#jlg", t_jos - 0.1, sound="check")


# ================================================================= ENCUESTA FINAL
PAIRS = [("RECIO × MAURI", "#3b82c4"), ("BERTA × PALOMA", "#db2777"), ("FINA × MARISA", "#16a34a"), ("CUESTA × PASTOR", "#7c3aed")]


def scene_final():
    fx, fy, fw, fh = F(3, 1)
    rows = "".join(f'<div class="poll" style="top:{150 + k * 92}px"><span>{n}</span><i id="pb{k}" style="background:{c}"></i></div>'
                   for k, (n, c) in enumerate(PAIRS))
    add(f'''<div id="pollc" class="card" style="{css_box(fx + 40, fy + 180, 880, 560, 6)}background:#fff;opacity:0">
      <div class="polh">{icon("message-circle", 56, INK, 2.6)} ¿QUÉ CRUCE QUIERES VER?</div>{rows}</div>''')
    cta = "Yo quiero ver a…"
    add(f'''<div id="cbx" class="card" style="{css_box(fx + 40, fy + 780, 880, 170, 6)}background:#fff;opacity:0">
      <div id="ctt" class="ctt">{chars(cta, "kc")}</div><div id="pub" class="pubb">Publicar</div></div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 800, fy + 900, 90, 90, 12)}opacity:0">{icon("mouse-pointer-2", 90, "#fff", 2.4).replace("<svg", "<svg fill=\"#0f1115\"")}</div>')
    t_cru, t_gus, t_ver, t_leo, t_com = P("cruce"), P("gustaria"), P("ver"), P("leo"), P("comentarios")
    travel(E("gil") - 0.05, F(3, 1), 3, 1630, dur=0.6)
    slide_in("#pollc", t_cru - 0.2, dy=-60)
    js('tl.set("[id^=pb]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    for k, w in enumerate([0.9, 0.7, 0.55, 0.8]):
        js(f'tl.to("#pb{k}", {{scaleX:{w}, duration:0.4, ease:"back.out(1.6)"}}, {t_gus + k * 0.15:.3f});')
    sfx(t_gus, "pop2", 0.25)
    slide_in("#cbx", t_ver, dy=60, sound=None)
    type_on("#ctt .kc", len(cta), t_ver + 0.2, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:160, y:160}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    cam(E("comentarios") + 0.1, (0, 100, 2200, 3900), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 42px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.htitle {{ font-size:84px; top:22px; }}
.bld {{ border-radius:18px 18px 0 0; border:8px solid rgba(0,0,0,0.25); overflow:hidden; }}
.bsign {{ position:absolute; left:30px; right:30px; top:24px; height:70px; border-radius:14px; font:900 38px {FONT}; text-align:center; line-height:70px; white-space:nowrap; letter-spacing:-1px; }}
.win {{ position:absolute; width:70px; height:80px; border-radius:8px; opacity:0.9; }}
.bdoor {{ position:absolute; left:50%; bottom:0; width:110px; height:130px; margin-left:-55px; background:#0b0c10; border-radius:55px 55px 0 0; }}
.nbad {{ border-radius:50%; color:#fff; font:900 70px {FONT}; text-align:center; line-height:110px; box-shadow:0 10px 30px rgba(0,0,0,0.45); }}
.stampbox {{ font:900 110px {FONT}; color:{BAD}; border:12px solid {BAD}; border-radius:26px; background:rgba(255,255,255,0.92); text-align:center; line-height:146px; letter-spacing:-2px; }}
.sb {{ background:#fff; border:7px solid; border-radius:36px; padding:54px 30px 26px; box-shadow:0 18px 40px rgba(0,0,0,0.45); }}
.sb:after {{ content:""; position:absolute; bottom:-34px; width:0; height:0; border-left:24px solid transparent; border-right:24px solid transparent; border-top:34px solid #fff; }}
.sb.l:after {{ left:90px; }} .sb.r:after {{ right:110px; }} .sb.c:after {{ left:50%; margin-left:-24px; }}
.who {{ position:absolute; left:26px; top:-30px; padding:4px 22px; border-radius:999px; color:#fff; font:900 38px {FONT}; white-space:nowrap; }}
.sbt {{ font-weight:800; color:{INK}; line-height:1.18; }}
.kc {{ opacity:0; }}
.door3 {{ border-radius:16px 16px 0 0; background:linear-gradient(90deg,#6b4428,#7c4f30); border:10px solid #3f2a1d; }}
.door3 b {{ position:absolute; left:50%; top:36px; margin-left:-60px; width:120px; height:56px; border-radius:10px; background:#fde68a; color:#3f2a1d; font:900 38px {FONT}; text-align:center; line-height:56px; }}
.dpole {{ border-radius:13px; background:linear-gradient(90deg,#64748b,#94a3b8); }}
.dryer {{ border-radius:115px 115px 30px 30px; background:linear-gradient(#f9a8d4,#db2777); border:8px solid #9d174d; }}
.bk {{ position:absolute; left:0; right:0; height:34px; border-radius:10px; background:#a16207; }}
.bl {{ position:absolute; bottom:0; width:30px; height:110px; background:#3f3f46; border-radius:6px; }}
.mtt {{ position:absolute; left:0; right:0; top:28px; text-align:center; font:900 52px {FONT}; color:{INK}; white-space:nowrap; }}
.crn {{ position:absolute; left:0; right:0; top:110px; text-align:center; }}
.mtb {{ position:absolute; left:50px; right:50px; top:120px; height:60px; border-radius:30px; background:#e2e8f0; overflow:hidden; }}
.mtb i {{ position:absolute; left:0; top:0; bottom:0; width:100%; border-radius:30px; transform-origin:0% 50%; }}
.urn {{ border-radius:20px; background:rgba(186,230,253,0.25); border:8px solid #bae6fd; }}
.urn .slot {{ position:absolute; left:50%; top:-8px; width:100px; height:16px; margin-left:-50px; background:#0b1220; border-radius:8px; }}
.urn b {{ position:absolute; left:0; right:0; bottom:20px; text-align:center; font:900 40px {FONT}; color:#e0f2fe; }}
.ballot {{ border-radius:6px; background:#fff; border:4px solid #cbd5e1; }}
.scol {{ position:absolute; top:30px; width:50%; text-align:center; }}
.scn {{ font:900 50px {FONT}; color:#475569; }}
.scdash {{ position:absolute; left:0; right:0; top:120px; text-align:center; font:900 120px {FONT}; color:#94a3b8; }}
.spot {{ border-radius:50% 50% 12px 12px; background:radial-gradient(ellipse at 50% 30%, rgba(255,236,170,0.55), rgba(255,236,170,0.08) 60%, transparent 75%); }}
.namepl {{ border-radius:24px; background:#fff; color:{INK}; font:900 76px {FONT}; text-align:center; line-height:120px; white-space:nowrap; letter-spacing:-1px; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.polh svg {{ flex:none; }}
.polh {{ position:absolute; left:40px; right:40px; top:40px; display:flex; align-items:center; gap:18px; font:900 50px {FONT}; color:{INK}; white-space:nowrap; }}
.poll {{ position:absolute; left:40px; right:40px; height:70px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:420px; font:900 44px {FONT}; color:{INK}; white-space:nowrap; }}
.poll i {{ flex:1; height:40px; border-radius:20px; }}
.ctt {{ position:absolute; left:40px; top:52px; font:800 54px {FONT}; color:{INK}; white-space:nowrap; }}
.pubb {{ position:absolute; right:30px; top:40px; padding:12px 40px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 56px {FONT}; }}
"""


def build():
    world()
    scene_hook()
    scene_recio()
    scene_berta()
    scene_fina()
    scene_cuesta()
    scene_actor()
    scene_final()
