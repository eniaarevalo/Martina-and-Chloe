"""Escenas del vídeo «La historia detrás del gol de Iniesta». Un solo mundo: un camino en zigzag
(agosto 2009 -> temporada 09-10 -> Johannesburgo -> Cornellà) que se dibuja mientras viaja la cámara."""
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
MILES = [("Johannesburgo", 0, 1630), ("Agosto 2009", 1, 570), ("2010 · 2012", 2, 1630), ("Cornellà", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            cls = "room pitchroom" if (r, c) == (0, 1) else "room"
            add(f'<div class="{cls}" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#c8102e"/><stop offset="0.5" stop-color="#facc15"/><stop offset="1" stop-color="#c8102e"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 240, ROAD[r] + 34, 480, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


def scoreboard(sid, x, y, w=840, left="ESP", right="NED", z=7, minute=""):
    sc, sh = roller(f"{sid}-g", "0", 110, "#fff")
    add(f'''<div id="{sid}" class="score" style="{css_box(x, y, w, 190, z)}">
      <span class="team">{left}</span>{sc}<span class="dash">-</span><span id="{sid}-r" class="goal0">0</span><span class="team">{right}</span>
      <span id="{sid}-min" class="minute">{minute}</span></div>''')
    return sh


def ball_svg(size):
    return icon("volleyball", size, INK, 2.2).replace("<svg", "<svg fill=\"#fff\"")


# ================================================================= GANCHO: la final
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    add(f'<div id="bm1" class="beam" data-layout-ignore style="{css_box(fx - 60, fy - 60, 420, 1000, 2)}transform:rotate(-24deg)"></div>')
    add(f'<div id="bm2" class="beam" data-layout-ignore style="{css_box(fx + 600, fy - 60, 420, 1000, 2)}transform:rotate(24deg)"></div>')
    cal, ch = roller("cal10", "0000", 70, "#fff")
    add(f'<div id="cal2" class="cnt" style="{css_box(fx + 200, fy + 30, 560, 130, 8)}background:{INK}"><span style="font:900 56px {FONT};color:#fff;margin-right:16px">11 JUL</span>{cal}</div>')
    add(f'<div id="final" class="pill" style="{css_box(fx + 150, fy + 195, None, None, 8)}background:#fff;color:{INK};font-size:58px;opacity:0">{icon("trophy", 56, "#ca8a04", 2.4)} FINAL DEL MUNDIAL</div>')
    scoreboard("sb0", fx + 60, fy + 330)
    add(f'<div id="pror" class="pill" style="{css_box(fx + 250, fy + 580, None, None, 8)}background:{BAD};color:#fff;font-size:58px;opacity:0">{icon("timer", 56, "#fff", 2.4)} PRÓRROGA</div>')
    ck, kh = roller("clk", "090", 96, "#fff")
    add(f'<div id="clk" class="clk" style="{css_box(fx + 250, fy + 730, 460, 160, 8)}opacity:0">{icon("clock", 84, ACC, 2.6)}{ck}<span style="font:900 96px {FONT};color:#fff">\'</span></div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: se encienden los focos y cae el marcador
    js('tl.fromTo(".beam", {opacity:0.25}, {opacity:0.9, duration:0.12, yoyo:true, repeat:3}, 0);')
    js('tl.fromTo("#sb0", {scale:1.25, opacity:1}, {scale:1, duration:0.45, ease:"back.out(1.8)"}, 0);')
    shake(0.4, 14)
    sfx(0.0, "whoosh", 0.4)
    sfx(0.4, "golpe", 0.5)
    t_jul, t_10, t_fin, t_mun, t_hol, t_c1, t_c2 = P("julio"), P("2010"), P("final"), P("mundial"), P("holanda"), P("cero"), P("cero", 2)
    js('tl.fromTo("#cal2", {opacity:0, y:-60}, {opacity:1, y:0, duration:0.35, ease:"back.out(2)"}, 0.1);')
    roll_set("cal10", "0000", ch)
    roll_to("cal10", "2010", ch, t_10 - 0.2, dur=0.6)
    pop("#final", t_fin, sound="pop2")
    js(f'tl.to("#sb0", {{scale:1.05, duration:0.15, yoyo:true, repeat:1}}, {t_hol:.3f});')
    js(f'tl.fromTo("#sb0-g", {{scale:1.3}}, {{scale:1, duration:0.3, ease:"back.out(3)"}}, {t_c1:.3f});')
    js(f'tl.fromTo("#sb0-r", {{scale:1.3}}, {{scale:1, duration:0.3, ease:"back.out(3)"}}, {t_c2:.3f});')
    js(f'tl.to(".beam", {{opacity:0.45, duration:0.6}}, {t_mun:.3f});')
    t_pro, t_cua, t_pen = P("prorroga"), P("cuatro"), P("penaltis")
    stamp("#pror", t_pro)
    sfx(t_pro, "golpe", 0.35)
    pop("#clk", t_pro + 0.25, sound=None)
    roll_set("clk", "090", kh)
    roll_to("clk", "116", kh, t_cua, dur=0.7, from_text="090")
    sfx(t_cua, "tic-rodillo", 0.3)
    js(f'tl.to("#clk", {{rotation:2, duration:0.08, yoyo:true, repeat:5}}, {t_pen:.3f});')


# ================================================================= LA JUGADA
def scene_jugada():
    fx, fy, fw, fh = F(0, 1)
    add(f'''<div id="pitch" data-layout-ignore style="{css_box(fx, fy + 40, fw, 1020, 3)}" class="pitch">
      <div class="pbox"></div><div class="parea"></div><div class="pcircle"></div><div class="pline"></div>
      <div id="net1" class="pgoal"></div></div>''')
    pts = {"torres": (150, 560), "def": (420, 430), "cesc": (330, 700), "iniesta": (640, 290)}
    for name, (x, y) in pts.items():
        if name == "def":
            add(f'<div id="tk-def" class="token orange" style="{css_box(fx + x - 45, fy + y - 45, 90, 90, 5)}"></div>')
        else:
            add(f'<div id="tk-{name}" class="token red" style="{css_box(fx + x - 55, fy + y - 55, 110, 110, 6)}"><span class="tlab">{name.capitalize()}</span></div>')
    for (x, y) in [(260, 330), (560, 470), (760, 640), (560, 820)]:
        add(f'<div class="token orange" style="{css_box(fx + x - 45, fy + y - 45, 90, 90, 5)}"></div>')
    add(f'<div class="token keeper" style="{css_box(fx + 435, fy + 70, 90, 90, 5)}"></div>')
    x0, y0 = pts["torres"]
    add(f'<div id="ball1" class="ball" style="{css_box(fx + x0 - 30 + 50, fy + y0 - 30, 60, 60, 9)}">{ball_svg(58)}</div>')
    segs = [("torres", "def"), ("def", "cesc"), ("cesc", "iniesta")]
    path_d = [f'<path id="seg-{a}" d="M {pts[a][0]} {pts[a][1]} L {pts[b][0]} {pts[b][1]}" stroke="{ACC}" stroke-width="10" fill="none" stroke-dasharray="20 14" opacity="0"/>' for a, b in segs]
    path_d.append(f'<path id="seg-shot" d="M {pts["iniesta"][0]} {pts["iniesta"][1]} L 480 110" stroke="#fff" stroke-width="12" fill="none" opacity="0"/>')
    add(f'<svg data-layout-ignore style="{css_box(fx, fy, 960, 1080, 5)}overflow:visible" viewBox="0 0 960 1080">{"".join(path_d)}</svg>')
    add(f'<div id="spot" class="ring" data-layout-ignore style="{css_box(fx + pts["iniesta"][0] - 110, fy + pts["iniesta"][1] - 110, 220, 220, 5)}opacity:0"></div>')
    sh = scoreboard("sb2", fx + 60, fy - 20, minute="116\'", z=10)
    add(f'<div id="star" style="{css_box(fx + 380, fy + 380, 200, 200, 11)}opacity:0">{icon("star", 200, "#facc15", 2).replace("<svg", "<svg fill=\"#facc15\"")}</div>')
    add(f'<div id="champ" class="pill" style="{css_box(fx + 70, fy + 600, None, None, 11)}background:#c8102e;color:#fff;font-size:62px;opacity:0">CAMPEONES DEL MUNDO</div>')
    t_tor = P("torres")
    travel(t_tor - 0.35, F(0, 1), 0, 1630, dur=0.6)
    js(f'tl.fromTo(".token", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, stagger:0.03, ease:"back.out(2)"}}, {t_tor - 0.3:.3f});')
    js('tl.set("#sb2", {opacity:0}, 0); tl.set("#ball1", {opacity:0}, 0);')
    js(f'tl.to("#ball1", {{opacity:1, duration:0.2}}, {t_tor:.3f});')
    bx0 = x0 + 50

    def move(to, t, dur=0.4):
        x1, y1 = pts[to]
        js(f'tl.to("#ball1", {{x:{x1 - bx0}, y:{y1 - y0}, duration:{dur}, ease:"power1.inOut"}}, {t:.3f});')
    t_cen, t_reb, t_cae, t_ve, t_and, t_are = P("centra"), P("rebota"), P("cae"), P("ve"), P("andres"), P("area")
    move("def", t_cen)
    js(f'tl.to("#seg-torres", {{opacity:1, duration:0.2}}, {t_cen:.3f});')
    sfx(t_cen, "click", 0.3)
    js(f'tl.to("#tk-def", {{scale:1.3, duration:0.12, yoyo:true, repeat:1}}, {t_reb:.3f});')
    sfx(t_reb, "golpe", 0.25)
    move("cesc", t_cae, 0.45)
    js(f'tl.to("#seg-def", {{opacity:1, duration:0.2}}, {t_cae:.3f});')
    js(f'tl.to("#tk-cesc", {{scale:1.25, duration:0.15, yoyo:true, repeat:1}}, {t_cae + 0.4:.3f});')
    js(f'tl.fromTo("#spot", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.35}}, {t_ve:.3f});')
    js(f'tl.to("#spot", {{scale:1.12, duration:0.3, yoyo:true, repeat:5}}, {t_ve + 0.35:.3f});')
    sfx(t_ve, "pop2", 0.25)
    move("iniesta", t_are - 0.1, 0.45)
    js(f'tl.to("#seg-cesc", {{opacity:1, duration:0.2}}, {t_are - 0.1:.3f});')
    sfx(t_are - 0.1, "click", 0.3)
    t_con, t_caer, t_dis, t_gol = P("controla"), P("caer"), P("dispara"), P("gol")
    cam(t_con - 0.25, (fx + 300, fy + 20, 560, 560), dur=0.5)
    xi, yi = pts["iniesta"]
    js(f'tl.to("#ball1", {{x:{xi - bx0 + 30}, y:{yi - y0 + 20}, duration:0.25, ease:"power2.out"}}, {t_con:.3f});')
    sfx(t_con, "click", 0.25)
    js(f'tl.to("#ball1", {{scale:1.7, duration:0.25, yoyo:true, repeat:1, ease:"sine.out"}}, {t_caer:.3f});')
    js(f'tl.to("#ball1", {{x:{480 - bx0}, y:{110 - y0}, duration:0.35, ease:"power3.in"}}, {t_dis + 0.1:.3f});')
    js(f'tl.to("#seg-shot", {{opacity:1, duration:0.2}}, {t_dis + 0.1:.3f}); tl.to("#spot", {{opacity:0, duration:0.2}}, {t_dis:.3f});')
    sfx(t_dis + 0.1, "whoosh", 0.45)
    # CLÍMAX
    js(f'tl.fromTo("#net1", {{scaleY:1}}, {{scaleY:1.5, transformOrigin:"50% 100%", duration:0.12, yoyo:true, repeat:3}}, {t_gol - 0.05:.3f});')
    shake(t_gol, 26)
    sfx(t_gol, "golpe-climax", 0.6)
    cam(t_gol + 0.15, F(0, 1), dur=0.5)
    js(f'tl.to("#sb2", {{opacity:1, duration:0.3}}, {t_gol:.3f});')
    roll_set("sb2-g", "0", sh)
    js(f'tl.to("#sb2-g-d0", {{y:{-(10 + 1) * sh}, duration:0.4, ease:"back.out(2)"}}, {t_gol + 0.1:.3f});')
    t_cam, t_pri = P("campeona"), P("primera")
    js(f'tl.fromTo("#star", {{opacity:0, scale:0.2, rotation:-90}}, {{opacity:1, scale:1, rotation:0, duration:0.5, ease:"back.out(2)"}}, {t_cam:.3f});')
    pop("#champ", t_pri, sound="pop")
    hearts("hj-", fx + 480, fy + 560, 6, t_cam + 0.2, spread=700, rise=300)
    # Camacho, en la tele
    card("tv", fx + 40, fy + 790, 880, 270, f'''
      <div id="mic" style="position:absolute;left:40px;top:45px;width:180px;height:180px;border-radius:50%;background:{ACC};display:flex;align-items:center;justify-content:center">{icon("mic", 110, INK, 2.6)}</div>
      <div style="position:absolute;left:250px;top:14px;font:800 46px {FONT};color:{ACC}">CAMACHO · TV</div>
      <div id="tvq" class="tvq">{chars("¡INIESTA", "tq")}<br>{chars("DE MI VIDA!", "tq2")}</div>''', bg="#0b1220", extra=f"border:6px solid {ACC};")
    for k in range(3):
        add(f'<div id="rg{k}" class="ring" data-layout-ignore style="{css_box(fx + 60, fy + 815, 220, 220, 12)}opacity:0"></div>')
    t_cmo, t_gri, t_ini, t_vid = P("camacho"), P("grito"), P("iniesta"), P("vida")
    slide_in("#tv", t_cmo - 0.1, dy=120, sound="whoosh-corto")
    for k in range(3):
        js(f'tl.fromTo("#rg{k}", {{opacity:0.9, scale:0.8}}, {{opacity:0, scale:2.2, duration:0.8, repeat:2, immediateRender:false}}, {t_gri + k * 0.27:.3f});')
    js(f'tl.to("#mic", {{scale:1.12, duration:0.12, yoyo:true, repeat:9}}, {t_gri:.3f});')
    type_on("#tvq .tq", 8, t_ini, E("iniesta"))
    type_on("#tvq .tq2", 11, E("iniesta"), E("vida"))
    shake(t_vid, 10)
    sfx(t_ini, "golpe", 0.35)


# ================================================================= LA CAMISETA
def scene_camiseta():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    msg = "Dani Jarque siempre con nosotros"
    add(f'''<div id="under" class="under" style="{css_box(fx + 180, fy + 30, 600, 600, 4)}">
      <div id="ut" class="handw">{chars(msg, "hc")}</div></div>''')
    add(f'''<div id="redsh" class="redsh" style="{css_box(fx + 180, fy + 30, 600, 600, 5)}"><span>6</span><div class="rshl">INIESTA</div></div>''')
    add(f'<div id="flag" style="{css_box(fx + 760, fy + 760, 200, 300, 5)}opacity:0">{icon("flag", 200, "#facc15", 2.4)}</div>')
    add(character("ini2", "ini", fx + 280, fl, 1.0, z=6))
    t_and, t_cor, t_qui, t_ens, t_men, t_dan, t_nos = (P("andres", 2), P("corner"), P("quita"), P("ensena"), P("mensaje"), P("dani"), P("nosotros"))
    travel(t_and - 0.3, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_and + 0.2)
    life("ini2", 0, G.DUR, 3)
    js(f'tl.fromTo("#ini2", {{opacity:0, x:-300}}, {{opacity:1, x:0, duration:0.9, ease:"power1.out"}}, {t_and - 0.1:.3f}); walk("ini2", {t_and - 0.1:.3f}, {t_and + 0.8:.3f}, 0.11);')
    js(f'tl.fromTo("#flag", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_cor:.3f}); tl.to("#flag", {{rotation:6, transformOrigin:"20% 100%", duration:0.4, yoyo:true, repeat:{int((G.DUR - t_cor) / 0.4)}}}, {t_cor + 0.35:.3f});')
    js(f'tl.fromTo("#redsh, #under", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_cor:.3f});')
    sfx(t_cor, "pop2", 0.3)
    js(f'tl.to("#redsh", {{y:-640, rotation:-8, duration:0.55, ease:"power3.in"}}, {t_qui + 0.1:.3f}); tl.to("#redsh", {{opacity:0, duration:0.2}}, {t_qui + 0.55:.3f});')
    js(f'tl.to(Q("ini2","armL"), {{rotation:160, svgOrigin:PIV.armL, duration:0.3}}, {t_qui:.3f}); tl.to(Q("ini2","armR"), {{rotation:-160, svgOrigin:PIV.armR, duration:0.3}}, {t_qui:.3f});')
    js(f'tl.to(Q("ini2","armL"), {{rotation:0, svgOrigin:PIV.armL, duration:0.3}}, {t_ens:.3f});')
    sfx(t_qui + 0.1, "whoosh-corto", 0.35)
    js(f'point("ini2", "R", {t_ens:.3f}, {t_nos + 0.6:.3f}, -130);')
    js(f'tl.fromTo("#under", {{boxShadow:"0 0 0px rgba(250,204,21,0)"}}, {{boxShadow:"0 0 90px rgba(250,204,21,0.55)", duration:0.6}}, {t_men:.3f});')
    type_on("#ut .hc", len(msg), t_dan, t_nos + 0.4)
    sfx(t_dan, "papel", 0.3)


# ================================================================= DANI
def scene_dani():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    card("dani", fx, fy + 30, fw, 330, f'''
      <div class="num21">21</div>
      <div style="position:absolute;left:250px;top:40px;font:900 76px {FONT};color:{INK}">DANI JARQUE</div>
      <div id="capt" class="pill" style="position:absolute;left:250px;top:140px;background:{ACC};color:{INK};opacity:0">CAPITÁN · ESPANYOL</div>
      <div id="age" style="position:absolute;left:250px;top:230px;font:800 54px {FONT};color:#555;opacity:0">26 años</div>''')
    add(f'<div id="sel" class="pill" style="{css_box(fx + 40, fy + 420, None, None, 8)}background:#c8102e;color:#fff;opacity:0">SELECCIÓN · INFERIORES</div>')
    add(character("kid1", "jar", fx + 170, fl, 0.95, z=6))
    add(character("kid2", "ini", fx + 430, fl, 0.95, z=6))
    add(f'''<div id="cnd" style="{css_box(fx + 700, fy + 640, 160, 420, 6)}opacity:0">
      <div id="flm" class="flame" style="position:absolute;left:50px;top:0;width:60px;height:96px"></div>
      <div class="candle" style="position:absolute;left:20px;top:110px;width:120px;height:300px"></div></div>''')
    add(f'<div id="y09" class="pill" style="{css_box(fx + 640, fy + 520, None, None, 8)}background:#334155;color:#fff;opacity:0">AGO 2009</div>')
    t_dan, t_cap, t_esp, t_ami, t_inf, t_ido, t_ant, t_26 = (P("dani", 2), P("capitan"), P("espanyol"), P("amigo"), P("inferiores"),
                                                           P("ido"), P("antes"), P("26"))
    travel(t_dan - 0.3, F(1, 0), 1, 570, dur=0.8)
    slide_in("#dani", t_dan, dy=-60, sound="pop")
    pop("#capt", t_cap, sound=None)
    for k, cid in enumerate(("kid1", "kid2")):
        life(cid, 0, G.DUR, 10 + k)
        js(f'tl.fromTo("#{cid}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_ami + k * 0.25:.3f});')
    js(f'tl.to(Q("kid1","armR"), {{rotation:-150, svgOrigin:PIV.armR, duration:0.25}}, {t_inf:.3f}); tl.to(Q("kid2","armL"), {{rotation:150, svgOrigin:PIV.armL, duration:0.25}}, {t_inf:.3f});')
    js(f'jump("kid1", {t_inf + 0.25:.3f}, 40); jump("kid2", {t_inf + 0.3:.3f}, 40);')
    sfx(t_inf + 0.25, "click", 0.4)
    pop("#sel", t_inf, sound="pop2")
    js(f'tl.to(Q("kid1","armR"), {{rotation:0, svgOrigin:PIV.armR, duration:0.4}}, {t_ido:.3f}); tl.to(Q("kid2","armL"), {{rotation:0, svgOrigin:PIV.armL, duration:0.4}}, {t_ido:.3f});')
    js(f'tl.to("#kid1", {{opacity:0.45, duration:1.0}}, {t_ido:.3f});')
    js(f'tl.fromTo("#cnd", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.8, ease:"power2.out"}}, {t_ido:.3f});')
    js(f'tl.to("#flm", {{scaleY:1.15, scaleX:0.9, transformOrigin:"50% 100%", duration:0.35, yoyo:true, repeat:{int((G.DUR - t_ido) / 0.35)}, ease:"sine.inOut"}}, {t_ido + 0.6:.3f});')
    js(f'tl.fromTo("#y09", {{opacity:0}}, {{opacity:1, duration:0.6}}, {t_ant:.3f});')
    js(f'tl.fromTo("#age", {{opacity:0, x:-20}}, {{opacity:1, x:0, duration:0.4}}, {t_26:.3f});')


# ================================================================= LA DEPRESIÓN Y EL GOL QUE AYUDÓ
def scene_luz():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    add(f'<div id="sun" class="sun" style="{css_box(fx + 620, fy + 60, 260, 260, 3)}opacity:0"></div>')
    add(character("ini1", "ini", fx + 260, fl, 1.15, z=6))
    add(f'<div id="cloud" style="{css_box(fx + 90, fy + 230, 340, 240, 9)}opacity:0">{icon("cloud", 320, "#94a3b8", 2.0).replace("<svg", "<svg fill=\"#475569\"")}</div>')
    add(f'''<div id="dep" class="pill pillx" style="{css_box(fx + 40, fy + 500, 470, 90, 8)}background:#475569;color:#fff;opacity:0">
      <span id="dep-a">DEPRESIÓN</span><span id="dep-b" style="opacity:0">{icon("sun", 50, "#fff", 2.6)} SE SIENTE BIEN</span></div>''')
    card("book", fx + 530, fy + 660, 400, 330, f'''
      <div style="position:absolute;left:30px;top:30px">{icon("book-open", 120, INK, 2.2)}</div>
      <div style="position:absolute;left:30px;top:170px;font:900 50px {FONT};color:{INK};line-height:1.1">La jugada<br>de mi vida</div>''')
    add(f'<div id="miniball" class="ball" style="{css_box(fx + 380, fy + 420, 90, 90, 9)}opacity:0">{ball_svg(86)}</div>')
    t_aq, t_and, t_dep, t_con, t_lib = P("aquel"), P("andres", 3), P("depresion"), P("conto"), P("libro")
    travel(t_aq - 0.3, F(2, 0), 2, 570, dur=0.8)
    hide_mile(1, t_aq + 0.2)
    life("ini1", 0, G.DUR, 2)
    js(f'tl.fromTo("#cloud", {{opacity:0, scale:0.5}}, {{opacity:0.9, scale:1, duration:0.7, ease:"power2.out"}}, {t_and:.3f});')
    js(f'tl.to(Q("ini1","head"), {{rotation:16, svgOrigin:PIV.head, duration:0.6}}, {t_and:.3f}); tl.to("#ini1", {{y:30, duration:0.6}}, {t_and:.3f});')
    js(f'tl.fromTo("#dep", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.5}}, {t_dep:.3f});')
    js(f'tl.to("#cloud", {{y:12, duration:1.1, yoyo:true, repeat:3, ease:"sine.inOut"}}, {t_dep:.3f});')
    slide_in("#book", t_lib - 0.1, dy=80, sound="papel", vol=0.4)
    t_mis, t_gol, t_ayu, t_sal, t_osc, t_vol, t_bie = (P("mismo"), P("gol", 2), P("ayudo"), P("salir"), P("oscuro"), P("volver"), P("bien"))
    js(f'tl.to("#book", {{x:40, opacity:0.0, duration:0.4}}, {t_mis:.3f});')
    js(f'tl.fromTo("#miniball", {{opacity:0, scale:0.3, y:-200}}, {{opacity:1, scale:1, y:0, duration:0.5, ease:"bounce.out"}}, {t_gol:.3f});')
    sfx(t_gol, "pop", 0.3)
    js(f'tl.to("#cloud", {{scale:1.12, duration:0.25, yoyo:true, repeat:1}}, {t_osc:.3f});')
    js(f'tl.to("#cloud", {{x:-500, opacity:0, duration:0.8, ease:"power2.in"}}, {t_vol:.3f});')
    sfx(t_vol, "whoosh", 0.3)
    js(f'tl.fromTo("#sun", {{opacity:0, y:240, scale:0.6}}, {{opacity:1, y:0, scale:1, duration:1.0, ease:"power2.out"}}, {t_sal:.3f});')
    js(f'tl.to("#sun", {{rotation:360, duration:6, ease:"none"}}, {t_sal + 1.0:.3f});')
    js(f'tl.to(Q("ini1","head"), {{rotation:0, svgOrigin:PIV.head, duration:0.5}}, {t_vol:.3f}); tl.to("#ini1", {{y:0, duration:0.5}}, {t_vol:.3f});')
    js(f'tl.to("#miniball", {{y:-60, duration:0.3, yoyo:true, repeat:3, ease:"power1.out"}}, {t_ayu:.3f});')
    flip("#dep", t_bie, ["#dep-a"], ["#dep-b"], sound="check", bg=GOOD_BG)
    js(f'jump("ini1", {t_bie + 0.1:.3f}, 50); tl.to(Q("ini1","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.2}}, {t_bie:.3f});')


# ================================================================= PREMIOS
def scene_premios():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    add(f'<div id="gb" class="goldball" style="{css_box(fx + 60, fy + 40, 220, 220, 6)}opacity:0"></div>')
    add(f'<div id="gbp" class="pill" style="{css_box(fx + 310, fy + 100, None, None, 7)}background:#facc15;color:{INK};font-size:60px;opacity:0">BALÓN DE ORO 2010</div>')
    yr, yh = roller("yr", "2010", 64, INK)
    card("uefa", fx + 60, fy + 290, 840, 170, f'''
      <div style="position:absolute;left:30px;top:25px">{icon("trophy", 120, "#ca8a04", 2.4)}</div>
      <div style="position:absolute;left:180px;top:26px;font:900 48px {FONT};color:{INK};white-space:nowrap">MEJOR JUGADOR</div>
      <div style="position:absolute;left:180px;top:90px;font:900 48px {FONT};color:#2563eb;white-space:nowrap">DE EUROPA</div>
      <div id="yrbox" style="position:absolute;right:30px;top:40px;padding:6px 18px;border-radius:18px;background:#f1f5f9;display:flex">{yr}</div>''')
    pods = [("p2", "2", fx + 60, 260, "#cbd5e1"), ("p1", "1", fx + 350, 340, "#facc15"), ("p3", "3", fx + 640, 200, "#d97706")]
    for pid, n, x, h, col in pods:
        add(f'<div id="{pid}" class="pod" style="{css_box(x, fl - h, 260, h, 5)}background:{col};transform-origin:50% 100%">{n}</div>')
    add(character("ini3", "ini", fx + 190, fl - 260, 0.72, z=6))
    t_ese, t_que, t_seg, t_bal, t_oro, t_12, t_ele, t_mej, t_eur = (P("ese", 3), P("quedo"), P("segundo"), P("balon", 2), P("oro"),
                                                                  P("2012"), P("elegido"), P("mejor"), P("europa"))
    travel(t_ese - 0.3, F(2, 1), 2, 1630, dur=0.75)
    js(f'tl.fromTo(".pod", {{scaleY:0}}, {{scaleY:1, duration:0.4, stagger:0.08, ease:"back.out(1.6)"}}, {t_ese:.3f});')
    sfx(t_ese + 0.1, "madera", 0.3)
    life("ini3", 0, G.DUR, 4)
    js(f'tl.fromTo("#ini3", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.45, ease:"bounce.out"}}, {t_seg - 0.1:.3f});')
    js(f'tl.to("#p2", {{backgroundColor:"#e2e8f0", scaleY:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_seg:.3f});')
    sfx(t_seg, "pop", 0.3)
    js(f'tl.fromTo("#gb", {{opacity:0, scale:0.3, rotation:-120}}, {{opacity:1, scale:1, rotation:0, duration:0.5, ease:"back.out(2)"}}, {t_bal:.3f});')
    pop("#gbp", t_oro, sound="pop2")
    js(f'tl.to("#gb", {{rotation:360, duration:5, ease:"none"}}, {t_oro + 0.5:.3f});')
    slide_in("#uefa", t_12 - 0.2, dy=60, sound="pop")
    roll_set("yr", "2010", yh)
    roll_to("yr", "2012", yh, t_12, dur=0.5, from_text="2010")
    js(f'tl.to("#ini3", {{y:-20, duration:0.2, yoyo:true, repeat:1}}, {t_mej:.3f}); wave("ini3", {t_ele:.3f}, {E("europa") + 0.4:.3f});')
    js(f'tl.to("#uefa", {{scale:1.04, duration:0.15, yoyo:true, repeat:1}}, {t_eur:.3f});')
    sfx(t_eur, "check", 0.35)


# ================================================================= LA GRADA DEL ESPANYOL
def scene_grada():
    fx, fy, fw, fh = F(3, 1)
    fans = []
    for r in range(4):
        for c in range(9):
            fans.append(f'<div class="fan" style="left:{30 + c * 100 + (r % 2) * 40}px;top:{60 + r * 130}px;background:{["#2563eb", "#f8fafc"][(r + c) % 2]}"></div>')
    add(f'<div id="stand" class="stand" style="{css_box(fx, fy + 260, fw, 620, 4)}">{"".join(fans)}</div>')
    card("esp", fx + 60, fy + 20, 840, 210, f'''
      <div style="position:absolute;left:36px;top:30px;font:900 72px {FONT};color:#2563eb">AFICIÓN ESPANYOL</div>
      <div id="rival" class="pill" style="position:absolute;left:36px;top:124px;background:{INK};color:#fff;font-size:46px;opacity:0">el gran rival del Barça</div>''')
    add(f'<div id="pie" class="pill" style="{css_box(fx + 250, fy + 930, None, None, 8)}background:{GOOD_BG};color:#fff;font-size:62px;opacity:0">{icon("hand", 62, "#fff", 2.6)} EN PIE</div>')
    t_has, t_afi, t_riv, t_apl, t_pie = P("hasta"), P("aficion"), P("rival"), P("aplaudido"), P("pie")
    travel(t_has - 0.3, F(3, 1), 3, 1630, dur=0.75)
    hide_mile(2, t_has + 0.2)
    slide_in("#esp", t_afi, dy=-60, sound="pop")
    pop("#rival", t_riv, sound=None)
    js(f'tl.fromTo("#stand", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_has:.3f});')
    js(f'tl.to(".fan", {{y:-18, duration:0.18, yoyo:true, repeat:{int((G.DUR - t_apl) / 0.18)}, stagger:{{each:0.02, from:"random"}}}}, {t_apl:.3f});')
    sfx(t_apl, "pop2", 0.3)
    js(f'tl.to(".fan", {{scaleY:1.35, transformOrigin:"50% 100%", duration:0.3, stagger:{{each:0.01, from:"center"}}}}, {t_pie:.3f});')
    stamp("#pie", t_pie, rot=-6)
    sfx(t_pie, "golpe", 0.3)


def scene_final():
    fx, fy, fw, fh = F(3, 0)
    cta = "Yo estaba…"
    card("cbox", fx + 60, fy + 200, 840, 520, f'''
      <div style="position:absolute;left:40px;top:40px;display:flex;align-items:center;gap:22px">{icon("message-circle", 90, INK, 2.4)}
        <span style="font:900 72px {FONT};color:{INK}">Comentarios</span></div>
      <div style="position:absolute;left:40px;top:170px;font:900 54px {FONT};color:#555">¿Dónde estabas tú?</div>
      <div id="ctt" style="position:absolute;left:40px;top:270px;font:800 76px {FONT};color:{INK}">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 760, fy + 640, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_don, t_mar, t_cue, t_com = P("donde"), P("marco"), P("cuentamelo"), P("comentarios")
    travel(t_don - 0.2, F(3, 0), 3, 570, dur=0.7)
    slide_in("#cbox", t_don, dy=80)
    type_on("#ctt .kc", len(cta), t_mar, t_cue + 0.2)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_cue:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.2:.3f});')
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.7, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.pitchroom {{ background:repeating-linear-gradient(0deg,#166534 0 90px,#15803d 90px 180px); }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:76px; top:28px; }}
.goalframe {{ border:18px solid #f8fafc; border-bottom:none; border-radius:10px 10px 0 0; }}
.net {{ position:absolute; inset:0; background:repeating-linear-gradient(45deg,rgba(255,255,255,0.25) 0 4px,transparent 4px 34px),repeating-linear-gradient(-45deg,rgba(255,255,255,0.25) 0 4px,transparent 4px 34px); }}
.ball {{ border-radius:50%; display:flex; align-items:center; justify-content:center; }}
.score {{ border-radius:30px; background:#0b1220; border:6px solid #334155; display:flex; align-items:center; justify-content:center; gap:26px; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.team {{ font:900 76px {FONT}; color:#fff; }}
.dash, .goal0 {{ font:900 110px {FONT}; color:#fff; }}
.minute {{ position:absolute; right:-20px; top:-34px; padding:4px 18px; border-radius:16px; background:{ACC}; color:{INK}; font:900 50px {FONT}; }}
.minute:empty {{ display:none; }}
@font-face {{ font-family:'Caveat'; font-weight:700; src:url('../assets/fonts/caveat-700.woff2') format('woff2'); }}
.tee {{ border-radius:30px 30px 20px 20px; background:#f8fafc; display:flex; align-items:center; justify-content:center; box-shadow:0 20px 50px rgba(0,0,0,0.45); }}
.tee span {{ font:700 58px 'Caveat', cursive; color:#1e3a8a; text-align:center; line-height:1.15;  }}
.num21 {{ position:absolute; left:40px; top:40px; width:180px; height:250px; border-radius:24px; background:repeating-linear-gradient(90deg,#2563eb 0 30px,#fff 30px 60px);
  font:900 120px {FONT}; color:{INK}; text-align:center; line-height:250px; -webkit-text-stroke:4px #fff; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; }}
.notif {{ border-radius:28px; background:rgba(255,255,255,0.96); display:flex; align-items:center; gap:22px; padding-left:22px;
  font:900 54px {FONT}; color:{BAD}; box-shadow:0 14px 30px rgba(0,0,0,0.35); white-space:nowrap; opacity:0; }}
.nicon {{ width:76px; height:76px; border-radius:22px; display:flex; align-items:center; justify-content:center; flex:none; }}
.pitch {{ border:8px solid rgba(255,255,255,0.7); border-radius:10px; }}
.pline {{ position:absolute; left:0; right:0; bottom:0; height:0; border-top:6px solid rgba(255,255,255,0.7); }}
.pcircle {{ position:absolute; left:50%; bottom:-120px; width:240px; height:240px; margin-left:-120px; border:6px solid rgba(255,255,255,0.7); border-radius:50%; }}
.pbox {{ position:absolute; left:180px; right:180px; top:0; height:260px; border:6px solid rgba(255,255,255,0.7); border-top:none; }}
.parea {{ position:absolute; left:340px; right:340px; top:0; height:110px; border:6px solid rgba(255,255,255,0.7); border-top:none; }}
.pgoal {{ position:absolute; left:400px; right:400px; top:-40px; height:44px; background:repeating-linear-gradient(90deg,#fff 0 4px,transparent 4px 20px); border:6px solid #fff; border-bottom:none; }}
.token {{ border-radius:50%; border:6px solid #fff; box-shadow:0 10px 24px rgba(0,0,0,0.4); }}
.token.red {{ background:#c8102e; }} .token.orange {{ background:#f97316; opacity:0.9; }} .token.keeper {{ background:#facc15; }}
.tlab {{ position:absolute; left:50%; top:112px; transform:translateX(-50%); padding:2px 16px; border-radius:12px; background:rgba(15,23,42,0.85); color:#fff; font:900 46px {FONT}; white-space:nowrap; }}
.under {{ border-radius:60px 60px 30px 30px; background:#f8fafc; box-shadow:0 30px 70px rgba(0,0,0,0.5); }}
.handw {{ position:absolute; left:50px; right:50px; top:150px; font:700 92px 'Caveat', cursive; color:#1e3a8a;  line-height:1.15; text-align:center; }}
.redsh {{ border-radius:60px 60px 30px 30px; background:#c8102e; box-shadow:0 30px 70px rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; }}
.redsh span {{ font:900 300px {FONT}; color:#facc15; }}
.rshl {{ position:absolute; top:60px; left:0; right:0; text-align:center; font:900 66px {FONT}; color:#facc15; }}
.ycard {{ border-radius:16px; background:#facc15; border:6px solid #fff; box-shadow:0 20px 50px rgba(0,0,0,0.5); opacity:0; }}
.stand {{ border-radius:30px; background:#0f172a; overflow:hidden; }}
.fan {{ position:absolute; width:70px; height:110px; border-radius:35px 35px 10px 10px; }}
.pubb {{ position:absolute; right:40px; bottom:40px; padding:16px 50px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 70px {FONT}; }}
.hc, .kc {{ opacity:0; }}

.beam {{ background:linear-gradient(180deg, rgba(255,255,255,0.55), rgba(255,255,255,0)); clip-path:polygon(45% 0,55% 0,100% 100%,0 100%); filter:blur(6px); }}
.clk {{ border-radius:28px; border:5px solid #fff; background:#0b1220; display:flex; align-items:center; justify-content:center; gap:14px; }}
.tv {{ border-radius:34px; background:#0b1220; border:6px solid {ACC}; box-shadow:0 24px 60px rgba(0,0,0,0.6); }}
.tvq {{ position:absolute; left:250px; top:70px; font:900 76px {FONT}; color:#fff; line-height:1.05; white-space:nowrap; }}
.ring {{ border-radius:50%; border:8px solid {ACC}; }}
.candle {{ border-radius:18px 18px 10px 10px; background:linear-gradient(90deg,#f1f5f9,#e2e8f0); }}
.flame {{ border-radius:50% 50% 50% 50% / 60% 60% 40% 40%; background:radial-gradient(circle at 50% 70%, #fff7c2, #facc15 45%, #f97316 80%); box-shadow:0 0 60px 20px rgba(250,204,21,0.35); }}
.pod {{ border-radius:20px 20px 0 0; display:flex; justify-content:center; padding-top:20px; font:900 110px {FONT}; color:rgba(15,23,42,0.55); }}
.goldball {{ border-radius:50%; background:radial-gradient(circle at 35% 30%, #fff3b0, #facc15 40%, #b45309 100%); box-shadow:0 0 70px 10px rgba(250,204,21,0.35); }}
.sun {{ border-radius:50%; background:radial-gradient(circle, #fde68a, #facc15 60%, #f59e0b); box-shadow:0 0 120px 40px rgba(250,204,21,0.35); }}
.pillx {{ position:relative; }}
.pillx span {{ position:absolute; left:0; right:0; top:0; bottom:0; display:flex; align-items:center; justify-content:center; gap:14px; }}
"""

def build():
    world()
    scene_hook()
    scene_jugada()
    scene_camiseta()
    scene_dani()
    scene_luz()
    scene_premios()
    scene_grada()
    scene_final()
