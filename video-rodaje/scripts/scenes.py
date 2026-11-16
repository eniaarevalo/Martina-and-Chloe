"""Escenas del vídeo «Lo que pasaba detrás de las cámaras de La que se avecina». Un solo mundo: camino en zigzag
(«¡Mauri!» -> Montepinar era un plató -> el conflicto -> cerrar el círculo -> risas de más -> el edificio nuevo -> encuesta)."""
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


# ================================================================= GANCHO: «¡Mauri!»
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    add(f'<div id="rec" class="rec" style="{css_box(fx + 700, fy + 150, 220, 80, 9)}opacity:0"><i id="recd"></i>REC</div>')
    add(f'<div id="clp" data-layout-ignore style="{css_box(fx + 40, fy + 130, 150, 150, 9)}opacity:0">{icon("clapperboard", 150, "#f8fafc", 2)}</div>')
    add(character("gil", "pastor", fx + 270, fl, 1.2, z=5))
    add(character("mer", "mauri", fx + 690, fl, 1.2, z=5))
    add(f'<div id="ngil" class="ntag" style="{css_box(fx + 120, fl - 40, 300, 60, 8)}opacity:0">JOSÉ LUIS GIL</div>')
    add(f'<div id="nmer" class="ntag" style="{css_box(fx + 550, fl - 40, 280, 60, 8)}opacity:0">LUIS MERLO</div>')
    nb = bubble("sbg", fx + 60, fy + 300, 380, "GIL", "¡Mauri!", "#1e3a8a", "l", fs=90)
    add(f'<div id="anh" class="pill" style="{css_box(fx + 300, fy + 480, None, None, 9)}background:#16a596;color:#fff;font-size:40px;opacity:0">'
        f'= AQUÍ NO HAY QUIEN VIVA</div>')
    for k, (x, y) in enumerate([(560, 360), (760, 300), (650, 220)]):
        add(f'<div id="ja{k}" class="ja" data-layout-ignore style="{css_box(fx + x, fy + y, 200, 90, 10)}opacity:0">JA JA</div>')
    add(f'<div id="tf" class="stampbox" style="{css_box(fx + 150, fy + 420, 660, 160, 11)}opacity:0;font-size:96px">TOMA FALSA</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: claqueta, REC y los dos actores entran
    js('tl.fromTo("#clp", {opacity:1, rotation:-25, scale:1.3}, {rotation:0, scale:1, duration:0.35, ease:"back.out(2)"}, 0);')
    sfx(0.3, "madera", 0.45)
    pop("#rec", 0.35, sound=None)
    js('tl.to("#recd", {opacity:0.2, duration:0.4, yoyo:true, repeat:-1, ease:"steps(1)"}, 0.5);')
    life("gil", 0, G.DUR, 1)
    life("mer", 0, G.DUR, 2)
    js('tl.fromTo("#gil", {opacity:0, x:-160}, {opacity:1, x:0, duration:0.45, ease:"power3.out"}, 0.1);')
    js('tl.fromTo("#mer", {opacity:0, x:160}, {opacity:1, x:0, duration:0.45, ease:"power3.out"}, 0.2);')
    t_jos, t_lla, t_mau, t_lui, t_per, t_aqu = P("jose"), P("llamo"), P("mauri"), P("luis", 2), P("personaje"), P("aqui")
    pop("#ngil", t_jos - 0.1, sound="pop2", vol=0.2)
    say("sbg", nb, "gil", t_mau, E("mauri") + 0.1, from_x=-40)
    js(f'point("gil", "R", {t_mau - 0.1:.3f}, {t_mau + 1.2:.3f}, -70);')
    sfx(t_mau, "golpe", 0.3)
    pop("#nmer", t_lui - 0.1, sound="pop2", vol=0.2)
    js(f'tl.to(Q("mer","brows"), {{y:-12, duration:0.2}}, {t_lui:.3f});')
    pop("#anh", t_aqu - 0.2, sound="pop")
    t_mer2, t_rei, t_tom = P("merlo", 2), P("reir"), P("tomas")
    js(f'tl.to("#sbg, #anh", {{opacity:0.2, duration:0.3}}, {t_mer2:.3f});')
    for k in range(3):
        js(f'tl.fromTo("#ja{k}", {{opacity:0, scale:0.4, y:20}}, {{opacity:1, scale:1, y:-30, duration:0.35, ease:"back.out(2)"}}, {t_rei - 0.4 + k * 0.18:.3f});')
    js(f'jump("mer", {t_rei - 0.4:.3f}, 40); jump("mer", {t_rei + 0.1:.3f}, 40); jump("mer", {t_rei + 0.6:.3f}, 40);')
    js(f'tl.to(Q("mer","mouth"), {{scaleY:2.6, svgOrigin:"120 134", duration:0.12, yoyo:true, repeat:9}}, {t_rei - 0.4:.3f});')
    js(f'tl.to(Q("gil","mouth"), {{scaleY:2.2, svgOrigin:"120 134", duration:0.12, yoyo:true, repeat:7}}, {t_rei:.3f});')
    sfx(t_rei - 0.3, "pop2", 0.3)
    stamp("#tf", t_tom - 0.2, rot=-8)


# ================================================================= 1 · MONTEPINAR ERA UN PLATÓ
def scene_plato():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "ERA UN PLATÓ", color="#facc15")
    building("mp", fx + 280, fy + 330, 400, 680, "MONTEPINAR", "#e2e8f0", "#38bdf8", "#0f766e", "#fff", z=4)
    add(f'''<div id="bkst" class="backs" style="{css_box(fx + 280, fy + 330, 400, 680, 4)}opacity:0">
      <i class="sc1"></i><i class="sc2"></i><b>DECORADO</b></div>''')
    for k, x in enumerate([fx + 30, fx + 760]):
        add(f'<div id="lm{k}" data-layout-ignore style="{css_box(x, fy + 250, 170, 170, 6)}opacity:0">{icon("lamp", 170, "#fde68a", 2.2)}</div>')
        add(f'<div id="cone{k}" class="cone {"l" if k == 0 else "r"}" data-layout-ignore style="{css_box(x + (30 if k == 0 else -330), fy + 380, 470, 620, 3)}opacity:0"></div>')
    t_pri, t_sec, t_mon, t_exi, t_dec, t_pla = P("primer"), P("secreto"), P("montepinar"), P("existia"), P("decorado"), P("plato")
    travel(t_pri - 0.3, F(0, 1), 0, 1630, dur=0.7)
    header_in("h1", t_pri, t_sec)
    js(f'tl.fromTo("#mp", {{opacity:0, y:80}}, {{opacity:1, y:0, duration:0.4, ease:"back.out(1.6)"}}, {t_mon - 0.2:.3f});')
    js(f'tl.to("#mp", {{x:10, duration:0.06, yoyo:true, repeat:5}}, {t_exi:.3f});')
    # gira y por detrás solo hay andamios
    js(f'tl.to("#mp", {{scaleX:0, duration:0.2, ease:"power2.in"}}, {t_dec - 0.2:.3f}); tl.set("#mp", {{opacity:0}}, {t_dec:.3f});')
    js(f'tl.fromTo("#bkst", {{opacity:1, scaleX:0}}, {{opacity:1, scaleX:1, duration:0.3, ease:"back.out(2)", immediateRender:false}}, {t_dec:.3f});')
    sfx(t_dec - 0.2, "whoosh-corto", 0.3)
    for k in range(2):
        pop(f"#lm{k}", t_pla - 0.5 + k * 0.1, sound="click" if k == 0 else None)
        js(f'tl.fromTo("#cone{k}", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_pla - 0.3 + k * 0.1:.3f});')


# ================================================================= EL CONFLICTO
def scene_conflicto():
    fx, fy, fw, fh = F(1, 1)
    header("h2", fx, fy, "!", "EL CONFLICTO", color="#ef4444", txt="#fff")
    chip("prd", fx + 40, fy + 300, "film", "PRODUCTORES", "#fff", INK, fs=46)
    chip("due", fx + 420, fy + 470, "building-2", "DUEÑOS DEL PLATÓ", "#fff", INK, fs=46)
    add(f'<div id="zc" data-layout-ignore style="{css_box(fx + 400, fy + 330, 150, 150, 9)}opacity:0">'
        f'{icon("zap", 150, ACC, 2.4).replace("<svg", "<svg fill=\"#ffd43b\"")}</div>')
    add(f'<div id="exit" data-layout-ignore style="{css_box(fx + 330, fy + 640, 300, 300, 5)}opacity:0">{icon("door-open", 300, "#f8fafc", 1.8)}</div>')
    add(f'<div id="adi" class="pill" style="{css_box(fx + 200, fy + 960, None, None, 9)}background:{BAD};color:#fff;font-size:52px;opacity:0">ADIÓS, MONTEPINAR</div>')
    t_y, t_tuv, t_dej, t_con, t_pro, t_due, t_pla2 = P("y", 2), P("tuvieron"), P("dejarlo"), P("conflicto"), P("productores"), P("duenos"), P("plato", 2)
    travel(t_tuv - 0.35, F(1, 1), 1, 1630, dur=0.7)
    header_in("h2", t_tuv - 0.1, t_dej)
    slide_in("#prd", t_pro - 0.2, dx=-80, dy=0)
    slide_in("#due", t_due - 0.2, dx=80, dy=0)
    js(f'tl.fromTo("#zc", {{opacity:0, scale:0.3, rotation:-30}}, {{opacity:1, scale:1, rotation:0, duration:0.25, ease:"back.out(3)"}}, {t_con:.3f});')
    sfx(t_con, "golpe", 0.4)
    shake(t_con + 0.05, 12)
    js(f'tl.to("#prd", {{x:-20, duration:0.08, yoyo:true, repeat:5}}, {t_due + 0.2:.3f}); tl.to("#due", {{x:20, duration:0.08, yoyo:true, repeat:5}}, {t_due + 0.2:.3f});')
    pop("#exit", t_dej - 0.1, sound="puerta", vol=0.3)
    stamp("#adi", t_pla2 - 0.2, rot=-4)


# ================================================================= CERRAR EL CÍRCULO
def scene_circulo():
    fx, fy, fw, fh = F(1, 0)
    header("h3", fx, fy, "○", "CERRAR EL CÍRCULO", color="#16a596", txt="#fff")
    add(f'''<div id="gho" class="ghostp" style="{css_box(fx + 230, fy + 380, 500, 560, 3)}opacity:0">
      <div class="ghl">PORTAL DE<br>AQUÍ NO HAY<br>QUIEN VIVA</div></div>''')
    building("mp2", fx + 350, fy + 520, 260, 400, "MONTEPINAR", "#e2e8f0", "#38bdf8", "#0f766e", "#fff", z=5)
    add(f'''<svg id="circ" data-layout-ignore style="{css_box(fx + 130, fy + 250, 700, 820, 8)}overflow:visible" viewBox="0 0 700 820">
      <ellipse id="cel" cx="350" cy="410" rx="330" ry="390" fill="none" stroke="#facc15" stroke-width="16" stroke-linecap="round"/></svg>''')
    add(f'<div id="acq" class="pill" style="{css_box(fx + 110, fy + 190, None, None, 10)}background:#fff;color:{INK};font-size:44px;opacity:0">'
        f'{icon("quote", 42, INK, 2.6)} ALBERTO CABALLERO</div>')
    C = 2 * 3.1416 * ((330 + 390) / 2)
    t_ant, t_ult, t_mon, t_gra, t_por, t_aqu, t_alb, t_cer, t_cir = (P("antes"), P("ultimas"), P("montepinar", 2), P("grabaron"), P("portal"),
                                                                     P("aqui", 2), P("alberto"), P("cerrar"), P("circulo"))
    travel(t_ant - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h3", t_ant, t_ant + 0.3)
    js(f'tl.fromTo("#gho", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_ult - 0.2:.3f});')
    js(f'tl.fromTo("#mp2", {{opacity:0, y:-500}}, {{opacity:1, y:0, duration:0.55, ease:"bounce.out"}}, {t_mon - 0.1:.3f});')
    sfx(t_mon + 0.3, "golpe", 0.3)
    js(f'tl.to("#mp2", {{opacity:0.25, duration:0.4}}, {t_por - 0.2:.3f});')
    js(f'tl.to("#gho", {{borderColor:"#facc15", duration:0.3}}, {t_por:.3f}); tl.to("#gho .ghl", {{color:"#facc15", scale:1.08, duration:0.3}}, {t_aqu:.3f});')
    sfx(t_por, "pop2", 0.3)
    pop("#acq", t_alb - 0.1, sound="pop")
    js(f'tl.set("#cel", {{strokeDasharray:{C:.0f}, strokeDashoffset:{C:.0f}, opacity:0}}, 0); tl.set("#cel", {{opacity:1}}, {t_cer - 0.1:.3f});')
    js(f'tl.to("#cel", {{strokeDashoffset:0, duration:{t_cir - t_cer + 0.5:.2f}, ease:"power2.inOut"}}, {t_cer - 0.1:.3f});')
    sfx(t_cir + 0.4, "check", 0.4)


# ================================================================= 2 · RISAS DE MÁS
def scene_risas():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h4", fx, fy, "2", "RISAS DE MÁS", color="#ec4899", txt="#fff")
    chip("mgo", fx + 40, fy + 190, "message-circle", "MACARENA GÓMEZ LO CONTÓ", "#fff", INK, fs=42)
    add(character("a1", "g2", fx + 230, fl, 1.15, z=5))
    add(character("a2", "g1", fx + 520, fl, 1.15, z=5))
    add(f'<div id="cmr" data-layout-ignore style="{css_box(fx + 720, fl - 330, 200, 200, 6)}opacity:0">{icon("video", 200, "#f8fafc", 2)}</div>')
    for k, (x, y) in enumerate([(60, 330), (600, 300), (330, 420)]):
        add(f'<div id="jr{k}" class="ja" data-layout-ignore style="{css_box(fx + x, fy + y, 220, 90, 10)}opacity:0">JA JA JA</div>')
    add(f'<div id="sal" class="pill" style="{css_box(fx + 330, fy + 560, None, None, 11)}background:{ACC};color:{INK};font-size:50px;opacity:0">'
        f'{icon("film", 48, INK, 2.6)} TOMAS FALSAS</div>')
    t_seg, t_mac, t_com, t_exa, t_ris, t_sab, t_tom = P("segundo"), P("macarena"), P("companeros"), P("exageran"), P("risa"), P("saben"), P("tomas", 2)
    travel(t_seg - 0.3, F(2, 0), 2, 570, dur=0.7)
    header_in("h4", t_seg, t_mac)
    pop("#mgo", t_mac + 0.1, sound="pop2")
    life("a1", 0, G.DUR, 3)
    life("a2", 0, G.DUR, 4)
    js(f'tl.fromTo("#a1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_com - 0.1:.3f});')
    js(f'tl.fromTo("#a2", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_com + 0.1:.3f});')
    for k in range(3):
        js(f'tl.fromTo("#jr{k}", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2.5)"}}, {t_exa + k * 0.15:.3f});')
        js(f'tl.to("#jr{k}", {{rotation:{(-1) ** k * 8}, duration:0.12, yoyo:true, repeat:7}}, {t_exa + 0.3 + k * 0.15:.3f});')
    for c, d in (("a1", 0), ("a2", 0.15)):
        js(f'jump("{c}", {t_exa + d:.3f}, 50); jump("{c}", {t_ris + d:.3f}, 50); jump("{c}", {t_sab + d:.3f}, 50);')
        js(f'tl.to(Q("{c}","mouth"), {{scaleY:2.8, svgOrigin:"120 134", duration:0.12, yoyo:true, repeat:15}}, {t_exa + d:.3f});')
    sfx(t_exa, "pop2", 0.3)
    pop("#cmr", t_sab - 0.2, sound="click")
    js(f'tl.to("#a1", {{x:120, duration:0.4}}, {t_sab:.3f}); tl.to("#a2", {{x:120, duration:0.4}}, {t_sab + 0.1:.3f});')
    stamp("#sal", t_tom - 0.2, rot=-5)


# ================================================================= EL EDIFICIO NUEVO
def scene_edificio():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h5", fx, fy, "+", "EL EDIFICIO NUEVO", color="#38bdf8")
    slabs = "".join(f'<i class="slab" id="sl{k}" style="bottom:{k * 62}px"></i>' for k in range(11))
    add(f'<div id="twr" class="twr" data-layout-ignore style="{css_box(fx + 390, fl - 700, 250, 690, 4)}">{slabs}</div>')
    rr, hh = roller("np", "00", 120, INK)
    add(f'<div id="npc" class="card" style="{css_box(fx + 660, fy + 300, 280, 230, 8)}background:#fff;opacity:0"><div class="npn">{rr}</div><div class="npl">PISOS</div></div>')
    chip("pat", fx + 20, fy + 330, "trees", "2 PATIOS", "#fff", INK, fs=42)
    chip("bar", fx + 20, fy + 500, "beer", "¡Y UN BAR!", ACC, INK, fs=42)
    t_nue, t_con, t_ent, t_onc, t_pat, t_bar = P("nueva"), P("construyeron"), P("entero"), P("once"), P("patios"), P("bar")
    travel(t_nue - 0.4, F(2, 1), 2, 1630, dur=0.6)
    header_in("h5", t_nue - 0.1, t_con)
    js('tl.set(".slab", {scaleY:0, transformOrigin:"50% 100%"}, 0);')
    for k in range(11):
        tt = t_con + (t_onc + 0.3 - t_con) * k / 11
        js(f'tl.to("#sl{k}", {{scaleY:1, duration:0.15, ease:"back.out(2)"}}, {tt:.3f});')
    sfx(t_con, "tic-rodillo", 0.3)
    slide_in("#npc", t_ent - 0.2, dx=60, dy=0)
    roll_set("np", "00", hh)
    roll_to("np", "11", hh, t_onc - 0.1, dur=0.6, spins=1)
    pop("#pat", t_pat - 0.2, sound="pop2")
    pop("#bar", t_bar - 0.3, sound="check")
    js(f'tl.to("#bar", {{rotation:-6, duration:0.1, yoyo:true, repeat:3}}, {t_bar + 0.2:.3f});')


# ================================================================= ENCUESTA FINAL
OPTS = [("GIL LLAMA «MAURI» A MERLO", "#1e3a8a"), ("MONTEPINAR ERA UN PLATÓ", "#facc15"),
        ("CERRAR EL CÍRCULO", "#16a596"), ("RISAS DE MÁS", "#ec4899")]


def scene_final():
    fx, fy, fw, fh = F(3, 1)
    rows = "".join(f'<div class="poll" style="top:{140 + k * 86}px"><span>{n}</span><i id="pb{k}" style="background:{c}"></i></div>'
                   for k, (n, c) in enumerate(OPTS))
    add(f'''<div id="pollc" class="card" style="{css_box(fx + 40, fy + 220, 880, 520, 6)}background:#fff;opacity:0">
      <div class="polh">{icon("message-circle", 54, INK, 2.6)} ¿CUÁL NO SABÍAS?</div>{rows}</div>''')
    cta = "Yo no sabía lo de…"
    add(f'''<div id="cbx" class="card" style="{css_box(fx + 40, fy + 780, 880, 170, 6)}background:#fff;opacity:0">
      <div id="ctt" class="ctt">{chars(cta, "kc")}</div><div id="pub" class="pubb">Publicar</div></div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 800, fy + 900, 90, 90, 12)}opacity:0">{icon("mouse-pointer-2", 90, "#fff", 2.4).replace("<svg", "<svg fill=\"#0f1115\"")}</div>')
    t_cua, t_sab, t_leo, t_com = P("cual"), P("sabias"), P("leo"), P("comentarios")
    travel(t_cua - 0.35, F(3, 1), 3, 1630, dur=0.6)
    slide_in("#pollc", t_cua - 0.1, dy=-60)
    js('tl.set("[id^=pb]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    for k, w in enumerate([0.9, 0.6, 0.75, 0.5]):
        js(f'tl.to("#pb{k}", {{scaleX:{w}, duration:0.35, ease:"back.out(1.6)"}}, {t_sab - 0.2 + k * 0.12:.3f});')
    sfx(t_sab, "pop2", 0.25)
    slide_in("#cbx", t_sab + 0.2, dy=60, sound=None)
    type_on("#ctt .kc", len(cta), t_leo - 0.2, t_com + 0.3)
    js(f'tl.fromTo("#cur", {{opacity:0, x:160, y:160}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.4:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.4:.3f});')
    sfx(t_com + 0.4, "click", 0.5)
    cam(E("comentarios") + 0.1, (0, 100, 2200, 3900), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.htitle {{ font-size:72px; top:30px; }}
.stampbox {{ font:900 100px {FONT}; color:{BAD}; border:12px solid {BAD}; border-radius:26px; background:rgba(255,255,255,0.94);
  display:flex; align-items:center; justify-content:center; gap:16px; letter-spacing:-2px; white-space:nowrap; }}
.rec {{ border-radius:999px; background:#111827; border:5px solid #ef4444; color:#fff; font:900 50px {FONT}; display:flex; align-items:center; justify-content:center; gap:14px; }}
.rec i {{ width:30px; height:30px; border-radius:50%; background:#ef4444; display:block; }}
.ntag {{ border-radius:14px; background:#0f172a; border:4px solid #fff; color:#fff; font:900 34px {FONT}; text-align:center; line-height:52px; white-space:nowrap; }}
.ja {{ font:900 64px {FONT}; color:{ACC}; text-shadow:0 6px 0 #b45309; white-space:nowrap; text-align:center; }}
.sb {{ background:#fff; border:7px solid; border-radius:36px; padding:54px 30px 26px; box-shadow:0 18px 40px rgba(0,0,0,0.45); }}
.sb:after {{ content:""; position:absolute; bottom:-34px; width:0; height:0; border-left:24px solid transparent; border-right:24px solid transparent; border-top:34px solid #fff; }}
.sb.l:after {{ left:90px; }} .sb.r:after {{ right:110px; }} .sb.c:after {{ left:50%; margin-left:-24px; }}
.who {{ position:absolute; left:26px; top:-30px; padding:4px 22px; border-radius:999px; color:#fff; font:900 38px {FONT}; white-space:nowrap; }}
.sbt {{ font-weight:900; color:{INK}; line-height:1.1; }}
.kc {{ opacity:0; }}
.bld {{ border-radius:18px 18px 0 0; border:8px solid rgba(0,0,0,0.25); overflow:hidden; }}
.bsign {{ position:absolute; left:24px; right:24px; top:24px; height:70px; border-radius:14px; font:900 34px {FONT}; text-align:center; line-height:70px; white-space:nowrap; letter-spacing:-1px; }}
.win {{ position:absolute; width:62px; height:76px; border-radius:8px; opacity:0.9; }}
.bdoor {{ position:absolute; left:50%; bottom:0; width:110px; height:130px; margin-left:-55px; background:#0b0c10; border-radius:55px 55px 0 0; }}
.backs {{ border-radius:18px 18px 0 0; background:repeating-linear-gradient(90deg, #3f3f46 0 14px, transparent 14px 120px), #1f2937; border:8px solid #52525b; overflow:hidden; }}
.backs .sc1, .backs .sc2 {{ position:absolute; left:-40px; right:-40px; height:14px; background:#71717a; }}
.backs .sc1 {{ top:220px; transform:rotate(30deg); }} .backs .sc2 {{ top:420px; transform:rotate(-30deg); }}
.backs b {{ position:absolute; left:0; right:0; bottom:40px; text-align:center; font:900 50px {FONT}; color:#fde68a; letter-spacing:2px; }}
.cone {{ background:linear-gradient(rgba(253,230,138,0.35), rgba(253,230,138,0)); }}
.cone.l {{ clip-path:polygon(0 0, 18% 0, 100% 100%, 30% 100%); }}
.cone.r {{ clip-path:polygon(82% 0, 100% 0, 70% 100%, 0 100%); }}
.ghostp {{ border:10px dashed rgba(255,255,255,0.35); border-radius:24px; }}
.ghl {{ position:absolute; left:0; right:0; bottom:20px; text-align:center; font:900 40px {FONT}; color:rgba(255,255,255,0.55); line-height:1.15; }}
.twr {{ }}
#mp2 .bsign {{ font-size:26px; left:14px; right:14px; }}
.slab {{ position:absolute; left:0; right:0; height:56px; border-radius:8px; background:linear-gradient(90deg,#e2e8f0,#cbd5e1);
  box-shadow:inset 0 -8px 0 #94a3b8; }}
.npn {{ position:absolute; left:0; right:0; top:20px; text-align:center; }}
.npl {{ position:absolute; left:0; right:0; bottom:20px; text-align:center; font:900 46px {FONT}; color:#475569; }}
.polh svg {{ flex:none; }}
.polh {{ position:absolute; left:40px; right:40px; top:40px; display:flex; align-items:center; gap:18px; font:900 50px {FONT}; color:{INK}; white-space:nowrap; }}
.poll {{ position:absolute; left:40px; right:40px; height:70px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:540px; flex:none; font:900 34px {FONT}; color:{INK}; white-space:nowrap; }}
.poll i {{ flex:1; height:36px; border-radius:18px; }}
.ctt {{ position:absolute; left:40px; top:52px; font:800 50px {FONT}; color:{INK}; white-space:nowrap; }}
.pubb {{ position:absolute; right:30px; top:40px; padding:12px 40px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 56px {FONT}; }}
"""


def build():
    world()
    scene_hook()
    scene_plato()
    scene_conflicto()
    scene_circulo()
    scene_risas()
    scene_edificio()
    scene_final()
