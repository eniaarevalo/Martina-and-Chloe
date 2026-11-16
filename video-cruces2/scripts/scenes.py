"""Escenas del vídeo «4 cruces que nunca viste. Parte 2» (CRUCE IMAGINADO). Un solo mundo: camino en zigzag
(los dos edificios -> Nines × Alicia -> Belén × Amador -> Paloma × Fina -> Emilio × Coque -> encuesta)."""
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


def ico(iid, x, y, size, name, col, z=9, fill=None, sw=2.4):
    svg = icon(name, size, col, sw)
    if fill:
        svg = svg.replace("<svg", f'<svg fill="{fill}"')
    add(f'<div id="{iid}" data-layout-ignore style="{css_box(x, y, size, size, z)}opacity:0">{svg}</div>')


# ================================================================= GANCHO: parte 2
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    building("bA", fx + 40, fy + 400, 400, 600, "DESENGAÑO 21", "#8a4b2f", "#fcd34d", "#fef3c7", "#7c2d12")
    building("bB", fx + 520, fy + 400, 400, 600, "MONTEPINAR", "#e2e8f0", "#38bdf8", "#0f766e", "#fff")
    add(f'<div id="p2" class="stampbox" style="{css_box(fx + 230, fy + 160, 500, 170, 11)}opacity:0">PARTE 2</div>')
    ico("spk", fx + 400, fy + 560, 160, "zap", ACC, fill="#ffd43b")
    for k, (x, y) in enumerate([(300, 470), (560, 440), (440, 380)]):
        ico(f"fl{k}", fx + x, fy + y, 120, "flame", "#f97316", z=10, fill="#fdba74")
    add(f'<div id="peor" class="pill" style="{css_box(fx + 330, fy + 360, None, None, 12)}background:{BAD};color:#fff;font-size:64px;opacity:0">PEOR</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: sello PARTE 2 y los edificios entran de golpe
    stamp("#p2", 0.05, rot=-6)
    js('tl.fromTo("#bA", {x:-460, opacity:1}, {x:-60, duration:0.5, ease:"power3.out"}, 0.1);')
    js('tl.fromTo("#bB", {x:460, opacity:1}, {x:60, duration:0.5, ease:"power3.out"}, 0.1);')
    sfx(0.1, "whoosh", 0.35)
    t_cru, t_ave, t_pe = P("cruzar"), P("avecina"), P("peor")
    js(f'tl.to("#p2", {{opacity:0, y:-40, duration:0.3}}, {t_cru - 0.3:.3f});')
    js(f'tl.to("#bA", {{x:0, duration:0.4, ease:"power2.in"}}, {t_cru:.3f}); tl.to("#bB", {{x:0, duration:0.4, ease:"power2.in"}}, {t_cru:.3f});')
    js(f'tl.fromTo("#spk", {{opacity:0, scale:0.3, rotation:-30}}, {{opacity:1, scale:1, rotation:0, duration:0.3, ease:"back.out(3)"}}, {t_cru + 0.4:.3f});')
    sfx(t_cru + 0.4, "golpe", 0.45)
    shake(t_cru + 0.4, 14)
    for k in range(3):
        js(f'tl.fromTo("#fl{k}", {{opacity:0, scale:0.2, y:40}}, {{opacity:1, scale:1, y:0, duration:0.3, ease:"back.out(2.5)"}}, {t_pe - 0.5 + k * 0.1:.3f});')
        js(f'tl.to("#fl{k}", {{scaleY:1.15, duration:0.15, yoyo:true, repeat:5}}, {t_pe - 0.2 + k * 0.05:.3f});')
    stamp("#peor", t_pe - 0.2, rot=8)
    shake(t_pe + 0.1, 20)


# ================================================================= 1 · NINES × ALICIA
def scene_piso():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "1", "NINES × ALICIA", color="#9333ea", txt="#fff")
    add(f'<div id="sink" class="sink" style="{css_box(fx + 290, fl - 250, 200, 240, 3)}opacity:0"></div>')
    add("".join(f'<div id="pl{k}" class="plato" data-layout-ignore style="{css_box(fx + 300, fl - 270 - k * 30, 180, 34, 4)}opacity:0"></div>' for k in range(10)))
    add(f'<div id="frg" class="fridge" style="{css_box(fx + 790, fl - 520, 160, 500, 3)}opacity:0"><b id="sos">SOS</b></div>')
    add(character("ni1", "nines", fx + 160, fl, 1.2, z=5))
    add(character("al1", "alicia", fx + 620, fl, 1.2, z=6))
    nn = bubble("sbn", fx + 10, fy + 180, 520, "NINES", "A ver, guapa, aquí cada una friega lo suyo.", "#9333ea", "l", fs=44)
    na = bubble("sba", fx + 450, fy + 280, 480, "ALICIA", "Perfecto. Pues lo mío… mañana.", "#06b6d4", "r", fs=44)
    add(f'<div id="sem" class="pill" style="{css_box(fx + 200, fy + 190, None, None, 10)}background:#fff;color:{INK};font-size:48px;opacity:0">'
        f'{icon("calendar", 46, INK, 2.6)} 1 SEMANA DESPUÉS</div>')
    t_uno, t_nin, t_ali, t_pis = P("uno"), P("nines"), P("alicia"), P("piso")
    travel(t_uno - 0.3, F(0, 1), 0, 1630, dur=0.7)
    header_in("h1", t_uno, t_nin)
    life("ni1", 0, G.DUR, 1)
    life("al1", 0, G.DUR, 2)
    js(f'tl.fromTo("#ni1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_nin:.3f});')
    js(f'tl.fromTo("#al1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_ali:.3f});')
    js(f'tl.fromTo("#sink, #frg", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_pis - 0.2:.3f});')
    t_n2, t_fri, t_a2, t_man = P("nines", 2), P("friega"), P("alicia", 2), P("manana")
    say("sbn", nn, "ni1", t_n2 + 0.3, E("suyo"), from_x=-60)
    js(f'point("ni1", "R", {t_fri - 0.2:.3f}, {t_fri + 1.0:.3f}, -70);')
    js(f'tl.to("#sbn", {{opacity:0.25, scale:0.92, duration:0.3}}, {t_a2 - 0.3:.3f});')
    say("sba", na, "al1", t_a2 + 0.2, E("manana"), from_x=60)
    js(f'tl.to(Q("al1","head"), {{rotation:-14, svgOrigin:PIV.head, duration:0.4}}, {t_man:.3f});')
    t_sem, t_pla, t_nev, t_aux = P("semana"), P("plato"), P("nevera"), P("auxilio")
    js(f'tl.to("#sbn, #sba", {{opacity:0, duration:0.25}}, {t_sem - 0.3:.3f});')
    pop("#sem", t_sem - 0.2, sound="pop2")
    for k in range(10):
        js(f'tl.fromTo("#pl{k}", {{opacity:0, y:-60}}, {{opacity:1, y:0, duration:0.18, ease:"back.out(2)"}}, {t_pla - 0.3 + k * 0.1:.3f});')
    sfx(t_pla, "tic-rodillo", 0.3)
    js(f'tl.to("[id^=pl]", {{rotation:3, duration:0.12, yoyo:true, repeat:5}}, {t_nev:.3f});')
    js(f'tl.fromTo("#sos", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(3)"}}, {t_aux - 0.2:.3f});')
    js(f'tl.to("#frg", {{x:10, duration:0.06, yoyo:true, repeat:9}}, {t_aux:.3f});')
    sfx(t_aux, "golpe", 0.35)


# ================================================================= 2 · BELÉN × AMADOR
def scene_cita():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    header("h2", fx, fy, "2", "BELÉN × AMADOR", color="#db2777", txt="#fff")
    add(f'<div id="tbl" class="tbl" style="{css_box(fx + 330, fl - 240, 300, 240, 6)}opacity:0"><i class="cand"></i><i class="flm"></i></div>')
    add(character("be1", "belen", fx + 190, fl, 1.2, z=5))
    add(character("am1", "amador", fx + 770, fl, 1.2, z=5))
    nb = bubble("sbb", fx + 10, fy + 180, 470, "BELÉN", "Mi último novio me dejó por mensaje.", "#db2777", "l", fs=44)
    nm = bubble("sbm", fx + 400, fy + 230, 550, "AMADOR", "Eso no es nada. A mí me han dejado más veces que a un coche mal aparcado.", "#ea580c", "r", fs=40)
    ico("phn", fx + 40, fy + 520, 120, "smartphone", "#f8fafc")
    ico("car", fx + 760, fy + 560, 140, "car", "#38bdf8")
    for k, (x, y) in enumerate([(160, 560), (230, 620), (740, 560), (810, 620)]):
        ico(f"tr{k}", fx + x, fy + y, 60, "droplet", "#38bdf8", z=10, fill="#bae6fd")
    add(f'''<div id="bill" class="card" style="{css_box(fx + 320, fy + 260, 320, 260, 9)}background:#fff;opacity:0">
      <div class="billt">{icon("receipt", 50, INK, 2.6)} CUENTA</div><div class="billn">48 €</div></div>''')
    add(f'<div id="sinp" class="stampbox" style="{css_box(fx + 230, fy + 500, 500, 140, 11)}opacity:0;font-size:76px">SIN PAGAR</div>')
    t_dos, t_bel, t_ama, t_cit = P("dos", 2), P("belen"), P("amador"), P("cita")
    travel(t_dos - 0.3, F(1, 1), 1, 1630, dur=0.7)
    header_in("h2", t_dos, t_bel)
    life("be1", 0, G.DUR, 3)
    life("am1", 0, G.DUR, 4)
    js(f'tl.fromTo("#be1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_bel:.3f});')
    js(f'tl.fromTo("#am1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_ama:.3f});')
    js(f'tl.fromTo("#tbl", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_cit - 0.1:.3f}); tl.to("#tbl .flm", {{scaleY:1.3, duration:0.3, yoyo:true, repeat:{int((G.DUR - t_cit) / 0.3) // 2 * 2 - 1}}}, {t_cit:.3f});')
    t_b2, t_men, t_a2, t_coc, t_apa = P("belen", 2), P("mensaje"), P("amador", 2), P("coche"), P("aparcado")
    say("sbb", nb, "be1", t_b2 + 0.4, E("mensaje"), from_x=-60)
    pop("#phn", t_men - 0.2, sound="pop2")
    js(f'tl.to("#phn", {{rotation:12, duration:0.07, yoyo:true, repeat:7}}, {t_men + 0.1:.3f});')
    js(f'tl.to("#sbb, #phn", {{opacity:0.25, duration:0.3}}, {t_a2 - 0.3:.3f});')
    say("sbm", nm, "am1", t_a2 + 0.3, E("aparcado"), from_x=60)
    js(f'tl.fromTo("#car", {{opacity:0, x:200}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {t_coc - 0.2:.3f});')
    sfx(t_coc, "whoosh-corto", 0.3)
    js(f'jump("am1", {t_apa:.3f}, 30);')
    t_med, t_llo, t_nin, t_car2 = P("media"), P("lloran"), P("ninguno"), P("cartera")
    js(f'tl.to("#sbb, #sbm, #phn, #car", {{opacity:0, duration:0.25}}, {t_med - 0.2:.3f});')
    for k in range(4):
        js(f'tl.fromTo("#tr{k}", {{opacity:0, y:-20}}, {{opacity:1, y:60, duration:0.6, repeat:2}}, {t_llo + k * 0.12:.3f});')
    js(f'tl.to(Q("be1","head"), {{rotation:-12, svgOrigin:PIV.head, duration:0.3}}, {t_llo:.3f}); tl.to(Q("am1","head"), {{rotation:12, svgOrigin:PIV.head, duration:0.3}}, {t_llo:.3f});')
    sfx(t_llo, "pop2", 0.25)
    slide_in("#bill", t_nin - 0.3, dy=-60)
    stamp("#sinp", t_car2 - 0.2, rot=-8)


# ================================================================= 3 · PALOMA × FINA
def scene_mercado():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    header("h3", fx, fy, "3", "PALOMA × FINA", color="#ea580c", txt="#fff")
    add(f'''<div id="stl" class="stall" style="{css_box(fx + 280, fy + 330, 400, 680, 2)}opacity:0">
      <div class="awn"></div><div class="ctr"></div>
      <div class="frt">{"".join(icon(n, 64, c, 2.4).replace("<svg", f'<svg fill="{f}"') for n, c, f in
                                  [("apple", "#b91c1c", "#ef4444"), ("cherry", "#9f1239", "#e11d48"), ("banana", "#ca8a04", "#fde047"), ("apple", "#15803d", "#4ade80")])}</div>
      <div id="shut" class="shut"></div></div>''')
    add(character("fi1", "fina", fx + 190, fl, 1.2, z=5))
    add(character("pa1", "paloma", fx + 770, fl, 1.2, z=5))
    nf = bubble("sbf", fx + 10, fy + 180, 460, "DOÑA FINA", "Señora, que estaba yo antes.", "#64748b", "l", fs=46)
    np_ = bubble("sbp", fx + 470, fy + 250, 470, "PALOMA", "¿Usted? Si acaba de llegar.", "#c2410c", "r", fs=46)
    ico("zp", fx + 410, fy + 520, 140, "zap", ACC, z=10, fill="#ffd43b")
    rr, hh = roller("mn", "00", 110, INK)
    add(f'<div id="mnc" class="card" style="{css_box(fx + 330, fy + 190, 300, 210, 9)}background:#fff;opacity:0"><div class="npn">{rr}</div><div class="npl">MINUTOS</div></div>')
    add(f'<div id="cer" class="stampbox" style="{css_box(fx + 250, fy + 430, 460, 140, 11)}opacity:0;font-size:80px">CERRADO</div>')
    t_tre, t_pal, t_fin, t_col, t_mer = P("tres"), P("paloma"), P("fina"), P("cola"), P("mercado")
    travel(t_tre - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h3", t_tre, t_pal)
    life("fi1", 0, G.DUR, 5)
    life("pa1", 0, G.DUR, 6)
    js(f'tl.fromTo("#pa1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_pal:.3f});')
    js(f'tl.fromTo("#fi1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_fin:.3f});')
    js(f'tl.fromTo("#stl", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_mer - 0.3:.3f});')
    t_f2, t_ant, t_p2, t_lle = P("fina", 2), P("antes"), P("paloma", 2), P("llegar")
    say("sbf", nf, "fi1", t_f2 + 0.4, E("antes"), from_x=-60)
    js(f'point("fi1", "R", {t_ant - 0.5:.3f}, {t_ant + 0.6:.3f}, -60);')
    js(f'tl.to("#sbf", {{opacity:0.3, scale:0.92, duration:0.3}}, {t_p2 - 0.3:.3f});')
    say("sbp", np_, "pa1", t_p2 + 0.3, E("llegar"), from_x=60)
    js(f'tl.to("#pa1", {{x:-40, duration:0.25}}, {t_lle:.3f}); tl.to("#fi1", {{x:40, duration:0.25}}, {t_lle:.3f});')
    js(f'tl.fromTo("#zp", {{opacity:0, scale:0.3, rotation:-30}}, {{opacity:1, scale:1, rotation:0, duration:0.25, ease:"back.out(3)"}}, {t_lle + 0.1:.3f});')
    sfx(t_lle + 0.1, "golpe", 0.4)
    shake(t_lle + 0.15, 10)
    t_die, t_piq, t_cer, t_nad = P("diez"), P("pique"), P("cerrado"), P("nada", 2)
    js(f'tl.to("#sbf, #sbp", {{opacity:0, duration:0.25}}, {t_die - 0.3:.3f});')
    slide_in("#mnc", t_die - 0.2, dy=-60)
    roll_set("mn", "00", hh)
    roll_to("mn", "10", hh, t_die, dur=0.8, spins=1)
    js(f'tl.to("#zp", {{rotation:20, duration:0.1, yoyo:true, repeat:9}}, {t_piq:.3f});')
    js('tl.set("#shut", {scaleY:0, transformOrigin:"50% 0%"}, 0);')
    js(f'tl.to("#shut", {{scaleY:1, duration:0.5, ease:"bounce.out"}}, {t_cer - 0.2:.3f});')
    sfx(t_cer, "puerta", 0.35)
    stamp("#cer", t_cer + 0.1, rot=-6)
    js(f'tl.to(Q("fi1","head"), {{rotation:-15, svgOrigin:PIV.head, duration:0.3}}, {t_nad:.3f}); tl.to(Q("pa1","head"), {{rotation:15, svgOrigin:PIV.head, duration:0.3}}, {t_nad:.3f});')


# ================================================================= 4 · EMILIO × COQUE
def scene_garita():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h4", fx, fy, "4", "EMILIO × COQUE", color="#2f62c0", txt="#fff")
    add(f'<div id="gar" class="garita" style="{css_box(fx + 330, fl - 520, 300, 510, 2)}opacity:0"><div class="gwin"></div><b>CONSERJERÍA</b></div>')
    add(character("em1", "emilio", fx + 200, fl, 1.2, z=5))
    add(character("co1", "coque", fx + 760, fl, 1.2, z=5))
    nc = bubble("sbc", fx + 480, fy + 180, 460, "COQUE", "¿No huele un poco raro aquí?", "#475569", "r", fs=46)
    ne = bubble("sbe", fx + 10, fy + 260, 540, "EMILIO", "¡Un poquito de por favor, que he fregado esta mañana!", "#2f62c0", "l", fs=42)
    for k, (x, y) in enumerate([(560, 560), (640, 500)]):
        ico(f"st{k}", fx + x, fy + y, 110, "wind", "#84cc16", z=9, sw=2.8)
    add(f'<div id="nf" class="stampbox" style="{css_box(fx + 130, fy + 250, 700, 150, 11)}opacity:0;font-size:70px">NO HABÍA FREGADO</div>')
    for k, (x, y) in enumerate([(300, 520), (700, 470), (500, 420)]):
        add(f'<div id="z{k}" class="zz" data-layout-ignore style="{css_box(fx + x, fy + y, 140, 90, 10)}opacity:0">Zzz</div>')
    t_cua, t_emi, t_coq, t_por = P("cuatro"), P("emilio"), P("coque"), P("portero")
    travel(t_cua - 0.3, F(2, 0), 2, 570, dur=0.7)
    header_in("h4", t_cua, t_emi)
    life("em1", 0, G.DUR, 7)
    life("co1", 0, G.DUR, 8)
    js(f'tl.fromTo("#em1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_emi:.3f});')
    js(f'tl.fromTo("#co1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_coq:.3f});')
    js(f'tl.fromTo("#gar", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_por - 0.2:.3f});')
    t_c2, t_hue, t_ra, t_e2, t_poq, t_fre = P("coque", 2), P("huele"), P("raro"), P("emilio", 2), P("poquito"), P("fregado")
    say("sbc", nc, "co1", t_c2 + 0.3, E("aqui", 3), from_x=60)
    for k in range(2):
        js(f'tl.fromTo("#st{k}", {{opacity:0, y:20}}, {{opacity:1, y:-30, duration:0.6}}, {t_hue + k * 0.15:.3f});')
        js(f'tl.to("#st{k}", {{x:15, duration:0.2, yoyo:true, repeat:7}}, {t_hue + 0.6 + k * 0.1:.3f});')
    js(f'tl.to(Q("co1","head"), {{rotation:-10, svgOrigin:PIV.head, duration:0.2, yoyo:true, repeat:3}}, {t_ra:.3f});')
    js(f'tl.to("#sbc", {{opacity:0.25, scale:0.92, duration:0.3}}, {t_e2 - 0.3:.3f});')
    say("sbe", ne, "em1", t_e2 + 0.3, E("manana", 2), from_x=-60)
    js(f'tl.to(Q("em1","armL"), {{rotation:60, svgOrigin:PIV.armL, duration:0.25, ease:"back.out(2)"}}, {t_poq - 0.1:.3f}); tl.to(Q("em1","armR"), {{rotation:-60, svgOrigin:PIV.armR, duration:0.25, ease:"back.out(2)"}}, {t_poq - 0.1:.3f});')
    js(f'tl.to(Q("em1","armL"), {{rotation:0, svgOrigin:PIV.armL, duration:0.3}}, {t_fre + 0.4:.3f}); tl.to(Q("em1","armR"), {{rotation:0, svgOrigin:PIV.armR, duration:0.3}}, {t_fre + 0.4:.3f});')
    sfx(t_poq, "golpe", 0.3)
    t_spo, t_hab, t_sie, t_gar = P("spoiler"), P("habia"), P("siesta"), P("garita")
    js(f'tl.to("#sbc, #sbe", {{opacity:0, duration:0.25}}, {t_spo - 0.3:.3f});')
    stamp("#nf", t_hab - 0.2, rot=-5)
    js(f'tl.to("#nf", {{opacity:0, duration:0.3}}, {t_sie - 0.6:.3f});')
    js(f'tl.to("#em1", {{x:200, duration:0.5}}, {t_sie - 0.4:.3f}); tl.to("#co1", {{x:-200, duration:0.5}}, {t_sie - 0.4:.3f});')
    for c, r in (("em1", 14), ("co1", -14)):
        js(f'tl.to(Q("{c}","head"), {{rotation:{r}, svgOrigin:PIV.head, duration:0.4}}, {t_sie:.3f}); tl.to(Q("{c}","eyes"), {{scaleY:0.08, svgOrigin:PIV.eyes, duration:0.2}}, {t_sie:.3f});')
    for k in range(3):
        js(f'tl.fromTo("#z{k}", {{opacity:0, y:30, scale:0.5}}, {{opacity:1, y:-40, scale:1, duration:0.7, repeat:1}}, {t_sie + k * 0.2:.3f});')
    sfx(t_gar, "pop2", 0.2)


# ================================================================= ENCUESTA
OPTS = [("VICENTA × VICENTE MAROTO", "#8a56b8"), ("MARISA × IZASKUN", "#16a34a"), ("MAURI × PASTOR", "#16a596"), ("CUESTA × RECIO", "#3b82c4")]


def scene_final():
    fx, fy, fw, fh = F(2, 1)
    rows = "".join(f'<div class="poll" style="top:{140 + k * 86}px"><span>{n}</span><i id="pb{k}" style="background:{c}"></i></div>'
                   for k, (n, c) in enumerate(OPTS))
    add(f'''<div id="pollc" class="card" style="{css_box(fx + 40, fy + 220, 880, 520, 6)}background:#fff;opacity:0">
      <div class="polh">{icon("message-circle", 54, INK, 2.6)} ¿CRUCE PARA LA PARTE 3?</div>{rows}</div>''')
    cta = "Yo quiero ver a…"
    add(f'''<div id="cbx" class="card" style="{css_box(fx + 40, fy + 780, 880, 170, 6)}background:#fff;opacity:0">
      <div id="ctt" class="ctt">{chars(cta, "kc")}</div><div id="pub" class="pubb">Publicar</div></div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 800, fy + 900, 90, 90, 12)}opacity:0">{icon("mouse-pointer-2", 90, "#fff", 2.4).replace("<svg", "<svg fill=\"#0f1115\"")}</div>')
    t_que, t_par, t_leo, t_com = P("cruce"), P("parte", 2), P("leo"), P("comentarios")
    travel(t_que - 0.35, F(2, 1), 2, 1630, dur=0.6)
    slide_in("#pollc", t_que - 0.1, dy=-60)
    js('tl.set("[id^=pb]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    for k, w in enumerate([0.85, 0.7, 0.55, 0.75]):
        js(f'tl.to("#pb{k}", {{scaleX:{w}, duration:0.35, ease:"back.out(1.6)"}}, {t_par - 0.3 + k * 0.12:.3f});')
    sfx(t_par, "pop2", 0.25)
    slide_in("#cbx", t_par + 0.2, dy=60, sound=None)
    type_on("#ctt .kc", len(cta), t_leo - 0.2, t_com + 0.3)
    js(f'tl.fromTo("#cur", {{opacity:0, x:160, y:160}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.4:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.4:.3f});')
    sfx(t_com + 0.4, "click", 0.5)
    cam(E("comentarios") + 0.1, (0, 100, 2200, 2700), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


def P_count(word):
    return sum(1 for w in G.NW if w == G.norm(word))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 42px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.htitle {{ font-size:80px; top:26px; }}
.bld {{ border-radius:18px 18px 0 0; border:8px solid rgba(0,0,0,0.25); overflow:hidden; }}
.bsign {{ position:absolute; left:30px; right:30px; top:24px; height:70px; border-radius:14px; font:900 38px {FONT}; text-align:center; line-height:70px; white-space:nowrap; letter-spacing:-1px; }}
.win {{ position:absolute; width:70px; height:80px; border-radius:8px; opacity:0.9; }}
.bdoor {{ position:absolute; left:50%; bottom:0; width:110px; height:130px; margin-left:-55px; background:#0b0c10; border-radius:55px 55px 0 0; }}
.stampbox {{ font:900 110px {FONT}; color:{BAD}; border:12px solid {BAD}; border-radius:26px; background:rgba(255,255,255,0.94);
  display:flex; align-items:center; justify-content:center; letter-spacing:-2px; white-space:nowrap; }}
.sb {{ background:#fff; border:7px solid; border-radius:36px; padding:54px 30px 26px; box-shadow:0 18px 40px rgba(0,0,0,0.45); }}
.sb:after {{ content:""; position:absolute; bottom:-34px; width:0; height:0; border-left:24px solid transparent; border-right:24px solid transparent; border-top:34px solid #fff; }}
.sb.l:after {{ left:90px; }} .sb.r:after {{ right:110px; }} .sb.c:after {{ left:50%; margin-left:-24px; }}
.who {{ position:absolute; left:26px; top:-30px; padding:4px 22px; border-radius:999px; color:#fff; font:900 38px {FONT}; white-space:nowrap; }}
.sbt {{ font-weight:800; color:{INK}; line-height:1.18; }}
.kc {{ opacity:0; }}
.sink {{ border-radius:20px 20px 0 0; background:#94a3b8; border:8px solid #64748b; }}
.plato {{ border-radius:50%; background:#f8fafc; border:5px solid #cbd5e1; }}
.fridge {{ border-radius:24px; background:#e2e8f0; border:8px solid #94a3b8; }}
.fridge:before {{ content:""; position:absolute; left:0; right:0; top:180px; height:8px; background:#94a3b8; }}
.fridge b {{ position:absolute; left:0; right:0; top:60px; text-align:center; font:900 60px {FONT}; color:{BAD}; opacity:0; }}
.tbl {{ }}
.tbl:before {{ content:""; position:absolute; left:0; right:0; top:90px; height:30px; border-radius:10px; background:#a16207; }}
.tbl:after {{ content:""; position:absolute; left:130px; top:120px; width:40px; height:120px; background:#78350f; }}
.cand {{ position:absolute; left:135px; top:30px; width:30px; height:60px; border-radius:6px; background:#fef3c7; }}
.flm {{ position:absolute; left:138px; top:0px; width:24px; height:34px; border-radius:50% 50% 50% 50% / 60% 60% 40% 40%; background:#fb923c; transform-origin:50% 100%; }}
.billt {{ position:absolute; left:0; right:0; top:30px; display:flex; align-items:center; justify-content:center; gap:12px; font:900 48px {FONT}; color:{INK}; }}
.billn {{ position:absolute; left:0; right:0; top:110px; text-align:center; font:900 100px {FONT}; color:{INK}; }}
.stall {{ }}
.awn {{ position:absolute; left:-20px; right:-20px; top:0; height:110px; border-radius:16px; background:repeating-linear-gradient(90deg,#ef4444 0 50px,#fff 50px 100px); }}
.ctr {{ position:absolute; left:0; right:0; bottom:0; height:280px; border-radius:12px; background:#a16207; }}
.frt {{ position:absolute; left:20px; right:20px; bottom:290px; display:flex; justify-content:space-around; }}
.shut {{ position:absolute; left:0; right:0; top:100px; bottom:0; background:repeating-linear-gradient(#6b7280 0 30px,#4b5563 30px 36px); border-radius:8px; }}
.npn {{ position:absolute; left:0; right:0; top:14px; text-align:center; }}
.npl {{ position:absolute; left:0; right:0; bottom:16px; text-align:center; font:900 40px {FONT}; color:#475569; }}
.garita {{ border-radius:20px 20px 0 0; background:#334155; border:8px solid #64748b; }}
.gwin {{ position:absolute; left:40px; right:40px; top:60px; height:160px; border-radius:12px; background:#7dd3fc; opacity:0.7; }}
.garita b {{ position:absolute; left:0; right:0; top:250px; text-align:center; font:900 34px {FONT}; color:#e2e8f0; }}
.zz {{ font:900 70px {FONT}; color:#a5b4fc; text-align:center; }}
.polh svg {{ flex:none; }}
.polh {{ position:absolute; left:40px; right:40px; top:40px; display:flex; align-items:center; gap:18px; font:900 48px {FONT}; color:{INK}; white-space:nowrap; }}
.poll {{ position:absolute; left:40px; right:40px; height:70px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:540px; flex:none; font:900 32px {FONT}; color:{INK}; white-space:nowrap; }}
.poll i {{ flex:1; height:36px; border-radius:18px; }}
.ctt {{ position:absolute; left:40px; top:52px; font:800 52px {FONT}; color:{INK}; white-space:nowrap; }}
.pubb {{ position:absolute; right:30px; top:40px; padding:12px 40px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 56px {FONT}; }}
"""


def build():
    world()
    scene_hook()
    scene_piso()
    scene_cita()
    scene_mercado()
    scene_garita()
    scene_final()
