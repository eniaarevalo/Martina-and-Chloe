"""Escenas del vídeo «¿Existe Mirador de Montepinar?». Un solo mundo: un camino en zigzag
(no existe -> el plató -> el truco -> el adiós -> el derribo -> la mudanza -> la fachada nueva -> el mapa y comentarios)."""
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
def building(bid, x, y, w, h, z=4, sign="MIRADOR DE MONTEPINAR", style="modern", floors=4, cols=4, piece_ids=False):
    """Fachada de bloque de pisos. style: modern (blanco y terracota) o classic (ladrillo, Contubernio)."""
    body = "#f1ede4" if style == "modern" else "#b45f3c"
    trim = "#c2410c" if style == "modern" else "#f5e6c8"
    fh = (h - 200) / floors
    parts = []
    for f in range(floors):
        for c in range(cols):
            wx = 30 + c * (w - 60) / cols
            ww = (w - 60) / cols - 24
            pid = f' id="{bid}-p{f}-{c}"' if piece_ids else ""
            parts.append(f'<div{pid} class="bw" style="left:{wx + 12:.0f}px;top:{80 + f * fh:.0f}px;width:{ww:.0f}px;height:{fh - 40:.0f}px;border-color:{trim}">'
                         f'<i class="bal" style="background:{trim}"></i></div>')
    parts.append(f'<div class="bsign" style="background:{trim};color:{body}">{sign}</div>')
    parts.append(f'<div class="bdoor" style="left:{w / 2 - 60:.0f}px;border-color:{trim}"></div>')
    add(f'<div id="{bid}" class="bld" style="{css_box(x, y, w, h, z)}background:{body}">{"".join(parts)}</div>')


def nave(nid, x, y, w, h, label="PLATÓ", z=3):
    add(f'''<div id="{nid}" class="nave" style="{css_box(x, y, w, h, z)}">
      <div class="nroof"></div><div class="nlab">{label}</div></div>''')


def spot(sid, x, y, z=5, rot=0):
    add(f'<div id="{sid}" class="spot" data-layout-ignore style="{css_box(x, y, 160, 260, z)}transform:rotate({rot}deg);opacity:0"></div>')


# ================================================================= MUNDO
MILES = [("Moraleja de Enmedio", 0, 1630), ("2007 · 2020", 1, 570), ("Temporada 13", 2, 1630), ("Contubernio 49", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#ea580c"/><stop offset="0.5" stop-color="#facc15"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 260, ROAD[r] + 34, 520, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= GANCHO: NUNCA HA EXISTIDO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    building("mt0", fx + 140, fy + 120, 680, 900, z=4)
    add(f'<div id="lqsa" class="pill" style="{css_box(fx + 250, fy + 20, None, None, 8)}background:#fff;color:{INK};font-size:52px;opacity:0">{icon("tv", 50, INK, 2.6)} LA QUE SE AVECINA</div>')
    add(f'<div id="noex" class="bigstamp" style="{css_box(fx + 120, fy + 420, 720, 200, 10)}opacity:0">NO EXISTE</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: el edificio cae a plomo
    js('tl.fromTo("#mt0", {y:-150, scaleY:1.15, transformOrigin:"50% 100%"}, {y:0, scaleY:1, duration:0.5, ease:"bounce.out"}, 0);')
    sfx(0.0, "whoosh", 0.4)
    sfx(0.4, "golpe", 0.5)
    shake(0.45, 14)
    js('tl.fromTo(".bw", {opacity:0.3}, {opacity:1, duration:0.2, stagger:{each:0.03, from:"random"}}, 0.4);')
    t_edi, t_ave, t_nun, t_exi = P("edificio"), P("avecina"), P("nunca"), P("existido")
    pop("#lqsa", t_edi, sound="pop2")
    js(f'tl.to("#lqsa", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_ave:.3f});')
    js(f'tl.to("#mt0", {{filter:"grayscale(1) brightness(0.6)", duration:0.4}}, {t_nun:.3f});')
    stamp("#noex", t_exi - 0.1)
    sfx(t_exi, "golpe-climax", 0.45)
    shake(t_exi + 0.05, 18)


# ================================================================= 1 · EL DECORADO (EL PLATÓ)
def scene_plato():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "EL DECORADO", color="#ea580c", txt="#fff")
    card("mapc", fx + 40, fy + 180, 880, 300, f'''
      <div class="mland"></div>
      <div id="mmad" class="mcity" style="left:470px;top:60px">MADRID</div>
      <div id="mpin" style="position:absolute;left:250px;top:110px;width:110px;height:110px;opacity:0">{icon("map-pin", 110, "#dc2626", 2.6).replace("<svg", "<svg fill=\"#fecaca\"")}</div>
      <div id="mlab" class="mlab" style="left:40px;top:225px;opacity:0">MORALEJA DE ENMEDIO</div>
      <div id="msur" class="pill" style="position:absolute;right:30px;bottom:24px;background:{INK};color:#fff;font-size:42px;opacity:0">{icon("arrow-down", 40, "#fff", 2.6)} SUR</div>''', bg="#dbeafe")
    nave("nv1", fx + 40, fy + 540, 880, 500)
    building("dz", fx + 110, fy + 640, 330, 390, z=5, sign="DESENGAÑO 21", style="classic", floors=3, cols=3)
    building("mt1", fx + 520, fy + 640, 330, 390, z=5, sign="MONTEPINAR", floors=3, cols=3)
    t_uno, t_dec, t_gra, t_mor, t_pue, t_sur, t_mis, t_aqu, t_viv = (P("uno"), P("decorado"), P("grababa"), P("moraleja"), P("pueblo"), P("sur"),
                                                                    P("mismo"), P("aqui"), P("viva"))
    travel(t_uno - 0.25, F(0, 1), 0, 1630, dur=0.6)
    header_in("h1", t_uno, t_dec)
    slide_in("#mapc", t_gra - 0.2, dy=-60, sound="pop")
    js(f'tl.fromTo("#mpin", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.4, ease:"bounce.out"}}, {t_mor:.3f});')
    sfx(t_mor, "pop", 0.35)
    js(f'tl.fromTo("#mlab", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.3}}, {t_mor + 0.2:.3f});')
    pop("#msur", t_sur - 0.1, sound=None)
    js(f'tl.fromTo("#nv1", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_mis - 0.3:.3f});')
    js(f'tl.fromTo("#mt1", {{opacity:0, scale:0.6, transformOrigin:"50% 100%"}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_mis:.3f});')
    js(f'tl.fromTo("#dz", {{opacity:0, scale:0.6, transformOrigin:"50% 100%"}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_aqu:.3f});')
    sfx(t_aqu, "pop2", 0.35)
    js(f'tl.to("#dz, #mt1", {{y:-14, duration:0.15, yoyo:true, repeat:1, stagger:0.1}}, {t_viv:.3f});')


# ================================================================= EL TRUCO: DECORADOS SEPARADOS
def scene_truco():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    blocks = [("PORTAL", 720), ("RELLANO", 380), ("PISO", 40)]
    for k, (lab, by) in enumerate(blocks):
        add(f'''<div id="blk{k}" class="blk" style="{css_box(fx + 260, fy + by, 440, 250, 4)}">
          <div class="blab">{lab}</div><div class="bdr2"></div></div>''')
    for k, (x, y, r) in enumerate([(80, 60, -25), (740, 60, 25), (80, 560, -25)]):
        spot(f"sp{k}", fx + x, fy + y, rot=r)
    add(character("v1", "g1", fx + 820, fl, 0.85, z=7))
    add(f'<div id="chg" class="pill" style="{css_box(fx + 40, fy + 930, None, None, 9)}background:{ACC};color:{INK};font-size:52px;opacity:0">{icon("door-open", 50, INK, 2.6)} ¡CAMBIO DE PLATÓ!</div>')
    t_y, t_tru, t_por, t_rel, t_pis, t_sep, t_cru, t_pue, t_cam = (P("y"), P("truco"), P("portal"), P("rellanos"), P("pisos"), P("separados"),
                                                                   P("cruzar"), P("puerta"), P("cambiabas"))
    travel(t_y - 0.3, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_y + 0.2)
    # el edificio entero (bloques juntos) que se despieza
    js(f'tl.set("#blk0", {{y:-90}}, 0); tl.set("#blk2", {{y:90}}, 0);')
    js(f'tl.fromTo("[id^=blk]", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_y:.3f});')
    for k, t in enumerate([t_por, t_rel, t_pis]):
        js(f'tl.to("#blk{k}", {{backgroundColor:"#fde68a", duration:0.15, yoyo:true, repeat:1}}, {t:.3f});')
        sfx(t, "pop2", 0.25)
    js(f'tl.to("#blk0", {{y:0, duration:0.6, ease:"back.out(1.6)"}}, {t_sep - 0.2:.3f}); tl.to("#blk2", {{y:0, duration:0.6, ease:"back.out(1.6)"}}, {t_sep - 0.2:.3f});')
    sfx(t_sep - 0.2, "whoosh", 0.35)
    js(f'tl.fromTo("[id^=sp]", {{opacity:0}}, {{opacity:0.8, duration:0.3, stagger:0.1}}, {t_sep:.3f});')
    life("v1", 0, G.DUR, 3)
    js(f'tl.fromTo("#v1", {{opacity:0, x:0}}, {{opacity:1, x:-200, duration:{t_pue + 0.1 - t_cru + 0.3:.2f}}}, {t_cru - 0.3:.3f}); walk("v1", {t_cru - 0.3:.3f}, {t_pue + 0.1:.3f}, 0.12);')
    js(f'tl.to("#v1", {{opacity:0, scale:0.8, duration:0.2}}, {t_pue + 0.1:.3f}); tl.set("#v1", {{y:{-767}, x:-200}}, {t_pue + 0.32:.3f}); tl.to("#v1", {{opacity:1, scale:1, duration:0.25}}, {t_cam:.3f});')
    sfx(t_pue + 0.1, "puerta", 0.35)
    pop("#chg", t_cam, sound="pop")


# ================================================================= 2 · EL ADIÓS
def scene_adios():
    fx, fy, fw, fh = F(1, 0)
    header("h2", fx, fy, "2", "EL ADIÓS", color="#64748b", txt="#fff")
    card("tio", fx + 40, fy + 190, 400, 230, f'''
      <div style="position:absolute;left:30px;top:24px;font:900 44px {FONT};color:#64748b">EL TÍO</div>
      <div style="position:absolute;left:30px;top:84px;font:900 52px {FONT};color:{INK};line-height:1.1">José Luis<br>Moreno</div>''')
    card("sob", fx + 520, fy + 190, 400, 230, f'''
      <div style="position:absolute;left:30px;top:24px;font:900 44px {FONT};color:#64748b">SOBRINOS</div>
      <div style="position:absolute;left:30px;top:84px;font:900 44px {FONT};color:{INK};line-height:1.1">Laura y Alberto<br>Caballero</div>''')
    add(f'<div id="fam" style="{css_box(fx + 440, fy + 260, 80, 80, 7)}opacity:0">{icon("arrow-right", 80, ACC, 3)}</div>')
    add(f'<div id="key" style="{css_box(fx + 170, fy + 450, 140, 140, 7)}opacity:0">{icon("key-round", 130, ACC, 2.6)}</div>')
    add(f'''<div id="ctr" class="ctr" style="{css_box(fx + 360, fy + 560, 240, 300, 8)}opacity:0">
      <div class="ctrh">ALQUILER</div>{"".join(f'<i class="ctl" style="top:{90 + k * 40}px"></i>' for k in range(4))}
      <div id="ctrA" class="ctrcut" style="clip-path:inset(0 50% 0 0)"></div><div id="ctrB" class="ctrcut" style="clip-path:inset(0 0 0 50%)"></div></div>''')
    add(f'<div id="sinac" class="bigstamp sm" style="{css_box(fx + 180, fy + 880, 600, 130, 10)}opacity:0">SIN ACUERDO</div>')
    t_dos, t_adi, t_pla, t_mor, t_tio, t_cre, t_lau, t_tra, t_neg, t_alq, t_hub, t_acu = (
        P("dos"), P("adios"), P("plato", 3), P("moreno"), P("tio"), P("creadores"), P("laura"), P("tras"), P("negociaciones"), P("alquiler"),
        P("hubo"), P("acuerdo"))
    travel(t_dos - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h2", t_dos, t_adi)
    js(f'tl.fromTo("#key", {{opacity:0, rotation:-60}}, {{opacity:1, rotation:0, duration:0.4, ease:"back.out(2)"}}, {t_pla:.3f});')
    slide_in("#tio", t_mor - 0.3, dy=-60, sound="pop")
    js(f'tl.to("#tio", {{scale:1.05, duration:0.15, yoyo:true, repeat:1}}, {t_tio:.3f});')
    js(f'tl.fromTo("#fam", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.3}}, {t_cre - 0.1:.3f});')
    slide_in("#sob", t_cre, dy=-60, sound="pop")
    js(f'tl.fromTo("#ctr", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_tra:.3f});')
    js(f'tl.to("#ctr", {{x:-200, rotation:-8, duration:0.35, yoyo:true, repeat:3, ease:"sine.inOut"}}, {t_neg:.3f});')
    js(f'tl.to("#ctr", {{x:200, rotation:8, duration:0.35, yoyo:true, repeat:1, ease:"sine.inOut"}}, {t_neg + 1.4:.3f});')
    sfx(t_neg, "papel", 0.35)
    js(f'tl.set("#ctr", {{x:0, rotation:0}}, {t_hub - 0.05:.3f});')
    js(f'tl.to("#ctr .ctrh, #ctr .ctl", {{opacity:0, duration:0.05}}, {t_acu - 0.05:.3f});')
    js(f'tl.fromTo("#ctrA", {{opacity:1}}, {{x:-90, rotation:-20, duration:0.4, ease:"power2.out"}}, {t_acu:.3f}); tl.fromTo("#ctrB", {{opacity:1}}, {{x:90, rotation:20, duration:0.4, ease:"power2.out"}}, {t_acu:.3f});')
    js(f'tl.set("#ctr", {{backgroundColor:"rgba(0,0,0,0)", boxShadow:"none"}}, {t_acu:.3f});')
    sfx(t_acu, "papel", 0.5)
    stamp("#sinac", t_acu + 0.1)
    sfx(t_acu + 0.1, "golpe", 0.4)


# ================================================================= EL DERRIBO
def scene_derribo():
    fx, fy, fw, fh = F(2, 0)
    building("mt2", fx + 160, fy + 220, 640, 820, z=4, piece_ids=True)
    yr, yh = roller("y20", "2007", 80, "#fff")
    add(f'<div id="y20b" class="cnt" style="{css_box(fx + 40, fy + 40, 360, 140, 8)}background:{INK};opacity:0">{yr}</div>')
    add(f'<div id="a13" class="pill" style="{css_box(fx + 450, fy + 70, None, None, 8)}background:{ACC};color:{INK};font-size:56px;opacity:0">13 AÑOS</div>')
    add(f'<div id="dust" class="dust2" data-layout-ignore style="{css_box(fx + 60, fy + 760, 840, 300, 9)}opacity:0"></div>')
    add(f'<div id="fin" class="bigstamp sm" style="{css_box(fx + 180, fy + 460, 600, 130, 10)}opacity:0">DESTRUIDO</div>')
    t_y4, t_20, t_des, t_tre, t_dec, t_mon, t_dst = P("y", 4), P("2020"), P("despues"), P("trece"), P("decorado", 2), P("montepinar", 2), P("destruyo")
    travel(t_y4 - 0.3, F(2, 0), 2, 570, dur=0.7)
    hide_mile(1, t_y4 + 0.2)
    pop("#y20b", t_y4, sound=None)
    roll_set("y20", "2007", yh)
    roll_to("y20", "2020", yh, t_20 - 0.1, dur=0.6, from_text="2007")
    pop("#a13", t_tre, sound="pop2")
    js(f'tl.to("#mt2", {{x:6, duration:0.06, yoyo:true, repeat:7}}, {t_mon:.3f});')
    k = 0
    for f in range(4):
        for c in range(4):
            js(f'tl.to("#mt2-p{f}-{c}", {{y:{700 - f * 140 + (c * 37) % 60}, x:{(c - 1.5) * 60}, rotation:{(c * 47 + f * 23) % 90 - 45}, opacity:0.6, duration:0.7, ease:"power2.in"}}, {t_dst - 0.1 + ((f * 4 + c) * 0.03):.3f});')
            k += 1
    js(f'tl.to("#mt2", {{scaleY:0.25, transformOrigin:"50% 100%", duration:0.7, ease:"power3.in"}}, {t_dst + 0.1:.3f});')
    js(f'tl.fromTo("#dust", {{opacity:0, scale:0.6}}, {{opacity:0.9, scale:1.2, duration:0.8}}, {t_dst + 0.5:.3f}); tl.to("#dust", {{opacity:0.3, duration:0.8}}, {t_dst + 1.3:.3f});')
    shake(t_dst + 0.6, 26)
    sfx(t_dst + 0.6, "golpe-climax", 0.55)
    stamp("#fin", t_dst + 0.4)


# ================================================================= 3 · LA MUDANZA
def scene_mudanza():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h3", fx, fy, "3", "LA MUDANZA", color="#8b5cf6", txt="#fff")
    add(f'<div id="truck" style="{css_box(fx - 60, fl - 260, 300, 260, 7)}opacity:0">{icon("truck", 290, "#e2e8f0", 2.2).replace("<svg", "<svg fill=\"#7c3aed\"")}</div>')
    add(f'<div id="c49" class="streetsign" style="{css_box(fx + 380, fy + 180, 540, 130, 8)}opacity:0;font-size:48px">CONTUBERNIO, 49</div>')
    n1, h1 = roller("m1500", "0.000", 70, "#fff")
    n2, h2 = roller("m800", "000", 70, "#fff")
    nave("nva", fx + 40, fy + 360, 520, 380, label="PLATÓ 1")
    nave("nvb", fx + 600, fy + 440, 320, 300, label="PLATÓ 2")
    add(f'<div id="ma" class="cnt" style="{css_box(fx + 110, fy + 560, 380, 120, 8)}background:{INK};opacity:0">{n1}<span class="m2">m²</span></div>')
    add(f'<div id="mb" class="cnt" style="{css_box(fx + 620, fy + 600, 280, 120, 8)}background:{INK};opacity:0">{n2}<span class="m2">m²</span></div>')
    t_tres, t_mud, t_vec, t_con, t_49, t_nue, t_dos2, t_15, t_800, t_cua = (P("tres"), P("mudanza"), P("vecinos"), P("contubernio"), P("49"),
                                                                          P("nuevo"), P("dos", 2), P("1500"), P("800"), P("cuadrados"))
    travel(t_tres - 0.3, F(2, 1), 2, 1630, dur=0.7)
    header_in("h3", t_tres, t_mud)
    js(f'tl.fromTo("#truck", {{x:-200, opacity:1}}, {{x:{fw - 200}, opacity:1, duration:{t_con - t_vec + 0.6:.2f}, ease:"power1.inOut", immediateRender:false}}, {t_vec - 0.3:.3f});')
    js(f'tl.to("#truck", {{y:-8, duration:0.12, yoyo:true, repeat:{int((t_con - t_vec + 0.6) / 0.12)}}}, {t_vec - 0.3:.3f});')
    sfx(t_vec - 0.3, "whoosh", 0.4)
    js(f'tl.to("#truck", {{opacity:0, duration:0.3}}, {t_nue:.3f});')
    js(f'tl.fromTo("#c49", {{opacity:0, rotation:-20, y:-80}}, {{opacity:1, rotation:-4, y:0, duration:0.45, ease:"back.out(2)"}}, {t_con:.3f});')
    sfx(t_con, "madera", 0.4)
    js(f'tl.to("#c49", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {t_49:.3f});')
    js(f'tl.fromTo("#nva, #nvb", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4, stagger:0.15}}, {t_dos2 - 0.1:.3f});')
    pop("#ma", t_15 - 0.3, sound=None)
    roll_set("m1500", "0.000", h1)
    roll_to("m1500", "1.500", h1, t_15 - 0.2, dur=0.6, from_text="0.000")
    pop("#mb", t_800 - 0.2, sound=None)
    roll_set("m800", "000", h2)
    roll_to("m800", "800", h2, t_800 - 0.1, dur=0.5)
    sfx(t_cua, "check", 0.35)


# ================================================================= LA FACHADA AL AIRE LIBRE
def scene_fachada():
    fx, fy, fw, fh = F(3, 1)
    fl = floor(3)
    add(f'<div id="sky3" class="sky3" data-layout-ignore style="{css_box(fx, fy + 20, fw, 1040, 1)}opacity:0"></div>')
    add(f'<div id="sun3" class="sun3" style="{css_box(fx + 740, fy + 40, 170, 170, 2)}opacity:0"></div>')
    building("ct", fx + 220, fy + 240, 520, 760, z=4, sign="CONTUBERNIO 49", style="classic")
    add(f'<div id="walk" class="walk" style="{css_box(fx + 0, fl - 40, fw, 40, 5)}opacity:0"></div>')
    for k, x in enumerate([60, 820]):
        add(f'<div id="lamp{k}" style="{css_box(fx + x, fl - 380, 90, 380, 6)}opacity:0"><i class="lpost"></i><i class="lhead"></i></div>')
    add(f'<div id="aire" class="pill" style="{css_box(fx + 40, fy + 60, None, None, 8)}background:#fff;color:{INK};font-size:52px;opacity:0">{icon("sun", 50, "#ca8a04", 2.6)} AL AIRE LIBRE</div>')
    t_y6, t_ahor, t_fac, t_air, t_cal, t_dec, t_luz, t_nat = (P("y", 6), P("ahora"), P("fachada"), P("aire"), P("calle"), P("decorado", 3), P("luz"),
                                                            P("natural"))
    travel(t_y6 - 0.3, F(3, 1), 3, 1630, dur=0.7)
    hide_mile(2, t_y6 + 0.2)
    js(f'tl.fromTo("#ct", {{opacity:0, y:120}}, {{opacity:1, y:0, duration:0.5, ease:"back.out(1.4)"}}, {t_fac - 0.2:.3f});')
    sfx(t_fac, "pop", 0.35)
    js(f'tl.fromTo("#sky3", {{opacity:0}}, {{opacity:1, duration:0.6}}, {t_air - 0.2:.3f});')
    pop("#aire", t_air, sound="pop2")
    js(f'tl.fromTo("#walk", {{opacity:0, scaleX:0}}, {{opacity:1, scaleX:1, duration:0.4}}, {t_cal - 0.1:.3f});')
    js(f'tl.fromTo("[id^=lamp]", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, stagger:0.15, ease:"back.out(2)"}}, {t_cal:.3f});')
    sfx(t_cal, "madera", 0.3)
    js(f'tl.fromTo("#sun3", {{opacity:0, y:120, scale:0.5}}, {{opacity:1, y:0, scale:1, duration:0.6, ease:"power2.out"}}, {t_luz - 0.1:.3f});')
    js(f'tl.to("#sun3", {{scale:1.12, duration:0.25, yoyo:true, repeat:1}}, {t_nat:.3f});')
    sfx(t_luz, "check", 0.3)


# ================================================================= EL MAPA + COMENTARIOS
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    card("map2", fx + 40, fy + 500, 880, 520, f'''
      <div class="grid2"></div>
      <div id="srch" class="srch">{icon("search", 50, "#64748b", 2.6)}<span>Mirador de Montepinar</span></div>
      <div id="none" class="none">SIN RESULTADOS</div>''', bg="#e0f2fe")
    add(f'<div id="mag" style="{css_box(fx + 200, fy + 700, 200, 200, 9)}opacity:0">{icon("search", 190, INK, 2.8)}</div>')
    cta = "Me quedo con…"
    card("cbox", fx + 40, fy + 20, 880, 460, f'''
      <div style="position:absolute;left:40px;top:30px;display:flex;align-items:center;gap:22px">{icon("message-circle", 80, INK, 2.4)}
        <span style="font:900 64px {FONT};color:{INK}">Comentarios</span></div>
      <div class="poll" style="top:140px"><span>MONTEPINAR</span><i id="pa" style="background:#ea580c"></i></div>
      <div class="poll" style="top:220px"><span>CONTUBERNIO</span><i id="pb" style="background:#8b5cf6"></i></div>
      <div id="ctt" style="position:absolute;left:40px;top:310px;font:800 62px {FONT};color:{INK};white-space:nowrap">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 390, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_asi, t_bus, t_mon, t_map, t_no, t_enc = P("asi"), P("buscas"), P("montepinar", 3), P("mapa"), P("no", 3), P("encontrar")
    travel(t_asi - 0.3, F(3, 0), 3, 570, dur=0.7)
    slide_in("#map2", t_asi, dy=60, sound="pop")
    js(f'tl.fromTo("#srch", {{opacity:0, y:-20}}, {{opacity:1, y:0, duration:0.3}}, {t_bus:.3f});')
    js(f'tl.fromTo("#mag", {{opacity:0}}, {{opacity:1, duration:0.2}}, {t_mon - 0.1:.3f});')
    js(f'tl.to("#mag", {{x:420, y:-60, duration:0.5, yoyo:true, repeat:2, ease:"sine.inOut"}}, {t_mon:.3f});')
    sfx(t_map, "whoosh-corto", 0.3)
    js(f'tl.to("#mag", {{opacity:0, duration:0.2}}, {t_no - 0.1:.3f});')
    stamp("#none", t_no)
    sfx(t_enc, "golpe", 0.4)
    t_que, t_mon4, t_con2, t_leo, t_com = P("quedas"), P("montepinar", 4), P("contubernio", 2), P("leo"), P("comentarios")
    slide_in("#cbox", t_que - 0.3, dy=-80)
    js('tl.set("#pa, #pb", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to("#pa", {{scaleX:1, duration:0.5, ease:"back.out(1.6)"}}, {t_mon4:.3f});')
    js(f'tl.to("#pb", {{scaleX:1, duration:0.5, ease:"back.out(1.6)"}}, {t_con2:.3f});')
    sfx(t_mon4, "pop2", 0.3)
    sfx(t_con2, "pop2", 0.3)
    type_on("#ctt .kc", len(cta), t_con2 + 0.4, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.2:.3f});')
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.5, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.htitle {{ font-size:76px; top:28px; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; gap:12px; }}
.bld {{ border-radius:14px 14px 4px 4px; box-shadow:0 24px 60px rgba(0,0,0,0.5); }}
.bw {{ position:absolute; background:#7dd3fc; border:8px solid; border-radius:6px; box-shadow:inset 0 0 0 6px rgba(255,255,255,0.35); }}
.bal {{ position:absolute; left:-12px; right:-12px; bottom:-22px; height:16px; border-radius:4px; }}
.bsign {{ position:absolute; left:20px; right:20px; top:14px; height:52px; border-radius:10px; font:900 40px {FONT}; text-align:center; line-height:52px; white-space:nowrap; overflow:hidden; }}
.bdoor {{ position:absolute; bottom:0; width:120px; height:120px; background:#3f2a1d; border:8px solid; border-bottom:none; border-radius:10px 10px 0 0; }}
.bigstamp {{ border:14px solid {BAD}; border-radius:24px; color:{BAD}; background:rgba(255,255,255,0.92); font:900 110px {FONT}; text-align:center; line-height:170px; transform:rotate(-10deg); white-space:nowrap; }}
.bigstamp.sm {{ font-size:84px; line-height:104px; border-width:10px; }}
.mland {{ position:absolute; inset:0; background:radial-gradient(ellipse at 60% 30%, #fde68a 0 22%, #bbf7d0 23% 60%, #dbeafe 61%); border-radius:30px; }}
.mcity {{ position:absolute; padding:6px 20px; border-radius:14px; background:{INK}; color:#fff; font:900 50px {FONT}; }}
.mlab {{ position:absolute; font:900 46px {FONT}; color:#b91c1c; white-space:nowrap; }}
.nave {{ border-radius:20px; background:#334155; border:6px solid #64748b; }}
.nroof {{ position:absolute; left:-20px; right:-20px; top:-70px; height:80px; background:#475569; clip-path:polygon(0 100%, 12% 0, 88% 0, 100% 100%); }}
.nlab {{ position:absolute; left:24px; top:16px; padding:4px 18px; border-radius:12px; background:{ACC}; color:{INK}; font:900 44px {FONT}; }}
.blk {{ border-radius:20px; background:#f1ede4; border:8px solid #c2410c; box-shadow:0 20px 40px rgba(0,0,0,0.45); }}
.blab {{ position:absolute; left:24px; top:20px; font:900 60px {FONT}; color:{INK}; }}
.bdr2 {{ position:absolute; right:30px; bottom:0; width:100px; height:150px; border-radius:10px 10px 0 0; background:#5b3a24; }}
.spot {{ background:linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0)); clip-path:polygon(40% 0, 60% 0, 100% 100%, 0 100%); filter:blur(4px); }}
.ctr {{ border-radius:14px; background:#fff; box-shadow:0 20px 40px rgba(0,0,0,0.45); }}
.ctrh {{ position:absolute; left:0; right:0; top:22px; text-align:center; font:900 40px {FONT}; color:{INK}; }}
.ctl {{ position:absolute; left:30px; right:30px; height:14px; border-radius:7px; background:#cbd5e1; }}
.ctrcut {{ position:absolute; inset:0; border-radius:14px; background:#fff; opacity:0; }}
.dust2 {{ border-radius:50%; background:radial-gradient(ellipse, rgba(214,211,209,0.9), rgba(214,211,209,0) 70%); }}
.streetsign {{ border-radius:16px; background:#1e3a8a; border:8px solid #fff; color:#fff; font:900 54px {FONT}; text-align:center; line-height:114px; white-space:nowrap; }}
.m2 {{ font:900 50px {FONT}; color:#fff; }}
.sky3 {{ border-radius:36px; background:linear-gradient(#7dd3fc, #e0f2fe 70%, #0f172a 71%); opacity:0.85; }}
.sun3 {{ border-radius:50%; background:#facc15; box-shadow:0 0 80px 30px rgba(250,204,21,0.6); }}
.walk {{ background:#94a3b8; border-radius:8px; }}
.lpost {{ position:absolute; left:38px; top:40px; width:14px; height:340px; background:#1e293b; }}
.lhead {{ position:absolute; left:10px; top:0; width:70px; height:56px; border-radius:20px 20px 8px 8px; background:#1e293b; box-shadow:0 30px 40px rgba(250,204,21,0.6); }}
.grid2 {{ position:absolute; inset:0; border-radius:30px; background-image:linear-gradient(rgba(14,116,144,0.15) 3px, transparent 3px), linear-gradient(90deg, rgba(14,116,144,0.15) 3px, transparent 3px); background-size:80px 80px; }}
.srch {{ position:absolute; left:40px; right:40px; top:30px; height:90px; border-radius:45px; background:#fff; display:flex; align-items:center; gap:16px; padding-left:24px; font:800 48px {FONT}; color:{INK}; box-shadow:0 8px 20px rgba(0,0,0,0.15); opacity:0; }}
.none {{ position:absolute; left:120px; top:250px; padding:10px 30px; border:10px solid {BAD}; border-radius:20px; color:{BAD}; background:rgba(255,255,255,0.95); font:900 72px {FONT}; transform:rotate(-8deg); opacity:0; }}
.poll {{ position:absolute; left:40px; right:40px; height:64px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:340px; font:900 46px {FONT}; color:{INK}; }}
.poll i {{ flex:1; height:40px; border-radius:20px; }}
.pubb {{ position:absolute; right:40px; bottom:30px; padding:12px 44px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 62px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_plato()
    scene_truco()
    scene_adios()
    scene_derribo()
    scene_mudanza()
    scene_fachada()
    scene_final()
