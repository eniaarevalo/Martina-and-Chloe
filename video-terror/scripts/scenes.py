"""Escenas de la historia de terror «La niña del puerto» (ficción). Un solo mundo: un camino en zigzag
(la llegada -> la niña -> las preguntas -> el puerto -> tres días -> la foto -> las tres de la mañana -> el lunes)."""
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
RED = "#dc2626"
PALE = "#e2e8f0"


def note(nid, x, y, w, text, z=8, rot=-3, size=64, cls="kh"):
    """Texto escrito a mano (Caveat) sobre papel viejo, que se escribe letra a letra con type_on."""
    add(f'<div id="{nid}" class="paper" style="{css_box(x, y, w, None, z)}transform:rotate({rot}deg);opacity:0">'
        f'<div class="hand" style="font-size:{size}px">{chars(text, cls)}</div></div>')
    return len(text)


def house(hid, x, y, w, h, z=3, lit=True):
    win = "#fde68a" if lit else "#111827"
    add(f'''<div id="{hid}" class="house" style="{css_box(x, y, w, h, z)}">
      <div class="hroof"></div>
      <div id="{hid}-w1" class="hwin" style="left:{w * 0.14:.0f}px;background:{win}"></div>
      <div id="{hid}-w2" class="hwin" style="right:{w * 0.14:.0f}px;background:{win}"></div>
      <div class="hdoor" style="left:{w / 2 - 50:.0f}px"></div></div>''')


def fog(fid, x, y, w, z=9):
    add(f'<div id="{fid}" class="fog" data-layout-ignore style="{css_box(x, y, w, 260, z)}"></div>')
    js(f'tl.fromTo("#{fid}", {{x:-80}}, {{x:80, duration:9, yoyo:true, repeat:{int(G.DUR / 9) + 1}, ease:"sine.inOut", immediateRender:false}}, 0);')


def flicker(sel, t, n=6):
    js(f'tl.to("{sel}", {{opacity:0.25, duration:0.05, yoyo:true, repeat:{n * 2 - 1}, ease:"steps(1)"}}, {t:.3f});')


def girl(gid, x, fl, sc=1.0, z=6):
    """La niña: nunca camina ni parpadea; se desliza y se queda quieta mirando."""
    add(character(gid, "nina", x, fl, sc, z=z))


# ================================================================= MUNDO
MILES = [("Jueves", 0, 1630), ("Viernes", 1, 570), ("Sábado", 2, 1630), ("Domingo", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#1e3a8a"/><stop offset="0.6" stop-color="#7f1d1d"/><stop offset="1" stop-color="{RED}"/></linearGradient></defs>
      <path d="{d}" stroke="#15171d" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.10)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="14" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 220, ROAD[r] + 34, 440, 70, 2)}">{lab}</div>')
    for r in range(4):
        fog(f"fog{r}", 0, ROWS[r] + 980, 2200)


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= LA LLEGADA (JUEVES)
def scene_llegada():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    add(f'<div id="sky0" class="sky" data-layout-ignore style="{css_box(fx, fy + 20, fw, 1040, 1)}"></div>')
    add(f'<div id="moon" class="moon" style="{css_box(fx + 720, fy + 60, 150, 150, 2)}"></div>')
    add(f'<div id="sea" class="sea" data-layout-ignore style="{css_box(fx, fy + 640, fw, 140, 2)}"></div>')
    house("hs0", fx + 520, fy + 430, 380, 300, z=3)
    yr, yh = roller("y08", "0000", 70, PALE)
    add(f'<div id="ycb" class="cnt" style="{css_box(fx + 40, fy + 40, 330, 120, 8)}">{yr}</div>')
    add(f'<div id="cdz" class="tagd" style="{css_box(fx + 40, fy + 190, None, None, 8)}opacity:0">{icon("map-pin", 44, RED, 2.6)} COSTA DE CÁDIZ</div>')
    add(character("pa", "padre", fx + 150, fl, 0.95, z=6))
    add(character("ma", "madre", fx + 300, fl, 0.92, z=6))
    add(character("hi", "hija", fx + 410, fl, 0.6, z=6))
    add(f'<div id="lug" style="{css_box(fx + 30, fl - 110, 110, 110, 7)}opacity:0">{icon("luggage", 100, "#94a3b8", 2.4)}</div>')
    add(f'<div id="jue" class="dayc" style="{css_box(fx + 600, fy + 820, 300, 150, 8)}opacity:0"><span>JUEVES</span></div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: el mar, la luna y la casa con las luces encendidas
    js('tl.fromTo("#moon", {scale:0.6, opacity:0.5}, {scale:1, opacity:1, duration:1.2, ease:"power2.out"}, 0);')
    js('tl.fromTo("#hs0", {opacity:1, y:30}, {y:0, duration:0.8, ease:"power3.out"}, 0);')
    js('tl.fromTo("#ycb", {opacity:1, scale:1.3}, {scale:1, duration:0.5, ease:"back.out(2)"}, 0);')
    js(f'tl.to("#sea", {{backgroundPosition:"240px 0", duration:{G.DUR:.2f}, ease:"none"}}, 0);')
    sfx(0.0, "viento", 0.18)
    sfx(0.0, "transicion-terror", 0.35)
    roll_set("y08", "0000", yh)
    t_08, t_fam, t_alq, t_pue, t_cad, t_lle, t_jue = P("2008"), P("familia"), P("alquilo"), P("pueblo"), P("cadiz"), P("llegaron"), P("jueves")
    roll_to("y08", "2008", yh, t_08 - 0.2, dur=0.6)
    for k, cid in enumerate(("pa", "ma", "hi")):
        life(cid, 0, G.DUR, 1 + k)
        js(f'tl.fromTo("#{cid}", {{opacity:0, x:-260}}, {{opacity:1, x:0, duration:1.2, ease:"power1.out"}}, {t_fam + k * 0.15:.3f}); walk("{cid}", {t_fam + k * 0.15:.3f}, {t_fam + 1.2 + k * 0.15:.3f}, 0.14);')
    js(f'tl.fromTo("#lug", {{opacity:0, x:-260}}, {{opacity:1, x:0, duration:1.2}}, {t_fam:.3f});')
    js(f'tl.to("#hs0-w1, #hs0-w2", {{boxShadow:"0 0 40px 10px rgba(253,230,138,0.6)", duration:0.5}}, {t_alq:.3f});')
    pop("#cdz", t_cad - 0.2, sound=None)
    js(f'tl.fromTo("#jue", {{opacity:0, y:-30}}, {{opacity:1, y:0, duration:0.5}}, {t_jue - 0.1:.3f});')
    sfx(t_jue, "golpe-terror", 0.3)


# ================================================================= LA NIÑA
def scene_nina():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    add(f'<div id="lamp" class="lampp" style="{css_box(fx + 760, fy + 200, 60, 860, 3)}"><i class="bulb"></i></div>')
    add(f'<div id="lcone" class="cone" data-layout-ignore style="{css_box(fx + 600, fy + 230, 380, 830, 2)}"></div>')
    add(character("pa1", "padre", fx + 170, fl, 0.95, z=6))
    add(character("ma1", "madre", fx + 320, fl, 0.92, z=6))
    add(character("hi1", "hija", fx + 430, fl, 0.6, z=6))
    girl("g1x", fx + 790, fl, 0.7)
    add(f'<div id="qm" class="qm2" style="{css_box(fx + 680, fy + 260, 220, 220, 8)}opacity:0">?</div>')
    add(f'<div id="perf" class="tagd" style="{css_box(fx + 60, fy + 120, None, None, 8)}opacity:0">{icon("sun", 44, "#fde68a", 2.6)} TODO PERFECTO</div>')
    t_tod, t_per, t_has, t_nin, t_ace, t_ell, t_sie, t_pre, t_ext = (P("todo"), P("perfecto"), P("hasta"), P("nina"), P("acercarse"), P("ellos"), P("siempre"),
                                                                    P("preguntas"), P("extranas"))
    travel(t_tod - 0.3, F(0, 1), 0, 1630, dur=0.8)
    for k, cid in enumerate(("pa1", "ma1", "hi1")):
        life(cid, 0, G.DUR, 4 + k)
    js(f'tl.fromTo("#pa1, #ma1, #hi1", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_tod - 0.2:.3f});')
    pop("#perf", t_per, sound=None)
    js(f'tl.to("#perf", {{opacity:0, duration:0.4}}, {t_has:.3f});')
    js(f'tl.fromTo("#g1x", {{opacity:0}}, {{opacity:1, duration:1.0, ease:"power1.in"}}, {t_nin - 0.3:.3f});')
    sfx(t_nin, "swish-terror", 0.4)
    flicker("#lcone, #lamp .bulb", t_nin - 0.2, 4)
    js(f'tl.to("#g1x", {{x:-260, duration:2.0, ease:"none"}}, {t_ace:.3f});')
    js(f'tl.to(Q("pa1","head"), {{rotation:10, svgOrigin:PIV.head, duration:0.4}}, {t_ell:.3f}); tl.to(Q("ma1","head"), {{rotation:10, svgOrigin:PIV.head, duration:0.4}}, {t_ell:.3f});')
    js(f'tl.to("#ma1", {{x:-40, duration:0.5}}, {t_ell:.3f}); tl.to("#hi1", {{x:-60, duration:0.5}}, {t_ell:.3f});')
    js(f'tl.fromTo("#qm", {{opacity:0, scale:0.4}}, {{opacity:0.9, scale:1, duration:0.5, ease:"back.out(2)"}}, {t_pre:.3f});')
    js(f'tl.to("#qm", {{rotation:12, duration:0.15, yoyo:true, repeat:5}}, {t_ext:.3f});')
    sfx(t_pre, "latido", 0.35)


# ================================================================= LAS PREGUNTAS
def scene_preguntas():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    girl("g2x", fx + 800, fl, 0.8)
    qs = [("¿Cuántos sois en casa?", "users", "cuantos"), ("¿La niña pequeña duerme sola?", "bed-single", "la"),
          ("¿Y cerráis la puerta con llave por la noche?", "key-round", "y")]
    lens = []
    for k, (q, ic, _) in enumerate(qs):
        lens.append(note(f"q{k}", fx + 40, fy + 60 + k * 300, 640, q, rot=[-3, 2, -2][k], size=60, cls=f"q{k}c"))
        add(f'<div id="qi{k}" style="{css_box(fx + 700, fy + 80 + k * 300, 120, 120, 9)}opacity:0">{icon(ic, 110, RED, 2.4)}</div>')
    t_cua, t_sol, t_la2, t_y, t_noc = P("cuantos"), P("sola"), P("la", 2), P("y"), P("noche")
    travel(t_cua - 0.4, F(1, 1), 1, 1630, dur=0.8)
    hide_mile(0, t_cua)
    js(f'tl.fromTo("#g2x", {{opacity:0}}, {{opacity:1, duration:0.8}}, {t_cua - 0.3:.3f});')
    starts = [t_cua, t_la2, t_y]
    ends = [P("casa", 2), t_sol, t_noc]
    for k in range(3):
        js(f'tl.fromTo("#q{k}", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.3}}, {starts[k] - 0.1:.3f});')
        type_on(f"#q{k} .q{k}c", lens[k], starts[k], ends[k] + 0.3)
        js(f'tl.fromTo("#qi{k}", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {ends[k]:.3f});')
        sfx(ends[k], "golpe-terror", 0.25)
        if k < 2:
            js(f'tl.to("#q{k}, #qi{k}", {{opacity:0.35, duration:0.4}}, {starts[k + 1] - 0.2:.3f});')
    js(f'tl.to("#g2x", {{x:-80, duration:{t_noc - t_cua:.2f}, ease:"none"}}, {t_cua:.3f});')
    js(f'tl.to(Q("g2x","head"), {{rotation:-10, svgOrigin:PIV.head, duration:0.6}}, {t_sol:.3f});')
    flicker("#qi1", t_sol + 0.4, 3)


# ================================================================= EL PUERTO (SÁBADO)
def scene_puerto():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    add(f'<div id="sky1" class="sky dusk" data-layout-ignore style="{css_box(fx, fy + 20, fw, 1040, 1)}"></div>')
    add(f'<div id="sea1" class="sea" data-layout-ignore style="{css_box(fx, fy + 700, fw, 200, 2)}"></div>')
    for k, x in enumerate([60, 640]):
        add(f'<div id="boat{k}" style="{css_box(fx + x, fy + 600, 240, 160, 3)}">{icon("sailboat", 230, "#64748b", 2.2).replace("<svg", "<svg fill=\"#1f2937\"")}</div>')
        js(f'tl.to("#boat{k}", {{y:-10, rotation:{3 if k else -3}, duration:1.6, yoyo:true, repeat:{int(G.DUR / 1.6)}, ease:"sine.inOut"}}, 0);')
    add(f'<div id="pier" class="pier" data-layout-ignore style="{css_box(fx, fy + 880, fw, 180, 3)}"></div>')
    add(f'<div id="sab" class="dayc" style="{css_box(fx + 40, fy + 60, 300, 150, 8)}opacity:0"><span>SÁBADO</span></div>')
    add(character("pa2", "padre", fx + 200, fl, 0.95, z=6))
    add(character("ma2", "madre", fx + 350, fl, 0.92, z=6))
    girl("g3x", fx + 760, fl, 0.75)
    n1 = note("dom", fx + 380, fy + 250, 540, "¿Os vais el domingo, verdad?", rot=3, size=58, cls="dc")
    add(f'<div id="como" class="bubble4" style="{css_box(fx + 40, fy + 330, 340, 120, 8)}opacity:0">¿Cómo lo sabes?</div>')
    t_los, t_dec, t_cas, t_sab, t_pue, t_nin3, t_vol, t_os, t_ver, t_pad, t_sab2, t_son = (
        P("los"), P("decidieron"), P("caso"), P("sabado"), P("puerto"), P("nina", 3), P("volvio"), P("os"), P("verdad"), P("padre"), P("sabia"), P("sonrio"))
    travel(t_los - 0.3, F(1, 0), 1, 570, dur=0.8)
    for k, cid in enumerate(("pa2", "ma2")):
        life(cid, 0, G.DUR, 7 + k)
    js(f'tl.fromTo("#pa2, #ma2", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_los - 0.2:.3f});')
    js(f'face("pa2", -1, {t_dec:.3f}); face("ma2", -1, {t_dec + 0.1:.3f});')
    js(f'tl.fromTo("#sab", {{opacity:0, y:-30}}, {{opacity:1, y:0, duration:0.5}}, {t_sab - 0.1:.3f});')
    sfx(t_sab, "golpe-terror", 0.3)
    js(f'walk("pa2", {t_pue - 0.2:.3f}, {t_nin3:.3f}, 0.15); walk("ma2", {t_pue - 0.2:.3f}, {t_nin3:.3f}, 0.15);')
    js(f'face("pa2", 1, {t_nin3:.3f}); face("ma2", 1, {t_nin3:.3f});')
    js(f'tl.set("#g3x", {{opacity:0}}, 0); tl.to("#g3x", {{opacity:1, duration:0.05}}, {t_vol:.3f});')
    sfx(t_vol, "impacto", 0.45)
    shake(t_vol + 0.05, 14)
    js(f'tl.to("#dom", {{opacity:1, duration:0.3}}, {t_os - 0.1:.3f});')
    type_on("#dom .dc", n1, t_os, t_ver + 0.3)
    js(f'tl.to(Q("pa2","brows"), {{y:-8, duration:0.2}}, {t_pad:.3f});')
    js(f'tl.to("#dom", {{opacity:0.3, duration:0.3}}, {t_pad:.3f});')
    pop("#como", t_pad + 0.2, sound=None)
    js(f'tl.to(Q("g3x","mouth"), {{scaleX:1.5, scaleY:1.3, svgOrigin:"120 136", duration:0.6}}, {t_son:.3f});')
    sfx(t_son, "swish-terror", 0.35)


# ================================================================= TRES DÍAS
def scene_tresdias():
    fx, fy, fw, fh = F(2, 0)
    days = ["JUE", "VIE", "SÁB", "DOM"]
    for k, d in enumerate(days):
        col = RED if k == 3 else "#e2e8f0"
        add(f'<div id="dd{k}" class="dbox" style="{css_box(fx + 50 + k * 225, fy + 300, 200, 220, 6)}border-color:{col};color:{col};opacity:0">{d}</div>')
        if k < 3:
            add(f'<div id="dx{k}" style="{css_box(fx + 70 + k * 225, fy + 320, 160, 180, 7)}opacity:0">{icon("x", 160, RED, 3.2)}</div>')
    n2 = note("tres", fx + 60, fy + 620, 840, "«Aquí las familias nunca se quedan más de tres días»", rot=-2, size=56, cls="tc")
    t_por, t_aqu, t_fam, t_nun, t_tres, t_dia = P("porque"), P("aqui"), P("familias"), P("nunca"), P("tres"), P("dias")
    travel(t_por - 0.4, F(2, 0), 2, 570, dur=0.7)
    hide_mile(1, t_por)
    js(f'tl.to("#tres", {{opacity:1, duration:0.3}}, {t_por:.3f});')
    type_on("#tres .tc", n2, t_aqu, t_dia + 0.3)
    for k in range(4):
        js(f'tl.fromTo("#dd{k}", {{opacity:0, y:-40}}, {{opacity:1, y:0, duration:0.3, ease:"back.out(2)"}}, {t_fam + k * 0.12:.3f});')
    for k in range(3):
        js(f'tl.fromTo("#dx{k}", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.2}}, {t_tres + k * 0.18:.3f});')
        sfx(t_tres + k * 0.18, "golpe-terror", 0.25)
    js(f'tl.to("#dd3", {{scale:1.15, boxShadow:"0 0 50px 10px rgba(220,38,38,0.6)", duration:0.25, yoyo:true, repeat:3}}, {t_dia:.3f});')


# ================================================================= LA FOTO
def scene_foto():
    fx, fy, fw, fh = F(2, 1)
    add(f'<div id="bulb2" class="bulb2" style="{css_box(fx + 440, fy + 20, 80, 120, 3)}opacity:0"></div>')
    add(f'<div id="halo2" class="halo2" data-layout-ignore style="{css_box(fx + 180, fy + 40, 600, 600, 2)}opacity:0"></div>')
    add(f'''<div id="drw" class="drawer2" style="{css_box(fx + 140, fy + 760, 680, 260, 4)}"><div class="knob"></div></div>''')
    add(f'''<div id="ph" class="photo" style="{css_box(fx + 270, fy + 220, 420, 500, 6)}opacity:0">
      <div id="ph-f" class="phf">{character("phg", "nina", 210, 520, 0.95, z=1)}</div>
      <div id="ph-b" class="phb"><div class="hand yr">1986</div></div></div>''')
    add(f'<div id="same" class="tagd" style="{css_box(fx + 60, fy + 60, None, None, 9)}opacity:0">{icon("scan-eye", 44, RED, 2.6)} LA MISMA NIÑA</div>')
    n3 = note("ult", fx + 60, fy + 760, 840, "«La última familia tampoco llegó a marcharse»", rot=-2, size=58, cls="uc")
    t_esa, t_mad, t_enc, t_fot, t_ant, t_caj, t_mis, t_nin4, t_rop, t_det, t_86, t_fra, t_ult, t_mar = (
        P("esa"), P("madre"), P("encontro"), P("foto"), P("antigua"), P("cajon"), P("misma"), P("nina", 4), P("ropa"), P("detras"), P("1986"), P("frase"),
        P("ultima"), P("marcharse"))
    travel(t_esa - 0.4, F(2, 1), 2, 1630, dur=0.8)
    js(f'tl.to("#halo2, #bulb2", {{opacity:1, duration:0.3}}, {t_esa - 0.3:.3f});')
    flicker("#halo2, #bulb2", t_esa + 0.2, 5)
    js(f'tl.fromTo("#drw", {{y:0}}, {{y:40, scaleX:1.04, duration:0.6, ease:"power2.out"}}, {t_caj - 0.3:.3f});')
    sfx(t_caj - 0.3, "madera", 0.4)
    js(f'tl.fromTo("#ph", {{opacity:0, y:300, rotation:-10}}, {{opacity:1, y:0, rotation:-3, duration:0.7, ease:"power2.out"}}, {t_ant - 0.1:.3f});')
    sfx(t_ant, "papel", 0.4)
    pop("#same", t_nin4 - 0.1, sound=None)
    js(f'tl.to("#ph", {{scale:1.08, duration:0.4}}, {t_mis:.3f});')
    sfx(t_nin4, "latido", 0.45)
    js(f'tl.to("#ph-f", {{boxShadow:"inset 0 0 0 10px {RED}", duration:0.3, yoyo:true, repeat:1}}, {t_rop:.3f});')
    # dar la vuelta a la foto
    js(f'tl.to("#ph", {{scaleX:0, duration:0.2, ease:"power2.in"}}, {t_det:.3f}); tl.set("#ph-f", {{opacity:0}}, {t_det + 0.2:.3f}); tl.set("#ph-b", {{opacity:1}}, {t_det + 0.2:.3f}); tl.to("#ph", {{scaleX:1.08, duration:0.25, ease:"back.out(2)"}}, {t_det + 0.2:.3f});')
    sfx(t_det, "swish-terror", 0.35)
    js(f'tl.fromTo("#ph-b .yr", {{opacity:0, scale:1.4}}, {{opacity:1, scale:1, duration:0.4}}, {t_86:.3f});')
    sfx(t_86, "impacto", 0.45)
    js(f'tl.to("#ph, #same", {{y:-120, scale:0.8, duration:0.5}}, {t_fra - 0.3:.3f}); tl.to("#drw", {{opacity:0.2, duration:0.4}}, {t_fra - 0.3:.3f});')
    js(f'tl.to("#ult", {{opacity:1, duration:0.3}}, {t_fra:.3f});')
    type_on("#ult .uc", n3, t_ult - 0.3, t_mar + 0.4)
    sfx(t_mar, "golpe-terror", 0.4)
    shake(t_mar + 0.1, 10)


# ================================================================= LAS TRES DE LA MAÑANA
def scene_tres():
    fx, fy, fw, fh = F(3, 1)
    fl = floor(3)
    cl, ch = roller("clk", "00:00", 110, RED)
    add(f'<div id="clkb" class="clk2" style="{css_box(fx + 230, fy + 40, 500, 170, 8)}opacity:0">{cl}</div>')
    add(f'''<div id="dr2" class="door3" style="{css_box(fx + 520, fy + 300, 340, 760, 3)}"><div id="dr2l" class="dleaf"></div></div>''')
    girl("g4x", fx + 690, fl, 0.75, z=4)
    add(character("ma3", "madre", fx + 230, fl, 0.92, z=6))
    n4 = note("mam", fx + 40, fy + 260, 520, "«Mamá, la niña dice que ya podemos ir con ella»", rot=-3, size=52, cls="mc")
    t_a6, t_tre2, t_man, t_peq, t_lla, t_mam, t_nin5, t_dic, t_pod, t_ell2 = (P("a", 6), P("tres", 2), P("manana"), P("pequena", 2), P("llamo"),
                                                                           P("mama"), P("nina", 5), P("dice"), P("podemos"), P("ella", 2))
    travel(t_a6 - 0.4, F(3, 1), 3, 1630, dur=0.8)
    hide_mile(2, t_a6)
    js(f'tl.to("#clkb", {{opacity:1, duration:0.3}}, {t_a6 - 0.2:.3f});')
    roll_set("clk", "00:00", ch)
    roll_to("clk", "03:00", ch, t_tre2 - 0.2, dur=0.6, from_text="00:00")
    sfx(t_tre2, "latido", 0.5)
    js(f'tl.to("#clkb", {{opacity:0.4, duration:0.4, yoyo:true, repeat:9, ease:"steps(1)"}}, {t_man:.3f});')
    life("ma3", 0, G.DUR, 9)
    js(f'tl.fromTo("#ma3", {{opacity:0}}, {{opacity:1, duration:0.5}}, {t_peq - 0.2:.3f}); tl.to(Q("ma3","head"), {{rotation:-12, svgOrigin:PIV.head, duration:0.4}}, {t_lla:.3f});')
    js(f'tl.to("#mam", {{opacity:1, duration:0.3}}, {t_mam - 0.2:.3f});')
    type_on("#mam .mc", n4, t_mam, t_ell2 + 0.4)
    js(f'tl.to("#dr2l", {{scaleX:0.25, transformOrigin:"0% 50%", duration:1.6, ease:"power1.inOut"}}, {t_nin5:.3f});')
    sfx(t_nin5, "transicion-terror", 0.45)
    js(f'tl.set("#g4x", {{opacity:0}}, 0); tl.to("#g4x", {{opacity:0.85, duration:1.4}}, {t_dic:.3f});')
    js(f'tl.to(Q("ma3","eyes"), {{scaleY:1.4, svgOrigin:PIV.eyes, duration:0.2}}, {t_pod:.3f});')
    sfx(t_ell2, "impacto", 0.5)


# ================================================================= EL LUNES
def scene_lunes():
    fx, fy, fw, fh = F(3, 0)
    fl = floor(3)
    add(f'<div id="lun" class="dayc" style="{css_box(fx + 40, fy + 40, 300, 150, 8)}opacity:0"><span>LUNES</span></div>')
    house("hs1", fx + 300, fy + 240, 440, 340, z=3, lit=False)
    add(f'<div id="vac" class="tagd" style="{css_box(fx + 360, fy + 600, None, None, 8)}opacity:0">VACÍA</div>')
    for k in range(2):
        add(f'<div id="lg{k}" style="{css_box(fx + 80 + k * 140, fl - 150, 130, 140, 6)}opacity:0">{icon("luggage", 130, "#94a3b8", 2.2)}</div>')
    add(character("own", "g1", fx + 820, fl, 0.9, z=6))
    add(f'''<div id="ph2" class="photo" style="{css_box(fx + 290, fy + 300, 380, 460, 9)}opacity:0">
      <div id="ph2-f" class="phf">{character("ph2g", "nina", 120, 470, 0.8, z=1)}{character("ph2h", "hija", 270, 470, 0.6, z=1)}</div>
      <div id="ph2-b" class="phb"><div class="hand yr">2008</div></div></div>''')
    add(f'<div id="fic" class="fic" style="{css_box(fx + 160, fy + 990, 640, 60, 9)}opacity:0;white-space:nowrap">HISTORIA DE FICCIÓN</div>')
    add(f'<div id="qq" class="qfinal" style="{css_box(fx + 40, fy + 820, 880, 150, 9)}opacity:0">¿Te habrías quedado hasta el domingo?</div>')
    t_el5, t_lun, t_due, t_vac, t_mal, t_sig, t_y3, t_caj2, t_fot2, t_nue, t_det2, t_08b, t_te, t_dom2 = (
        P("el", 5), P("lunes"), P("dueno"), P("vacia"), P("maletas"), P("seguian"), P("y", 3), P("cajon", 2), P("foto", 2), P("nueva"), P("detras", 2),
        P("2008", 2), P("te"), P("domingo", 2))
    travel(t_el5 - 0.4, F(3, 0), 3, 570, dur=0.8)
    js(f'tl.fromTo("#lun", {{opacity:0, y:-30}}, {{opacity:1, y:0, duration:0.5}}, {t_lun - 0.1:.3f});')
    sfx(t_lun, "golpe-terror", 0.3)
    life("own", 0, G.DUR, 11)
    js(f'tl.fromTo("#own", {{opacity:0, x:120}}, {{opacity:1, x:0, duration:0.8}}, {t_due - 0.3:.3f}); walk("own", {t_due - 0.3:.3f}, {t_due + 0.5:.3f}, 0.14); face("own", -1, {t_due:.3f});')
    pop("#vac", t_vac, sound=None)
    js(f'tl.fromTo("[id^=lg]", {{opacity:0}}, {{opacity:1, duration:0.4, stagger:0.15}}, {t_mal:.3f});')
    js(f'tl.to(Q("own","eyes"), {{scaleY:1.3, svgOrigin:PIV.eyes, duration:0.2}}, {t_sig:.3f});')
    js(f'tl.to("#hs1, #vac, [id^=lg], #own", {{opacity:0.25, duration:0.5}}, {t_y3:.3f});')
    js(f'tl.fromTo("#ph2", {{opacity:0, y:200, rotation:8}}, {{opacity:1, y:0, rotation:2, duration:0.7, ease:"power2.out"}}, {t_fot2 - 0.2:.3f});')
    sfx(t_fot2, "papel", 0.4)
    js(f'tl.to("#ph2", {{scale:1.1, duration:0.5}}, {t_nue:.3f});')
    js(f'tl.to("#ph2", {{scaleX:0, duration:0.2, ease:"power2.in"}}, {t_det2:.3f}); tl.set("#ph2-f", {{opacity:0}}, {t_det2 + 0.2:.3f}); tl.set("#ph2-b", {{opacity:1}}, {t_det2 + 0.2:.3f}); tl.to("#ph2", {{scaleX:1.1, duration:0.25, ease:"back.out(2)"}}, {t_det2 + 0.2:.3f});')
    js(f'tl.fromTo("#ph2-b .yr", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.4}}, {t_08b - 0.1:.3f});')
    sfx(t_08b, "impacto", 0.6)
    shake(t_08b + 0.05, 20)
    js(f'tl.fromTo("#qq", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.5}}, {t_te - 0.2:.3f});')
    js(f'tl.fromTo("#fic", {{opacity:0}}, {{opacity:1, duration:0.6}}, {t_te + 0.4:.3f});')
    sfx(t_dom2, "golpe-terror", 0.35)


CSS = """
@font-face {{ font-family:'Caveat'; font-weight:700; src:url('../assets/fonts/caveat-700.woff2') format('woff2'); }}
#glow {{ background:radial-gradient(ellipse at 50% 70%, rgba(127,29,29,0.35), rgba(30,58,138,0.15) 45%, transparent 70%) !important; }}
#grid {{ opacity:0.45; }}
.room {{ background:rgba(0,0,0,0.25); border:4px solid rgba(255,255,255,0.05); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0b0b0f; border:5px solid #7f1d1d; color:#e2e8f0; font:900 46px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.cnt {{ border-radius:24px; border:4px solid #334155; background:#0b0b0f; display:flex; align-items:center; justify-content:center; }}
.fog {{ border-radius:50%; background:radial-gradient(ellipse, rgba(203,213,225,0.16), rgba(203,213,225,0) 70%); filter:blur(10px); }}
.sky {{ border-radius:36px; background:linear-gradient(#020617, #0f172a 70%); }}
.sky.dusk {{ background:linear-gradient(#1e1b4b, #312e81 40%, #0f172a 75%); }}
.moon {{ border-radius:50%; background:radial-gradient(circle at 40% 40%, #f8fafc, #cbd5e1 60%, #94a3b8); box-shadow:0 0 80px 20px rgba(226,232,240,0.35); }}
.sea {{ background:repeating-linear-gradient(90deg, #0c4a6e 0 60px, #075985 60px 120px); opacity:0.75; border-radius:20px; }}
.house {{ background:#e7e5e4; border-radius:8px; box-shadow:0 20px 50px rgba(0,0,0,0.6); }}
.hroof {{ position:absolute; left:-20px; right:-20px; top:-90px; height:100px; background:#7c2d12; clip-path:polygon(10% 100%, 50% 0, 90% 100%); }}
.hwin {{ position:absolute; top:50px; width:90px; height:90px; border-radius:6px; border:6px solid #57534e; }}
.hdoor {{ position:absolute; bottom:0; width:100px; height:150px; background:#1c1917; border-radius:8px 8px 0 0; }}
.tagd {{ padding:8px 26px; border-radius:999px; background:#0b0b0f; border:4px solid #7f1d1d; color:#e2e8f0; font:900 46px {FONT}; white-space:nowrap; display:inline-flex; align-items:center; gap:14px; }}
.dayc {{ border-radius:20px; background:#f8fafc; border:6px solid #0b0b0f; box-shadow:0 10px 30px rgba(0,0,0,0.5); overflow:hidden; }}
.dayc::before {{ content:""; position:absolute; left:0; right:0; top:0; height:30px; background:{BAD}; }}
.dayc span {{ position:absolute; left:0; right:0; top:42px; text-align:center; font:900 66px {FONT}; color:#0b0b0f; }}
.lampp {{ }}
.lampp::before {{ content:""; position:absolute; left:24px; top:40px; width:12px; height:820px; background:#1f2937; }}
.bulb {{ position:absolute; left:0; top:0; width:60px; height:60px; border-radius:50%; background:#fde68a; box-shadow:0 0 40px 14px rgba(253,230,138,0.6); }}
.cone {{ background:linear-gradient(rgba(253,230,138,0.28), rgba(253,230,138,0)); clip-path:polygon(45% 0, 55% 0, 100% 100%, 0 100%); }}
.qm2 {{ font:900 220px 'Caveat', cursive; color:{BAD}; text-align:center; line-height:220px; }}
.paper {{ padding:24px 34px; border-radius:6px; background:linear-gradient(#f5f0e1, #e8dfc6); box-shadow:0 20px 40px rgba(0,0,0,0.6); }}
.hand {{ font-family:'Caveat', cursive; font-weight:700; color:#1f1300; line-height:1.1; }}
.kh, .q0c, .q1c, .q2c, .dc, .tc, .uc, .mc {{ opacity:0; }}
.bubble4 {{ border-radius:30px; background:#f8fafc; color:#0b0b0f; font:900 46px {FONT}; text-align:center; line-height:120px; white-space:nowrap; }}
.pier {{ background:repeating-linear-gradient(90deg, #3f2a1d 0 70px, #2b1c13 70px 76px); border-top:10px solid #57381f; }}
.dbox {{ border-radius:20px; border:8px solid; background:#0b0b0f; font:900 72px {FONT}; text-align:center; line-height:200px; }}
.bulb2 {{ border-radius:50% 50% 40% 40%; background:#fde68a; box-shadow:0 0 50px 16px rgba(253,230,138,0.6); }}
.halo2 {{ border-radius:50%; background:radial-gradient(circle, rgba(253,230,138,0.22), rgba(253,230,138,0) 70%); }}
.drawer2 {{ border-radius:10px; background:linear-gradient(#5b3a24,#3f2a1d); border:8px solid #2b1c13; }}
.knob {{ position:absolute; left:calc(50% - 30px); top:100px; width:60px; height:40px; border-radius:12px; background:#a16207; }}
.photo {{ border-radius:10px; background:#f5f0e1; padding:20px; box-shadow:0 30px 60px rgba(0,0,0,0.7); }}
.phf {{ position:absolute; left:20px; right:20px; top:20px; bottom:70px; overflow:hidden; background:linear-gradient(#a8a29e,#78716c); filter:sepia(0.8) contrast(1.1); }}
.phb {{ position:absolute; inset:20px; display:flex; align-items:center; justify-content:center; opacity:0; background:#efe6cf; }}
.yr {{ font-size:150px; color:#7f1d1d; }}
.clk2 {{ border-radius:24px; background:#0b0b0f; border:6px solid #1f2937; display:flex; align-items:center; justify-content:center; box-shadow:0 0 40px rgba(220,38,38,0.35); }}
.door3 {{ background:#0b0b0f; border:12px solid #3f2a1d; border-bottom:none; }}
.dleaf {{ position:absolute; inset:0; background:linear-gradient(90deg,#5b3a24,#3f2a1d); }}
.fic {{ font:800 34px {FONT}; color:#94a3b8; text-align:center; letter-spacing:4px; }}
.qfinal {{ border-radius:30px; background:#0b0b0f; border:5px solid {BAD}; color:#f8fafc; font:900 52px {FONT}; text-align:center; display:flex; align-items:center; justify-content:center; padding:0 20px; }}
"""


def build():
    world()
    scene_llegada()
    scene_nina()
    scene_preguntas()
    scene_puerto()
    scene_tresdias()
    scene_foto()
    scene_tres()
    scene_lunes()
