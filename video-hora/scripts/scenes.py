"""Escenas del vídeo «¿Cenamos tarde por culpa de Hitler?». Un solo mundo: un camino en zigzag
(el mito -> 1940 -> Galicia y Londres -> el sol -> no cuadra -> la posguerra -> las cenas -> el Congreso)."""
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
SUN = "#f59e0b"


def aclock(cid, x, y, size, hh, mm, z=6, ring="#e2e8f0"):
    """Reloj de agujas. Las agujas (cid-h, cid-m) giran con rotation y transformOrigin en su base."""
    oy = (size - 32) / 2 - 6
    ticks = "".join(f'<i class="tk" style="transform-origin:4px {oy:.0f}px;transform:rotate({k * 30}deg)"></i>' for k in range(12))
    add(f'''<div id="{cid}" class="aclock" style="{css_box(x, y, size, size, z)}border-color:{ring}">
      <div class="tkw">{ticks}</div>
      <div id="{cid}-h" class="hand hh" style="transform:rotate({(hh % 12) * 30 + mm * 0.5}deg)"></div>
      <div id="{cid}-m" class="hand mh" style="transform:rotate({mm * 6}deg)"></div><div class="hub"></div></div>''')


def dclock(did, x, y, w, label, time, z=7, col="#fff", bg="#0b1220"):
    add(f'''<div id="{did}" class="dclock" style="{css_box(x, y, w, 170, z)}background:{bg}">
      <div class="dl">{label}</div><div id="{did}-t" class="dt" style="color:{col}">{time}</div></div>''')


def plate(pid, x, y, size, z=5):
    add(f'''<div id="{pid}" class="plate2" style="{css_box(x, y, size, size, z)}">
      <div class="pin">{icon("utensils", size * 0.4, "#94a3b8", 2.2)}</div></div>''')


# ================================================================= MUNDO
MILES = [("1940", 0, 1630), ("Galicia · Londres · Polonia", 1, 570), ("La posguerra", 2, 1630), ("Hoy", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="{SUN}"/><stop offset="0.5" stop-color="#ef4444"/><stop offset="1" stop-color="#6366f1"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 300, ROAD[r] + 34, 600, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    plate("pl0", fx + 80, fy + 560, 420)
    aclock("ck0", fx + 520, fy + 120, 380, 22, 0)
    add(f'<div id="t22" class="tbig" style="{css_box(fx + 560, fy + 520, 300, 120, 7)}">22:00</div>')
    add(f'<div id="hit" class="pill" style="{css_box(fx + 80, fy + 180, None, None, 8)}background:#fff;color:{INK};font-size:52px;opacity:0">¿POR CULPA DE HITLER?</div>')
    add(f'<div id="mito" class="stampbox" style="{css_box(fx + 480, fy + 700, 420, 170, 9)}opacity:0">¿MITO?</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: el reloj cae y da la hora de cenar
    js('tl.fromTo("#ck0", {scale:1.4, rotation:-10, opacity:1}, {scale:1, rotation:0, duration:0.5, ease:"back.out(2)"}, 0);')
    js('tl.fromTo("#ck0-m", {rotation:-360}, {rotation:0, duration:0.8, ease:"power3.out"}, 0);')
    js('tl.fromTo("#pl0", {scale:0.6, opacity:1}, {scale:1, duration:0.45, ease:"back.out(2)"}, 0.1);')
    sfx(0.0, "whoosh", 0.35)
    sfx(0.5, "tic-rodillo", 0.35)
    t_cen, t_tar, t_hit, t_his, t_cur = P("cenamos"), P("tarde"), P("hitler"), P("historia"), P("curiosa")
    js(f'tl.to("#t22", {{scale:1.12, duration:0.15, yoyo:true, repeat:1}}, {t_tar:.3f});')
    pop("#hit", t_hit - 0.3, sound="pop2")
    js(f'tl.to("#hit", {{rotation:-3, duration:0.1, yoyo:true, repeat:3}}, {t_his:.3f});')
    stamp("#mito", t_cur - 0.1)
    sfx(t_cur, "golpe", 0.45)


# ================================================================= 1 · EL CAMBIO (1940)
def scene_cambio():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "EL CAMBIO", color=SUN, txt=INK)
    yr, yh = roller("y40", "0000", 70, "#fff")
    add(f'<div id="ycb" class="cnt" style="{css_box(fx + 40, fy + 180, 330, 120, 8)}background:{INK};opacity:0">{yr}</div>')
    add(f'<div id="fr" class="pill" style="{css_box(fx + 410, fy + 200, None, None, 8)}background:#fff;color:{INK};font-size:48px;opacity:0">{icon("clock", 46, INK, 2.6)} FRANCO ADELANTA</div>')
    aclock("ck1", fx + 330, fy + 340, 300, 12, 0)
    dclock("dpt", fx + 20, fy + 700, 300, "PORTUGAL", "12:00")
    dclock("des", fx + 330, fy + 700, 300, "ESPAÑA", "12:00", col=ACC)
    dclock("duk", fx + 640, fy + 700, 300, "LONDRES", "12:00")
    add(f'<div id="des2" class="dt2" style="{css_box(fx + 330, fy + 760, 300, 110, 9)}opacity:0;color:{BAD}">13:00</div>')
    t_uno, t_cam, t_40, t_fra, t_ade, t_hora, t_has, t_lon, t_por = (P("uno"), P("cambio"), P("1940"), P("franco"), P("adelanto"), P("hora"),
                                                                    P("hasta"), P("londres"), P("portugal"))
    travel(t_uno - 0.25, F(0, 1), 0, 1630, dur=0.6)
    header_in("h1", t_uno, t_cam)
    pop("#ycb", t_40 - 0.3, sound=None)
    roll_set("y40", "0000", yh)
    roll_to("y40", "1940", yh, t_40 - 0.2, dur=0.6)
    pop("#fr", t_fra, sound="pop2")
    js(f'tl.fromTo("#ck1", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_fra:.3f});')
    js(f'tl.to("#ck1-m", {{rotation:"+=360", duration:0.8, ease:"power2.inOut"}}, {t_ade:.3f}); tl.to("#ck1-h", {{rotation:"+=30", duration:0.8, ease:"power2.inOut"}}, {t_ade:.3f});')
    sfx(t_ade, "tic-rodillo", 0.35)
    js(f'tl.to("#ck1", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_hora:.3f});')
    js(f'tl.fromTo("#dpt, #des, #duk", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.3, stagger:0.08}}, {t_has - 0.2:.3f});')
    js(f'tl.to("#duk", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_lon:.3f}); tl.to("#dpt", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_por:.3f});')
    sfx(t_lon, "pop2", 0.25)
    sfx(t_por, "pop2", 0.25)
    # al final, el reloj de España salta a las 13:00
    js(f'tl.to("#des-t", {{opacity:0, duration:0.15}}, {t_por + 0.4:.3f}); tl.fromTo("#des2", {{opacity:0, y:-40}}, {{opacity:1, y:0, duration:0.3, ease:"back.out(2)"}}, {t_por + 0.45:.3f});')
    sfx(t_por + 0.45, "golpe", 0.3)


# ================================================================= GALICIA, LONDRES Y POLONIA
def scene_mapa():
    fx, fy, fw, fh = F(1, 1)
    add(f'<div id="axis" class="axis" style="{css_box(fx + 40, fy + 700, 880, 12, 4)}"></div>')
    add(f'<div id="wl" class="axl" style="{css_box(fx + 30, fy + 730, 140, 60, 4)}">OESTE</div>')
    add(f'<div id="el" class="axl" style="{css_box(fx + 790, fy + 730, 140, 60, 4)}">ESTE</div>')
    pts = [("gal", "GALICIA", 150, "13:00", ACC), ("lon", "LONDRES", 430, "12:00", "#fff"), ("pol", "POLONIA", 800, "13:00", ACC)]
    for pid, lab, x, t, col in pts:
        add(f'<div id="{pid}-p" class="dot" style="{css_box(fx + x - 22, fy + 684, 44, 44, 6)}opacity:0"></div>')
        dclock(f"{pid}-c", fx + x - 120, fy + 460, 240, lab, t, col=col)
        js(f'tl.set("#{pid}-c", {{opacity:0}}, 0);')
    add(f'<div id="same" class="pill" style="{css_box(fx + 240, fy + 220, None, None, 8)}background:{ACC};color:{INK};font-size:50px;opacity:0">= MISMA HORA</div>')
    add(f'<div id="oeste" class="pill" style="{css_box(fx + 60, fy + 840, None, None, 8)}background:{BAD};color:#fff;font-size:46px;opacity:0">{icon("arrow-left", 44, "#fff", 2.6)} MÁS AL OESTE QUE LONDRES</div>')
    t_des, t_ten, t_mis, t_pol, t_aun, t_gal, t_oes, t_lon2 = (P("desde"), P("tenemos"), P("misma"), P("polonia"), P("aunque"), P("galicia"), P("oeste"),
                                                             P("londres", 2))
    travel(t_des - 0.3, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_des)
    js(f'tl.fromTo("#axis", {{scaleX:0}}, {{scaleX:1, transformOrigin:"0% 50%", duration:0.6}}, {t_des:.3f});')
    js(f'tl.fromTo("#pol-p, #pol-c", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35}}, {t_pol - 0.1:.3f});')
    sfx(t_pol, "pop2", 0.3)
    pop("#same", t_mis, sound=None)
    js(f'tl.fromTo("#gal-p, #gal-c", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35}}, {t_gal - 0.1:.3f});')
    sfx(t_gal, "pop2", 0.3)
    js(f'tl.to("#gal-c, #pol-c", {{scale:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_gal + 0.4:.3f});')
    js(f'tl.fromTo("#lon-p, #lon-c", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35}}, {t_lon2 - 0.3:.3f});')
    pop("#oeste", t_oes, sound="check")


# ================================================================= EL SOL CON RETRASO
def scene_sol():
    fx, fy, fw, fh = F(1, 0)
    add(f'''<svg id="arc" data-layout-ignore style="{css_box(fx + 60, fy + 160, 840, 600, 3)}overflow:visible" viewBox="0 0 840 600">
      <path id="arcp" d="M 20 560 Q 420 -200 820 560" stroke="rgba(245,158,11,0.5)" stroke-width="8" fill="none" stroke-dasharray="16 14"/></svg>''')
    add(f'<div id="sun" class="sun" style="{css_box(fx + 20, fy + 640, 160, 160, 5)}"></div>')
    add(f'<div id="hor" class="horiz" data-layout-ignore style="{css_box(fx + 20, fy + 760, 920, 10, 4)}"></div>')
    dclock("dsol", fx + 300, fy + 820, 360, "MEDIODÍA SOLAR", "12:00", col=ACC)
    add(f'<div id="inv" class="pill" style="{css_box(fx + 60, fy + 180, None, None, 8)}background:#1e3a8a;color:#fff;font-size:48px;opacity:0">{icon("snowflake", 46, "#fff", 2.6)} INVIERNO</div>')
    add(f'<div id="retr" class="pill" style="{css_box(fx + 560, fy + 180, None, None, 8)}background:{BAD};color:#fff;font-size:48px;opacity:0">CON RETRASO</div>')
    t_por, t_sol, t_ret, t_inv, t_med, t_lle, t_una, t_y = P("por", 2), P("sol"), P("retraso"), P("invierno"), P("mediodia"), P("llega"), P("una", 2), P("media")
    travel(t_por - 0.3, F(1, 0), 1, 570, dur=0.7)
    js(f'tl.fromTo("#arc", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_por:.3f});')
    # el sol recorre el arco (aprox. con dos tramos)
    js(f'tl.to("#sun", {{x:340, y:-470, duration:{t_lle - t_sol:.2f}, ease:"sine.out"}}, {t_sol:.3f});')
    pop("#retr", t_ret, sound="pop2")
    pop("#inv", t_inv, sound=None)
    js(f'tl.fromTo("#dsol", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.3}}, {t_med - 0.2:.3f});')
    js(f'tl.to("#dsol-t", {{opacity:0, duration:0.12}}, {t_una - 0.2:.3f});')
    add(f'<div id="dsol2" class="dt2" style="{css_box(fx + 300, fy + 880, 360, 110, 9)}opacity:0;color:{BAD}">13:30</div>')
    js(f'tl.fromTo("#dsol2", {{opacity:0, scale:1.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_una - 0.1:.3f});')
    sfx(t_una, "golpe", 0.35)
    js(f'tl.to("#sun", {{boxShadow:"0 0 120px 50px rgba(245,158,11,0.7)", duration:0.4, yoyo:true, repeat:1}}, {t_y:.3f});')


# ================================================================= 2 · EL MITO
def scene_mito():
    fx, fy, fw, fh = F(2, 0)
    header("h2", fx, fy, "2", "EL MITO", color=BAD, txt="#fff")
    add(f'<div id="pv" class="pill" style="{css_box(fx + 40, fy + 190, None, None, 8)}background:#fff;color:{INK};font-size:48px;opacity:0">{icon("flower", 46, "#db2777", 2.6)} PRIMAVERA DE 1940</div>')
    aclock("cke", fx + 80, fy + 330, 340, 13, 0)
    aclock("ckd", fx + 540, fy + 330, 340, 14, 0, ring="#ef4444")
    add(f'<div id="le" class="axl" style="{css_box(fx + 80, fy + 690, 340, 70, 6)}opacity:0">ESPAÑA</div>')
    add(f'<div id="ld" class="axl" style="{css_box(fx + 540, fy + 690, 340, 70, 6)}opacity:0">ALEMANIA</div>')
    add(f'<div id="plus1" class="pill" style="{css_box(fx + 600, fy + 250, None, None, 9)}background:{BAD};color:#fff;font-size:52px;opacity:0">+1 HORA</div>')
    add(f'<div id="nc" class="stampbox" style="{css_box(fx + 170, fy + 790, 620, 170, 9)}opacity:0">NO CUADRA</div>')
    t_dos, t_mit, t_dic, t_hit2, t_pri, t_ale, t_seg, t_del = P("dos"), P("mito"), P("dice"), P("hitler", 2), P("primavera"), P("alemania"), P("seguia"), P("delante")
    travel(t_dos - 0.3, F(2, 0), 2, 570, dur=0.7)
    hide_mile(1, t_dos)
    header_in("h2", t_dos, t_mit)
    js(f'tl.fromTo("#cke, #le", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_dic:.3f});')
    js(f'tl.fromTo("#ckd, #ld", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_hit2 - 0.1:.3f});')
    sfx(t_dic, "pop2", 0.25)
    sfx(t_hit2, "pop2", 0.25)
    pop("#pv", t_pri - 0.1, sound=None)
    js(f'tl.to("#ckd-m", {{rotation:"+=360", duration:0.6, ease:"power2.inOut"}}, {t_ale:.3f});')
    pop("#plus1", t_seg, sound="check")
    stamp("#nc", t_del - 0.1)
    sfx(t_del, "golpe", 0.45)


# ================================================================= 3 · LA VERDADERA RAZÓN
def scene_razon():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h3", fx, fy, "3", "LA VERDADERA RAZÓN", color=GOOD_BG, txt="#fff")
    add(character("wk", "g1", fx + 200, fl, 1.0, z=6))
    for k in range(2):
        add(f'<div id="bc{k}" style="{css_box(fx + 90 + k * 170, fl - 180, 130, 130, 7)}opacity:0">{icon("briefcase", 120, "#e2e8f0", 2.2).replace("<svg", "<svg fill=\"#78350f\"")}</div>')
    add(f'<div id="x2" class="pill" style="{css_box(fx + 90, fy + 200, None, None, 8)}background:{ACC};color:{INK};font-size:52px;opacity:0">2 TRABAJOS</div>')
    aclock("ck3", fx + 460, fy + 200, 260, 18, 0)
    add(f'<div id="pg" class="pill" style="{css_box(fx + 430, fy + 480, None, None, 8)}background:#334155;color:#fff;font-size:44px;opacity:0">POSGUERRA</div>')
    card("sinc", fx + 460, fy + 620, 460, 220, f'''
      <div style="position:absolute;left:28px;top:24px;font:900 44px {FONT};color:#64748b">ESTUDIO · SINC</div>
      <div style="position:absolute;left:28px;top:90px;display:flex;align-items:center;gap:14px;font:900 46px {FONT};color:{INK}">
        {icon("sun", 64, SUN, 2.6)} SOL &gt; {icon("clock", 60, INK, 2.6)}</div>''')
    t_tres, t_raz, t_pos, t_dos2, t_tra, t_tar2, t_cas, t_est, t_sinc, t_sol2, t_rel = (
        P("tres"), P("razon"), P("posguerra"), P("dos", 2), P("trabajos"), P("tarde", 2), P("casa"), P("estudio"), P("sinc"), P("sol", 2), P("reloj"))
    travel(t_tres - 0.3, F(2, 1), 2, 1630, dur=0.7)
    header_in("h3", t_tres, t_raz)
    life("wk", 0, G.DUR, 3)
    js(f'tl.fromTo("#wk", {{opacity:0, x:-80}}, {{opacity:1, x:0, duration:0.4}}, {t_pos - 0.2:.3f});')
    pop("#pg", t_pos, sound=None)
    js(f'tl.fromTo("[id^=bc]", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.35, stagger:0.15, ease:"bounce.out"}}, {t_dos2:.3f});')
    pop("#x2", t_tra, sound="pop2")
    js(f'tl.fromTo("#ck3", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_tra:.3f}); tl.to("#ck3-m", {{rotation:"+=1440", duration:1.2, ease:"power1.inOut"}}, {t_tar2 - 0.4:.3f}); tl.to("#ck3-h", {{rotation:"+=120", duration:1.2, ease:"power1.inOut"}}, {t_tar2 - 0.4:.3f});')
    sfx(t_tar2, "tic-rodillo", 0.3)
    js(f'tl.to(Q("wk","head"), {{rotation:10, svgOrigin:PIV.head, duration:0.4}}, {t_cas:.3f}); tl.to(Q("wk","eyes"), {{scaleY:0.4, svgOrigin:PIV.eyes, duration:0.3}}, {t_cas:.3f});')
    slide_in("#sinc", t_est, dy=60, sound="pop")
    js(f'tl.to("#sinc", {{scale:1.05, duration:0.15, yoyo:true, repeat:1}}, {t_sinc:.3f});')
    js(f'tl.to("#sinc svg:first-of-type", {{rotation:180, duration:0.6}}, {t_sol2:.3f});')
    sfx(t_rel, "check", 0.3)


# ================================================================= RESULTADO: LAS CENAS
def scene_cenas():
    fx, fy, fw, fh = F(3, 1)
    plate("pes", fx + 60, fy + 260, 380)
    plate("pno", fx + 520, fy + 260, 380)
    dclock("tes", fx + 70, fy + 690, 360, "ESPAÑA", "22:00", col=ACC)
    dclock("tno", fx + 530, fy + 690, 360, "PAÍSES NÓRDICOS", "17:00", col="#93c5fd")
    add(f'<div id="moon" style="{css_box(fx + 330, fy + 120, 120, 120, 7)}opacity:0">{icon("moon", 110, "#fde68a", 2.4).replace("<svg", "<svg fill=\"#fde68a\"")}</div>')
    add(f'<div id="sunn" style="{css_box(fx + 790, fy + 120, 120, 120, 7)}opacity:0">{icon("sun", 110, SUN, 2.4)}</div>')
    t_res, t_cen, t_die, t_nor, t_cin, t_sei = P("resultado"), P("cenamos", 2), P("diez"), P("nordicos"), P("cinco"), P("seis")
    travel(t_res - 0.3, F(3, 1), 3, 1630, dur=0.7)
    hide_mile(2, t_res)
    js(f'tl.fromTo("#pes, #tes", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_cen - 0.1:.3f});')
    js(f'tl.fromTo("#moon", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35}}, {t_die - 0.1:.3f});')
    js(f'tl.to("#tes", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_die:.3f});')
    sfx(t_die, "pop", 0.3)
    js(f'tl.fromTo("#pno, #tno", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_nor - 0.2:.3f});')
    js(f'tl.fromTo("#sunn", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35}}, {t_cin - 0.1:.3f});')
    js(f'tl.to("#tno", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_sei:.3f});')
    sfx(t_cin, "pop", 0.3)


# ================================================================= EL CONGRESO + COMENTARIOS
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    add(f'<div id="cong" style="{css_box(fx + 60, fy + 60, 260, 260, 6)}opacity:0">{icon("landmark", 250, "#e2e8f0", 2.2)}</div>')
    add(f'''<div id="opts" class="opts" style="{css_box(fx + 360, fy + 90, 560, 200, 6)}opacity:0">
      <div class="op">{icon("clock", 46, ACC, 2.6)} MISMA HORA</div><div class="op">{icon("clock", 46, "#93c5fd", 2.6)} HORA DE PORTUGAL</div></div>''')
    add(f'<div id="ydeb" class="pill" style="{css_box(fx + 380, fy + 320, None, None, 8)}background:#334155;color:#fff;font-size:44px;opacity:0">AÑOS DE DEBATE</div>')
    cta = "Yo ceno a las…"
    times = ["20:00", "21:00", "22:00", "23:00"]
    card("cbox", fx + 40, fy + 440, 880, 560, f'''
      <div style="position:absolute;left:40px;top:28px;display:flex;align-items:center;gap:22px">{icon("message-circle", 76, INK, 2.4)}
        <span style="font:900 60px {FONT};color:{INK}">Comentarios</span></div>
      {"".join(f'<div class="poll" style="top:{130 + k * 64}px"><span>{t}</span><i id="pp{k}" style="background:{["#22c55e", "#84cc16", ACC, BAD][k]}"></i></div>' for k, t in enumerate(times))}
      <div id="ctt" style="position:absolute;left:40px;top:410px;font:800 56px {FONT};color:{INK};white-space:nowrap">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 930, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_vol, t_por2, t_lle, t_con, t_tu, t_hor, t_cen3, t_leo, t_com = (P("volver"), P("portugal", 2), P("lleva"), P("congreso"), P("tu"), P("hora", 7),
                                                                    P("cenas"), P("leo"), P("comentarios"))
    travel(t_vol - 0.3, F(3, 0), 3, 570, dur=0.6)
    js(f'tl.fromTo("#opts", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.4}}, {t_vol:.3f});')
    js(f'tl.to("#opts .op:last-child", {{scale:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_por2:.3f});')
    js(f'tl.fromTo("#cong", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_lle:.3f});')
    pop("#ydeb", t_con - 0.2, sound="pop2")
    slide_in("#cbox", t_tu - 0.3, dy=80)
    js('tl.set("[id^=pp]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to("[id^=pp]", {{scaleX:1, duration:0.4, stagger:0.12, ease:"back.out(1.6)"}}, {t_hor - 0.1:.3f});')
    sfx(t_hor, "pop2", 0.3)
    type_on("#ctt .kc", len(cta), t_cen3, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.2:.3f});')
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.htitle {{ font-size:70px; top:32px; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; gap:12px; }}
.aclock {{ border-radius:50%; background:#f8fafc; border:16px solid; box-shadow:0 24px 60px rgba(0,0,0,0.5); }}
.tkw {{ position:absolute; inset:0; }}
.tk {{ position:absolute; left:calc(50% - 4px); top:6px; width:8px; height:24px; border-radius:4px; background:#94a3b8; }}
.hand {{ position:absolute; left:calc(50% - 6px); bottom:50%; width:12px; border-radius:6px; transform-origin:50% 100%; }}
.hh {{ height:28%; background:{INK}; }} .mh {{ height:40%; background:{BAD}; }}
.hub {{ position:absolute; left:calc(50% - 14px); top:calc(50% - 14px); width:28px; height:28px; border-radius:50%; background:{INK}; }}
.tbig {{ font:900 100px {FONT}; color:{ACC}; text-align:center; line-height:120px; }}
.stampbox {{ border:12px solid {BAD}; border-radius:24px; color:{BAD}; background:rgba(255,255,255,0.94); font:900 100px {FONT}; text-align:center; line-height:146px; transform:rotate(-8deg); white-space:nowrap; }}
.plate2 {{ border-radius:50%; background:radial-gradient(circle, #f8fafc 0 55%, #e2e8f0 56% 70%, #cbd5e1 71%); box-shadow:0 20px 50px rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; }}
.dclock {{ border-radius:24px; border:5px solid #334155; }}
.dl {{ position:absolute; left:0; right:0; top:14px; text-align:center; font:900 34px {FONT}; color:#94a3b8; white-space:nowrap; }}
.dt {{ position:absolute; left:0; right:0; top:58px; text-align:center; font:900 86px {FONT}; font-variant-numeric:tabular-nums; }}
.dt2 {{ font:900 86px {FONT}; text-align:center; line-height:110px; font-variant-numeric:tabular-nums; }}
.axis {{ border-radius:6px; background:linear-gradient(90deg,#38bdf8,#f8fafc,#ef4444); }}
.axl {{ font:900 40px {FONT}; color:#94a3b8; text-align:center; }}
.dot {{ border-radius:50%; background:#fff; border:8px solid {ACC}; }}
.sun {{ border-radius:50%; background:radial-gradient(circle,#fde68a,#f59e0b 60%,#d97706); box-shadow:0 0 70px 20px rgba(245,158,11,0.5); }}
.horiz {{ background:#475569; border-radius:5px; }}
.opts {{ display:flex; flex-direction:column; gap:20px; }}
.op {{ border-radius:999px; background:#fff; color:{INK}; font:900 42px {FONT}; display:flex; align-items:center; gap:14px; padding:14px 28px; white-space:nowrap; }}
.poll {{ position:absolute; left:40px; right:40px; height:56px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:170px; font:900 44px {FONT}; color:{INK}; font-variant-numeric:tabular-nums; }}
.poll i {{ flex:1; height:32px; border-radius:16px; }}
.pubb {{ position:absolute; right:40px; bottom:30px; padding:12px 44px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 62px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_cambio()
    scene_mapa()
    scene_sol()
    scene_mito()
    scene_razon()
    scene_cenas()
    scene_final()
