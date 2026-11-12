"""Escenas del vídeo «Por qué acabó Aquí no hay quien viva y nació La que se avecina». Un solo mundo:
un camino en zigzag 2006 -> Antena 3 -> Telecinco -> Juzgado que se dibuja mientras viaja la cámara."""
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




def montepinar(mid, x, y, w, h, z=4):
    """Edificio moderno (estilo urbanización) para La que se avecina."""
    rows = []
    fh = (h - 200) / 4
    for f in range(4):
        rows.append(f'<div id="{mid}-fl{f}" class="mfloor" style="top:{90 + f * fh:.0f}px;height:{fh:.0f}px">'
                    + "".join(f'<div class="mwin" style="left:{30 + i * (w - 60) / 3:.0f}px;width:{(w - 60) / 3 - 24:.0f}px"></div>' for i in range(3))
                    + '<div class="mglass"></div></div>')
    add(f'''<div id="{mid}" class="mont" style="{css_box(x, y, w, h, z)}">
      <div class="mtop"><span id="{mid}-sg">MIRADOR DE MONTEPINAR</span></div>{"".join(rows)}<div class="mdoor"></div></div>''')


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#ffd43b"/><stop offset="1" stop-color="#22c55e"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in [("2006", 0, 570), ("Antena 3", 1, 1630), ("Telecinco", 2, 570), ("Juzgado · 2012", 3, 1630)]:
        add(f'<div class="mile" data-layout-ignore style="{css_box(x - 230, ROAD[r] + 34, 460, 70, 2)}">{lab}</div>')


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    facade("fac0", fx + 160, fy + 330, 640, 740, n_win=5, scale_win=1.0)
    aud, ah = roller("aud0", "0", 64, "#fff")
    add(f'''<div id="aud" class="panel" style="{css_box(fx + 80, fy + 30, 800, 240, 7)}">
      <div class="ptit">{icon("trending-up", 60, GOOD, 2.6)}<span>Audiencia</span></div>
      <div id="lider" class="pill" style="position:absolute;left:40px;top:130px;background:{GOOD_BG};color:#fff;font-size:64px;opacity:0">{icon("crown", 52, "#fff", 2.6)} LÍDER</div></div>''')
    add(f'<div id="st-can" class="stamp" style="{css_box(fx + 200, fy + 540, None, None, 9)}color:{BAD};border-color:{BAD};font-size:84px">CANCELADA</div>')
    cam(0, (fx + 60, fy + 0, 840, 520), whoosh=False)
    cam(0.1, F(0, 0), dur=0.9, ease="power3.inOut", whoosh=False)
    js('tl.fromTo("#aud", {y:-400}, {y:0, duration:0.4, ease:"bounce.out"}, 0);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.35, "golpe", 0.4)
    for f in range(4):
        js(f'tl.fromTo("#fac0-fl{3 - f}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.25, ease:"back.out(2)"}}, {0.1 + 0.1 * f:.3f});')
    js('tl.fromTo("#fac0 .fshop", {opacity:0}, {opacity:1, duration:0.25}, 0.05);')
    t_aud, t_pel = P("audiencia"), P("pelea")
    pop("#lider", t_aud, sound="pop")
    stamp("#st-can", t_pel, rot=-12)
    shake(t_pel + 0.3, 16)
    js(f'tl.to("#fac0", {{filter:"grayscale(0.7)", duration:0.4}}, {t_pel + 0.3:.3f});')


def scene_lqsa():
    fx, fy, fw, fh = F(0, 1)
    montepinar("mon", fx + 140, fy + 200, 680, 860)
    t_y, t_nac, t_ave = P("y"), P("nacio"), P("avecina")
    travel(t_y, F(0, 1), 0, 1630, dur=0.8)
    for f in range(4):
        js(f'tl.fromTo("#mon-fl{3 - f}", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.25, ease:"back.out(2)"}}, {t_nac + 0.1 * f:.3f});')
    sfx(t_nac, "pop2", 0.3)
    js(f'tl.fromTo("#mon-sg", {{opacity:0.25}}, {{opacity:1, duration:0.12, repeat:3, yoyo:true}}, {t_ave:.3f}); tl.set("#mon-sg", {{opacity:1}}, {t_ave + 0.5:.3f});')
    sfx(t_ave, "click", 0.4)
    floaty("#mon", t_ave + 0.6, G.DUR, 5, 2.6)


# ================================================================= 1 · EL FINAL
def scene_contrato():
    fx, fy, fw, fh = F(1, 1)
    header("h1", fx, fy, "1", "EL FINAL")
    cal, ch = roller("cal1", "0000", 80, "#fff")
    card("ctr", fx + 60, fy + 190, 840, 620, f'''
      <div style="position:absolute;left:40px;top:36px;font:900 72px {FONT};color:{INK}">CONTRATO</div>
      <div style="position:absolute;left:40px;top:136px;right:40px;height:16px;border-radius:8px;background:#e5e7eb"></div>
      <div style="position:absolute;left:40px;top:176px;right:140px;height:16px;border-radius:8px;background:#e5e7eb"></div>
      <div style="position:absolute;left:40px;top:216px;right:90px;height:16px;border-radius:8px;background:#e5e7eb"></div>
      <div class="sig" style="left:40px">Antena 3</div><div class="sig" style="left:440px">Miramón Mendi</div>
      <div id="ctr-st" class="stamp" style="position:absolute;left:150px;top:260px;color:{BAD};border-color:{BAD};font-size:70px;opacity:0">CADUCADO</div>''')
    add(f'<div id="corner" style="{css_box(fx + 760, fy + 670, 140, 140, 7)}background:#fff;clip-path:polygon(100% 0,100% 100%,0 100%);border-radius:0 0 40px 0"></div>')
    add(f'''<div id="cal" class="cnt" style="{css_box(fx + 260, fy + 860, 440, 150, 8)}background:{INK}">
      <span style="font:900 60px {FONT};color:#fff;margin-right:20px">JUN</span>{cal}</div>''')
    t_uno, t_fin, t_jun, t_06, t_cad, t_ren = P("uno"), P("final"), P("junio"), P("2006"), P("caduco"), P("renovo")
    travel(t_uno, F(1, 1), 1, 1630, dur=0.85)
    header_in("h1", t_uno, t_fin)
    pop("#ctr", t_jun - 0.2, sound="papel", vol=0.4)
    js(f'tl.set("#corner", {{opacity:0}}, 0); tl.set("#corner", {{opacity:1}}, {t_jun - 0.2:.3f});')
    pop("#cal", t_06 - 0.1, sound=None)
    roll_set("cal1", "0000", ch)
    roll_to("cal1", "2006", ch, t_06, dur=0.6)
    stamp("#ctr-st", t_cad, rot=-10)
    js(f'tl.to("#ctr", {{backgroundColor:"#fee2e2", duration:0.3}}, {t_cad + 0.3:.3f});')
    js(f'tl.to("#corner", {{y:420, x:60, rotation:160, opacity:0, duration:0.7, ease:"power2.in"}}, {t_ren:.3f});')
    sfx(t_ren, "papel", 0.45)


def scene_compra():
    fx, fy, fw, fh = F(1, 0)
    pct, ph = roller("pct", "00", 110, INK)
    card("pie", fx + 60, fy + 100, 840, 620, f'''
      <div style="position:absolute;left:40px;top:30px;font:900 62px {FONT};color:{INK}">Miramón Mendi</div>
      <svg style="position:absolute;left:40px;top:140px" width="420" height="420" viewBox="0 0 420 420">
        <circle cx="210" cy="210" r="150" fill="none" stroke="#e5e7eb" stroke-width="110"/>
        <circle id="pie-s" cx="210" cy="210" r="150" fill="none" stroke="#2563eb" stroke-width="110" transform="rotate(-90 210 210)"/></svg>
      <div style="position:absolute;left:500px;top:250px">{pct}<span style="font:900 110px {FONT};color:{INK}">%</span></div>
      <div style="position:absolute;left:500px;top:390px;font:800 50px {FONT};color:#2563eb">Telecinco</div>''')
    add(f'''<div id="nt1" class="notif" style="{css_box(fx + 60, fy + 780, 840, 130, 8)}">
      <div class="nicon" style="background:#2563eb">{icon("bell", 56, "#fff", 2.6)}</div><span>Telecinco compra el 15 %</span></div>''')
    circ = 2 * 3.14159 * 150
    t_jus, t_tel, t_com, t_15, t_pro = P("justo"), P("telecinco"), P("compro"), P("15%"), P("productora")
    travel(t_jus, F(1, 0), 1, 570, dur=0.8)
    pop("#pie", t_tel, sound="pop")
    js(f'tl.set("#pie-s", {{strokeDasharray:"0 {circ:.0f}"}}, 0);')
    js(f'tl.to("#pie-s", {{strokeDasharray:"{circ * 0.15:.0f} {circ:.0f}", duration:0.7, ease:"power3.out"}}, {t_15:.3f});')
    roll_set("pct", "00", ph)
    roll_to("pct", "15", ph, t_15, dur=0.7)
    js(f'tl.fromTo("#nt1", {{opacity:0, y:-150}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_pro:.3f});')
    sfx(t_pro, "pop2", 0.35)
    cam(E("productora") + 0.05, ROW(1), dur=0.45)


# ================================================================= 2 · EL SALTO
def scene_salto():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h2", fx, fy, "2", "EL SALTO")
    card("cad", fx, fy + 180, 450, 200, f'''
      <div style="position:absolute;left:30px;top:30px;font:900 60px {FONT};color:{INK}">CADENA</div>
      <div class="okb" style="background:{BAD}">{icon("x", 70, "#fff", 3.4)}</div>''')
    card("prod", fx + 510, fy + 180, 450, 200, f'''
      <div style="position:absolute;left:30px;top:30px;font:900 52px {FONT};color:{INK}">PRODUCTORA</div>
      <div class="okb" style="background:{GOOD_BG}">{icon("check", 70, "#fff", 3.4)}</div>''')
    actors = [("a1", "g1", fx + 200), ("a2", "g2", fx + 480), ("a3", "g3", fx + 760)]
    add(f'''<svg id="ties" data-layout-ignore style="{css_box(fx, fy + 380, 960, 300, 5)}overflow:visible" viewBox="0 0 960 300">
      {"".join(f'<path class="tie" d="M 735 0 Q {(x - fx + 735) / 2:.0f} 150 {x - fx:.0f} 290" stroke="#22c55e" stroke-width="6" fill="none" stroke-dasharray="14 10"/>' for _, _, x in actors)}</svg>''')
    for aid, kind, x in actors:
        add(character(aid, kind, x, fl, 1.1, z=6))
        add(f'<div id="{aid}-box" class="box" style="{css_box(x - 60, fl - 560, 120, 120, 7)}">{icon("package", 100, "#7c4a00", 2.4).replace("<svg", "<svg fill=\"#e2b06b\"")}</div>')
    t_dos, t_sal, t_act, t_con, t_pro, t_cad = P("dos"), P("salto"), P("actores"), P("contrato", 2), P("productora", 2), P("cadena")
    travel(t_dos, F(2, 0), 2, 570, dur=0.85)
    header_in("h2", t_dos, t_sal)
    for k, (aid, kind, x) in enumerate(actors):
        js(f'tl.fromTo("#{aid}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_act + k * 0.1:.3f});')
        life(aid, t_act, G.DUR, 10 + k)
    sfx(t_act, "pop2", 0.3)
    pop("#prod", t_pro, sound="pop")
    js('tl.set(".tie", {strokeDashoffset:400, opacity:0}, 0);')
    js(f'tl.to(".tie", {{opacity:1, strokeDashoffset:0, duration:0.6, stagger:0.1}}, {t_pro + 0.2:.3f});')
    pop("#cad", t_cad, sound="pop")
    t_rep, t_mud, t_tel = P("reparto"), P("mudo"), P("telecinco", 2)
    for k, (aid, kind, x) in enumerate(actors):
        js(f'tl.fromTo("#{aid}-box", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_rep + k * 0.1:.3f});')
        js(f'tl.to(Q("{aid}","armL"), {{rotation:-160, svgOrigin:PIV.armL, duration:0.3}}, {t_rep + k * 0.1:.3f}); tl.to(Q("{aid}","armR"), {{rotation:160, svgOrigin:PIV.armR, duration:0.3}}, {t_rep + k * 0.1:.3f});')
        js(f'tl.to("#{aid}, #{aid}-box", {{x:1150, duration:1.6, ease:"power1.in"}}, {t_mud + k * 0.12:.3f}); tl.to("#{aid}, #{aid}-box", {{opacity:0, duration:0.3}}, {t_mud + 1.4 + k * 0.12:.3f});')
        js(f'tl.to(Q("{aid}","legL"), {{rotation:25, svgOrigin:PIV.legL, duration:0.15, yoyo:true, repeat:9}}, {t_mud + k * 0.12:.3f}); tl.to(Q("{aid}","legR"), {{rotation:-25, svgOrigin:PIV.legR, duration:0.15, yoyo:true, repeat:9}}, {t_mud + k * 0.12:.3f});')
    sfx(t_mud, "whoosh-corto", 0.3)


def scene_estreno():
    fx, fy, fw, fh = F(2, 1)
    yr, yh = roller("yr7", "2006", 70, "#fff")
    add(f'''<div id="tv" style="{css_box(fx + 140, fy + 40, 680, 400, 5)}">
      <div class="screen"><div id="tv-t" style="font:900 96px {FONT};color:#fff;opacity:0">ESTRENO</div>
        <div id="tv-s" style="font:800 52px {FONT};color:#cfd8ff;opacity:0">La que se avecina</div></div><div class="knob k1"></div><div class="knob k2"></div></div>''')
    add(f'''<div id="cal7" class="cnt" style="{css_box(fx + 220, fy + 460, 520, 120, 8)}background:{INK}">
      <span style="font:900 56px {FONT};color:#fff;margin-right:18px">22 ABR</span>{yr}</div>''')
    add(f'<div class="colh" style="{css_box(fx + 20, fy + 620, 440, 80, 6)}background:{BAD}">ANHQV</div>')
    add(f'<div class="colh" style="{css_box(fx + 500, fy + 620, 440, 80, 6)}background:{GOOD_BG}">LQSA</div>')
    names = [("n1", "Fernando Tejero", "fernando"), ("n2", "José Luis Gil", "jose"), ("n3", "Eduardo Gómez", "eduardo")]
    for k, (nid, txt, w) in enumerate(names):
        add(f'<div id="{nid}" class="ncard" style="{css_box(fx + 20, fy + 720 + k * 110, 440, 96, 7)}">{txt}</div>')
    t_abr, t_07, t_est, t_cam = P("abril"), P("2007"), P("estreno"), P("cambiaron")
    travel(P("telecinco", 2) - 0.1, F(2, 1), 2, 1630, dur=0.8)
    js(f'tl.set("#tv", {{opacity:0}}, 0); tl.to("#tv", {{opacity:1, duration:0.3}}, {t_abr - 0.6:.3f});')
    pop("#cal7", t_abr, sound="pop2")
    roll_set("yr7", "2006", yh)
    js(f'tl.to("#yr7-d3", {{y:{-(10 + 7) * yh}, duration:0.4, ease:"back.out(2)"}}, {t_07:.3f});')
    js(f'tl.to("#tv .screen", {{backgroundColor:"#1d3fa8", duration:0.25}}, {t_est:.3f});')
    js(f'tl.fromTo("#tv-t", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_est:.3f}); tl.to("#tv-s", {{opacity:1, duration:0.3}}, {t_est + 0.4:.3f});')
    sfx(t_est, "golpe", 0.35)
    for k, (nid, txt, w) in enumerate(names):
        pop(f"#{nid}", P(w), sound="pop2", vol=0.25)
        js(f'tl.to("#{nid}", {{x:480, duration:0.45, ease:"power3.inOut"}}, {t_cam + k * 0.12:.3f}); tl.to("#{nid}", {{backgroundColor:"#dcfce7", duration:0.3}}, {t_cam + k * 0.12 + 0.3:.3f});')
    sfx(t_cam, "whoosh-corto", 0.3)
    cam(E("edificio") + 0.05, ROW(2), dur=0.45)


# ================================================================= 3 · EL JUICIO
def scene_juicio():
    fx, fy, fw, fh = F(3, 1)
    header("h3", fx, fy, "3", "EL JUICIO")
    eur, eh = roller("eur", "0.000.000", 76, INK)
    card("dem", fx, fy + 180, fw, 300, f'''
      <div style="position:absolute;left:36px;top:30px">{icon("file-x", 110, BAD, 2.2)}</div>
      <div style="position:absolute;left:170px;top:30px;font:900 70px {FONT};color:{INK}">DEMANDA</div>
      <div id="dem-pl" class="pill" style="position:absolute;left:170px;top:120px;background:{BAD};color:#fff;opacity:0">PLAGIO</div>
      <div id="dem-e" style="position:absolute;left:40px;top:200px;opacity:0">{eur}<span style="font:900 76px {FONT};color:{INK}"> €</span></div>''')
    add(f'<div id="scale" style="{css_box(fx + 80, fy + 560, 420, 420, 5)}">{icon("scale", 400, "#e5e7eb", 1.8)}</div>')
    add(f'<div id="gavel" style="{css_box(fx + 560, fy + 560, 340, 340, 6)}">{icon("gavel", 320, ACC, 2.0)}</div>')
    add(f'<div id="st-des" class="stamp" style="{css_box(fx + 70, fy + 560, None, None, 9)}color:#15803d;border-color:#15803d;font-size:70px;line-height:1.05;text-align:center">DEMANDA<br>DESESTIMADA</div>')
    t_tres, t_jui, t_den, t_pla, t_mil, t_12, t_raz = P("tres"), P("juicio"), P("denuncio"), P("plagio"), P("millones"), P("2012"), P("razon")
    travel(t_tres, F(3, 1), 3, 1630, dur=0.85)
    header_in("h3", t_tres, t_jui)
    slide_in("#dem", t_den, dy=-60, sound="papel", vol=0.4)
    pop("#dem-pl", t_pla, sound="pop")
    js(f'tl.to("#dem-e", {{opacity:1, duration:0.2}}, {t_mil - 0.3:.3f});')
    roll_set("eur", "0000000", eh)
    roll_to("eur", "3000000", eh, t_mil - 0.3, dur=0.8, stagger=0.04)
    js(f'tl.fromTo("#scale, #gavel", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_mil + 0.4:.3f});')
    # CLÍMAX: el mazo golpea
    js(f'tl.to("#gavel", {{rotation:-35, transformOrigin:"80% 80%", duration:0.25, ease:"power2.out"}}, {t_12 - 0.25:.3f}); tl.to("#gavel", {{rotation:10, duration:0.12, ease:"power4.in"}}, {t_12:.3f}); tl.to("#gavel", {{rotation:0, duration:0.2}}, {t_12 + 0.15:.3f});')
    shake(t_12 + 0.1, 24)
    sfx(t_12 + 0.08, "golpe-climax", 0.55)
    js(f'tl.to("#scale", {{rotation:-12, transformOrigin:"50% 20%", duration:0.6, ease:"elastic.out(1,0.5)"}}, {t_raz:.3f});')
    stamp("#st-des", t_raz + 0.1, rot=-8)
    sfx(t_raz + 0.4, "check", 0.45)


def scene_final():
    fx, fy, fw, fh = F(3, 0)
    sen = "«Una comedia de vecinos es una idea demasiado general»"
    add(f'''<div id="sen" class="bubble big" style="{css_box(fx + 20, fy + 40, 920, None, 8)}">
      <div style="font:900 46px {FONT};color:#666;margin-bottom:10px">LA SENTENCIA</div>
      <div id="sen-t" style="font:900 58px {FONT};color:{INK};line-height:1.12">{chars(sen, "sc")}</div></div>''')
    mini = []
    for i in range(5):
        mini.append(f'<div class="mb" style="left:{20 + i * 190}px;height:{120 + (i * 37) % 70}px;background:{["#e8b84a", "#dfe6ee", "#f97316", "#a78bfa", "#60a5fa"][i]}"></div>')
    add(f'<div id="minis" data-layout-ignore style="{css_box(fx + 20, fy + 360, 920, 200, 5)}">{"".join(mini)}</div>')
    card("poll", fx + 60, fy + 600, 840, 440, f'''
      <div id="poll-a" style="position:absolute;inset:0">
        <div style="position:absolute;left:40px;top:40px">{icon("receipt", 120, INK, 2.2)}</div>
        <div style="position:absolute;left:190px;top:40px;font:900 80px {FONT};color:{INK}">COSTAS</div>
        <div class="pill" style="position:absolute;left:190px;top:150px;background:{BAD};color:#fff">PAGA: ANTENA 3</div></div>
      <div id="poll-b" style="position:absolute;inset:0;opacity:0">
        <div style="position:absolute;left:40px;top:34px;font:900 64px {FONT};color:{INK}">¿De qué edificio eres?</div>
        <div id="ob1" class="opt" style="top:140px;border-color:{ACC}">DESENGAÑO 21</div>
        <div id="ob2" class="opt" style="top:280px;border-color:{GOOD}">MONTEPINAR</div></div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 700, fy + 900, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_seg, t_com, t_due, t_cos, t_tu, t_des, t_mon, t_cmt = (P("segun"), P("comedia"), P("dueno"), P("costas"), P("tu"),
                                                             P("desengano"), P("montepinar"), P("comenta"))
    travel(t_seg, F(3, 0), 3, 570, dur=0.8)
    pop("#sen", t_seg + 0.3, sound="pop2")
    type_on("#sen-t .sc", len(sen), t_com, t_due + 0.2)
    js(f'tl.fromTo(".mb", {{scaleY:0, transformOrigin:"50% 100%"}}, {{scaleY:1, duration:0.4, stagger:0.08, ease:"back.out(2)"}}, {P("vecinos"):.3f});')
    pop("#poll", t_cos - 0.1, sound="pop")
    flip("#poll", t_tu, ["#poll-a"], ["#poll-b"])
    pop("#ob1", t_des, sound="pop2")
    pop("#ob2", t_mon, sound="pop2")
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_mon + 0.2:.3f});')
    js(f'tl.to("#cur", {{x:-100, y:20, duration:0.4}}, {t_cmt - 0.4:.3f}); tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_cmt:.3f});')
    js(f'tl.to("#ob2", {{backgroundColor:"#dcfce7", scale:1.04, duration:0.2}}, {t_cmt + 0.05:.3f});')
    sfx(t_cmt, "click", 0.5)
    cam(t_cmt + 0.45, (0, 100, 2200, 5200), dur=0.8, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:78px; top:26px; }}
.fbody {{ position:absolute; inset:0; background:#e8b84a; border-radius:10px; box-shadow:0 30px 70px rgba(0,0,0,0.45); }}
.fcorn {{ position:absolute; left:-18px; right:-18px; top:0; height:40px; background:#c98f2c; border-radius:8px; }}
.ffloor {{ position:absolute; left:0; right:0; border-bottom:8px solid #c98f2c; }}
.fwin {{ position:absolute; background:#33475b; border:6px solid #fff3d6; border-radius:6px 6px 0 0; }}
.frail {{ position:absolute; left:-12px; right:-12px; bottom:-18px; height:22px; border:5px solid #1f2937; border-top-width:6px; border-radius:3px; }}
.fshop {{ position:absolute; height:150px; }}
.sgt {{ position:absolute; left:0; right:0; top:0; }}
.fsign {{ position:relative; height:56px; border-radius:10px; background:#1f2937; color:#fff; font:900 30px {FONT}; text-align:center; line-height:56px; white-space:nowrap; overflow:hidden; }}
.fdoor {{ margin:12px auto 0; width:70%; height:80px; background:#5b3a1e; border-radius:8px 8px 0 0; }}
.mont {{ background:#dfe6ee; border-radius:14px; box-shadow:0 30px 70px rgba(0,0,0,0.45); }}
.mtop {{ position:absolute; left:-10px; right:-10px; top:-10px; height:90px; background:#0f766e; border-radius:12px; text-align:center; line-height:90px; font:900 46px {FONT}; color:#fff; white-space:nowrap; }}
.mfloor {{ position:absolute; left:0; right:0; border-bottom:10px solid #94a3b8; }}
.mwin {{ position:absolute; top:22px; bottom:32px; background:linear-gradient(135deg,#5eead4,#0e7490); border-radius:6px; }}
.mglass {{ position:absolute; left:16px; right:16px; bottom:0; height:30px; background:rgba(125,211,252,0.5); border-top:5px solid #e2e8f0; }}
.mdoor {{ position:absolute; left:50%; bottom:0; width:140px; height:110px; margin-left:-70px; background:#334155; border-radius:8px 8px 0 0; }}
.panel {{ border-radius:40px; background:#fff; box-shadow:0 24px 60px rgba(0,0,0,0.45); }}
.ptit {{ position:absolute; left:40px; top:30px; display:flex; align-items:center; gap:20px; font:900 66px {FONT}; color:{INK}; }}
.sig {{ position:absolute; top:520px; width:370px; white-space:nowrap; font-size:42px !important; border-top:5px solid {INK}; padding-top:10px; font:900 48px {FONT}; color:{INK}; font-style:italic; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; }}
.notif {{ border-radius:30px; background:rgba(255,255,255,0.96); display:flex; align-items:center; gap:24px; padding-left:24px;
  font:800 50px {FONT}; color:{INK}; box-shadow:0 14px 30px rgba(0,0,0,0.35); white-space:nowrap; }}
.nicon {{ width:80px; height:80px; border-radius:22px; display:flex; align-items:center; justify-content:center; flex:none; }}
.okb {{ position:absolute; right:30px; bottom:30px; width:100px; height:100px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
.box {{ opacity:0; }}
#tv {{ background:#2a2e3a; border-radius:56px; box-shadow:0 30px 80px rgba(0,0,0,0.5); }}
#tv .screen {{ position:absolute; left:36px; top:36px; right:150px; bottom:36px; border-radius:36px; background:#05060a;
  display:flex; flex-direction:column; align-items:center; justify-content:center; }}
#tv .knob {{ position:absolute; right:42px; width:70px; height:70px; border-radius:50%; background:#8b93a7; }}
#tv .k1 {{ top:100px; }} #tv .k2 {{ top:220px; }}
.colh {{ border-radius:22px; color:#fff; font:900 56px {FONT}; text-align:center; line-height:80px; }}
.ncard {{ border-radius:24px; background:#fff; font:900 50px {FONT}; color:{INK}; text-align:center; line-height:96px; white-space:nowrap; box-shadow:0 10px 24px rgba(0,0,0,0.35); }}
.mb {{ position:absolute; bottom:0; width:160px; border-radius:10px 10px 0 0; }}
.opt {{ position:absolute; left:40px; right:40px; height:110px; border-radius:30px; border:8px solid; background:#fff; font:900 62px {FONT}; color:{INK}; text-align:center; line-height:94px; }}
.sc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_lqsa()
    scene_contrato()
    scene_compra()
    scene_salto()
    scene_estreno()
    scene_juicio()
    scene_final()
