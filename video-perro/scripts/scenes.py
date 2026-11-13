"""Escenas del vídeo «Lo que un perro hace en tu cabeza». Un solo mundo: un camino en zigzag
(mirada -> felicidad -> cortisol -> responsabilidad -> rutina -> madurez -> salud -> no es un capricho)."""
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
DOG_FILL, DOG_LINE = "#c08a52", "#3b2412"


def dog(did, x, y, size, z=6, flip=False):
    """Perro de perfil (mira a la derecha; flip = mira a la izquierda). Cola y cabeza con id para animarlas."""
    fl = ' transform="translate(300,0) scale(-1,1)"' if flip else ""
    leg = "#8a5a2b"
    svg = f'''<svg viewBox="0 0 300 260" width="100%" height="100%" style="overflow:visible"><g{fl}>
      <ellipse cx="150" cy="248" rx="110" ry="10" fill="#000" opacity="0.3"/>
      <g id="{did}-tail"><path d="M 70 130 Q 30 110 34 60" stroke="{DOG_FILL}" stroke-width="22" fill="none" stroke-linecap="round"/></g>
      <rect x="80" y="170" width="26" height="76" rx="13" fill="{leg}"/><rect x="190" y="170" width="26" height="76" rx="13" fill="{leg}"/>
      <ellipse cx="145" cy="150" rx="88" ry="54" fill="{DOG_FILL}"/>
      <rect x="105" y="172" width="26" height="74" rx="13" fill="{DOG_FILL}"/><rect x="212" y="172" width="26" height="74" rx="13" fill="{DOG_FILL}"/>
      <g id="{did}-head">
        <circle cx="232" cy="92" r="52" fill="{DOG_FILL}"/>
        <ellipse cx="276" cy="112" rx="32" ry="22" fill="#e9c49a"/>
        <circle cx="300" cy="104" r="10" fill="{DOG_LINE}"/>
        <path d="M 270 128 Q 282 140 294 128" stroke="{DOG_LINE}" stroke-width="5" fill="none" stroke-linecap="round"/>
        <ellipse cx="282" cy="140" rx="9" ry="12" fill="#f472b6"/>
        <circle cx="246" cy="80" r="8" fill="{DOG_LINE}"/><circle cx="248" cy="77" r="2.5" fill="#fff"/>
        <ellipse cx="200" cy="82" rx="20" ry="40" fill="{DOG_LINE}" opacity="0.85" transform="rotate(18 200 82)"/>
      </g></g></svg>'''
    add(f'<div id="{did}" class="dogw" style="{css_box(x, y, size, size * 260 / 300, z)}">{svg}</div>')


def dog_life(did, t0, t1):
    n = int((t1 - t0) / 0.25)
    js(f'tl.fromTo("#{did}-tail", {{rotation:-14}}, {{rotation:14, svgOrigin:"70 130", duration:0.25, yoyo:true, repeat:{n}, ease:"sine.inOut", immediateRender:false}}, {t0:.3f});')
    js(f'tl.to("#{did}-head", {{rotation:-4, svgOrigin:"200 130", duration:0.9, yoyo:true, repeat:{int((t1 - t0) / 0.9)}, ease:"sine.inOut"}}, {t0:.3f});')


def tube(tid, x, y, label, color, z=6):
    add(f'''<div id="{tid}" class="tube" style="{css_box(x, y, 170, 470, z)}">
      <div id="{tid}-liq" class="liq" style="background:{color}"></div></div>
      <div id="{tid}-lab" class="tlab2" style="{css_box(x - 40, y + 480, 250, 70, z)}">{label}</div>''')


def bar(bid, x, y, w, label, color, z=6):
    add(f'''<div id="{bid}" class="hbar" style="{css_box(x, y, w, 120, z)}">
      <div class="hbl">{label}</div><div class="hbt"><div id="{bid}-f" class="hbf" style="background:{color}"></div></div></div>''')


# ================================================================= MUNDO
MILES = [("Japón · 2015", 0, 1630), ("El día a día", 1, 570), ("Crecer", 2, 1630), ("3,8 millones", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#f472b6"/><stop offset="0.5" stop-color="#facc15"/><stop offset="1" stop-color="#22c55e"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 240, ROAD[r] + 34, 480, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= GANCHO: LA MIRADA
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    add(character("own0", "g1", fx + 250, fl, 1.25, z=6))
    dog("dog0", fx + 520, fl - 312, 380, z=6, flip=True)
    add(f'''<svg id="beam0" data-layout-ignore style="{css_box(fx + 250, fy + 500, 520, 120, 7)}overflow:visible;opacity:0" viewBox="0 0 520 120">
      <path d="M 20 70 Q 260 -30 500 70" stroke="{ACC}" stroke-width="12" fill="none" stroke-dasharray="20 14" stroke-linecap="round"/></svg>''')
    add(f'<div id="brain" class="brainw" style="{css_box(fx + 330, fy + 60, 300, 300, 8)}">{icon("brain", 260, "#f9a8d4", 2.2).replace("<svg", "<svg fill=\"#831843\"")}</div>')
    add(f'<div id="lit" class="pill" style="{css_box(fx + 600, fy + 150, None, None, 9)}background:{ACC};color:{INK};font-size:58px;opacity:0">¡LITERAL!</div>')
    cam(0, F(0, 0), whoosh=False)
    life("own0", 0, G.DUR, 1)
    dog_life("dog0", 0, G.DUR)
    # primer segundo: se cruzan las miradas y salta la chispa
    js('tl.fromTo("#own0", {x:-120}, {x:0, duration:0.5, ease:"power3.out"}, 0); tl.fromTo("#dog0", {x:140}, {x:0, duration:0.5, ease:"power3.out"}, 0);')
    js('tl.fromTo("#beam0", {opacity:0}, {opacity:1, duration:0.2}, 0.35); tl.fromTo("#beam0 path", {strokeDashoffset:0}, {strokeDashoffset:-136, duration:0.8, repeat:5, ease:"none"}, 0.35);')
    js('tl.fromTo("#brain", {scale:0.4, opacity:0.4}, {scale:1, opacity:1, duration:0.45, ease:"back.out(2.5)"}, 0.1);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.4, "pop", 0.4)
    t_ojo, t_cam, t_qui, t_no, t_hab = P("ojos"), P("cambia"), P("quimica"), P("no"), P("hablar")
    js(f'tl.to(Q("own0","head"), {{rotation:6, svgOrigin:PIV.head, duration:0.3}}, {t_ojo:.3f});')
    js(f'tl.to("#brain svg", {{filter:"drop-shadow(0 0 40px #f472b6)", duration:0.4}}, {t_cam:.3f});')
    js(f'tl.to("#brain", {{scale:1.12, duration:0.2, yoyo:true, repeat:3}}, {t_qui:.3f});')
    hearts("hh0-", fx + 480, fy + 380, 5, t_qui, spread=360, rise=260)
    stamp("#lit", t_hab - 0.1)
    sfx(t_hab, "golpe", 0.35)


# ================================================================= 1 · LA FELICIDAD (OXITOCINA)
def scene_felicidad():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "LA FELICIDAD", color="#ec4899", txt="#fff")
    yr, yh = roller("y15", "0000", 64, "#fff")
    add(f'<div id="jp" class="cnt" style="{css_box(fx + 40, fy + 180, 380, 120, 8)}background:{INK};opacity:0"><span class="jpf"><i></i></span>{yr}</div>')
    add(f'<div id="oxi" class="pill" style="{css_box(fx + 450, fy + 200, None, None, 8)}background:#ec4899;color:#fff;font-size:52px;opacity:0">{icon("heart-handshake", 50, "#fff", 2.6)} OXITOCINA</div>')
    tube("tb1", fx + 80, fy + 340, "PERRO", "#f472b6")
    tube("tb2", fx + 320, fy + 340, "DUEÑO", "#f472b6")
    add(f'<div id="mb" class="pill" style="{css_box(fx + 530, fy + 520, None, None, 8)}background:#fff;color:{INK};font-size:42px;opacity:0">{icon("baby", 42, INK, 2.6)} MADRE·BEBÉ</div>')
    add(f'<div id="eqm" class="eqm" style="{css_box(fx + 560, fy + 380, 220, 120, 8)}opacity:0">=</div>')
    t_uno, t_fel, t_est, t_jap, t_oxi, t_vin, t_per, t_due = (P("uno"), P("felicidad"), P("estudio"), P("japones"), P("oxitocina"), P("vinculo"),
                                                            P("perros"), P("duenos"))
    travel(t_uno - 0.25, F(0, 1), 0, 1630, dur=0.6)
    header_in("h1", t_uno, t_fel)
    pop("#jp", t_est, sound=None)
    roll_set("y15", "0000", yh)
    roll_to("y15", "2015", yh, t_jap, dur=0.5)
    pop("#oxi", t_oxi, sound="pop2")
    js(f'tl.to("#oxi", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_vin:.3f});')
    js(f'tl.fromTo("#tb1, #tb1-lab", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_per:.3f});')
    js(f'tl.fromTo("#tb2, #tb2-lab", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_due:.3f});')
    sfx(t_per, "pop2", 0.25)
    sfx(t_due, "pop2", 0.25)
    js('tl.set("#tb1-liq, #tb2-liq", {scaleY:0.18, transformOrigin:"50% 100%"}, 0);')
    t_sub, t_dos, t_cir, t_mad, t_beb = P("subia"), P("dos"), P("circuito"), P("madre"), P("bebe")
    js(f'tl.to("#tb1-liq, #tb2-liq", {{scaleY:0.85, duration:0.8, ease:"power2.out"}}, {t_sub:.3f});')
    sfx(t_sub, "check", 0.35)
    hearts("hh1-", fx + 250, fy + 420, 4, t_dos, spread=320, rise=240)
    js(f'tl.fromTo("#eqm", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_cir:.3f});')
    pop("#mb", t_mad, sound="pop")
    js(f'tl.to("#mb", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_beb:.3f});')


# ================================================================= EL CORTISOL
def scene_cortisol():
    fx, fy, fw, fh = F(1, 1)
    tm, th = roller("tmr", "00", 110, "#fff")
    add(f'<div id="tmb" class="cnt" style="{css_box(fx + 40, fy + 40, 440, 180, 8)}background:{INK};opacity:0">{icon("timer", 90, ACC, 2.6)}{tm}<span class="mins">MIN</span></div>')
    dog("dog1", fx + 120, fy + 520, 420, z=6)
    add(f'<div id="hand1" style="{css_box(fx + 260, fy + 420, 200, 200, 8)}opacity:0">{icon("hand", 190, "#7c2d12", 2.2).replace("<svg", "<svg fill=\"#f3cdab\"")}</div>')
    add(f'''<div id="cbar" class="vbar" style="{css_box(fx + 680, fy + 260, 200, 720, 6)}opacity:0">
      <div id="cbar-f" class="vbf"></div></div>
      <div id="cbl" class="tlab2" style="{css_box(fx + 620, fy + 160, 320, 80, 7)}opacity:0">CORTISOL</div>''')
    add(f'<div id="stress" class="pill" style="{css_box(fx + 560, fy + 1000 - 100, None, None, 9)}background:{GOOD_BG};color:#fff;font-size:48px;opacity:0">{icon("trending-down", 46, "#fff", 2.6)} ESTRÉS</div>')
    t_aca, t_sol, t_die, t_min, t_baj, t_cor, t_est = P("acariciar"), P("solo"), P("diez"), P("minutos"), P("baja"), P("cortisol"), P("estres")
    travel(t_aca - 0.3, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_aca + 0.2)
    dog_life("dog1", 0, G.DUR)
    js(f'tl.fromTo("#hand1", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.3}}, {t_aca:.3f});')
    js(f'tl.to("#hand1", {{x:120, duration:0.45, yoyo:true, repeat:{int((P("hormona", 2) - t_aca) / 0.45)}, ease:"sine.inOut"}}, {t_aca + 0.3:.3f});')
    pop("#tmb", t_sol, sound=None)
    roll_set("tmr", "00", th)
    roll_to("tmr", "10", th, t_die - 0.1, dur=0.5)
    sfx(t_die, "tic-rodillo", 0.3)
    js(f'tl.to("#tmb", {{scale:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_min:.3f});')
    js(f'tl.fromTo("#cbar, #cbl", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_baj - 0.3:.3f});')
    js(f'tl.fromTo("#cbar-f", {{scaleY:0.95, backgroundColor:"{BAD}"}}, {{scaleY:0.35, backgroundColor:"{GOOD}", transformOrigin:"50% 100%", duration:1.1, ease:"power2.inOut", immediateRender:false}}, {t_baj:.3f});')
    js(f'tl.set("#cbar-f", {{scaleY:0.95, backgroundColor:"{BAD}", transformOrigin:"50% 100%"}}, 0);')
    sfx(t_baj, "whoosh-corto", 0.3)
    pop("#stress", t_est - 0.1, sound="check")
    hearts("hh2-", fx + 300, fy + 560, 3, t_cor, spread=240, rise=220)


# ================================================================= 2 · LA RESPONSABILIDAD
def scene_resp():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    header("h2", fx, fy, "2", "LA RESPONSABILIDAD", color="#2563eb", txt="#fff")
    items = [("footprints", "PASEO"), ("bone", "COMIDA"), ("stethoscope", "CUIDADOS")]
    rows = "".join(f'''<div class="agr" style="top:{110 + i * 110}px"><span id="ck{i}" class="agk">{icon("check", 46, "#fff", 3.6)}</span>
        {icon(ic, 56, INK, 2.4)}<span class="agt">{tx}</span></div>''' for i, (ic, tx) in enumerate(items))
    card("agenda", fx + 40, fy + 180, 520, 470, f'<div style="position:absolute;left:30px;top:24px;font:900 54px {FONT};color:{INK}">HOY</div>{rows}')
    add(character("own1", "g1", fx + 700, fl, 1.0, z=6))
    dog("dog2", fx + 760, fl - 164, 200, z=7, flip=True)
    add(f'<div id="umb" style="{css_box(fx + 560, fl - 640, 280, 280, 8)}opacity:0">{icon("umbrella", 270, "#1e3a8a", 2.4).replace("<svg", "<svg fill=\"#3b82f6\"")}</div>')
    add(f'<div id="cld" style="{css_box(fx + 580, fy + 170, 340, 240, 4)}opacity:0">{icon("cloud-lightning", 300, "#94a3b8", 2.0).replace("<svg", "<svg fill=\"#334155\"")}</div>')
    for k in range(8):
        add(f'<div id="rd{k}" class="drop" data-layout-ignore style="{css_box(fx + 80 + k * 110, fy + 260, 10, 60, 5)}opacity:0"></div>')
    add(f'<div id="noex" class="pill" style="{css_box(fx + 60, fy + 700, None, None, 8)}background:{BAD};color:#fff;font-size:52px;opacity:0">{icon("ban", 50, "#fff", 2.6)} SIN EXCUSAS</div>')
    t_dos, t_res, t_per, t_exc, t_sac, t_com, t_cui, t_llu, t_tru = (P("dos", 2), P("responsabilidad"), P("perro", 2), P("excusas"), P("sacarlo"),
                                                                   P("comer"), P("cuidarlo"), P("llueva"), P("truene"))
    travel(t_dos - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h2", t_dos, t_res)
    life("own1", 0, G.DUR, 2)
    dog_life("dog2", 0, G.DUR)
    js(f'tl.fromTo("#own1, #dog2", {{opacity:0, x:80}}, {{opacity:1, x:0, duration:0.4}}, {t_per:.3f});')
    stamp("#noex", t_exc)
    sfx(t_exc, "golpe", 0.3)
    slide_in("#agenda", t_exc + 0.3, dy=60, sound="papel", vol=0.3)
    for i, t in enumerate([t_sac, t_com, t_cui]):
        js(f'tl.fromTo("#ck{i}", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.25, ease:"back.out(3)"}}, {t:.3f});')
        sfx(t, "check", 0.3)
    js(f'tl.to("#noex", {{opacity:0, duration:0.3}}, {t_sac:.3f});')
    js(f'tl.fromTo("#cld", {{opacity:0, y:-60}}, {{opacity:1, y:0, duration:0.4}}, {t_llu - 0.1:.3f});')
    for k in range(8):
        js(f'tl.fromTo("#rd{k}", {{opacity:0, y:0}}, {{opacity:0.9, y:700, duration:0.6, repeat:4, ease:"power1.in", immediateRender:false}}, {t_llu + k * 0.07:.3f});')
    js(f'tl.to("#cld", {{x:8, duration:0.06, yoyo:true, repeat:5}}, {t_tru:.3f});')
    shake(t_tru, 10)
    sfx(t_tru, "golpe", 0.35)
    js(f'tl.fromTo("#umb", {{opacity:0, scale:0.3, rotation:-30}}, {{opacity:1, scale:1, rotation:0, duration:0.4, ease:"back.out(2)"}}, {t_tru + 0.1:.3f});')
    js(f'walk("own1", {t_tru + 0.2:.3f}, {t_tru + 1.0:.3f}, 0.14);')


# ================================================================= LA RUTINA
def scene_rutina():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    add(f'<div id="win" class="wnd" style="{css_box(fx + 560, fy + 60, 360, 360, 3)}"><div id="sun" class="sun"></div></div>')
    add(f'<div id="bed" class="bed" style="{css_box(fx + 40, fl - 200, 600, 200, 4)}"></div>')
    add(character("own2", "g1", fx + 330, fl - 90, 1.0, z=5))
    dog("dog3", fx + 640, fl - 213, 260, z=7, flip=True)
    add(f'<div id="alarm" style="{css_box(fx + 60, fy + 200, 220, 220, 8)}opacity:0">{icon("alarm-clock", 210, "#fff", 2.4)}</div>')
    add(f'<div id="ad" class="pill" style="{css_box(fx + 40, fy + 60, None, None, 8)}background:#475569;color:#fff;font-size:48px;opacity:0">ANSIEDAD · DEPRESIÓN</div>')
    add(f'<div id="rut" class="pill" style="{css_box(fx + 300, fy + 260, None, None, 8)}background:{GOOD_BG};color:#fff;font-size:52px;opacity:0">{icon("repeat", 50, "#fff", 2.6)} RUTINA</div>')
    add(f'<div id="mot" class="pill" style="{css_box(fx + 300, fy + 380, None, None, 8)}background:{ACC};color:{INK};font-size:52px;opacity:0">{icon("sparkles", 50, INK, 2.6)} UN MOTIVO</div>')
    t_y5, t_ans, t_dep, t_cue, t_rut, t_mot, t_lev = P("y", 5), P("ansiedad"), P("depresion"), P("cuentan"), P("rutina"), P("motivo"), P("levantarse")
    travel(t_y5 - 0.3, F(2, 0), 2, 570, dur=0.7)
    hide_mile(1, t_y5 + 0.2)
    life("own2", 0, G.DUR, 3)
    dog_life("dog3", 0, G.DUR)
    # tumbado en la cama
    js(f'tl.set("#own2", {{rotation:-90, transformOrigin:"50% 90%", y:40, x:110}}, 0);')
    js(f'tl.to(Q("own2","eyes"), {{scaleY:0.15, svgOrigin:PIV.eyes, duration:0.2}}, {t_y5:.3f});')
    pop("#ad", t_ans - 0.1, sound=None)
    js(f'tl.fromTo("#sun", {{y:200}}, {{y:200, duration:0.1}}, 0);')
    js(f'tl.fromTo("#alarm", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_cue:.3f});')
    js(f'tl.to("#alarm", {{rotation:12, duration:0.06, yoyo:true, repeat:13}}, {t_cue + 0.3:.3f});')
    sfx(t_cue + 0.3, "tic-rodillo", 0.35)
    js(f'tl.fromTo("#dog3", {{x:0, y:0}}, {{x:-220, y:-60, duration:0.35, ease:"power2.out"}}, {t_rut - 0.2:.3f}); tl.to("#dog3", {{y:0, duration:0.25, ease:"bounce.out"}}, {t_rut + 0.15:.3f});')
    pop("#rut", t_rut, sound="pop")
    pop("#mot", t_mot, sound="pop2")
    js(f'tl.to("#own2", {{rotation:0, y:-60, x:0, duration:0.5, ease:"back.out(1.6)"}}, {t_lev:.3f}); tl.to(Q("own2","eyes"), {{scaleY:1, svgOrigin:PIV.eyes, duration:0.2}}, {t_lev:.3f});')
    js(f'tl.to("#sun", {{y:0, duration:0.8, ease:"power2.out"}}, {t_lev:.3f});')
    sfx(t_lev, "whoosh-corto", 0.3)


# ================================================================= 3 · LA MADUREZ
def scene_madurez():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h3", fx, fy, "3", "LA MADUREZ", color=GOOD_BG, txt="#fff")
    add(f'''<div id="yo" style="{css_box(fx + 60, fy + 200, 420, 200, 7)}opacity:0">
      <div class="yob">YO</div><div id="yoar" class="yoar">{icon("arrow-right", 150, ACC, 3.2)}</div></div>''')
    dog("dog4", fx + 560, fy + 180, 260, z=6, flip=True)
    add(f'<div id="otro" class="pill" style="{css_box(fx + 580, fy + 450, None, None, 8)}background:{ACC};color:{INK};font-size:52px;opacity:0">PRIMERO ÉL</div>')
    add(character("kid", "g3", fx + 170, fl, 0.8, z=6))
    dog("dog5", fx + 260, fl - 139, 170, z=6, flip=True)
    bar("bem", fx + 470, fy + 640, 450, "EMPATÍA", "#ec4899")
    bar("bau", fx + 470, fy + 820, 450, "AUTOESTIMA", GOOD)
    t_tres, t_mad, t_cui, t_dep, t_obl, t_otr, t_ant = P("tres"), P("madurez"), P("cuidar"), P("depende"), P("obliga"), P("otro"), P("antes")
    travel(t_tres - 0.3, F(2, 1), 2, 1630, dur=0.7)
    header_in("h3", t_tres, t_mad)
    dog_life("dog4", 0, G.DUR)
    dog_life("dog5", 0, G.DUR)
    js(f'tl.fromTo("#yo", {{opacity:0, x:-60}}, {{opacity:1, x:0, duration:0.35}}, {t_cui:.3f});')
    js(f'tl.fromTo("#yoar", {{rotation:180}}, {{rotation:180, duration:0.1}}, {t_cui:.3f});')
    js(f'tl.fromTo("#dog4", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_dep:.3f});')
    sfx(t_dep, "pop2", 0.3)
    js(f'tl.to("#yoar", {{rotation:0, duration:0.6, ease:"back.out(2)"}}, {t_otr - 0.3:.3f});')
    sfx(t_otr - 0.3, "whoosh-corto", 0.3)
    pop("#otro", t_ant, sound="check")
    t_nin, t_rel, t_emp, t_aut = P("ninos"), P("relacionan"), P("empatia"), P("autoestima")
    life("kid", 0, G.DUR, 7)
    js(f'tl.fromTo("#kid, #dog5", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_nin - 0.1:.3f}); wave("kid", {t_nin + 0.3:.3f}, {t_aut + 0.8:.3f});')
    js(f'tl.fromTo("#bem, #bau", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_rel:.3f});')
    js('tl.set("#bem-f, #bau-f", {scaleX:0.2, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to("#bem-f", {{scaleX:0.85, duration:0.6, ease:"back.out(1.6)"}}, {t_emp:.3f});')
    js(f'tl.to("#bau-f", {{scaleX:0.8, duration:0.6, ease:"back.out(1.6)"}}, {t_aut:.3f});')
    sfx(t_emp, "check", 0.3)
    sfx(t_aut, "check", 0.3)


# ================================================================= DE REGALO: LA SALUD
def scene_salud():
    fx, fy, fw, fh = F(3, 1)
    people = "".join(f'<div class="pp" style="left:{(i % 12) * 74}px;top:{(i // 12) * 84}px">{icon("user", 60, "#94a3b8", 2.6)}</div>' for i in range(48))
    add(f'<div id="crowd" style="{css_box(fx + 40, fy + 40, 880, 340, 4)}">{people}</div>')
    mm, mh = roller("mil", "0,0", 96, "#fff")
    add(f'<div id="mlb" class="cnt" style="{css_box(fx + 220, fy + 400, 520, 150, 8)}background:{INK};opacity:0">{icon("users", 80, "#fff", 2.6)}{mm}<span class="mins">M</span></div>')
    add(f'<div id="hrt" style="{css_box(fx + 60, fy + 600, 330, 330, 6)}opacity:0">{icon("heart-pulse", 320, "#fecaca", 2.2).replace("<svg", "<svg fill=\"#b91c1c\"")}</div>')
    pc, ph = roller("p24", "00", 120, "#fff")
    add(f'<div id="pcb" class="cnt" style="{css_box(fx + 430, fy + 640, 460, 190, 8)}background:{GOOD_BG};opacity:0"><span class="big">−</span>{pc}<span class="big">%</span></div>')
    add(f'<div id="rsk" class="pill" style="{css_box(fx + 440, fy + 860, None, None, 8)}background:#fff;color:{INK};font-size:46px;opacity:0">RIESGO DE MUERTE</div>')
    add(f'<div id="aso" class="pill" style="{css_box(fx + 440, fy + 950, None, None, 8)}background:#334155;color:#fff;font-size:40px;opacity:0">ASOCIACIÓN, NO CAUSA</div>')
    t_y8, t_reg, t_cas, t_mil, t_ten, t_aso, t_24, t_rie, t_mor = (P("y", 8), P("regalo"), P("casi"), P("millones"), P("tener"), P("asocio"), P("24"),
                                                                  P("riesgo"), P("morir"))
    travel(t_y8 - 0.3, F(3, 1), 3, 1630, dur=0.7)
    hide_mile(2, t_y8 + 0.2)
    js(f'tl.fromTo("#crowd .pp", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.25, stagger:0.015, ease:"back.out(2)"}}, {t_reg:.3f});')
    sfx(t_reg, "pop2", 0.3)
    pop("#mlb", t_cas, sound=None)
    roll_set("mil", "0,0", mh)
    roll_to("mil", "3,8", mh, t_mil - 0.2, dur=0.6)
    js(f'tl.fromTo("#hrt", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_ten:.3f});')
    js(f'tl.to("#hrt", {{scale:1.08, duration:0.18, yoyo:true, repeat:9}}, {t_ten + 0.4:.3f});')
    pop("#aso", t_aso, sound=None)
    pop("#pcb", t_24 - 0.3, sound="pop")
    roll_set("p24", "00", ph)
    roll_to("p24", "24", ph, t_24 - 0.2, dur=0.5)
    sfx(t_24, "check", 0.4)
    pop("#rsk", t_rie, sound=None)
    js(f'tl.to("#pcb", {{scale:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_mor:.3f});')


# ================================================================= NO ES UN CAPRICHO + COMENTARIOS
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    fl = floor(3)
    dog("dog6", fx + 260, fl - 361, 440, z=6)
    add(f'<div id="capr" class="pill" style="{css_box(fx + 80, fy + 500, None, None, 9)}background:{BAD};color:#fff;font-size:60px;opacity:0">{icon("ban", 56, "#fff", 2.6)} NO ES UN CAPRICHO</div>')
    add(f'<div id="vida" class="pill" style="{css_box(fx + 180, fy + 640, None, None, 9)}background:#fff;color:{INK};font-size:56px;opacity:0">{icon("heart", 52, BAD, 2.6).replace("<svg", f"<svg fill=\"{BAD}\"")} ES UNA VIDA</div>')
    cta = "Desde que tengo perro…"
    card("cbox", fx + 40, fy + 30, 880, 440, f'''
      <div style="position:absolute;left:40px;top:34px;display:flex;align-items:center;gap:22px">{icon("message-circle", 84, INK, 2.4)}
        <span style="font:900 68px {FONT};color:{INK}">Comentarios</span></div>
      <div style="position:absolute;left:40px;top:150px;font:900 50px {FONT};color:#555">¿Qué ha cambiado en ti?</div>
      <div id="ctt" style="position:absolute;left:40px;top:240px;font:800 64px {FONT};color:{INK};white-space:nowrap">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 380, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_per, t_ojo, t_cap, t_vid, t_dep = P("pero"), P("ojo"), P("capricho"), P("vida"), P("depende", 2)
    travel(t_per - 0.3, F(3, 0), 3, 570, dur=0.7)
    dog_life("dog6", 0, G.DUR)
    js(f'tl.fromTo("#dog6", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_per:.3f});')
    js(f'tl.to("#dog6", {{scale:1.06, duration:0.2, yoyo:true, repeat:1}}, {t_ojo:.3f});')
    stamp("#capr", t_cap)
    sfx(t_cap, "golpe", 0.4)
    pop("#vida", t_vid, sound="pop")
    js(f'tl.to("#vida", {{scale:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_dep:.3f});')
    t_qha, t_cue, t_com = P("cambiado"), P("cuentamelo"), P("comentarios")
    js(f'tl.to("#capr, #vida", {{y:420, duration:0.5, ease:"power2.inOut"}}, {t_qha - 0.3:.3f});')
    js(f'tl.to("#dog6", {{y:120, scale:0.75, transformOrigin:"50% 100%", duration:0.5}}, {t_qha - 0.3:.3f});')
    slide_in("#cbox", t_qha - 0.2, dy=-80)
    type_on("#ctt .kc", len(cta), t_qha + 0.2, t_com)
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
.big {{ font:900 110px {FONT}; color:#fff; }}
.mins {{ font:900 56px {FONT}; color:#fff; margin-left:10px; }}
.brainw {{ display:flex; align-items:center; justify-content:center; border-radius:50%; background:radial-gradient(circle, rgba(244,114,182,0.35), rgba(244,114,182,0) 70%); }}
.jpf {{ width:90px; height:60px; border-radius:8px; background:#fff; position:relative; margin-right:14px; }}
.jpf i {{ position:absolute; left:27px; top:12px; width:36px; height:36px; border-radius:50%; background:#dc2626; }}
.tube {{ border-radius:20px 20px 85px 85px; border:8px solid #e2e8f0; background:rgba(255,255,255,0.06); overflow:hidden; opacity:0; }}
.liq {{ position:absolute; left:0; right:0; bottom:0; height:100%; }}
.tlab2 {{ font:900 50px {FONT}; color:#fff; text-align:center; opacity:0; }}
.eqm {{ font:900 120px {FONT}; color:{ACC}; text-align:center; line-height:120px; }}
.vbar {{ border-radius:40px; border:8px solid #e2e8f0; background:rgba(255,255,255,0.06); overflow:hidden; }}
.vbf {{ position:absolute; left:0; right:0; bottom:0; height:100%; }}
.agr {{ position:absolute; left:30px; display:flex; align-items:center; gap:20px; }}
.agk {{ width:64px; height:64px; border-radius:16px; background:{GOOD_BG}; display:flex; align-items:center; justify-content:center; opacity:0; }}
.agt {{ font:900 56px {FONT}; color:{INK}; }}
.drop {{ border-radius:5px; background:#93c5fd; }}
.wnd {{ border-radius:30px; border:14px solid #e2e8f0; background:linear-gradient(#fde68a,#38bdf8); overflow:hidden; }}
.sun {{ position:absolute; left:100px; top:80px; width:140px; height:140px; border-radius:50%; background:#facc15; box-shadow:0 0 60px 20px rgba(250,204,21,0.6); }}
.bed {{ border-radius:30px 30px 10px 10px; background:linear-gradient(#e2e8f0 0 30%, #6366f1 30%); }}
.yob {{ position:absolute; left:0; top:20px; width:170px; height:160px; border-radius:30px; background:#fff; color:{INK}; font:900 80px {FONT}; text-align:center; line-height:160px; }}
.yoar {{ position:absolute; left:200px; top:20px; width:160px; height:160px; display:flex; align-items:center; justify-content:center; }}
.hbar {{ opacity:0; }}
.hbl {{ font:900 50px {FONT}; color:#fff; }}
.hbt {{ position:absolute; left:0; right:0; top:62px; height:50px; border-radius:25px; background:rgba(255,255,255,0.12); overflow:hidden; }}
.hbf {{ position:absolute; left:0; top:0; bottom:0; width:100%; border-radius:25px; }}
.pp {{ position:absolute; width:60px; height:60px; }}
.pubb {{ position:absolute; right:40px; bottom:36px; padding:14px 46px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 66px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_felicidad()
    scene_cortisol()
    scene_resp()
    scene_rutina()
    scene_madurez()
    scene_salud()
    scene_final()
