"""Escenas del vídeo «¿Por qué cruzamos los dedos?». Un solo mundo: un camino en zigzag
(el gesto -> la cruz -> el deseo -> las mentiras -> la ciencia -> no se repitió -> de viaje -> comentarios)."""
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
SKIN, SKIN_D = "#f3c9a0", "#a86b3c"
IDX_R, MID_R = 24, -22   # el índice se inclina a la derecha y el corazón a la izquierda: se cruzan


def hand_cross(hid, x, y, size, z=6, glow=False):
    """Mano con el índice y el corazón cruzados (viewBox 300x400). size = ancho."""
    st = f'stroke="{SKIN_D}" stroke-width="7"'
    svg = f'''<svg viewBox="0 0 300 400" width="100%" height="100%" style="overflow:visible">
      <rect x="100" y="320" width="110" height="80" rx="20" fill="{SKIN}" {st}/>
      <rect x="70" y="170" width="170" height="175" rx="60" fill="{SKIN}" {st}/>
      <rect x="175" y="165" width="70" height="48" rx="24" fill="{SKIN}" {st}/>
      <rect x="180" y="205" width="62" height="44" rx="22" fill="{SKIN}" {st}/>
      <g transform="rotate(-32 70 270)"><rect x="30" y="210" width="52" height="110" rx="26" fill="{SKIN}" {st}/></g>
      <g id="{hid}-idx"><rect x="92" y="28" width="48" height="182" rx="24" fill="{SKIN}" {st}/></g>
      <g id="{hid}-mid"><rect x="142" y="14" width="50" height="196" rx="25" fill="{SKIN}" {st}/></g>
    </svg>'''
    cls = "handw glow" if glow else "handw"
    add(f'<div id="{hid}" class="{cls}" style="{css_box(x, y, size, size * 4 / 3, z)}">{svg}</div>')
    js(f'tl.set("#{hid}-idx", {{rotation:{IDX_R}, svgOrigin:"116 200"}}, 0); tl.set("#{hid}-mid", {{rotation:{MID_R}, svgOrigin:"167 200"}}, 0);')


def fist(fid, x, y, size, z=6):
    """Puño con el pulgar apretado dentro (gesto alemán)."""
    st = f'stroke="{SKIN_D}" stroke-width="7"'
    svg = f'''<svg viewBox="0 0 300 300" width="100%" height="100%" style="overflow:visible">
      <rect x="60" y="60" width="190" height="190" rx="60" fill="{SKIN}" {st}/>
      {"".join(f'<rect x="{70 + k * 45}" y="40" width="45" height="80" rx="22" fill="{SKIN}" {st}/>' for k in range(4))}
      <rect id="{fid}-th" x="80" y="110" width="120" height="44" rx="22" fill="#e9b689" {st}/>
      <rect x="110" y="240" width="100" height="60" rx="18" fill="{SKIN}" {st}/></svg>'''
    add(f'<div id="{fid}" style="{css_box(x, y, size, size, z)}">{svg}</div>')


def pointer_hand(pid, x, y, size, z=6, rot=0, flip=False):
    sx = "scaleX(-1) " if flip else ""
    add(f'<div id="{pid}" style="{css_box(x, y, size, size, z)}"><div style="width:100%;height:100%;transform:{sx}rotate({rot}deg)">{icon("pointer", size, SKIN_D, 2.2).replace("<svg", f"<svg fill=\"{SKIN}\"")}</div></div>')


def sparkles(prefix, cx, cy, n, t, r=260, z=8, color="#facc15"):
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        add(f'<div id="{prefix}{i}" data-layout-ignore style="{css_box(x - 35, y - 35, 70, 70, z)}opacity:0">{icon("sparkles", 70, color, 2.4)}</div>')
        js(f'tl.fromTo("#{prefix}{i}", {{opacity:0, scale:0.3, rotation:-40}}, {{opacity:1, scale:1, rotation:0, duration:0.35, ease:"back.out(3)", immediateRender:false}}, {t + i * 0.05:.3f});')
        js(f'tl.to("#{prefix}{i}", {{opacity:0, scale:0.6, duration:0.5}}, {t + 1.2 + i * 0.05:.3f});')


# ================================================================= MUNDO
MILES = [("Cristianismo", 0, 1630), ("La espalda", 1, 570), ("Alemania · 2010", 2, 1630), ("El mundo", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#facc15"/><stop offset="0.5" stop-color="#22c55e"/><stop offset="1" stop-color="#ec4899"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 260, ROAD[r] + 34, 520, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    add(f'<div id="halo" class="halo" data-layout-ignore style="{css_box(fx + 180, fy + 200, 600, 600, 3)}"></div>')
    hand_cross("h0", fx + 300, fy + 220, 360, z=6)
    add(f'<div id="pq" class="bigq" style="{css_box(fx + 160, fy + 760, 640, 170, 9)}opacity:0">¿POR QUÉ?</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: la mano entra y cruza los dedos de golpe
    js('tl.fromTo("#h0", {scale:1.4, rotation:-12}, {scale:1, rotation:0, duration:0.45, ease:"back.out(2.2)"}, 0);')
    js(f'tl.fromTo("#h0-mid", {{rotation:0}}, {{rotation:{MID_R}, svgOrigin:"167 200", duration:0.3, ease:"back.out(3)", immediateRender:false}}, 0.15);')
    js(f'tl.fromTo("#h0-idx", {{rotation:0}}, {{rotation:{IDX_R}, svgOrigin:"116 200", duration:0.3, ease:"back.out(3)", immediateRender:false}}, 0.15);')
    js('tl.fromTo("#halo", {scale:0.4, opacity:1}, {scale:1, opacity:0.8, duration:0.6, ease:"power2.out"}, 0.1);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.4, "pop", 0.45)
    shake(0.45, 10)
    sparkles("sk0-", fx + 480, fy + 460, 7, 0.4, r=300)
    t_sal, t_bie, t_sab = P("salga"), P("bien"), P("sabes")
    js(f'tl.to("#h0", {{y:-20, duration:0.25, yoyo:true, repeat:1}}, {t_bie:.3f});')
    js(f'tl.to("#halo", {{scale:1.1, duration:0.4, yoyo:true, repeat:3}}, {t_sal:.3f});')
    stamp("#pq", t_sab - 0.1)
    sfx(t_sab, "golpe", 0.4)


# ================================================================= 1 · LA CRUZ
def scene_cruz():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "LA CRUZ", color=ACC)
    add(f'<div id="acp" class="pill" style="{css_box(fx + 40, fy + 180, None, None, 8)}background:{GOOD_BG};color:#fff;font-size:52px;opacity:0">{icon("badge-check", 50, "#fff", 2.6)} LA MÁS ACEPTADA</div>')
    hand_cross("h1h", fx + 60, fy + 340, 280, z=6)
    add(f'<div id="eq" class="eqs" style="{css_box(fx + 360, fy + 470, 120, 120, 7)}opacity:0">=</div>')
    add(f'<div id="crs" style="{css_box(fx + 500, fy + 320, 360, 360, 6)}opacity:0">{icon("cross", 340, "#facc15", 2.4).replace("<svg", "<svg fill=\"#78350f\"")}</div>')
    add(f'<div id="shd" style="{css_box(fx + 560, fy + 740, 260, 260, 7)}opacity:0">{icon("shield", 250, "#bfdbfe", 2.4).replace("<svg", "<svg fill=\"#1d4ed8\"")}</div>')
    for k, (x, y) in enumerate([(380, 760), (420, 920), (880, 820)]):
        add(f'<div id="gh{k}" style="{css_box(fx + x, fy + y, 110, 110, 6)}opacity:0">{icon("ghost", 100, "#e9d5ff", 2.4).replace("<svg", "<svg fill=\"#6b21a8\"")}</div>')
    add(f'<div id="enc" class="pill" style="{css_box(fx + 60, fy + 830, None, None, 8)}background:#fff;color:{INK};font-size:48px;opacity:0">COMO LLEVARLA ENCIMA</div>')
    t_uno, t_cru, t_exp, t_ace, t_cri, t_cru2, t_ded, t_pro, t_mal, t_hac, t_man, t_lle = (
        P("uno"), P("cruz"), P("explicacion"), P("aceptada"), P("cristianos"), P("cruz", 2), P("dedos", 2), P("protegerse"), P("mal"),
        P("hacer"), P("mano"), P("llevarla"))
    travel(t_uno - 0.25, F(0, 1), 0, 1630, dur=0.6)
    header_in("h1", t_uno, t_cru)
    pop("#acp", t_ace - 0.1, sound="pop2")
    js(f'tl.fromTo("#h1h", {{opacity:0, x:-100}}, {{opacity:1, x:0, duration:0.4}}, {t_cri - 0.2:.3f});')
    js(f'tl.fromTo("#eq", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(3)"}}, {t_cru2 - 0.1:.3f});')
    js(f'tl.fromTo("#crs", {{opacity:0, scale:0.3, rotation:-45}}, {{opacity:1, scale:1, rotation:0, duration:0.45, ease:"back.out(2)"}}, {t_cru2:.3f});')
    sfx(t_cru2, "golpe", 0.35)
    js(f'tl.to("#h1h-mid, #h1h-idx", {{y:-10, duration:0.15, yoyo:true, repeat:1}}, {t_ded:.3f});')
    js(f'tl.fromTo("#shd", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_pro:.3f});')
    sfx(t_pro, "pop", 0.3)
    for k in range(3):
        js(f'tl.fromTo("#gh{k}", {{opacity:0, x:0}}, {{opacity:1, duration:0.2}}, {t_mal - 0.1 + k * 0.08:.3f}); tl.to("#gh{k}", {{x:{[-180, -160, 200][k]}, y:{[-60, 80, 40][k]}, opacity:0, duration:0.5, ease:"power2.out"}}, {t_mal + 0.3 + k * 0.08:.3f});')
    sfx(t_mal + 0.3, "whoosh-corto", 0.3)
    js(f'tl.to("#h1h", {{filter:"drop-shadow(0 0 40px #facc15)", duration:0.4}}, {t_hac:.3f}); tl.to("#crs", {{scale:0.45, x:-330, y:110, duration:0.6, ease:"power2.inOut"}}, {t_man:.3f}); tl.to("#eq", {{opacity:0, duration:0.2}}, {t_man:.3f});')
    pop("#enc", t_lle, sound="check")


# ================================================================= LA OTRA TEORÍA
def scene_deseo():
    fx, fy, fw, fh = F(1, 1)
    pointer_hand("pa", fx + 120, fy + 300, 300, z=6, rot=35)
    pointer_hand("pb", fx + 540, fy + 300, 300, z=6, rot=35, flip=True)
    add(f'<div id="star" style="{css_box(fx + 380, fy + 120, 200, 200, 8)}opacity:0">{icon("star", 200, "#facc15", 2).replace("<svg", "<svg fill=\"#facc15\"")}</div>')
    add(f'<div id="des" class="pill" style="{css_box(fx + 330, fy + 650, None, None, 8)}background:{ACC};color:{INK};font-size:58px;opacity:0">DESEO</div>')
    add(f'<div id="scr" style="{css_box(fx + 380, fy + 760, 200, 200, 6)}opacity:0">{icon("scroll", 190, "#fde68a", 2.2).replace("<svg", "<svg fill=\"#78350f\"")}</div>')
    add(f'<div id="sp" class="bigstamp sm" style="{css_box(fx + 140, fy + 820, 680, 130, 10)}opacity:0">SIN PRUEBAS</div>')
    t_hay, t_teo, t_dos, t_ind, t_sel, t_jun, t_des, t_nin, t_dem = (P("hay"), P("teoria"), P("dos"), P("indices"), P("sellar"), P("juntos"), P("deseo"),
                                                                    P("ninguna"), P("demostrada"))
    travel(t_hay - 0.3, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_hay + 0.2)
    js(f'tl.fromTo("#pa", {{opacity:0, x:-200}}, {{opacity:1, x:0, duration:0.4}}, {t_dos:.3f}); tl.fromTo("#pb", {{opacity:0, x:200}}, {{opacity:1, x:0, duration:0.4}}, {t_dos + 0.15:.3f});')
    sfx(t_dos, "whoosh-corto", 0.3)
    js(f'tl.to("#pa", {{x:110, y:-30, duration:0.4, ease:"back.out(2)"}}, {t_ind:.3f}); tl.to("#pb", {{x:-110, y:-30, duration:0.4, ease:"back.out(2)"}}, {t_ind:.3f});')
    sfx(t_ind + 0.3, "click", 0.4)
    js(f'tl.fromTo("#star", {{opacity:0, scale:0.2, rotation:-90}}, {{opacity:1, scale:1, rotation:0, duration:0.5, ease:"back.out(2)"}}, {t_sel:.3f});')
    js(f'tl.to("#star", {{scale:1.15, duration:0.2, yoyo:true, repeat:3}}, {t_jun:.3f});')
    pop("#des", t_des, sound="check")
    js(f'tl.fromTo("#scr", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.3}}, {t_nin - 0.2:.3f});')
    stamp("#sp", t_dem - 0.1)
    sfx(t_dem, "golpe", 0.4)


# ================================================================= 2 · LAS MENTIRAS
def scene_mentiras():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    header("h2", fx, fy, "2", "LAS MENTIRAS", color=BAD, txt="#fff")
    add(character("lia", "g1", fx + 300, fl, 1.25, z=6))
    add(f'<div id="xr" class="xray" style="{css_box(fx + 540, fy + 420, 380, 380, 8)}opacity:0"><div class="xrl">DETRÁS</div></div>')
    hand_cross("h2h", fx + 640, fy + 470, 190, z=9)
    add(f'<div id="bub" class="bub2" style="{css_box(fx + 380, fy + 200, 520, 160, 8)}opacity:0">"¡Te lo prometo!"</div>')
    add(f'<div id="cul" class="pill" style="{css_box(fx + 560, fy + 860, None, None, 9)}background:#fff;color:{INK};font-size:56px;opacity:0;text-decoration:line-through;text-decoration-color:{BAD};text-decoration-thickness:8px">CULPA</div>')
    t_dos2, t_men, t_qui, t_mie, t_cru, t_esp, t_cru4, t_lib, t_cul = (P("dos", 2), P("mentiras"), P("quien"), P("miente"), P("cruza"), P("espalda"),
                                                                     P("cruz", 4), P("librara"), P("culpa"))
    travel(t_dos2 - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h2", t_dos2, t_men)
    life("lia", 0, G.DUR, 2)
    js('tl.set("#h2h", {opacity:0}, 0);')
    js(f'tl.fromTo("#lia", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_qui - 0.1:.3f});')
    js(f'tl.to(Q("lia","mouth"), {{scaleX:1.35, svgOrigin:"120 136", duration:0.2}}, {t_mie:.3f}); tilt("lia", {t_mie:.3f});')
    pop("#bub", t_mie, sound="pop2")
    js(f'tl.to(Q("lia","armR"), {{rotation:30, svgOrigin:PIV.armR, duration:0.3}}, {t_cru - 0.1:.3f});')
    js(f'tl.fromTo("#xr", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_cru:.3f});')
    js(f'tl.to("#h2h", {{opacity:1, duration:0.2}}, {t_cru + 0.2:.3f});')
    sfx(t_cru, "whoosh-corto", 0.3)
    js(f'tl.to("#xr", {{scale:1.05, duration:0.15, yoyo:true, repeat:1}}, {t_esp:.3f});')
    js(f'tl.to("#h2h", {{filter:"drop-shadow(0 0 30px #facc15)", duration:0.3}}, {t_cru4:.3f});')
    pop("#cul", t_lib, sound="pop")
    js(f'tl.to("#cul", {{scale:0.85, opacity:0.5, duration:0.3}}, {t_cul + 0.2:.3f});')
    sfx(t_cul, "check", 0.3)


# ================================================================= 3 · LA CIENCIA (EL GOLF)
def scene_golf():
    fx, fy, fw, fh = F(2, 0)
    header("h3", fx, fy, "3", "LA CIENCIA", color="#16a34a", txt="#fff")
    yr, yh = roller("y10", "0000", 64, "#fff")
    add(f'<div id="deb" class="cnt" style="{css_box(fx + 40, fy + 180, 380, 120, 8)}background:{INK};opacity:0"><span class="def"><i style="background:#111"></i><i style="background:#dc2626"></i><i style="background:#facc15"></i></span>{yr}</div>')
    add(f'<div id="psy" class="pill" style="{css_box(fx + 450, fy + 200, None, None, 8)}background:#fff;color:{INK};font-size:48px;opacity:0">{icon("brain", 46, INK, 2.6)} PSICÓLOGOS</div>')
    add(f'''<div id="green" class="green" style="{css_box(fx + 20, fy + 360, 920, 680, 3)}opacity:0">
      <div class="hole"></div><div class="gflag"></div></div>''')
    add(f'<div id="ball" class="gball" style="{css_box(fx + 160, fy + 880, 90, 90, 8)}opacity:0">{icon("clover", 56, GOOD_BG, 2.6)}</div>')
    add(f'<div id="luck" class="pill" style="{css_box(fx + 60, fy + 760, None, None, 9)}background:{GOOD_BG};color:#fff;font-size:46px;opacity:0">{icon("clover", 44, "#fff", 2.6)} "DA SUERTE"</div>')
    pc, ph = roller("putts", "0", 90, "#fff")
    add(f'<div id="pcb" class="cnt" style="{css_box(fx + 600, fy + 760, 320, 150, 9)}background:{INK};opacity:0">{icon("flag-triangle-right", 60, "#fff", 2.6)}{pc}</div>')
    t_tres, t_cie, t_20, t_psi, t_ale, t_pel, t_gol, t_sue, t_emb, t_mas = (P("tres"), P("ciencia"), P("2010"), P("psicologos"), P("alemanes"),
                                                                          P("pelota"), P("golf"), P("suerte"), P("embocas"), P("mas", 2))
    travel(t_tres - 0.3, F(2, 0), 2, 570, dur=0.7)
    hide_mile(1, t_tres + 0.2)
    header_in("h3", t_tres, t_cie)
    pop("#deb", t_20 - 0.4, sound=None)
    roll_set("y10", "0000", yh)
    roll_to("y10", "2010", yh, t_20 - 0.3, dur=0.6)
    pop("#psy", t_psi, sound="pop2")
    js(f'tl.fromTo("#green", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_pel - 0.3:.3f});')
    js(f'tl.fromTo("#ball", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(3)"}}, {t_pel:.3f});')
    sfx(t_gol, "pop", 0.3)
    pop("#luck", t_sue - 0.1, sound="check")
    pop("#pcb", t_emb - 0.3, sound=None)
    roll_set("putts", "0", ph)
    # putts: la bola rueda hasta el hoyo (hoyo en x 700, y 520 de la caja verde)
    js(f'tl.to("#ball", {{x:520, y:-370, duration:0.6, ease:"power2.out"}}, {t_emb - 0.2:.3f}); tl.to("#ball", {{scale:0.5, opacity:0, duration:0.15}}, {t_emb + 0.4:.3f});')
    sfx(t_emb + 0.4, "click", 0.5)
    roll_to("putts", "1", ph, t_emb + 0.4, dur=0.3)
    js(f'tl.set("#ball", {{x:0, y:0}}, {t_emb + 0.6:.3f}); tl.to("#ball", {{opacity:1, scale:1, duration:0.2}}, {t_emb + 0.65:.3f});')
    js(f'tl.to("#ball", {{x:520, y:-370, duration:0.5, ease:"power2.out"}}, {t_mas:.3f}); tl.to("#ball", {{scale:0.5, opacity:0, duration:0.15}}, {t_mas + 0.5:.3f});')
    sfx(t_mas + 0.5, "click", 0.5)
    roll_to("putts", "2", ph, t_mas + 0.5, dur=0.3)
    js(f'tl.to("#pcb", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_mas + 0.6:.3f});')


# ================================================================= LA SEGURIDAD Y LA RÉPLICA
def scene_replica():
    fx, fy, fw, fh = F(2, 1)
    add(f'''<div id="conf" class="vbar2" style="{css_box(fx + 60, fy + 120, 200, 640, 6)}opacity:0"><div id="conf-f" class="vbf2"></div></div>
      <div id="confl" class="tl2" style="{css_box(fx + 20, fy + 780, 280, 70, 6)}opacity:0">CONFIANZA</div>''')
    add(f'<div id="arr" style="{css_box(fx + 330, fy + 300, 260, 160, 7)}opacity:0">{icon("move-right", 250, ACC, 3)}</div>')
    add(f'<div id="hole2" class="hole big" style="{css_box(fx + 640, fy + 330, 220, 110, 5)}opacity:0"></div>')
    add(f'<div id="ayu" class="pill" style="{css_box(fx + 520, fy + 480, None, None, 8)}background:{GOOD_BG};color:#fff;font-size:52px;opacity:0">TE AYUDA</div>')
    add(f'<div id="ball2" class="gball" style="{css_box(fx + 380, fy + 700, 90, 90, 8)}opacity:0">{icon("clover", 56, GOOD_BG, 2.6)}</div>')
    add(f'<div id="hole3" class="hole big" style="{css_box(fx + 640, fy + 700, 220, 110, 5)}opacity:0"></div>')
    add(f'<div id="nsr" class="bigstamp sm" style="{css_box(fx + 140, fy + 880, 700, 130, 10)}opacity:0">NO SE REPITIÓ</div>')
    t_la9, t_cre, t_seg, t_seg2, t_ayu, t_aun, t_rep, t_exp, t_no, t_igu = (P("la", 9), P("creer"), P("seguridad"), P("seguridad", 2), P("ayuda"),
                                                                          P("aunque"), P("repitieron"), P("experimento"), P("no"), P("igual"))
    travel(t_la9 - 0.3, F(2, 1), 2, 1630, dur=0.7)
    js(f'tl.fromTo("#conf, #confl", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_cre - 0.2:.3f});')
    js('tl.set("#conf-f", {scaleY:0.1, transformOrigin:"50% 100%"}, 0);')
    js(f'tl.to("#conf-f", {{scaleY:0.9, duration:0.9, ease:"back.out(1.4)"}}, {t_seg:.3f});')
    sfx(t_seg, "check", 0.3)
    js(f'tl.fromTo("#arr", {{opacity:0, x:-60}}, {{opacity:1, x:0, duration:0.4}}, {t_seg2:.3f}); tl.fromTo("#hole2", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_seg2:.3f});')
    pop("#ayu", t_ayu, sound="pop")
    js(f'tl.fromTo("#ball2, #hole3", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_aun:.3f});')
    js(f'tl.to("#conf, #confl, #arr, #hole2, #ayu", {{opacity:0.25, duration:0.3}}, {t_aun:.3f});')
    js(f'tl.to("#ball2", {{x:420, duration:0.7, ease:"power2.out"}}, {t_rep:.3f}); tl.to("#ball2", {{y:-120, x:500, duration:0.4, ease:"power1.out"}}, {t_exp + 0.1:.3f});')
    sfx(t_rep, "whoosh-corto", 0.3)
    stamp("#nsr", t_no)
    sfx(t_no, "golpe", 0.4)
    js(f'tl.to("#ball2", {{opacity:0.4, duration:0.3}}, {t_igu:.3f});')


# ================================================================= DE VIAJE
def scene_viaje():
    fx, fy, fw, fh = F(3, 1)
    card("vn", fx + 40, fy + 120, 420, 640, f'''
      <div class="ctit"><span class="flagvn"><i></i></span>VIETNAM</div>''')
    hand_cross("h3h", fx + 140, fy + 300, 220, z=7)
    add(f'<div id="vnx" style="{css_box(fx + 110, fy + 300, 280, 290, 8)}opacity:0">{icon("x", 280, BAD, 3.4)}</div>')
    add(f'<div id="ins" class="pill" style="{css_box(fx + 100, fy + 640, None, None, 9)}background:{BAD};color:#fff;font-size:50px;opacity:0">INSULTO</div>')
    card("de", fx + 500, fy + 120, 420, 640, f'''
      <div class="ctit"><span class="def"><i style="background:#111"></i><i style="background:#dc2626"></i><i style="background:#facc15"></i></span>ALEMANIA</div>''')
    fist("fs", fx + 580, fy + 300, 260, z=7)
    add(f'<div id="sue" class="pill" style="{css_box(fx + 560, fy + 640, None, None, 9)}background:{GOOD_BG};color:#fff;font-size:48px;opacity:0">= SUERTE</div>')
    add(f'<div id="via" class="pill" style="{css_box(fx + 300, fy + 830, None, None, 9)}background:#fff;color:{INK};font-size:52px;opacity:0">{icon("plane", 50, INK, 2.6)} ¡CUIDADO!</div>')
    t_y3, t_via, t_cui, t_vie, t_ins, t_ale, t_sue, t_apr, t_pul = (P("y", 3), P("viaje"), P("cuidado"), P("vietnam"), P("insulto"), P("alemania"),
                                                                   P("suerte", 3), P("apretando"), P("pulgares"))
    travel(t_y3 - 0.3, F(3, 1), 3, 1630, dur=0.7)
    hide_mile(2, t_y3 + 0.2)
    pop("#via", t_via, sound="pop2")
    js(f'tl.to("#via", {{rotation:-4, duration:0.1, yoyo:true, repeat:3}}, {t_cui:.3f});')
    slide_in("#vn", t_vie - 0.2, dy=-60, sound="pop")
    js(f'tl.fromTo("#h3h", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_vie:.3f});')
    js(f'tl.fromTo("#vnx", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_ins - 0.1:.3f});')
    pop("#ins", t_ins, sound="golpe", vol=0.35)
    slide_in("#de", t_ale - 0.2, dy=-60, sound="pop")
    js(f'tl.fromTo("#fs", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_ale:.3f});')
    pop("#sue", t_sue, sound="check")
    js(f'tl.to("#fs", {{scale:0.9, duration:0.12, yoyo:true, repeat:5}}, {t_apr:.3f}); tl.to("#fs-th", {{fill:"#d99a66", duration:0.2}}, {t_pul:.3f});')
    sfx(t_apr, "click", 0.3)


# ================================================================= CIERRE + COMENTARIOS
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    hand_cross("h4", fx + 330, fy + 520, 300, z=6)
    add(f'<div id="hrt" style="{css_box(fx + 620, fy + 560, 200, 200, 7)}opacity:0">{icon("heart", 190, BAD, 2.4).replace("<svg", f"<svg fill=\"{BAD}\"")}</div>')
    add(f'<div id="qz" class="pill" style="{css_box(fx + 120, fy + 900, None, None, 9)}background:{ACC};color:{INK};font-size:58px;opacity:0">QUIZÁ CÓMO TE SIENTES</div>')
    add(f'<div id="nsu" class="pill" style="{css_box(fx + 160, fy + 560, None, None, 9)}background:#334155;color:#fff;font-size:46px;opacity:0;text-decoration:line-through">SUERTE</div>')
    cta = "Yo siempre antes de…"
    card("cbox", fx + 40, fy + 20, 880, 440, f'''
      <div style="position:absolute;left:40px;top:34px;display:flex;align-items:center;gap:22px">{icon("message-circle", 84, INK, 2.4)}
        <span style="font:900 68px {FONT};color:{INK}">Comentarios</span></div>
      <div style="position:absolute;left:40px;top:150px;font:900 50px {FONT};color:#555">¿Tú cruzas los dedos?</div>
      <div id="ctt" style="position:absolute;left:40px;top:240px;font:800 64px {FONT};color:{INK};white-space:nowrap">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 370, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_asi, t_cam, t_sue4, t_qui, t_sie = P("asi"), P("cambia"), P("suerte", 4), P("quiza"), P("sientes")
    travel(t_asi - 0.3, F(3, 0), 3, 570, dur=0.7)
    js(f'tl.fromTo("#h4", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_asi:.3f});')
    pop("#nsu", t_sue4 - 0.1, sound="pop2")
    js(f'tl.fromTo("#hrt", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(3)"}}, {t_qui:.3f}); tl.to("#hrt", {{scale:1.12, duration:0.2, yoyo:true, repeat:3}}, {t_sie:.3f});')
    pop("#qz", t_sie - 0.1, sound="check")
    t_tu, t_cru, t_cue, t_com = P("tu", 2), P("cruzas", 2), P("cuentamelo"), P("comentarios")
    slide_in("#cbox", t_tu - 0.2, dy=-80)
    js(f'tl.to("#h4-mid", {{rotation:{MID_R - 8}, svgOrigin:"167 200", duration:0.2, yoyo:true, repeat:1}}, {t_cru:.3f});')
    type_on("#ctt .kc", len(cta), t_cru + 0.2, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_cue:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.2:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.2:.3f});')
    sfx(t_com + 0.2, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.1:.3f});')
    cam(E("comentarios") + 0.05, (0, 100, 2200, 5200), dur=0.45, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.htitle {{ font-size:76px; top:28px; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; gap:12px; }}
.halo {{ border-radius:50%; background:radial-gradient(circle, rgba(250,204,21,0.45), rgba(250,204,21,0) 65%); }}
.handw svg {{ filter:drop-shadow(0 20px 30px rgba(0,0,0,0.45)); }}
.bigq {{ border-radius:30px; background:{ACC}; color:{INK}; font:900 120px {FONT}; text-align:center; line-height:170px; white-space:nowrap; }}
.bigstamp {{ border:14px solid {BAD}; border-radius:24px; color:{BAD}; background:rgba(255,255,255,0.92); font:900 110px {FONT}; text-align:center; line-height:170px; transform:rotate(-10deg); white-space:nowrap; }}
.bigstamp.sm {{ font-size:80px; line-height:104px; border-width:10px; }}
.eqs {{ font:900 120px {FONT}; color:#fff; text-align:center; line-height:120px; }}
.xray {{ border-radius:50%; border:10px dashed #38bdf8; background:rgba(56,189,248,0.12); }}
.xrl {{ position:absolute; left:0; right:0; top:-70px; text-align:center; font:900 46px {FONT}; color:#38bdf8; }}
.bub2 {{ border-radius:40px; background:#fff; color:{INK}; font:900 58px {FONT}; text-align:center; line-height:160px; white-space:nowrap; }}
.def {{ width:90px; height:60px; border-radius:8px; overflow:hidden; display:flex; flex-direction:column; margin-right:14px; border:3px solid #fff; }}
.def i {{ flex:1; }}
.green {{ border-radius:40px; background:radial-gradient(ellipse at 60% 30%, #4ade80, #15803d 70%); border:8px solid #166534; }}
.hole {{ position:absolute; left:640px; top:100px; width:120px; height:60px; border-radius:50%; background:#052e16; box-shadow:inset 0 8px 0 rgba(0,0,0,0.5); }}
.hole.big {{ position:absolute; left:auto; top:auto; background:#052e16; border:8px solid #4ade80; }}
.gflag {{ position:absolute; left:695px; top:-90px; width:10px; height:200px; background:#fff; }}
.gflag::after {{ content:""; position:absolute; left:10px; top:0; width:90px; height:60px; background:{BAD}; clip-path:polygon(0 0, 100% 50%, 0 100%); }}
.gball {{ border-radius:50%; background:radial-gradient(circle at 35% 30%, #fff, #e2e8f0 60%, #94a3b8); display:flex; align-items:center; justify-content:center; box-shadow:0 10px 20px rgba(0,0,0,0.4); }}
.vbar2 {{ border-radius:40px; border:8px solid #e2e8f0; background:rgba(255,255,255,0.06); overflow:hidden; }}
.vbf2 {{ position:absolute; left:0; right:0; bottom:0; height:100%; background:linear-gradient({GOOD},#15803d); }}
.tl2 {{ font:900 46px {FONT}; color:#fff; text-align:center; }}
.ctit {{ position:absolute; left:0; right:0; top:30px; display:flex; align-items:center; justify-content:center; font:900 54px {FONT}; color:{INK}; }}
.flagvn {{ width:90px; height:60px; border-radius:8px; background:#da251d; position:relative; margin-right:14px; }}
.flagvn i {{ position:absolute; left:30px; top:15px; width:30px; height:30px; background:#ffcd00; clip-path:polygon(50% 0, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%); }}
.pubb {{ position:absolute; right:40px; bottom:36px; padding:14px 46px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 66px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_cruz()
    scene_deseo()
    scene_mentiras()
    scene_golf()
    scene_replica()
    scene_viaje()
    scene_final()
