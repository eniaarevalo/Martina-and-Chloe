"""Escenas del vídeo «¿Por qué queremos a Antonio Recio?». Un solo mundo: un camino en zigzag
(Montepinar -> la distancia -> el niño malo -> desconexión moral) que se dibuja mientras viaja la cámara."""
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





# ================================================================= MUNDO
def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#38bdf8"/><stop offset="1" stop-color="#f43f5e"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in [("Montepinar", 0, 570), ("La distancia", 1, 1630), ("El niño malo", 2, 570), ("Desconexión moral", 3, 1630)]:
        add(f'<div class="mile" data-layout-ignore style="{css_box(x - 240, ROAD[r] + 34, 480, 70, 2)}">{lab}</div>')


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    add(character("rec0", "recio", fx + 480, fl - 60, 1.6, z=5))
    add(f'''<div id="counter" class="fcount" style="{css_box(fx + 60, fl - 330, 840, 330, 6)}">
      <div class="ice"></div>{"".join(f'<div class="fish" style="left:{70 + i * 140}px;top:{30 + (i % 2) * 20}px">{icon("fish", 110, "#0369a1", 2.2).replace("<svg", "<svg fill=\"#7dd3fc\"")}</div>' for i in range(5))}
      <div class="csign">MAYORISTA DE MARISCO</div></div>''')
    for k, (tid, txt, y) in enumerate([("tg1", "RACISTA", 40), ("tg2", "HOMÓFOBO", 160), ("tg3", "TIRANO", 280)]):
        add(f'<div id="{tid}" class="tagr" style="{css_box(fx + (40 if k % 2 == 0 else 520), fy + y, None, None, 8)}">{txt}</div>')
    add(f'''<div id="react" class="react" style="{css_box(fx + 160, fy + 30, 640, 160, 9)}">
      {icon("heart", 80, BAD, 2.4).replace("<svg", f"<svg fill=\"{BAD}\"")}<span id="react-n">{roller("rn", "000.000", 72, INK)[0]}</span></div>''')
    rh = round(72 * 1.12)
    cam(0, (fx + 140, fy + 360, 680, 720), whoosh=False)
    cam(0.1, F(0, 0), dur=0.8, ease="power3.out", whoosh=False)
    js(f'tl.fromTo("#rec0", {{y:-400, opacity:0}}, {{y:0, opacity:1, duration:0.45, ease:"bounce.out"}}, 0);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.4, "golpe", 0.45)
    shake(0.42, 14)
    life("rec0", 0.5, G.DUR, 1)
    js(f'tl.to(Q("rec0","brows"), {{rotation:12, svgOrigin:"120 88", duration:0.2}}, 0.4);')
    for tid, w in (("tg1", "racista"), ("tg2", "homofobo"), ("tg3", "tirano")):
        stamp(f"#{tid}", P(w), rot=-8 if tid != "tg2" else 6)
    t_aun, t_pub, t_ado = P("aun"), P("publico"), P("adora")
    js(f'tl.to(".tagr", {{scale:0.55, opacity:0.4, duration:0.4, stagger:0.05}}, {t_aun:.3f});')
    pop("#react", t_pub, sound="pop")
    roll_set("rn", "000000", rh)
    roll_to("rn", "999999", rh, t_ado, dur=1.2, spins=2, stagger=0.05)
    hearts("h0-", fx + 480, fy + 200, 6, t_ado, spread=600, rise=380)


def scene_porque():
    fx, fy, fw, fh = F(0, 1)
    add(f'''<div id="brain" style="{css_box(fx + 255, fy + 60, 450, 450, 5)}">{icon("brain", 450, "#f9a8d4", 1.6)}</div>''')
    add(f'<div id="qmark" style="{css_box(fx + 700, fy + 40, 180, 220, 6)}font:900 200px {FONT};color:{ACC};text-align:center;line-height:220px">?</div>')
    for i in range(3):
        add(f'<div id="sl{i}" class="slot" style="{css_box(fx + 90 + i * 280, fy + 640, 220, 220, 6)}">{i + 1}</div>')
    t_por, t_psi, t_tres = P("por"), P("psicologia"), P("tres")
    travel(t_por, F(0, 1), 0, 1630, dur=0.7)
    pop("#qmark", t_por + 0.2, sound="pop2")
    js(f'tl.to("#qmark", {{rotation:12, y:-14, duration:0.3, yoyo:true, repeat:5, ease:"sine.inOut"}}, {t_por + 0.6:.3f});')
    pop("#brain", t_psi, sound="pop")
    js(f'tl.to("#brain", {{scale:1.05, duration:0.6, yoyo:true, repeat:{int((G.DUR - t_psi) / 0.6)}, ease:"sine.inOut"}}, {t_psi + 0.4:.3f});')
    js(f'tl.fromTo(".slot", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.35, stagger:0.12, ease:"back.out(2)"}}, {t_tres:.3f});')
    sfx(t_tres, "pop2", 0.3)
    cam(E("respuestas") + 0.05, ROW(0), dur=0.4)


# ================================================================= 1 · LA DISTANCIA
def scene_estudio():
    fx, fy, fw, fh = F(1, 1)
    header("h1", fx, fy, "1", "LA DISTANCIA")
    card("est", fx, fy + 170, fw, 250, f'''
      <div style="position:absolute;left:36px;top:40px">{icon("graduation-cap", 120, INK, 2.2)}</div>
      <div style="position:absolute;left:190px;top:34px;font:900 70px {FONT};color:{INK}">Estudio · 2010</div>
      <div id="est-u" style="position:absolute;left:190px;top:130px;font:800 54px {FONT};color:#555;opacity:0">Universidad de Colorado</div>''')
    parts = [("f1", "INMORAL", BAD, "inmoral"), ("f2", "INOFENSIVO", GOOD_BG, "inofensivo"), ("f3", "RISA", ACC, "gracia")]
    add(f'''<div id="form" style="{css_box(fx, fy + 470, fw, 300, 6)}">
      <div id="f1" class="fpart" style="left:0;top:0;background:{BAD}">INMORAL</div>
      <div class="fop" style="left:420px;top:10px">+</div>
      <div id="f2" class="fpart" style="left:500px;top:0;background:{GOOD_BG}">INOFENSIVO</div>
      <div class="fop" style="left:150px;top:180px">=</div>
      <div id="f3" class="fpart" style="left:240px;top:170px;background:{ACC};color:{INK}">{icon("laugh", 70, INK, 2.6)} RISA</div></div>''')
    t_uno, t_dis, t_10, t_col, t_inm, t_gra, t_ino = (P("uno"), P("distancia"), P("2010"), P("colorado"), P("inmoral"),
                                                      P("gracia"), P("inofensivo"))
    travel(t_uno, F(1, 1), 1, 1630, dur=0.85)
    header_in("h1", t_uno, t_dis)
    slide_in("#est", t_10, dy=-60)
    js(f'tl.fromTo("#est-u", {{opacity:0, x:-20}}, {{opacity:1, x:0, duration:0.3}}, {t_col:.3f});')
    pop("#f1", t_inm, sound="pop")
    pop("#f3", t_gra, sound="pop")
    pop("#f2", t_ino, sound="pop")
    js('tl.set(".fop", {opacity:0}, 0);')
    js(f'tl.to(".fop", {{opacity:1, duration:0.2}}, {t_gra:.3f});')


def scene_tele():
    fx, fy, fw, fh = F(1, 0)
    add(f'''<div id="tv" style="{css_box(fx + 470, fy + 40, 480, 420, 5)}">
      <div class="screen" id="tv-s"></div><div class="knob k1"></div><div class="knob k2"></div></div>''')
    add(character("rec2", "recio", fx + 640, fy + 400, 0.68, z=6))
    add(f'''<div id="meter" class="meter" style="{css_box(fx + 20, fy + 60, 400, 400, 6)}">
      <div class="mlab">DISTANCIA</div><div class="mbar"><div id="mfill" class="mfill"></div></div>
      <div class="mlab" style="margin-top:20px">RISA</div><div class="mbar"><div id="rfill" class="mfill" style="background:{ACC}"></div></div></div>''')
    q = "«Como vecino no lo soportarías; por la tele, sí»"
    add(f'''<div id="qj" class="bubble big" style="{css_box(fx + 20, fy + 500, 920, None, 8)}">
      <div style="font:900 46px {FONT};color:#666;margin-bottom:8px">JORDI SÁNCHEZ</div>
      <div id="qj-t" style="font:900 56px {FONT};color:{INK};line-height:1.12">{chars(q, "qc")}</div></div>''')
    add(f'<div id="door" class="opt2" style="{css_box(fx + 60, fy + 840, 400, 220, 6)}">{icon("door-closed", 110, INK, 2.2)}<div id="door-x" class="okb" style="background:{BAD}">{icon("x", 60, "#fff", 3.4)}</div></div>')
    add(f'<div id="tvok" class="opt2" style="{css_box(fx + 500, fy + 840, 400, 220, 6)}">{icon("tv", 110, INK, 2.2)}<div id="tv-ok" class="okb" style="background:{GOOD_BG}">{icon("check", 60, "#fff", 3.4)}</div></div>')
    t_y, t_pan, t_dis2, t_ino2 = P("y", 3), P("pantalla"), P("distancia", 2), P("inofensivo", 2)
    travel(t_y, F(1, 0), 1, 570, dur=0.7)
    pop("#tv", t_pan, sound="pop")
    js(f'tl.to("#tv-s", {{backgroundColor:"#1d3fa8", duration:0.2}}, {t_pan + 0.1:.3f});')
    js(f'tl.fromTo("#rec2", {{opacity:0, scale:0.4, transformOrigin:"50% 100%"}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_pan + 0.2:.3f});')
    life("rec2", 0, G.DUR, 3)
    pop("#meter", t_dis2 - 0.1, sound=None)
    js('tl.set("#mfill, #rfill", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to("#mfill", {{scaleX:0.9, duration:0.6, ease:"power2.out"}}, {t_dis2:.3f}); tl.to("#rfill", {{scaleX:0.95, duration:0.6, ease:"power2.out"}}, {t_ino2:.3f});')
    sfx(t_ino2, "pop2", 0.3)
    t_jor, t_com, t_tel = P("jordi"), P("como"), P("tele")
    pop("#qj", t_jor, sound="pop2")
    type_on("#qj-t .qc", len(q), t_com, t_tel + 0.3)
    pop("#door", P("vecino"), sound="pop2")
    stamp("#door-x", P("soportarias"), rot=0)
    pop("#tvok", t_tel, sound="pop2")
    sfx(t_tel + 0.2, "check", 0.4)
    cam(E("si") + 0.05, ROW(1), dur=0.4)


# ================================================================= 2 · EL NIÑO MALO
def scene_nino():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h2", fx, fy, "2", "EL NIÑO MALO")
    add(character("rec3", "recio", fx + 300, fl, 1.4, z=6))
    for i in range(4):
        add(f'''<div id="fail{i}" class="notif" style="{css_box(fx + 520, fy + 190 + i * 130, 420, 110, 8)}">
          <div class="nicon" style="background:{BAD}">{icon("x", 50, "#fff", 3.2)}</div><span>FALLO</span></div>''')
    add(f'''<div id="tant" style="{css_box(fx + 520, fy + 750, 420, 300, 7)}">
      <div id="tant-a" class="bigb" style="background:{BAD}">{icon("angry", 160, "#fff", 2.2)}</div>
      <div id="tant-b" class="bigb" style="background:#ec4899;opacity:0">{icon("heart", 170, "#fff", 2.2).replace("<svg", "<svg fill=\"#fff\"")}</div></div>''')
    card("jordi", fx, fy + 190, 500, 150, f'''
      <div style="position:absolute;left:24px;top:30px">{icon("user", 90, INK, 2.2)}</div>
      <div style="position:absolute;left:120px;top:20px;font:900 48px {FONT};color:{INK};white-space:nowrap">Jordi Sánchez</div>
      <div style="position:absolute;left:120px;top:82px;font:800 46px {FONT};color:#555">el actor</div>''')
    t_dos, t_nin, t_rec, t_mal, t_enf, t_cri = P("dos"), P("nino"), P("recio", 2), P("mal"), P("enfada"), P("crio")
    travel(t_dos, F(2, 0), 2, 570, dur=0.85)
    header_in("h2", t_dos, t_nin)
    life("rec3", 0, G.DUR, 4)
    for i, t in enumerate([t_rec, t_rec + 0.4, t_mal, t_mal + 0.3]):
        js(f'tl.fromTo("#fail{i}", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.35, ease:"bounce.out"}}, {t:.3f});')
        sfx(t, "pop2", 0.25)
    # rabieta: pataleo y cara roja
    js(f'tl.to(Q("rec3","head").querySelector("circle"), {{attr:{{fill:"#f87171"}}, duration:0.3}}, {t_enf:.3f});')
    js(f'tl.to(Q("rec3","legL"), {{rotation:-30, svgOrigin:PIV.legL, duration:0.1, yoyo:true, repeat:9}}, {t_enf:.3f}); tl.to(Q("rec3","legR"), {{rotation:30, svgOrigin:PIV.legR, duration:0.1, yoyo:true, repeat:9}}, {t_enf + 0.05:.3f});')
    js(f'tl.to(Q("rec3","armL"), {{rotation:-140, svgOrigin:PIV.armL, duration:0.12, yoyo:true, repeat:7}}, {t_enf:.3f}); tl.to(Q("rec3","armR"), {{rotation:140, svgOrigin:PIV.armR, duration:0.12, yoyo:true, repeat:7}}, {t_enf + 0.06:.3f});')
    pop("#tant", t_cri, sound="golpe", vol=0.3)
    t_act, t_inf, t_car = P("actor"), P("infantil"), P("carino")
    js(f'tl.set("#jordi", {{opacity:0}}, 0); tl.to("#fail0, #fail1, #fail2, #fail3", {{opacity:0, x:200, duration:0.3, stagger:0.05}}, {t_act - 0.2:.3f});')
    slide_in("#jordi", t_act, dy=-40, sound=None)
    js(f'tl.to(Q("rec3","head").querySelector("circle"), {{attr:{{fill:"#efc09a"}}, duration:0.4}}, {t_inf:.3f});')
    flip("#tant", t_car, ["#tant-a"], ["#tant-b"])
    hearts("h2-", fx + 730, fy + 700, 5, t_car + 0.2, spread=300, rise=300)
    cam(E("carino") + 0.05, ROW(2), dur=0.4)


# ================================================================= 3 · DESCONEXIÓN MORAL
def scene_moral():
    fx, fy, fw, fh = F(3, 1)
    header("h3", fx, fy, "3", "DESCONEXIÓN")
    card("jm", fx, fy + 170, 440, 380, f'''
      <div style="position:absolute;left:0;right:0;top:20px;text-align:center;font:900 46px {FONT};color:{INK}">JUICIO MORAL</div>
      <div style="position:absolute;left:0;right:0;top:80px;text-align:center">{icon("scale", 170, INK, 2.0)}</div>
      <div id="jm-l" class="lamp2" style="background:{BAD}"></div>''')
    add(f'<div id="plug" style="{css_box(fx + 330, fy + 590, 150, 150, 7)}">{icon("plug-zap", 140, ACC, 2.2)}</div>')
    card("enj", fx + 500, fy + 170, 460, 380, f'''
      <div style="position:absolute;left:0;right:0;top:20px;text-align:center;font:900 46px {FONT};color:{INK}">DISFRUTE</div>
      <svg style="position:absolute;left:30px;top:90px" width="400" height="260" viewBox="0 0 400 260">
        <path d="M 20 240 L 380 240" stroke="#e5e7eb" stroke-width="6"/>
        <path id="enj-l" d="M 20 230 L 140 190 L 260 110 L 380 20" stroke="{GOOD}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>''')
    add(f'<div id="sat" class="stamp" style="{css_box(fx + 140, fy + 780, None, None, 9)}color:#2563eb;border-color:#2563eb;font-size:80px">SÁTIRA</div>')
    add(character("rec4", "recio", fx + 800, floor(3), 1.0, z=5))
    t_tres, t_des, t_est, t_dis, t_juz = P("tres", 2), P("desconexion"), P("estudios"), P("disfrutar"), P("juzgarlo")
    travel(t_tres, F(3, 1), 3, 1630, dur=0.85)
    header_in("h3", t_tres, t_des)
    pop("#jm", t_est, sound="pop")
    pop("#enj", P("personaje"), sound="pop")
    js('tl.set("#enj-l", {strokeDasharray:600, strokeDashoffset:600}, 0);')
    js(f'tl.to("#enj-l", {{strokeDashoffset:0, duration:0.7, ease:"power2.out"}}, {t_dis:.3f});')
    js(f'tl.fromTo("#plug", {{opacity:0}}, {{opacity:1, duration:0.2}}, {t_dis - 0.2:.3f}); tl.to("#plug", {{x:120, y:200, rotation:60, opacity:0.4, duration:0.5, ease:"power2.in"}}, {t_juz:.3f});')
    js(f'tl.to("#jm-l", {{backgroundColor:"#374151", duration:0.2}}, {t_juz + 0.2:.3f}); tl.to("#jm", {{opacity:0.55, duration:0.3}}, {t_juz + 0.2:.3f});')
    sfx(t_juz + 0.15, "click", 0.4)
    life("rec4", 0, G.DUR, 5)
    t_seg, t_cri = P("segun"), P("critica")
    stamp("#sat", t_cri, rot=-8)
    js(f'tl.fromTo("#rec4", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_seg:.3f});')


def scene_heroe():
    fx, fy, fw, fh = F(3, 0)
    add(f'''<div id="post" style="{css_box(fx + 180, fy + 20, 600, 640, 6)}" class="poster">
      <div id="post-a" class="pin"><div class="ptxt" style="color:#2563eb">SÁTIRA</div></div>
      <div id="post-b" class="pin" style="opacity:0;background:linear-gradient(#fde68a,#f59e0b)">
        <div class="ptxt" style="color:{INK}">MI HÉROE</div>{"".join(f'<div class="stars" style="left:{40 + i * 120}px">{icon("star", 80, INK, 2).replace("<svg", f"<svg fill=\"{INK}\"")}</div>' for i in range(5))}</div></div>''')
    add(character("rec5", "recio", fx + 480, fy + 600, 1.0, z=7))
    add(f'<div id="alarm" style="{css_box(fx + 790, fy + 20, 150, 150, 8)}">{icon("siren", 140, BAD, 2.2)}</div>')
    card("poll", fx + 60, fy + 700, 840, 360, f'''
      <div style="position:absolute;left:40px;top:28px;font:900 60px {FONT};color:{INK}">¿Y tú?</div>
      <div id="o1" class="opt" style="top:110px;border-color:{BAD}">TE RÍES DE RECIO</div>
      <div id="o2" class="opt" style="top:230px;border-color:{GOOD}">TE RÍES CON RECIO</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 760, fy + 1000, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_aun2, t_cre, t_heroe, t_tu, t_de, t_con, t_cmt = (P("aun", 2), P("creador"), P("heroe"), P("tu"), P("de", P_n("de")),
                                                       P("con"), P("comenta"))
    travel(t_aun2 - 0.3, F(3, 0), 3, 570, dur=0.7)
    js(f'tl.fromTo("#post", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_aun2 - 0.1:.3f});')
    life("rec5", 0, G.DUR, 6)
    js(f'tl.fromTo("#rec5", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_aun2:.3f});')
    # CLÍMAX
    flip("#post", t_heroe, ["#post-a"], ["#post-b"], sound=None)
    shake(t_heroe + 0.05, 22)
    sfx(t_heroe, "golpe-climax", 0.55)
    js(f'tl.fromTo("#alarm", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(3)"}}, {t_heroe + 0.1:.3f});')
    js(f'tl.to("#alarm", {{opacity:0.3, duration:0.2, yoyo:true, repeat:{int((G.DUR - t_heroe) / 0.2)}}}, {t_heroe + 0.4:.3f});')
    js(f'jump("rec5", {t_heroe + 0.2:.3f}, 60); wave("rec5", {t_heroe + 0.6:.3f}, {G.DUR - 0.05:.3f});')
    pop("#poll", t_tu, sound="pop")
    pop("#o1", t_de, sound="pop2")
    pop("#o2", t_con, sound="pop2")
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_con + 0.1:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_cmt:.3f}); tl.to("#o2", {{backgroundColor:"#dcfce7", scale:1.04, duration:0.2}}, {t_cmt + 0.05:.3f});')
    sfx(t_cmt, "click", 0.5)
    cam(t_cmt + 0.5, (0, 100, 2200, 5200), dur=0.8, box=dict(x=60, y=390, w=960, h=1100))


def P_n(word):
    """Índice de la última vez que se dice `word` antes de «con» en la frase final."""
    import gen
    seq = [i for i in range(len(gen.NW)) if gen.NW[i] == "de"]
    tcon = P("con")
    return max(k + 1 for k, i in enumerate(seq) if gen.WORDS[i]["start"] < tcon)


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:78px; top:26px; }}
.fcount {{ background:#e2e8f0; border-radius:20px 20px 0 0; border-top:16px solid #94a3b8; }}
.ice {{ position:absolute; left:20px; right:20px; top:10px; height:150px; border-radius:12px; background:repeating-linear-gradient(90deg,#f1f5f9 0 30px,#e0f2fe 30px 60px); }}
.fish {{ position:absolute; }}
.csign {{ position:absolute; left:0; right:0; bottom:40px; text-align:center; font:900 56px {FONT}; color:#0f172a; }}
.tagr {{ font:900 70px {FONT}; color:#fff; background:{BAD}; padding:6px 30px; border-radius:20px; box-shadow:0 14px 30px rgba(0,0,0,0.4); opacity:0; white-space:nowrap; }}
.react {{ border-radius:40px; background:#fff; display:flex; align-items:center; justify-content:center; gap:28px; box-shadow:0 20px 50px rgba(0,0,0,0.45); }}
.slot {{ border-radius:30px; border:8px dashed rgba(255,255,255,0.6); color:#fff; font:900 120px {FONT}; text-align:center; line-height:204px; }}
.fpart {{ position:absolute; height:130px; padding:0 34px; border-radius:30px; color:#fff; font:900 64px {FONT}; line-height:130px; white-space:nowrap; display:flex; align-items:center; gap:16px; }}
.fop {{ position:absolute; font:900 90px {FONT}; color:#fff; }}
#tv {{ background:#2a2e3a; border-radius:46px; box-shadow:0 30px 80px rgba(0,0,0,0.5); }}
#tv .screen {{ position:absolute; left:30px; top:30px; right:120px; bottom:30px; border-radius:30px; background:#05060a; }}
#tv .knob {{ position:absolute; right:32px; width:58px; height:58px; border-radius:50%; background:#8b93a7; }}
#tv .k1 {{ top:90px; }} #tv .k2 {{ top:200px; }}
.meter {{ border-radius:36px; background:#fff; padding:36px; box-shadow:0 20px 50px rgba(0,0,0,0.45); }}
.mlab {{ font:900 50px {FONT}; color:{INK}; }}
.mbar {{ margin-top:12px; height:60px; border-radius:30px; background:#e5e7eb; overflow:hidden; }}
.mfill {{ width:100%; height:100%; background:#38bdf8; border-radius:30px; }}
.opt2 {{ border-radius:36px; background:#fff; display:flex; align-items:center; justify-content:center; box-shadow:0 14px 30px rgba(0,0,0,0.35); }}
.okb {{ position:absolute; right:24px; top:24px; width:90px; height:90px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
.notif {{ border-radius:28px; background:rgba(255,255,255,0.96); display:flex; align-items:center; gap:22px; padding-left:22px;
  font:900 56px {FONT}; color:{BAD}; box-shadow:0 14px 30px rgba(0,0,0,0.35); white-space:nowrap; opacity:0; }}
.nicon {{ width:76px; height:76px; border-radius:22px; display:flex; align-items:center; justify-content:center; flex:none; }}
.bigb {{ position:absolute; inset:0; border-radius:50px; display:flex; align-items:center; justify-content:center; }}
.lamp2 {{ position:absolute; left:50%; bottom:24px; width:56px; height:56px; margin-left:-28px; border-radius:50%; }}
.poster {{ border-radius:24px; overflow:hidden; box-shadow:0 30px 70px rgba(0,0,0,0.5); }}
.pin {{ position:absolute; inset:0; background:#e0e7ff; }}
.ptxt {{ position:absolute; left:0; right:0; top:40px; text-align:center; font:900 110px {FONT}; }}
.stars {{ position:absolute; top:190px; }}
.opt {{ position:absolute; left:40px; right:40px; height:100px; border-radius:30px; border:8px solid; background:#fff; font:900 56px {FONT}; color:{INK}; text-align:center; line-height:84px; }}
.qc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_porque()
    scene_estudio()
    scene_tele()
    scene_nino()
    scene_moral()
    scene_heroe()
