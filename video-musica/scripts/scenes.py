"""Escenas del vídeo «¿Por qué ponen música en el súper?». Un solo mundo: un camino en zigzag por los pasillos
(gancho -> ritmo -> vino -> sin darse cuenta -> lo caro -> el reloj -> ¿manipulación? -> comentarios)."""
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
def note_svg(size, color):
    return icon("music", size, color, 2.6)


def bottle(bid, x, y, kind, z=6, h=230, label=""):
    """Botella: cuerpo + cuello + etiqueta con bandera (fr / de) o precio."""
    body = {"fr": "#7f1d1d", "de": "#3f6212", "a": "#7f1d1d", "b": "#581c87", "c": "#1e293b"}[kind]
    flag = ""
    if kind == "fr":
        flag = '<div class="flag"><i style="background:#1d4ed8"></i><i style="background:#fff"></i><i style="background:#dc2626"></i></div>'
    elif kind == "de":
        flag = '<div class="flag hz"><i style="background:#111"></i><i style="background:#dc2626"></i><i style="background:#facc15"></i></div>'
    lab = f'<div class="blab">{label}</div>' if label else ""
    add(f'''<div id="{bid}" class="bottle" style="{css_box(x, y, 80, h, z)}">
      <div class="bneck" style="background:{body}"></div><div class="bbody" style="background:{body}">{flag}{lab}</div></div>''')


def shelf(sid, x, y, w, rows=2, z=2, seed=0):
    cols = ["#ef4444", "#f59e0b", "#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#14b8a6", "#f97316"]
    items = []
    for r in range(rows):
        n = int((w - 40) / 86)
        for c in range(n):
            col = cols[(c * 3 + r * 5 + seed) % len(cols)]
            hh = 70 + ((c * 7 + r * 3 + seed) % 4) * 14
            items.append(f'<div class="prod" style="left:{24 + c * 86}px;top:{r * 170 + 150 - hh}px;height:{hh}px;background:{col}"></div>')
        items.append(f'<div class="board" style="top:{r * 170 + 150}px"></div>')
    add(f'<div id="{sid}" class="shelf" data-layout-ignore style="{css_box(x, y, w, rows * 170 + 20, z)}">{"".join(items)}</div>')


def notes_burst(prefix, x, y, n, t, spread=420, rise=260, z=9, color=ACC):
    for i in range(n):
        nx = x + (i - (n - 1) / 2) * spread / max(1, n - 1)
        add(f'<div id="{prefix}{i}" data-layout-ignore style="{css_box(nx - 40, y, 80, 80, z)}opacity:0">{note_svg(80, color)}</div>')
        tt = t + i * 0.08
        js(f'tl.fromTo("#{prefix}{i}", {{opacity:0, y:0, scale:0.4, rotation:-20}}, {{opacity:1, y:{rise * 0.5:.0f}, scale:1, rotation:10, duration:0.45, ease:"back.out(2)", immediateRender:false}}, {tt:.3f});')
        js(f'tl.to("#{prefix}{i}", {{y:{rise}, x:{(i % 3 - 1) * 50}, opacity:0, duration:1.1, ease:"power1.in"}}, {tt + 0.5:.3f});')


def speaker(sid, x, y, size=200, z=7):
    add(f'<div id="{sid}" class="spk" style="{css_box(x, y, size, size, z)}">{icon("speaker", size * 0.7, "#fff", 2.2)}</div>')


def cart(cid, x, y, size=240, z=7):
    add(f'<div id="{cid}" style="{css_box(x, y, size, size, z)}">{icon("shopping-cart", size, "#e2e8f0", 2.2)}</div>')


# ================================================================= MUNDO
MILES = [("EE. UU. · 1982", 0, 1630), ("Reino Unido", 1, 570), ("Tienda de vinos", 2, 1630), ("Tu súper", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#22c55e"/><stop offset="0.5" stop-color="#facc15"/><stop offset="1" stop-color="#ef4444"/></linearGradient></defs>
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
    fl = floor(0)
    shelf("sh0", fx + 20, fy + 300, 920, rows=2, z=2)
    speaker("spk0", fx + 380, fy + 20, 200)
    add(character("cli0", "g2", fx + 230, fl, 1.05, z=6))
    cart("cart0", fx + 340, fl - 250, 250)
    add(f'<div id="ent" class="pill" style="{css_box(fx + 110, fy + 255, None, None, 9)}background:#fff;color:{INK};font-size:54px;opacity:0">{icon("party-popper", 50, INK, 2.4)} ¿PARA ENTRETENERTE?</div>')
    add(f'<div id="entx" data-layout-ignore style="{css_box(fx + 100, fy + 296, 740, 12, 10)}background:{BAD};border-radius:6px;opacity:0"></div>')
    add(f'''<div id="tick" class="ticket" style="{css_box(fx + 620, fy + 420, 300, 520, 9)}">
      <div class="tkh">TICKET</div>{"".join(f'<div class="tkl" style="top:{90 + i * 52}px;width:{150 + (i * 37) % 90}px"></div>' for i in range(7))}
      <div class="tkt">TOTAL</div><div id="tkst" class="tkstamp">MEDIDO</div></div>''')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: el altavoz suelta un golpe de notas y el carrito frena
    js('tl.fromTo("#spk0", {scale:1.35}, {scale:1, duration:0.4, ease:"back.out(2.5)"}, 0);')
    js('tl.to("#spk0", {scale:1.08, duration:0.2, yoyo:true, repeat:13, ease:"sine.inOut"}, 0.4);')
    notes_burst("nb0-", fx + 480, fy + 160, 5, 0.05, spread=520, rise=300)
    shake(0.1, 12)
    sfx(0.0, "golpe", 0.5)
    life("cli0", 0, G.DUR, 1)
    js(f'tl.fromTo("#cli0, #cart0", {{x:-260}}, {{x:0, duration:0.8, ease:"power3.out"}}, 0); walk("cli0", 0, 0.8, 0.13);')
    js('tl.fromTo("#cart0", {rotation:0}, {rotation:-6, transformOrigin:"0% 100%", duration:0.12, yoyo:true, repeat:1}, 0.8);')
    t_sue, t_mus, t_no, t_ent = P("suena"), P("musica"), P("no"), P("entretenerte")
    js(f'tl.to(Q("cli0","head"), {{rotation:-10, svgOrigin:PIV.head, duration:0.3}}, {t_sue:.3f}); tilt("cli0", {t_mus:.3f});')
    notes_burst("nb1-", fx + 480, fy + 160, 4, t_mus, spread=420, rise=260)
    pop("#ent", t_no, sound="pop2")
    js(f'tl.fromTo("#entx", {{opacity:1, scaleX:0, transformOrigin:"0% 50%"}}, {{opacity:1, scaleX:1, duration:0.25, ease:"power2.out", immediateRender:false}}, {t_ent + 0.3:.3f});')
    sfx(t_ent + 0.3, "golpe", 0.3)
    t_com, t_mas, t_med = P("compres"), P("mas"), P("medido")
    js(f'tl.to("#ent, #entx", {{opacity:0, y:-40, duration:0.3}}, {P("esta", 2):.3f});')
    js(f'tl.fromTo("#tick", {{opacity:0, scaleY:0.2, transformOrigin:"50% 0%"}}, {{opacity:1, scaleY:0.55, duration:0.35, ease:"back.out(2)"}}, {t_com - 0.1:.3f});')
    js(f'tl.to("#tick", {{scaleY:1, duration:0.6, ease:"power2.out"}}, {t_mas:.3f});')
    sfx(t_com - 0.1, "papel", 0.35)
    stamp("#tkst", t_med)
    sfx(t_med, "golpe", 0.4)


# ================================================================= 1 · EL RITMO
def scene_ritmo():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "1", "EL RITMO", color=ACC)
    add(f'''<div id="met" style="{css_box(fx + 720, fy + 0, 200, 260, 7)}">
      <div class="metb"></div><div id="metarm" class="metarm"></div></div>''')
    cal, ch = roller("cal", "0000", 70, "#fff")
    add(f'<div id="calb" class="cnt" style="{css_box(fx + 40, fy + 190, 330, 120, 8)}background:{INK}">{cal}</div>')
    add(f'''<div id="tog" class="tog" style="{css_box(fx + 400, fy + 190, 520, 120, 8)}">
      <div id="tgk" class="tgk"></div><span class="tga">LENTA</span><span class="tgb">RÁPIDA</span></div>''')
    shelf("sh1", fx + 20, fy + 360, 920, rows=1, z=2, seed=3)
    add(character("cli1", "g2", fx + 160, fl, 1.0, z=6))
    cart("cart1", fx + 250, fl - 230, 230)
    for i in range(4):
        add(f'<div id="it{i}" class="prod" style="{css_box(fx + 300 + i * 40, fl - 240 - (i % 2) * 30, 40, 70, 8)}background:{["#ef4444", "#22c55e", "#3b82f6", "#f59e0b"][i]};opacity:0"></div>')
    pc, phh = roller("pct", "00", 110, "#fff")
    add(f'<div id="pctb" class="cnt" style="{css_box(fx + 600, fy + 680, 340, 180, 8)}background:{GOOD_BG};opacity:0"><span class="big">+</span>{pc}<span class="big">%</span></div>')
    add(f'<div id="vent" class="pill" style="{css_box(fx + 620, fy + 580, None, None, 8)}background:#fff;color:{INK};opacity:0">{icon("trending-up", 50, GOOD_BG, 2.6)} VENTAS</div>')
    t_uno, t_rit, t_82, t_est, t_pro, t_len, t_rap = (P("uno"), P("ritmo"), P("1982"), P("estados"), P("probaron"), P("lenta"), P("rapida"))
    travel(t_uno - 0.25, F(0, 1), 0, 1630, dur=0.7)
    header_in("h1", t_uno, t_rit)
    js(f'tl.fromTo("#met", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_rit:.3f});')
    js(f'tl.fromTo("#metarm", {{rotation:-28}}, {{rotation:28, transformOrigin:"50% 100%", duration:0.45, ease:"sine.inOut", yoyo:true, repeat:{int((t_len - t_rit) / 0.45)}, immediateRender:false}}, {t_rit + 0.3:.3f});')
    pop("#calb", t_82 - 0.3, sound=None)
    roll_set("cal", "0000", ch)
    roll_to("cal", "1982", ch, t_82 - 0.1, dur=0.6)
    js(f'tl.fromTo("#sh1", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_est:.3f});')
    pop("#tog", t_pro, sound="pop2")
    js(f'tl.to("#tgk", {{x:0, duration:0.25}}, {t_len:.3f}); tl.to("#tgk", {{x:260, duration:0.25, ease:"back.out(2)"}}, {t_rap:.3f});')
    sfx(t_rap, "click", 0.4)
    js(f'tl.to("#metarm", {{rotation:28, duration:0.15, yoyo:true, repeat:3}}, {t_rap:.3f});')
    t_len2, t_cam, t_des, t_ven, t_sub, t_38 = P("lenta", 2), P("caminaba"), P("despacio"), P("ventas"), P("subieron"), P("38")
    js(f'tl.to("#tgk", {{x:0, duration:0.3, ease:"back.out(2)"}}, {t_len2:.3f});')
    sfx(t_len2, "click", 0.4)
    js(f'tl.fromTo("#metarm", {{rotation:-28}}, {{rotation:28, transformOrigin:"50% 100%", duration:0.9, ease:"sine.inOut", yoyo:true, repeat:{int((G.DUR - t_len2) / 0.9)}, immediateRender:false}}, {t_len2 + 0.3:.3f});')
    life("cli1", 0, G.DUR, 2)
    js(f'tl.fromTo("#cli1, #cart1, [id^=it]", {{x:0}}, {{x:120, duration:{t_ven - t_cam + 0.6:.2f}, ease:"none", immediateRender:false}}, {t_cam:.3f}); walk("cli1", {t_cam:.3f}, {t_ven + 0.6:.3f}, 0.42);')
    for i in range(4):
        js(f'tl.fromTo("#it{i}", {{opacity:0, y:-160}}, {{opacity:1, y:0, duration:0.35, ease:"bounce.out"}}, {t_des + i * 0.35:.3f});')
        sfx(t_des + i * 0.35, "pop2", 0.2)
    pop("#vent", t_ven, sound=None)
    pop("#pctb", t_sub, sound="pop")
    roll_set("pct", "00", phh)
    roll_to("pct", "38", phh, t_38 - 0.1, dur=0.6)
    sfx(t_38, "check", 0.4)
    js(f'tl.to("#pctb", {{scale:1.08, duration:0.15, yoyo:true, repeat:1}}, {E("%"):.3f});')


# ================================================================= 2 · EL VINO
def scene_vino():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    header("h2", fx, fy, "2", "EL VINO", color="#7c3aed", txt="#fff")
    add(f'<div id="wsh" class="wshelf" style="{css_box(fx + 40, fy + 190, 880, 330, 3)}"></div>')
    for i in range(4):
        bottle(f"fr{i}", fx + 80 + i * 100, fy + 230, "fr", z=5)
        bottle(f"de{i}", fx + 520 + i * 100, fy + 230, "de", z=5)
    add(f'<div id="same" class="pill" style="{css_box(fx + 230, fy + 540, None, None, 8)}background:#fff;color:{INK};opacity:0">{icon("tag", 50, INK, 2.6)} MISMO PRECIO</div>')
    add(f'<div id="mus" class="pill pillx" style="{css_box(fx + 40, fy + 660, 620, 100, 8)}background:#1d4ed8;color:#fff;font-size:46px;opacity:0">'
        f'<span id="mus-a">{icon("music", 50, "#fff", 2.6)} ACORDEÓN FRANCÉS</span><span id="mus-b" style="opacity:0">{icon("music", 50, "#fff", 2.6)} MÚSICA ALEMANA</span></div>')
    a1, ah = roller("cfr", "00", 90, "#fff")
    a2, _ = roller("cde", "00", 90, "#fff")
    add(f'<div id="bfr" class="cnt" style="{css_box(fx + 40, fy + 800, 400, 150, 8)}background:#1e3a8a;opacity:0"><span class="flg">FR</span>{a1}</div>')
    add(f'<div id="bde" class="cnt" style="{css_box(fx + 520, fy + 800, 400, 150, 8)}background:#3f3f46;opacity:0"><span class="flg">DE</span>{a2}</div>')
    add(f'<div id="crown" data-layout-ignore style="{css_box(fx + 180, fy + 720, 120, 100, 9)}opacity:0">{icon("crown", 100, "#facc15", 2.6).replace("<svg", "<svg fill=\"#facc15\"")}</div>')
    t_dos, t_vin, t_ing, t_fra, t_ale, t_pre = P("dos"), P("vino"), P("ingles"), P("franceses"), P("alemanes"), P("precio")
    travel(t_dos - 0.25, F(1, 1), 1, 1630, dur=0.75)
    hide_mile(0, t_dos + 0.3)
    header_in("h2", t_dos, t_vin)
    js(f'tl.fromTo("#wsh", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_ing:.3f});')
    js(f'tl.fromTo("[id^=fr]", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.35, stagger:0.06, ease:"back.out(2)"}}, {t_fra:.3f});')
    js(f'tl.fromTo("[id^=de]", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.35, stagger:0.06, ease:"back.out(2)"}}, {t_ale:.3f});')
    sfx(t_fra, "pop2", 0.25)
    sfx(t_ale, "pop2", 0.25)
    pop("#same", t_pre - 0.2, sound="check")
    t_dia, t_aco, t_ven, t_40, t_8 = P("dias"), P("acordeon"), P("vendieron"), P("40"), P("8")
    js(f'tl.to("#same", {{opacity:0, duration:0.3}}, {t_dia:.3f});')
    pop("#mus", t_aco - 0.1, sound="pop")
    notes_burst("nv-", fx + 300, fy + 600, 4, t_aco, spread=300, rise=-220, color="#93c5fd")
    pop("#bfr", t_ven, sound=None)
    pop("#bde", t_ven + 0.1, sound=None)
    for i in range(4):
        js(f'tl.to("#fr{i}", {{y:-40, duration:0.15, yoyo:true, repeat:3}}, {t_ven + i * 0.12:.3f});')
    roll_set("cfr", "00", ah)
    roll_set("cde", "00", ah)
    roll_to("cfr", "40", ah, t_40, dur=0.6)
    sfx(t_40, "check", 0.4)
    roll_to("cde", "08", ah, t_8, dur=0.5)
    js(f'tl.fromTo("#crown", {{opacity:0, y:-60}}, {{opacity:1, y:0, duration:0.35, ease:"bounce.out"}}, {t_8 + 0.3:.3f});')
    t_mu3, t_alm, t_gan, t_alem = P("musica", 3), P("alemana"), P("ganaba"), P("aleman")
    flip("#mus", t_alm - 0.1, ["#mus-a"], ["#mus-b"], bg="#3f3f46")
    notes_burst("nv2-", fx + 700, fy + 600, 4, t_alm, spread=300, rise=-220, color="#fde047")
    for i in range(4):
        js(f'tl.to("#de{i}", {{y:-40, duration:0.15, yoyo:true, repeat:3}}, {t_gan + i * 0.12:.3f});')
    roll_to("cfr", "12", ah, t_gan, dur=0.5)
    roll_to("cde", "22", ah, t_gan + 0.1, dur=0.5)
    js(f'tl.to("#crown", {{x:480, duration:0.45, ease:"power2.inOut"}}, {t_alem:.3f});')
    sfx(t_alem, "check", 0.4)


# ================================================================= SIN DARSE CUENTA
def scene_marioneta():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    cx = fx + 400
    sc = 1.25
    add(character("cli2", "g2", cx, fl, sc, z=6))
    # mano izquierda/derecha en coordenadas de página (puntos 71,304 y 169,304 del esqueleto)
    left, top = cx - 120 * sc, fl - 430 * sc
    hlx, hrx, hy = left + 71 * sc, left + 169 * sc, top + 304 * sc
    hx_head = cx
    bar_y = fy + 120
    add(f'''<div id="ctrl" style="{css_box(cx - 200, bar_y - 60, 400, 120, 9)}">
      <div class="cbar"></div><div class="cnote">{note_svg(110, ACC)}</div></div>''')
    add(f'''<svg id="strings" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 8)}overflow:visible;opacity:0" viewBox="0 0 2200 5300">
      <path d="M {cx - 180} {bar_y} L {hlx} {hy}" stroke="#e2e8f0" stroke-width="4"/>
      <path d="M {cx + 180} {bar_y} L {hrx} {hy}" stroke="#e2e8f0" stroke-width="4"/>
      <path d="M {cx} {bar_y} L {hx_head} {top + 50 * sc}" stroke="#e2e8f0" stroke-width="4"/></svg>''')
    bottle("wx", fx + 690, fl - 230, "fr", z=6)
    add(f'<div id="sdc" class="pill" style="{css_box(fx + 440, fy + 400, None, None, 9)}background:{BAD};color:#fff;font-size:48px;opacity:0">{icon("eye-off", 48, "#fff", 2.6)} SIN DARSE CUENTA</div>')
    t_y6, t_inq, t_cas, t_cue, t_mus, t_ele, t_ell = P("y", 6), P("inquietante"), P("casi"), P("cuenta"), P("musica", 4), P("elegido"), P("ellos")
    travel(t_y6 - 0.3, F(1, 0), 1, 570, dur=0.75)
    life("cli2", 0, G.DUR, 3)
    js(f'tl.fromTo("#cli2", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_y6:.3f});')
    js(f'tl.fromTo("#wx", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_y6 + 0.2:.3f});')
    js(f'tl.fromTo("#ctrl", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.5, ease:"back.out(1.6)"}}, {t_inq:.3f});')
    js(f'tl.fromTo("#strings", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t_inq + 0.3:.3f});')
    sfx(t_inq, "whoosh-corto", 0.35)
    js(f'tl.to(Q("cli2","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.3}}, {t_cas:.3f});')
    js(f'tl.to("#ctrl", {{rotation:-10, duration:0.5, yoyo:true, repeat:3, ease:"sine.inOut"}}, {t_cue:.3f});')
    stamp("#sdc", t_cue)
    sfx(t_cue, "golpe", 0.3)
    js(f'tl.to(Q("cli2","armR"), {{rotation:-70, svgOrigin:PIV.armR, duration:0.4, ease:"back.out(2)"}}, {t_ele:.3f});')
    js(f'tl.to("#wx", {{x:-60, y:-120, rotation:-15, duration:0.4, ease:"power2.out"}}, {t_ele + 0.1:.3f});')
    js(f'tl.to("#ctrl .cnote", {{scale:1.2, duration:0.15, yoyo:true, repeat:3}}, {t_mus:.3f});')
    sfx(t_ele, "pop", 0.3)
    js(f'tl.to(Q("cli2","head"), {{rotation:8, svgOrigin:PIV.head, duration:0.3, yoyo:true, repeat:1}}, {t_ell:.3f});')


# ================================================================= 3 · LO CARO
def scene_caro():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h3", fx, fy, "3", "LO CARO", color=GOOD_BG, txt="#fff")
    add(f'<div id="vio" class="pill" style="{css_box(fx + 40, fy + 190, None, None, 8)}background:#fff;color:{INK};font-size:56px;opacity:0">{icon("music-4", 54, INK, 2.6)} MÚSICA CLÁSICA</div>')
    add(f'<div id="wsh3" class="wshelf" style="{css_box(fx + 40, fy + 330, 560, 720, 3)}"></div>')
    tiers = [("c1", "€", fy + 820, "a"), ("c2", "€€", fy + 580, "b"), ("c3", "€€€", fy + 350, "c")]
    for bid, lab, by, kind in tiers:
        bottle(bid, fx + 150, by, kind, z=5, h=200)
        add(f'<div id="{bid}p" class="ptag" style="{css_box(fx + 270, by + 60, 240, 90, 6)}">{lab}</div>')
    add(f'<div id="hand" data-layout-ignore style="{css_box(fx + 620, fy + 840, 160, 160, 10)}opacity:0">{icon("pointer", 150, "#fff", 2.2).replace("<svg", "<svg fill=\"#f3cdab\"")}</div>')
    add(f'<div id="eqb" class="pill" style="{css_box(fx + 630, fy + 560, None, None, 8)}background:#334155;color:#fff;font-size:48px;opacity:0">= BOTELLAS</div>')
    add(f'<div id="more" class="pill" style="{css_box(fx + 630, fy + 560, None, None, 9)}background:{GOOD_BG};color:#fff;font-size:52px;opacity:0">MÁS CARO</div>')
    t_tres, t_car, t_cla, t_com, t_vin2, t_com2, t_car2 = (P("tres"), P("caro"), P("clasica"), P("compraba"), P("vino", 2), P("compraba", 2), P("caro", 2))
    travel(t_tres - 0.25, F(2, 0), 2, 570, dur=0.75)
    hide_mile(1, t_tres + 0.3)
    header_in("h3", t_tres, t_car)
    js(f'tl.fromTo("#wsh3, [id^=c1], [id^=c2], [id^=c3]", {{opacity:0}}, {{opacity:1, duration:0.4, stagger:0.05}}, {t_car:.3f});')
    pop("#vio", t_cla - 0.2, sound="pop2")
    notes_burst("nc-", fx + 760, fy + 300, 3, t_cla, spread=200, rise=-160, color="#fff")
    js(f'tl.fromTo("#hand", {{opacity:0, x:80}}, {{opacity:1, x:0, duration:0.35}}, {t_com - 0.1:.3f});')
    js(f'tl.to("#hand", {{x:-30, duration:0.15, yoyo:true, repeat:1}}, {t_vin2:.3f});')
    pop("#eqb", t_vin2 - 0.1, sound="pop2")
    js(f'tl.to("#hand", {{y:-470, duration:0.8, ease:"power2.inOut"}}, {t_com2:.3f});')
    sfx(t_com2, "whoosh-corto", 0.3)
    js(f'tl.to("#c3p", {{scale:1.15, backgroundColor:"{ACC}", duration:0.2, yoyo:true, repeat:1}}, {t_car2:.3f});')
    js(f'tl.to("#c3", {{y:-30, duration:0.2, yoyo:true, repeat:1}}, {t_car2:.3f});')
    js(f'tl.to("#eqb", {{opacity:0, duration:0.2}}, {t_car2 - 0.1:.3f});')
    pop("#more", t_car2, sound="check")


# ================================================================= EL RELOJ
def scene_reloj():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    add(f'''<div id="clock" class="clock" style="{css_box(fx + 270, fy + 40, 420, 420, 6)}">
      {"".join(f'<i class="tick" style="transform:rotate({k * 30}deg)"></i>' for k in range(12))}
      <div id="hh" class="hand hh"></div><div id="mh" class="hand mh"></div><div class="hub"></div></div>''')
    add(f'<div id="unk" class="bubble2" style="{css_box(fx + 600, fy + 520, 300, 160, 8)}opacity:0">{note_svg(80, INK)}<span>?</span></div>')
    shelf("sh5", fx + 20, fy + 540, 560, rows=1, z=2, seed=5)
    add(character("cli3", "g2", fx + 300, fl, 1.0, z=6))
    add(f'<div id="mtime" class="pill" style="{css_box(fx + 560, fy + 760, None, None, 8)}background:{BAD};color:#fff;font-size:54px;opacity:0">{icon("hourglass", 52, "#fff", 2.6)} + TIEMPO</div>')
    t_jue, t_rel, t_can, t_con, t_que, t_rat, t_cue = P("juega"), P("reloj"), P("canciones"), P("conoces"), P("quedas"), P("rato"), P("cuenta", 2)
    travel(t_jue - 0.3, F(2, 1), 2, 1630, dur=0.7)
    js(f'tl.fromTo("#clock", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_rel - 0.1:.3f});')
    sfx(t_rel, "tic-rodillo", 0.3)
    js(f'tl.fromTo("#mh", {{rotation:0}}, {{rotation:60, transformOrigin:"50% 100%", duration:1.0, ease:"steps(6)", immediateRender:false}}, {t_rel:.3f});')
    life("cli3", 0, G.DUR, 4)
    js(f'tl.fromTo("#cli3", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_can - 0.2:.3f}); js_dummy = 0;' if False else
       f'tl.fromTo("#cli3", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_can - 0.2:.3f});')
    pop("#unk", t_con - 0.1, sound="pop2")
    js(f'tl.to("#mh", {{rotation:780, transformOrigin:"50% 100%", duration:1.6, ease:"power2.inOut"}}, {t_que:.3f});')
    js(f'tl.to("#hh", {{rotation:65, transformOrigin:"50% 100%", duration:1.6, ease:"power2.inOut"}}, {t_que:.3f});')
    sfx(t_que, "whoosh", 0.3)
    pop("#mtime", t_rat, sound="pop")
    js(f'tl.to(Q("cli3","head"), {{rotation:-8, svgOrigin:PIV.head, duration:0.3, yoyo:true, repeat:1}}, {t_cue:.3f}); tilt("cli3", {t_cue:.3f});')


# ================================================================= ¿MANIPULACIÓN?
def scene_manip():
    fx, fy, fw, fh = F(3, 1)
    fl = floor(3)
    add(f'''<div id="bal" style="{css_box(fx + 80, fy + 60, 560, 520, 6)}">
      <div class="bpost"></div><div class="bbase"></div>
      <div id="beam" class="beam2">
        <div id="panl" class="pan" style="left:-30px"><span>COMPRAR</span></div>
        <div id="panr" class="pan" style="right:-30px"><span>NO</span></div></div></div>''')
    add(f'<div id="qm" class="qmark" style="{css_box(fx + 640, fy + 40, 240, 240, 9)}opacity:0">?</div>')
    add(f'<div id="dropn" data-layout-ignore style="{css_box(fx + 110, fy - 200, 110, 110, 9)}opacity:0">{note_svg(110, ACC)}</div>')
    add(character("cli4", "g2", fx + 760, fl, 1.0, z=6))
    left, top = fx + 760 - 120, fl - 430
    add(f'<div id="phones" style="{css_box(left + 30, top + 10, 180, 180, 8)}opacity:0">{icon("headphones", 180, "#111827", 3.2)}</div>')
    add(f'<div id="ear" style="{css_box(fx + 640, fy + 340, 140, 140, 8)}opacity:0">{icon("ear", 130, "#fff", 2.4)}</div>')
    card("lista", fx + 60, fy + 640, 420, 380, f'''
      <div style="position:absolute;left:30px;top:24px;font:900 56px {FONT};color:{INK}">LISTA</div>
      {"".join(f'<div class="li" style="top:{110 + i * 64}px"><span id="lc{i}" class="lck">{icon("check", 40, "#fff", 3.4)}</span><span class="lt" style="width:{170 + (i * 53) % 120}px"></span></div>' for i in range(4))}''')
    t_es, t_man, t_nad, t_obl, t_emp, t_poq, t_not = P("es"), P("manipulacion"), P("nadie", 2), P("obliga"), P("empujan"), P("poquito"), P("notes")
    travel(t_es - 0.3, F(3, 1), 3, 1630, dur=0.75)
    hide_mile(2, t_es + 0.3)
    js(f'tl.fromTo("#bal", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4}}, {t_es:.3f});')
    stamp("#qm", t_man)
    sfx(t_man, "golpe", 0.35)
    life("cli4", 0, G.DUR, 5)
    js(f'tl.fromTo("#cli4", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_es:.3f});')
    js(f'tl.to("#beam", {{rotation:0, duration:0.3}}, {t_obl:.3f});')
    js(f'tl.to("#qm", {{opacity:0, duration:0.3}}, {t_obl:.3f});')
    js(f'tl.fromTo("#dropn", {{opacity:0, y:0}}, {{opacity:1, y:300, duration:0.45, ease:"power2.in"}}, {t_emp - 0.2:.3f});')
    js(f'tl.to("#beam", {{rotation:-9, duration:0.5, ease:"back.out(2)"}}, {t_emp + 0.25:.3f});')
    js(f'tl.to("#dropn", {{y:340, duration:0.5, ease:"back.out(2)"}}, {t_emp + 0.25:.3f});')
    sfx(t_emp + 0.25, "madera", 0.4)
    js(f'tl.to("#beam", {{rotation:-6, duration:0.3, yoyo:true, repeat:1}}, {t_poq:.3f});')
    js(f'tl.to(Q("cli4","eyes"), {{scaleY:0.2, svgOrigin:PIV.eyes, duration:0.1, yoyo:true, repeat:1}}, {t_not:.3f});')
    t_pro, t_esc, t_def, t_lis, t_cas = P("proxima"), P("escucha"), P("defenderte"), P("lista"), P("cascos")
    js(f'tl.to("#bal, #dropn", {{opacity:0.25, duration:0.4}}, {t_pro:.3f});')
    pop("#ear", t_esc - 0.1, sound="pop2")
    js(f'tl.to("#ear", {{scale:1.12, duration:0.2, yoyo:true, repeat:3}}, {t_esc + 0.3:.3f});')
    slide_in("#lista", t_def, dy=80, sound="papel", vol=0.35)
    for i in range(4):
        js(f'tl.fromTo("#lc{i}", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.2, ease:"back.out(3)"}}, {t_lis + i * 0.12:.3f});')
    sfx(t_lis, "check", 0.35)
    js(f'tl.fromTo("#phones", {{opacity:0, y:-160}}, {{opacity:1, y:0, duration:0.35, ease:"bounce.out"}}, {t_cas:.3f});')
    js(f'jump("cli4", {t_cas + 0.3:.3f}, 40);')
    sfx(t_cas, "pop", 0.35)


def scene_final():
    fx, fy, fw, fh = F(3, 0)
    cta = "En el mío suena…"
    card("cbox", fx + 60, fy + 200, 840, 520, f'''
      <div style="position:absolute;left:40px;top:40px;display:flex;align-items:center;gap:22px">{icon("message-circle", 90, INK, 2.4)}
        <span style="font:900 72px {FONT};color:{INK}">Comentarios</span></div>
      <div style="position:absolute;left:40px;top:170px;font:900 54px {FONT};color:#555">¿Qué suena en tu súper?</div>
      <div id="ctt" style="position:absolute;left:40px;top:270px;font:800 72px {FONT};color:{INK}">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 760, fy + 640, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_que, t_can, t_te, t_com = P("que", 6), P("cancion"), P("leo"), P("comentarios")
    travel(t_que - 0.2, F(3, 0), 3, 570, dur=0.7)
    slide_in("#cbox", t_que, dy=80)
    notes_burst("nf-", fx + 480, fy + 160, 4, t_can, spread=500, rise=-180)
    type_on("#ctt .kc", len(cta), t_can + 0.3, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_te:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.2:.3f});')
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.7, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; }}
.htitle {{ font-size:76px; top:28px; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; gap:10px; }}
.big {{ font:900 100px {FONT}; color:#fff; }}
.flg {{ font:900 56px {FONT}; color:#fff; margin-right:20px; padding:0 14px; border-radius:12px; background:rgba(255,255,255,0.18); }}
.shelf {{ }}
.board {{ position:absolute; left:0; right:0; height:20px; border-radius:6px; background:#64748b; }}
.prod {{ position:absolute; width:62px; border-radius:10px 10px 6px 6px; box-shadow:inset 0 -12px 0 rgba(0,0,0,0.18); }}
.spk {{ border-radius:40px; background:#1f2937; border:6px solid #475569; display:flex; align-items:center; justify-content:center; }}
.ticket {{ background:#f8fafc; border-radius:12px 12px 0 0; box-shadow:0 20px 50px rgba(0,0,0,0.5); opacity:0;
  -webkit-mask:linear-gradient(#000 0 0) top/100% calc(100% - 20px) no-repeat, radial-gradient(circle 14px at 50% 100%, transparent 98%, #000) bottom/36px 20px repeat-x; }}
.tkh {{ position:absolute; left:0; right:0; top:22px; text-align:center; font:900 50px {FONT}; color:{INK}; letter-spacing:4px; }}
.tkl {{ position:absolute; left:30px; height:14px; border-radius:7px; background:#cbd5e1; }}
.tkt {{ position:absolute; left:30px; bottom:40px; font:900 50px {FONT}; color:{INK}; }}
.tkstamp {{ position:absolute; left:34px; top:190px; padding:4px 12px; border:7px solid {BAD}; border-radius:14px; color:{BAD}; font:900 44px {FONT}; transform:rotate(-14deg); opacity:0; background:rgba(255,255,255,0.85); }}
.metb {{ position:absolute; left:0; right:0; bottom:0; height:240px; background:#a16207; clip-path:polygon(32% 0,68% 0,100% 100%,0 100%); border-radius:10px; }}
.metarm {{ position:absolute; left:94px; bottom:30px; width:12px; height:220px; background:#f8fafc; border-radius:6px; }}
.metarm::before {{ content:""; position:absolute; left:-14px; top:40px; width:40px; height:30px; border-radius:6px; background:{ACC}; }}
.tog {{ border-radius:999px; background:#1f2937; border:5px solid #fff; display:flex; align-items:center; justify-content:space-around; opacity:0; }}
.tog span {{ position:relative; z-index:2; font:900 52px {FONT}; color:#fff; width:250px; text-align:center; }}
.tgk {{ position:absolute; left:6px; top:6px; width:244px; height:98px; border-radius:999px; background:#2563eb; }}
.wshelf {{ border-radius:24px; background:linear-gradient(#3f2a1d,#2b1c13); border:6px solid #5b3a24; }}
.bottle {{ }}
.bneck {{ position:absolute; left:26px; top:0; width:28px; height:70px; border-radius:8px 8px 0 0; }}
.bbody {{ position:absolute; left:0; right:0; top:60px; bottom:0; border-radius:26px 26px 12px 12px; box-shadow:inset -10px 0 0 rgba(255,255,255,0.12); }}
.flag {{ position:absolute; left:10px; right:10px; top:50px; height:44px; display:flex; border-radius:6px; overflow:hidden; border:3px solid #fff; }}
.flag i {{ flex:1; }}
.flag.hz {{ flex-direction:column; }}
.ptag {{ border-radius:20px; background:#fff; color:{INK}; font:900 70px {FONT}; display:flex; align-items:center; justify-content:center; }}
.pillx {{ position:relative; }}
.pillx span {{ position:absolute; left:0; right:0; top:0; bottom:0; display:flex; align-items:center; justify-content:center; gap:14px; }}
.cbar {{ position:absolute; left:0; right:0; top:50px; height:22px; border-radius:11px; background:#a16207; }}
.cnote {{ position:absolute; left:145px; top:-10px; width:110px; height:110px; }}
.clock {{ border-radius:50%; background:#f8fafc; border:14px solid #334155; box-shadow:0 24px 60px rgba(0,0,0,0.5); }}
.tick {{ position:absolute; left:calc(50% - 5px); top:8px; width:10px; height:30px; background:#94a3b8; border-radius:5px; transform-origin:5px 188px; }}
.hand {{ position:absolute; left:calc(50% - 7px); bottom:50%; width:14px; border-radius:7px; background:{INK}; }}
.hh {{ height:110px; }} .mh {{ height:160px; background:{BAD}; }}
.hub {{ position:absolute; left:calc(50% - 18px); top:calc(50% - 18px); width:36px; height:36px; border-radius:50%; background:{INK}; }}
.bubble2 {{ border-radius:40px; background:#fff; display:flex; align-items:center; justify-content:center; gap:10px; font:900 110px {FONT}; color:{INK}; }}
.bpost {{ position:absolute; left:270px; top:60px; width:20px; height:420px; background:#94a3b8; border-radius:10px; }}
.bbase {{ position:absolute; left:170px; bottom:0; width:220px; height:40px; background:#94a3b8; border-radius:20px; }}
.beam2 {{ position:absolute; left:20px; top:60px; width:520px; height:20px; background:#cbd5e1; border-radius:10px; transform-origin:50% 50%; }}
.pan {{ position:absolute; top:20px; width:200px; height:150px; }}
.pan::before {{ content:""; position:absolute; left:98px; top:0; width:4px; height:80px; background:#cbd5e1; }}
.pan span {{ position:absolute; left:0; right:0; top:80px; height:70px; border-radius:0 0 100px 100px; background:#e2e8f0; color:{INK}; font:900 32px {FONT}; text-align:center; line-height:60px; }}
.qmark {{ border-radius:50%; background:{ACC}; color:{INK}; font:900 190px {FONT}; text-align:center; line-height:240px; }}
.li {{ position:absolute; left:30px; display:flex; align-items:center; gap:20px; }}
.lck {{ width:50px; height:50px; border-radius:12px; background:{GOOD_BG}; display:flex; align-items:center; justify-content:center; }}
.lt {{ height:16px; border-radius:8px; background:#cbd5e1; display:block; }}
.pubb {{ position:absolute; right:40px; bottom:40px; padding:16px 50px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 70px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_ritmo()
    scene_vino()
    scene_marioneta()
    scene_caro()
    scene_reloj()
    scene_manip()
    scene_final()
