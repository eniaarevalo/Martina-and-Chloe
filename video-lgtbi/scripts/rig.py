"""Personajes 2D en SVG: cabeza, cuerpo, brazos y piernas articulados, ojos que parpadean.
Todos comparten el mismo esqueleto (viewBox 240x440, pies en y=430) para que las
animaciones (respirar, andar, saludar...) funcionen igual en todos."""

PIVOT = {
    "armL": "71 188", "armR": "169 188", "legL": "107 296", "legR": "133 296",
    "head": "120 160", "upper": "120 300", "eyes": "120 106", "rig": "120 430",
}

PAL = {
    "juan":    dict(skin="#f1c7a0", hair="#3b2a20", shirt="#5d6474", sleeve="#5d6474", pants="#2b2f3a"),
    "emilio":  dict(skin="#e8b48a", hair="#17171b", shirt="#2f62c0", sleeve="#2f62c0", pants="#1e2f5c"),
    "paco":    dict(skin="#e8b48a", hair="#17171b", shirt="#d94b4b", sleeve="#d94b4b", pants="#1e2f5c"),
    "vicenta": dict(skin="#f0c9a8", hair="#c9c9d2", shirt="#8a56b8", sleeve="#8a56b8", pants="#d9b9a0"),
    "mauri":   dict(skin="#f2c49e", hair="#6b4426", shirt="#16a596", sleeve="#16a596", pants="#e6dfcf"),
    "vecina1": dict(skin="#e9bb93", hair="#6b3b2a", shirt="#3fae6a", sleeve="#3fae6a", pants="#e2b796"),
    "vecina2": dict(skin="#f1cfae", hair="#e0b44e", shirt="#f0883e", sleeve="#f0883e", pants="#e8c3a0"),
    "fernando": dict(skin="#efc29b", hair="#4a2f1f", shirt="#8e2a3c", sleeve="#8e2a3c", pants="#2f3542"),
    "bea":     dict(skin="#f3cdab", hair="#2b1d16", shirt="#e0a100", sleeve="#e0a100", pants="#33415c"),
    "g1":      dict(skin="#c98e64", hair="#1b1b1b", shirt="#2563eb", sleeve="#2563eb", pants="#334155"),
    "g2":      dict(skin="#f2c9a5", hair="#b45309", shirt="#db2777", sleeve="#db2777", pants="#1f2937"),
    "g3":      dict(skin="#8d5a3b", hair="#111111", shirt="#16a34a", sleeve="#16a34a", pants="#3f3f46"),
}
# estilo de pelo de cada personaje nuevo (reutiliza los dibujos que ya existen)
HAIR_STYLE = {"fernando": "juan", "bea": "mauri", "g1": "emilio", "g2": "vecina2", "g3": "juan"}


def _hair(kind, c):
    kind = HAIR_STYLE.get(kind, kind)
    if kind == "juan":
        return (f'<path d="M64 102 Q62 46 120 44 Q178 46 176 102 Q170 74 150 68 Q120 60 92 70 Q70 78 64 102 Z" fill="{c}"/>'
                f'<rect x="60" y="92" width="10" height="26" rx="5" fill="{c}"/><rect x="170" y="92" width="10" height="26" rx="5" fill="{c}"/>')
    if kind in ("emilio", "paco"):
        return (f'<path d="M62 100 L70 58 L86 70 L96 44 L112 62 L124 38 L136 60 L152 44 L160 68 L176 58 L178 100 '
                f'Q160 76 120 74 Q80 76 62 100 Z" fill="{c}"/>')
    if kind == "vicenta":
        return (f'<circle cx="120" cy="40" r="24" fill="{c}"/>'
                f'<path d="M62 108 Q58 50 120 50 Q182 50 178 108 Q172 80 150 74 Q120 68 90 74 Q68 80 62 108 Z" fill="{c}"/>')
    if kind == "mauri":
        return (f'<path d="M64 98 Q60 40 128 34 Q176 34 180 70 Q182 96 176 100 Q168 70 140 66 Q100 62 80 76 Q68 86 64 98 Z" fill="{c}"/>')
    if kind == "vecina1":
        curls = "".join(f'<circle cx="{x}" cy="{y}" r="18" fill="{c}"/>' for x, y in
                        [(70, 90), (82, 62), (106, 48), (134, 48), (158, 62), (170, 90)])
        rolls = "".join(f'<rect x="{x}" y="{y}" width="22" height="13" rx="6" fill="#f39bc1"/>' for x, y in
                        [(96, 40), (124, 40), (150, 56)])
        return curls + rolls
    if kind == "vecina2":
        return (f'<path d="M58 132 Q50 46 120 44 Q190 46 182 132 L166 132 Q170 88 150 76 Q120 66 90 76 Q70 88 74 132 Z" fill="{c}"/>')
    return ""


def _torso_details(kind):
    if kind == "juan":
        return ('<path d="M100 170 L120 214 L140 170 Z" fill="#ffffff"/>'
                '<path d="M114 176 L126 176 L130 238 L120 250 L110 238 Z" fill="#c0392b"/>')
    if kind in ("emilio", "paco"):
        btn_op = "1" if kind == "emilio" else "0"
        tag_op = "0" if kind == "emilio" else "1"
        return (f'<g class="buttons" opacity="{btn_op}"><circle cx="120" cy="200" r="6" fill="#f4c542"/>'
                '<circle cx="120" cy="232" r="6" fill="#f4c542"/><circle cx="120" cy="264" r="6" fill="#f4c542"/>'
                '<path d="M98 172 L120 190 L142 172" stroke="#f4c542" stroke-width="5" fill="none"/></g>'
                f'<g class="nametag" opacity="{tag_op}"><rect x="128" y="196" width="34" height="20" rx="4" fill="#ffd43b"/></g>')
    if kind == "vicenta":
        return ('<path d="M96 170 L120 196 L144 170" stroke="#f3e9ff" stroke-width="6" fill="none"/>'
                '<path d="M70 262 L170 262 L182 318 L58 318 Z" fill="#4b3a5a"/>')
    if kind == "mauri":
        return ('<path d="M98 170 L112 192 L120 176 L128 192 L142 170 Z" fill="#ffffff"/>')
    if kind == "fernando":
        return ('<path d="M92 168 L120 190 L148 168 L148 182 L120 204 L92 182 Z" fill="#ffffff"/>'
                '<path d="M74 240 L166 240" stroke="#6e1f2e" stroke-width="8"/><path d="M74 272 L166 272" stroke="#6e1f2e" stroke-width="8"/>')
    if kind == "bea":
        return ('<path d="M100 168 L120 300 L140 168" stroke="#ffffff" stroke-width="14" fill="none"/>'
                '<rect x="86" y="214" width="20" height="14" rx="3" fill="#7c4a00"/>')
    if kind in ("g1", "g2", "g3"):
        return '<rect x="70" y="250" width="100" height="14" fill="#000" opacity="0.15"/>'
    if kind in ("vecina1", "vecina2"):
        return ('<path d="M68 250 L172 250 L186 320 L54 320 Z" fill="currentColor" opacity="0.9"/>'
                '<rect x="94" y="196" width="52" height="54" rx="10" fill="#ffffff" opacity="0.85"/>')
    return ""


def _head_extra(kind):
    out = ""
    if kind == "juan":
        out += ('<g fill="none" stroke="#222" stroke-width="4"><circle cx="100" cy="106" r="15"/>'
                '<circle cx="140" cy="106" r="15"/><path d="M115 106 L125 106"/></g>')
    if kind in ("emilio", "paco"):
        sc = "1" if kind == "emilio" else "0"
        out += (f'<g class="cap" data-s="{sc}"><path d="M60 70 Q64 26 120 24 Q176 26 180 70 Z" fill="#1d3f86"/>'
                '<rect x="56" y="64" width="128" height="14" rx="7" fill="#132c61"/>'
                '<path d="M120 70 L186 70 Q196 78 184 84 L120 80 Z" fill="#132c61"/>'
                '<circle cx="120" cy="46" r="8" fill="#f4c542"/></g>')
    if kind == "vicenta":
        out += '<circle cx="64" cy="124" r="6" fill="#ffffff"/><circle cx="176" cy="124" r="6" fill="#ffffff"/>'
    return out


def _prop(kind):
    if kind in ("emilio", "paco"):
        sc = "1" if kind == "emilio" else "0"
        return (f'<g class="broom" data-s="{sc}"><rect x="165" y="170" width="9" height="236" rx="4" fill="#b07a3c"/>'
                '<path d="M150 400 L190 400 L200 446 L140 446 Z" fill="#e2b84b"/>'
                '<path d="M150 412 L190 412" stroke="#b58d2c" stroke-width="4"/></g>')
    return ""


def character(cid, kind, cx, floor, sc=1.0, extra_cls="", z=5):
    p = PAL[kind]
    w, h = 240 * sc, 440 * sc
    left, top = cx - 120 * sc, floor - 430 * sc
    mouth = '<path class="mouth" d="M104 132 Q120 146 136 132" stroke="#6a2e1e" stroke-width="5" fill="none" stroke-linecap="round"/>'
    brows = ('<path class="brows" d="M88 88 Q100 82 112 88 M128 88 Q140 82 152 88" stroke="#2a1d16" '
             'stroke-width="5" fill="none" stroke-linecap="round"/>')
    color_attr = f' color="{p["shirt"]}"'
    return f'''<svg id="{cid}" class="chr {extra_cls}" data-layout-ignore viewBox="0 0 240 440" width="{w:.0f}" height="{h:.0f}"
  style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;overflow:visible;z-index:{z}"{color_attr}>
  <ellipse class="shadow" cx="120" cy="432" rx="70" ry="12" fill="#000" opacity="0.35"/>
  <g class="rig">
    <g class="legL"><rect x="94" y="292" width="26" height="130" rx="13" fill="{p['pants']}"/><ellipse cx="102" cy="426" rx="22" ry="11" fill="#1b1b1f"/></g>
    <g class="legR"><rect x="120" y="292" width="26" height="130" rx="13" fill="{p['pants']}"/><ellipse cx="138" cy="426" rx="22" ry="11" fill="#1b1b1f"/></g>
    <g class="upper">
      <rect class="shirt" x="70" y="166" width="100" height="144" rx="38" fill="{p['shirt']}"/>
      {_torso_details(kind)}
      <g class="head">
        <rect x="108" y="146" width="24" height="30" fill="{p['skin']}"/>
        <circle cx="120" cy="104" r="56" fill="{p['skin']}"/>
        <circle cx="64" cy="108" r="10" fill="{p['skin']}"/><circle cx="176" cy="108" r="10" fill="{p['skin']}"/>
        {_hair(kind, p['hair'])}
        <g class="eyes"><ellipse cx="100" cy="106" rx="7" ry="9" fill="#16161a"/><ellipse cx="140" cy="106" rx="7" ry="9" fill="#16161a"/>
          <circle cx="102" cy="103" r="2.4" fill="#fff"/><circle cx="142" cy="103" r="2.4" fill="#fff"/></g>
        {brows}
        <circle cx="86" cy="128" r="9" fill="#ff8a8a" opacity="0.35"/><circle cx="154" cy="128" r="9" fill="#ff8a8a" opacity="0.35"/>
        {mouth}
        {_head_extra(kind)}
      </g>
      <g class="armL"><rect class="sleeve" x="58" y="180" width="26" height="120" rx="13" fill="{p['sleeve']}"/><circle cx="71" cy="304" r="15" fill="{p['skin']}"/></g>
      <g class="armR">{_prop(kind)}<rect class="sleeve" x="156" y="180" width="26" height="120" rx="13" fill="{p['sleeve']}"/><circle cx="169" cy="304" r="15" fill="{p['skin']}"/></g>
    </g>
  </g>
</svg>'''
