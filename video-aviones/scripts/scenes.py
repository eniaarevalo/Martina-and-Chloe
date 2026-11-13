"""Escenas del vídeo «¿Por qué las ventanas de los aviones son redondas?». Un solo mundo: un camino en zigzag
(1954 -> el Comet -> globo -> fatiga -> tanque -> esquina/curva -> solución -> ventanilla y comentarios)."""
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
def plane(pid, x, y, w, z=6, body="#e2e8f0", stripe="#1d4ed8", win="sq", crack=False, roofwin=False):
    """Avión de perfil (viewBox 1000x360). win: 'sq' ventanas con esquinas, 'rd' redondeadas."""
    wins = []
    for i in range(11):
        wx = 250 + i * 50
        if win == "sq":
            wins.append(f'<rect x="{wx}" y="150" width="30" height="34" rx="2" fill="#0f172a"/>')
        else:
            wins.append(f'<rect x="{wx}" y="148" width="30" height="40" rx="15" fill="#0f172a"/>')
    rw = (f'<rect id="{pid}-rw" x="520" y="96" width="34" height="22" rx="2" fill="#0f172a" stroke="{ACC}" stroke-width="0"/>' if roofwin else "")
    cr = (f'<path id="{pid}-crack" d="M 554 96 L 575 120 L 562 140 L 590 168 L 578 190 L 606 222" stroke="{BAD}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' if crack else "")
    svg = f'''<svg viewBox="0 0 1000 360" width="{w}" height="{w * 0.36:.0f}" style="overflow:visible">
      <path d="M 820 150 L 930 40 L 975 40 L 940 170 Z" fill="{stripe}"/>
      <path id="{pid}-fus" d="M 60 200 Q 60 100 200 90 L 900 90 Q 960 95 970 170 Q 960 250 880 255 L 160 255 Q 70 250 60 200 Z" fill="{body}"/>
      <path d="M 100 215 L 960 215" stroke="{stripe}" stroke-width="14"/>
      <path d="M 95 160 Q 110 128 150 128 L 175 128 L 175 165 L 95 165 Z" fill="#0f172a"/>
      {"".join(wins)}{rw}
      <path d="M 420 235 L 700 235 L 560 330 L 470 330 Z" fill="#94a3b8"/>
      <path d="M 860 230 L 960 230 L 930 270 L 880 270 Z" fill="#94a3b8"/>{cr}</svg>'''
    add(f'<div id="{pid}" style="{css_box(x, y, w, w * 0.36, z)}">{svg}</div>')


def arrows_ring(prefix, cx, cy, r, n, z=8, color="#38bdf8", size=70, inward=False):
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        deg = math.degrees(a) + (180 if inward else 0)
        add(f'<div id="{prefix}{i}" class="arr" data-layout-ignore style="{css_box(x - size / 2, y - size / 2, size, size, z)}transform:rotate({deg:.0f}deg);opacity:0">{icon("arrow-right", size, color, 3)}</div>')


def win_box(wid, x, y, w, h, radius, z=6, color="#0f172a", border="#cbd5e1"):
    add(f'<div id="{wid}" class="pwin" style="{css_box(x, y, w, h, z)}border-radius:{radius}px;background:{color};border-color:{border}"></div>')


# ================================================================= MUNDO
MILES = [("1952 · 1954", 0, 1630), ("La fatiga", 1, 570), ("Farnborough", 2, 1630), ("Hoy", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#38bdf8"/><stop offset="0.5" stop-color="#facc15"/><stop offset="1" stop-color="#22c55e"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 240, ROAD[r] + 34, 480, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    add(f'<div id="sky0" class="sky" data-layout-ignore style="{css_box(fx, fy + 20, fw, 1040, 1)}"></div>')
    for k, (cx, cy) in enumerate([(160, 160), (700, 120), (20, 880)]):
        add(f'<div id="cl0{k}" data-layout-ignore style="{css_box(fx + cx, fy + cy, 220, 150, 2)}">{icon("cloud", 220, "#cbd5e1", 2).replace("<svg", "<svg fill=\"#e2e8f0\" opacity=\"0.35\"")}</div>')
    plane("pl0", fx + 40, fy + 330, 880, z=6, crack=True)
    yr, yh = roller("y54", "1954", 80, "#fff")
    add(f'<div id="yb" class="cnt" style="{css_box(fx + 40, fy + 40, 330, 130, 8)}background:{INK}">{yr}</div>')
    add(f'<div id="x2" class="pill" style="{css_box(fx + 420, fy + 60, None, None, 8)}background:{BAD};color:#fff;font-size:60px;opacity:0">{icon("plane", 56, "#fff", 2.6)} ×2</div>')
    add(f'<div id="m3" class="pill" style="{css_box(fx + 620, fy + 60, None, None, 8)}background:#fff;color:{INK};font-size:56px;opacity:0">{icon("calendar", 52, INK, 2.6)} 3 MESES</div>')
    add(f'''<div id="corner" style="{css_box(fx + 330, fy + 640, 300, 300, 9)}opacity:0">
      <svg viewBox="0 0 300 300" width="300" height="300"><path d="M 40 260 L 40 40 L 260 40" stroke="{BAD}" stroke-width="34" fill="none" stroke-linejoin="miter"/>
      <circle id="cdot" cx="40" cy="40" r="34" fill="{ACC}"/></svg></div>''')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: el avión entra a toda velocidad
    js('tl.fromTo("#pl0", {x:-700, rotation:-4}, {x:0, rotation:0, duration:0.6, ease:"power3.out"}, 0);')
    js(f'tl.to("#pl0", {{y:-14, duration:1.0, yoyo:true, repeat:{int(G.DUR / 1.0)}, ease:"sine.inOut"}}, 0.6);')
    js('tl.to("[id^=cl0]", {x:-120, duration:7, ease:"none"}, 0);')
    sfx(0.0, "whoosh", 0.5)
    roll_set("y54", "1954", yh)
    js('tl.fromTo("#yb", {scale:1.4}, {scale:1, duration:0.4, ease:"back.out(2)"}, 0.1);')
    t_dos, t_rom, t_ple, t_tre, t_esq = P("dos"), P("rompieron"), P("pleno"), P("tres"), P("esquina")
    pop("#x2", t_dos, sound="pop2")
    js(f'tl.set("#pl0-crack", {{strokeDasharray:200, strokeDashoffset:200}}, 0);')
    js(f'tl.to("#pl0-crack", {{strokeDashoffset:0, duration:0.35, ease:"power2.in"}}, {t_rom:.3f});')
    shake(t_rom + 0.3, 20)
    sfx(t_rom + 0.3, "golpe", 0.5)
    js(f'tl.to("#pl0", {{rotation:3, duration:0.12, yoyo:true, repeat:3}}, {t_ple:.3f});')
    pop("#m3", t_tre, sound="pop2")
    t_cul = P("culpa")
    js(f'tl.to("#pl0", {{opacity:0.35, duration:0.4}}, {t_cul:.3f});')
    js(f'tl.fromTo("#corner", {{opacity:0, scale:0.3, rotation:-30}}, {{opacity:1, scale:1, rotation:0, duration:0.45, ease:"back.out(2)"}}, {t_esq - 0.15:.3f});')
    js(f'tl.to("#cdot", {{scale:1.4, transformOrigin:"40px 40px", duration:0.2, yoyo:true, repeat:3}}, {t_esq + 0.2:.3f});')
    sfx(t_esq, "golpe-climax", 0.35)
    cam(t_esq - 0.1, (fx + 300, fy + 600, 420, 420), dur=0.35)


# ================================================================= EL COMET
def scene_comet():
    fx, fy, fw, fh = F(0, 1)
    add(f'<div id="sky1" class="sky" data-layout-ignore style="{css_box(fx, fy + 20, fw, 1040, 1)}"></div>')
    card("cmc", fx + 40, fy + 30, 880, 200, f'''
      <div style="position:absolute;left:36px;top:26px;font:900 46px {FONT};color:#64748b">DE HAVILLAND</div>
      <div style="position:absolute;left:36px;top:80px;font:900 96px {FONT};color:{INK}">COMET</div>
''')
    add(f'<div id="jet1" class="pill" style="{css_box(fx + 420, fy + 250, None, None, 9)}background:{ACC};color:{INK};font-size:52px;opacity:0">1.º A REACCIÓN</div>')
    plane("pl1", fx + 40, fy + 560, 700, z=6, body="#f8fafc", stripe="#1e3a8a")
    add(f'<div id="alt" class="altbar" style="{css_box(fx + 820, fy + 280, 90, 740, 5)}"><div id="altf" class="altf"></div></div>')
    add(f'<div id="altic" style="{css_box(fx + 810, fy + 250, 110, 110, 7)}opacity:0">{icon("arrow-up", 110, "#38bdf8", 3)}</div>')
    arrows_ring("zq", fx + 390, fy + 506, 230, 8, size=70, color="#f97316")
    add(f'<div id="presu" class="pill" style="{css_box(fx + 60, fy + 920, None, None, 8)}background:#c2410c;color:#fff;font-size:54px;opacity:0">{icon("gauge", 52, "#fff", 2.6)} PRESURIZADA</div>')
    t_era, t_com, t_pri, t_rea, t_vol, t_alt, t_cab, t_pre = (P("era"), P("comet"), P("primer"), P("reaccion"), P("volaba"), P("altisimo"),
                                                            P("cabina"), P("presurizada"))
    travel(t_era - 0.2, F(0, 1), 0, 1630, dur=0.6)
    slide_in("#cmc", t_com - 0.1, dy=-60, sound="pop")
    js(f'tl.fromTo("#pl1", {{opacity:0, x:-400}}, {{opacity:1, x:0, duration:0.6, ease:"power3.out"}}, {t_pri:.3f});')
    sfx(t_pri, "whoosh", 0.35)
    stamp("#jet1", t_rea)
    sfx(t_rea, "golpe", 0.35)
    js(f'tl.fromTo("#altf", {{scaleY:0.1}}, {{scaleY:1, transformOrigin:"50% 100%", duration:0.9, ease:"power2.out"}}, {t_vol:.3f});')
    js(f'tl.to("#pl1", {{y:-180, rotation:-6, duration:0.9, ease:"power2.out"}}, {t_vol:.3f}); tl.to("#pl1", {{rotation:0, duration:0.4}}, {t_alt + 0.5:.3f});')
    js(f'tl.fromTo("#altic", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.3}}, {t_alt:.3f});')
    sfx(t_vol, "whoosh-corto", 0.3)
    js(f'tl.to("#jet1", {{opacity:0, y:-30, duration:0.3}}, {t_cab - 0.2:.3f});')
    js(f'tl.fromTo("[id^=zq]", {{opacity:0, x:0}}, {{opacity:1, duration:0.3, stagger:0.04}}, {t_cab:.3f});')
    js(f'tl.to("[id^=zq]", {{scale:1.25, duration:0.25, yoyo:true, repeat:5}}, {t_pre:.3f});')
    pop("#presu", t_pre, sound="pop2")


# ================================================================= EL GLOBO
def scene_globo():
    fx, fy, fw, fh = F(1, 1)
    plane("pl2", fx + 60, fy + 360, 840, z=6, body="#f8fafc", stripe="#1e3a8a")
    add(f'<div id="inf" class="pill" style="{css_box(fx + 80, fy + 120, None, None, 8)}background:#c2410c;color:#fff;font-size:60px;opacity:0">{icon("maximize-2", 54, "#fff", 2.8)} SE INFLA</div>')
    add(f'<div id="des" class="pill" style="{css_box(fx + 500, fy + 120, None, None, 8)}background:#38bdf8;color:{INK};font-size:60px;opacity:0">{icon("minimize-2", 54, INK, 2.8)} SE DESINFLA</div>')
    add(f'<div id="vlb" class="cnt" style="{css_box(fx + 260, fy + 760, 440, 150, 8)}background:{INK};opacity:0">{icon("plane-takeoff", 80, "#fff", 2.6)}<span style="font:900 64px {FONT};color:#fff;margin-left:16px">VUELO</span></div>')
    t_cad, t_inf, t_glo, t_ate, t_des = P("cada"), P("infla"), P("globo"), P("aterrizar"), P("desinfla")
    travel(t_cad - 0.3, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_cad + 0.2)
    js(f'tl.fromTo("#pl2", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_cad - 0.2:.3f});')
    pop("#vlb", t_cad, sound=None)
    js(f'tl.to("#pl2", {{scaleY:1.35, scaleX:1.05, duration:0.7, ease:"power2.out"}}, {t_inf:.3f});')
    pop("#inf", t_inf, sound="pop")
    js(f'tl.to("#pl2", {{scaleY:1.42, duration:0.2, yoyo:true, repeat:1}}, {t_glo:.3f});')
    js(f'tl.to("#pl2", {{scaleY:1, scaleX:1, duration:0.7, ease:"power2.inOut"}}, {t_ate:.3f});')
    js(f'tl.to("#inf", {{opacity:0.3, duration:0.3}}, {t_ate:.3f});')
    pop("#des", t_des, sound="pop2")
    js(f'tl.to("#pl2", {{y:20, duration:0.3}}, {t_des:.3f});')


# ================================================================= 1 · LA FATIGA
def scene_fatiga():
    fx, fy, fw, fh = F(1, 0)
    header("h1", fx, fy, "1", "LA FATIGA", color="#f97316", txt="#fff")
    add(f'''<div id="clip" style="{css_box(fx + 140, fy + 220, 300, 400, 6)}">
      <div id="clA" class="clh" style="clip-path:inset(0 0 50% 0)">{icon("paperclip", 300, "#cbd5e1", 2.4)}</div>
      <div id="clB" class="clh" style="clip-path:inset(50% 0 0 0)">{icon("paperclip", 300, "#cbd5e1", 2.4)}</div></div>''')
    vc, vh = roller("vc", "000", 70, "#fff")
    add(f'<div id="vcb" class="cnt" style="{css_box(fx + 520, fy + 300, 400, 130, 8)}background:{INK};opacity:0">{icon("repeat", 60, "#fff", 2.6)}{vc}</div>')
    add(f'''<div id="plate" class="plate" style="{css_box(fx + 140, fy + 680, 700, 300, 6)}opacity:0">
      {"".join(f'<i class="riv" style="left:{40 + k * 100}px"></i>' for k in range(7))}
      <svg style="position:absolute;left:0;top:0" width="700" height="300" viewBox="0 0 700 300">
      <path id="pcrack" d="M 340 0 L 360 60 L 330 110 L 380 170 L 350 230 L 390 300" stroke="{BAD}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="plab">METAL</div></div>''')
    t_uno, t_fat, t_dob, t_muc, t_rom, t_met, t_ig = P("uno"), P("fatiga"), P("dobla"), P("muchas"), P("rompe"), P("metal"), P("igual")
    travel(t_uno - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h1", t_uno, t_fat)
    js(f'tl.fromTo("#clip", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.3}}, {t_dob - 0.2:.3f});')
    js(f'tl.fromTo("#clA", {{rotation:-25}}, {{rotation:25, transformOrigin:"50% 100%", duration:0.18, yoyo:true, repeat:{int((t_rom - t_dob) / 0.18)}, ease:"sine.inOut", immediateRender:false}}, {t_dob:.3f});')
    sfx(t_dob, "tic-rodillo", 0.3)
    pop("#vcb", t_muc - 0.1, sound=None)
    roll_set("vc", "000", vh)
    roll_to("vc", "999", vh, t_muc, dur=max(0.4, t_rom - t_muc - 0.1), spins=2)
    js(f'tl.to("#clA", {{x:-120, y:-160, rotation:-60, duration:0.45, ease:"power2.out"}}, {t_rom + 0.05:.3f});')
    js(f'tl.to("#clB", {{x:80, y:40, rotation:30, duration:0.45, ease:"power2.out"}}, {t_rom + 0.05:.3f});')
    shake(t_rom + 0.05, 14)
    sfx(t_rom + 0.05, "golpe", 0.45)
    js(f'tl.fromTo("#plate", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_met - 0.2:.3f});')
    js('tl.set("#pcrack", {strokeDasharray:340, strokeDashoffset:340}, 0);')
    js(f'tl.to("#pcrack", {{strokeDashoffset:0, duration:0.6, ease:"power2.in"}}, {t_ig - 0.2:.3f});')
    sfx(t_ig, "golpe", 0.35)


# ================================================================= 2 · EL TANQUE Y LA ESQUINA
def scene_tanque():
    fx, fy, fw, fh = F(2, 0)
    header("h2", fx, fy, "2", "LAS ESQUINAS", color="#38bdf8", txt=INK)
    add(f'''<div id="tank" class="tank" style="{css_box(fx + 20, fy + 300, 920, 700, 4)}">
      <div id="water" class="water"></div></div>''')
    plane("pl3", fx + 70, fy + 520, 820, z=6, body="#f8fafc", stripe="#1e3a8a", crack=True, roofwin=True)
    for k in range(6):
        add(f'<div id="bub{k}" class="bub" data-layout-ignore style="{css_box(fx + 120 + k * 140, fy + 900, 40, 40, 7)}opacity:0"></div>')
    cy, cyh = roller("cyc", "000", 64, "#fff")
    add(f'<div id="cycb" class="cnt" style="{css_box(fx + 560, fy + 180, 380, 110, 8)}background:{INK};opacity:0">{icon("refresh-cw", 54, "#38bdf8", 2.6)}{cy}</div>')
    add(f'<div id="rjo" class="pill" style="{css_box(fx + 120, fy + 420, None, None, 9)}background:{BAD};color:#fff;font-size:58px;opacity:0">{icon("zap", 54, "#fff", 2.6)} ¡SE RAJÓ!</div>')
    t_dos, t_esq, t_enc, t_met, t_tan, t_agu, t_inf, t_otr = (P("dos", 2), P("esquinas"), P("encontrar"), P("metieron"), P("tanque"), P("agua"),
                                                            P("inflaron"), P("otra"))
    travel(t_dos - 0.3, F(2, 0), 2, 570, dur=0.75)
    hide_mile(1, t_dos + 0.2)
    header_in("h2", t_dos, t_esq)
    js(f'tl.fromTo("#tank", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_enc:.3f});')
    js(f'tl.fromTo("#pl3", {{opacity:0, y:-500}}, {{opacity:1, y:0, duration:0.6, ease:"bounce.out"}}, {t_met:.3f});')
    sfx(t_met + 0.3, "golpe", 0.3)
    js(f'tl.fromTo("#water", {{scaleY:0}}, {{scaleY:1, transformOrigin:"50% 100%", duration:0.9, ease:"power2.out"}}, {t_tan:.3f});')
    sfx(t_tan, "whoosh", 0.35)
    for k in range(6):
        js(f'tl.fromTo("#bub{k}", {{opacity:0, y:0}}, {{opacity:0.8, y:-420, duration:1.4, repeat:3, ease:"power1.in", immediateRender:false}}, {t_agu + k * 0.15:.3f});')
    pop("#cycb", t_inf - 0.1, sound=None)
    roll_set("cyc", "000", cyh)
    js(f'tl.to("#pl3", {{scaleY:1.18, duration:0.22, yoyo:true, repeat:{int((P("hasta") - t_inf) / 0.22) // 2 * 2 + 1}, ease:"sine.inOut"}}, {t_inf:.3f});')
    roll_to("cyc", "999", cyh, t_inf, dur=P("hasta") - t_inf, spins=3)
    t_has, t_raj, t_gri, t_esq2, t_ven, t_tec = P("hasta"), P("rajo"), P("grieta"), P("esquina", 2), P("ventanita"), P("techo")
    js('tl.set("#pl3-crack", {strokeDasharray:200, strokeDashoffset:200}, 0);')
    js(f'tl.to("#pl3-crack", {{strokeDashoffset:0, duration:0.3, ease:"power2.in"}}, {t_raj:.3f});')
    shake(t_raj + 0.1, 20)
    sfx(t_raj + 0.1, "golpe-climax", 0.5)
    stamp("#rjo", t_raj + 0.1)
    # zoom a la ventanita del techo (en la caja del avión: x 520..554, y 96..118 de 1000x360)
    s = 820 / 1000
    rx, ry = fx + 70 + 537 * s, fy + 520 + 107 * s
    js(f'tl.to("#rjo", {{opacity:0, duration:0.2}}, {t_gri - 0.1:.3f});')
    cam(t_gri, (rx - 170, ry - 140, 340, 340), dur=0.6)
    js(f'tl.to("#pl3-rw", {{attr:{{"stroke-width":8}}, duration:0.3, yoyo:true, repeat:5}}, {t_ven:.3f});')
    sfx(t_esq2, "pop2", 0.3)
    js(f'tl.to("#pl3-crack", {{attr:{{"stroke-width":14}}, duration:0.2, yoyo:true, repeat:3}}, {t_tec:.3f});')


# ================================================================= ESQUINA CONTRA CURVA
def scene_curva():
    fx, fy, fw, fh = F(2, 1)
    win_box("wsq", fx + 60, fy + 300, 380, 440, 6, z=5)
    win_box("wrd", fx + 520, fy + 300, 380, 440, 160, z=5)
    add(f'<div id="lsq" class="wlab" style="{css_box(fx + 60, fy + 40, 380, 80, 6)}opacity:0">ESQUINA</div>')
    add(f'<div id="lrd" class="wlab" style="{css_box(fx + 520, fy + 40, 380, 80, 6)}opacity:0">CURVA</div>')
    # flechas que chocan en la esquina (izquierda) y que rodean la curva (derecha)
    for k, (x, y, rot) in enumerate([(-90, 40, 0), (60, -110, 90), (-60, -40, 45)]):
        add(f'<div id="fa{k}" data-layout-ignore style="{css_box(fx + 60 + x, fy + 300 + y, 80, 80, 7)}transform:rotate({rot}deg);opacity:0">{icon("arrow-right", 80, "#f97316", 3)}</div>')
    add(f'<div id="hot" class="hot" data-layout-ignore style="{css_box(fx + 60 - 70, fy + 300 - 70, 140, 140, 8)}opacity:0"></div>')
    add(f'''<svg id="flow" data-layout-ignore style="{css_box(fx + 470, fy + 250, 480, 540, 7)}overflow:visible;opacity:0" viewBox="0 0 480 560">
      <path id="fl1" d="M 240 10 Q 450 10 450 200 L 450 360 Q 450 550 240 550" stroke="{GOOD}" stroke-width="12" fill="none" stroke-dasharray="26 18"/>
      <path id="fl2" d="M 240 10 Q 30 10 30 200 L 30 360 Q 30 550 240 550" stroke="{GOOD}" stroke-width="12" fill="none" stroke-dasharray="26 18"/></svg>''')
    add(f'<div id="bad1" class="pill" style="{css_box(fx + 70, fy + 800, None, None, 8)}background:{BAD};color:#fff;font-size:50px;opacity:0">{icon("target", 48, "#fff", 2.6)} UN PUNTO</div>')
    add(f'<div id="good1" class="pill" style="{css_box(fx + 540, fy + 800, None, None, 8)}background:{GOOD_BG};color:#fff;font-size:50px;opacity:0">{icon("waves", 48, "#fff", 2.6)} SE REPARTE</div>')
    t_en5, t_esq3, t_fue, t_con, t_pun, t_cur, t_rep = P("en", 5), P("esquina", 3), P("fuerza"), P("concentra"), P("punto"), P("curva"), P("reparte")
    travel(t_en5 - 0.3, F(2, 1), 2, 1630, dur=0.6)
    js(f'tl.fromTo("#wsq", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_esq3 - 0.1:.3f});')
    js(f'tl.fromTo("#lsq", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_esq3:.3f});')
    sfx(t_esq3, "pop", 0.3)
    js(f'tl.fromTo("[id^=fa]", {{opacity:0, x:-60, y:-60}}, {{opacity:1, x:0, y:0, duration:0.4, stagger:0.08}}, {t_fue:.3f});')
    js(f'tl.fromTo("#hot", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.3}}, {t_con:.3f});')
    js(f'tl.to("#hot", {{scale:1.35, duration:0.2, yoyo:true, repeat:5}}, {t_con + 0.3:.3f});')
    sfx(t_con, "golpe", 0.35)
    pop("#bad1", t_pun, sound="pop2")
    js(f'tl.fromTo("#wrd", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_cur - 0.1:.3f});')
    js(f'tl.fromTo("#lrd", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_cur:.3f});')
    sfx(t_cur, "pop", 0.3)
    js(f'tl.to("#flow", {{opacity:1, duration:0.3}}, {t_rep - 0.1:.3f});')
    js(f'tl.fromTo("#fl1, #fl2", {{strokeDashoffset:0}}, {{strokeDashoffset:-220, duration:1.2, repeat:2, ease:"none"}}, {t_rep - 0.1:.3f});')
    pop("#good1", t_rep, sound="check")


# ================================================================= 3 · LA SOLUCIÓN
def scene_solucion():
    fx, fy, fw, fh = F(3, 1)
    header("h3", fx, fy, "3", "LA SOLUCIÓN", color=GOOD_BG, txt="#fff")
    win_box("wmorph", fx + 60, fy + 190, 260, 330, 4, z=6, color="#38bdf8")
    add(f'<div id="okc" style="{css_box(fx + 240, fy + 170, 110, 110, 8)}opacity:0">{icon("circle-check", 110, GOOD, 2.6).replace("<svg", "<svg fill=\"#052e16\"")}</div>')
    add(f'''<div id="skin" style="{css_box(fx + 420, fy + 220, 480, 260, 6)}">
      <div class="sklab">FUSELAJE</div><div id="skbar" class="skbar"></div></div>''')
    # tres capas de la ventanilla
    for k in range(3):
        add(f'<div id="pane{k}" class="pane" style="{css_box(fx + 140 + k * 40, fy + 560 + k * 20, 300, 420, 6 - k)}opacity:0;background:rgba(186,230,253,{0.25 + k * 0.2})">'
            + (f'<div id="hole" class="hole"></div>' if k == 1 else "") + '</div>')
    add(f'<div id="c3" class="pill" style="{css_box(fx + 560, fy + 600, None, None, 8)}background:#fff;color:{INK};font-size:54px;opacity:0">{icon("layers", 52, INK, 2.6)} 3 CAPAS</div>')
    add(f'<div id="ah" class="pill" style="{css_box(fx + 560, fy + 740, None, None, 8)}background:{ACC};color:{INK};font-size:50px;opacity:0">{icon("wind", 48, INK, 2.6)} AGUJERITO</div>')
    add(f'<div id="eqp" class="pill" style="{css_box(fx + 560, fy + 880, None, None, 8)}background:{GOOD_BG};color:#fff;font-size:50px;opacity:0">= PRESIÓN</div>')
    for k in range(3):
        add(f'<div id="air{k}" data-layout-ignore style="{css_box(fx + 330 + k * 0, fy + 700 + k * 50, 70, 70, 9)}opacity:0">{icon("arrow-left", 70, "#38bdf8", 3)}</div>')
    t_tres, t_sol, t_des, t_ven, t_red, t_fus, t_gru = P("tres", 2), P("solucion"), P("desde"), P("ventanas"), P("redondeadas"), P("fuselaje"), P("grueso")
    travel(t_tres - 0.3, F(3, 1), 3, 1630, dur=0.7)
    hide_mile(2, t_tres + 0.2)
    header_in("h3", t_tres, t_sol)
    js(f'tl.fromTo("#wmorph", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_ven - 0.1:.3f});')
    js(f'tl.to("#wmorph", {{borderRadius:"120px", duration:0.6, ease:"back.out(1.6)"}}, {t_red:.3f});')
    sfx(t_red, "whoosh-corto", 0.3)
    js(f'tl.fromTo("#okc", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(3)"}}, {t_red + 0.5:.3f});')
    sfx(t_red + 0.5, "check", 0.35)
    js(f'tl.fromTo("#skin", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_fus - 0.1:.3f});')
    js(f'tl.fromTo("#skbar", {{scaleY:0.3}}, {{scaleY:1, transformOrigin:"50% 0%", duration:0.6, ease:"back.out(2)"}}, {t_gru:.3f});')
    sfx(t_gru, "madera", 0.35)
    t_tie, t_cap, t_med, t_agu, t_igu, t_pre = P("tienen"), P("capas"), P("medio"), P("agujerito"), P("igualar"), P("presion")
    js(f'tl.fromTo("[id^=pane]", {{opacity:0, x:0}}, {{opacity:1, duration:0.3, stagger:0.1}}, {t_tie:.3f});')
    js(f'tl.fromTo("#pane0", {{x:0}}, {{x:-60, duration:0.4}}, {t_cap:.3f}); tl.fromTo("#pane2", {{x:0}}, {{x:60, duration:0.4}}, {t_cap:.3f});')
    pop("#c3", t_cap, sound="pop2")
    js(f'tl.to("#pane1", {{y:-20, duration:0.2, yoyo:true, repeat:1}}, {t_med:.3f});')
    js(f'tl.fromTo("#hole", {{scale:0.4}}, {{scale:1.8, duration:0.25, yoyo:true, repeat:3}}, {t_agu:.3f});')
    pop("#ah", t_agu, sound="pop")
    js(f'tl.fromTo("[id^=air]", {{opacity:0, x:80}}, {{opacity:1, x:-40, duration:0.6, stagger:0.12, repeat:1}}, {t_igu:.3f});')
    pop("#eqp", t_pre, sound="check")


# ================================================================= VENTANILLA Y COMENTARIOS
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    fl = floor(3)
    win_box("vw", fx + 120, fy + 520, 300, 400, 140, z=4, color="#7dd3fc", border="#e2e8f0")
    add(f'<div id="vcl" data-layout-ignore style="{css_box(fx + 150, fy + 640, 200, 140, 5)}">{icon("cloud", 200, "#fff", 2).replace("<svg", "<svg fill=\"#fff\"")}</div>')
    add(f'<div id="glow" class="wglow" data-layout-ignore style="{css_box(fx + 100, fy + 500, 340, 440, 3)}opacity:0"></div>')
    add(character("pas", "g2", fx + 640, fl, 1.0, z=6))
    cta = "Yo sí lo vi…"
    card("cbox", fx + 60, fy + 30, 840, 440, f'''
      <div style="position:absolute;left:40px;top:34px;display:flex;align-items:center;gap:22px">{icon("message-circle", 84, INK, 2.4)}
        <span style="font:900 68px {FONT};color:{INK}">Comentarios</span></div>
      <div style="position:absolute;left:40px;top:150px;font:900 50px {FONT};color:#555">¿Te habías fijado?</div>
      <div id="ctt" style="position:absolute;left:40px;top:240px;font:800 72px {FONT};color:{INK}">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 760, fy + 380, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_pro, t_mir, t_ven, t_sab, t_cur, t_alg = P("proxima"), P("mires"), P("ventanilla"), P("sabes"), P("curva", 2), P("algo")
    travel(t_pro - 0.3, F(3, 0), 3, 570, dur=0.7)
    life("pas", 0, G.DUR, 6)
    js(f'tl.fromTo("#vw, #vcl", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_pro:.3f});')
    js(f'tl.to("#vcl", {{x:120, duration:6, ease:"none"}}, {t_pro:.3f});')
    js(f'tl.fromTo("#pas", {{opacity:0, x:120}}, {{opacity:1, x:0, duration:0.5}}, {t_mir - 0.2:.3f}); face("pas", -1, {t_mir:.3f});')
    js(f'point("pas", "L", {t_ven:.3f}, {t_sab + 0.6:.3f}, 70);')
    js(f'tl.to("#glow", {{opacity:1, duration:0.4}}, {t_cur:.3f}); tl.to("#glow", {{scale:1.06, duration:0.3, yoyo:true, repeat:3}}, {t_cur + 0.4:.3f});')
    sfx(t_cur, "check", 0.35)
    js(f'tl.to(Q("pas","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.2}}, {t_alg:.3f});')
    t_hab, t_agu2, t_leo, t_com = P("habias"), P("agujerito", 2), P("leo"), P("comentarios")
    slide_in("#cbox", t_hab - 0.2, dy=-80)
    type_on("#ctt .kc", len(cta), t_agu2, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.2:.3f});')
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.7, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:76px; top:28px; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; gap:12px; }}
.sky {{ border-radius:36px; background:linear-gradient(#0c4a6e, #0f172a); opacity:0.7; }}
.altbar {{ border-radius:45px; background:#1f2937; border:5px solid #475569; overflow:hidden; }}
.altf {{ position:absolute; left:0; right:0; bottom:0; height:100%; background:linear-gradient(#38bdf8,#1d4ed8); }}
.clh {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }}
.plate {{ border-radius:18px; background:linear-gradient(135deg,#cbd5e1,#94a3b8); border:6px solid #e2e8f0; }}
.riv {{ position:absolute; top:24px; width:22px; height:22px; border-radius:50%; background:#64748b; }}
.plab {{ position:absolute; left:30px; bottom:20px; font:900 50px {FONT}; color:#334155; }}
.tank {{ border-radius:30px; border:10px solid #94a3b8; border-top:none; background:rgba(15,23,42,0.6); overflow:hidden; }}
.water {{ position:absolute; left:0; right:0; bottom:0; height:100%; background:linear-gradient(rgba(56,189,248,0.55), rgba(29,78,216,0.65)); }}
.bub {{ border-radius:50%; border:5px solid rgba(255,255,255,0.8); }}
.pwin {{ border:18px solid #cbd5e1; box-shadow:0 20px 50px rgba(0,0,0,0.45); }}
.wlab {{ font:900 64px {FONT}; color:#fff; text-align:center; }}
.hot {{ border-radius:50%; background:radial-gradient(circle, rgba(239,68,68,0.95), rgba(239,68,68,0)); }}
.sklab {{ font:900 50px {FONT}; color:#fff; }}
.skbar {{ position:absolute; left:0; right:0; top:80px; height:150px; border-radius:16px; background:linear-gradient(#cbd5e1,#64748b); border:5px solid #fff; }}
.pane {{ border-radius:120px; border:6px solid #e0f2fe; }}
.hole {{ position:absolute; left:calc(50% - 14px); bottom:40px; width:28px; height:28px; border-radius:50%; background:{ACC}; box-shadow:0 0 30px 8px rgba(250,204,21,0.6); }}
.wglow {{ border-radius:170px; box-shadow:0 0 80px 30px rgba(250,204,21,0.55); border:8px solid {ACC}; }}
.pubb {{ position:absolute; right:40px; bottom:36px; padding:14px 46px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 66px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_comet()
    scene_globo()
    scene_fatiga()
    scene_tanque()
    scene_curva()
    scene_solucion()
    scene_final()
