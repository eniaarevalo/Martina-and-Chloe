"""Escenas del vídeo «El edificio de Aquí no hay quien viva existe». Un solo mundo: un plano de calles
en zigzag (Desengaño -> Valverde -> Colón -> Moraleja) que se dibuja mientras la cámara viaja."""
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


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#ffd43b"/><stop offset="1" stop-color="#f97316"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    # nombres de calles en el camino, como en un plano
    for lab, r, x in [("C. del Desengaño", 0, 570), ("C. de Valverde", 1, 1630), ("C. de Colón", 2, 570), ("Moraleja de Enmedio", 3, 1630)]:
        add(f'<div class="mile" data-layout-ignore style="{css_box(x - 260, ROAD[r] + 34, 520, 70, 2)}">{lab}</div>')


# ================================================================= 0 · GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    facade("fac0", fx + 130, fy + 330, 700, 740, n_win=5, scale_win=1.1)
    add(f'''<div id="plate" style="{css_box(fx + 60, fy + 40, 840, 250, 8)}" class="plate">
      <div class="plate-in"><div class="plate-t">C. DEL DESENGAÑO</div><div id="plate-n" class="plate-n">21</div></div></div>''')
    add(f'''<div id="x0" class="bigx" style="{css_box(fx + 640, fy + 10, 200, 200, 9)}background:{BAD}">
      <div id="x0a" class="ic">{icon("x", 140, "#fff", 3.4)}</div><div id="x0b" class="ic" style="opacity:0">{icon("check", 140, "#fff", 3.4)}</div></div>''')
    cam(0, (fx + 40, fy + 0, 880, 420), whoosh=False)
    cam(0.15, F(0, 0), dur=0.9, ease="power3.inOut", whoosh=False)
    js('tl.fromTo("#plate", {y:-500, rotation:-8}, {y:0, rotation:0, duration:0.35, ease:"bounce.out"}, 0);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.3, "golpe", 0.45)
    shake(0.33, 14)
    t_21, t_no, t_edi, t_si = P("21"), P("no"), P("edificio"), P("si")
    stamp("#x0", t_no, rot=-8)
    js(f'tl.to("#plate-n", {{color:"{BAD}", duration:0.2}}, {t_no:.3f});')
    # la fachada se levanta planta a planta
    for f in range(4):
        js(f'tl.fromTo("#fac0-fl{3 - f}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.25, ease:"back.out(2)"}}, {0.1 + 0.1 * f:.3f});')
    js('tl.fromTo("#fac0 .fshop", {opacity:0}, {opacity:1, duration:0.25}, 0.05);')
    js(f'tl.to("#fac0", {{scale:1.04, duration:0.18, yoyo:true, repeat:1, transformOrigin:"50% 100%"}}, {t_edi:.3f});')
    sfx(t_edi, "pop2", 0.3)
    flip("#x0", t_si, ["#x0a"], ["#x0b"], bg=GOOD_BG)
    sfx(t_si + 0.15, "check", 0.45)
    floaty("#plate", t_si + 0.5, G.DUR, 6, 2.6)
    cam(E("si") + 0.1, ROW(0), dur=0.5)


# ================================================================= 1 · LA CALLE
def scene_calle():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "1", "LA CALLE")
    card("leyenda", fx, fy + 170, fw, 210, f'''
      <div style="position:absolute;left:36px;top:50px">{icon("book-open", 110, INK, 2.2)}</div>
      <div style="position:absolute;left:180px;top:30px;font:900 70px {FONT};color:{INK}">«¡Qué desengaño!»</div>
      <div id="ley-tag" class="pill" style="position:absolute;left:180px;top:118px;background:{ACC};color:{INK};opacity:0">LEYENDA</div>''')
    add(character("cab1", "g1", fx + 160, fl, 1.15, z=6))
    add(character("cab2", "fernando", fx + 800, fl, 1.15, z=6))
    add(character("dama", "vecina2", fx + 480, fl, 1.15, z=5))
    add(f'<div id="sw1" class="sword" style="{css_box(fx + 250, fy + 600, 150, 150, 7)}">{icon("sword", 150, "#d1d5db", 2.6)}</div>')
    add(f'<div id="sw2" class="sword" style="{css_box(fx + 560, fy + 600, 150, 150, 7)}">{icon("sword", 150, "#d1d5db", 2.6)}</div>')
    head_y = fl - 430 * 1.15 + 50 * 1.15
    add(f'<div id="veil" style="{css_box(fx + 480 - 80, head_y - 20, 160, 200, 7)}border-radius:80px 80px 30px 30px;background:rgba(255,255,255,0.88)"></div>')
    add(f'<div id="skull" style="{css_box(fx + 480 - 75, head_y, 150, 150, 8)}opacity:0">{icon("skull", 150, "#f8fafc", 2.4).replace("<svg", "<svg fill=\"#111827\"")}</div>')
    t_uno, t_cal, t_des, t_ley = P("uno"), P("calle"), P("desengano", 2), P("leyenda")
    travel(t_uno, F(0, 1), 0, 1630, dur=0.8)
    header_in("h1", t_uno, t_cal)
    slide_in("#leyenda", t_des, dy=-60)
    pop("#ley-tag", t_ley, sound="pop")
    life("cab1", 0, G.DUR, 1)
    life("cab2", 0, G.DUR, 2)
    life("dama", 0, G.DUR, 3)
    js('face("cab2", -1, 0);')
    t_cab, t_bat, t_dam, t_ros, t_calv = P("caballeros"), P("batian"), P("dama"), P("rostro"), P("calavera")
    js(f'tl.fromTo("#cab1", {{x:-300, opacity:0}}, {{x:0, opacity:1, duration:0.5}}, {t_cab - 0.3:.3f}); walk("cab1", {t_cab - 0.3:.3f}, {t_cab + 0.2:.3f}, 0.13);')
    js(f'tl.fromTo("#cab2", {{x:300, opacity:0}}, {{x:0, opacity:1, duration:0.5}}, {t_cab - 0.2:.3f}); walk("cab2", {t_cab - 0.2:.3f}, {t_cab + 0.3:.3f}, 0.13);')
    # duelo: espadas que chocan
    js(f'tl.fromTo("#sw1", {{opacity:0, rotation:-60}}, {{opacity:1, rotation:20, duration:0.25}}, {t_bat:.3f});')
    js(f'tl.fromTo("#sw2", {{opacity:0, rotation:150}}, {{opacity:1, rotation:70, duration:0.25}}, {t_bat:.3f});')
    for k in range(3):
        tt = t_bat + 0.3 + k * 0.22
        js(f'tl.to("#sw1", {{rotation:{30 if k % 2 == 0 else 5}, x:{20 if k % 2 == 0 else 0}, duration:0.11, yoyo:true, repeat:1}}, {tt:.3f});')
        js(f'tl.to("#sw2", {{rotation:{60 if k % 2 == 0 else 85}, x:{-20 if k % 2 == 0 else 0}, duration:0.11, yoyo:true, repeat:1}}, {tt:.3f});')
        sfx(tt + 0.1, "click", 0.3)
    js(f'tl.fromTo("#dama", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4}}, {t_dam:.3f}); tl.fromTo("#veil", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_dam:.3f});')
    js(f'tl.to("#veil", {{y:-160, opacity:0, duration:0.4, ease:"power2.in"}}, {t_ros:.3f});')
    js(f'tl.to("#skull", {{opacity:1, scale:1.15, duration:0.25, ease:"back.out(3)"}}, {t_calv - 0.1:.3f});')
    sfx(t_calv, "golpe", 0.4)
    js(f'jump("cab1", {t_calv:.3f}, 70); jump("cab2", {t_calv + 0.05:.3f}, 70);')
    js(f'tl.to("#sw1, #sw2", {{y:500, rotation:"+=180", opacity:0, duration:0.6, ease:"power2.in"}}, {t_calv + 0.1:.3f});')


def scene_busca():
    fx, fy, fw, fh = F(1, 1)
    q = "Desengaño 21"
    card("srch", fx, fy + 120, fw, 600, f'''
      <div class="mapbar">{icon("landmark", 60, "#fff", 2.4)}<span style="font:900 52px {FONT};color:#fff;margin-left:18px">Callejero de Madrid</span></div>
      <div class="sbox">{icon("search", 64, "#555", 2.6)}<div id="srch-q" style="font:800 64px {FONT};color:{INK};margin-left:22px">{chars(q, "sq")}</div></div>
      <div id="srch-r" class="sres" style="opacity:0">{icon("circle-x", 80, "#fff", 2.6)}<span>Sin resultados</span></div>''')
    add(f'''<div id="nums" style="{css_box(fx + 40, fy + 780, 880, 120, 6)}">{"".join(f'<div class="num" id="n{i}">{v}</div>' for i, v in enumerate([1, 3, 5, 7, 9, 11, 13, 15]))}</div>''')
    t_per, t_ayu, t_cal, t_num, t_21 = P("pero", 2), P("ayuntamiento"), P("calle", 3), P("numero"), P("21", 2)
    travel(t_per, F(1, 1), 1, 1630, dur=0.8)
    slide_in("#srch", t_ayu, dy=80)
    js(f'tl.fromTo(".num", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.25, stagger:0.07}}, {t_cal:.3f});')
    type_on("#srch-q .sq", len(q), t_num - 0.3, t_21 + 0.2)
    pop("#srch-r", t_21 + 0.25, sound="golpe", vol=0.35)
    js(f'tl.to("#srch", {{keyframes:[{{x:-10}},{{x:10}},{{x:-6}},{{x:0}}], duration:0.3}}, {t_21 + 0.3:.3f});')
    cam(E("21", 2) + 0.1, (COLX[0], ROWS[0] + 150, 2120, 2450), dur=0.5)


# ================================================================= 2 · EL EDIFICIO DE VERDAD
def scene_colon():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    header("h2", fx, fy, "2", "EL EDIFICIO")
    add(f'''<div id="map" style="{css_box(fx, fy + 170, fw, 560, 4)}" class="mapc">
      <svg width="960" height="560" viewBox="0 0 960 560" style="position:absolute;inset:0">
        <path d="M 60 150 L 900 150" stroke="#cbd5e1" stroke-width="44"/>
        <path d="M 60 440 L 900 440" stroke="#cbd5e1" stroke-width="44"/>
        <path id="valv" d="M 480 150 L 480 440" stroke="{ACC}" stroke-width="44"/>
        <path id="route" d="M 160 150 L 480 150 L 480 440 L 760 440" stroke="{BAD}" stroke-width="12" fill="none" stroke-dasharray="20 16"/></svg>
      <div class="sname" style="left:70px;top:70px">C. del Desengaño</div>
      <div class="sname" style="left:130px;top:265px">C. de Valverde</div>
      <div class="sname" style="left:70px;top:480px">C. de Colón</div>
      <div id="pin" style="position:absolute;left:700px;top:290px;opacity:0">{icon("map-pin", 130, "#fff", 2.2).replace("<svg", f"<svg fill=\"{BAD}\"")}</div>
      <div id="dist" class="pill" style="position:absolute;left:560px;top:20px;background:{INK};color:#fff;opacity:0">500 m</div></div>''')
    card("addr", fx + 60, fy + 760, 840, 150, f'''
      <div style="position:absolute;left:30px;top:30px">{icon("building", 90, INK, 2.2)}</div>
      <div style="position:absolute;left:150px;top:18px;font:900 64px {FONT};color:{INK}">C. de Colón, 14</div>
      <div style="position:absolute;left:150px;top:90px;font:800 46px {FONT};color:#555">Malasaña · Madrid</div>''')
    card("crea", fx + 60, fy + 935, 840, 140, f'''
      <div style="position:absolute;left:30px;top:25px">{icon("user", 90, INK, 2.2)}</div>
      <div style="position:absolute;left:150px;top:16px;font:900 56px {FONT};color:{INK}">Alberto Caballero</div>
      <div style="position:absolute;left:150px;top:80px;font:800 46px {FONT};color:#555">creador de la serie</div>
      <div id="conf" class="sticker" style="position:absolute;right:20px;top:15px;width:110px;height:110px;background:#15803d;opacity:0">{icon("check", 80, "#fff", 3.4)}</div>''')
    add(character("walk", "g2", fx + 160, fy + 170 + 150 + 10, 0.42, z=7))
    t_dos, t_edi, t_fac, t_col, t_14, t_mal = P("dos", 2), P("edificio", 2), P("fachada"), P("colon"), P("14"), P("malasana")
    travel(t_dos, F(1, 0), 1, 570, dur=0.8)
    header_in("h2", t_dos, t_edi)
    slide_in("#map", t_fac, dy=60)
    js(f'tl.fromTo("#pin", {{opacity:0, y:-160}}, {{opacity:1, y:0, duration:0.45, ease:"bounce.out"}}, {t_col:.3f});')
    sfx(t_col, "pop", 0.4)
    pop("#addr", t_14, sound="pop2")
    js(f'tl.fromTo("#addr div:last-child", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_mal:.3f});')
    t_500, t_and = P("500"), P("andando")
    js('tl.set("#route", {strokeDasharray:"20 16", strokeDashoffset:0}, 0); tl.set("#route", {opacity:0}, 0);')
    js(f'tl.to("#route", {{opacity:1, duration:0.2}}, {t_500 - 0.2:.3f});')
    pop("#dist", t_500, sound="pop")
    # el muñeco va andando por el plano: Desengaño -> Valverde -> Colón
    life("walk", 0, G.DUR, 4)
    js(f'tl.fromTo("#walk", {{opacity:0}}, {{opacity:1, duration:0.2}}, {t_500 - 0.2:.3f});')
    js(f'tl.to("#walk", {{keyframes:[{{x:320, duration:0.6}},{{y:290, duration:0.7}},{{x:600, duration:0.6}}], ease:"none"}}, {t_500 - 0.1:.3f});')
    js(f'walk("walk", {t_500 - 0.1:.3f}, {t_500 + 1.8:.3f}, 0.12);')
    t_conf, t_alb = P("confirmo"), P("alberto")
    pop("#crea", t_conf, sound="pop2")
    stamp("#conf", t_alb, rot=-6)
    js(f'tl.set("#conf", {{opacity:0}}, 0);')
    cam(E("caballero") + 0.05, ROW(1), dur=0.45)


# ================================================================= 3 · FICCIÓN CONTRA REALIDAD
def scene_versus():
    fx, fy, fw, fh = F(2, 0)
    header("h3", fx, fy, "3", "FICCIÓN vs REALIDAD")
    add(f'<div class="vlab" style="{css_box(fx + 10, fy + 165, 450, 80, 6)}background:{PURPLE}">SERIE</div>')
    add(f'<div class="vlab" style="{css_box(fx + 500, fy + 165, 450, 80, 6)}background:{GOOD_BG}">REAL</div>')
    facade("fs", fx + 10, fy + 270, 450, 700, n_win=6, scale_win=0.62, signs=("BANCO", "VIDEOCLUB"))
    facade("fr", fx + 500, fy + 270, 450, 700, n_win=6, scale_win=0.62, signs=("BANCO", "VIDEOCLUB"), signs_b=("CREPERÍA", "FERRETERÍA"))
    c6, h6 = roller("c6", "0", 70, "#fff")
    c4, h4 = roller("c4", "0", 70, "#fff")
    add(f'<div id="cs" class="cnt" style="{css_box(fx + 180, fy + 985, 110, 90, 8)}">{c6}</div>')
    add(f'<div id="cr" class="cnt" style="{css_box(fx + 670, fy + 985, 110, 90, 8)}">{c4}</div>')
    t_tres, t_fic, t_real = P("tres"), P("ficcion"), P("realidad")
    travel(t_tres, F(2, 0), 2, 570, dur=0.85)
    header_in("h3", t_tres, t_fic)
    pop("#fs", t_fic, sound="pop2")
    pop("#fr", t_real, sound="pop2")
    t_r2, t_cua, t_ser, t_seis = P("real", 2), P("cuatro"), P("serie"), P("seis")
    pop("#cr", t_cua - 0.1, sound=None)
    roll_set("c4", "0", h4)
    roll_to("c4", "4", h4, t_cua, dur=0.5)
    # en la real sobran dos ventanas por planta: se encogen y las demás se recolocan
    w = 450
    for f in range(4):
        for i in (4, 5):
            js(f'tl.to("#fr-w{f}-{i}", {{scale:0, opacity:0, duration:0.3, ease:"back.in(2)"}}, {t_cua + 0.15 + f * 0.05:.3f});')
        for i in range(4):
            dx = (i + 0.5) * w / 4 - (i + 0.5) * w / 6
            js(f'tl.to("#fr-w{f}-{i}", {{x:{dx:.0f}, duration:0.35, ease:"power2.inOut"}}, {t_cua + 0.35 + f * 0.05:.3f});')
    pop("#cs", t_ser - 0.1, sound=None)
    roll_set("c6", "0", h6)
    roll_to("c6", "6", h6, t_seis, dur=0.5)
    js(f'tl.to("#fs .fwin", {{scale:1.12, duration:0.15, yoyo:true, repeat:1, stagger:0.01}}, {t_seis:.3f});')
    t_aba, t_ban, t_vid, t_cre, t_fer = P("abajo"), P("banco"), P("videoclub"), P("creperia"), P("ferreteria")
    js(f'tl.to("#fr-sg0, #fs-sg0", {{scale:1.1, duration:0.15, yoyo:true, repeat:1}}, {t_ban:.3f}); tl.to("#fr-sg1, #fs-sg1", {{scale:1.1, duration:0.15, yoyo:true, repeat:1}}, {t_vid:.3f});')
    for k, (t, txt) in enumerate([(t_cre, "CREPERÍA"), (t_fer, "FERRETERÍA")]):
        js(f'tl.to("#fr-sg{k} .fsign", {{scaleY:0, duration:0.12}}, {t:.3f}); tl.set("#fr-sa{k}", {{opacity:0}}, {t + 0.12:.3f}); tl.set("#fr-sb{k}", {{opacity:1}}, {t + 0.12:.3f});')
        js(f'tl.set("#fr-sg{k} .fsign", {{backgroundColor:"{GOOD_BG}"}}, {t + 0.12:.3f}); tl.to("#fr-sg{k} .fsign", {{scaleY:1, duration:0.25, ease:"back.out(2)"}}, {t + 0.12:.3f});')
        sfx(t, "whoosh-corto", 0.2)


# ================================================================= 4 · EL PLATÓ
def scene_plato():
    fx, fy, fw, fh = F(2, 1)
    header("h4", fx, fy, "4", "EL PLATÓ")
    for i, lx in enumerate([fx + 120, fx + 470, fx + 820]):
        add(f'<div id="lamp{i}" class="lampc" style="{css_box(lx - 60, fy + 160, 120, 120, 6)}">{icon("lightbulb", 90, ACC, 2.4)}</div>')
    add(f'<div id="beam" class="beam" data-layout-ignore style="{css_box(fx + 40, fy + 270, 880, 620, 2)}"></div>')
    add(f'''<div id="set" style="{css_box(fx + 180, fy + 300, 600, 600, 4)}">
      <div id="set-f" class="setface"></div>
      <div id="set-b" class="setback" style="opacity:0">{"".join(f'<div class="lath" style="left:{40 + i * 130}px"></div>' for i in range(5))}
        <div class="brace"></div><div class="brace b2"></div></div></div>''')
    facade("fp", fx + 180, fy + 300, 600, 600, n_win=4, scale_win=0.8, signs=("BANCO", "VIDEOCLUB"), z=5)
    m2, mh = roller("m2", "0.000", 70, INK)
    add(f'<div id="m2c" class="pill" style="{css_box(fx + 20, fy + 920, None, None, 8)}background:#fff;color:{INK};font-size:62px">{m2} m²</div>')
    add(f'<div id="mor" class="pill" style="{css_box(fx + 470, fy + 930, None, None, 8)}background:{INK};color:#fff;border:4px solid #fff">{icon("map-pin", 44, "#fff", 2.6)} Moraleja</div>')
    add(f'<div id="clap" class="sticker" style="{css_box(fx + 790, fy + 280, 160, 160, 9)}">{icon("clapperboard", 96, INK, 2.4)}</div>')
    yr, yh = roller("yr6", "2003", 70, "#fff")
    add(f'<div id="cal6" class="cnt" style="{css_box(fx + 330, fy + 520, 300, 110, 9)}background:{BAD};width:300px">{yr}</div>')
    t_cua, t_pla, t_nin, t_gra, t_dec, t_2000, t_mor = (P("cuatro", 2), P("plato"), P("ningun"), P("grabo"), P("decorado"),
                                                      P("2000"), P("moraleja"))
    travel(t_cua, F(2, 1), 2, 1630, dur=0.8)
    header_in("h4", t_cua, t_pla)
    js(f'tl.fromTo(".lampc", {{opacity:0, y:-60}}, {{opacity:1, y:0, duration:0.3, stagger:0.1}}, {t_pla:.3f});')
    js(f'tl.fromTo("#beam", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_pla + 0.2:.3f});')
    pop("#fp", t_nin, sound="pop2")
    pop("#clap", t_gra, sound="click", vol=0.5)
    # la fachada gira y por detrás es un decorado de madera
    js(f'tl.to("#fp", {{scaleX:0, duration:0.2, ease:"power2.in"}}, {t_dec:.3f}); tl.set("#fp", {{opacity:0}}, {t_dec + 0.2:.3f});')
    js(f'tl.set("#set-b", {{opacity:1}}, {t_dec + 0.2:.3f}); tl.fromTo("#set", {{scaleX:0}}, {{scaleX:1, duration:0.3, ease:"back.out(2)", immediateRender:false}}, {t_dec + 0.2:.3f});')
    sfx(t_dec, "whoosh-corto", 0.3)
    pop("#m2c", t_2000 - 0.1, sound=None)
    roll_set("m2", "0000", mh)
    roll_to("m2", "2000", mh, t_2000, dur=0.6)
    pop("#mor", t_mor, sound="pop")
    # 2006: lo desmontan
    t_06, t_des = P("2006"), P("desmontaron")
    pop("#cal6", t_06 - 0.15, sound=None)
    roll_set("yr6", "2003", yh)
    js(f'tl.to("#yr6-d3", {{y:{-(10 + 6) * yh}, duration:0.5, ease:"power3.out"}}, {t_06:.3f});')
    sfx(t_06, "tic-rodillo", 0.3)
    js(f'tl.to("#set-b .lath, #set-b .brace", {{y:300, rotation:40, opacity:0, duration:0.5, stagger:0.06, ease:"power2.in"}}, {t_des:.3f});')
    js(f'tl.to("#beam", {{opacity:0, duration:0.4}}, {t_des + 0.3:.3f}); tl.to(".lampc", {{opacity:0.35, duration:0.3}}, {t_des + 0.3:.3f});')
    sfx(t_des, "madera", 0.5)
    cam(E("desmontaron") + 0.0, ROW(2), dur=0.45)


# ================================================================= CLÍMAX: LA MAQUETA
def scene_maqueta():
    fx, fy, fw, fh = F(3, 1)
    add(f'''<div id="paper" style="{css_box(fx + 120, fy + 80, 720, 900, 4)}" class="paper">
      <div class="pcut" style="left:60px;top:60px;width:600px;height:640px"></div>
      <div class="pcut" style="left:60px;top:730px;width:290px;height:120px"></div>
      <div class="pcut" style="left:370px;top:730px;width:290px;height:120px"></div>
      <div id="scis" style="position:absolute;left:30px;top:20px">{icon("scissors", 90, INK, 2.4)}</div></div>''')
    add(f'''<div id="mini" style="{css_box(fx + 230, fy + 300, 500, 640, 6)}opacity:0">
      {"".join(f'<div class="mroom" style="left:{20 + c * 240}px;top:{20 + r * 150}px;background:{["#fde68a", "#bfdbfe", "#fbcfe8", "#bbf7d0", "#fed7aa", "#ddd6fe", "#fecaca", "#a5f3fc"][r * 2 + c]}"></div>' for r in range(4) for c in range(2))}
      <div class="mstair"></div></div>''')
    add(f'<div id="mlab" class="pill" style="{css_box(fx + 220, fy + 960, None, None, 8)}background:{ACC};color:{INK};opacity:0">MAQUETA RECORTABLE</div>')
    t_hoy, t_casa, t_ilu, t_maq, t_rec = P("hoy"), P("casa"), P("ilustrador"), P("maqueta"), P("recortar")
    travel(t_hoy - 0.1, F(3, 1), 3, 1630, dur=0.75)
    js(f'tl.fromTo("#paper", {{opacity:0, y:120, rotation:-6}}, {{opacity:1, y:0, rotation:0, duration:0.5, ease:"power3.out"}}, {t_casa:.3f});')
    sfx(t_casa, "papel", 0.4)
    js(f'tl.to("#scis", {{keyframes:[{{x:600, duration:0.5}},{{y:620, duration:0.5}},{{x:0, duration:0.5}}], ease:"none"}}, {t_ilu:.3f});')
    sfx(t_ilu, "click", 0.3)
    # se pliega y se levanta el edificio en miniatura
    js(f'tl.to("#paper", {{scaleY:0.05, y:420, duration:0.35, ease:"power3.in"}}, {t_maq - 0.15:.3f});')
    js(f'tl.set("#paper", {{opacity:0}}, {t_maq + 0.2:.3f});')
    js(f'tl.fromTo("#mini", {{opacity:1, scaleY:0, transformOrigin:"50% 100%"}}, {{opacity:1, scaleY:1, duration:0.55, ease:"back.out(1.8)", immediateRender:false}}, {t_maq + 0.1:.3f});')
    js(f'tl.set("#mini", {{opacity:0}}, 0);')
    js(f'tl.fromTo(".mroom", {{scale:0}}, {{scale:1, duration:0.3, stagger:0.05, ease:"back.out(2)", immediateRender:false}}, {t_maq + 0.4:.3f});')
    shake(t_maq + 0.1, 20)
    sfx(t_maq + 0.1, "golpe-climax", 0.5)
    pop("#mlab", t_rec, sound="pop")
    floaty("#mini", t_rec + 0.4, G.DUR, 8, 2.4)


# ================================================================= FINAL
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    fl = floor(3)
    msg = "¿Sabías que Desengaño 21 no existe?"
    card("wa", fx, fy + 100, fw, 560, f'''
      <div class="chathead">{icon("users", 54, "#fff", 2.4)}<span style="font:900 52px {FONT};color:#fff;margin-left:16px">Amigos</span></div>
      <div class="bubble" style="left:auto;right:30px;top:150px;width:760px;background:#d9fdd3">
        <div id="wa-t" style="font:800 58px {FONT};color:{INK};line-height:1.12">{chars(msg, "wc")}</div>
        <div id="wa-v" style="text-align:right;opacity:0">{icon("check-check", 54, "#34b7f1", 2.8)}</div></div>
      <div id="wa-send" class="sendb">{icon("send", 64, "#fff", 2.6)}</div>''', bg="#f4f5f7")
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 560, 140, 140, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 130, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    add(character("f1", "g1", fx + 250, fl, 1.1, z=6))
    add(character("f2", "g3", fx + 700, fl, 1.1, z=6))
    t_man, t_tod, t_des, t_ex = P("mandaselo"), P("todavia"), P("desengano", 3), P("existe", 2)
    travel(t_man - 0.2, F(3, 0), 3, 570, dur=0.7)
    slide_in("#wa", t_man, dy=80)
    type_on("#wa-t .wc", len(msg), t_man + 0.2, t_ex - 0.1)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_des:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_ex:.3f}); tl.to("#wa-send", {{scale:0.88, duration:0.08, yoyo:true, repeat:1}}, {t_ex:.3f});')
    sfx(t_ex, "click", 0.5)
    js(f'tl.to("#wa-v", {{opacity:1, duration:0.2}}, {t_ex + 0.3:.3f});')
    sfx(t_ex + 0.35, "check", 0.4)
    for k, cid in enumerate(("f1", "f2")):
        life(cid, 0, G.DUR, 50 + k)
        js(f'tl.fromTo("#{cid}", {{opacity:0, x:{-300 if k == 0 else 300}}}, {{opacity:1, x:0, duration:0.6}}, {t_tod:.3f}); walk("{cid}", {t_tod:.3f}, {t_tod + 0.6:.3f}, 0.13);')
        js(f'wave("{cid}", {t_ex + 0.2:.3f}, {G.DUR - 0.05:.3f});')
    # el mapa entero, con el camino completo
    cam(t_ex + 0.45, (0, 100, 2200, 5200), dur=0.8, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0b5cad; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:78px; top:26px; }}
.facade {{ }}
.fbody {{ position:absolute; inset:0; background:#e8b84a; border-radius:10px; box-shadow:0 30px 70px rgba(0,0,0,0.45); }}
.fcorn {{ position:absolute; left:-18px; right:-18px; top:0; height:40px; background:#c98f2c; border-radius:8px; }}
.ffloor {{ position:absolute; left:0; right:0; border-bottom:8px solid #c98f2c; }}
.fwin {{ position:absolute; background:#33475b; border:6px solid #fff3d6; border-radius:6px 6px 0 0; }}
.frail {{ position:absolute; left:-12px; right:-12px; bottom:-18px; height:22px; border:5px solid #1f2937; border-top-width:6px; border-radius:3px; }}
.fshop {{ position:absolute; height:150px; }}
.sgt {{ position:absolute; left:0; right:0; top:0; }}
.fsign {{ position:relative; height:56px; border-radius:10px; background:#1f2937; color:#fff; font:900 30px {FONT}; text-align:center; line-height:56px; white-space:nowrap; overflow:hidden; }}
.fdoor {{ margin:12px auto 0; width:70%; height:80px; background:#5b3a1e; border-radius:8px 8px 0 0; }}
.plate {{ background:#fff; border-radius:26px; box-shadow:0 20px 60px rgba(0,0,0,0.5); }}
.plate-in {{ position:absolute; inset:14px; border:10px solid #1d4ed8; border-radius:16px; display:flex; align-items:center; justify-content:space-between; padding:0 36px; }}
.plate-t {{ font:900 64px {FONT}; color:#1d4ed8; letter-spacing:-1px; }}
.plate-n {{ font:900 120px {FONT}; color:#1d4ed8; }}
.bigx {{ border-radius:50%; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.bigx .ic {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }}
.sword {{ opacity:0; }}
.mapbar {{ height:110px; background:#1d4ed8; border-radius:40px 40px 0 0; display:flex; align-items:center; padding-left:36px; }}
.sbox {{ position:absolute; left:40px; right:40px; top:160px; height:130px; border-radius:65px; background:#f1f3f6; border:4px solid #d1d5db; display:flex; align-items:center; padding-left:36px; }}
.sres {{ position:absolute; left:40px; right:40px; top:340px; height:150px; border-radius:30px; background:{BAD}; display:flex; align-items:center; justify-content:center; gap:24px; font:900 66px {FONT}; color:#fff; }}
.num {{ display:inline-block; width:94px; height:94px; margin-right:16px; border-radius:16px; background:#fff; border:6px solid #1d4ed8; color:#1d4ed8; font:900 50px {FONT}; text-align:center; line-height:82px; }}
.mapc {{ background:#eef2f7; border-radius:40px; overflow:hidden; box-shadow:0 24px 60px rgba(0,0,0,0.45); }}
.sname {{ position:absolute; font:900 46px {FONT}; color:#334155; white-space:nowrap; }}
.vlab {{ border-radius:24px; color:#fff; font:900 60px {FONT}; text-align:center; line-height:80px; }}
.cnt {{ border-radius:24px; background:{INK}; border:5px solid #fff; display:flex; align-items:center; justify-content:center; }}
.lampc {{ border-radius:50%; background:#1f2937; display:flex; align-items:center; justify-content:center; border:5px solid #374151; }}
.beam {{ background:linear-gradient(rgba(255,212,59,0.18), rgba(255,212,59,0)); clip-path:polygon(10% 0, 90% 0, 100% 100%, 0 100%); }}
.setface {{ position:absolute; inset:0; }}
.setback {{ position:absolute; inset:0; background:#3b2a1a; border:10px solid #8b6840; border-radius:8px; }}
.lath {{ position:absolute; top:0; bottom:0; width:34px; background:#c49a6c; }}
.brace {{ position:absolute; left:-20px; right:-20px; top:280px; height:30px; background:#a07a4c; transform-origin:50% 50%; rotate:-28deg; }}
.brace.b2 {{ rotate:28deg; }}
.paper {{ background:#fffdf5; border-radius:12px; box-shadow:0 30px 70px rgba(0,0,0,0.5); }}
.pcut {{ position:absolute; border:6px dashed #9ca3af; border-radius:8px; background:repeating-linear-gradient(0deg, rgba(232,184,74,0.35) 0 40px, transparent 40px 80px); }}
.mroom {{ position:absolute; width:220px; height:130px; border-radius:10px; border:6px solid #e8b84a; }}
#mini {{ background:#fff7e6; border:14px solid #e8b84a; border-radius:14px; box-shadow:0 30px 70px rgba(0,0,0,0.5); }}
.mstair {{ position:absolute; left:226px; top:20px; width:8px; height:590px; background:#c98f2c; }}
.sendb {{ position:absolute; right:40px; bottom:40px; width:130px; height:130px; border-radius:50%; background:#16a34a; display:flex; align-items:center; justify-content:center; }}
.sq, .wc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_calle()
    scene_busca()
    scene_colon()
    scene_versus()
    scene_plato()
    scene_maqueta()
    scene_final()
