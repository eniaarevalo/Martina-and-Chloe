"""Escenas del vídeo «Las Supernenas de Aquí no hay quien viva». Un solo mundo: un camino en zigzag
(homenaje -> quiénes eran -> El verdugo -> el papel de Vicenta -> la mirilla -> las frases -> el impacto -> La que se avecina y las tres estrellas)."""
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
# Personajes: Marisa (rizos), Concha (melena rubia), Vicenta (moño gris)
TRIO = [("marisa", "vecina1", "MARISA", "Mariví Bilbao", "#16a34a"),
        ("concha", "vecina2", "CONCHA", "Emma Penella", "#ea580c"),
        ("vicenta", "vicenta", "VICENTA", "Gemma Cuervo", "#7c3aed")]


def portrait(pid, kind, x, y, size, color, z=6):
    """Retrato ovalado con el personaje de medio cuerpo."""
    sc = size / 260
    add(f'''<div id="{pid}" class="frame" style="{css_box(x, y, size, size * 1.25, z)}border-color:{color}">
      {character(pid + "-c", kind, size / 2, size * 1.25 + 140 * sc, sc * 1.25, z=1)}</div>''')


def plate(pid, x, y, w, top, sub, color, z=7):
    add(f'''<div id="{pid}" class="plate" style="{css_box(x, y, w, 120, z)}border-color:{color}">
      <div class="pt" style="color:{color}">{top}</div><div class="ps">{sub}</div></div>''')


# ================================================================= MUNDO
MILES = [("Desengaño 21", 0, 1630), ("El casting", 1, 570), ("El portal", 2, 1630), ("Siempre", 3, 1630)]


def world():
    for r in range(4):
        for c in (0, 1):
            add(f'<div class="room" data-layout-ignore style="{css_box(COLX[c] + 10, ROWS[r] + 120, CW - 20, CH - 150, 0)}"></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in PTS)
    add(f'''<svg id="roadsvg" data-layout-ignore style="{css_box(0, 0, 2200, 5300, 1)}overflow:visible" viewBox="0 0 2200 5300">
      <defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="5200">
        <stop offset="0" stop-color="#16a34a"/><stop offset="0.5" stop-color="#ea580c"/><stop offset="1" stop-color="#7c3aed"/></linearGradient></defs>
      <path d="{d}" stroke="#262a35" stroke-width="54" fill="none" stroke-linejoin="round"/>
      <path d="{d}" stroke="rgba(255,255,255,0.18)" stroke-width="5" fill="none" stroke-dasharray="26 22" stroke-linejoin="round"/>
      <path id="road" d="{d}" stroke="url(#rb)" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>''')
    js(f'tl.set("#road", {{strokeDasharray:{TOTAL:.1f}, strokeDashoffset:{TOTAL:.1f}}}, 0);')
    for lab, r, x in MILES:
        add(f'<div id="mile{r}" class="mile" data-layout-ignore style="{css_box(x - 260, ROAD[r] + 34, 520, 70, 2)}">{lab}</div>')


def hide_mile(r, t):
    js(f'tl.to("#mile{r}", {{opacity:0, duration:0.3}}, {t:.3f});')


# ================================================================= GANCHO: EL HOMENAJE
def scene_hook():
    fx, fy, fw, fh = F(0, 0)
    for k, (pid, kind, name, actress, col) in enumerate(TRIO):
        portrait(f"pt{k}", kind, fx + 30 + k * 310, fy + 260, 280, col, z=6)
        add(f'<div id="pn{k}" class="pname" style="{css_box(fx + 30 + k * 310, fy + 630, 280, 70, 7)}color:{col}">{name}</div>')
    add(f'<div id="rib" style="{css_box(fx + 820, fy + 230, 120, 120, 9)}opacity:0">{icon("ribbon", 110, "#e5e7eb", 2.4).replace("<svg", "<svg fill=\"#111827\"")}</div>')
    add(f'<div id="sup" class="supt" style="{css_box(fx + 60, fy + 760, 840, 150, 9)}opacity:0">LAS SUPERNENAS</div>')
    add(f'<div id="anh" class="pill" style="{css_box(fx + 180, fy + 940, None, None, 9)}background:#fff;color:{INK};font-size:46px;opacity:0">{icon("tv", 44, INK, 2.6)} AQUÍ NO HAY QUIEN VIVA</div>')
    cam(0, F(0, 0), whoosh=False)
    # primer segundo: los tres retratos caen en su sitio
    js('tl.fromTo(".frame", {y:-80, opacity:1, rotation:-4}, {y:0, rotation:0, duration:0.5, stagger:0.1, ease:"bounce.out"}, 0);')
    js('tl.fromTo(".pname", {opacity:1, scale:1.3}, {scale:1, duration:0.4, stagger:0.1, ease:"back.out(2)"}, 0.1);')
    sfx(0.0, "whoosh", 0.35)
    sfx(0.45, "madera", 0.4)
    for k in range(3):
        life(f"pt{k}-c", 0, G.DUR, 1 + k)
    t_mur, t_vic, t_ult, t_sup, t_aqu = P("murio"), P("vicenta"), P("ultima"), P("supernenas"), P("aqui")
    js(f'tl.to("#pt0, #pt1", {{filter:"grayscale(0.7) brightness(0.8)", duration:0.6}}, {t_mur:.3f});')
    js(f'tl.to("#pt2", {{boxShadow:"0 0 60px 10px rgba(167,139,250,0.7)", duration:0.5}}, {t_vic:.3f});')
    js(f'tl.fromTo("#rib", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_vic + 0.2:.3f});')
    sfx(t_vic + 0.2, "pop2", 0.3)
    js(f'tl.to("#pt2", {{filter:"grayscale(0.7) brightness(0.8)", duration:0.8}}, {t_ult:.3f});')
    js(f'tl.fromTo("#sup", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(2)"}}, {t_sup - 0.1:.3f});')
    sfx(t_sup, "golpe", 0.35)
    pop("#anh", t_aqu, sound=None)


# ================================================================= 1 · QUIÉNES ERAN
def scene_quienes():
    fx, fy, fw, fh = F(0, 1)
    fl = floor(0)
    header("h1", fx, fy, "1", "QUIÉNES ERAN", color="#16a34a", txt="#fff")
    for k, (pid, kind, name, actress, col) in enumerate(TRIO):
        add(character(f"w{k}", kind, fx + 170 + k * 310, fl - 330, 0.95, z=5))
        plate(f"pl{k}", fx + 20 + k * 310, fy + 760, 300, name, actress, col)
    add(f'<div id="cin" class="pill" style="{css_box(fx + 120, fy + 200, None, None, 8)}background:#fff;color:{INK};font-size:52px;opacity:0">{icon("film", 50, INK, 2.6)} CINE</div>')
    add(f'<div id="tea" class="pill" style="{css_box(fx + 520, fy + 200, None, None, 8)}background:#fff;color:{INK};font-size:52px;opacity:0">{icon("drama", 50, INK, 2.6)} TEATRO</div>')
    t_uno, t_qui, t_mar, t_con, t_vic2, t_act, t_vet, t_cin, t_tea = (P("uno"), P("quienes"), P("marisa"), P("concha"), P("vicenta", 2), P("actrices"),
                                                                    P("veteranas"), P("cine"), P("teatro"))
    travel(t_uno - 0.25, F(0, 1), 0, 1630, dur=0.6)
    header_in("h1", t_uno, t_qui)
    for k, t in enumerate([t_mar, t_con, t_vic2]):
        life(f"w{k}", 0, G.DUR, 4 + k)
        js(f'tl.fromTo("#w{k}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t - 0.1:.3f});')
        js(f'tl.fromTo("#pl{k}", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.3}}, {t:.3f});')
        sfx(t, "pop2", 0.3)
    js(f'tl.to("[id^=pl]", {{scale:1.05, duration:0.15, yoyo:true, repeat:1, stagger:0.08}}, {t_vet:.3f});')
    pop("#cin", t_cin - 0.1, sound="pop")
    pop("#tea", t_tea - 0.1, sound="pop")


# ================================================================= EL VERDUGO
def scene_verdugo():
    fx, fy, fw, fh = F(1, 1)
    fl = floor(1)
    portrait("cv", "vecina2", fx + 60, fy + 120, 360, "#ea580c", z=6)
    add(f'<div id="cvp" class="pill" style="{css_box(fx + 50, fy + 640, None, None, 7)}background:#fff;color:#ea580c;font-size:44px;opacity:0">CONCHA · <span style="color:#475569">Emma Penella</span></div>')
    add(f'''<div id="post" class="poster" style="{css_box(fx + 500, fy + 120, 420, 600, 6)}opacity:0">
      <div class="pst1">EL VERDUGO</div><div class="pst2">BERLANGA</div>
      <div class="pst3">{icon("clapperboard", 170, "#fde68a", 2.2)}</div></div>''')
    add(f'<div id="estr" class="pill" style="{css_box(fx + 260, fy + 800, None, None, 8)}background:{ACC};color:{INK};font-size:54px;opacity:0">{icon("star", 52, INK, 2.6)} ESTRELLA DEL CINE</div>')
    t_emm, t_pen, t_est, t_cin2, t_pro, t_ver, t_ber = P("emma"), P("penella"), P("estrella"), P("cine", 2), P("protagonizo"), P("verdugo"), P("berlanga")
    travel(t_emm - 0.3, F(1, 1), 1, 1630, dur=0.7)
    hide_mile(0, t_emm + 0.2)
    js(f'tl.fromTo("#cv", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_emm:.3f});')
    js(f'tl.fromTo("#cvp", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.3}}, {t_pen:.3f});')
    life("cv-c", 0, G.DUR, 7)
    pop("#estr", t_est, sound="check")
    js(f'tl.fromTo("#post", {{opacity:0, rotation:8, y:-60}}, {{opacity:1, rotation:-3, y:0, duration:0.5, ease:"back.out(2)"}}, {t_pro:.3f});')
    sfx(t_pro, "papel", 0.35)
    js(f'tl.to("#post", {{scale:1.05, duration:0.15, yoyo:true, repeat:1}}, {t_ver:.3f});')
    js(f'tl.to("#post .pst2", {{color:"{ACC}", duration:0.2}}, {t_ber:.3f});')


# ================================================================= EL PAPEL DE VICENTA
def scene_casting():
    fx, fy, fw, fh = F(1, 0)
    fl = floor(1)
    add(f'''<div id="scr" class="script" style="{css_box(fx + 80, fy + 150, 380, 480, 6)}opacity:0">
      <div class="sh">GUION</div><div class="sl">VICENTA</div>{"".join(f'<i class="sline" style="top:{180 + k * 50}px;width:{240 - (k % 3) * 40}px"></i>' for k in range(5))}</div>''')
    add(f'<div id="quo" class="quote" style="{css_box(fx + 500, fy + 180, 420, 200, 8)}opacity:0">«No quiero estar aquí»</div>')
    add(f'<div id="asq" class="pill" style="{css_box(fx + 500, fy + 430, None, None, 7)}background:#fff;color:#475569;font-size:44px;opacity:0">MARÍA ASQUERINO</div>')
    add(f'<div id="asqx" class="xline" data-layout-ignore style="{css_box(fx + 505, fy + 462, 440, 12, 9)}opacity:0"></div>')
    add(character("vin", "vicenta", fx + 280, fl, 1.0, z=6))
    add(f'<div id="gem" class="pill" style="{css_box(fx + 380, fy + 560, None, None, 7)}background:#fff;color:#7c3aed;font-size:44px;opacity:0">VICENTA · <span style="color:#475569">Gemma Cuervo</span></div>')
    t_y3, t_vic3, t_cas, t_otr, t_pap, t_mar, t_asq, t_rec, t_lee, t_gui = (P("y", 3), P("vicenta", 3), P("casi"), P("otra"), P("papel"), P("maria"),
                                                                          P("asquerino"), P("rechazo"), P("leer"), P("guion"))
    travel(t_y3 - 0.3, F(1, 0), 1, 570, dur=0.7)
    js(f'tl.fromTo("#scr", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_vic3:.3f});')
    js(f'tl.to("#scr", {{rotation:-6, duration:0.15, yoyo:true, repeat:1}}, {t_otr:.3f});')
    js(f'tl.fromTo("#asq", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.35}}, {t_mar - 0.1:.3f});')
    sfx(t_mar, "pop2", 0.3)
    js(f'tl.fromTo("#quo", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t_rec:.3f});')
    js(f'tl.fromTo("#asqx", {{opacity:1, scaleX:0, transformOrigin:"0% 50%"}}, {{opacity:1, scaleX:1, duration:0.3, immediateRender:false}}, {t_rec + 0.2:.3f});')
    sfx(t_rec, "golpe", 0.35)
    js(f'tl.to("#scr", {{scaleY:0.08, transformOrigin:"50% 0%", duration:0.35, ease:"power2.in"}}, {t_lee:.3f});')
    sfx(t_lee, "papel", 0.35)
    life("vin", 0, G.DUR, 8)
    js(f'tl.fromTo("#vin", {{opacity:0, x:-120}}, {{opacity:1, x:0, duration:0.5}}, {t_gui - 0.2:.3f}); walk("vin", {t_gui - 0.2:.3f}, {t_gui + 0.3:.3f}, 0.13);')
    js(f'tl.fromTo("#gem", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_gui:.3f});')
    sfx(t_gui, "check", 0.35)


# ================================================================= 2 · LA MIRILLA
def scene_mirilla():
    fx, fy, fw, fh = F(2, 0)
    fl = floor(2)
    header("h2", fx, fy, "2", "POR QUÉ FUNCIONABAN", color="#ea580c", txt="#fff")
    add(f'''<div id="door" class="door2" style="{css_box(fx + 230, fy + 180, 500, 820, 3)}">
      <div id="peep" class="peep"></div></div>''')
    for k, (pid, kind, name, actress, col) in enumerate(TRIO):
        add(f'<div id="ey{k}" class="eyes2" style="{css_box(fx + 380 + (k - 1) * 70, fy + 340 + k * 34, 200, 60, 6)}opacity:0"><i></i><i></i></div>')
    add(f'<div id="tod" class="pill" style="{css_box(fx + 160, fy + 580, None, None, 8)}background:{ACC};color:{INK};font-size:52px;opacity:0">{icon("eye", 50, INK, 2.6)} SE ENTERABAN DE TODO</div>')
    for k, (pid, kind, name, actress, col) in enumerate(TRIO):
        add(character(f"pp{k}", kind, fx + 200 + k * 280, fl, 0.75, z=7))
    add(f'<div id="tuyo" class="pill" style="{css_box(fx + 120, fy + 680, None, None, 9)}background:#fff;color:{INK};font-size:46px;opacity:0">{icon("house", 44, INK, 2.6)} TODOS TENEMOS UNAS</div>')
    t_dos, t_fun, t_ojo, t_edi, t_ent, t_nad, t_tod, t_sup2, t_por = (P("dos"), P("funcionaban"), P("ojos"), P("edificio"), P("enteraban"), P("nadie"),
                                                                     P("todos"), P("supernenas", 2), P("portal"))
    travel(t_dos - 0.3, F(2, 0), 2, 570, dur=0.7)
    hide_mile(1, t_dos + 0.2)
    header_in("h2", t_dos, t_fun)
    js(f'tl.fromTo("#door", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4}}, {t_ojo - 0.3:.3f});')
    js(f'tl.fromTo("#peep", {{scale:0.4}}, {{scale:1, duration:0.4, ease:"back.out(2)"}}, {t_ojo:.3f});')
    for k in range(3):
        js(f'tl.fromTo("#ey{k}", {{opacity:0, scaleY:0.1}}, {{opacity:1, scaleY:1, duration:0.2}}, {t_edi + k * 0.15:.3f});')
        js(f'tl.to("#ey{k}", {{x:30, duration:0.3, yoyo:true, repeat:5, ease:"sine.inOut"}}, {t_ent + k * 0.1:.3f});')
    sfx(t_edi, "pop2", 0.3)
    pop("#tod", t_nad - 0.2, sound="pop")
    js(f'tl.to("#door, [id^=ey], #tod", {{opacity:0.15, duration:0.4}}, {t_tod - 0.1:.3f});')
    for k in range(3):
        life(f"pp{k}", 0, G.DUR, 10 + k)
        js(f'tl.fromTo("#pp{k}", {{opacity:0, x:-80}}, {{opacity:1, x:0, duration:0.4}}, {t_tod + k * 0.12:.3f});')
    pop("#tuyo", t_sup2 - 0.2, sound="check")
    js(f'tl.to(Q("pp0","head"), {{rotation:12, svgOrigin:PIV.head, duration:0.3, yoyo:true, repeat:1}}, {t_por:.3f}); tl.to(Q("pp2","head"), {{rotation:-12, svgOrigin:PIV.head, duration:0.3, yoyo:true, repeat:1}}, {t_por:.3f});')


# ================================================================= LAS FRASES
def scene_frases():
    fx, fy, fw, fh = F(2, 1)
    fl = floor(2)
    for k, (pid, kind, name, actress, col) in enumerate(TRIO):
        add(character(f"fr{k}", kind, fx + 170 + k * 310, fl, 0.95, z=6))
        add(f'<div id="bb{k}" class="bub3" style="{css_box(fx + 40 + k * 310, fy + 280 + (k % 2) * 90, 260, 140, 7)}border-color:{col};opacity:0">{icon("message-square", 60, col, 2.6)}<b style="color:{col}">!?</b></div>')
    for k, (x, y) in enumerate([(300, 300), (610, 330), (450, 240)]):
        add(f'<div id="zp{k}" data-layout-ignore style="{css_box(fx + x, fy + y, 110, 110, 9)}opacity:0">{icon("zap", 100, ACC, 2.6).replace("<svg", "<svg fill=\"#facc15\"")}</div>')
    add(f'<div id="mf" class="pill" style="{css_box(fx + 200, fy + 80, None, None, 9)}background:{ACC};color:{INK};font-size:56px;opacity:0">{icon("quote", 54, INK, 2.6)} LAS MEJORES FRASES</div>')
    t_y4, t_car, t_dis, t_cho, t_ell, t_sal, t_fra = P("y", 4), P("caracteres"), P("distintos"), P("chocaban"), P("ellos"), P("salian"), P("frases")
    travel(t_y4 - 0.3, F(2, 1), 2, 1630, dur=0.7)
    for k in range(3):
        life(f"fr{k}", 0, G.DUR, 13 + k)
        js(f'tl.fromTo("#fr{k}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {t_car + k * 0.15:.3f});')
        js(f'tl.fromTo("#bb{k}", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_dis + k * 0.15:.3f});')
    sfx(t_dis, "pop2", 0.3)
    js(f'tl.to("#bb0", {{x:60, duration:0.15, yoyo:true, repeat:3}}, {t_cho:.3f}); tl.to("#bb2", {{x:-60, duration:0.15, yoyo:true, repeat:3}}, {t_cho:.3f}); tl.to("#bb1", {{y:-40, duration:0.15, yoyo:true, repeat:3}}, {t_cho:.3f});')
    for k in range(3):
        js(f'tl.fromTo("#zp{k}", {{opacity:0, scale:0.3, rotation:-30}}, {{opacity:1, scale:1, rotation:0, duration:0.25, ease:"back.out(3)"}}, {t_cho + 0.1 + k * 0.1:.3f}); tl.to("#zp{k}", {{opacity:0, duration:0.3}}, {t_sal + 0.3:.3f});')
    sfx(t_cho + 0.1, "golpe", 0.35)
    shake(t_cho + 0.15, 10)
    js(f'tl.to(Q("fr1","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.2}}, {t_ell:.3f});')
    stamp("#mf", t_fra - 0.2)
    sfx(t_fra, "check", 0.35)


# ================================================================= 3 · EL IMPACTO
def scene_impacto():
    fx, fy, fw, fh = F(3, 1)
    fl = floor(3)
    header("h3", fx, fy, "3", "EL IMPACTO", color="#7c3aed", txt="#fff")
    add(f'''<div id="tv" class="tvb" style="{css_box(fx + 260, fy + 180, 440, 300, 5)}opacity:0">
      {"".join(f'<i class="tvd" style="left:{70 + k * 110}px;background:{TRIO[k][4]}"></i>' for k in range(3))}</div>''')
    add(f'<div id="pri" class="pill" style="{css_box(fx + 220, fy + 500, None, None, 8)}background:{ACC};color:{INK};font-size:48px;opacity:0">MÁXIMA AUDIENCIA</div>')
    add(f'<div id="sofa" style="{css_box(fx + 80, fl - 260, 520, 260, 4)}opacity:0">{icon("sofa", 520, "#4c1d95", 1.8).replace("<svg", "<svg fill=\"#7c3aed\"")}</div>')
    add(character("ab", "vicenta", fx + 230, fl - 60, 0.75, z=5))
    add(character("ni", "g3", fx + 430, fl - 60, 0.6, z=5))
    add(f'<div id="phone" class="phone" style="{css_box(fx + 640, fy + 600, 260, 420, 7)}opacity:0">'
        + "".join(f'<i id="mm{k}" class="meme" style="top:{30 + k * 120}px;background:{TRIO[k][4]}"></i>' for k in range(3)) + '</div>')
    t_tres, t_imp, t_pus, t_sen, t_cen, t_max, t_abu, t_nie, t_jun, t_mem = (P("tres", 3), P("impacto"), P("pusieron"), P("senoras"), P("centro"),
                                                                           P("maxima"), P("abuelas"), P("nietos"), P("juntos"), P("memes"))
    travel(t_tres - 0.3, F(3, 1), 3, 1630, dur=0.7)
    hide_mile(2, t_tres + 0.2)
    header_in("h3", t_tres, t_imp)
    js(f'tl.fromTo("#tv", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t_pus:.3f});')
    js(f'tl.fromTo(".tvd", {{scale:0}}, {{scale:1, duration:0.3, stagger:0.12, ease:"back.out(3)"}}, {t_sen:.3f});')
    sfx(t_sen, "pop2", 0.3)
    js(f'tl.to("#tv", {{boxShadow:"0 0 60px 10px rgba(250,204,21,0.6)", duration:0.4}}, {t_cen:.3f});')
    pop("#pri", t_max - 0.1, sound="pop")
    js(f'tl.fromTo("#sofa", {{opacity:0}}, {{opacity:1, duration:0.3}}, {t_abu - 0.3:.3f});')
    life("ab", 0, G.DUR, 16)
    life("ni", 0, G.DUR, 17)
    js(f'tl.fromTo("#ab", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_abu:.3f}); tl.fromTo("#ni", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_nie:.3f});')
    js(f'jump("ab", {t_jun:.3f}, 25); jump("ni", {t_jun + 0.1:.3f}, 35);')
    js(f'tl.to(Q("ab","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.2}}, {t_jun:.3f}); tl.to(Q("ni","mouth"), {{scaleX:1.3, svgOrigin:"120 136", duration:0.2}}, {t_jun:.3f});')
    sfx(t_jun, "check", 0.3)
    js(f'tl.fromTo("#phone", {{opacity:0, y:80}}, {{opacity:1, y:0, duration:0.35}}, {t_mem - 0.3:.3f});')
    js(f'tl.fromTo(".meme", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.25, stagger:0.12}}, {t_mem:.3f});')
    hearts("hm-", fx + 770, fy + 600, 4, t_mem + 0.2, spread=200, rise=240)


# ================================================================= LA QUE SE AVECINA + ESTRELLAS + COMENTARIOS
def scene_final():
    fx, fy, fw, fh = F(3, 0)
    fl = floor(3)
    new_names = ["IZASKUN", "CHARO", "MARI TERE"]
    for k, (pid, kind, name, actress, col) in enumerate(TRIO):
        add(character(f"ft{k}", kind, fx + 170 + k * 310, fl, 0.9, z=6))
        add(f'''<div id="tag{k}" class="tag2" style="{css_box(fx + 40 + k * 310, fy + 560, 260, 80, 7)}border-color:{col}">
          <span id="ta{k}" style="color:{col}">{name}</span><span id="tb{k}" style="color:{col};opacity:0">{new_names[k]}</span></div>''')
        add(f'<div id="st{k}" style="{css_box(fx + 100 + k * 310, fy + 80, 140, 140, 5)}opacity:0">{icon("star", 130, "#fde68a", 2.2).replace("<svg", f"<svg fill=\"{col}\"")}</div>')
        add(f'<div id="sy{k}" class="sy" style="{css_box(fx + 70 + k * 310, fy + 230, 200, 60, 5)}opacity:0">{["2013", "2007", "2026"][k]}</div>')
    add(f'<div id="lqsa" class="pill" style="{css_box(fx + 230, fy + 440, None, None, 8)}background:#fff;color:{INK};font-size:46px;opacity:0">{icon("tv", 44, INK, 2.6)} LA QUE SE AVECINA</div>')
    add(f'<div id="rell" class="pill" style="{css_box(fx + 170, fy + 330, None, None, 8)}background:{ACC};color:{INK};font-size:50px;opacity:0">EL RELLANO SIGUE SIENDO SUYO</div>')
    cta = "Yo era más…"
    card("cbox", fx + 40, fy + 20, 880, 500, f'''
      <div style="position:absolute;left:40px;top:28px;display:flex;align-items:center;gap:22px">{icon("message-circle", 80, INK, 2.4)}
        <span style="font:900 64px {FONT};color:{INK}">Comentarios</span></div>
      {"".join(f'<div class="poll" style="top:{130 + k * 70}px"><span style="color:{TRIO[k][4]}">{TRIO[k][2]}</span><i id="pb{k}" style="background:{TRIO[k][4]}"></i></div>' for k in range(3))}
      <div id="ctt" style="position:absolute;left:40px;top:350px;font:800 60px {FONT};color:{INK};white-space:nowrap">{chars(cta, "kc")}</div>
      <div id="pub" class="pubb">Publicar</div>''')
    add(f'<div id="cur" data-layout-ignore style="{css_box(fx + 780, fy + 430, 130, 130, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 120, "#fff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    t_las, t_pas, t_ave, t_cha, t_iza, t_mt, t_em2, t_07, t_mv, t_13, t_ge2, t_ano, t_rel, t_suy = (
        P("las", 4), P("pasaron"), P("avecina"), P("charo"), P("izaskun"), P("tere"), P("emma", 2), P("2007"), P("marivi"), P("2013"), P("gemma", 2),
        P("ano"), P("rellano"), P("suyo"))
    travel(t_las - 0.3, F(3, 0), 3, 570, dur=0.7)
    for k in range(3):
        life(f"ft{k}", 0, G.DUR, 20 + k)
        js(f'tl.fromTo("#ft{k}, #tag{k}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35}}, {t_las + k * 0.1:.3f});')
    pop("#lqsa", t_ave - 0.2, sound="pop")
    for k, t in [(1, t_cha), (0, t_iza), (2, t_mt)]:
        flip(f"#tag{k}", t - 0.1, [f"#ta{k}"], [f"#tb{k}"], sound="whoosh-corto")
    js(f'tl.to("#lqsa", {{opacity:0, duration:0.3}}, {t_em2 - 0.2:.3f});')
    for k, t in [(1, t_07), (0, t_13), (2, t_ano)]:
        js(f'tl.fromTo("#st{k}", {{opacity:0, scale:0.2, y:80}}, {{opacity:1, scale:1, y:0, duration:0.6, ease:"back.out(2)"}}, {t - 0.2:.3f});')
        js(f'tl.fromTo("#sy{k}", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t:.3f});')
        js(f'tl.to("#ft{k}", {{opacity:0.45, duration:0.6}}, {t + 0.2:.3f});')
        sfx(t, "check", 0.25)
    js(f'tl.to("[id^=st]", {{scale:1.12, duration:0.4, yoyo:true, repeat:1}}, {t_rel:.3f});')
    pop("#rell", t_rel - 0.1, sound="pop2")
    t_tu, t_mar2, t_con3, t_vic4, t_leo, t_com = P("tu"), P("marisa", 2), P("concha", 3), P("vicenta", 4), P("leo"), P("comentarios")
    js(f'tl.to("#rell, [id^=st], [id^=sy]", {{opacity:0, duration:0.3}}, {t_tu - 0.3:.3f});')
    slide_in("#cbox", t_tu - 0.3, dy=-80)
    js('tl.set("[id^=pb]", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    for k, t in enumerate([t_mar2, t_con3, t_vic4]):
        js(f'tl.to("#pb{k}", {{scaleX:1, duration:0.4, ease:"back.out(1.6)"}}, {t:.3f}); tl.to("#ft{k}", {{opacity:1, duration:0.3}}, {t:.3f}); jump("ft{k}", {t:.3f}, 30);')
        sfx(t, "pop2", 0.25)
    type_on("#ctt .kc", len(cta), t_vic4 + 0.3, t_com)
    js(f'tl.fromTo("#cur", {{opacity:0, x:200, y:200}}, {{opacity:1, x:0, y:0, duration:0.4}}, {t_leo:.3f});')
    js(f'tl.to("#cur", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_com + 0.3:.3f}); tl.to("#pub", {{scale:0.9, backgroundColor:"#166534", duration:0.1, yoyo:true, repeat:1}}, {t_com + 0.3:.3f});')
    sfx(t_com + 0.3, "click", 0.5)
    js(f'tl.to(".mile", {{opacity:1, duration:0.4}}, {E("comentarios") + 0.2:.3f});')
    cam(E("comentarios") + 0.1, (0, 100, 2200, 5200), dur=0.6, box=dict(x=60, y=390, w=960, h=1100))


CSS = """
.room {{ background:rgba(255,255,255,0.025); border:4px solid rgba(255,255,255,0.07); border-radius:40px; }}
.mile {{ border-radius:999px; background:#0f172a; border:6px solid #fff; color:#fff; font:900 46px {FONT}; text-align:center; line-height:58px; white-space:nowrap; }}
.htitle {{ font-size:72px; top:30px; }}
.frame {{ border-radius:50% / 42%; border:12px solid; background:radial-gradient(circle at 50% 35%, #fef3c7, #fcd34d 60%, #b45309); overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.pname {{ font:900 46px {FONT}; text-align:center; }}
.supt {{ border-radius:30px; background:#fff; color:#7c3aed; font:900 88px {FONT}; text-align:center; line-height:150px; white-space:nowrap; letter-spacing:-2px; }}
.plate {{ border-radius:24px; background:#fff; border:6px solid; overflow:hidden; }}
.pt {{ position:absolute; left:0; right:0; top:18px; line-height:44px; text-align:center; font:900 40px {FONT}; white-space:nowrap; }}
.ps {{ position:absolute; left:0; right:0; top:68px; line-height:40px; text-align:center; font:800 34px {FONT}; color:#475569; white-space:nowrap; }}
.poster {{ border-radius:16px; background:linear-gradient(#111827,#3f2a1d); border:8px solid #fde68a; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.pst1 {{ position:absolute; left:0; right:0; top:60px; text-align:center; font:900 54px {FONT}; color:#fff; white-space:nowrap; }}
.pst2 {{ position:absolute; left:0; right:0; top:150px; text-align:center; font:900 46px {FONT}; color:#fde68a; letter-spacing:6px; }}
.pst3 {{ position:absolute; left:0; right:0; top:280px; display:flex; justify-content:center; }}
.script {{ border-radius:14px; background:#fff; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
.sh {{ position:absolute; left:0; right:0; top:26px; text-align:center; font:900 54px {FONT}; color:{INK}; }}
.sl {{ position:absolute; left:0; right:0; top:100px; text-align:center; font:900 40px {FONT}; color:#7c3aed; }}
.sline {{ position:absolute; left:60px; height:16px; border-radius:8px; background:#cbd5e1; }}
.quote {{ border-radius:30px; background:{BAD}; color:#fff; font:900 52px {FONT}; text-align:center; display:flex; align-items:center; justify-content:center; padding:0 20px; line-height:1.15; }}
.xline {{ background:{BAD}; border-radius:7px; transform-origin:0% 50%; }}
.door2 {{ border-radius:20px 20px 0 0; background:linear-gradient(90deg,#7c4a2d,#5b3a24); border:10px solid #3f2a1d; }}
.peep {{ position:absolute; left:150px; top:120px; width:200px; height:200px; border-radius:50%; background:radial-gradient(circle,#fde68a,#ca8a04 70%); border:12px solid #a16207; }}
.eyes2 i {{ position:absolute; top:10px; width:40px; height:40px; border-radius:50%; background:#fff; border:6px solid #111; }}
.eyes2 i:first-child {{ left:40px; }} .eyes2 i:last-child {{ left:120px; }}
.bub3 {{ border-radius:40px; background:#fff; border:6px solid; display:flex; align-items:center; justify-content:center; gap:12px; font:900 64px {FONT}; }}
.tvb {{ border-radius:30px; background:#0b1220; border:14px solid #334155; }}
.tvd {{ position:absolute; top:80px; width:90px; height:130px; border-radius:45px 45px 20px 20px; }}
.phone {{ border-radius:40px; background:#0b1220; border:10px solid #e2e8f0; }}
.meme {{ position:absolute; left:24px; right:24px; height:100px; border-radius:16px; }}
.tag2 {{ border-radius:20px; background:#fff; border:6px solid; overflow:hidden; }}
.tag2 span {{ position:absolute; left:0; right:0; top:0; bottom:0; display:flex; align-items:center; justify-content:center; font:900 40px {FONT}; white-space:nowrap; }}
.sy {{ font:900 46px {FONT}; color:#fde68a; text-align:center; }}
.poll {{ position:absolute; left:40px; right:40px; height:60px; display:flex; align-items:center; gap:20px; }}
.poll span {{ width:250px; font:900 46px {FONT}; }}
.poll i {{ flex:1; height:36px; border-radius:18px; }}
.pubb {{ position:absolute; right:40px; bottom:30px; padding:12px 44px; border-radius:999px; background:{GOOD_BG}; color:#fff; font:900 62px {FONT}; }}
.kc {{ opacity:0; }}
"""


def build():
    world()
    scene_hook()
    scene_quienes()
    scene_verdugo()
    scene_casting()
    scene_mirilla()
    scene_frases()
    scene_impacto()
    scene_final()
