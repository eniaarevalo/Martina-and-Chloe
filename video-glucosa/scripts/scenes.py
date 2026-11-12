"""Escenas del vídeo «Picos de glucosa: qué son, por qué importan y cómo reducirlos». Un solo mundo:
un camino en zigzag (qué es -> por qué importa -> cómo reducirlos) que se dibuja mientras viaja la cámara."""
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
WIN_W, WIN_H = 52, 78


def facade(fid, x, y, w, h, n_win=6, floors=4, signs=("BANCO", "VIDEOCLUB"), z=4, scale_win=1.0, signs_b=("", "")):
    """Fachada del edificio: cuerpo ocre, cornisa, balcones y dos locales abajo.
    Cada ventana es una pieza con id para poder moverla o encogerla en su sitio."""
    fh = (h - 230) / floors
    parts = [f'<div class="fbody"></div><div class="fcorn"></div>']
    for f in range(floors):
        fy = 60 + f * fh
        parts.append(f'<div id="{fid}-fl{f}" class="ffloor" style="top:{fy:.0f}px;height:{fh:.0f}px">')
        for i in range(n_win):
            cx = (i + 0.5) * w / n_win
            ww, wh = WIN_W * scale_win, WIN_H * scale_win
            parts.append(f'<div id="{fid}-w{f}-{i}" class="fwin" style="left:{cx - ww / 2:.0f}px;top:{fh * 0.18:.0f}px;'
                         f'width:{ww:.0f}px;height:{wh:.0f}px"><div class="frail"></div></div>')
        parts.append('</div>')
    sy = h - 170
    for k, s in enumerate(signs):
        parts.append(f'<div id="{fid}-sg{k}" class="fshop" style="left:{20 + k * (w / 2):.0f}px;top:{sy:.0f}px;width:{w / 2 - 40:.0f}px">'
                     f'<div class="fsign"><span id="{fid}-sa{k}" class="sgt">{s}</span><span id="{fid}-sb{k}" class="sgt" style="opacity:0">{signs_b[k]}</span></div><div class="fdoor"></div></div>')
    add(f'<div id="{fid}" class="facade" style="{css_box(x, y, w, h, z)}">{"".join(parts)}</div>')
    return fh






# ================================================================= PIEZAS
def chart(cid, x, y, w, h, paths, line140=True, z=6, title=None):
    """Tarjeta con gráfica de glucosa. paths = [(id, d, color)] en coordenadas 0..w-60 x 0..h-?"""
    gw, gh = w - 80, h - (130 if title else 70)
    lines = "".join(f'<path id="{pid}" d="{d}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                    for pid, d, col in paths)
    l140 = (f'<path d="M 0 {gh * 0.35:.0f} L {gw} {gh * 0.35:.0f}" stroke="#94a3b8" stroke-width="5" stroke-dasharray="16 12"/>'
            f'<text x="{gw - 10}" y="{gh * 0.35 - 14:.0f}" text-anchor="end" font-family="{FONT}" font-weight="900" font-size="46" fill="#64748b">140</text>') if line140 else ""
    ttl = f'<div style="position:absolute;left:40px;top:26px;font:900 54px {FONT};color:{INK}">{title}</div>' if title else ""
    card(cid, x, y, w, h, f'''{ttl}
      <svg style="position:absolute;left:40px;top:{110 if title else 40}px;overflow:visible" width="{gw}" height="{gh}" viewBox="0 0 {gw} {gh}">
        <path d="M 0 {gh} L {gw} {gh}" stroke="#e5e7eb" stroke-width="6"/>{l140}{lines}</svg>''', z=z)
    return gw, gh


def draw(pid, t, dur=0.8, length=2000):
    js(f'tl.set("#{pid}", {{strokeDasharray:{length}, strokeDashoffset:{length}}}, 0);')
    js(f'tl.to("#{pid}", {{strokeDashoffset:0, duration:{dur}, ease:"power2.inOut"}}, {t:.3f});')


def food(fid, name, x, y, size, color, z=7, fill=None):
    svg = icon(name, size, color, 2.2)
    if fill:
        svg = svg.replace("<svg", f'<svg fill="{fill}"')
    add(f'<div id="{fid}" class="food" style="{css_box(x, y, size, size, z)}">{svg}</div>')


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#f43f5e"/><stop offset="0.5" stop-color="#facc15"/><stop offset="1" stop-color="#22c55e"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in [("Qué es", 0, 1630), ("Por qué importa", 1, 570), ("Cómo reducirlos", 2, 1630), ("Tu próxima comida", 3, 570)]:
        add(f'<div class="mile" data-layout-ignore style="{css_box(x - 250, ROAD[r] + 34, 500, 70, 2)}">{lab}</div>')


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    gw, gh = chart("ch0", fx + 40, fy + 20, 880, 430, [("c0", "M 0 300 C 120 300 160 20 260 20 C 360 20 380 340 520 340 C 620 340 680 290 800 290", BAD)], line140=False)
    add(f'<div id="tag0" class="tagr" style="{css_box(fx + 200, fy + 470, None, None, 8)}background:{BAD}">PICO DE GLUCOSA</div>')
    add(character("p0", "g2", fx + 330, fl, 1.25, z=5))
    add(f'<div class="table" style="{css_box(fx + 80, fl - 230, 800, 40, 6)}"></div><div class="tleg" style="{css_box(fx + 140, fl - 190, 30, 190, 5)}"></div><div class="tleg" style="{css_box(fx + 790, fl - 190, 30, 190, 5)}"></div>')
    food("plate0", "utensils", fx + 520, fl - 360, 130, "#e5e7eb")
    add(f'<div id="zz0" class="zz" style="{css_box(fx + 420, fl - 640, 140, 140, 9)}">Z</div>')
    cam(0, (fx + 60, fy + 380, 840, 700), whoosh=False)
    cam(0.1, F(0, 0), dur=0.9, ease="power3.inOut", whoosh=False)
    sfx(0.0, "whoosh", 0.4)
    life("p0", 0, G.DUR, 1)
    js(f'tl.fromTo("#ch0", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.35}}, 0.05);')
    draw("c0", 0.15, dur=1.6)
    t_baj, t_com, t_pic = P("bajon"), P("comer"), P("pico")
    # bosteza: ojos se cierran y cabeza cae
    js(f'tl.to(Q("p0","eyes"), {{scaleY:0.15, svgOrigin:PIV.eyes, duration:0.3}}, {t_baj:.3f}); tl.to(Q("p0","head"), {{rotation:14, svgOrigin:PIV.head, duration:0.5}}, {t_baj:.3f});')
    js(f'tl.fromTo("#zz0", {{opacity:0, y:30, scale:0.5}}, {{opacity:1, y:-40, scale:1, duration:0.6}}, {t_com:.3f}); tl.to("#zz0", {{opacity:0, y:-120, duration:0.6}}, {t_com + 1.0:.3f});')
    sfx(t_baj, "pop2", 0.25)
    stamp("#tag0", t_pic, rot=-5)
    js(f'tl.to(Q("p0","eyes"), {{scaleY:1, svgOrigin:PIV.eyes, duration:0.2}}, {t_pic + 0.5:.3f}); tl.to(Q("p0","head"), {{rotation:0, svgOrigin:PIV.head, duration:0.3}}, {t_pic + 0.5:.3f});')


# ================================================================= 1 · QUÉ ES
def scene_que():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "QUÉ ES")
    num, nh = roller("gl", "000", 130, INK)
    add(f'''<div id="phone" class="phone" style="{css_box(fx + 30, fy + 170, 360, 640, 6)}">
      <div class="pnotch"></div><div style="margin-top:90px;text-align:center;font:800 46px {FONT};color:#64748b">Glucosa</div>
      <div style="text-align:center">{num}</div><div style="text-align:center;font:800 46px {FONT};color:#64748b">mg/dL</div>
      <div id="okg" class="okb2" style="background:{GOOD_BG}">{icon("check", 60, "#fff", 3.4)}</div></div>''')
    gw, gh = chart("ch1", fx + 420, fy + 170, 540, 640, [
        ("c1a", "M 0 470 C 90 470 130 260 210 260 C 290 260 330 470 460 470", GOOD),
        ("c1b", "M 0 470 C 70 470 100 20 170 20 C 240 20 260 520 460 520", BAD)])
    add(f'<div id="clk" class="pill" style="{css_box(fx + 520, fy + 840, None, None, 8)}background:#fff;color:{INK}">{icon("clock", 50, INK, 2.6)} 2-3 h</div>')
    food("donut", "donut", fx + 60, fy + 850, 170, "#be185d", fill="#f9a8d4")
    food("bread", "croissant", fx + 260, fy + 850, 170, "#92400e", fill="#fcd34d")
    t_uno, t_que, t_com, t_sub, t_nor = P("uno"), P("que"), P("comes"), P("sube"), P("normal")
    travel(t_uno, F(0, 1), 0, 1630, dur=0.85)
    header_in("h1", t_uno, t_que)
    pop("#phone", t_com, sound="pop")
    roll_set("gl", "090", nh)
    js(f'tl.set("#gl-d1", {{y:{-9 * nh}}}, 0);')
    roll_to("gl", "120", nh, t_sub, dur=0.7)
    pop("#okg", t_nor, sound="check", vol=0.35)
    pop("#ch1", t_sub, sound=None)
    draw("c1a", t_sub + 0.1, dur=1.0)
    js('tl.set("#c1b", {opacity:0}, 0);')
    t_san, t_140, t_hor = P("sana"), P("140"), P("horas")
    js(f'tl.to("#ch1 svg", {{scale:1.04, transformOrigin:"50% 35%", duration:0.2, yoyo:true, repeat:1}}, {t_140:.3f});')
    sfx(t_140, "pop2", 0.3)
    pop("#clk", P("baja") , sound="pop2")
    # 3: un pico
    t_pic, t_bru, t_har, t_dul = P("pico", 2), P("brusca"), P("harinas"), P("dulces")
    js(f'tl.set("#c1b", {{opacity:1}}, {t_pic:.3f});')
    draw("c1b", t_pic, dur=0.9)
    js(f'tl.to("#gl-d0", {{y:{-(10 + 1) * nh}, duration:0.4}}, {t_bru:.3f}); tl.to("#gl-d1", {{y:{-(10 + 8) * nh}, duration:0.5}}, {t_bru:.3f}); tl.to("#gl-d2", {{y:{-(10 + 5) * nh}, duration:0.6}}, {t_bru:.3f});')
    js(f'tl.to("#okg", {{backgroundColor:"{BAD}", rotation:180, duration:0.3}}, {t_bru:.3f});')
    shake(t_bru + 0.1, 10)
    pop("#bread", t_har, sound="pop")
    pop("#donut", t_dul, sound="pop")
    cam(E("dulces") + 0.05, ROW(0), dur=0.45)


# ================================================================= 2 · POR QUÉ IMPORTA
def scene_importa():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    header("h2", fx, fy, "2", "POR QUÉ IMPORTA")
    gw, gh = chart("ch2", fx + 40, fy + 170, 880, 400, [("c2", "M 0 250 C 120 250 160 20 280 20 C 400 20 420 320 560 320 C 660 320 700 250 800 250", BAD)], line140=False)
    add(f'<div id="dip" class="pill" style="{css_box(fx + 520, fy + 520, None, None, 8)}background:{BAD};color:#fff">BAJÓN</div>')
    add(character("p1", "g2", fx + 230, fl, 1.1, z=5))
    add(f'<div id="zz1" class="zz" style="{css_box(fx + 300, fl - 600, 120, 120, 9)}">Z</div>')
    card("st21", fx + 440, fy + 640, 520, 230, f'''
      <div style="position:absolute;left:30px;top:30px">{icon("users", 90, INK, 2.2)}</div>
      <div style="position:absolute;left:140px;top:24px;font:900 64px {FONT};color:{INK}">2021</div>
      <div style="position:absolute;left:140px;top:112px;font:800 46px {FONT};color:#555;white-space:nowrap">1.070 personas</div>''')
    for i, txt in enumerate(["Más hambre", "Más calorías"]):
        add(f'''<div id="hn{i}" class="notif" style="{css_box(fx + 440, fy + 900 + i * 0, 520, 110, 8)}">
          <div class="nicon" style="background:{BAD}">{icon("cookie", 54, "#fff", 2.6)}</div><span>{txt}</span></div>''')
    t_dos, t_imp, t_tra, t_gra, t_baj = P("dos"), P("importa"), P("tras"), P("grande"), P("bajon", 2)
    travel(t_dos, F(1, 1), 1, 1630, dur=0.85)
    header_in("h2", t_dos, t_imp)
    pop("#ch2", t_tra, sound="pop2")
    draw("c2", t_gra - 0.2, dur=1.2)
    pop("#dip", t_baj, sound="golpe", vol=0.3)
    life("p1", 0, G.DUR, 2)
    js(f'tl.to(Q("p1","eyes"), {{scaleY:0.15, svgOrigin:PIV.eyes, duration:0.3}}, {t_baj:.3f}); tl.to(Q("p1","head"), {{rotation:14, svgOrigin:PIV.head, duration:0.5}}, {t_baj:.3f});')
    js(f'tl.fromTo("#zz1", {{opacity:0, y:30}}, {{opacity:1, y:-40, duration:0.6}}, {t_baj + 0.2:.3f}); tl.to("#zz1", {{opacity:0, y:-120, duration:0.5}}, {t_baj + 1.1:.3f});')
    t_est, t_21, t_mil, t_ham, t_cal = P("estudio"), P("2021"), P("mil"), P("hambre"), P("calorias")
    slide_in("#st21", t_est, dy=60)
    js(f'tl.to(Q("p1","eyes"), {{scaleY:1, svgOrigin:PIV.eyes, duration:0.2}}, {t_est:.3f}); tl.to(Q("p1","head"), {{rotation:0, svgOrigin:PIV.head, duration:0.3}}, {t_est:.3f});')
    js(f'tl.fromTo("#hn0", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_ham:.3f});')
    js(f'tl.to("#hn0", {{y:-10, scale:0.92, opacity:0, duration:0.25}}, {t_cal - 0.05:.3f}); tl.fromTo("#hn1", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_cal:.3f});')
    sfx(t_ham, "pop2", 0.3)
    sfx(t_cal, "pop2", 0.3)
    js(f'tl.to(Q("p1","upper"), {{keyframes:[{{x:-6}},{{x:6}},{{x:-4}},{{x:0}}], duration:0.35}}, {t_ham + 0.1:.3f});')


def scene_salud():
    fx, fy, fw, fh = F(1, 0)
    gw, gh = chart("ch3", fx + 40, fy + 40, 880, 360, [("c3", "M 0 230 L 90 30 L 180 230 L 270 30 L 360 230 L 450 30 L 540 230 L 630 30 L 720 230 L 800 120", BAD)], line140=False)
    card("dia", fx + 40, fy + 440, 880, 260, f'''
      <div style="position:absolute;left:36px;top:46px">{icon("siren", 130, BAD, 2.2)}</div>
      <div style="position:absolute;left:200px;top:40px;font:900 70px {FONT};color:{INK}">CON DIABETES</div>
      <div style="position:absolute;left:200px;top:140px;font:800 52px {FONT};color:{BAD}">Complicaciones</div>''')
    card("san", fx + 40, fy + 740, 880, 260, f'''
      <div style="position:absolute;left:36px;top:46px">{icon("microscope", 130, INK, 2.2)}</div>
      <div style="position:absolute;left:200px;top:40px;font:900 70px {FONT};color:{INK}">GENTE SANA</div>
      <div id="enest" class="pill" style="position:absolute;left:200px;top:140px;background:{ACC};color:{INK};opacity:0">EN ESTUDIO</div>''')
    t_y, t_dia, t_rep, t_com = P("personas", 2) - 0.3, P("diabetes"), P("repetidos"), P("complicaciones")
    travel(t_y, F(1, 0), 1, 570, dur=0.75)
    pop("#dia", t_dia, sound="pop")
    pop("#ch3", t_rep - 0.1, sound=None)
    draw("c3", t_rep, dur=0.9)
    js(f'tl.to("#dia", {{keyframes:[{{x:-8}},{{x:8}},{{x:-5}},{{x:0}}], duration:0.35}}, {t_com:.3f});')
    sfx(t_com, "golpe", 0.3)
    t_gen, t_lar, t_est = P("gente"), P("largo"), P("estudia")
    pop("#san", t_gen, sound="pop")
    pop("#enest", t_est, sound="pop2")
    cam(E("estudia") + 0.05, ROW(1), dur=0.45)


# ================================================================= 3 · CÓMO REDUCIRLOS
def scene_orden():
    fx, fy, fw, fh = F(2, 0)
    header("h3", fx, fy, "3", "CÓMO REDUCIRLOS")
    add(f'<div id="plate" class="plate" style="{css_box(fx + 210, fy + 170, 540, 540, 5)}"></div>')
    items = [("salad", "salad", "#15803d", "#86efac", 290, 230, "verdura"), ("beef", "drumstick", "#9a3412", "#fdba74", 520, 300, "proteina"),
             ("pasta", "wheat", "#a16207", "#fde68a", 380, 480, "hidratos")]
    for k, (fid, ic, col, fill, x, y, w) in enumerate(items):
        food(fid, ic, fx + x, fy + y, 170, col, fill=fill)
        add(f'<div id="{fid}-n" class="numb" style="{css_box(fx + x + 120, fy + y - 30, 80, 80, 8)}">{k + 1}</div>')
    pct, ph = roller("pc", "00", 110, "#fff")
    gw, gh = chart("ch4", fx + 40, fy + 740, 640, 320, [
        ("c4a", "M 0 230 C 90 230 130 20 220 20 C 300 20 330 230 560 230", BAD),
        ("c4b", "M 0 230 C 110 230 160 120 260 120 C 350 120 380 230 560 230", GOOD)], line140=False)
    add(f'<div id="pct" class="bigp" style="{css_box(fx + 700, fy + 760, 240, 280, 8)}">-{pct}<span style="font:900 80px {FONT}">%</span></div>')
    t_tres, t_red, t_pri, t_ord, t_ver, t_pro, t_hid = (P("tres"), P("reducirlos"), P("primero"), P("orden"), P("verdura"),
                                                        P("proteina"), P("hidratos"))
    travel(t_tres, F(2, 0), 2, 570, dur=0.85)
    header_in("h3", t_tres, t_red)
    pop("#plate", t_ord, sound="pop2")
    for fid, *_r, w in items:
        tt = P(w)
        js(f'tl.fromTo("#{fid}", {{opacity:0, y:-200, rotation:-20}}, {{opacity:1, y:0, rotation:0, duration:0.4, ease:"bounce.out"}}, {tt:.3f});')
        pop(f"#{fid}-n", tt + 0.25, sound="pop", vol=0.25)
    # CLÍMAX
    t_est, t_baj, t_37 = P("estudio", 2), P("bajo"), P("37%")
    pop("#ch4", t_est, sound="pop2")
    draw("c4a", t_est + 0.2, dur=0.8)
    draw("c4b", t_baj, dur=0.8)
    pop("#pct", t_baj, sound=None)
    roll_set("pc", "00", ph)
    roll_to("pc", "37", ph, t_37 - 0.3, dur=0.7)
    shake(t_37, 22)
    sfx(t_37, "golpe-climax", 0.55)


def scene_camina():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    add(character("p2", "g2", fx + 200, fl, 1.2, z=6))
    add(f'<div id="watch" class="pill" style="{css_box(fx + 380, fy + 90, None, None, 8)}background:#fff;color:{INK};font-size:64px">{icon("timer", 76, INK, 2.4)} unos minutos</div>')
    gw, gh = chart("ch5", fx + 40, fy + 260, 880, 380, [("c5a", "M 0 250 C 120 250 160 20 280 20 C 400 20 420 250 800 250", "#fda4af"),
                                                       ("c5b", "M 0 250 C 140 250 200 140 300 140 C 400 140 440 250 800 250", GOOD)], line140=False)
    add(f'<div id="foot" style="{css_box(fx + 600, fl - 200, 160, 160, 7)}">{icon("footprints", 150, GOOD, 2.4)}</div>')
    t_seg, t_cam, t_min, t_ayu = P("segundo"), P("camina"), P("minutos"), P("ayudan")
    travel(t_seg, F(2, 1), 2, 1630, dur=0.8)
    life("p2", 0, G.DUR, 3)
    pop("#ch5", t_seg + 0.3, sound=None)
    draw("c5a", t_seg + 0.4, dur=0.5)
    js(f'tl.to("#p2", {{x:420, duration:2.2, ease:"none"}}, {t_cam:.3f}); walk("p2", {t_cam:.3f}, {t_cam + 2.2:.3f}, 0.16);')
    js(f'tl.fromTo("#foot", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_cam + 0.3:.3f});')
    pop("#watch", t_min - 0.1, sound="click", vol=0.4)
    draw("c5b", t_cam + 0.3, dur=1.4)
    js(f'tl.to("#c5a", {{opacity:0.35, duration:0.4}}, {t_ayu:.3f});')
    sfx(t_ayu, "check", 0.4)


def scene_final():
    fx, fy, fw, fh = F(3, 1)
    card("pl2", fx + 60, fy + 40, 840, 420, f'''
      <div id="pl2-a" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:40px">
        {icon("wheat", 200, "#a16207", 2.2).replace("<svg", "<svg fill=\"#fde68a\"")}
        <div class="okb3" style="background:{BAD}">{icon("x", 90, "#fff", 3.4)}</div></div>
      <div id="pl2-b" style="position:absolute;inset:0;opacity:0;display:flex;align-items:center;justify-content:center;gap:24px">
        {icon("wheat", 150, "#a16207", 2.2).replace("<svg", "<svg fill=\"#fde68a\"")}{icon("salad", 150, "#15803d", 2.2).replace("<svg", "<svg fill=\"#86efac\"")}
        {icon("drumstick", 150, "#9a3412", 2.2).replace("<svg", "<svg fill=\"#fdba74\"")}{icon("droplet", 120, "#a16207", 2.2).replace("<svg", "<svg fill=\"#fde047\"")}
        <div class="okb3" style="background:{GOOD_BG}">{icon("check", 90, "#fff", 3.4)}</div></div>''')
    for k, (txt, w) in enumerate([("FIBRA", "fibra"), ("PROTEÍNA", "proteina"), ("GRASA", "grasa")]):
        add(f'<div id="lb{k}" class="pill" style="{css_box(fx + [60, 290, 640][k], fy + 490, None, None, 8)}background:{GOOD_BG};color:#fff;opacity:0">{txt}</div>')
    msg = "Tú, que siempre te duermes después de comer"
    card("chat", fx + 60, fy + 600, 840, 400, f'''
      <div class="chathead">{icon("users", 54, "#fff", 2.4)}<span style="font:900 52px {FONT};color:#fff;margin-left:16px">Amigos</span></div>
      <div class="bubble" style="left:30px;top:140px;width:620px;background:#d9fdd3">
        <div id="ct" style="font:800 54px {FONT};color:{INK};line-height:1.12">{chars(msg, "kc")}</div></div>
      <div id="send" class="sendb">{icon("send", 60, "#fff", 2.6)}</div>''', bg="#f4f5f7")
    add(f'<div id="disc" class="disc" style="{css_box(fx + 60, fy + 1020, 840, 70, 9)}">Divulgativo · consulta a tu médico</div>')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 900, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_ter, t_sol, t_aco = P("tercero"), P("solos"), P("acompanalos")
    travel(t_ter - 0.3, F(3, 1), 3, 1630, dur=0.75)
    pop("#pl2", t_ter, sound="pop")
    pop("#pl2-a .okb3", t_sol, sound="golpe", vol=0.3)
    flip("#pl2", t_aco, ["#pl2-a"], ["#pl2-b"])
    for k, w in enumerate(("fibra", "proteina", "grasa")):
        n = 2 if w == "proteina" else 1
        pop(f"#lb{k}", P(w, n), sound="pop2", vol=0.3)
    sfx(t_aco + 0.3, "check", 0.4)
    t_man, t_sie, t_com3 = P("mandaselo"), P("siempre"), P("comer", 3)
    slide_in("#chat", t_man, dy=80)
    type_on("#ct .kc", len(msg), t_man + 0.3, t_com3 + 0.3)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_com3 - 0.2:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com3 + 0.35:.3f}); tl.to("#send", {{scale:0.88, duration:0.08, yoyo:true, repeat:1}}, {t_com3 + 0.35:.3f});')
    sfx(t_com3 + 0.35, "click", 0.5)
    js(f'tl.fromTo("#disc", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_man:.3f});')
    cam(t_com3 + 0.8, (0, 100, 2200, 5200), dur=0.7, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:74px; top:28px; }}
.tagr {{ font:900 72px {FONT}; color:#fff; padding:6px 30px; border-radius:20px; box-shadow:0 14px 30px rgba(0,0,0,0.4); white-space:nowrap; }}
.table {{ background:#a07a4c; border-radius:14px; }} .tleg {{ background:#6e5233; }}
.zz {{ font:900 120px {FONT}; color:#93c5fd; opacity:0; text-align:center; }}
.food {{ opacity:1; }}
.phone {{ border-radius:56px; background:#fff; border:14px solid #1f2937; box-shadow:0 30px 70px rgba(0,0,0,0.5); }}
.pnotch {{ position:absolute; left:50%; top:16px; width:120px; height:26px; margin-left:-60px; border-radius:13px; background:#1f2937; }}
.okb2 {{ position:absolute; left:50%; bottom:40px; width:100px; height:100px; margin-left:-50px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
.okb3 {{ width:130px; height:130px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex:none; }}
.notif {{ border-radius:28px; background:rgba(255,255,255,0.96); display:flex; align-items:center; gap:22px; padding-left:22px;
  font:900 54px {FONT}; color:{INK}; box-shadow:0 14px 30px rgba(0,0,0,0.35); white-space:nowrap; opacity:0; }}
.nicon {{ width:76px; height:76px; border-radius:22px; display:flex; align-items:center; justify-content:center; flex:none; }}
.plate {{ border-radius:50%; background:radial-gradient(circle,#fff 0 58%,#e5e7eb 58% 64%,#fff 64%); box-shadow:0 30px 70px rgba(0,0,0,0.45); }}
.numb {{ border-radius:50%; background:{INK}; border:5px solid #fff; color:#fff; font:900 52px {FONT}; text-align:center; line-height:70px; }}
.bigp {{ border-radius:36px; background:{GOOD_BG}; color:#fff; font:900 110px {FONT}; display:flex; align-items:center; justify-content:center; }}
.chathead {{ height:110px; background:#1f2430; border-radius:40px 40px 0 0; display:flex; align-items:center; padding-left:36px; }}
.sendb {{ position:absolute; right:36px; bottom:30px; width:120px; height:120px; border-radius:50%; background:#16a34a; display:flex; align-items:center; justify-content:center; }}
.disc {{ border-radius:999px; background:rgba(15,23,42,0.9); border:3px solid rgba(255,255,255,0.4); color:#e2e8f0; font:800 46px {FONT}; text-align:center; line-height:64px; opacity:0; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_que()
    scene_importa()
    scene_salud()
    scene_orden()
    scene_camina()
    scene_final()
