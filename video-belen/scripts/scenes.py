"""Escenas del vídeo «Lo que diría la psicología de Belén y Emilio». Un solo mundo: un camino en zigzag
(la pareja -> el desprecio -> ¡imbécil! -> el tira y afloja -> la tragaperras -> el paso que nunca llega -> la química -> ficción y vida real)."""
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
PINK, BLUE = "#db2777", "#2f62c0"


def couple(pre, x, fl, sc=1.0, gap=330, z=6):
    """Emilio (portero) a la izquierda y Belén a la derecha, mirándose."""
    add(character(f"{pre}e", "emilio", x, fl, sc, z=z))
    add(character(f"{pre}b", "belen", x + gap, fl, sc, z=z))
    js(f'face("{pre}b", -1, 0);')


def big_heart(hid, x, y, size, z=7):
    add(f'''<div id="{hid}" style="{css_box(x, y, size, size, z)}">
      <div id="{hid}-a" class="hh" style="clip-path:polygon(0 0, 52% 0, 44% 30%, 56% 55%, 46% 100%, 0 100%)">{icon("heart", size, "#fecdd3", 1.6).replace("<svg", f"<svg fill=\"{PINK}\"")}</div>
      <div id="{hid}-b" class="hh" style="clip-path:polygon(52% 0, 100% 0, 100% 100%, 46% 100%, 56% 55%, 44% 30%)">{icon("heart", size, "#fecdd3", 1.6).replace("<svg", f"<svg fill=\"{PINK}\"")}</div></div>''')


def crack(hid, t, dx=40):
    js(f'tl.to("#{hid}-a", {{x:{-dx}, rotation:-12, duration:0.35, ease:"back.out(2)"}}, {t:.3f}); tl.to("#{hid}-b", {{x:{dx}, rotation:12, duration:0.35, ease:"back.out(2)"}}, {t:.3f});')


def mend(hid, t):
    js(f'tl.to("#{hid}-a, #{hid}-b", {{x:0, rotation:0, duration:0.3, ease:"back.out(2)"}}, {t:.3f});')


# ================================================================= MUNDO
MILES = [("Desengaño 21", 0, 1630), ("Rompen", 1, 570), ("Vuelven", 2, 1630), ("Y vuelta a empezar", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="{PINK}"/><stop offset="0.5" stop-color="#7c3aed"/><stop offset="1" stop-color="{BLUE}"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 280, ROAD[r] + 34, 560, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= GANCHO
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    fl = floor(0)
    couple("c0", fx + 230, fl, 1.15, gap=500)
    big_heart("bh0", fx + 330, fy + 120, 300)
    add(f'<div id="fav" class="pill" style="{css_box(fx + 200, fy + 470, None, None, 8)}background:{PINK};color:#fff;font-size:50px;opacity:0">{icon("heart", 46, "#fff", 2.6)} LA PAREJA FAVORITA</div>')
    add(f'<div id="psi" class="pill" style="{css_box(fx + 230, fy + 470, None, None, 9)}background:#fff;color:{INK};font-size:50px;opacity:0">{icon("search", 46, INK, 2.8)} PSICOLOGÍA</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: el corazón late entre los dos
    js('tl.fromTo("#bh0", {scale:1.5, opacity:1}, {scale:1, duration:0.5, ease:"back.out(2.5)"}, 0);')
    js('tl.to("#bh0", {scale:1.08, duration:0.25, yoyo:true, repeat:5, ease:"sine.inOut"}, 0.5);')
    sfx(0.0, "whoosh", 0.35)
    sfx(0.3, "pop", 0.4)
    life("c0e", 0, G.DUR, 1)
    life("c0b", 0, G.DUR, 2)
    t_fav, t_psi, t_ana, t_sal, t_par = P("favorita"), P("psicologia"), P("analizara"), P("saldrian"), P("parados")
    pop("#fav", t_fav - 0.2, sound="pop2")
    js(f'tl.to("#fav", {{opacity:0, duration:0.2}}, {t_psi - 0.2:.3f});')
    pop("#psi", t_psi, sound=None)
    js(f'tl.to("#psi", {{x:20, duration:0.3, yoyo:true, repeat:3, ease:"sine.inOut"}}, {t_ana:.3f});')
    crack("bh0", t_sal)
    sfx(t_sal, "golpe", 0.45)
    shake(t_sal + 0.05, 14)
    js(f'tl.to(Q("c0e","mouth"), {{scaleX:0.7, svgOrigin:"120 136", duration:0.2}}, {t_par:.3f}); tl.to(Q("c0b","brows"), {{y:6, rotation:-5, svgOrigin:"120 88", duration:0.2}}, {t_par:.3f});')


# ================================================================= 1 · EL DESPRECIO
def scene_gottman():
    fx, fy, fw, fh = F(0, 1)
    header("h1", fx, fy, "1", "EL DESPRECIO", color=BAD, txt="#fff")
    card("gm", fx + 40, fy + 190, 600, 230, f'''
      <div style="position:absolute;left:30px;top:30px">{icon("graduation-cap", 110, INK, 2.2)}</div>
      <div style="position:absolute;left:170px;top:36px;font:900 46px {FONT};color:{INK};white-space:nowrap">JOHN GOTTMAN</div>
      <div style="position:absolute;left:170px;top:116px;font:800 44px {FONT};color:#64748b">psicólogo</div>''')
    add(f'<div id="dec" class="pill" style="{css_box(fx + 660, fy + 230, None, None, 8)}background:#334155;color:#fff;font-size:46px;opacity:0">{icon("hourglass", 44, "#fff", 2.6)} DÉCADAS</div>')
    add(f'''<div id="thermo" class="therm" style="{css_box(fx + 120, fy + 470, 720, 110, 6)}opacity:0">
      <div id="thf" class="thf"></div><span>RIESGO DE RUPTURA</span></div>''')
    add(f'<div id="dsp" class="stampbox" style="{css_box(fx + 170, fy + 680, 620, 170, 9)}opacity:0">DESPRECIO</div>')
    t_uno, t_des, t_psi, t_got, t_dec, t_enc, t_pre, t_rup, t_des2 = (P("uno"), P("desprecio"), P("psicologo"), P("gottman"), P("decadas"), P("encontro"),
                                                                    P("predictor"), P("ruptura"), P("desprecio", 2))
    travel(t_uno - 0.25, F(0, 1), 0, 1630, dur=0.6)
    header_in("h1", t_uno, t_des)
    slide_in("#gm", t_psi, dy=-60, sound="pop")
    pop("#dec", t_dec - 0.1, sound=None)
    js(f'tl.fromTo("#thermo", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_enc:.3f});')
    js('tl.set("#thf", {scaleX:0.1, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to("#thf", {{scaleX:1, duration:1.0, ease:"power2.in"}}, {t_pre:.3f});')
    sfx(t_pre, "whoosh-corto", 0.3)
    js(f'tl.to("#thermo", {{x:8, duration:0.05, yoyo:true, repeat:7}}, {t_rup:.3f});')
    stamp("#dsp", t_des2 - 0.1)
    sfx(t_des2, "golpe", 0.45)


# ================================================================= ¡IMBÉCIL!
def scene_imbecil():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    items = [("message-square-x", "INSULTOS"), ("laugh", "BURLAS"), ("eye-off", "OJOS EN BLANCO")]
    for k, (ic, lab) in enumerate(items):
        add(f'<div id="it{k}" class="itm" style="{css_box(fx + 40 + k * 300, fy + 60, 280, 200, 7)}opacity:0">{icon(ic, 90, BAD, 2.4)}<span>{lab}</span></div>')
    couple("c1", fx + 230, fl, 1.1, gap=480)
    add(f'<div id="imb" class="imb" style="{css_box(fx + 330, fy + 330, 600, 220, 9)}opacity:0">¡IMBÉCIL!</div>')
    t_ins, t_bur, t_ojo, t_sue, t_imb = P("insultos"), P("burlas"), P("ojos"), P("suena"), P("imbecil")
    travel(t_ins - 0.35, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_ins)
    for k, t in enumerate([t_ins, t_bur, t_ojo]):
        js(f'tl.fromTo("#it{k}", {{opacity:0, y:-40}}, {{opacity:1, y:0, duration:0.3, ease:"back.out(2)"}}, {t:.3f});')
        sfx(t, "pop2", 0.3)
    life("c1e", 0, G.DUR, 3)
    life("c1b", 0, G.DUR, 4)
    js(f'tl.to(Q("c1b","eyes"), {{y:-8, duration:0.2, yoyo:true, repeat:1}}, {t_ojo + 0.2:.3f});')
    js(f'tilt("c1b", {t_sue:.3f});')
    js(f'tl.to("#it0, #it1, #it2", {{opacity:0.3, duration:0.3}}, {t_imb - 0.3:.3f});')
    js(f'tl.fromTo("#imb", {{opacity:0, scale:0.3, rotation:-10}}, {{opacity:1, scale:1, rotation:-4, duration:0.3, ease:"back.out(3)"}}, {t_imb - 0.05:.3f});')
    js(f'point("c1b", "R", {t_imb - 0.1:.3f}, {t_imb + 0.8:.3f}, -100);')
    js(f'tl.to("#c1e", {{scaleY:0.92, transformOrigin:"50% 100%", duration:0.2}}, {t_imb + 0.05:.3f});')
    sfx(t_imb, "golpe-climax", 0.5)
    shake(t_imb + 0.05, 20)


# ================================================================= 2 · EL TIRA Y AFLOJA
def scene_tira():
    fx, fy, fw, fh = F(1, 0)
    header("h2", fx, fy, "2", "EL TIRA Y AFLOJA", color="#7c3aed", txt="#fff")
    big_heart("bh1", fx + 330, fy + 200, 300)
    add(f'<div id="rupb" class="cnt" style="{css_box(fx + 40, fy + 560, 420, 140, 8)}background:{BAD};opacity:0">{icon("heart-crack", 70, "#fff", 2.6)}<span class="cntl">ROMPEN</span></div>')
    add(f'<div id="vueb" class="cnt" style="{css_box(fx + 500, fy + 560, 420, 140, 8)}background:{GOOD_BG};opacity:0">{icon("heart", 70, "#fff", 2.6)}<span class="cntl">VUELVEN</span></div>')
    add(f'<div id="eng" class="pill" style="{css_box(fx + 280, fy + 750, None, None, 8)}background:{ACC};color:{INK};font-size:54px;opacity:0">{icon("magnet", 50, INK, 2.6)} ENGANCHA</div>')
    add(f'<div id="ref" class="pill" style="{css_box(fx + 120, fy + 870, None, None, 8)}background:#fff;color:{INK};font-size:48px;opacity:0">REFUERZO INTERMITENTE</div>')
    t_dos, t_tir, t_rom, t_vol, t_otr, t_eng, t_ref, t_int = P("dos"), P("tira"), P("rompian"), P("volvian"), P("otra"), P("engancha"), P("refuerzo"), P("intermitente")
    travel(t_dos - 0.3, F(1, 0), 1, 570, dur=0.7)
    header_in("h2", t_dos, t_tir)
    pop("#rupb", t_rom - 0.1, sound=None)
    pop("#vueb", t_vol - 0.1, sound=None)
    beats = [t_rom, t_vol, t_otr - 0.2, t_otr + 0.25]
    for i, t in enumerate(beats):
        if i % 2 == 0:
            crack("bh1", t)
            js(f'tl.to("#rupb", {{scale:1.1, duration:0.12, yoyo:true, repeat:1}}, {t:.3f});')
            sfx(t, "golpe", 0.25)
        else:
            mend("bh1", t)
            js(f'tl.to("#vueb", {{scale:1.1, duration:0.12, yoyo:true, repeat:1}}, {t:.3f});')
            sfx(t, "pop", 0.25)
    mend("bh1", t_eng - 0.1)
    pop("#eng", t_eng, sound="pop2")
    pop("#ref", t_ref, sound=None)
    js(f'tl.to("#ref", {{scale:1.06, duration:0.15, yoyo:true, repeat:1}}, {t_int:.3f});')


# ================================================================= LA TRAGAPERRAS
def scene_tragaperras():
    fx, fy, fw, fh = F(2, 0)
    syms = ["cherry", "heart", "x", "cherry", "heart", "cherry", "x", "heart"]
    cols = {"cherry": "#dc2626", "heart": PINK, "x": "#334155"}
    strips = []
    for k in range(3):
        cells = "".join(f'<div class="sym">{icon(s, 120, cols[s], 2.6)}</div>' for s in syms * 2)
        strips.append(f'<div class="reel" style="left:{60 + k * 230}px"><div id="rl{k}" class="rstrip">{cells}</div></div>')
    add(f'''<div id="slot" class="slot" style="{css_box(fx + 80, fy + 120, 760, 560, 5)}">
      <div class="stop">TRAGAPERRAS</div>{"".join(strips)}</div>''')
    add(f'<div id="lever" class="lever" style="{css_box(fx + 850, fy + 200, 60, 340, 4)}"><i></i></div>')
    add(f'<div id="casi" class="pill" style="{css_box(fx + 260, fy + 720, None, None, 8)}background:{BAD};color:#fff;font-size:54px;opacity:0">¡CASI!</div>')
    add(f'<div id="otra" class="pill" style="{css_box(fx + 190, fy + 850, None, None, 8)}background:#fff;color:{INK};font-size:50px;opacity:0">{icon("rotate-ccw", 48, INK, 2.6)} OTRA VEZ…</div>')
    t_mec, t_tra, t_nun, t_pre, t_dej, t_int = P("mecanismo"), P("tragaperras"), P("nunca"), P("premio"), P("dejar"), P("intentarlo")
    travel(t_mec - 0.3, F(2, 0), 2, 570, dur=0.7)
    hide_mile(1, t_mec)
    js(f'tl.fromTo("#slot", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_tra - 0.2:.3f});')
    h = 150
    def spin(t, stops):
        js(f'tl.to("#lever i", {{rotation:40, transformOrigin:"50% 100%", duration:0.15, yoyo:true, repeat:1}}, {t:.3f});')
        sfx(t, "tic-rodillo", 0.35)
        for k in range(3):
            js(f'tl.fromTo("#rl{k}", {{y:0}}, {{y:{-stops[k] * h}, duration:{0.9 + k * 0.25:.2f}, ease:"power2.out", immediateRender:false}}, {t + 0.1:.3f});')
    spin(t_tra, [8, 8, 2])
    js(f'tl.fromTo("#casi", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(3)"}}, {t_pre:.3f});')
    sfx(t_pre, "golpe", 0.35)
    spin(t_dej - 0.1, [11, 11, 14])
    pop("#otra", t_int, sound="pop2")


# ================================================================= 3 · EL PASO QUE NUNCA LLEGA
def scene_paso():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    header("h3", fx, fy, "3", "EL PASO QUE NUNCA LLEGA", color=BLUE, txt="#fff")
    couple("c2", fx + 250, fl, 1.0, gap=440)
    add(f'<div id="fwd" style="{css_box(fx + 360, fy + 360, 220, 120, 8)}opacity:0">{icon("move-right", 210, GOOD, 3)}</div>')
    add(f'<div id="bck" style="{css_box(fx + 600, fy + 500, 220, 120, 8)}opacity:0">{icon("move-right", 210, BAD, 3).replace("<svg", "<svg style=\"transform:scaleX(-1)\"")}</div>')
    for k, (x, y) in enumerate([(80, 250), (560, 220), (300, 560)]):
        add(f'<div id="ar{k}" class="argb" style="{css_box(fx + x, fy + y, 260, 120, 9)}opacity:0">{icon("zap", 56, ACC, 2.6)}<b>!!</b></div>')
    add(f'<div id="nohab" class="pill" style="{css_box(fx + 220, fy + 200, None, None, 9)}background:#334155;color:#fff;font-size:48px;opacity:0;text-decoration:line-through">HABLARLO</div>')
    t_tres, t_paso, t_que, t_ava, t_otr, t_atr, t_hab, t_dis, t_cos = (P("tres"), P("paso"), P("queria"), P("avanzar"), P("otro"), P("atras"), P("hablarlo"),
                                                                     P("discutian"), P("cosa"))
    travel(t_tres - 0.3, F(2, 1), 2, 1630, dur=0.7)
    header_in("h3", t_tres, t_paso)
    life("c2e", 0, G.DUR, 5)
    life("c2b", 0, G.DUR, 6)
    js(f'tl.fromTo("#fwd", {{opacity:0, x:-60}}, {{opacity:1, x:0, duration:0.4}}, {t_que:.3f});')
    js(f'tl.to("#c2e", {{x:110, duration:0.6}}, {t_ava:.3f}); walk("c2e", {t_ava:.3f}, {t_ava + 0.6:.3f}, 0.13);')
    js(f'tl.fromTo("#bck", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.4}}, {t_otr:.3f});')
    js(f'tl.to("#c2b", {{x:120, duration:0.6}}, {t_atr - 0.2:.3f}); walk("c2b", {t_atr - 0.2:.3f}, {t_atr + 0.4:.3f}, 0.13);')
    sfx(t_atr, "whoosh-corto", 0.3)
    js(f'tl.to("#fwd, #bck", {{opacity:0, duration:0.3}}, {t_hab - 0.2:.3f});')
    pop("#nohab", t_hab, sound=None)
    for k in range(3):
        js(f'tl.fromTo("#ar{k}", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.25, ease:"back.out(3)"}}, {t_dis + k * 0.2:.3f});')
        js(f'tl.to("#ar{k}", {{rotation:{(k - 1) * 8}, duration:0.1, yoyo:true, repeat:5}}, {t_dis + 0.3 + k * 0.2:.3f});')
    sfx(t_dis, "golpe", 0.35)
    js(f'tl.to(Q("c2e","mouth"), {{scaleY:2, svgOrigin:"120 136", duration:0.12, yoyo:true, repeat:5}}, {t_dis:.3f}); tl.to(Q("c2b","mouth"), {{scaleY:2, svgOrigin:"120 136", duration:0.12, yoyo:true, repeat:5}}, {t_dis + 0.1:.3f});')
    shake(t_cos, 8)


# ================================================================= LA QUÍMICA
def scene_quimica():
    fx, fy, fw, fh = F(3, 1)
    fl = floor(3)
    couple("c3", fx + 300, fl, 1.05, gap=360)
    for k, (x, y) in enumerate([(380, 520), (520, 470), (450, 600), (300, 440), (600, 580)]):
        add(f'<div id="sp{k}" data-layout-ignore style="{css_box(fx + x, fy + y, 90, 90, 8)}opacity:0">{icon("sparkles", 90, ACC, 2.4)}</div>')
    add(f'<div id="qr" class="pill" style="{css_box(fx + 250, fy + 120, None, None, 8)}background:{PINK};color:#fff;font-size:56px;opacity:0">{icon("flame", 52, "#fff", 2.6)} QUÍMICA REAL</div>')
    add(f'<div id="ft" class="pill" style="{css_box(fx + 230, fy + 260, None, None, 8)}background:#fff;color:{INK};font-size:46px;opacity:0">FERNANDO TEJERO</div>')
    add(f'<div id="cel" class="stampbox sm" style="{css_box(fx + 170, fy + 330, 620, 130, 9)}opacity:0">CELOS REALES</div>')
    t_y8, t_enc, t_qui, t_rea, t_fer, t_cel, t_ver = P("y", 8), P("encantaban"), P("quimica"), P("real"), P("fernando"), P("celos"), P("verdad")
    travel(t_y8 - 0.3, F(3, 1), 3, 1630, dur=0.7)
    hide_mile(2, t_y8)
    life("c3e", 0, G.DUR, 7)
    life("c3b", 0, G.DUR, 8)
    js(f'tl.to(Q("c3e","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.2}}, {t_enc:.3f}); tl.to(Q("c3b","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.2}}, {t_enc:.3f});')
    for k in range(5):
        js(f'tl.fromTo("#sp{k}", {{opacity:0, scale:0.3, rotation:-40}}, {{opacity:1, scale:1, rotation:0, duration:0.3, ease:"back.out(3)"}}, {t_qui + k * 0.08:.3f});')
        js(f'tl.to("#sp{k}", {{scale:1.2, duration:0.25, yoyo:true, repeat:5}}, {t_qui + 0.4 + k * 0.08:.3f});')
    pop("#qr", t_rea - 0.1, sound="pop")
    pop("#ft", t_fer, sound=None)
    stamp("#cel", t_cel - 0.1)
    sfx(t_cel, "golpe", 0.4)
    js(f'tl.to(Q("c3e","brows"), {{y:6, duration:0.2}}, {t_ver:.3f});')


# ================================================================= FICCIÓN VS VIDA REAL + COMENTARIOS
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    add(f'''<div id="fic" class="half" style="{css_box(fx + 40, fy + 40, 420, 520, 5)}background:#4c0519">
      <div class="hlab">FICCIÓN</div><div class="hic">{icon("popcorn", 170, "#fde68a", 2.2)}</div></div>''')
    add(f'''<div id="vid" class="half" style="{css_box(fx + 500, fy + 40, 420, 520, 5)}background:#0f172a">
      <div class="hlab">VIDA REAL</div><div class="hic"><div id="bat" class="bat"><i id="batf"></i></div></div></div>''')
    hearts("hf-", fx + 250, fy + 300, 4, P("engancha", 2), spread=260, rise=200)
    cta = "Mi Belén era…"
    card("cbox", fx + 40, fy + 600, 880, 440, f'''
      <div style="position:absolute;left:40px;top:28px;display:flex;align-items:center;gap:22px">{icon("message-circle", 76, INK, 2.4)}
        <span style="font:900 60px {FONT};color:{INK}">Comentarios</span></div>
      <div class="poll" style="top:130px"><span style="color:{BLUE}">EMILIO</span><i id="pe" style="background:{BLUE}"></i></div>
      <div class="poll" style="top:200px"><span style="color:{PINK}">BELÉN</span><i id="pb" style="background:{PINK}"></i></div>
      <div id="ctt" style="position:absolute;left:40px;top:285px;font:800 58px {FONT};color:{INK};white-space:nowrap">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 960, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_en3, t_fic, t_dra, t_eng2, t_vid, t_des, t_tu, t_emi2, t_bel2, t_leo, t_com = (
        P("en", 3), P("ficcion"), P("drama"), P("engancha", 2), P("vida"), P("desgasta"), P("tu"), P("emilio", 2), P("belen", 2), P("leo"), P("comentarios"))
    travel(t_en3 - 0.3, F(3, 0), 3, 570, dur=0.6)
    js(f'tl.fromTo("#fic", {{opacity:0, x:-60}}, {{opacity:1, x:0, duration:0.4}}, {t_fic - 0.1:.3f});')
    js(f'tl.to("#fic .hic", {{scale:1.15, duration:0.2, yoyo:true, repeat:3}}, {t_dra:.3f});')
    sfx(t_dra, "pop2", 0.3)
    js(f'tl.fromTo("#vid", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.4}}, {t_vid - 0.2:.3f});')
    js('tl.set("#batf", {scaleX:1, transformOrigin:"0% 50%", backgroundColor:"#22c55e"}, 0);')
    js(f'tl.to("#batf", {{scaleX:0.12, backgroundColor:"{BAD}", duration:1.0, ease:"power2.in"}}, {t_des - 0.3:.3f});')
    sfx(t_des, "golpe", 0.35)
    slide_in("#cbox", t_tu - 0.3, dy=80)
    js('tl.set("#pe, #pb", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to("#pe", {{scaleX:1, duration:0.4, ease:"back.out(1.6)"}}, {t_emi2:.3f}); tl.to("#pb", {{scaleX:1, duration:0.4, ease:"back.out(1.6)"}}, {t_bel2:.3f});')
    sfx(t_emi2, "pop2", 0.25)
    sfx(t_bel2, "pop2", 0.25)
    type_on("#ctt .kc", len(cta), t_bel2 + 0.2, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.2:.3f});')
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.htitle {{ font-size:66px; top:34px; }}
.cnt {{ border-radius:28px; border:5px solid #fff; display:flex; align-items:center; justify-content:center; gap:12px; }}
.cntl {{ font:900 56px {FONT}; color:#fff; }}
.hh {{ position:absolute; inset:0; }}
.hh svg {{ width:100%; height:100%; filter:drop-shadow(0 20px 30px rgba(0,0,0,0.45)); }}
.therm {{ border-radius:55px; background:#1f2937; border:6px solid #fff; overflow:hidden; }}
.thf {{ position:absolute; left:0; top:0; bottom:0; width:100%; background:linear-gradient(90deg,{GOOD},{ACC},{BAD}); }}
.therm span {{ position:absolute; left:0; right:0; top:0; bottom:0; display:flex; align-items:center; justify-content:center; font:900 48px {FONT}; color:#fff; text-shadow:0 2px 8px rgba(0,0,0,0.6); }}
.stampbox {{ border:12px solid {BAD}; border-radius:24px; color:{BAD}; background:rgba(255,255,255,0.94); font:900 110px {FONT}; text-align:center; line-height:146px; transform:rotate(-8deg); white-space:nowrap; }}
.stampbox.sm {{ font-size:80px; line-height:106px; }}
.itm {{ border-radius:28px; background:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px; }}
.itm span {{ font:900 36px {FONT}; color:{INK}; white-space:nowrap; }}
.imb {{ border-radius:40px; background:{BAD}; color:#fff; font:900 120px {FONT}; text-align:center; line-height:220px; white-space:nowrap; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.slot {{ border-radius:40px; background:linear-gradient(#7c3aed,#4c1d95); border:10px solid {ACC}; box-shadow:0 30px 60px rgba(0,0,0,0.5); }}
.stop {{ position:absolute; left:0; right:0; top:20px; text-align:center; font:900 54px {FONT}; color:{ACC}; letter-spacing:3px; }}
.reel {{ position:absolute; top:120px; width:200px; height:380px; border-radius:20px; background:#fff; overflow:hidden; border:6px solid #1f2937; }}
.rstrip {{ position:absolute; left:0; right:0; top:115px; }}
.sym {{ height:150px; display:flex; align-items:center; justify-content:center; }}
.lever i {{ position:absolute; left:20px; top:0; width:20px; height:300px; border-radius:10px; background:#cbd5e1; }}
.lever i::before {{ content:""; position:absolute; left:-20px; top:-40px; width:60px; height:60px; border-radius:50%; background:{BAD}; }}
.argb {{ border-radius:40px; background:#fff; display:flex; align-items:center; justify-content:center; gap:10px; font:900 64px {FONT}; color:{BAD}; }}
.half {{ border-radius:36px; border:6px solid rgba(255,255,255,0.8); overflow:hidden; }}
.hlab {{ position:absolute; left:0; right:0; top:30px; text-align:center; font:900 56px {FONT}; color:#fff; }}
.hic {{ position:absolute; left:0; right:0; top:170px; display:flex; justify-content:center; }}
.bat {{ position:relative; width:260px; height:140px; border-radius:24px; border:10px solid #fff; }}
.bat::after {{ content:""; position:absolute; right:-34px; top:36px; width:20px; height:50px; border-radius:6px; background:#fff; }}
.bat i {{ position:absolute; left:8px; top:8px; bottom:8px; right:8px; border-radius:12px; }}
.poll {{ position:absolute; left:40px; right:40px; height:60px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:230px; font:900 46px {FONT}; }}
.poll i {{ flex:1; height:36px; border-radius:18px; }}
.pubb {{ position:absolute; right:40px; bottom:30px; padding:12px 44px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 62px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_gottman()
    scene_imbecil()
    scene_tira()
    scene_tragaperras()
    scene_paso()
    scene_quimica()
    scene_final()
