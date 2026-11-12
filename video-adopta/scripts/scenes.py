"""Escenas del vídeo «Adopta, no compres». Un solo mundo: un camino en zigzag
(criadero -> carretera -> protectora -> hogar) que se dibuja mientras viaja la cámara."""
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



def pet(pid, kind, x, y, size, color="#f8fafc", bg="#334155", z=6):
    """Perro o gato (icono de Lucide) dentro de un círculo; respira con un tween en build()."""
    add(f'<div id="{pid}" class="pet" style="{css_box(x, y, size, size, z)}background:{bg}">'
        f'{icon(kind, int(size * 0.66), color, 2.0)}</div>')
    PETS.append(pid)


PETS = []


def breathe_pets():
    for k, pid in enumerate(PETS):
        js(f'tl.to("#{pid} svg", {{scale:1.06, y:-3, transformOrigin:"50% 80%", duration:{0.8 + (k % 4) * 0.1:.2f}, yoyo:true, '
           f'repeat:{int(G.DUR / 0.8)}, ease:"sine.inOut"}}, {(k % 5) * 0.13:.2f});')


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#ef4444"/><stop offset="0.6" stop-color="#f59e0b"/><stop offset="1" stop-color="#22c55e"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in [("Criadero", 0, 1630), ("Carretera", 1, 570), ("Protectora", 2, 1630), ("Hogar", 3, 570)]:
        add(f'<div class="mile" data-layout-ignore style="{css_box(x - 220, ROAD[r] + 34, 440, 70, 2)}">{icon("paw-print", 40, "#fff", 2.6)} {lab}</div>')


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    pr, ph = roller("price", "0.000", 80, INK)
    add(f'''<div id="shop" class="shopw" style="{css_box(fx + 40, fy + 40, 880, 520, 5)}">
      <div class="shopsign">{icon("store", 56, "#fff", 2.4)} TIENDA</div></div>''')
    pet("pup0", "dog", fx + 330, fy + 170, 300, bg="#f59e0b")
    add(f'<div id="tag0" class="ptag" style="{css_box(fx + 600, fy + 200, 300, 120, 7)}">{pr} €</div>')
    add(f'<div id="st-pro" class="stamp" style="{css_box(fx + 140, fy + 260, None, None, 9)}color:{BAD};border-color:{BAD};font-size:66px;opacity:0">PROHIBIDO · LEY 7/2023</div>')
    add(f'''<div id="cage0" class="cage" style="{css_box(fx + 180, fy + 640, 600, 400, 3)}"></div>''')
    pet("mom0", "dog", fx + 360, fy + 720, 240, color="#fecaca", bg="#7f1d1d", z=4)
    add(f'<div class="bars" data-layout-ignore style="{css_box(fx + 180, fy + 640, 600, 400, 6)}"></div>')
    add(f'<div id="mlab" class="pill" style="{css_box(fx + 330, fy + 1050 - 20, None, None, 8)}background:{BAD};color:#fff;opacity:0">SU MADRE</div>')
    cam(0, (fx + 20, fy + 20, 920, 600), whoosh=False)
    js('tl.fromTo("#pup0", {scale:0.75}, {scale:1, duration:0.45, ease:"back.out(3)"}, 0);')
    sfx(0.0, "pop", 0.4)
    t_com, t_cac, t_pag, t_exp, t_mad = P("compras"), P("cachorro"), P("pagando"), P("explotacion"), P("madre")
    pop("#tag0", t_cac, sound="pop2")
    roll_set("price", "0000", ph)
    roll_to("price", "1000", ph, t_pag, dur=0.7)
    cam(t_exp - 0.1, F(0, 0), dur=0.6, ease="power3.inOut")
    js(f'tl.fromTo("#cage0, #mom0", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_exp:.3f});')
    pop("#mlab", t_mad, sound="golpe", vol=0.35)
    t_mot, t_ado = P("motivos"), P("adoptar")
    cam(t_mot, ROW(0), dur=0.6)


# ================================================================= 1 · LA MADRE
def scene_criadero():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "LA MADRE", color=BAD, txt="#fff")
    for r in range(2):
        for c in range(3):
            x, y = fx + 20 + c * 320, fy + 180 + r * 300
            add(f'<div class="cage" style="{css_box(x, y, 280, 260, 4)}"></div>')
            pet(f"cg{r}{c}", "dog" if (r + c) % 2 == 0 else "cat", x + 50, y + 40, 180, color="#fecaca", bg="#7f1d1d", z=4)
            add(f'<div class="bars" data-layout-ignore style="{css_box(x, y, 280, 260, 5)}"></div>')
    cn, ch = roller("cam", "0", 80, "#fff")
    add(f'<div id="camc" class="cnt" style="{css_box(fx + 40, fy + 820, 520, 130, 8)}background:{BAD}"><span style="font:900 58px {FONT};color:#fff;margin-right:20px">CAMADAS</span>{cn}</div>')
    add(f'<div id="eur" class="cnt" style="{css_box(fx + 600, fy + 820, 320, 130, 8)}background:{INK}">{icon("euro", 70, GOOD, 2.6)}<span id="eur-t" style="font:900 60px {FONT};color:{GOOD};margin-left:12px">+++</span></div>')
    add(f'<div id="desc" class="stamp" style="{css_box(fx + 200, fy + 380, None, None, 9)}color:{BAD};border-color:{BAD};font-size:90px">DESCARTADA</div>')
    t_uno, t_mad2, t_cri, t_per, t_gat, t_jau, t_par, t_c1, t_c2 = (P("uno"), P("madre", 2), P("criaderos"), P("perras"), P("gatas"),
                                                                   P("jaulas"), P("pariendo"), P("camada"), P("camada", 2))
    travel(t_uno, F(0, 1), 0, 1630, dur=0.85)
    header_in("h1", t_uno, t_mad2)
    js(f'tl.fromTo(".cage, .bars", {{opacity:0}}, {{opacity:1, duration:0.4, stagger:0.03}}, {t_cri - 0.2:.3f});')
    for r in range(2):
        for c in range(3):
            w = t_per if (r + c) % 2 == 0 else t_gat
            js(f'tl.fromTo("#cg{r}{c}", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {w + 0.05 * (r * 3 + c):.3f});')
    sfx(t_per, "pop2", 0.3)
    pop("#camc", t_par, sound=None)
    roll_set("cam", "0", ch)
    for i, t in enumerate([t_par + 0.1, t_c1, t_c1 + 0.3, t_c2]):
        js(f'tl.to("#cam-d0", {{y:{-(10 + i + 1) * ch}, duration:0.18, ease:"back.out(2)"}}, {t:.3f});')
        sfx(t, "pop2", 0.2)
    t_ren, t_aba = P("rentables"), P("abandonadas")
    pop("#eur", P("dejan"), sound="pop")
    js(f'tl.to("#eur", {{backgroundColor:"{BAD}", duration:0.3}}, {t_ren:.3f}); tl.to("#eur-t", {{color:"#fff", duration:0.3}}, {t_ren:.3f});')
    js(f'tl.set("#eur-t", {{opacity:0}}, {t_ren + 0.15:.3f});')
    stamp("#desc", t_aba, rot=-10)


def scene_gijon():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    n3, nh = roller("n300", "000", 120, INK)
    card("news", fx, fy + 40, fw, 330, f'''
      <div class="nbar">{icon("siren", 60, "#fff", 2.4)}<span>GUARDIA CIVIL · GIJÓN</span></div>
      <div style="position:absolute;left:40px;top:150px;font:900 70px {FONT};color:{INK}">2026</div>
      <div style="position:absolute;left:300px;top:130px">+{n3}</div>
      <div style="position:absolute;left:300px;top:256px;font:800 46px {FONT};color:#555">perros rescatados</div>''')
    for i in range(4):
        x = fx + 30 + i * 235
        add(f'<div class="cage" style="{css_box(x, fy + 450, 210, 200, 4)}"></div>')
        pet(f"rs{i}", "dog", x + 35, fy + 475, 140, color="#fff", bg="#475569", z=4)
        add(f'<div id="door{i}" class="bars" style="{css_box(x, fy + 450, 210, 200, 5)}"></div>')
    add(character("vol", "g3", fx + 200, fl, 1.1, z=6))
    t_26, t_gua, t_res, t_300, t_gij = P("2026"), P("guardia"), P("rescato"), P("300"), P("gijon")
    travel(t_26 - 0.3, F(1, 1), 1, 1630, dur=0.8)
    slide_in("#news", t_gua, dy=-60, sound="pop")
    roll_set("n300", "000", nh)
    roll_to("n300", "300", nh, t_300, dur=0.7)
    life("vol", 0, G.DUR, 1)
    js(f'tl.fromTo("#vol", {{x:-300, opacity:0}}, {{x:0, opacity:1, duration:0.6}}, {t_res - 0.3:.3f}); walk("vol", {t_res - 0.3:.3f}, {t_res + 0.3:.3f}, 0.13);')
    for i in range(4):
        js(f'tl.to("#door{i}", {{scaleX:0.08, transformOrigin:"0% 50%", duration:0.3, ease:"power3.out"}}, {t_res + 0.3 + i * 0.25:.3f});')
        js(f'tl.to("#rs{i}", {{y:-30, duration:0.2, yoyo:true, repeat:1}}, {t_res + 0.5 + i * 0.25:.3f}); tl.to("#rs{i}", {{backgroundColor:"{GOOD_BG}", duration:0.3}}, {t_res + 0.4 + i * 0.25:.3f});')
        sfx(t_res + 0.3 + i * 0.25, "click", 0.25)
    js(f'point("vol", "R", {t_gij:.3f}, {t_gij + 0.9:.3f}, -100);')
    cam(E("gijon") + 0.05, (COLX[0], ROWS[0] + 150, 2120, 2450), dur=0.5)


# ================================================================= 2 · EL CACHORRO
def scene_camion():
    fx, fy, fw, fh = F(1, 0)
    header("h2", fx, fy, "2", "EL CACHORRO")
    add(f'''<div id="map" class="mapc" style="{css_box(fx, fy + 170, fw, 470, 4)}">
      <svg width="960" height="470" viewBox="0 0 960 470" style="position:absolute;inset:0">
        <path id="route" d="M 860 90 C 700 120 600 200 480 230 C 340 270 220 320 110 380" stroke="{BAD}" stroke-width="12" fill="none" stroke-dasharray="22 16"/></svg>
      <div class="mlab2" style="right:30px;top:30px">EUROPA DEL ESTE</div><div class="mlab2" style="left:30px;bottom:30px">ESPAÑA</div>
      <div id="truck" style="position:absolute;left:760px;top:40px">{icon("truck", 130, INK, 2.2).replace("<svg", "<svg fill=\"#fde68a\"")}</div></div>''')
    cl, chh = roller("hrs", "00", 110, "#fff")
    add(f'<div id="clk" class="cnt" style="{css_box(fx + 200, fy + 690, 560, 170, 8)}background:{INK}">{icon("clock", 90, "#fff", 2.4)}<span style="font:900 110px {FONT};color:#fff;margin-left:20px">+</span>{cl}<span style="font:900 70px {FONT};color:#fff;margin-left:10px">h</span></div>')
    pet("pup1", "dog", fx + 380, fy + 900, 150, color="#fff", bg="#9a3412", z=6)
    t_dos, t_cac2, t_cam, t_eur, t_via, t_15 = P("dos"), P("cachorro", 2), P("camiones"), P("europa"), P("viajes"), P("15")
    travel(t_dos, F(1, 0), 1, 570, dur=0.85)
    header_in("h2", t_dos, t_cac2)
    pop("#map", t_cam - 0.2, sound=None)
    js('tl.set("#route", {strokeDashoffset:900, strokeDasharray:"22 16"}, 0); tl.set("#route", {opacity:0}, 0);')
    js(f'tl.to("#route", {{opacity:1, duration:0.2}}, {t_eur:.3f});')
    js(f'tl.to("#truck", {{keyframes:[{{x:-280, y:150, duration:1.2}},{{x:-640, y:290, duration:1.4}}], ease:"none"}}, {t_eur:.3f});')
    sfx(t_cam, "whoosh", 0.3)
    pop("#clk", t_via, sound=None)
    roll_set("hrs", "00", chh)
    roll_to("hrs", "15", chh, t_15 - 0.3, dur=0.7)
    pop("#pup1", t_cac2 + 0.2, sound="pop2")


def scene_falso():
    fx, fy, fw, fh = F(2, 0)
    card("cart", fx + 60, fy + 60, 840, 460, f'''
      <div style="position:absolute;left:40px;top:36px;font:900 66px {FONT};color:{INK}">CARTILLA</div>
      <div style="position:absolute;left:40px;top:136px;right:40px;height:16px;border-radius:8px;background:#e5e7eb"></div>
      <div style="position:absolute;left:40px;top:176px;right:160px;height:16px;border-radius:8px;background:#e5e7eb"></div>
      <div style="position:absolute;left:40px;top:216px;right:90px;height:16px;border-radius:8px;background:#e5e7eb"></div>
      <div style="position:absolute;left:40px;top:300px">{icon("paw-print", 110, "#94a3b8", 2.2)}</div>
      <div id="fake" class="stamp" style="position:absolute;left:320px;top:250px;color:{BAD};border-color:{BAD};font-size:90px;opacity:0">FALSO</div>''')
    card("parvo", fx + 60, fy + 580, 840, 300, f'''
      <div style="position:absolute;left:40px;top:60px">{icon("thermometer", 170, BAD, 2.2)}</div>
      <div style="position:absolute;left:230px;top:70px;font:900 74px {FONT};color:{INK}">PARVOVIRUS</div>
      <div style="position:absolute;left:230px;top:170px;font:800 50px {FONT};color:#666">a veces</div>''')
    t_con, t_pap, t_fal, t_enf, t_par = P("con"), P("papeles"), P("falsos"), P("enfermedades"), P("parvovirus")
    travel(t_con - 0.1, F(2, 0), 2, 570, dur=0.6)
    pop("#cart", t_pap, sound="papel", vol=0.4)
    stamp("#fake", t_fal, rot=-12)
    pop("#parvo", t_enf, sound="pop")
    js(f'tl.to("#parvo", {{keyframes:[{{x:-8}},{{x:8}},{{x:-5}},{{x:0}}], duration:0.35}}, {t_par:.3f});')
    cam(E("parvovirus") + 0.05, (COLX[0], ROWS[1] + 150, 2120, 2450), dur=0.5)


# ================================================================= 3 · EL ABANDONO
def scene_abandono():
    fx, fy, fw, fh = F(2, 1)
    header("h3", fx, fy, "3", "EL ABANDONO")
    big, bh = roller("big", "000.000", 150, "#fff")
    add(f'<div id="bigc" class="cnt" style="{css_box(fx, fy + 170, fw, 280, 8)}background:{INK};flex-direction:column">{big}'
        f'<span style="font:900 54px {FONT};color:#cbd5e1">perros y gatos · 2025</span></div>')
    paws = "".join(f'<div class="paw" style="left:{(i * 173) % 900}px;top:{(i * 97) % 520}px">{icon("paw-print", 70, "#f59e0b", 2.4)}</div>' for i in range(24))
    add(f'<div id="paws" data-layout-ignore style="{css_box(fx + 20, fy + 160, 920, 560, 3)}">{paws}</div>')
    bars = [("Camadas no deseadas", 15, BAD), ("Pérdida de interés", 13, "#64748b"), ("Comportamiento", 12, "#64748b")]
    rows = "".join(f'<div class="brow"><div class="blab">{t}</div><div class="btrack"><div id="bar{i}" class="bfill" style="width:{v * 5.2:.0f}%;background:{c}"></div></div><div class="bval">{v} %</div></div>'
                   for i, (t, v, c) in enumerate(bars))
    card("causes", fx, fy + 480, fw, 520, f'<div style="padding:30px 36px">{rows}</div>')
    t_tres, t_aba, t_25, t_pro, t_rec, t_285 = P("tres"), P("abandono"), P("2025"), P("protectoras"), P("recogieron"), P("285.000")
    travel(t_tres, F(2, 1), 2, 1630, dur=0.85)
    header_in("h3", t_tres, t_aba)
    pop("#bigc", t_25, sound="pop")
    roll_set("big", "000000", bh)
    roll_to("big", "285000", bh, t_285 - 0.4, dur=1.0, spins=2, stagger=0.05)
    shake(t_285 + 0.2, 22)
    sfx(t_285 + 0.2, "golpe-climax", 0.55)
    js(f'tl.fromTo(".paw", {{opacity:0, scale:0.2}}, {{opacity:0.85, scale:1, duration:0.3, stagger:0.03, ease:"back.out(2)"}}, {t_285:.3f});')
    js(f'tl.to(".paw", {{opacity:0, duration:0.5}}, {P("primera") - 0.3:.3f});')
    t_pri, t_cam = P("primera"), P("camadas")
    pop("#causes", t_pri - 0.2, sound=None)
    js('tl.set(".bfill", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to(".bfill", {{scaleX:1, duration:0.6, stagger:0.15, ease:"power3.out"}}, {t_cam - 0.1:.3f});')
    js(f'tl.to(".brow:first-child", {{scale:1.05, duration:0.2, yoyo:true, repeat:1}}, {t_cam + 0.6:.3f});')
    sfx(t_cam, "pop2", 0.3)
    cam(E("deseadas") + 0.05, ROW(2), dur=0.4)


def scene_ciclo():
    fx, fy, fw, fh = F(3, 1)
    add(f'''<div id="cyc" style="{css_box(fx + 230, fy + 20, 500, 500, 5)}">
      <svg width="500" height="500" viewBox="0 0 500 500"><circle id="ring" cx="250" cy="250" r="190" fill="none" stroke="{BAD}" stroke-width="26" stroke-dasharray="330 68"/></svg>
      <div class="cyl" style="left:170px;top:20px">camada</div><div class="cyl" style="left:300px;top:380px">abandono</div><div class="cyl" style="left:20px;top:300px">camada</div>
      <div id="cut" style="position:absolute;left:185px;top:185px">{icon("scissors", 130, "#fff", 2.4)}</div></div>''')
    card("law", fx + 60, fy + 560, 840, 300, f'''
      <div style="position:absolute;left:40px;top:40px">{icon("store", 130, INK, 2.2)}</div>
      <div style="position:absolute;left:210px;top:40px;font:900 60px {FONT};color:{INK}">Venta en tiendas</div>
      <div id="lawst" class="stamp" style="position:absolute;left:210px;top:140px;color:{BAD};border-color:{BAD};font-size:60px;opacity:0">PROHIBIDA · LEY 7/2023</div>''')
    add(f'<div id="dem" class="pill" style="{css_box(fx + 120, fy + 900, None, None, 8)}background:{BAD};color:#fff">{icon("trending-down", 50, "#fff", 2.6)} Mientras haya demanda…</div>')
    t_ado, t_est, t_cor, t_cic = P("adoptar", 2), P("esterilizar"), P("corta"), P("ciclo")
    travel(t_ado - 0.2, F(3, 1), 3, 1630, dur=0.7)
    pop("#cyc", t_ado, sound="pop")
    js(f'tl.to("#cyc svg", {{rotation:300, transformOrigin:"50% 50%", duration:1.6, ease:"none"}}, {t_ado:.3f});')
    js(f'tl.fromTo("#cut", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(3)"}}, {t_est:.3f});')
    js(f'tl.to("#ring", {{stroke:"{GOOD}", strokeDasharray:"1000 194", duration:0.4}}, {t_cor:.3f}); tl.to("#cut", {{x:170, y:-60, rotation:-30, duration:0.3}}, {t_cor:.3f});')
    sfx(t_cor, "click", 0.4)
    sfx(t_cic, "check", 0.4)
    t_ley, t_pro, t_tie = P("ley"), P("prohibe"), P("tiendas")
    pop("#law", t_ley, sound="pop")
    stamp("#lawst", t_pro, rot=-6)
    t_neg, t_com = P("negocio"), P("compra")
    pop("#dem", t_neg, sound="golpe", vol=0.3)


def scene_hogar():
    fx, fy, fw, fh = F(3, 0)
    fl = floor(3)
    add(f'<div id="home" class="homec" style="{css_box(fx + 160, fy + 20, 640, 270, 4)}">{icon("heart-handshake", 140, "#fff", 2.2)}<span>ADOPTA</span></div>')
    add(character("f1", "g1", fx + 200, fl, 1.05, z=6))
    add(character("f2", "vecina2", fx + 760, fl, 1.05, z=6))
    pet("adog", "dog", fx + 330, fl - 220, 200, bg="#f59e0b", z=7)
    pet("acat", "cat", fx + 540, fl - 220, 200, bg="#a78bfa", z=7)
    msg = "¿Has pensado en adoptar?"
    card("chat", fx + 60, fy + 320, 840, 250, f'''
      <div class="bubble" style="left:30px;top:40px;width:600px;background:#d9fdd3">
        <div id="ct" style="font:800 58px {FONT};color:{INK};line-height:1.12">{chars(msg, "kc")}</div></div>
      <div id="send" class="sendb">{icon("send", 60, "#fff", 2.6)}</div>''', bg="#f4f5f7")
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 470, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_ado, t_noc, t_com, t_pen, t_mas = P("adopta"), P("compres"), P("comparte"), P("pensando"), P("mascota")
    travel(t_ado - 0.2, F(3, 0), 3, 570, dur=0.7)
    stamp("#home", t_ado, rot=-3)
    for k, cid in enumerate(("f1", "f2")):
        life(cid, 0, G.DUR, 5 + k)
        js(f'tl.fromTo("#{cid}", {{opacity:0, x:{-260 if k == 0 else 260}}}, {{opacity:1, x:0, duration:0.6}}, {t_ado:.3f}); walk("{cid}", {t_ado:.3f}, {t_ado + 0.6:.3f}, 0.13);')
        js(f'wave("{cid}", {t_mas + 0.2:.3f}, {G.DUR - 0.05:.3f});')
    js(f'tl.fromTo("#adog, #acat", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.4, stagger:0.15, ease:"back.out(2.4)"}}, {t_noc:.3f});')
    js(f'tl.to("#adog, #acat", {{y:-40, duration:0.2, yoyo:true, repeat:3, stagger:0.1}}, {t_noc + 0.5:.3f});')
    sfx(t_noc, "pop", 0.4)
    slide_in("#chat", t_com, dy=80)
    type_on("#ct .kc", len(msg), t_com + 0.2, t_pen + 0.4)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_pen:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_mas:.3f}); tl.to("#send", {{scale:0.88, duration:0.08, yoyo:true, repeat:1}}, {t_mas:.3f});')
    sfx(t_mas, "click", 0.5)
    hearts("hf-", fx + 480, fy + 130, 6, t_mas + 0.2, spread=600, rise=200)
    cam(E("mascota") + 0.2, (0, 100, 2200, 5200), dur=0.7, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:76px; top:28px; }}
.pet {{ border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 14px 34px rgba(0,0,0,0.45); }}
.shopw {{ border-radius:30px; background:linear-gradient(#e0f2fe,#bae6fd); border:14px solid #f8fafc; box-shadow:0 30px 70px rgba(0,0,0,0.5); }}
.shopsign {{ position:absolute; left:0; right:0; top:-10px; height:90px; border-radius:20px 20px 0 0; background:#0ea5e9; color:#fff; font:900 56px {FONT};
  display:flex; align-items:center; justify-content:center; gap:16px; }}
.ptag {{ border-radius:24px; background:#fff; border:6px solid {INK}; display:flex; align-items:center; justify-content:center; font:900 80px {FONT}; color:{INK}; rotate:6deg; }}
.cage {{ border-radius:18px; background:#1e293b; border:8px solid #64748b; }}
.bars {{ border-radius:18px; background:repeating-linear-gradient(90deg, transparent 0 34px, #94a3b8 34px 42px); border:8px solid #94a3b8; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; }}
.nbar {{ height:110px; background:#1d4ed8; border-radius:40px 40px 0 0; display:flex; align-items:center; gap:18px; padding-left:36px; font:900 50px {FONT}; color:#fff; }}
.mapc {{ background:#eef2f7; border-radius:40px; overflow:hidden; box-shadow:0 24px 60px rgba(0,0,0,0.45); }}
.mlab2 {{ position:absolute; font:900 50px {FONT}; color:#334155; }}
.paw {{ position:absolute; opacity:0; }}
.brow {{ display:flex; align-items:center; gap:18px; margin-bottom:30px; }}
.blab {{ width:400px; font:900 46px {FONT}; color:{INK}; line-height:1.05; }}
.btrack {{ flex:1; height:60px; border-radius:30px; background:#e5e7eb; overflow:hidden; }}
.bfill {{ height:100%; border-radius:30px; }}
.bval {{ width:150px; font:900 52px {FONT}; color:{INK}; text-align:right; white-space:nowrap; }}
.cyl {{ position:absolute; padding:6px 20px; border-radius:999px; background:#fff; font:900 46px {FONT}; color:{INK}; }}
.homec {{ border-radius:40px; background:{GOOD_BG}; display:flex; align-items:center; justify-content:center; gap:30px; font:900 96px {FONT}; color:#fff; box-shadow:0 30px 70px rgba(0,0,0,0.45); }}
.sendb {{ position:absolute; right:36px; bottom:50px; width:120px; height:120px; border-radius:50%; background:#16a34a; display:flex; align-items:center; justify-content:center; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_criadero()
    scene_gijon()
    scene_camion()
    scene_falso()
    scene_abandono()
    scene_ciclo()
    scene_hogar()
    breathe_pets()
