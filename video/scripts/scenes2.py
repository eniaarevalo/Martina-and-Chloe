"""Segunda mitad del vídeo: castings (2ºA), Tejero (3ºB), estreno (azotea) y final.
Se importa desde gen.py y usa sus mismas herramientas (P, cam, pop, roller...)."""
import gen as G
from gen import (GOOD_BG, P, E, add, js, sfx, card, css_box, icon, chars, type_on, roller, roll_to, roll_set, cam, shake,
                 pop, slide_in, stamp, floaty, life, frame, cell, COLX, ROWY, CH, FLOOR, GOOD, BAD, ACC, INK, FONT)
from rig import character


def flip(sel, t, hide, show, sound="whoosh-corto"):
    """Da la vuelta a una pieza en su sitio y cambia su contenido a mitad del giro."""
    js(f'tl.to("{sel}", {{scaleY:0, duration:0.14, ease:"power2.in"}}, {t:.3f});')
    for h in hide:
        js(f'tl.set("{h}", {{opacity:0}}, {t + 0.14:.3f});')
    for s in show:
        js(f'tl.set("{s}", {{opacity:1}}, {t + 0.14:.3f});')
    js(f'tl.to("{sel}", {{scaleY:1, duration:0.26, ease:"back.out(2.2)"}}, {t + 0.14:.3f});')
    if sound:
        G.sfx(t, sound, 0.2)


def avatar(cid, kind, size=220):
    return (f'<div class="avatar" style="width:{size}px;height:{size}px">'
            f'{character(cid, kind, size / 2, 470, 1.0, z=1)}</div>')


# ================================================================= BLOQUE 2: castings (2ºA)
CARDS = [
    # id, personaje, rig, actor que iba a ser, actor que fue
    ("k1", "JUAN CUESTA", "juan", "Pablo Carbonell", "José Luis Gil"),
    ("k2", "VICENTA", "vicenta", "María Asquerino", "Gemma Cuervo"),
    ("k3", "MAURI", "mauri", "Luis Merlo", "Luis Merlo"),
]


def scene_castings():
    fx, fy, fw, fh = frame("2", 0)
    add(f'''<div id="h2" style="{css_box(fx, fy + 10, fw, 150, 6)}">
      <div id="h2-badge" class="badge" style="background:{BAD};color:#fff"><span id="h2-b2">2</span>
        <span id="h2-b3" class="over" style="opacity:0">3</span></div>
      <div id="h2-title" class="htitle"><span id="h2-t2">IBAN A SER</span>
        <span id="h2-t3" class="over" style="opacity:0;color:{GOOD};font-size:78px;top:12px">ACABARON SIENDO</span></div></div>''')
    ys = [fy + 190, fy + 520, fy + 850]
    for (cid, role, kind, was, became), y in zip(CARDS, ys):
        add(f'<div id="{cid}-ph" class="ph" data-layout-ignore style="{css_box(fx, y, fw, 290, 4)}"></div>')
        role_el = (f'<div id="{cid}-role" style="position:absolute;left:280px;top:28px;font:900 70px {FONT};color:{INK}">'
                   f'{role}</div>')
        card(cid, fx, y, fw, 290, f'''
          <div style="position:absolute;left:30px;top:35px">{avatar(cid + "-av", kind)}</div>
          {role_el}
          <div style="position:absolute;left:280px;top:122px;height:70px;width:420px">
            <span id="{cid}-pa" class="pill" style="position:absolute;left:0;top:0;background:{BAD};color:#fff;opacity:0">IBA A SER</span>
            <span id="{cid}-pb" class="pill" style="position:absolute;left:0;top:0;background:{GOOD_BG};color:#fff;opacity:0">ACABÓ SIENDO</span></div>
          <div style="position:absolute;left:280px;top:200px;height:72px;width:640px">
            <span id="{cid}-na" style="position:absolute;left:0;top:0;font:800 58px {FONT};color:#333;opacity:0;white-space:nowrap">{was}</span>
            <span id="{cid}-nb" style="position:absolute;left:0;top:0;font:900 58px {FONT};color:#15803d;opacity:0;white-space:nowrap">{became}</span></div>
        ''', z=6)
    # pegatinas
    add(f'<div id="k1-st" class="sticker" style="{css_box(fx + 790, ys[0] - 50, 170, 170, 9)}">'
        f'{icon("clapperboard", 96, INK, 2.4)}<div class="stlab">CINE</div></div>')
    add(f'<div id="k2-st" class="sticker" style="{css_box(fx + 790, ys[1] - 50, 170, 170, 9)}">'
        f'{icon("scroll-text", 96, INK, 2.4)}<div class="stlab">GUION</div></div>')
    cnt, ch = roller("k3-cnt", "0", 90, "#fff")
    add(f'''<div id="k3-st" class="sticker" style="{css_box(fx + 790, ys[2] - 50, 170, 170, 9)}background:{BAD}">
      <div id="k3-sta" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 70px {FONT};color:#fff">×{cnt}</div>
      <div id="k3-stb" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;background:{GOOD};border-radius:50%">{icon("check", 110, "#fff", 3.4)}</div></div>''')
    for i in range(4):
        add(f'<div id="k3-x{i}" class="xdot" style="{css_box(fx + 700 + i * 62, ys[2] + 214, 54, 54, 8)}">'
            f'{icon("x", 40, "#fff", 3.6)}</div>')
    # bocadillo de Vicenta
    quote = "«Yo no quiero estar aquí»"
    add(f'''<div id="quote" class="bubble big" style="{css_box(fx + 80, ys[1] + 330, 800, None, 10)}">
      <div id="quote-t" style="font:900 62px {FONT};color:{INK};line-height:1.15">{chars(quote, "qc")}</div>
      <div class="tail"></div></div>''')

    # ---- tiempos
    t_dos, t_iban = P("dos", 2), P("iban")
    cam(t_dos, frame("2", 0), dur=0.8)
    pop("#h2-badge", t_dos, sound="pop")
    js(f'tl.fromTo("#h2-title", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {t_iban:.3f});')
    js(f'tl.fromTo(".ph", {{opacity:0, scale:0.9}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)", stagger:0.12}}, {t_iban + 0.15:.3f});')
    sfx(t_iban + 0.15, "pop2", 0.2)

    def focus(i, t, extra_h=0):
        y = ys[i]
        cam(t, (fx - 20, y - 120, fw + 40, 530 + extra_h), dur=0.55)

    # carta 1: Juan Cuesta
    t_juan, t_pablo, t_cine = P("juan", 2), P("pablo"), P("cine")
    focus(0, t_juan - 0.15)
    pop("#k1", t_juan, sound="pop")
    js(f'tl.set("#k1-pa", {{opacity:1}}, {t_pablo:.3f}); tl.fromTo("#k1-na", {{opacity:0, x:-24}}, {{opacity:1, x:0, duration:0.3}}, {t_pablo:.3f});')
    sfx(t_pablo, "pop2", 0.25)
    stamp("#k1-st", t_cine, rot=10)
    sfx(t_cine, "click", 0.5)
    life("k1-av", t_juan, G.DUR, 11)
    # carta 2: Vicenta
    t_vic, t_mar, t_gui, t_yo = P("vicenta"), P("maria"), P("guion"), P("yo")
    focus(1, t_vic - 0.15, extra_h=260)
    pop("#k2", t_vic, sound="pop")
    js(f'tl.set("#k2-pa", {{opacity:1}}, {t_mar:.3f}); tl.fromTo("#k2-na", {{opacity:0, x:-24}}, {{opacity:1, x:0, duration:0.3}}, {t_mar:.3f});')
    sfx(t_mar, "pop2", 0.25)
    stamp("#k2-st", t_gui, rot=-8)
    sfx(t_gui, "paginas", 0.35)
    life("k2-av", t_vic, G.DUR, 13)
    js(f'tilt("k2-av", {t_yo:.3f});')
    js(f'tl.fromTo("#quote", {{opacity:0, scale:0.6, transformOrigin:"20% 0%"}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_yo - 0.05:.3f});')
    type_on("#quote-t .qc", 25, t_yo, E("aqui") - 0.1)
    # carta 3: Mauri / Luis Merlo
    t_luis, t_rech, t_mau, t_cua = P("luis", 2), P("rechazo"), P("mauri"), P("cuatro")
    js(f'tl.to("#quote", {{scale:0.1, opacity:0, x:620, y:-330, duration:0.4, ease:"power3.in"}}, {t_luis - 0.05:.3f});')
    focus(2, t_luis)
    pop("#k3", t_luis, sound="pop")
    js(f'tl.set("#k3-pa", {{opacity:1}}, {t_luis:.3f}); tl.fromTo("#k3-na", {{opacity:0, x:-24}}, {{opacity:1, x:0, duration:0.3}}, {t_luis + 0.05:.3f});')
    js(f'tl.fromTo("#k3-role", {{opacity:0.15}}, {{opacity:1, duration:0.25}}, {t_mau:.3f});')
    js(f'tl.set("#k3-role", {{opacity:0.15}}, {t_luis:.3f});')
    pop("#k3-st", t_rech - 0.05, sound=None)
    roll_set("k3-cnt", "0", ch)
    steps = [t_rech, t_rech + (t_cua - t_rech) / 3, t_rech + 2 * (t_cua - t_rech) / 3, t_cua]
    for i, t in enumerate(steps):
        js(f'tl.to("#k3-cnt-d0", {{y:{-(10 + i + 1) * ch}, duration:0.2, ease:"back.out(2)"}}, {t:.3f});')
        pop(f"#k3-x{i}", t, sound="pop2", vol=0.3)
    life("k3-av", t_luis, G.DUR, 17)

    # bloque 3: los que acabaron siendo -> todo se da la vuelta en su sitio
    t_tres, t_acab = P("tres"), P("acabaron")
    cam(t_tres, frame("2", 0), dur=0.6)
    js(f'tl.to("#h2-badge", {{backgroundColor:"{GOOD}", duration:0.3}}, {t_tres:.3f});')
    flip("#h2-badge", t_tres, ["#h2-b2"], ["#h2-b3"])
    flip("#h2-title", t_acab, ["#h2-t2"], ["#h2-t3"], sound=None)
    for i, (cid, *_r) in enumerate(CARDS):
        tt = t_acab + 0.18 * i
        flip(f"#{cid}", tt, [f"#{cid}-pa", f"#{cid}-na"], [f"#{cid}-pb", f"#{cid}-nb"])
        sfx(tt + 0.2, "check", 0.3)
    flip("#k3-st", t_acab + 0.4, ["#k3-sta"], ["#k3-stb"], sound=None)
    js(f'tl.to(".xdot", {{scale:0, opacity:0, duration:0.25, stagger:0.05, ease:"back.in(2)"}}, {t_acab + 0.4:.3f});')
    for i in range(3):
        js(f'jump("k{i + 1}-av", {t_acab + 0.3 + 0.18 * i:.3f}, 30);')


# ================================================================= Vecinas de ambiente (2ºB) y salón (3ºA)
def scene_ambient():
    floor2 = FLOOR["2"]
    add(character("vec1", "vecina1", 1430, floor2, 1.5, z=4))
    add(character("vec2", "vecina2", 1820, floor2, 1.5, z=4))
    js('face("vec2", -1, 0);')
    life("vec1", 0, G.DUR, 21)
    life("vec2", 0, G.DUR, 22)
    for k in range(6):
        js(f'point("vec{1 + k % 2}", "R", {2 + k * 7.5:.2f}, {3.4 + k * 7.5:.2f}, -70);')
    add(f'<div class="sofa" data-layout-ignore style="{css_box(220, FLOOR["3"] - 260, 640, 260, 3)}"></div>')
    add(f'<div class="lamp" data-layout-ignore style="{css_box(900, FLOOR["3"] - 620, 90, 620, 3)}"></div>')


# ================================================================= BLOQUE 3: Tejero (3ºB)
def scene_tejero():
    gx, gy, gw, gh = frame("3", 1)
    floor = FLOOR["3"]
    add(f'<div id="vc-sign" style="{css_box(gx + 160, gy - 10, 640, 130, 5)}"><span id="vc-off">VIDEOCLUB</span>'
        f'<span id="vc-on" class="over" style="opacity:0">VIDEOCLUB</span></div>')
    card("tj", gx, gy + 160, gw, 230, f'''
      <div style="position:absolute;left:40px;top:24px;font:900 72px {FONT};color:{INK}">FERNANDO TEJERO</div>
      <div style="position:absolute;left:40px;top:130px;width:880px;height:74px">
        <span id="tj-pa" class="pill" style="position:absolute;left:0;top:0;background:{BAD};color:#fff;opacity:0">IBA A SER</span>
        <span id="tj-na" style="position:absolute;left:350px;top:2px;font:900 60px {FONT};color:#333;opacity:0">PACO</span>
        <span id="tj-pb" class="pill" style="position:absolute;left:0;top:0;background:{GOOD_BG};color:#fff;opacity:0">ACABÓ SIENDO</span>
        <span id="tj-nb" style="position:absolute;left:460px;top:2px;font:900 60px {FONT};color:#15803d;opacity:0">EMILIO</span></div>''')
    day, dh = roller("day", "0", 110)
    card("dia", gx + 20, gy + 440, 320, 230, f'''
      <div style="height:70px;background:{INK};border-radius:40px 40px 0 0;text-align:center;font:900 50px {FONT};color:#fff;line-height:70px">DÍA</div>
      <div style="position:absolute;left:0;right:0;top:86px;text-align:center">{day}</div>''')
    # estanterías con cintas
    tapes = []
    cols = ["#ef4444", "#3b82f6", "#f59e0b", "#22c55e", "#a855f7", "#ec4899", "#14b8a6"]
    for r in range(3):
        for c in range(8):
            tapes.append(f'<div class="tape" style="left:{20 + c * 62}px;top:{20 + r * 120}px;background:{cols[(r * 3 + c) % 7]}"></div>')
    add(f'<div id="shelves" data-layout-ignore style="{css_box(gx + 420, gy + 700, 540, 380, 2)}">{"".join(tapes)}</div>')
    add(character("paco", "paco", gx + 230, floor, 1.6, z=5))
    add(f'''<div id="counter-v" data-layout-ignore style="{css_box(gx, floor - 230, 470, 230, 6)}" class="counter">
      <div class="counter-top"></div><div class="counter-sign" style="top:56px;font-size:64px">ALQUILER</div></div>''')
    msg = "¿Y si soy el portero?"
    add(f'''<div id="pb" class="bubble big" style="{css_box(gx + 330, gy + 400, 300, None, 10)}">
      <div id="pb-t" style="font:900 48px {FONT};color:{INK};line-height:1.15">{chars(msg, "pc")}</div><div class="tail l"></div></div>''')

    # ---- tiempos
    t_fer, t_paco, t_vc = P("fernando"), P("paco"), P("videoclub")
    js('tl.set("#paco .cap", {scale:0, svgOrigin:"120 50"}, 0); tl.set("#paco .broom", {scale:0, svgOrigin:"169 304"}, 0);')
    cam(t_fer, frame("3", 1), dur=0.85)
    slide_in("#tj", t_fer + 0.25, dy=-60, sound="pop")
    js(f'tl.set("#tj-pa", {{opacity:1}}, {t_paco:.3f}); tl.fromTo("#tj-na", {{opacity:0, x:-24}}, {{opacity:1, x:0, duration:0.3}}, {t_paco:.3f});')
    sfx(t_paco, "pop2", 0.3)
    js(f'wave("paco", {t_paco:.3f}, {t_paco + 1.2:.3f});')
    js(f'tl.to("#paco .armR", {{rotation:0, svgOrigin:"169 188", duration:0.3}}, {t_paco + 1.25:.3f});')
    js(f'tl.to("#vc-on", {{opacity:1, duration:0.12, repeat:3, yoyo:true}}, {t_vc:.3f}); tl.set("#vc-on", {{opacity:1}}, {t_vc + 0.5:.3f});')
    sfx(t_vc, "click", 0.35)
    life("paco", 0, G.DUR, 31)
    t_pid, t_port, t_tres, t_emi = P("pidio"), P("portero", 2), P("tres", 2), P("emilio", 2)
    js(f'point("paco", "L", {t_pid:.3f}, {t_port + 0.2:.3f}, 150);')
    js(f'tl.fromTo("#pb", {{opacity:0, scale:0.5, transformOrigin:"0% 100%"}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t_pid:.3f});')
    type_on("#pb-t .pc", len(msg), t_pid + 0.05, t_port + 0.35)
    # sale de detrás del mostrador
    js(f'tl.to("#paco", {{x:430, duration:0.65, ease:"power1.inOut"}}, {t_port + 0.3:.3f});')
    js(f'walk("paco", {t_port + 0.3:.3f}, {t_port + 0.95:.3f}, 0.16);')
    js(f'tl.to("#pb", {{x:300, y:-30, duration:0.65, ease:"power1.inOut"}}, {t_port + 0.3:.3f});')
    pop("#dia", t_tres, sound=None)
    roll_set("day", "0", dh)
    for i, tt in enumerate([t_tres, t_tres + 0.22, t_tres + 0.44]):
        js(f'tl.to("#day-d0", {{y:{-(10 + i + 1) * dh}, duration:0.18, ease:"back.out(2)"}}, {tt:.3f});')
        sfx(tt, "pop2", 0.25)
    # se transforma en Emilio en su sitio
    js(f'tl.to("#paco .shirt, #paco .sleeve", {{attr:{{fill:"#2f62c0"}}, duration:0.35}}, {t_emi:.3f});')
    js(f'tl.to("#paco .nametag", {{opacity:0, duration:0.2}}, {t_emi:.3f}); tl.to("#paco .buttons", {{opacity:1, duration:0.3}}, {t_emi + 0.1:.3f});')
    js(f'tl.to("#pb", {{scale:0.1, opacity:0, x:120, y:120, duration:0.3, ease:"power3.in"}}, {t_emi - 0.1:.3f});')
    js(f'tl.to("#paco .cap", {{scale:1, svgOrigin:"120 50", duration:0.4, ease:"back.out(3)"}}, {t_emi + 0.1:.3f});')
    js(f'tl.to("#paco .broom", {{scale:1, svgOrigin:"169 304", duration:0.4, ease:"back.out(2)"}}, {t_emi + 0.2:.3f});')
    js(f'jump("paco", {t_emi + 0.15:.3f}, 50);')
    flip("#tj", t_emi, ["#tj-pa", "#tj-na"], ["#tj-pb", "#tj-nb"])
    sfx(t_emi + 0.25, "check", 0.4)
    # bloque entero: castings + Tejero
    t_blk = t_emi + 0.5
    cam(t_blk, (COLX[0], ROWY["3"], 2120, 2 * CH), dur=0.3)
    js(f'face("paco", 1, {t_blk:.3f});')
    js(f'tl.to("#paco", {{x:1100, duration:1.1, ease:"power1.in"}}, {t_blk + 0.2:.3f});')
    js(f'walk("paco", {t_blk + 0.2:.3f}, {t_blk + 1.3:.3f}, 0.15);')


# ================================================================= BLOQUE 4: el estreno (azotea)
def scene_estreno():
    rx, ry, rw = 620, 110, 960
    add(f'''<div id="h4" style="{css_box(rx, ry + 10, rw, 150, 6)}">
      <div id="h4-badge" class="badge" style="background:{ACC}">4</div>
      <div id="h4-title" class="htitle">EL ESTRENO</div></div>''')
    aud, ah = roller("aud", "0.000.000", 118, "#fff")
    add(f'''<div id="tv" style="{css_box(rx + 40, ry + 190, 880, 520, 5)}">
      <div class="ant a1"></div><div class="ant a2"></div>
      <div id="tv-screen" class="screen">
        <div id="tv-date" style="font:900 64px {FONT};color:#fff;opacity:0">7 SEP 2003</div>
        <div style="margin-top:6px">{aud}</div>
        <div id="tv-lab" style="font:800 50px {FONT};color:#cfd8ff;opacity:0">espectadores</div></div>
      <div class="knob k1"></div><div class="knob k2"></div></div>''')
    big, bh = roller("big", "0.000.000", 84)
    path = "M 40 170 L 330 120 L 560 80 L 800 20"
    card("chart", rx + 40, ry + 740, 880, 390, f'''
      <div style="position:absolute;left:36px;top:28px;font:900 52px {FONT};color:#555">NOV 2003</div>
      <div style="position:absolute;right:36px;top:18px">{big}</div>
      <svg style="position:absolute;left:20px;top:110px" width="840" height="190" viewBox="0 0 840 190">
        <path d="M 40 180 L 800 180" stroke="#e5e7eb" stroke-width="6"/>
        <path id="chart-line" d="{path}" stroke="{GOOD}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <circle id="chart-dot0" cx="40" cy="170" r="16" fill="{GOOD}"/>
        <circle id="chart-dot" cx="800" cy="20" r="20" fill="{GOOD}"/>
        <circle id="chart-ring" cx="800" cy="20" r="20" fill="none" stroke="{GOOD}" stroke-width="6"/></svg>
      <div style="position:absolute;left:36px;top:300px;width:420px;height:62px;border-radius:31px;background:#e5e7eb;overflow:hidden">
        <div id="bar" style="width:100%;height:100%;background:{GOOD};border-radius:31px"></div></div>
      <div id="bar-lab" style="position:absolute;left:480px;top:296px;font:900 60px {FONT};color:{INK};opacity:0">40,1 % cuota</div>''')

    t_cua, t_est = P("cuatro", 2), P("estreno")
    cam(t_cua, (rx, ry, rw, 1140), dur=0.85)
    pop("#h4-badge", t_cua, sound="pop")
    js(f'tl.fromTo("#h4-title", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {t_est:.3f});')
    t_sep, t_2003, t_dos = P("septiembre"), P("2003"), P("dos", 3)
    js(f'tl.fromTo("#tv-screen", {{backgroundColor:"#0b0d14"}}, {{backgroundColor:"#1d3fa8", duration:0.35}}, {t_sep:.3f});')
    sfx(t_sep, "click", 0.4)
    js(f'tl.fromTo("#tv-date", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {t_2003:.3f});')
    roll_set("aud", "0000000", ah)
    roll_to("aud", "2507000", ah, t_dos, dur=1.0, spins=1, stagger=0.05)
    js(f'tl.to("#tv-lab", {{opacity:1, duration:0.3}}, {t_dos + 0.4:.3f});')
    floaty("#tv", t_dos + 1.2, G.DUR, 5, 2.6)
    # clímax
    t_nov, t_73, t_40 = P("noviembre"), P("7,3"), P("40%")
    slide_in("#chart", t_nov - 0.1, dy=140, dur=0.45)
    js('tl.set("#chart-line", {strokeDasharray:900, strokeDashoffset:900}, 0); tl.set("#chart-dot, #chart-ring", {scale:0, svgOrigin:"800 20"}, 0);')
    js('tl.set("#bar", {scaleX:0, transformOrigin:"0% 50%"}, 0);')
    js(f'tl.to("#chart-line", {{strokeDashoffset:0, duration:{max(0.3, t_73 - t_nov):.2f}, ease:"power2.in"}}, {t_nov:.3f});')
    roll_set("big", "0000000", bh)
    roll_to("big", "7308000", bh, t_73, dur=0.9, spins=2, stagger=0.04)
    js(f'tl.to("#chart-dot", {{scale:1, svgOrigin:"800 20", duration:0.3, ease:"back.out(3)"}}, {t_73:.3f});')
    js(f'tl.fromTo("#chart-ring", {{scale:1, opacity:1}}, {{scale:4, opacity:0, svgOrigin:"800 20", duration:0.7, ease:"power2.out", immediateRender:false}}, {t_73:.3f});')
    shake(t_73, 22)
    sfx(t_73, "golpe-climax", 0.55)
    js(f'tl.to("#bar", {{scaleX:0.401, duration:0.6, ease:"power3.out"}}, {t_40:.3f});')
    js(f'tl.fromTo("#bar-lab", {{opacity:0, x:-20}}, {{opacity:1, x:0, duration:0.3}}, {t_40:.3f});')
    sfx(t_40, "pop", 0.35)


# ================================================================= FINAL: cartel y comentarios
def scene_final():
    yr, yh = roller("bbyr", "2006", 120, "#666")
    js('tl.set("#bb-a .bbsub", {opacity:0}, 0);')
    BB = [f'<div id="bb-yr" style="{css_box(0, 600, 1900, 150, 5)}text-align:center;opacity:0">{yr}</div>']
    m59, mh = roller("m59", "0,0", 330, INK)
    BB.append(f'''<div id="bb-b" style="{css_box(0, 0, 1900, 780, 5)}opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
      <div style="display:flex;align-items:baseline;gap:30px">{m59}<span style="font:900 260px {FONT};color:{INK}">M</span></div>
      <div id="bb-b2" style="font:800 110px {FONT};color:#555;opacity:0;margin-top:-10px">personas al mes</div></div>''')
    BB.append(f'''<div id="bb-c" style="{css_box(0, 0, 1900, 780, 5)}opacity:0">
      <div style="position:absolute;left:80px;top:60px;display:flex;align-items:center;gap:30px">{icon("message-circle", 120, INK, 2.6)}
        <span style="font:900 110px {FONT};color:{INK}">Comentarios</span></div>
      <div class="cbox"><div class="cav">{icon("users", 90, "#fff", 2.6)}</div>
        <div id="ctext" style="font:800 110px {FONT};color:{INK}">{chars("Yo sería…", "cc")}<span id="caret" class="caret"></span></div></div>
      <div id="cbtn" class="cbtn">Publicar</div></div>''')
    for i, h in enumerate(G.HTML):
        if h.startswith('<div id="bb" '):
            G.HTML[i] = h.replace('<div id="bb-a" class="bbface">', "".join(BB) + '<div id="bb-a" class="bbface">')
    add(f'<div id="cursor" data-layout-ignore style="{css_box(1760, -250, 160, 160, 12)}opacity:0">'
        f'{icon("mouse-pointer-2", 150, "#ffffff", 2.2).replace("<svg", "<svg fill=\"#111\"")}</div>')
    # vecinos que suben a la azotea
    roof = FLOOR["roof"]
    cast = [("f-vec1", "vecina1", 140), ("f-juan", "juan", 330), ("f-vic", "vicenta", 520),
            ("f-mau", "mauri", 1680), ("f-emi", "emilio", 1870), ("f-vec2", "vecina2", 2060)]
    for cid, kind, x in cast:
        add(character(cid, kind, x, roof, 1.35, z=7))

    t_vei, t_desp, t_59, t_pers = P("veinte"), P("despues"), P("5,9"), P("personas")
    cam(t_vei, (40, -900, 2120, 2200), dur=0.9)
    js(f'tl.fromTo("#bb", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.55, ease:"back.out(1.6)"}}, {t_vei:.3f});')
    sfx(t_vei, "pop", 0.35)
    js(f'tl.fromTo("#bb-yr", {{opacity:0}}, {{opacity:1, duration:0.25}}, {t_vei + 0.3:.3f});')
    roll_set("bbyr", "2006", yh)
    js(f'tl.to("#bbyr-d2", {{y:{-(10 + 2) * yh}, duration:0.7, ease:"power3.out"}}, {t_desp:.3f});')
    sfx(t_desp, "tic-rodillo", 0.3)
    flip("#bb", t_59 - 0.1, ["#bb-a", "#bb-yr"], ["#bb-b"])
    roll_set("m59", "00", mh)
    roll_to("m59", "59", mh, t_59, dur=0.7, spins=1)
    js(f'tl.fromTo("#bb-b2", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {t_pers:.3f});')
    floaty("#bb", t_59 + 0.6, G.DUR, 8, 2.8)
    # comentarios
    t_com, t_des, t_ser = P("comenta"), P("desengano"), P("serias")
    flip("#bb", t_com, ["#bb-b"], ["#bb-c"])
    type_on("#ctext .cc", 10, t_com + 0.35, t_des)
    js(f'tl.fromTo("#caret", {{opacity:1}}, {{opacity:0, duration:0.3, repeat:{int((G.DUR - t_com) / 0.3)}, yoyo:true, ease:"steps(1)"}}, {t_com:.3f});')
    js(f'tl.fromTo("#cursor", {{opacity:0, x:-500, y:500}}, {{opacity:1, x:0, y:0, duration:0.7, ease:"power2.out"}}, {t_des:.3f});')
    js(f'tl.to("#cursor", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, {t_ser:.3f});')
    js(f'tl.to("#cbtn", {{scale:0.92, duration:0.08, yoyo:true, repeat:1}}, {t_ser:.3f});')
    js(f'tl.to("#cbtn", {{backgroundColor:"#166534", duration:0.2}}, {t_ser + 0.1:.3f});')
    sfx(t_ser, "click", 0.5)
    sfx(t_ser + 0.15, "check", 0.4)
    huts = {True: 230, False: 1970}
    for k, (cid, kind, x) in enumerate(cast):
        left = x < 1100
        door = huts[left]
        t0 = t_com - 0.2 + (k % 3) * 0.18
        js(f'tl.fromTo("#{cid}", {{x:{door - x}, opacity:0}}, {{x:0, opacity:1, duration:0.7, ease:"power1.out"}}, {t0:.3f});')
        js(f'face("{cid}", {1 if left else -1}, 0);')
        js(f'walk("{cid}", {t0:.3f}, {t0 + 0.7:.3f}, 0.14);')
        js(f'face("{cid}", 1, {t0 + 0.75:.3f});')
        life(cid, t0, G.DUR, 40 + k)
        js(f'wave("{cid}", {t0 + 0.9 + (k % 2) * 0.15:.3f}, {G.DUR - 0.1:.3f});')
        js(f'jump("{cid}", {t_ser + 0.15 + (k % 3) * 0.08:.3f}, 40);')
