"""Escenas del vídeo «¿Y si Maite no hubiera tenido un hijo con Sergio?» (IMAGINADO). Un solo mundo: camino en zigzag
(el carrito -> lo que pasó -> Sergio se va -> 1 · el secreto -> 2 · la pareja -> 3 · Sergio -> encuesta)."""
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
def bubble(bid, x, y, w, who, text, col, side="l", z=8, fs=40):
    """Bocadillo de diálogo con el nombre de quien habla. Devuelve el nº de letras (para escribirlo)."""
    add(f'''<div id="{bid}" class="sb {side}" style="{css_box(x, y, w, None, z)}border-color:{col};opacity:0">
      <div class="who" style="background:{col}">{who}</div><div class="sbt" style="font-size:{fs}px">{chars(text, "kc")}</div></div>''')
    return len(text.replace(" ", ""))


def talk(cid, t0, t1):
    n = max(1, 2 * int((t1 - t0) / 0.24) - 1)
    js(f'tl.fromTo(Q("{cid}","mouth"), {{scaleY:1}}, {{scaleY:2.4, svgOrigin:"120 134", duration:0.12, yoyo:true, repeat:{n}, immediateRender:false}}, {t0:.3f});')


def say(bid, n, cid, t0, t1, from_x=0):
    js(f'tl.fromTo("#{bid}", {{opacity:0, scale:0.5, x:{from_x}}}, {{opacity:1, scale:1, x:0, duration:0.3, ease:"back.out(2)"}}, {t0 - 0.3:.3f});')
    sfx(t0 - 0.3, "pop", 0.25)
    js(f'typeOn("#{bid} .kc", {t0:.3f}, {t1:.3f});')
    talk(cid, t0, t1)


def tag_imaginado(r, x):
    add(f'<div id="ti{r}{x}" class="mile" data-layout-ignore style="{css_box(x - 260, ROAD[r] + 34, 520, 70, 2)}">CRUCE IMAGINADO</div>')


def building(bid, x, y, w, h, name, wall, win, sign_bg, sign_col, z=3):
    wins = "".join(f'<i class="win" style="left:{40 + c * ((w - 80) // 3)}px;top:{120 + r * 110}px;background:{win}"></i>'
                   for r in range(4) for c in range(3))
    add(f'''<div id="{bid}" class="bld" style="{css_box(x, y, w, h, z)}background:{wall}">
      <div class="bsign" style="background:{sign_bg};color:{sign_col}">{name}</div>{wins}<div class="bdoor"></div></div>''')


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            if (r, c) == (3, 0):
                continue
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#f97316"/><stop offset="0.5" stop-color="#db2777"/><stop offset="1" stop-color="#7c3aed"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for r, x in [(0, 1630), (1, 1630), (1, 570), (2, 570)]:
        tag_imaginado(r, x)


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            if (r, c) == (3, 0):
                continue
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#facc15"/><stop offset="0.5" stop-color="#22c55e"/><stop offset="1" stop-color="#0ea5e9"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')


def chip(cid, x, y, ic, label, bg, col, z=8, fs=46):
    add(f'<div id="{cid}" class="pill" style="{css_box(x, y, None, None, z)}background:{bg};color:{col};font-size:{fs}px;opacity:0">'
        f'{icon(ic, fs, col, 2.6)} {label}</div>')


def coins(cid, x, base, n, z=6, w=150):
    """Montón de monedas (n monedas) apoyado en y=base."""
    html = "".join(f'<i class="coin" style="bottom:{k * 26}px"></i>' for k in range(n))
    add(f'<div id="{cid}" class="coins" data-layout-ignore style="{css_box(x, base - 26 * n - 40, w, 26 * n + 40, z)}">{html}</div>')


def pram(pid, x, y, z=6, sc=1.0):
    """Carrito de bebé con el bebé dentro (ojos grandes)."""
    add(f'''<div id="{pid}" class="pram" data-layout-ignore style="{css_box(x, y, 420 * sc, 380 * sc, z)}transform-origin:50% 100%">
      <svg viewBox="0 0 420 380" width="{420 * sc:.0f}" height="{380 * sc:.0f}" style="overflow:visible">
        <path d="M60 150 Q60 70 150 60 L150 170 Z" fill="#7c3aed"/>
        <rect x="50" y="160" width="300" height="120" rx="50" fill="#a78bfa"/>
        <circle cx="210" cy="150" r="56" fill="#f6d2b4"/>
        <circle cx="190" cy="146" r="13" fill="#fff"/><circle cx="232" cy="146" r="13" fill="#fff"/>
        <circle cx="192" cy="148" r="7" fill="#16161a"/><circle cx="234" cy="148" r="7" fill="#16161a"/>
        <path d="M198 174 Q210 182 222 174" stroke="#6a2e1e" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M350 180 L390 120" stroke="#475569" stroke-width="12" stroke-linecap="round"/>
        <circle cx="110" cy="320" r="40" fill="#1f2937" stroke="#94a3b8" stroke-width="10"/>
        <circle cx="290" cy="320" r="40" fill="#1f2937" stroke="#94a3b8" stroke-width="10"/>
      </svg></div>''')


# ================================================================= GANCHO: el carrito
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    add(character("mt0", "maite", fx + 170, fl, 1.1, z=5))
    add(character("sg0", "sergio", fx + 790, fl, 1.1, z=5))
    pram("pr0", fx + 165, fl - 590, z=6, sc=1.5)
    add(f'<div id="qq" class="qbig" style="{css_box(fx + 330, fy + 230, 300, 300, 9)}opacity:0">?</div>')
    add(f'<div id="img" class="stampbox" style="{css_box(fx + 190, fy + 600, 580, 150, 10)}opacity:0;font-size:84px">IMAGINADO</div>')
    add(f'<div id="lqs" class="pill" style="{css_box(fx + 240, fy + 150, None, None, 8)}background:#0f766e;color:#fff;font-size:50px;opacity:0">LA QUE SE AVECINA</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: el carrito cae de golpe, todo tiembla y el bebé mira a cámara
    js('tl.fromTo("#pr0", {y:-900, rotation:-12, opacity:1}, {y:0, rotation:0, duration:0.45, ease:"power3.in"}, 0);')
    js('tl.to("#pr0", {keyframes:[{scaleY:0.82, scaleX:1.12, duration:0.08},{scaleY:1.05, scaleX:0.97, duration:0.12},{scaleY:1, scaleX:1, duration:0.1}]}, 0.45);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.45, "golpe-climax", 0.5)
    shake(0.45, 22)
    life("mt0", 0, G.DUR, 1)
    life("sg0", 0, G.DUR, 2)
    js('tl.fromTo("#mt0", {opacity:0, x:-200}, {opacity:1, x:0, duration:0.35, ease:"back.out(2)"}, 0.6);')
    js('tl.fromTo("#sg0", {opacity:0, x:200}, {opacity:1, x:0, duration:0.35, ease:"back.out(2)"}, 0.7);')
    js('tilt("mt0", 0.8); tilt("sg0", 0.9);')
    t_ave, t_nun, t_nac = P("avecina"), P("nunca"), P("nacido")
    pop("#lqs", t_ave - 0.4, sound="pop2")
    js(f'tl.to("#lqs", {{opacity:0, duration:0.2}}, {t_nun - 0.3:.3f});')
    # ¿y si nunca hubiera nacido? -> el carrito se desvanece y queda un «?»
    js(f'tl.to("#pr0", {{opacity:0, scale:0.6, filter:"blur(8px)", duration:0.45, ease:"power2.in"}}, {t_nun:.3f});')
    js(f'tl.fromTo("#qq", {{opacity:0, scale:0.3, rotation:-20}}, {{opacity:1, scale:1, rotation:0, duration:0.4, ease:"back.out(2.4)"}}, {t_nun + 0.2:.3f});')
    sfx(t_nun + 0.2, "pop", 0.35)
    stamp("#img", t_nac - 0.25, rot=-6)
    js(f'tl.to(Q("mt0","head"), {{rotation:-10, svgOrigin:PIV.head, duration:0.3}}, {t_nac:.3f}); tl.to(Q("sg0","head"), {{rotation:10, svgOrigin:PIV.head, duration:0.3}}, {t_nac:.3f});')


# ================================================================= LO QUE PASÓ
def scene_paso():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "✓", "LO QUE PASÓ", color="#22c55e")
    add(character("am1", "amador", fx + 160, fl, 1.05, z=5))
    add(character("mt1", "maite", fx + 480, fl, 1.05, z=5))
    add(character("sg1", "sergio", fx + 800, fl, 1.05, z=5))
    for k, (x, n) in enumerate([(fx + 30, "AMADOR"), (fx + 360, "MAITE"), (fx + 680, "SERGIO")]):
        add(f'<div id="nt{k}" class="ntag" style="{css_box(x, fl - 40, 250, 60, 8)}opacity:0">{n}</div>')
    add(f'<div id="ring" data-layout-ignore style="{css_box(fx + 260, fy + 420, 120, 120, 8)}opacity:0">{icon("gem", 120, "#facc15", 2.6)}</div>')
    add(f'<div id="hrt" data-layout-ignore style="{css_box(fx + 580, fy + 410, 130, 130, 8)}opacity:0">'
        f'{icon("heart", 130, "#ef4444", 2.4).replace("<svg", "<svg fill=\"#fca5a5\"")}</div>')
    pram("pr1", fx + 360, fy + 180, z=7, sc=0.6)
    add(f'<div id="ojo" class="pill" style="{css_box(fx + 260, fy + 170, None, None, 9)}background:{ACC};color:{INK};font-size:48px;opacity:0">«OJOS DE POLLO»</div>')
    t_lo, t_pas, t_mai, t_cas, t_ama, t_ave, t_ser, t_nac, t_nin, t_apo, t_ojo = (P("lo", 2), P("paso"), P("maite"), P("casada"), P("amador"),
                                                                                  P("aventura"), P("sergio"), P("nacio"), P("nino"), P("apodado"), P("ojos"))
    travel(t_lo - 0.12, F(0, 1), 0, 1630, dur=0.6)
    header_in("h1", t_lo, t_pas)
    for k, (c, t) in enumerate([("mt1", t_mai), ("am1", t_ama - 0.2), ("sg1", t_ser - 0.1)]):
        life(c, 0, G.DUR, 3 + k)
        js(f'tl.fromTo("#{c}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t:.3f});')
    for k, t in enumerate([t_ama - 0.2, t_mai, t_ser - 0.1]):
        js(f'tl.fromTo("#nt{k}", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t + 0.1:.3f});')
    pop("#ring", t_cas, sound="check")
    pop("#hrt", t_ave, sound="pop2")
    js(f'tl.to("#hrt", {{scale:1.2, duration:0.15, yoyo:true, repeat:3}}, {t_ave + 0.4:.3f});')
    js(f'tl.to(Q("am1","brows"), {{y:10, duration:0.2}}, {t_ave + 0.2:.3f});')
    js(f'tl.to("#ring, #hrt", {{opacity:0.3, duration:0.3}}, {t_nac - 0.2:.3f});')
    js(f'tl.fromTo("#pr1", {{opacity:0, y:-300}}, {{opacity:1, y:0, duration:0.5, ease:"bounce.out"}}, {t_nac - 0.1:.3f});')
    sfx(t_nin, "golpe", 0.3)
    pop("#ojo", t_ojo - 0.1, sound="pop")
    js(f'tl.to("#ojo", {{rotation:-4, duration:0.1, yoyo:true, repeat:3}}, {t_ojo + 0.3:.3f});')


# ================================================================= SERGIO SE VA
def scene_viaje():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    add(character("sg2", "sergio", fx + 300, fl, 1.15, z=5))
    add(f'<div id="lug" class="lug" style="{css_box(fx + 390, fl - 220, 170, 210, 6)}opacity:0"><i></i></div>')
    add(f'<div id="pln" data-layout-ignore style="{css_box(fx + 600, fy + 330, 200, 200, 8)}opacity:0">{icon("plane", 200, "#f8fafc", 2)}</div>')
    add(f'<div id="clk" data-layout-ignore style="{css_box(fx + 700, fy + 560, 170, 170, 7)}opacity:0">{icon("clapperboard", 170, "#facc15", 2)}</div>')
    add(f'<div id="chc" class="pill" style="{css_box(fx + 120, fy + 190, None, None, 9)}background:#0ea5e9;color:#fff;font-size:50px;opacity:0">AL OTRO LADO DEL CHARCO</div>')
    t_ser, t_que, t_fue, t_rod, t_pel, t_cha = P("sergio", 2), P("quedarse"), P("fue"), P("rodar"), P("pelicula"), P("charco")
    travel(t_ser - 0.4, F(1, 1), 1, 1630, dur=0.6)
    life("sg2", 0, G.DUR, 6)
    js(f'tl.fromTo("#sg2", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_ser - 0.2:.3f});')
    js(f'tl.fromTo("#lug", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_que - 0.2:.3f});')
    sfx(t_que, "madera", 0.3)
    js(f'wave("sg2", {t_fue - 0.2:.3f}, {t_rod + 0.4:.3f}); tl.to(Q("sg2","armR"), {{rotation:0, svgOrigin:PIV.armR, duration:0.3}}, {t_rod + 0.5:.3f});')
    js(f'tl.fromTo("#pln", {{opacity:0, x:-500, y:300, rotation:-20}}, {{opacity:1, x:0, y:0, rotation:-20, duration:0.8, ease:"power2.out"}}, {t_fue:.3f});')
    sfx(t_fue, "whoosh", 0.4)
    pop("#clk", t_pel - 0.1, sound="madera", vol=0.35)
    js(f'tl.to("#clk", {{rotation:-12, duration:0.08, yoyo:true, repeat:3}}, {t_pel + 0.3:.3f});')
    pop("#chc", t_cha - 0.5, sound="pop2")
    js(f'tl.to("#pln", {{x:400, y:-300, opacity:0, duration:0.6, ease:"power2.in"}}, {E("charco"):.3f});')


# ================================================================= 1 · EL SECRETO (imaginado)
def scene_secreto():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    header("h2", fx, fy, "1", "EL SECRETO", color="#a855f7", txt="#fff")
    add(character("mt3", "maite", fx + 280, fl, 1.15, z=5))
    add(f'''<div id="av" class="card" style="{css_box(fx + 470, fy + 300, 440, 300, 6)}background:#fff;opacity:0">
      <div class="avt">{icon("heart", 70, "#ef4444", 2.6)}<b>AVENTURA</b><span>CON SERGIO</span></div></div>''')
    add(f'<div id="lck" data-layout-ignore style="{css_box(fx + 610, fy + 540, 170, 170, 8)}opacity:0">{icon("lock", 170, "#facc15", 2.4)}</div>')
    add(f'<div id="shh" class="pill" style="{css_box(fx + 80, fy + 330, None, None, 9)}background:#a855f7;color:#fff;font-size:56px;opacity:0">¡SHHH!</div>')
    add(f'<div id="pr3" class="nopram" style="{css_box(fx + 520, fl - 260, 300, 240, 5)}opacity:0">{icon("baby", 150, "#94a3b8", 2.4)}</div>')
    t_aho, t_ima, t_uno, t_beb, t_ave, t_fac, t_esc = P("ahora"), P("imaginado"), P("uno"), P("bebe", 2), P("aventura", 2), P("facil"), P("esconder")
    travel(t_aho - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h2", t_uno, t_uno + 0.3)
    life("mt3", 0, G.DUR, 7)
    js(f'tl.fromTo("#mt3", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_uno:.3f});')
    js(f'tl.fromTo("#pr3", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_beb - 0.2:.3f}); tl.to("#pr3", {{opacity:0, scale:0.5, duration:0.35}}, {t_beb + 0.3:.3f});')
    sfx(t_beb + 0.3, "whoosh-corto", 0.25)
    slide_in("#av", t_ave - 0.2, dx=60, dy=0)
    js(f'tl.fromTo("#lck", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_fac:.3f});')
    sfx(t_fac + 0.3, "click", 0.4)
    js(f'tl.to("#av", {{opacity:0.5, duration:0.3}}, {t_esc:.3f});')
    pop("#shh", t_esc - 0.1, sound="pop")
    js(f'point("mt3", "R", {t_esc - 0.2:.3f}, {t_esc + 0.9:.3f}, -150);')


# ================================================================= 2 · LA PAREJA (imaginado)
def scene_pareja():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h3", fx, fy, "2", "LA PAREJA", color="#ec4899", txt="#fff")
    add(character("am3", "amador", fx + 300, fl, 1.15, z=5))
    add(character("mt4", "maite", fx + 660, fl, 1.15, z=5))
    rr, hh = roller("mj", "00", 130, INK)
    add(f'''<div id="mjc" class="card" style="{css_box(fx + 230, fy + 220, 500, 280, 8)}background:#fff;opacity:0">
      <div class="mjt">MESES JUNTOS</div><div class="mjn">{rr}<span class="mjq">+</span></div></div>''')
    add(f'<div id="nss" class="pill" style="{css_box(fx + 250, fy + 540, None, None, 9)}background:{BAD};color:#fff;font-size:50px;opacity:0">¿NUNCA SE SABE?</div>')
    t_dos, t_ama, t_agu, t_jun, t_tie, t_aun, t_nun = P("dos"), P("amador", 2), P("aguantado"), P("juntos"), P("tiempo"), P("aunque"), P("nunca", 2)
    travel(t_dos - 0.3, F(2, 0), 2, 570, dur=0.7)
    header_in("h3", t_dos, t_dos + 0.3)
    life("am3", 0, G.DUR, 8)
    life("mt4", 0, G.DUR, 9)
    js(f'tl.fromTo("#am3", {{opacity:0, x:-100}}, {{opacity:1, x:0, duration:0.35}}, {t_ama - 0.1:.3f}); tl.fromTo("#mt4", {{opacity:0, x:100}}, {{opacity:1, x:0, duration:0.35}}, {t_ama + 0.1:.3f});')
    js(f'tl.to(Q("am3","armR"), {{rotation:-42, svgOrigin:PIV.armR, duration:0.35, ease:"back.out(2)"}}, {t_agu:.3f}); tl.to(Q("mt4","armL"), {{rotation:42, svgOrigin:PIV.armL, duration:0.35, ease:"back.out(2)"}}, {t_agu:.3f});')
    slide_in("#mjc", t_agu - 0.2, dy=-60)
    roll_set("mj", "00", hh)
    roll_to("mj", "36", hh, t_jun, dur=1.2, spins=1)
    js(f'tl.fromTo(".mjq", {{opacity:0}}, {{opacity:1, duration:0.2}}, {t_tie + 0.2:.3f});')
    # aunque con Amador... nunca se sabe: todo se tambalea
    js(f'tl.to("#mjc", {{rotation:6, duration:0.12, yoyo:true, repeat:7}}, {t_aun:.3f});')
    js(f'tl.to(Q("am3","armR"), {{rotation:0, svgOrigin:PIV.armR, duration:0.3}}, {t_nun:.3f}); tl.to(Q("mt4","armL"), {{rotation:0, svgOrigin:PIV.armL, duration:0.3}}, {t_nun:.3f});')
    js(f'tilt("mt4", {t_nun:.3f}); tl.to(Q("am3","head"), {{rotation:-12, svgOrigin:PIV.head, duration:0.2, yoyo:true, repeat:3}}, {t_nun:.3f});')
    pop("#nss", t_nun - 0.3, sound="golpe", vol=0.3)


# ================================================================= 3 · SERGIO (imaginado) + TRAMA PERDIDA
def scene_sergio():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h4", fx, fy, "3", "SERGIO", color="#0ea5e9", txt="#fff")
    add(character("sg3", "sergio", fx + 260, fl, 1.15, z=5))
    add(f'<div id="lug2" class="lug" style="{css_box(fx + 360, fl - 220, 170, 210, 6)}opacity:0"><i></i></div>')
    add(f'''<svg id="cab" data-layout-ignore style="{css_box(fx + 450, fl - 160, 460, 120, 5)}overflow:visible" viewBox="0 0 460 120">
      <path id="cabp" d="M0 60 C 80 0, 140 120, 220 60 S 360 0, 440 70" stroke="#f472b6" stroke-width="12" fill="none" stroke-linecap="round"/></svg>''')
    add(f'<div id="sci" data-layout-ignore style="{css_box(fx + 600, fl - 260, 140, 140, 8)}opacity:0">{icon("scissors", 140, "#f8fafc", 2.4)}</div>')
    add(f'<div id="sin" class="pill" style="{css_box(fx + 330, fy + 230, None, None, 9)}background:#0ea5e9;color:#fff;font-size:50px;opacity:0">SIN CABOS SUELTOS</div>')
    add(f'<div id="tpe" class="stampbox" style="{css_box(fx + 150, fy + 360, 660, 160, 11)}opacity:0;font-size:82px">TRAMA PERDIDA</div>')
    t_tre, t_ser, t_dej, t_atr, t_via, t_cab, t_sue = P("tres"), P("sergio", 4), P("dejado"), P("atras"), P("viaje"), P("cabos"), P("sueltos")
    t_y, t_per, t_tra, t_loc = P("serie"), P("perdido"), P("tramas"), P("locas")
    travel(t_tre - 0.3, F(2, 1), 2, 1630, dur=0.6)
    header_in("h4", t_tre, t_tre + 0.3)
    life("sg3", 0, G.DUR, 10)
    js(f'tl.fromTo("#sg3", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_ser:.3f});')
    js(f'tl.fromTo("#lug2", {{opacity:0, y:-100}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_dej:.3f});')
    js('tl.set("#cabp", {strokeDasharray:560, strokeDashoffset:560}, 0);')
    js(f'tl.to("#cabp", {{strokeDashoffset:0, duration:0.6}}, {t_atr:.3f});')
    pop("#sci", t_cab - 0.4, sound=None)
    js(f'tl.to("#sci", {{rotation:-30, duration:0.1, yoyo:true, repeat:3}}, {t_cab - 0.1:.3f});')
    js(f'tl.to("#cabp", {{opacity:0, duration:0.3}}, {t_sue:.3f});')
    sfx(t_cab, "papel", 0.4)
    pop("#sin", t_sue - 0.1, sound="check")
    js(f'tl.to("#sci, #sin", {{opacity:0, duration:0.3}}, {t_per - 0.3:.3f});')
    stamp("#tpe", t_tra - 0.25, rot=-6)
    js(f'tl.to("#tpe", {{scale:1.08, duration:0.12, yoyo:true, repeat:1}}, {t_loc:.3f});')


# ================================================================= ENCUESTA
OPTS = [("MEJOR", "#22c55e"), ("PEOR", "#ef4444"), ("IGUAL", "#94a3b8")]


def scene_final():
    fx, fy, fw, fh = F(3, 1)
    rows = "".join(f'<div class="poll" style="top:{150 + k * 100}px"><span>{n}</span><i id="pb{k}" style="background:{c}"></i></div>'
                   for k, (n, c) in enumerate(OPTS))
    add(f'''<div id="pollc" class="card" style="{css_box(fx + 40, fy + 220, 880, 500, 6)}background:#fff;opacity:0">
      <div class="polh">{icon("message-circle", 54, INK, 2.6)} SIN ESE BEBÉ, LA SERIE…</div>{rows}</div>''')
    cta = "Habría sido…"
    add(f'''<div id="cbx" class="card" style="{css_box(fx + 40, fy + 760, 880, 170, 6)}background:#fff;opacity:0">
      <div id="ctt" class="ctt">{chars(cta, "kc")}</div><div id="pub" class="pubb">Publicar</div></div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 800, fy + 880, 90, 90, 12)}opacity:0">{icon("mouse-pointer-2", 90, "#fff", 2.4).replace("<svg", "<svg fill=\"#0f1115\"")}</div>')
    t_tu, t_mej, t_peo, t_leo, t_com = P("tu"), P("mejor"), P("peor"), P("leo"), P("comentarios")
    travel(t_tu - 0.35, F(3, 1), 3, 1630, dur=0.6)
    slide_in("#pollc", t_tu - 0.1, dy=-60)
    js('tl.set("[id^=pb]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    for k, (w, t) in enumerate([(0.5, t_mej), (0.85, t_peo), (0.35, t_peo + 0.3)]):
        js(f'tl.to("#pb{k}", {{scaleX:{w}, duration:0.4, ease:"back.out(1.6)"}}, {t:.3f});')
        sfx(t, "pop2", 0.22)
    slide_in("#cbx", t_peo + 0.3, dy=60, sound=None)
    type_on("#ctt .kc", len(cta), t_leo - 0.2, t_com + 0.3)
    js(f'tl.fromTo("#cur", {{opacity:0, x:160, y:160}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.4:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.4:.3f});')
    sfx(t_com + 0.4, "click", 0.5)
    cam(E("comentarios") + 0.1, (0, 100, 2200, 3900), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 42px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.htitle {{ font-size:76px; top:28px; }}
.stampbox {{ font:900 100px {FONT}; color:{BAD}; border:12px solid {BAD}; border-radius:26px; background:rgba(255,255,255,0.94);
  display:flex; align-items:center; justify-content:center; gap:16px; letter-spacing:-2px; white-space:nowrap; }}
.qbig {{ font:900 300px {FONT}; color:{ACC}; text-align:center; line-height:300px; text-shadow:0 14px 0 #b45309; }}
.ntag {{ border-radius:14px; background:#0f172a; border:4px solid #fff; color:#fff; font:900 34px {FONT}; text-align:center; line-height:52px; white-space:nowrap; }}
.lug {{ border-radius:22px; background:#b45309; border:8px solid #78350f; }}
.lug i {{ position:absolute; left:50%; top:-46px; width:70px; height:46px; margin-left:-35px; border:10px solid #78350f; border-bottom:none; border-radius:20px 20px 0 0; }}
.avt {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; }}
.avt b {{ font:900 64px {FONT}; color:{INK}; }} .avt span {{ font:900 40px {FONT}; color:#64748b; }}
.nopram {{ display:flex; align-items:center; justify-content:center; border:8px dashed #94a3b8; border-radius:30px; }}
.mjt {{ position:absolute; left:0; right:0; top:28px; text-align:center; font:900 50px {FONT}; color:#475569; }}
.mjn {{ position:absolute; left:0; right:0; top:100px; text-align:center; }}
.mjq {{ font:900 110px {FONT}; color:{INK}; vertical-align:top; opacity:0; }}
.polh svg {{ flex:none; }}
.polh {{ position:absolute; left:40px; right:40px; top:40px; display:flex; align-items:center; gap:18px; font:900 48px {FONT}; color:{INK}; white-space:nowrap; }}
.poll {{ position:absolute; left:40px; right:40px; height:76px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:220px; flex:none; font:900 52px {FONT}; color:{INK}; white-space:nowrap; }}
.poll i {{ flex:1; height:44px; border-radius:22px; }}
.ctt {{ position:absolute; left:40px; top:52px; font:800 54px {FONT}; color:{INK}; white-space:nowrap; }}
.pubb {{ position:absolute; right:30px; top:40px; padding:12px 40px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 56px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    for r_, x_ in [(1, 570), (2, 570), (2, 1630)]:
        tag_imaginado(r_, x_)
    scene_hook()
    scene_paso()
    scene_viaje()
    scene_secreto()
    scene_pareja()
    scene_sergio()
    scene_final()
