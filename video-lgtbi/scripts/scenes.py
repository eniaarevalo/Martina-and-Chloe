"""Escenas del vídeo LGTBI. Un solo mundo: un camino en zigzag (la línea de tiempo 2003 -> hoy)
que se dibuja en arcoíris mientras la cámara viaja de parada en parada.

Orden de las paradas (fila, columna):
  fila 0: gancho (c0) -> 1 armario (c1)
  fila 1: 2 familia/Bea (c1) -> 2 tabú/Zequi (c0)
  fila 2: 3 ley 2005 (c0) -> 3 boda (c1)
  fila 3: 4 Luis Merlo (c1) -> 4 Adrià Collado (c0)
  fila 4: clímax (casas) y comentarios
"""
import math
import gen as G
from gen import (P, E, js, sfx, add, card, css_box, icon, chars, type_on, roller, roll_set, cam, shake, pop,
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
       (R_X, ROAD[3]), (L_X, ROAD[3]), (L_X, ROAD[4]), (R_X, ROAD[4])]
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


# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    add(f'<div class="room" data-layout-ignore style="{css_box(COLX[0] + 10, ROWS[4] + 120, 2100, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 6600, 1)}overflow:visible" viewBox="0 0 2200 6600">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="6500">
        <stop offset="0" stop-color="#ef4444"/><stop offset="0.2" stop-color="#f97316"/><stop offset="0.4" stop-color="#facc15"/>
        <stop offset="0.6" stop-color="#22c55e"/><stop offset="0.8" stop-color="#3b82f6"/><stop offset="1" stop-color="#a855f7"/></linearGradient></defs>
      <path d="{d}" stroke="rgba(255,255,255,0.08)" stroke-width="22" fill="none" stroke-linejoin="round" stroke-dasharray="4 28" stroke-linecap="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    # hitos de la línea de tiempo
    for lab, r, x in [("2003", 0, 300), ("2004", 1, 1830), ("2005", 2, 300), ("2006", 2, 1830), ("HOY", 3, 1830)]:
        add(f'<div class="mile" data-layout-ignore style="{css_box(x - 90, ROAD[r] + 26, 180, 70, 2)}">{lab}</div>')


# ================================================================= 0 · GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    add(f'''<div id="tv0" style="{css_box(fx + 110, fy + 150, 740, 500, 3)}">
      <div class="ant a1"></div><div class="ant a2"></div>
      <div id="tv0-screen" class="screen"><div id="tv0-y" style="font:900 150px {FONT};color:#fff;letter-spacing:-4px">2003</div>
        <div id="tv0-pt" class="pill" style="background:{ACC};color:{INK};opacity:0;margin-top:8px">PRIME TIME</div></div>
      <div class="knob k1"></div><div class="knob k2"></div></div>''')
    add(f'<div id="st-legal" class="stamp" style="{css_box(fx + 520, fy + 90, None, None, 8)}color:{BAD};border-color:{BAD};opacity:0">NO ES LEGAL</div>')
    add(character("mau0", "mauri", fx + 340, fl, 1.4, z=6))
    add(character("fer0", "fernando", fx + 610, fl, 1.4, z=6))

    tvcx, tvcy = fx + 480, fy + 400
    cam(0, (fx + 60, fy + 60, 840, 720), whoosh=False)
    cam(0.05, F(0, 0), dur=0.85, ease="power4.out", whoosh=False)
    sfx(0.0, "click", 0.5)
    sfx(0.05, "whoosh", 0.4)
    js('tl.set("#tv0-screen", {backgroundColor:"#1d3fa8"}, 0);')
    js('tl.fromTo("#tv0-y", {scale:1.25}, {scale:1, duration:0.4, ease:"back.out(2)"}, 0.0);')
    # salen de la tele
    for cid, cx in (("mau0", fx + 340), ("fer0", fx + 610)):
        js(f'tl.fromTo("#{cid}", {{x:{tvcx - cx}, y:{-(fl - tvcy - 120)}, scale:0.35, transformOrigin:"50% 100%"}}, '
           f'{{x:0, y:0, scale:1, duration:0.8, ease:"power2.out"}}, 0.1);')
        js(f'walk("{cid}", 0.1, 0.9, 0.16);')
    t_legal, t_mau, t_fer, t_par, t_prime = P("legal"), P("mauri"), P("fernando"), P("pareja"), P("prime")
    stamp("#st-legal", t_legal, rot=-10)
    js(f'tilt("mau0", {t_legal + 0.2:.3f}); tilt("fer0", {t_legal + 0.25:.3f});')
    js(f'jump("mau0", {t_mau:.3f}, 40);')
    js(f'jump("fer0", {t_fer:.3f}, 40);')
    hold_hands("mau0", "fer0", t_par)
    sfx(t_par, "pop", 0.3)
    pop("#tv0-pt", t_prime, sound="pop2")
    life("mau0", 0.9, G.DUR, 1)
    life("fer0", 0.9, G.DUR, 2)
    t_cam, t_vid = P("cambiaron"), P("vidas")
    hearts("h0-", fx + 475, fl - 700, 6, t_cam, spread=520, rise=480)
    cam(t_vid, ROW(0), dur=0.6)


# ================================================================= 1 · EL ARMARIO (2003)
def scene_armario():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "1", "EL ARMARIO", year="2003")
    msg = "¿Esos dos son… compañeros de piso?"
    card("chat1", fx, fy + 170, fw, 300, f'''
      <div class="chathead"><span class="dot"></span>{icon("users", 54, "#fff", 2.4)}
        <span style="font:900 50px {FONT};color:#fff;margin-left:16px">Vecinos</span></div>
      <div id="chat1-m" style="position:absolute;left:36px;top:132px;right:36px;font:800 52px {FONT};color:{INK};line-height:1.12">{chars(msg)}</div>''',
         bg="#f4f5f7")
    add(f'''<div id="ward" style="{css_box(fx + 560, fy + 520, 380, 540, 4)}" class="ward">
      <div class="ward-top"></div></div>''')
    add(f'<div id="ward-l" class="wdoor" style="{css_box(fx + 578, fy + 560, 172, 490, 7)}"><div class="knobw r"></div></div>')
    add(f'<div id="ward-r" class="wdoor" style="{css_box(fx + 750, fy + 560, 172, 490, 7)}"><div class="knobw"></div></div>')
    add(character("mau1", "mauri", fx + 170, fl, 1.3, z=6))
    add(character("fer1", "fernando", fx + 400, fl, 1.3, z=5))
    add(f'<div id="ch-sal" class="chip" style="{css_box(fx + 330, fy + 640, None, None, 9)}background:{GOOD_BG}">SALIR DEL ARMARIO</div>')
    add(f'<div id="ch-voy" class="chip" style="{css_box(fx + 330, fy + 760, None, None, 9)}background:{BAD}">ME VOY</div>')
    add(f'<div id="cur1" data-layout-ignore style="{css_box(fx + 760, fy + 700, 110, 110, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 100, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')

    t_uno, t_arm = P("uno"), P("armario")
    travel(t_uno, F(0, 1), 0, 1630, dur=0.8)
    header_in("h1", t_uno, t_arm, year=True)
    life("mau1", 0, G.DUR, 3)
    life("fer1", 0, G.DUR, 4)
    t_pri, t_fer, t_nad, t_sup = P("primera"), P("fernando", 2), P("nadie"), P("supiera")
    slide_in("#chat1", t_pri, dy=-60)
    # Fernando se mete en el armario
    js(f'tl.to("#ward-l", {{scaleX:0.12, transformOrigin:"0% 50%", duration:0.3, ease:"power3.out"}}, {t_fer:.3f});')
    js(f'tl.to("#ward-r", {{scaleX:0.12, transformOrigin:"100% 50%", duration:0.3, ease:"power3.out"}}, {t_fer:.3f});')
    sfx(t_fer, "puerta", 0.3)
    js(f'tl.to("#fer1", {{x:350, duration:0.7, ease:"power1.inOut"}}, {t_fer + 0.1:.3f});')
    js(f'walk("fer1", {t_fer + 0.1:.3f}, {t_fer + 0.8:.3f}, 0.15);')
    js(f'tl.to("#ward-l, #ward-r", {{scaleX:1, duration:0.16, ease:"power4.in"}}, {t_nad:.3f});')
    sfx(t_nad + 0.12, "madera", 0.5)
    js(f'tl.to("#ward", {{keyframes:[{{rotation:-1.5}},{{rotation:1.5}},{{rotation:0}}], duration:0.3}}, {t_nad + 0.15:.3f});')
    type_on("#chat1-m .ch", len(msg), t_nad + 0.05, t_sup + 0.7)
    # el ultimátum
    t_mau, t_ult, t_sal, t_arm2, t_dej = P("mauri", 2), P("ultimatum"), P("sales"), P("armario", 2), P("dejas")
    js(f'point("mau1", "R", {t_mau:.3f}, {t_dej - 0.1:.3f}, -95);')
    js(f'tl.to("#ward", {{keyframes:[{{x:-6}},{{x:6}},{{x:-4}},{{x:0}}], duration:0.3}}, {t_ult:.3f});')
    sfx(t_ult, "golpe", 0.3)
    pop("#ch-sal", t_sal, sound="pop")
    pop("#ch-voy", t_dej, sound="pop")
    js(f'tl.fromTo("#cur1", {{opacity:0, x:120, y:80}}, {{opacity:1, x:0, y:0, duration:0.35}}, {t_sal + 0.1:.3f});')
    js(f'tl.to("#cur1", {{y:110, duration:0.3, ease:"power2.inOut"}}, {t_dej + 0.1:.3f});')
    js(f'tl.to("#cur1", {{y:0, duration:0.3, ease:"power2.inOut"}}, {t_dej + 0.5:.3f});')
    js(f'tl.to(Q("mau1","armL"), {{rotation:-70, svgOrigin:PIV.armL, duration:0.3}}, {t_dej:.3f});')
    js(f'tl.to(Q("mau1","armR"), {{rotation:70, svgOrigin:PIV.armR, duration:0.3}}, {t_dej + 0.05:.3f});')
    cam(E("dejas") + 0.05, ROW(0), dur=0.45)


# ================================================================= 2 · LA FAMILIA (Bea)
def scene_bea():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    header("h2", fx, fy, "2", "LA FAMILIA", color=PURPLE, txt="#fff")
    card("bea-c", fx, fy + 170, fw, 170, f'''
      <div style="position:absolute;left:40px;top:28px;font:900 84px {FONT};color:{INK}">BEA</div>
      <div id="bea-am" style="position:absolute;left:250px;top:46px;font:800 56px {FONT};color:#555;opacity:0">su mejor amiga</div>
      <div id="bea-les" class="pill" style="position:absolute;right:30px;top:-36px;background:{PURPLE};color:#fff;opacity:0">LESBIANA</div>''')
    q = "¿Tendrías un hijo conmigo?"
    add(f'''<div id="bub2" class="bubble big" style="{css_box(fx + 240, fy + 370, 720, 210, 9)}padding:0">
      <div id="bub2-a" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:24px">
        {icon("baby", 120, INK, 2.4)}<span style="font:900 120px {FONT};color:{PURPLE}">?</span></div>
      <div id="bub2-b" style="position:absolute;left:36px;top:24px;right:30px;opacity:0">
        <div id="bub2-t" style="font:900 52px {FONT};color:{INK}">{chars(q, "qc")}</div>
        <div id="bub2-p" class="pill" style="display:inline-block;margin-top:14px;background:{PURPLE};color:#fff;font-size:46px;opacity:0">INSEMINACIÓN ARTIFICIAL</div></div>
      <div class="tail" style="left:60px;top:auto;bottom:-30px;border-bottom:none;border-top:34px solid #fff"></div></div>''')
    add(character("bea1", "bea", fx + 190, fl, 1.15, z=6))
    add(character("mau2", "mauri", fx + 800, fl, 1.15, z=6))

    t_dos, t_fam = P("dos"), P("familia")
    travel(t_dos, F(1, 1), 1, 1630, dur=0.85)
    header_in("h2", t_dos, t_fam)
    t_bea, t_mej, t_les, t_mad = P("bea"), P("mejor"), P("lesbiana"), P("madre")
    js(f'tl.fromTo("#bea1", {{x:-520, opacity:0}}, {{x:0, opacity:1, duration:0.8, ease:"power2.out"}}, {t_bea - 0.2:.3f});')
    js(f'walk("bea1", {t_bea - 0.2:.3f}, {t_bea + 0.6:.3f}, 0.15);')
    slide_in("#bea-c", t_bea, dy=-60)
    js(f'tl.fromTo("#bea-am", {{opacity:0, x:-20}}, {{opacity:1, x:0, duration:0.3}}, {t_mej:.3f});')
    pop("#bea-les", t_les, sound="pop")
    pop("#bub2", t_mad, sound="pop2")
    life("bea1", t_bea + 0.6, G.DUR, 5)
    life("mau2", 0, G.DUR, 6)
    t_pid, t_hijo, t_ins = P("pidio"), P("hijo"), P("inseminacion")
    flip("#bub2", t_pid, ["#bub2-a"], ["#bub2-b"])
    type_on("#bub2-t .qc", len(q), t_pid + 0.1, t_hijo + 0.3)
    js(f'point("bea1", "R", {t_pid:.3f}, {t_ins:.3f}, -80);')
    js(f'jump("mau2", {t_hijo + 0.2:.3f}, 55);')
    pop("#bub2-p", t_ins, sound="pop")


def scene_tabu():
    fx, fy, fw, fh = F(1, 0)
    add(f'''<div id="tag" style="{css_box(fx + 180, fy + 10, 600, 160, 8)}border-radius:30px;background:{BAD}">
      <div id="tag-a" class="tagt">TABÚ</div><div id="tag-b" class="tagt" style="opacity:0">NATURAL ✓</div></div>''')
    for nid, kind, x, lab in (("nm", "bea", fx, "MADRE<br>LESBIANA"), ("np", "mauri", fx + 500, "PADRE<br>GAY")):
        card(nid, x, fy + 230, 460, 230, f'''
          <div style="position:absolute;left:20px;top:30px">{avatar(nid + "-av", kind, 170)}</div>
          <div style="position:absolute;left:204px;top:52px;font:900 48px {FONT};color:{INK};line-height:1.15">{lab}</div>''')
    add(f'''<svg id="tree" data-layout-ignore style="{css_box(fx, fy + 460, 960, 200, 4)}overflow:visible" viewBox="0 0 960 200">
      <path id="tree-l" d="M 230 0 L 230 80 L 480 80 L 480 190" stroke="#fff" stroke-width="10" fill="none" stroke-linejoin="round"/>
      <path id="tree-r" d="M 730 0 L 730 80 L 480 80" stroke="#fff" stroke-width="10" fill="none" stroke-linejoin="round"/></svg>''')
    card("baby", fx + 260, fy + 650, 440, 400, f'''
      <svg id="pram" style="position:absolute;left:60px;top:20px" width="320" height="260" viewBox="0 0 320 260">
        <path d="M 40 40 L 40 150 Q 40 190 90 190 L 250 190 Q 290 190 290 150 L 290 110 L 150 110 L 150 40 Z" fill="{PURPLE}"/>
        <path d="M 150 40 Q 280 40 290 110 L 150 110 Z" fill="#a78bfa"/>
        <circle cx="90" cy="225" r="28" fill="#1f2937"/><circle cx="250" cy="225" r="28" fill="#1f2937"/>
        <g id="bface" opacity="0"><circle cx="210" cy="92" r="40" fill="#f6d0b0"/><circle cx="198" cy="88" r="5" fill="#111"/>
          <circle cx="222" cy="88" r="5" fill="#111"/><path d="M200 104 Q210 112 220 104" stroke="#a0522d" stroke-width="4" fill="none"/></g>
        <text id="bq" x="215" y="100" font-family="{FONT}" font-weight="900" font-size="70" fill="#fff" text-anchor="middle">?</text></svg>
      <div id="baby-n" style="position:absolute;left:0;right:0;top:300px;text-align:center;font:900 72px {FONT};color:{INK};opacity:0">ZEQUI</div>''')

    t_una, t_mad2, t_pad, t_cri, t_beb, t_tab = P("una"), P("madre", 2), P("padre"), P("criando"), P("bebe"), P("tabu")
    travel(t_una, F(1, 0), 1, 570, dur=0.7)
    pop("#nm", t_mad2, sound="pop")
    pop("#np", t_pad, sound="pop")
    life("nm-av", t_mad2, G.DUR, 7)
    life("np-av", t_pad, G.DUR, 8)
    js('tl.set("#tree-l, #tree-r", {strokeDasharray:700, strokeDashoffset:700}, 0);')
    js(f'tl.to("#tree-l, #tree-r", {{strokeDashoffset:0, duration:0.6, ease:"power2.inOut"}}, {t_cri:.3f});')
    pop("#baby", t_beb, sound="pop2")
    stamp("#tag", t_tab, rot=-4)
    js(f'tl.to("#tag", {{keyframes:[{{x:-8}},{{x:8}},{{x:-6}},{{x:0}}], duration:0.35}}, {t_tab + 0.35:.3f});')
    t_zeq, t_nat = P("zequi"), P("naturalidad")
    js(f'tl.to("#bq", {{opacity:0, duration:0.15}}, {t_zeq:.3f}); tl.to("#bface", {{opacity:1, duration:0.25}}, {t_zeq + 0.1:.3f});')
    js(f'tl.fromTo("#baby-n", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {t_zeq:.3f});')
    sfx(t_zeq, "pop", 0.3)
    js(f'tl.fromTo("#pram", {{rotation:-3}}, {{rotation:3, transformOrigin:"50% 90%", duration:0.6, ease:"sine.inOut", yoyo:true, repeat:{int((G.DUR - t_zeq) / 0.6)}, immediateRender:false}}, {t_zeq + 0.2:.3f});')
    flip("#tag", t_nat, ["#tag-a"], ["#tag-b"], bg=GOOD_BG)
    sfx(t_nat + 0.2, "check", 0.4)
    cam(E("naturalidad") + 0.0, ROW(1), dur=0.45)


# ================================================================= 3 · LA BODA
def scene_ley():
    fx, fy, fw, fh = F(2, 0)
    header("h3", fx, fy, "3", "LA BODA", year="2005")
    card("doc", fx + 40, fy + 170, 880, 460, f'''
      <div style="position:absolute;left:36px;top:36px">{icon("file-text", 120, INK, 2.2)}</div>
      <div style="position:absolute;left:180px;top:30px;font:900 84px {FONT};color:{INK}">BOE</div>
      <div style="position:absolute;left:180px;top:122px;font:800 60px {FONT};color:#444">Ley 13/2005</div>
      <div style="position:absolute;left:40px;top:220px;font:800 54px {FONT};color:{INK}">Matrimonio igualitario</div>
      <div id="doc-st" style="position:absolute;left:40px;top:320px;height:90px;width:560px;border-radius:45px;background:{BAD}">
        <div id="doc-a" class="sttxt">✗ NO LEGAL</div><div id="doc-b" class="sttxt" style="opacity:0">✓ LEGAL</div></div>''')
    add(f'<div id="gavel" class="sticker" style="{css_box(fx + 730, fy + 120, 190, 190, 9)}">{icon("gavel", 120, INK, 2.4)}</div>')
    notes = ["Ya es ley", "Matrimonio igualitario: aprobado", "Julio de 2005: en vigor"]
    for i, n in enumerate(notes):
        add(f'''<div id="nt{i}" class="notif" style="{css_box(fx + 40, fy + 680 + i * 125, 880, 110, 8)}">
          <div class="nicon">{icon("bell", 50, "#fff", 2.6)}</div><span>{n}</span></div>''')
    t_tres, t_boda, t_2005, t_esp, t_leg, t_mat, t_igu = (P("tres"), P("boda"), P("2005"), P("espana"), P("legalizo"),
                                                          P("matrimonio"), P("igualitario"))
    travel(t_tres, F(2, 0), 2, 570, dur=0.85)
    header_in("h3", t_tres, t_boda, year=True)
    pop("#doc", t_2005, sound="papel", vol=0.4)
    js(f'tl.to("#doc", {{rotation:-1.5, duration:0.2, yoyo:true, repeat:1}}, {t_esp:.3f});')
    stamp("#gavel", t_leg, rot=-15)
    flip("#doc-st", t_leg + 0.15, ["#doc-a"], ["#doc-b"], sound=None, bg=GOOD_BG)
    sfx(t_leg + 0.3, "check", 0.4)
    for i, t in enumerate([t_mat, t_igu, t_igu + 0.45]):
        js(f'tl.fromTo("#nt{i}", {{opacity:0, y:-160}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t:.3f});')
        sfx(t, "pop2", 0.3)


def scene_boda():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    flowers = "".join(
        f'<circle cx="{350 + 300 * math.cos(math.radians(a)):.0f}" cy="{380 - 300 * math.sin(math.radians(a)):.0f}" r="26" '
        f'fill="{["#ef4444", "#f97316", "#facc15", "#22c55e", "#3b82f6", "#a855f7"][k % 6]}"/>'
        for k, a in enumerate(range(0, 181, 15)))
    add(f'''<svg id="arch" data-layout-ignore style="{css_box(fx + 130, fy + 200, 700, 860, 3)}overflow:visible" viewBox="0 0 700 860">
      <path d="M 50 860 L 50 380 A 300 300 0 0 1 650 380 L 650 860" stroke="#e5e7eb" stroke-width="30" fill="none"/>{flowers}</svg>''')
    card("si", fx + 80, fy + 40, 800, 160, f'''
      <div style="position:absolute;left:0;right:0;top:12px;text-align:center;font:900 52px {FONT};color:#666">JUNIO 2006</div>
      <div style="position:absolute;left:0;right:0;top:66px;text-align:center;font:900 76px {FONT};color:{GOOD_BG}">¡SÍ, QUIERO!</div>''')
    add(f'<div id="rings" class="sticker" style="{css_box(fx + 400, fy + 340, 160, 160, 9)}">{icon("gem", 100, PURPLE, 2.4)}</div>')
    add(character("mau3", "mauri", fx + 360, fl, 1.3, z=6))
    add(character("fer3", "fernando", fx + 600, fl, 1.3, z=6))
    conf = []
    for i in range(36):
        col = ["#ef4444", "#f97316", "#facc15", "#22c55e", "#3b82f6", "#a855f7"][i % 6]
        conf.append(f'<div class="cf" data-layout-ignore style="{css_box(fx + 60 + (i * 157) % 840, fy + 120 + (i * 61) % 160, 18, 30, 10)}background:{col}"></div>')
    add("".join(conf))
    t_ano, t_mau, t_fer, t_cas = P("ano"), P("mauri", 4), P("fernando", 3), P("casaron")
    travel(t_ano, F(2, 1), 2, 1630, dur=0.8)
    js(f'tl.fromTo("#mau3", {{x:-520, opacity:0}}, {{x:0, opacity:1, duration:0.8, ease:"power2.out"}}, {t_mau - 0.3:.3f}); walk("mau3", {t_mau - 0.3:.3f}, {t_mau + 0.5:.3f}, 0.15);')
    js(f'face("fer3", -1, 0); tl.fromTo("#fer3", {{x:520, opacity:0}}, {{x:0, opacity:1, duration:0.8, ease:"power2.out"}}, {t_fer - 0.3:.3f}); walk("fer3", {t_fer - 0.3:.3f}, {t_fer + 0.5:.3f}, 0.15); face("fer3", 1, {t_fer + 0.55:.3f});')
    life("mau3", t_mau + 0.5, G.DUR, 9)
    life("fer3", t_fer + 0.6, G.DUR, 10)
    hold_hands("mau3", "fer3", t_cas - 0.1)
    pop("#si", t_cas, sound="pop")
    pop("#rings", t_cas + 0.15, sound=None)
    sfx(t_cas + 0.1, "check", 0.4)
    js(f'tl.fromTo(".cf", {{opacity:0, y:-80, rotation:0}}, {{opacity:1, y:820, rotation:540, duration:2.2, ease:"power1.in", stagger:0.03}}, {t_cas:.3f});')
    js(f'tl.to(".cf", {{opacity:0, duration:0.3}}, {t_cas + 2.6:.3f});')
    js(f'jump("mau3", {t_cas + 0.4:.3f}, 45); jump("fer3", {t_cas + 0.5:.3f}, 45);')
    cam(E("serie", 2) + 0.0, ROW(2), dur=0.45)


# ================================================================= 4 · LA VIDA REAL
def scene_merlo():
    fx, fy, fw, fh = F(3, 1)
    fl = floor(3)
    header("h4", fx, fy, "4", "LA VIDA REAL", color=GOOD_BG, year="HOY", txt="#fff")
    cnt, ch = roller("cnt4", "0", 84, "#fff")
    card("merlo", fx, fy + 170, fw, 290, f'''
      <div class="mav" style="background:#16a596">{icon("mic", 100, "#fff", 2.4)}</div>
      <div style="position:absolute;left:240px;top:40px;font:900 76px {FONT};color:{INK}">LUIS MERLO</div>
      <div style="position:absolute;left:240px;top:140px;font:800 52px {FONT};color:#555">el actor de Mauri</div>''')
    add(f'''<div id="m-st" class="sticker" style="{css_box(fx + 800, fy + 120, 170, 170, 9)}background:{BAD}">
      <div id="m-sta" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 70px {FONT};color:#fff">×{cnt}</div>
      <div id="m-stb" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;background:{GOOD_BG};border-radius:50%">{icon("check", 110, "#fff", 3.4)}</div></div>''')
    for i in range(4):
        add(f'<div id="mx{i}" class="xdot" style="{css_box(fx + 240 + i * 70, fy + 380, 60, 60, 8)}">'
            f'<div class="xa">{icon("x", 44, "#fff", 3.6)}</div><div class="xb" style="opacity:0">{icon("check", 44, "#fff", 3.6)}</div></div>')
    quote = "«Mauri cambió muchas vidas»"
    add(f'''<div id="mq" style="{css_box(fx + 20, fy + 480, 920, 180, 8)}border-radius:36px;background:{BAD}">
      <div id="mq-a" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 64px {FONT};color:#fff">¿Un gay en prime time?</div>
      <div id="mq-b" style="position:absolute;left:40px;right:40px;top:22px;opacity:0;font:900 66px {FONT};color:{INK};line-height:1.1">{chars(quote, "mc")}</div></div>''')
    add(character("mau4", "mauri", fx + 800, fl, 0.9, z=6))
    t_cua, t_vid, t_lui, t_rec, t_cua2, t_mie = P("cuatro"), P("vida"), P("luis"), P("rechazo"), P("cuatro", 2), P("miedo")
    travel(t_cua, F(3, 1), 3, 1630, dur=0.9)
    header_in("h4", t_cua, t_vid, year=True)
    slide_in("#merlo", t_lui, dy=-60, sound="pop")
    pop("#m-st", t_rec - 0.05, sound=None)
    roll_set("cnt4", "0", ch)
    steps = [t_rec, t_rec + (t_cua2 - t_rec) / 3, t_rec + 2 * (t_cua2 - t_rec) / 3, t_cua2]
    for i, t in enumerate(steps):
        js(f'tl.to("#cnt4-d0", {{y:{-(10 + i + 1) * ch}, duration:0.2, ease:"back.out(2)"}}, {t:.3f});')
        pop(f"#mx{i}", t, sound="pop2", vol=0.3)
    js('tl.set("#mx0, #mx1, #mx2, #mx3", {backgroundColor:"' + BAD + '"}, 0);')
    pop("#mq", t_mie, sound="golpe", vol=0.3)
    life("mau4", 0, G.DUR, 11)
    js(f'tilt("mau4", {t_mie:.3f});')
    t_hoy, t_dic, t_vid2 = P("hoy"), P("dice"), P("vidas", 2)
    flip("#m-st", t_hoy, ["#m-sta"], ["#m-stb"], sound=None)
    for i in range(4):
        tt = t_hoy + 0.08 * i
        js(f'tl.to("#mx{i}", {{backgroundColor:"{GOOD_BG}", duration:0.2}}, {tt:.3f}); tl.set("#mx{i} .xa", {{opacity:0}}, {tt:.3f}); tl.set("#mx{i} .xb", {{opacity:1}}, {tt:.3f});')
    sfx(t_hoy, "check", 0.4)
    flip("#mq", t_dic, ["#mq-a"], ["#mq-b"], bg="#ffffff")
    type_on("#mq-b .mc", len(quote), t_dic + 0.15, t_vid2 + 0.45)
    js(f'wave("mau4", {t_vid2:.3f}, {t_vid2 + 1.5:.3f});')


def scene_collado():
    fx, fy, fw, fh = F(3, 0)
    fl = floor(3)
    card("coll", fx, fy + 170, fw, 290, f'''
      <div class="mav" style="background:#8e2a3c">{icon("mic", 100, "#fff", 2.4)}</div>
      <div style="position:absolute;left:240px;top:40px;font:900 74px {FONT};color:{INK}">ADRIÀ COLLADO</div>
      <div style="position:absolute;left:240px;top:140px;font:800 52px {FONT};color:#555">el actor de Fernando</div>''')
    add(character("fer4", "fernando", fx + 800, fl, 1.15, z=6))
    people = [("p1", "g1", fx + 110), ("p2", "g2", fx + 340), ("p3", "g3", fx + 570)]
    for k, (pid, kind, x) in enumerate(people):
        add(character(pid, kind, x, fl, 1.1, z=6))
        add(f'<div id="{pid}-b" class="bubble big" style="{css_box(x - 112, fy + 470 + (k % 2) * 110, 224, None, 9)}padding:18px 6px;text-align:center">'
            f'<span style="font:900 46px {FONT};color:{GOOD_BG}">¡Gracias!</span></div>')
    t_adr, t_par, t_cal, t_gra = P("adria"), P("paran"), P("calle"), P("gracias")
    travel(t_adr, F(3, 0), 3, 570, dur=0.75)
    slide_in("#coll", t_adr + 0.1, dy=-60, sound="pop")
    life("fer4", 0, G.DUR, 12)
    js('face("fer4", -1, 0);')
    for k, (pid, kind, x) in enumerate(people):
        t0 = t_par - 0.4 + k * 0.15
        js(f'tl.fromTo("#{pid}", {{x:{-700 - k * 80}, opacity:0}}, {{x:0, opacity:1, duration:1.0, ease:"power1.out"}}, {t0:.3f}); walk("{pid}", {t0:.3f}, {t0 + 1.0:.3f}, 0.14);')
        life(pid, t0 + 1.0, G.DUR, 20 + k)
        js(f'tl.fromTo("#{pid}-b", {{opacity:0, scale:0.4, transformOrigin:"50% 100%"}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2.4)"}}, {t_gra + k * 0.16:.3f});')
        sfx(t_gra + k * 0.16, "pop", 0.25)
        js(f'wave("{pid}", {t_gra + k * 0.16:.3f}, {t_gra + 1.6:.3f});')
    js(f'jump("fer4", {t_gra + 0.3:.3f}, 40);')


# ================================================================= CLÍMAX + COMENTARIOS
def scene_climax():
    y0 = ROWS[4]
    xs = [150, 800, 1450]
    msg = "Mamá, papá: tengo que contaros algo"
    for i, x in enumerate(xs):
        add(f'''<div id="hs{i}" style="{css_box(x, y0 + 200, 600, 720, 3)}">
          <div class="hroof"></div><div class="hbody">
            <div id="win{i}" class="win"><div id="wc{i}" class="wchat">{chars(msg, f"w{i}c")}</div></div></div></div>''')
    cta = "Gracias a ellos…"
    add(f'''<div id="cta" style="{css_box(560, y0 + 720, 1080, 540, 7)}" class="ctab">
      <div style="position:absolute;left:60px;top:40px;display:flex;align-items:center;gap:26px">{icon("message-circle", 110, INK, 2.6)}
        <span style="font:900 92px {FONT};color:{INK}">Comentarios</span></div>
      <div id="cta-t" style="position:absolute;left:60px;top:180px;font:800 96px {FONT};color:{INK}">{chars(cta, "kc")}<span id="caret" class="caret"></span></div>
      <div id="cta-btn" class="cbtn">Publicar</div></div>''')
    add(f'<div id="cur2" data-layout-ignore style="{css_box(1400, y0 + 1160, 170, 170, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 160, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    add(character("mau5", "mauri", 400, floor(4), 1.3, z=8))
    add(character("fer5", "fernando", 1800, floor(4), 1.3, z=8))

    t_muc, t_pub, t_que, t_atr, t_casa = P("muchos"), P("publico"), P("queria", 3), P("atrevieron"), P("casa")
    travel(t_muc - 0.25, (xs[0] + 300 - 480, y0 + 150, 960, 900), 4, 450, dur=0.7)
    for i, x in enumerate(xs):
        tl0 = [t_muc + 0.25, t_pub + 0.15, t_que + 0.15][i]
        js(f'tl.to("#win{i}", {{backgroundColor:"#ffe8a3", duration:0.3}}, {tl0:.3f});')
        sfx(tl0, "click", 0.25)
        type_on(f"#wc{i} .w{i}c", len(msg), tl0 + 0.05, [t_pub, t_que, t_atr][i] + 0.1)
    cam(t_pub - 0.1, (xs[1] + 300 - 480, y0 + 150, 960, 900), dur=0.5)
    cam(t_que - 0.1, (xs[2] + 300 - 480, y0 + 150, 960, 900), dur=0.5)
    road_to(t_pub - 0.1, 4, 2000, 1.2)
    cam(t_atr, (xs[0] - 60, y0 + 150, 2020, 900), dur=0.6)
    shake(t_atr, 20)
    sfx(t_atr, "golpe-climax", 0.5)
    for i, x in enumerate(xs):
        hearts(f"hc{i}-", x + 300, y0 + 220, 5, t_atr + 0.1 + i * 0.08, spread=420, rise=420)
    js(f'tl.to("#hs0, #hs1, #hs2", {{y:-16, duration:0.18, yoyo:true, repeat:1, stagger:0.06}}, {t_casa:.3f});')
    # comentarios
    t_si, t_mau, t_fer, t_ayu, t_cue, t_com = P("si"), P("mauri", 7), P("fernando", 4), P("ayudaron"), P("cuentalo"), P("comentarios")
    cam(t_si, (230, y0 + 200, 1740, 1090), dur=0.7)
    slide_in("#cta", t_si, dy=200, dur=0.5)
    js(f'tl.fromTo("#mau5", {{x:-500, opacity:0}}, {{x:0, opacity:1, duration:0.7, ease:"power2.out"}}, {t_mau - 0.2:.3f}); walk("mau5", {t_mau - 0.2:.3f}, {t_mau + 0.5:.3f}, 0.14);')
    js(f'face("fer5", -1, 0); tl.fromTo("#fer5", {{x:500, opacity:0}}, {{x:0, opacity:1, duration:0.7, ease:"power2.out"}}, {t_fer - 0.2:.3f}); walk("fer5", {t_fer - 0.2:.3f}, {t_fer + 0.5:.3f}, 0.14);')
    life("mau5", t_mau + 0.5, G.DUR, 31)
    life("fer5", t_fer + 0.5, G.DUR, 32)
    js(f'wave("mau5", {t_mau + 0.6:.3f}, {G.DUR - 0.05:.3f}); wave("fer5", {t_fer + 0.7:.3f}, {G.DUR - 0.05:.3f});')
    type_on("#cta-t .kc", len(cta), t_ayu, t_cue + 0.3)
    js(f'tl.fromTo("#caret", {{opacity:1}}, {{opacity:0, duration:0.3, repeat:{int((G.DUR - t_si) / 0.3)}, yoyo:true, ease:"steps(1)"}}, {t_si:.3f});')
    js(f'tl.fromTo("#cur2", {{opacity:0, x:300, y:300}}, {{opacity:1, x:0, y:0, duration:0.6, ease:"power2.out"}}, {t_cue:.3f});')
    js(f'tl.to("#cur2", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#cta-btn", {{scale:0.92, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    js(f'tl.to("#cta-btn", {{backgroundColor:"#166534", duration:0.2}}, {t_com + 0.4:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    sfx(t_com + 0.45, "check", 0.4)
    hearts("hf-", 1100, y0 + 160, 6, t_com + 0.45, spread=1300, rise=300)


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#11131a; border:4px solid rgba(255,255,255,0.25); color:#fff; font:900 46px {FONT}; text-align:center; line-height:62px; }}
.ypill {{ position:absolute; right:0; top:34px; padding:6px 26px; border-radius:999px; background:#fff; color:{INK}; font:900 56px {FONT}; }}
#tv0 {{ background:#2a2e3a; border-radius:60px; box-shadow:0 30px 80px rgba(0,0,0,0.5); }}
#tv0 .screen {{ position:absolute; left:40px; top:40px; right:160px; bottom:40px; border-radius:40px; background:#05060a;
  display:flex; flex-direction:column; align-items:center; justify-content:center; }}
#tv0 .ant {{ position:absolute; top:-90px; width:10px; height:110px; background:#8b93a7; border-radius:5px; }}
#tv0 .a1 {{ left:260px; transform-origin:50% 100%; rotate:-25deg; }} #tv0 .a2 {{ left:440px; transform-origin:50% 100%; rotate:25deg; }}
#tv0 .knob {{ position:absolute; right:45px; width:74px; height:74px; border-radius:50%; background:#8b93a7; }}
#tv0 .k1 {{ top:120px; }} #tv0 .k2 {{ top:250px; }}
.chip {{ font:900 50px {FONT}; color:#fff; padding:14px 34px; border-radius:999px; white-space:nowrap; box-shadow:0 14px 30px rgba(0,0,0,0.4); }}
.ward {{ background:#6b4426; border-radius:18px; border:10px solid #4a2d17; }}
.ward-top {{ position:absolute; left:-24px; right:-24px; top:-40px; height:40px; background:#4a2d17; border-radius:12px 12px 0 0; }}
.wdoor {{ background:linear-gradient(90deg,#8b5a32,#9c6a3e); border:5px solid #4a2d17; border-radius:8px; }}
.knobw {{ position:absolute; left:18px; top:230px; width:20px; height:60px; border-radius:10px; background:#e8d3a8; }}
.knobw.r {{ left:auto; right:18px; }}
.tagt {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font:900 96px {FONT}; color:#fff; white-space:nowrap; }}
.sttxt {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font:900 56px {FONT}; color:#fff; }}
.notif {{ border-radius:30px; background:rgba(255,255,255,0.96); display:flex; align-items:center; gap:24px; padding-left:24px;
  font:800 48px {FONT}; color:{INK}; box-shadow:0 14px 30px rgba(0,0,0,0.35); white-space:nowrap; }}
.nicon {{ width:70px; height:70px; border-radius:20px; background:{GOOD_BG}; display:flex; align-items:center; justify-content:center; flex:none; }}
.mav {{ position:absolute; left:40px; top:50px; width:170px; height:170px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
.xdot .xa, .xdot .xb {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }}
.hroof {{ position:absolute; left:-30px; right:-30px; top:0; height:200px; background:#c2410c; clip-path:polygon(50% 0, 100% 100%, 0 100%); }}
.hbody {{ position:absolute; left:0; right:0; top:200px; bottom:0; background:#2b2f3d; border-radius:0 0 20px 20px; border:6px solid #3b4152; }}
.win {{ position:absolute; left:50px; right:50px; top:50px; height:380px; border-radius:22px; background:#0d1018; border:10px solid #8b93a7; }}
.wchat {{ position:absolute; left:26px; right:26px; top:30px; font:900 62px {FONT}; color:{INK}; line-height:1.12; }}
.ctab {{ border-radius:56px; background:#fff; box-shadow:0 30px 80px rgba(0,0,0,0.5); }}
.ctab .cbtn {{ right:50px; bottom:40px; font-size:84px; padding:18px 56px; }}
.cf {{ border-radius:4px; opacity:0; }}
.heart {{ opacity:0; }}
.htitle {{ font-size:78px; top:26px; }}
.mc, .kc, .w0c, .w1c, .w2c {{ opacity:0; }}
"""


SPANS = {  # (primera palabra, n) -> tramo de voz que corresponde a cada escena
    "scene_hook": ("antes", 1, "uno", 1), "scene_armario": ("uno", 1, "dos", 1), "scene_bea": ("dos", 1, "una", 1),
    "scene_tabu": ("una", 1, "tres", 1), "scene_ley": ("tres", 1, "ano", 1), "scene_boda": ("ano", 1, "cuatro", 1),
    "scene_merlo": ("cuatro", 1, "adria", 1), "scene_collado": ("adria", 1, "y", 99), "scene_climax": ("muchos", 1, None, 0)}


def _guard(fn):
    def run():
        before = set(G.SYNC)
        fn()
        a, na, b, nb = SPANS[fn.__name__]
        lo = P(a, na) - 1.0
        hi = G.DUR + 1 if b is None or nb == 99 else P(b, nb) + 1.2
        for k in set(G.SYNC) - before:
            t = G.SYNC[k]["empieza"]
            if not lo <= t <= hi:
                raise SystemExit(f"{fn.__name__}: el anclaje {k} ({t}s) cae fuera de su tramo de voz [{lo:.1f}, {hi:.1f}]")
    return run


def build():
    global scene_hook, scene_armario, scene_bea, scene_tabu, scene_ley, scene_boda, scene_merlo, scene_collado, scene_climax
    scene_hook, scene_armario, scene_bea, scene_tabu, scene_ley, scene_boda, scene_merlo, scene_collado, scene_climax = map(
        _guard, (scene_hook, scene_armario, scene_bea, scene_tabu, scene_ley, scene_boda, scene_merlo, scene_collado, scene_climax))
    world()
    scene_hook()
    scene_armario()
    scene_bea()
    scene_tabu()
    scene_ley()
    scene_boda()
    scene_merlo()
    scene_collado()
    scene_climax()
