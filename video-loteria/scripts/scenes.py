"""Escenas del vídeo «¿Por qué la Lotería de Navidad la cantan niños?». Un solo mundo: un camino en zigzag
(22 de diciembre -> 1771 -> 1812 -> el colegio -> la teoría -> el ritual -> los bombos y el Gordo -> 250 años y comentarios)."""
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
GOLD = "#f5c542"


def lball(bid, x, y, size, text, z=7, gold=False):
    cls = "lball gold" if gold else "lball"
    add(f'<div id="{bid}" class="{cls}" style="{css_box(x, y, size, size, z)}"><span style="font-size:{size * min(0.34, 1.25 / max(1, len(text))):.0f}px">{text}</span></div>')


def decimo(did, x, y, num, z=5, rot=0):
    add(f'''<div id="{did}" class="dec" style="{css_box(x, y, 300, 170, z)}transform:rotate({rot}deg)">
      <div class="dech">LOTERÍA NACIONAL</div><div class="decn">{num}</div><div class="decf">20 €</div></div>''')


def drum(did, x, y, size, z=5, color=GOLD):
    spokes = "".join(f'<i class="spk" style="transform:rotate({k * 30}deg)"></i>' for k in range(6))
    add(f'''<div id="{did}" style="{css_box(x, y, size, size + size * 0.25, z)}">
      <div class="dstand" style="left:{size * 0.3:.0f}px;top:{size * 0.8:.0f}px;width:{size * 0.4:.0f}px;height:{size * 0.45:.0f}px"></div>
      <div id="{did}-cage" class="cage" style="width:{size}px;height:{size}px;border-color:{color}">{spokes}
        {"".join(f'<b class="mini" style="left:{30 + (k * 53) % (size - 90)}px;top:{size * 0.45 + (k * 37) % (size * 0.4):.0f}px"></b>' for k in range(int(size / 30)))}</div></div>''')


def confetti(prefix, x, y, n, t, w=900, z=12):
    cols = ["#ef4444", "#facc15", "#22c55e", "#3b82f6", "#ec4899", "#f97316"]
    for i in range(n):
        cx = x + (i * 97) % w
        add(f'<div id="{prefix}{i}" class="conf" data-layout-ignore style="{css_box(cx, y, 20, 34, z)}background:{cols[i % 6]};opacity:0"></div>')
        js(f'tl.fromTo("#{prefix}{i}", {{opacity:1, y:0, rotation:0}}, {{opacity:1, y:{700 + (i * 53) % 300}, x:{(i % 5 - 2) * 40}, rotation:{360 + i * 40}, duration:{1.6 + (i % 4) * 0.3:.1f}, ease:"power1.in", immediateRender:false}}, {t + (i % 7) * 0.05:.3f});')
        js(f'tl.to("#{prefix}{i}", {{opacity:0, duration:0.3}}, {t + 2.4:.3f});')


def notes(prefix, x, y, n, t, color=ACC, rise=200, spread=240, z=9):
    for i in range(n):
        nx = x + (i - (n - 1) / 2) * spread / max(1, n - 1)
        add(f'<div id="{prefix}{i}" data-layout-ignore style="{css_box(nx - 35, y, 70, 70, z)}opacity:0">{icon("music", 70, color, 2.6)}</div>')
        tt = t + i * 0.12
        js(f'tl.fromTo("#{prefix}{i}", {{opacity:0, y:0, scale:0.4}}, {{opacity:1, y:{-rise * 0.5:.0f}, scale:1, duration:0.4, ease:"back.out(2)", immediateRender:false}}, {tt:.3f});')
        js(f'tl.to("#{prefix}{i}", {{y:{-rise}, opacity:0, duration:0.9, ease:"power1.in"}}, {tt + 0.45:.3f});')


# ================================================================= MUNDO
MILES = [("Madrid · 1771", 0, 1630), ("Madrid", 1, 570), ("Ensayos", 2, 1630), ("22 de diciembre", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#dc2626"/><stop offset="0.5" stop-color="{GOLD}"/><stop offset="1" stop-color="#16a34a"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 240, ROAD[r] + 34, 480, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= GANCHO: 22 DE DICIEMBRE
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    for k, (x, y, r, n) in enumerate([(40, 60, -12, "48302"), (640, 40, 10, "07215"), (20, 440, 8, "91877"), (660, 420, -9, "33410")]):
        decimo(f"dc{k}", fx + x, fy + y, n, z=3, rot=r)
    add(f'''<div id="cal" class="calc" style="{css_box(fx + 330, fy + 180, 300, 300, 8)}">
      <div class="calh">DICIEMBRE</div><div class="caln">22</div></div>''')
    lball("b0", fx + 400, fy + 40, 160, "22", z=9)
    add(character("k1", "g1", fx + 250, fl, 0.85, z=6))
    add(character("k2", "g2", fx + 700, fl, 0.85, z=6))
    add(f'<div id="pq" class="pill" style="{css_box(fx + 170, fy + 540, None, None, 10)}background:{BAD};color:#fff;font-size:70px;opacity:0">¿POR QUÉ NIÑOS?</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: cae la bola, rebota y aparece el 22 de diciembre
    js(f'tl.fromTo("#b0", {{y:0, rotation:-180}}, {{y:{fl - 140 - (fy + 40):.0f}, rotation:0, duration:0.55, ease:"bounce.out"}}, 0);')
    js('tl.fromTo("[id^=dc]", {opacity:1, scale:1.35}, {opacity:1, scale:1, duration:0.4, stagger:0.05, ease:"back.out(2)"}, 0);')
    js('tl.fromTo("#cal", {opacity:1, scale:1.6}, {opacity:1, scale:1, duration:0.45, ease:"back.out(2)"}, 0);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.45, "madera", 0.5)
    shake(0.5, 12)
    life("k1", 0, G.DUR, 1)
    life("k2", 0, G.DUR, 2)
    t_esp, t_par, t_nin, t_can, t_num, t_por, t_nin2 = P("espana"), P("para"), P("ninos"), P("cantar"), P("numeros"), P("por"), P("ninos", 2)
    js(f'tl.to("[id^=dc]", {{y:"+=20", duration:0.15, yoyo:true, repeat:1}}, {t_par:.3f});')
    js(f'tl.fromTo("#k1, #k2", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35, stagger:0.1}}, {t_nin - 0.1:.3f});')
    js(f'tl.to(Q("k1","mouth"), {{scaleY:2, svgOrigin:"120 136", duration:0.15, yoyo:true, repeat:5}}, {t_can:.3f}); tl.to(Q("k2","mouth"), {{scaleY:2, svgOrigin:"120 136", duration:0.15, yoyo:true, repeat:5}}, {t_can + 0.1:.3f});')
    notes("n0-", fx + 480, fy + 660, 4, t_can, spread=420)
    js(f'tl.to("#b0", {{scale:1.15, duration:0.15, yoyo:true, repeat:1}}, {t_num:.3f});')
    stamp("#pq", t_nin2 - 0.15)
    sfx(t_nin2, "golpe", 0.45)


# ================================================================= 1 · EL ORIGEN (1771)
def scene_origen():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "1", "EL ORIGEN", color=GOLD)
    yr, yh = roller("y71", "0000", 80, "#fff")
    add(f'<div id="ycb" class="cnt" style="{css_box(fx + 40, fy + 190, 340, 140, 8)}background:{INK};opacity:0">{yr}</div>')
    add(f'<div id="crown" class="pill" style="{css_box(fx + 420, fy + 210, None, None, 8)}background:{GOLD};color:{INK};font-size:54px;opacity:0">{icon("crown", 52, INK, 2.6)} CARLOS III</div>')
    add(f'<div id="sch" class="pill" style="{css_box(fx + 40, fy + 380, None, None, 8)}background:#fff;color:{INK};font-size:52px;opacity:0">{icon("school", 50, INK, 2.6)} ALUMNO DE SAN ILDEFONSO</div>')
    add(character("k3", "g1", fx + 260, fl, 1.0, z=6))
    lball("b1", fx + 560, fy + 640, 200, "1.º", z=7)
    add(f'<div id="prem" class="pill" style="{css_box(fx + 520, fy + 870, None, None, 9)}background:{GOOD_BG};color:#fff;font-size:56px;opacity:0">¡PREMIADO!</div>')
    t_uno, t_ori, t_17, t_car, t_alu, t_can, t_pri, t_pre = P("uno"), P("origen"), P("1771"), P("carlos"), P("alumno"), P("canto"), P("primera"), P("premiado")
    travel(t_uno - 0.25, F(0, 1), 0, 1630, dur=0.6)
    header_in("h1", t_uno, t_ori)
    pop("#ycb", t_17 - 0.3, sound=None)
    roll_set("y71", "0000", yh)
    roll_to("y71", "1771", yh, t_17 - 0.2, dur=0.6)
    pop("#crown", t_car, sound="pop2")
    pop("#sch", t_alu, sound="pop2")
    life("k3", 0, G.DUR, 3)
    js(f'tl.fromTo("#k3", {{opacity:0, x:-100}}, {{opacity:1, x:0, duration:0.4}}, {t_alu:.3f});')
    js(f'tl.fromTo("#b1", {{opacity:0, scale:0.3, rotation:-180}}, {{opacity:1, scale:1, rotation:0, duration:0.45, ease:"back.out(2)"}}, {t_can - 0.1:.3f});')
    js(f'point("k3", "R", {t_can:.3f}, {t_pre + 0.6:.3f}, -100);')
    js(f'tl.to(Q("k3","mouth"), {{scaleY:2, svgOrigin:"120 136", duration:0.15, yoyo:true, repeat:5}}, {t_can:.3f});')
    notes("n1-", fx + 260, fy + 560, 3, t_can, spread=200)
    stamp("#prem", t_pre)
    sfx(t_pre, "check", 0.4)


# ================================================================= 1812: CÁDIZ
def scene_cadiz():
    fx, fy, fw, fh = F(1, 1)
    add(f'<div id="tline" class="tline" style="{css_box(fx + 80, fy + 300, 800, 14, 4)}"></div>')
    for k, (yr, x) in enumerate([("1771", 80), ("1812", 880)]):
        add(f'<div id="td{k}" class="tdot" style="{css_box(fx + x - 30, fy + 277, 60, 60, 5)}opacity:0"></div>')
        add(f'<div id="tl{k}" class="tlab" style="{css_box(fx + x - 130, fy + 160, 260, 90, 5)}opacity:0">{yr}</div>')
    card("lnav", fx + 120, fy + 420, 720, 220, f'''
      <div style="position:absolute;left:36px;top:30px">{icon("gift", 120, "#dc2626", 2.4)}</div>
      <div style="position:absolute;left:190px;top:40px;font:900 58px {FONT};color:{INK};line-height:1.15">LOTERÍA<br>DE NAVIDAD</div>''')
    add(f'''<div id="map" class="mapb" style="{css_box(fx + 180, fy + 700, 600, 340, 4)}opacity:0">
      <div class="coast"></div><div id="pin" class="pinw">{icon("map-pin", 120, "#dc2626", 2.6).replace("<svg", "<svg fill=\"#fecaca\"")}</div>
      <div class="cz">CÁDIZ</div></div>''')
    t_ant, t_inc, t_nac, t_lot, t_nav, t_cad, t_12 = P("antes"), P("incluso"), P("naciera"), P("loteria"), P("navidad"), P("cadiz"), P("1812")
    travel(t_ant - 0.3, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_ant + 0.2)
    js(f'tl.fromTo("#tline", {{scaleX:0}}, {{scaleX:1, transformOrigin:"0% 50%", duration:0.8, ease:"power2.inOut"}}, {t_ant:.3f});')
    js(f'tl.fromTo("#td0, #tl0", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_ant:.3f});')
    sfx(t_ant, "whoosh-corto", 0.3)
    slide_in("#lnav", t_lot - 0.1, dy=60, sound="pop")
    js(f'tl.to("#lnav", {{scale:1.05, duration:0.15, yoyo:true, repeat:1}}, {t_nav:.3f});')
    js(f'tl.fromTo("#map", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_cad - 0.3:.3f});')
    js(f'tl.fromTo("#pin", {{y:-120, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"bounce.out"}}, {t_cad:.3f});')
    sfx(t_cad, "pop", 0.35)
    js(f'tl.fromTo("#td1, #tl1", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_12:.3f});')
    sfx(t_12, "check", 0.3)


# ================================================================= 2 · EL COLEGIO
def scene_colegio():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    header("h2", fx, fy, "2", "EL COLEGIO", color="#dc2626", txt="#fff")
    cols = "".join(f'<i class="col" style="left:{60 + k * 130}px"></i>' for k in range(5))
    add(f'''<div id="school" class="school" style="{css_box(fx + 120, fy + 300, 720, 760, 3)}">
      <div class="roof"></div><div class="ssign">SAN ILDEFONSO</div>{cols}<div id="door" class="sdoor"></div></div>''')
    add(f'<div id="mad" class="pill" style="{css_box(fx + 600, fy + 190, None, None, 8)}background:#fff;color:{INK};font-size:52px;opacity:0">{icon("map-pin", 50, "#dc2626", 2.6)} MADRID</div>')
    add(f'<div id="sig" class="pill" style="{css_box(fx + 40, fy + 190, None, None, 8)}background:{GOLD};color:{INK};font-size:52px;opacity:0">{icon("hourglass", 50, INK, 2.6)} SIGLOS</div>')
    for k in range(3):
        add(character(f"o{k}", ["g3", "g2", "g1"][k], fx + 100 + k * 110, fl, 0.6, z=6))
    t_dos, t_col, t_san, t_ant, t_mad, t_sig, t_aco, t_hue = (P("dos"), P("colegio"), P("san", 2), P("antiguos"), P("madrid"), P("siglos"), P("acogio"),
                                                            P("huerfanos"))
    travel(t_dos - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h2", t_dos, t_col)
    js(f'tl.fromTo("#school", {{opacity:0, y:80}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {t_san - 0.1:.3f});')
    sfx(t_san, "puerta", 0.3)
    js(f'tl.to("#school .ssign", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_ant:.3f});')
    pop("#mad", t_mad, sound="pop2")
    pop("#sig", t_sig, sound="pop2")
    js(f'tl.to("#door", {{scaleX:0.15, transformOrigin:"0% 50%", duration:0.4}}, {t_aco:.3f});')
    for k in range(3):
        life(f"o{k}", 0, G.DUR, 10 + k)
        js(f'tl.fromTo("#o{k}", {{opacity:0, x:-120}}, {{opacity:1, x:{180 - k * 40}, duration:0.9, ease:"power1.out"}}, {t_aco + k * 0.15:.3f}); walk("o{k}", {t_aco + k * 0.15:.3f}, {t_hue + 0.6:.3f}, 0.12);')


# ================================================================= LA TEORÍA
def scene_teoria():
    fx, fy, fw, fh = F(2, 0)
    add(f'<div id="qm" class="qmark" style="{css_box(fx + 330, fy + 40, 300, 300, 8)}opacity:0">?</div>')
    add(f'<div id="nad" class="pill" style="{css_box(fx + 180, fy + 360, None, None, 8)}background:#334155;color:#fff;font-size:52px;opacity:0">NADIE LO SABE SEGURO</div>')
    add(f'<div id="teo" class="pill" style="{css_box(fx + 300, fy + 470, None, None, 8)}background:{GOLD};color:{INK};font-size:54px;opacity:0">{icon("lightbulb", 52, INK, 2.6)} TEORÍA</div>')
    add(f'<div id="pig" style="{css_box(fx + 280, fy + 640, 400, 400, 6)}opacity:0">{icon("piggy-bank", 380, "#9d174d", 2.2).replace("<svg", "<svg fill=\"#f9a8d4\"")}</div>')
    add(f'<div id="pigl" class="pill" style="{css_box(fx + 330, fy + 980, None, None, 8)}background:#fff;color:{INK};font-size:44px;opacity:0">COLEGIO</div>')
    for k in range(5):
        add(f'<div id="coin{k}" class="coin" data-layout-ignore style="{css_box(fx + 390 + (k % 3) * 60, fy + 520, 90, 90, 9)}opacity:0">€</div>')
    add(f'<div id="alu" class="pill" style="{css_box(fx + 660, fy + 760, None, None, 8)}background:{GOOD_BG};color:#fff;font-size:46px;opacity:0">{icon("users", 44, "#fff", 2.6)} ALUMNOS</div>')
    t_nad, t_seg, t_eli, t_teo, t_col, t_gan, t_din, t_alu = (P("nadie"), P("seguro"), P("eligieron"), P("teoria"), P("colegio", 2), P("ganaba"),
                                                            P("dinero"), P("alumnos"))
    travel(t_nad - 0.3, F(2, 0), 2, 570, dur=0.7)
    hide_mile(1, t_nad + 0.2)
    stamp("#qm", t_nad)
    sfx(t_nad, "golpe", 0.35)
    pop("#nad", t_seg, sound=None)
    js(f'tl.to("#qm", {{rotation:15, duration:0.2, yoyo:true, repeat:3}}, {t_eli:.3f});')
    pop("#teo", t_teo, sound="pop")
    js(f'tl.fromTo("#pig", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_col:.3f});')
    pop("#pigl", t_col + 0.2, sound=None)
    for k in range(5):
        js(f'tl.fromTo("#coin{k}", {{opacity:0, y:-120}}, {{opacity:1, y:160, duration:0.4, ease:"power2.in", immediateRender:false}}, {t_gan + k * 0.18:.3f}); tl.to("#coin{k}", {{opacity:0, duration:0.1}}, {t_gan + k * 0.18 + 0.4:.3f});')
        sfx(t_gan + k * 0.18 + 0.38, "click", 0.2)
    js(f'tl.to("#pig", {{scale:1.08, duration:0.15, yoyo:true, repeat:3}}, {t_din:.3f});')
    pop("#alu", t_alu, sound="check")


# ================================================================= 3 · EL RITUAL
def scene_ritual():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h3", fx, fy, "3", "EL RITUAL", color=GOOD_BG, txt="#fff")
    yr, yh = roller("y84", "0000", 70, "#fff")
    add(f'<div id="ycb2" class="cnt" style="{css_box(fx + 40, fy + 180, 320, 120, 8)}background:{INK};opacity:0">{yr}</div>')
    add(f'<div id="chi" class="pill" style="{css_box(fx + 400, fy + 200, None, None, 8)}background:#1d4ed8;color:#fff;font-size:50px;opacity:0">SOLO CHICOS</div>')
    add(f'<div id="ambos" class="pill" style="{css_box(fx + 400, fy + 200, None, None, 9)}background:#be185d;color:#fff;font-size:50px;opacity:0">NIÑOS Y NIÑAS</div>')
    add(f'<div id="lect" class="lect" style="{css_box(fx + 140, fl - 300, 420, 300, 5)}"></div>')
    add(character("boy", "g1", fx + 240, fl - 60, 0.95, z=4))
    add(character("girl", "g2", fx + 460, fl - 60, 0.95, z=4))
    add(f'''<div id="cal2" class="calc wide" style="{css_box(fx + 600, fy + 420, 320, 330, 8)}opacity:0">
      <div class="calh">OCT → DIC</div>
      {"".join(f'<div class="ckr" style="top:{110 + i * 70}px"><span id="cc{i}" class="cck">{icon("check", 34, "#fff", 3.6)}</span><span class="ckl"></span></div>' for i in range(3))}</div>''')
    add(f'<div id="nf" class="pill" style="{css_box(fx + 600, fy + 790, None, None, 8)}background:{BAD};color:#fff;font-size:44px;opacity:0">CERO FALLOS</div>')
    t_tres, t_rit, t_has, t_84, t_chi, t_hoy, t_nin, t_hue, t_ens, t_oct, t_fal = (P("tres"), P("ritual"), P("hasta"), P("1984"), P("chicos"), P("hoy"),
                                                                                 P("ninas"), P("huerfanos", 2), P("ensayan"), P("octubre"), P("fallar"))
    travel(t_tres - 0.3, F(2, 1), 2, 1630, dur=0.7)
    header_in("h3", t_tres, t_rit)
    pop("#ycb2", t_has, sound=None)
    roll_set("y84", "0000", yh)
    roll_to("y84", "1984", yh, t_84 - 0.2, dur=0.6)
    life("boy", 0, G.DUR, 4)
    life("girl", 0, G.DUR, 5)
    js(f'tl.fromTo("#lect, #boy", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_84:.3f});')
    pop("#chi", t_chi, sound="pop2")
    js(f'tl.to("#chi", {{opacity:0, duration:0.2}}, {t_nin - 0.3:.3f});')
    pop("#ambos", t_nin - 0.2, sound="pop")
    js(f'tl.fromTo("#girl", {{opacity:0, x:200}}, {{opacity:1, x:0, duration:0.5, ease:"back.out(1.6)"}}, {t_hoy:.3f}); walk("girl", {t_hoy:.3f}, {t_hoy + 0.5:.3f}, 0.12);')
    js(f'tl.to(Q("boy","mouth"), {{scaleY:2, svgOrigin:"120 136", duration:0.15, yoyo:true, repeat:5}}, {t_ens:.3f}); tl.to(Q("girl","mouth"), {{scaleY:2, svgOrigin:"120 136", duration:0.15, yoyo:true, repeat:5}}, {t_ens + 0.1:.3f});')
    js(f'tl.fromTo("#cal2", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_ens:.3f});')
    for i in range(3):
        js(f'tl.fromTo("#cc{i}", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.2, ease:"back.out(3)"}}, {t_oct + i * 0.2:.3f});')
    sfx(t_oct, "check", 0.3)
    notes("n3-", fx + 350, fl - 520, 4, t_ens, spread=300)
    stamp("#nf", t_fal)
    sfx(t_fal, "golpe", 0.3)


# ================================================================= LOS BOMBOS Y EL GORDO
def scene_bombos():
    fx, fy, fw, fh = F(3, 1)
    drum("dbig", fx + 40, fy + 120, 480, z=4)
    drum("dsm", fx + 620, fy + 300, 280, z=4, color="#e2e8f0")
    nb, nh = roller("cnt100", "000.000", 60, "#fff")
    add(f'<div id="c100" class="cnt" style="{css_box(fx + 60, fy + 20, 440, 100, 8)}background:{INK};opacity:0">{icon("circle-dot", 50, GOLD, 2.6)}{nb}</div>')
    lball("bn", fx + 220, fy + 560, 130, "48302", z=8)
    lball("bp", fx + 700, fy + 640, 120, "PREMIO", z=8)
    lball("bg", fx + 330, fy + 300, 300, "GORDO", z=11, gold=True)
    pr, ph = roller("mil4", "0.000.000", 96, INK)
    add(f'<div id="gbox" class="cnt" style="{css_box(fx + 60, fy + 680, 840, 200, 12)}background:{GOLD};border-color:#fff;opacity:0">{pr}<span class="eur">€</span></div>')
    t_uno3, t_sac, t_bol, t_cie, t_mil, t_otr, t_pre = P("uno", 3), P("saca"), P("bola"), P("cien"), P("mil"), P("otro"), P("premio")
    travel(t_uno3 - 0.3, F(3, 1), 3, 1630, dur=0.7)
    hide_mile(2, t_uno3 + 0.2)
    js(f'tl.fromTo("#dbig, #dsm", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_uno3 - 0.2:.3f});')
    js(f'tl.to("#dbig-cage", {{rotation:720, duration:{P("gordo") - t_uno3 + 3:.2f}, ease:"none"}}, {t_uno3:.3f});')
    js(f'tl.to("#dsm-cage", {{rotation:-720, duration:{P("gordo") - t_uno3 + 3:.2f}, ease:"none"}}, {t_uno3:.3f});')
    sfx(t_uno3, "tic-rodillo", 0.3)
    js(f'tl.fromTo("#bn", {{opacity:0, y:-260, scale:0.3}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"bounce.out"}}, {t_bol - 0.1:.3f});')
    sfx(t_bol, "madera", 0.4)
    pop("#c100", t_cie - 0.2, sound=None)
    roll_set("cnt100", "000.000", nh)
    roll_to("cnt100", "100.000", nh, t_cie - 0.1, dur=0.6)
    js(f'tl.fromTo("#bp", {{opacity:0, y:-200, scale:0.3}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"bounce.out"}}, {t_pre - 0.2:.3f});')
    sfx(t_pre, "madera", 0.4)
    t_gor, t_fra, t_esp, t_cua, t_mill, t_eur = P("gordo"), P("frase"), P("esperamos"), P("cuatro"), P("millones"), P("euros")
    # CLÍMAX
    js(f'tl.to("#bn, #bp", {{opacity:0.25, duration:0.3}}, {t_gor - 0.1:.3f});')
    js(f'tl.fromTo("#bg", {{opacity:0, scale:0.2, rotation:-200}}, {{opacity:1, scale:1, rotation:0, duration:0.6, ease:"back.out(1.8)"}}, {t_gor - 0.15:.3f});')
    sfx(t_gor, "golpe-climax", 0.55)
    shake(t_gor + 0.1, 22)
    js(f'tl.to("#bg", {{scale:1.08, duration:0.2, yoyo:true, repeat:5}}, {t_fra:.3f});')
    js(f'tl.fromTo("#gbox", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_cua - 0.3:.3f});')
    roll_set("mil4", "0.000.000", ph)
    roll_to("mil4", "4.000.000", ph, t_cua - 0.1, dur=0.7, from_text="0.000.000")
    confetti("cf", fx + 20, fy - 40, 26, t_mill - 0.1)
    sfx(t_mill, "check", 0.45)
    js(f'tl.to("#gbox", {{scale:1.06, duration:0.15, yoyo:true, repeat:3}}, {t_eur:.3f});')


# ================================================================= 250 AÑOS + COMENTARIOS
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    lights = "".join(f'<i id="lt{k}" class="lt" style="left:{20 + k * 72}px;top:{30 + (k % 2) * 18}px;background:{["#ef4444", "#facc15", "#22c55e", "#3b82f6"][k % 4]}"></i>' for k in range(13))
    add(f'<div id="garl" class="garl" style="{css_box(fx + 0, fy + 500, 960, 100, 5)}"><div class="wire"></div>{lights}</div>')
    yr, yh = roller("y250", "000", 120, INK)
    add(f'<div id="y250b" class="cnt" style="{css_box(fx + 180, fy + 640, 600, 200, 7)}background:#fff;border-color:{GOLD};opacity:0"><span class="mas">+</span>{yr}<span class="mas">AÑOS</span></div>')
    add(f'<div id="voz" class="pill" style="{css_box(fx + 190, fy + 880, None, None, 8)}background:#dc2626;color:#fff;font-size:56px;opacity:0">{icon("mic", 52, "#fff", 2.6)} LA VOZ DE LA NAVIDAD</div>')
    cta = "Una vez me tocó…"
    card("cbox", fx + 40, fy + 20, 880, 440, f'''
      <div style="position:absolute;left:40px;top:34px;display:flex;align-items:center;gap:22px">{icon("message-circle", 84, INK, 2.4)}
        <span style="font:900 68px {FONT};color:{INK}">Comentarios</span></div>
      <div style="position:absolute;left:40px;top:150px;font:900 50px {FONT};color:#555">¿Te ha tocado alguna vez?</div>
      <div id="ctt" style="position:absolute;left:40px;top:240px;font:800 66px {FONT};color:{INK};white-space:nowrap">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 370, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_mas, t_250, t_des, t_voz, t_nav = P("mas", 3), P("250"), P("despues"), P("voz"), P("navidad", 2)
    travel(t_mas - 0.3, F(3, 0), 3, 570, dur=0.7)
    js(f'tl.fromTo("#garl", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_mas:.3f});')
    js(f'tl.fromTo("[id^=lt]", {{opacity:0.2, scale:0.6}}, {{opacity:1, scale:1, duration:0.15, stagger:0.06}}, {t_mas:.3f});')
    js(f'tl.to("[id^=lt]", {{opacity:0.4, duration:0.3, yoyo:true, repeat:9, stagger:{{each:0.05, from:"random"}}}}, {t_voz:.3f});')
    pop("#y250b", t_250 - 0.3, sound=None)
    roll_set("y250", "000", yh)
    roll_to("y250", "250", yh, t_250 - 0.2, dur=0.6)
    sfx(t_250, "check", 0.35)
    pop("#voz", t_voz, sound="pop")
    js(f'tl.to("#voz", {{scale:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_nav:.3f});')
    t_te, t_toc, t_cue, t_com = P("te"), P("tocado"), P("cuentamelo"), P("comentarios")
    slide_in("#cbox", t_te - 0.2, dy=-80)
    type_on("#ctt .kc", len(cta), t_toc, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_cue:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.2:.3f});')
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:76px; top:28px; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; gap:12px; }}
.lball {{ border-radius:50%; background:radial-gradient(circle at 35% 30%, #fff7e0, #e8c9a0 55%, #b98b5a); box-shadow:0 14px 30px rgba(0,0,0,0.45);
  display:flex; align-items:center; justify-content:center; }}
.lball span {{ font-family:{FONT}; font-weight:900; color:#3b2412; letter-spacing:-1px; }}
.lball.gold {{ background:radial-gradient(circle at 35% 30%, #fff7cc, #f5c542 50%, #b45309); box-shadow:0 0 80px 20px rgba(245,197,66,0.55); }}
.dec {{ border-radius:14px; background:linear-gradient(135deg,#fef3c7,#fde68a); border:4px solid #b45309; box-shadow:0 12px 26px rgba(0,0,0,0.4); }}
.dech {{ position:absolute; left:0; right:0; top:10px; text-align:center; font:900 26px {FONT}; color:#7c2d12; letter-spacing:1px; }}
.decn {{ position:absolute; left:0; right:0; top:46px; text-align:center; font:900 72px {FONT}; color:#7c2d12; letter-spacing:4px; }}
.decf {{ position:absolute; right:14px; bottom:8px; font:900 28px {FONT}; color:#7c2d12; }}
.calc {{ border-radius:30px; background:#fff; box-shadow:0 20px 50px rgba(0,0,0,0.45); overflow:hidden; }}
.calh {{ height:80px; background:#dc2626; color:#fff; font:900 46px {FONT}; text-align:center; line-height:80px; }}
.caln {{ font:900 170px {FONT}; color:{INK}; text-align:center; line-height:200px; }}
.ckr {{ position:absolute; left:30px; right:30px; display:flex; align-items:center; gap:16px; }}
.cck {{ width:50px; height:50px; border-radius:12px; background:{GOOD_BG}; display:flex; align-items:center; justify-content:center; opacity:0; }}
.ckl {{ flex:1; height:16px; border-radius:8px; background:#cbd5e1; }}
.tline {{ border-radius:7px; background:linear-gradient(90deg,#f5c542,#dc2626); }}
.tdot {{ border-radius:50%; background:#fff; border:10px solid #f5c542; }}
.tlab {{ font:900 76px {FONT}; color:#fff; text-align:center; }}
.mapb {{ border-radius:30px; background:#0c4a6e; overflow:hidden; border:6px solid #e2e8f0; }}
.coast {{ position:absolute; left:-40px; top:-40px; width:420px; height:420px; border-radius:46% 54% 40% 60%; background:#d6b88a; }}
.pinw {{ position:absolute; left:250px; top:70px; width:120px; height:120px; }}
.cz {{ position:absolute; left:200px; top:200px; font:900 70px {FONT}; color:#fff; text-shadow:0 4px 12px rgba(0,0,0,0.6); }}
.school {{ background:#e7d3b0; border-radius:14px; border:6px solid #b08968; }}
.roof {{ position:absolute; left:-30px; right:-30px; top:-110px; height:120px; background:#9a3412; clip-path:polygon(8% 100%, 50% 0, 92% 100%); }}
.ssign {{ position:absolute; left:110px; right:110px; top:24px; padding:10px 0; border-radius:12px; background:#7c2d12; color:#fde68a; font:900 50px {FONT}; text-align:center; }}
.col {{ position:absolute; top:120px; width:44px; height:620px; border-radius:8px; background:#f5ead6; box-shadow:inset -8px 0 0 rgba(0,0,0,0.1); }}
.sdoor {{ position:absolute; left:290px; bottom:0; width:140px; height:240px; border-radius:70px 70px 0 0; background:#5b3a24; }}
.qmark {{ border-radius:50%; background:#f5c542; color:{INK}; font:900 230px {FONT}; text-align:center; line-height:300px; }}
.coin {{ border-radius:50%; background:radial-gradient(circle at 35% 30%, #fff3b0, #facc15 60%, #b45309); border:5px solid #92400e; font:900 56px {FONT}; color:#78350f; text-align:center; line-height:80px; }}
.lect {{ border-radius:20px 20px 0 0; background:linear-gradient(#7c2d12,#5b1d0b); border:6px solid #b08968; }}
.lect::before {{ content:"LOTERÍA"; position:absolute; left:0; right:0; top:40px; text-align:center; font:900 50px {FONT}; color:#fde68a; }}
.cage {{ position:absolute; left:0; top:0; border-radius:50%; border:16px solid; background:rgba(245,197,66,0.08); box-shadow:0 20px 50px rgba(0,0,0,0.45); overflow:hidden; }}
.spk {{ position:absolute; left:calc(50% - 4px); top:0; width:8px; height:100%; background:rgba(255,255,255,0.35); }}
.mini {{ position:absolute; width:34px; height:34px; border-radius:50%; background:radial-gradient(circle at 35% 30%, #fff7e0, #d9b688); }}
.dstand {{ position:absolute; background:#475569; border-radius:12px 12px 0 0; }}
.eur {{ font:900 96px {FONT}; color:{INK}; margin-left:12px; }}
.conf {{ border-radius:4px; }}
.garl {{ }}
.wire {{ position:absolute; left:0; right:0; top:40px; height:6px; background:#334155; border-radius:3px; }}
.lt {{ position:absolute; width:40px; height:56px; border-radius:50% 50% 45% 45%; box-shadow:0 0 30px 6px rgba(255,255,255,0.35); }}
.mas {{ font:900 90px {FONT}; color:{INK}; margin:0 8px; }}
.pubb {{ position:absolute; right:40px; bottom:36px; padding:14px 46px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 66px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_origen()
    scene_cadiz()
    scene_colegio()
    scene_teoria()
    scene_ritual()
    scene_bombos()
    scene_final()
