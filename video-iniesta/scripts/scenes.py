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
def world():
    for r in range(4):
        for c in (0, 1):
            pitch = (r, c) in ((2, 0),)
            cls = "room pitchroom" if pitch else "room"
            add(f'<div class="{cls}" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#c8102e"/><stop offset="0.5" stop-color="#facc15"/><stop offset="1" stop-color="#c8102e"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in [("Agosto 2009", 0, 1630), ("Temporada 09-10", 1, 570), ("Johannesburgo", 2, 1630), ("Cornellà", 3, 570)]:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 240, ROAD[r] + 34, 480, 70, 2)}">{lab}</div>')


def scoreboard(sid, x, y, w=840, left="ESP", right="NED", z=7, minute=""):
    sc, sh = roller(f"{sid}-g", "0", 110, "#fff")
    add(f'''<div id="{sid}" class="score" style="{css_box(x, y, w, 190, z)}">
      <span class="team">{left}</span>{sc}<span class="dash">-</span><span class="goal0">0</span><span class="team">{right}</span>
      <span id="{sid}-min" class="minute">{minute}</span></div>''')
    return sh


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    add(f'''<div id="goal0" style="{css_box(fx + 120, fy + 40, 720, 420, 4)}" class="goalframe"><div id="net0" class="net"></div></div>''')
    add(f'<div id="ball0" class="ball" style="{css_box(fx + 430, fy + 700, 100, 100, 8)}">{icon("volleyball", 96, INK, 2.2).replace("<svg", "<svg fill=\"#fff\"")}</div>')
    sh = scoreboard("sb0", fx + 60, fy + 480)
    add(f'<div id="tee0" class="tee" style="{css_box(fx + 530, fy + 680, 320, 250, 6)}"><span>Dani Jarque<br>siempre con<br>nosotros</span></div>')
    add(character("ini0", "ini", fx + 300, fl, 1.15, z=6))
    add(f'<div id="mood" class="pill" style="{css_box(fx + 520, fy + 980, None, None, 8)}background:{BAD};color:#fff;opacity:0">{icon("cloud-rain", 50, "#fff", 2.6)} HUNDIDO</div>')
    cam(0, (fx + 80, fy + 20, 800, 820), whoosh=False)
    js(f'tl.fromTo("#ball0", {{x:0, y:0, scale:1.6}}, {{x:0, y:-520, scale:0.7, duration:0.35, ease:"power3.in"}}, 0);')
    js('tl.fromTo("#net0", {scaleY:1}, {scaleY:0.82, transformOrigin:"50% 0%", duration:0.12, yoyo:true, repeat:3}, 0.33);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.34, "golpe", 0.5)
    shake(0.35, 18)
    js(f'tl.set("#ball0", {{opacity:0}}, 1.2);')
    roll_set("sb0-g", "0", sh)
    js(f'tl.to("#sb0-g-d0", {{y:{-(10 + 1) * sh}, duration:0.4, ease:"back.out(2)"}}, 0.45);')
    t_esp, t_ded, t_ami, t_mue = P("espana"), P("dedico"), P("amigo"), P("muerto")
    js(f'tl.fromTo("#tee0", {{opacity:0, y:40, rotation:-6}}, {{opacity:1, y:0, rotation:3, duration:0.4, ease:"back.out(2)"}}, {t_ded:.3f});')
    sfx(t_ded, "pop2", 0.3)
    js(f'tl.to("#tee0", {{rotation:-2, duration:0.4}}, {t_mue:.3f});')
    t_y, t_mar, t_hun = P("y"), P("marco"), P("hundido")
    life("ini0", 0, G.DUR, 1)
    js(f'tl.fromTo("#ini0", {{opacity:0, x:-200}}, {{opacity:1, x:0, duration:0.5}}, {t_y:.3f}); walk("ini0", {t_y:.3f}, {t_y + 0.5:.3f}, 0.13);')
    js(f'tl.to(Q("ini0","head"), {{rotation:18, svgOrigin:PIV.head, duration:0.5}}, {t_hun:.3f}); tl.to(Q("ini0","eyes"), {{scaleY:0.3, svgOrigin:PIV.eyes, duration:0.3}}, {t_hun:.3f});')
    pop("#mood", t_hun, sound="pop2")


# ================================================================= 1 · EL AMIGO
def scene_amigo():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "1", "EL AMIGO", color="#2563eb", txt="#fff")
    cal, ch = roller("cal9", "0000", 70, "#fff")
    card("dani", fx, fy + 170, fw, 330, f'''
      <div class="num21">21</div>
      <div style="position:absolute;left:250px;top:40px;font:900 76px {FONT};color:{INK}">DANI JARQUE</div>
      <div id="capt" class="pill" style="position:absolute;left:250px;top:140px;background:{ACC};color:{INK};opacity:0">CAPITÁN · ESPANYOL</div>
      <div id="age" style="position:absolute;left:250px;top:230px;font:800 54px {FONT};color:#555;opacity:0">26 años</div>
      <div id="hrt" style="position:absolute;right:40px;top:150px;opacity:0">{icon("heart-crack", 130, BAD, 2.4)}</div>''')
    add(f'<div id="cal" class="cnt" style="{css_box(fx + 260, fy + 530, 440, 120, 8)}background:{INK}"><span style="font:900 56px {FONT};color:#fff;margin-right:16px">AGO</span>{cal}</div>')
    add(character("kid1", "jar", fx + 300, fl, 1.0, z=6))
    add(character("kid2", "ini", fx + 640, fl, 1.0, z=6))
    add(f'<div id="sel" class="pill" style="{css_box(fx + 280, fy + 680, None, None, 8)}background:#c8102e;color:#fff;opacity:0">SELECCIÓN · INFERIORES</div>')
    t_uno, t_ami2, t_ago, t_09, t_dan, t_cap, t_esp, t_inf, t_26 = (P("uno"), P("amigo", 2), P("agosto"), P("2009"), P("dani"),
                                                                   P("capitan"), P("espanyol"), P("infarto"), P("26"))
    travel(t_uno, F(0, 1), 0, 1630, dur=0.85)
    header_in("h1", t_uno, t_ami2)
    pop("#cal", t_ago, sound="pop2")
    roll_set("cal9", "0000", ch)
    roll_to("cal9", "2009", ch, t_09, dur=0.6)
    slide_in("#dani", t_dan, dy=-60, sound="pop")
    pop("#capt", t_cap, sound=None)
    pop("#hrt", t_inf, sound="golpe", vol=0.35)
    js(f'tl.to("#hrt", {{opacity:0.35, duration:0.6}}, {t_inf + 0.8:.3f});')
    js(f'tl.fromTo("#age", {{opacity:0, x:-20}}, {{opacity:1, x:0, duration:0.3}}, {t_26:.3f});')
    t_era, t_ini, t_cat, t_sel = P("era"), P("iniesta"), P("categorias"), P("seleccion")
    for k, cid in enumerate(("kid1", "kid2")):
        life(cid, 0, G.DUR, 10 + k)
        js(f'tl.fromTo("#{cid}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_era + k * 0.4:.3f});')
    js(f'tl.to(Q("kid1","armR"), {{rotation:-150, svgOrigin:PIV.armR, duration:0.25}}, {t_cat:.3f}); tl.to(Q("kid2","armL"), {{rotation:150, svgOrigin:PIV.armL, duration:0.25}}, {t_cat:.3f});')
    js(f'jump("kid1", {t_cat + 0.25:.3f}, 40); jump("kid2", {t_cat + 0.3:.3f}, 40);')
    sfx(t_cat + 0.25, "click", 0.4)
    pop("#sel", t_sel, sound="pop2")
    cam(E("seleccion") + 0.05, ROW(0), dur=0.4)


# ================================================================= 2 · EL BAJÓN
def scene_bajon():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    header("h2", fx, fy, "2", "EL BAJÓN", color="#64748b", txt="#fff")
    for i in range(4):
        add(f'''<div id="les{i}" class="notif" style="{css_box(fx + 470, fy + 180 + i * 125, 480, 110, 8)}">
          <div class="nicon" style="background:{BAD}">{icon("bandage", 54, "#fff", 2.6)}</div><span>LESIÓN {i + 1}</span></div>''')
    add(character("ini1", "ini", fx + 230, fl, 1.15, z=6))
    add(f'<div id="cloud" style="{css_box(fx + 70, fy + 300, 320, 220, 9)}">{icon("cloud-rain", 300, "#94a3b8", 2.0).replace("<svg", "<svg fill=\"#475569\"")}</div>')
    add(f'<div id="dep" class="pill" style="{css_box(fx + 60, fy + 560, None, None, 8)}background:#475569;color:#fff;opacity:0">DEPRESIÓN</div>')
    card("book", fx + 470, fy + 720, 480, 330, f'''
      <div style="position:absolute;left:30px;top:30px">{icon("book-open", 120, INK, 2.2)}</div>
      <div style="position:absolute;left:30px;top:170px;font:900 50px {FONT};color:{INK};line-height:1.1">La jugada<br>de mi vida</div>''')
    t_dos, t_baj, t_tem, t_les, t_mus, t_cay, t_dep = (P("dos"), P("bajon"), P("temporada"), P("lesiones"), P("musculares"),
                                                     P("cayo"), P("depresion"))
    travel(t_dos, F(1, 1), 1, 1630, dur=0.85)
    js(f'tl.to("#mile0", {{opacity:0, duration:0.3}}, {t_dos + 0.3:.3f});')
    header_in("h2", t_dos, t_baj)
    life("ini1", 0, G.DUR, 2)
    for i, t in enumerate([t_les, t_les + 0.3, t_mus, t_mus + 0.3]):
        js(f'tl.fromTo("#les{i}", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.35, ease:"bounce.out"}}, {t:.3f});')
        sfx(t, "pop2", 0.25)
    js(f'tl.to(Q("ini1","head"), {{rotation:18, svgOrigin:PIV.head, duration:0.5}}, {t_cay:.3f}); tl.to("#ini1", {{y:40, duration:0.5}}, {t_cay:.3f});')
    js(f'tl.fromTo("#cloud", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.6, ease:"power2.out"}}, {t_cay:.3f});')
    pop("#dep", t_dep, sound="golpe", vol=0.3)
    t_con, t_lib, t_jug = P("conto"), P("libro"), P("jugada")
    js(f'tl.to(".notif", {{opacity:0, x:120, duration:0.3, stagger:0.05}}, {t_con - 0.1:.3f});')
    slide_in("#book", t_lib, dy=80, sound="papel", vol=0.4)
    js(f'tl.to("#cloud", {{opacity:0.25, y:-60, duration:0.8}}, {t_jug:.3f}); tl.to(Q("ini1","head"), {{rotation:0, svgOrigin:PIV.head, duration:0.5}}, {t_jug:.3f}); tl.to("#ini1", {{y:0, duration:0.5}}, {t_jug:.3f});')


# ================================================================= 3 · EL MINUTO 116
def scene_previa():
    fx, fy, fw, fh = F(1, 0)
    header("h3", fx, fy, "3", "MINUTO 116", color=ACC)
    sh = scoreboard("sb1", fx + 60, fy + 190, minute="116'")
    cal, ch = roller("cal10", "0000", 70, "#fff")
    add(f'<div id="cal2" class="cnt" style="{css_box(fx + 200, fy + 440, 560, 130, 8)}background:{INK}"><span style="font:900 56px {FONT};color:#fff;margin-right:16px">11 JUL</span>{cal}</div>')
    add(f'<div id="final" class="pill" style="{css_box(fx + 140, fy + 620, None, None, 8)}background:#fff;color:{INK};font-size:58px;opacity:0">{icon("trophy", 56, "#ca8a04", 2.4)} FINAL DEL MUNDIAL</div>')
    add(f'<div id="pror" class="pill" style="{css_box(fx + 220, fy + 760, None, None, 8)}background:{BAD};color:#fff;font-size:58px;opacity:0">{icon("timer", 56, "#fff", 2.4)} PRÓRROGA</div>')
    t_tres, t_116, t_jul, t_10, t_fin, t_hol, t_pro = (P("tres"), P("116"), P("julio"), P("2010"), P("final"), P("holanda"), P("prorroga"))
    travel(t_tres, F(1, 0), 1, 570, dur=0.85)
    header_in("h3", t_tres, P("minuto"))
    pop("#sb1", t_116 - 0.1, sound="pop")
    js(f'tl.fromTo("#sb1-min", {{scale:1.6, color:"#fff"}}, {{scale:1, color:"{INK}", duration:0.4, ease:"back.out(2)"}}, {t_116:.3f});')
    pop("#cal2", t_jul - 0.3, sound=None)
    roll_set("cal10", "0000", ch)
    roll_to("cal10", "2010", ch, t_10, dur=0.6)
    pop("#final", t_fin, sound="pop2")
    js(f'tl.to("#sb1", {{scale:1.04, duration:0.15, yoyo:true, repeat:1}}, {t_hol:.3f});')
    pop("#pror", t_pro, sound="pop2")


def scene_jugada():
    fx, fy, fw, fh = F(2, 0)
    add(f'''<div id="pitch" data-layout-ignore style="{css_box(fx, fy + 40, fw, 1020, 3)}" class="pitch">
      <div class="pbox"></div><div class="parea"></div><div class="pcircle"></div><div class="pline"></div>
      <div id="net1" class="pgoal"></div></div>''')
    pts = {"puyol": (300, 900), "navas": (790, 690), "torres": (820, 360), "cesc": (360, 470), "iniesta": (620, 250)}
    for name, (x, y) in pts.items():
        add(f'<div id="tk-{name}" class="token red" style="{css_box(fx + x - 55, fy + y - 55, 110, 110, 6)}"><span class="tlab">{name.capitalize()}</span></div>')
    for k, (x, y) in enumerate([(200, 600), (560, 640), (700, 470), (480, 330), (300, 300)]):
        add(f'<div class="token orange" style="{css_box(fx + x - 45, fy + y - 45, 90, 90, 5)}"></div>')
    add(f'<div class="token keeper" style="{css_box(fx + 435, fy + 70, 90, 90, 5)}"></div>')
    add(f'<div id="ball1" class="ball" style="{css_box(fx + 300 - 30, fy + 900 - 30, 60, 60, 9)}">{icon("volleyball", 58, INK, 2.2).replace("<svg", "<svg fill=\"#fff\"")}</div>')
    seq = [("puyol", "navas", P("navas")), ("navas", "torres", P("torres") - 0.3), ("torres", "cesc", P("rebota")),
           ("cesc", "iniesta", P("cesc", 2) + 0.2)]
    path_d = []
    for a, b, t in seq:
        (x0, y0), (x1, y1) = pts[a], pts[b]
        path_d.append(f'<path id="seg-{a}" d="M {x0} {y0 + 40} L {x1} {y1 + 40}" stroke="{ACC}" stroke-width="10" fill="none" stroke-dasharray="20 14" opacity="0"/>')
    path_d.append(f'<path id="seg-shot" d="M {pts["iniesta"][0]} {pts["iniesta"][1] + 40} L 480 120" stroke="#fff" stroke-width="12" fill="none" opacity="0"/>')
    add(f'<svg data-layout-ignore style="{css_box(fx, fy, 960, 1080, 5)}overflow:visible" viewBox="0 0 960 1080">{"".join(path_d)}</svg>')
    sh = scoreboard("sb2", fx + 60, fy - 20, minute="116'", z=10)
    add(f'<div id="star" style="{css_box(fx + 380, fy + 480, 200, 200, 11)}opacity:0">{icon("star", 200, "#facc15", 2).replace("<svg", "<svg fill=\"#facc15\"")}</div>')
    add(f'<div id="champ" class="pill" style="{css_box(fx + 70, fy + 700, None, None, 11)}background:#c8102e;color:#fff;font-size:62px;opacity:0">CAMPEONES DEL MUNDO</div>')
    t_puy = P("puyol")
    travel(t_puy - 0.3, F(2, 0), 2, 570, dur=0.7)
    js(f'tl.to("#mile1", {{opacity:0, duration:0.3}}, {t_puy - 0.3 + 0.3:.3f});')
    js(f'tl.fromTo(".token", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, stagger:0.04, ease:"back.out(2)"}}, {t_puy - 0.2:.3f});')
    pop("#tk-puyol", t_puy, sound="pop2", vol=0.3)
    js(f'tl.fromTo("#ball1", {{opacity:0}}, {{opacity:1, duration:0.2}}, {t_puy:.3f});')
    js('tl.set("#sb2", {opacity:0}, 0);')
    for a, b, t in seq:
        (x0, y0), (x1, y1) = pts[a], pts[b]
        js(f'tl.to("#ball1", {{x:{x1 - pts["puyol"][0]}, y:{y1 - pts["puyol"][1]}, duration:0.45, ease:"power1.inOut"}}, {t:.3f});')
        js(f'tl.to("#seg-{a}", {{opacity:1, duration:0.2}}, {t:.3f});')
        js(f'tl.to("#tk-{b}", {{scale:1.25, duration:0.15, yoyo:true, repeat:1}}, {t + 0.4:.3f});')
        sfx(t, "click", 0.3)
    t_con, t_dis, t_gol = P("controla"), P("dispara"), P("gol", 2)
    cam(t_con - 0.2, (fx + 260, fy + 40, 560, 600), dur=0.6)
    js(f'tl.to("#ball1", {{x:{480 - pts["puyol"][0]}, y:{120 - pts["puyol"][1]}, duration:0.7, ease:"power2.in"}}, {t_dis + 0.15:.3f});')
    js(f'tl.to("#seg-shot", {{opacity:1, duration:0.2}}, {t_dis + 0.15:.3f});')
    sfx(t_dis + 0.15, "whoosh", 0.4)
    # CLÍMAX
    js(f'tl.fromTo("#net1", {{scaleY:1}}, {{scaleY:1.5, transformOrigin:"50% 100%", duration:0.12, yoyo:true, repeat:3}}, {t_gol - 0.05:.3f});')
    shake(t_gol, 26)
    sfx(t_gol, "golpe-climax", 0.6)
    cam(t_gol + 0.15, F(2, 0), dur=0.5)
    js(f'tl.to("#sb2", {{opacity:1, duration:0.3}}, {t_gol:.3f});')
    roll_set("sb2-g", "0", sh)
    js(f'tl.to("#sb2-g-d0", {{y:{-(10 + 1) * sh}, duration:0.4, ease:"back.out(2)"}}, {t_gol + 0.1:.3f});')
    t_cam, t_pri = P("campeona"), P("primera")
    js(f'tl.fromTo("#star", {{opacity:0, scale:0.2, rotation:-90}}, {{opacity:1, scale:1, rotation:0, duration:0.5, ease:"back.out(2)"}}, {t_cam:.3f});')
    pop("#champ", t_pri, sound="pop")
    hearts("hj-", fx + 480, fy + 650, 6, t_cam + 0.2, spread=700, rise=300)


def scene_camiseta():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    msg = "Dani Jarque siempre con nosotros"
    add(f'''<div id="under" class="under" style="{css_box(fx + 180, fy + 60, 600, 640, 4)}">
      <div id="ut" class="handw">{chars(msg, "hc")}</div></div>''')
    add(f'''<div id="redsh" class="redsh" style="{css_box(fx + 180, fy + 60, 600, 640, 5)}"><span>6</span><div class="rshl">INIESTA</div></div>''')
    add(f'<div id="yc" class="ycard" style="{css_box(fx + 720, fy + 720, 170, 240, 8)}"></div>')
    add(character("ini2", "ini", fx + 300, fl, 1.0, z=6))
    t_ini, t_qui, t_cam, t_deb, t_dan, t_nos = (P("iniesta", 4), P("quita"), P("camiseta"), P("debajo"), P("dani", 2), P("nosotros"))
    travel(t_ini - 0.2, F(2, 1), 2, 1630, dur=0.7)
    js(f'tl.fromTo("#redsh, #under", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_ini:.3f});')
    js(f'tl.to("#redsh", {{y:-700, rotation:-8, duration:0.6, ease:"power3.in"}}, {t_qui + 0.1:.3f}); tl.to("#redsh", {{opacity:0, duration:0.2}}, {t_qui + 0.6:.3f});')
    sfx(t_qui + 0.1, "whoosh-corto", 0.35)
    type_on("#ut .hc", len(msg), t_dan, t_nos + 0.4)
    life("ini2", 0, G.DUR, 3)
    js(f'tl.fromTo("#ini2", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_deb:.3f}); point("ini2", "R", {t_deb:.3f}, {t_nos + 0.5:.3f}, -130);')
    t_tar, t_ama, t_imp = P("tarjeta"), P("amarilla"), P("importo")
    js(f'tl.fromTo("#yc", {{opacity:0, rotation:-90, scale:0.4}}, {{opacity:1, rotation:12, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_tar:.3f});')
    sfx(t_tar, "pop", 0.35)
    js(f'tl.to(Q("ini2","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.2}}, {t_imp:.3f}); jump("ini2", {t_imp:.3f}, 40);')
    cam(E("importo") + 0.05, ROW(2), dur=0.4)


def scene_grada():
    fx, fy, fw, fh = F(3, 1)
    fans = []
    for r in range(4):
        for c in range(9):
            fans.append(f'<div class="fan" style="left:{30 + c * 100 + (r % 2) * 40}px;top:{40 + r * 130}px;background:{["#2563eb", "#f8fafc"][(r + c) % 2]}"></div>')
    add(f'<div id="stand" class="stand" style="{css_box(fx, fy + 260, fw, 620, 4)}">{"".join(fans)}</div>')
    card("esp", fx + 60, fy + 20, 840, 210, f'''
      <div style="position:absolute;left:36px;top:30px;font:900 72px {FONT};color:#2563eb">AFICIÓN ESPANYOL</div>
      <div id="rival" class="pill" style="position:absolute;left:36px;top:124px;background:{INK};color:#fff;font-size:46px;opacity:0">el gran rival del Barça</div>''')
    ap, ah = roller("clap", "0000", 90, "#fff")
    add(f'<div id="cl" class="cnt" style="{css_box(fx + 200, fy + 920, 560, 140, 8)}background:{GOOD_BG}">{icon("hand", 80, "#fff", 2.4)}{ap}</div>')
    t_des, t_afi, t_esp, t_riv, t_bar, t_apl, t_est = (P("desde", 2), P("aficion"), P("espanyol", 2), P("rival"), P("barca"), P("aplaude"), P("estadio"))
    travel(t_des - 0.2, F(3, 1), 3, 1630, dur=0.75)
    js(f'tl.to("#mile2", {{opacity:0, duration:0.3}}, {t_des - 0.2 + 0.3:.3f});')
    slide_in("#esp", t_afi, dy=-60, sound="pop")
    pop("#rival", t_riv, sound=None)
    js(f'tl.fromTo("#stand", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_afi:.3f});')
    js(f'tl.to(".fan", {{y:-26, duration:0.18, yoyo:true, repeat:{int((G.DUR - t_apl) / 0.18)}, stagger:{{each:0.02, from:"random"}}}}, {t_apl:.3f});')
    sfx(t_apl, "pop2", 0.3)
    pop("#cl", t_apl, sound=None)
    roll_set("clap", "0000", ah)
    roll_to("clap", "9999", ah, t_apl + 0.1, dur=1.4, spins=2)


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
    t_don, t_mar, t_cue, t_com = P("donde"), P("marco", 2), P("cuentamelo"), P("comentarios")
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
"""


def build():
    world()
    scene_hook()
    scene_amigo()
    scene_bajon()
    scene_previa()
    scene_jugada()
    scene_camiseta()
    scene_grada()
    scene_final()
