"""Detail drawings for the proof sheets (Detail_Drawings tab).

Every drawing: viewBox 0 0 100 100, printed about 1.32" square on the proof.
Style:  WALL = gray + hatch   PARTS = black outline   HARDWARE = red   ACRYLIC / POLY = light blue
        LIGHT = yellow   EARTH = tan + hatch   CONCRETE = gray + stipple   LABELS = 5 pt Arial
Placeholders: {VARIABLE} or {VARIABLE|fallback} are replaced with the part's current value
(upper case) when the proof is drawn, e.g. {EMBED DEPTH} -> 36".
Only plain shapes (rect, line, path, circle, polygon, text): no ids, no gradients, so many
drawings can share a page and the SVG stays editable in Illustrator / CorelDRAW.
"""
WALL_F, HATCH, INK, HW, ACR, ACR_S, LBL = "#D9D9D9", "#9A9A9A", "#231F20", "#C1272D", "#DCEEF6", "#5B9BBF", "#444444"
ALUM, LED, GLOW, EARTH, EARTH_H, CONC = "#BCBEC0", "#F5B400", "#FFE680", "#EFE6D6", "#B9A88A", "#D3D3D3"
FS, LH = 5.2, 6.0


def f(v):
    return f"{v:g}" if isinstance(v, (int, float)) else v


def rect(x, y, w, h, fill="#FFFFFF", stroke=INK, sw=0.9, extra=""):
    s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}"{s}{extra}/>'


def line(x1, y1, x2, y2, stroke=INK, sw=0.9, extra=""):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{stroke}" stroke-width="{f(sw)}"{extra}/>'


def path(d, fill="none", stroke=INK, sw=0.9, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}"{extra}/>'


def circ(cx, cy, r, fill="#FFFFFF", stroke=INK, sw=0.8):
    s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}"{s}/>'


def text(x, y, lines, color=LBL, anchor="start", bold=False, size=FS):
    if isinstance(lines, str):
        lines = [lines]
    b = ' font-weight="bold"' if bold else ""
    return "".join(f'<text x="{f(x)}" y="{f(y + i * LH)}" font-family="Arial" font-size="{f(size)}"{b} fill="{color}" '
                   f'text-anchor="{anchor}">{t}</text>' for i, t in enumerate(lines))


def _tw(t, bold=False):
    import re
    t = re.sub(r"&#\d+;", "o", re.sub(r"\{([^{}|]+)(\|[^{}]*)?\}", lambda m: "X" * 8, t))
    return len(t) * FS * (0.62 if bold else 0.56)


def call(px, py, tx, ty, lines, color=LBL, anchor="start", bold=False):
    """Leader from a point on the part (dot) to the nearest edge of the label, never through it."""
    ls = [lines] if isinstance(lines, str) else lines
    w = max(_tw(t, bold) for t in ls)
    x0 = tx if anchor == "start" else tx - w if anchor == "end" else tx - w / 2
    x1, y0, y1 = x0 + w, ty - FS * 0.8, ty + (len(ls) - 1) * LH + 1
    if px < x0 - 1:
        ex, ey = x0 - 1, ty - 1.7
    elif px > x1 + 1:
        ex, ey = x1 + 1, ty - 1.7
    else:
        ex, ey = px, (y1 + 1.2) if py > y1 else (y0 - 1.2)
    return (line(px, py, ex, ey, color, 0.45) + circ(px, py, 0.9, color, None) +
            text(tx, ty, lines, color, anchor, bold))


def wall(x0=4, x1=15, y0=6, y1=94, label=True):
    h = "".join(line(x0, y, x1, y - (x1 - x0), HATCH, 0.45) for y in range(int(y0 + (x1 - x0)), int(y1) + 1, 6))
    out = rect(x0, y0, x1 - x0, y1 - y0, WALL_F, None) + h + line(x1, y0, x1, y1, INK, 1.1)
    return out


def hdim(x0, x1, y, label, color=LBL, above=True):
    t = 2
    return (line(x0, y, x1, y, color, 0.45) + line(x0, y - t, x0, y + t, color, 0.45) + line(x1, y - t, x1, y + t, color, 0.45) +
            text((x0 + x1) / 2, y - 1.6 if above else y + 5.6, label, color, "middle"))


def vdim(x, y0, y1, label_lines, color=LBL):
    t = 2
    return (line(x, y0, x, y1, color, 0.45) + line(x - t, y0, x + t, y0, color, 0.45) + line(x - t, y1, x + t, y1, color, 0.45) +
            text(x + 3, (y0 + y1) / 2 - (len(label_lines) - 1) * LH / 2 + 1.8, label_lines, color))


def stud(x0, x1, y, t=1.5):
    return rect(x0, y - t / 2, x1 - x0, t, HW, None)


def earth(y0, x0=0, x1=100, y1=100):
    h = "".join(line(x, y1, x + 9, y1 - 9, EARTH_H, 0.4) for x in range(int(x0) - 6, int(x1), 7))
    return (rect(x0, y0, x1 - x0, y1 - y0, EARTH, None) +
            "".join(line(x, y0 + 4, x + 3, y0 + 1, EARTH_H, 0.4) for x in range(int(x0) + 2, int(x1), 6)) +
            line(x0, y0, x1, y0, INK, 1.0))


def concrete(x, y, w, h):
    dots = ""
    k = 0
    for yy in range(int(y) + 3, int(y + h) - 1, 4):
        for xx in range(int(x) + 2 + (k % 2) * 2, int(x + w) - 1, 4):
            dots += circ(xx, yy, 0.38, "#8A8A8A", None)
        k += 1
    return rect(x, y, w, h, CONC, INK, 0.8) + dots


def led(x, y, w=3.2, h=6):
    return rect(x, y, w, h, LED, "#B07F00", 0.4, ' rx="0.8"')


def rays(x0, y, x1, n=3, spread=5):
    return "".join(line(x0, y, x1, y + (i - (n - 1) / 2) * spread, "#E0A800", 0.45, ' stroke-dasharray="1.4,1"') for i in range(n))


D = []   # (id, category, title, components, match_rule, notes, markup)


def add(did, cat, title, comps, rule, notes, body):
    D.append((did, cat, title, comps, rule, notes, body))


# =====================================================================  MOUNTING
add("MNT_TAPE", "Mounting", "VHB TAPE MOUNT", "", "MOUNTING~=Tape",
    "Panel bonded flat to the wall with VHB tape.",
    wall() +
    "".join(rect(15, y, 3.2, 10, HW, None) for y in (18, 45, 72)) +
    rect(18.2, 10, 4.5, 80) +
    call(16.6, 23, 34, 24.5, "VHB TAPE", HW, bold=True) +
    call(20.5, 60, 34, 61.5, "SIGN PANEL"))

add("MNT_STUD_FLUSH", "Mounting", "STUD MOUNT - FLUSH", "",
    "MOUNTING=Stud Mount - Flush OR BACKER MOUNTING=Stud Mount",
    "Threaded studs set into drilled holes with adhesive; panel sits tight to the wall.",
    wall() +
    "".join(rect(6, y - 1.8, 9, 3.6, "#FFFFFF", HATCH, 0.4) for y in (28, 72)) +
    rect(15, 10, 4.5, 80) +
    "".join(stud(7, 17.5, y) for y in (28, 72)) +
    call(10, 28, 30, 29.5, "THREADED STUD", HW, bold=True) +
    call(7.5, 72, 30, 70.5, ["DRILLED HOLE", "+ ADHESIVE"]) +
    call(17.2, 50, 30, 51.5, "SIGN PANEL"))

add("MNT_STUD_SPACER", "Mounting", "STUD MOUNT - SPACER", "", "MOUNTING=Stud Mount - Spacer",
    "Studs with spacers hold the panel off the wall. Gap comes from MOUNTING DETAIL.",
    wall() +
    "".join(rect(15, y - 3.5, 12, 7, "#FFFFFF", HW, 0.9) + stud(7, 30, y) for y in (28, 72)) +
    rect(27, 10, 4.5, 80) +
    call(21, 24.5, 40, 18.5, "SPACER", HW, bold=True) +
    call(10, 72, 40, 83.5, "THREADED STUD", HW, bold=True) +
    call(29.2, 50, 40, 51.5, "SIGN PANEL") +
    hdim(15, 27, 93.5, "GAP", above=False))

add("MNT_STANDOFFS", "Mounting", "STAND-OFF MOUNT", "", "MOUNTING=Stand-offs|Standoffs",
    "Barrel stand-offs fastened to the wall; caps clamp the panel.",
    wall() +
    "".join(stud(7, 16, y, 1.2) + rect(15, y - 4.5, 14, 9, "#FFFFFF", HW, 0.9, ' rx="1.5"') +
            rect(33.5, y - 5, 3.8, 10, HW, None, 0, ' rx="1.2"') for y in (24, 76)) +
    rect(29, 10, 4.5, 80, ACR, ACR_S) +
    call(22, 19.5, 44, 13, "STAND-OFF", HW, bold=True) +
    call(35.4, 80, 44, 88, "CAP", HW, bold=True) +
    call(31.2, 50, 44, 51.5, "SIGN PANEL") +
    hdim(15, 29, 96, "DEPTH", above=False))

add("MNT_RACEWAY", "Mounting", "RACEWAY MOUNT", "CHANNEL_LETTERS_FL", "MOUNTING=Raceway",
    "Letters mounted to a painted raceway; power supply inside the raceway.",
    wall() +
    rect(15, 56, 13, 18, "#FFFFFF", HW, 1.1) + stud(7, 16, 65, 1.4) +
    rect(17, 61, 7, 8, "#FFFFFF", HW, 0.5) + text(20.5, 67, "PS", HW, "middle", True, 4.2) +
    rect(28, 18, 22, 64) +
    rect(50, 18, 3, 64, ACR, ACR_S, 0.7) + rect(52.6, 16.5, 2.4, 67, INK, None) +
    "".join(led(28.8, y) for y in (28, 47, 66)) +
    path("M 34 62 Q 30 66 24 65", extra=' stroke-dasharray="1.2,0.8"', sw=0.6) +
    call(24, 74, 38, 92, "RACEWAY", HW, bold=True) +
    call(39, 18, 62, 13, "RETURN") +
    call(51.5, 40, 62, 41.5, "FACE") +
    call(53.8, 81, 62, 81.5, "TRIM CAP"))

add("MNT_FLUSH_CL", "Mounting", "FLUSH MOUNT (LETTERS)", "CHANNEL_LETTERS_FL", "MOUNTING=Flush Mount",
    "Letters stud-mounted directly to the wall; wires pass through the wall to a remote power supply.",
    rect(1, 44, 7, 11, "#FFFFFF", HW, 0.8) + text(4.5, 51.5, "PS", HW, "middle", True, 4.2) +
    wall(9, 19) +
    rect(19, 18, 22, 64) +
    rect(41, 18, 3, 64, ACR, ACR_S, 0.7) + rect(43.6, 16.5, 2.4, 67, INK, None) +
    "".join(led(19.8, y) for y in (28, 47, 66)) +
    "".join(stud(11, 22, y, 1.4) for y in (24, 76)) +
    path("M 24 56 L 8 50", extra=' stroke-dasharray="1.2,0.8"', sw=0.6) +
    call(14, 24, 54, 16, ["MOUNTING", "STUD"], HW, bold=True) +
    call(13, 51.5, 54, 52, ["WIRES TO", "REMOTE PS"]) +
    call(30, 82, 54, 86.5, "RETURN") +
    call(42.5, 36, 54, 33, "FACE"))

add("MNT_PUSH_THRU", "Mounting", "PUSH-THRU DETAIL", "",
    "MOUNTING=Push-Thru OR ROUTING=Push-Thru OR COPY TYPE=Push-Thru Acrylic",
    "Thick acrylic copy pushed through the routed face and lit from inside the cabinet.",
    rect(6, 8, 38, 84, "#F7F7F7", INK, 0.6, ' stroke-dasharray="2,1.2"') +
    rect(40, 8, 3.2, 30, INK, None) + rect(40, 62, 3.2, 30, INK, None) +
    rect(33, 38, 17, 24, ACR, ACR_S, 0.8) +
    rect(8, 8, 2.5, 84, ALUM, INK, 0.5) +
    "".join(led(10.5, y) for y in (20, 47, 74)) +
    rays(13.7, 50, 32, 3, 6) +
    call(41.6, 22, 56, 21, ["ROUTED", "ALUM. FACE"]) +
    call(47, 50, 56, 51.5, ["PUSH-THRU", "ACRYLIC"], ACR_S, bold=True) +
    call(12, 77, 56, 82, "LED MODULES", "#B07F00") +
    text(24, 98, "CABINET", HATCH, "middle"))

add("MNT_HANG_SWING", "Mounting", "HANGING BRACKET - SWING", "", "MOUNTING=Hanging Bracket - Swinging",
    "Sign hangs from eye bolts and S-hooks so it can swing.",
    wall(3, 11) +
    rect(11, 10, 4, 20, HW, None) + rect(15, 16, 70, 3.5, HW, None) + circ(85, 17.75, 2.4, HW, None) +
    "".join(circ(x, 23.5, 2.1, "none", HW, 0.9) + circ(x, 28.6, 2.1, "none", HW, 0.9) +
            line(x, 30.7, x, 38, HW, 0.9) for x in (30, 70)) +
    rect(22, 38, 56, 40) + text(50, 60, "SIGN", HATCH, "middle", True, 6) +
    path("M 36 86 Q 50 92 64 86", stroke=LBL, sw=0.5) + path("M 61.5 84.2 L 64 86 L 61 87.5", stroke=LBL, sw=0.5) +
    path("M 38.5 84.2 L 36 86 L 39 87.5", stroke=LBL, sw=0.5) +
    text(50, 97, "SWINGS FREELY", LBL, "middle") +
    call(55, 17.7, 62, 9, "BRACKET", HW, bold=True) +
    call(72, 26, 82, 30, ["EYE BOLTS", "+ S-HOOKS"], HW))

add("MNT_HANG_FIXED", "Mounting", "HANGING BRACKET - FIXED", "", "MOUNTING=Hanging Bracket - Fixed",
    "Sign bolted rigidly under the bracket arm (does not swing).",
    wall(3, 11) +
    rect(11, 10, 4, 20, HW, None) + rect(15, 16, 70, 3.5, HW, None) +
    "".join(rect(x - 1.8, 19.5, 3.6, 24, HW, None) + circ(x, 22.5, 1.1, "#FFFFFF", None) +
            circ(x, 40.5, 1.1, "#FFFFFF", None) for x in (30, 70)) +
    rect(22, 34, 56, 44) + text(50, 59, "SIGN", HATCH, "middle", True, 6) +
    call(55, 17.7, 62, 9, "BRACKET", HW, bold=True) +
    call(71.8, 30, 82, 30, ["FIXED", "STRAPS", "+ BOLTS"], HW) +
    text(50, 90, "DOES NOT SWING", LBL, "middle"))

add("MNT_BLADE", "Mounting", "BLADE BRACKET", "", "MOUNTING=Blade Bracket",
    "Projecting (blade) sign held off the wall by a bracket; readable from both sides.",
    wall(3, 11) +
    rect(11, 14, 4, 72, HW, None) +
    "".join(rect(15, y - 1.6, 17, 3.2, HW, None) + circ(13, y, 1, "#FFFFFF", None) for y in (30, 70)) +
    rect(32, 20, 50, 60) +
    "".join(circ(35, y, 1.1, HW, None) for y in (30, 70)) +
    text(57, 48, "BLADE", HATCH, "middle", True, 6) + text(57, 55, "SIGN", HATCH, "middle", True, 6) +
    call(13, 82, 22, 92, "WALL PLATE", HW, bold=True) +
    call(24, 30, 40, 11, "BRACKET ARMS", HW, bold=True) +
    text(57, 66, "DOUBLE SIDED", LBL, "middle"))

# =====================================================================  LETTER CONSTRUCTION
add("LTR_FRONT_LIT", "Letter Construction", "FRONT LIT SECTION", "CHANNEL_LETTERS_FL", "",
    "Section through one letter stroke: LEDs light the acrylic face from inside.",
    wall(3, 12) +
    rect(12, 16, 2.4, 68, ALUM, INK, 0.6) +
    rect(14.4, 14.5, 32, 2.6, ALUM, INK, 0.6) + rect(14.4, 82.9, 32, 2.6, ALUM, INK, 0.6) +
    rect(46.4, 16, 3, 68, ACR, ACR_S, 0.7) +
    rect(45.5, 12.8, 5.6, 4.2, INK, None) + rect(49.4, 12.8, 1.7, 9, INK, None) +
    rect(45.5, 83, 5.6, 4.2, INK, None) + rect(49.4, 78.2, 1.7, 9, INK, None) +
    "".join(led(14.6, y) + rays(17.8, y + 3, 45.8, 3, 4) for y in (27, 47, 67)) +
    "".join(stud(5, 16, y, 1.3) for y in (22, 78)) +
    hdim(12, 46.4, 8, "{RETURN|RETURN}") +
    call(50.2, 14, 58, 12, ["TRIM CAP", "{TRIM CAP}"], INK, bold=True) +
    call(48, 38, 58, 34, ["ACRYLIC", "FACE"], ACR_S, bold=True) +
    call(17, 50, 58, 52, "LED MODULES", "#B07F00") +
    call(34, 86, 34, 96, "ALUM. RETURN", LBL, "middle"))

add("LTR_HALO_LIT", "Letter Construction", "HALO LIT SECTION", "HALO_LETTERS", "LETTER TYPE=Reverse Lit (Halo)",
    "Section: solid face, LEDs shine back through a clear back to wash the wall with light.",
    wall(3, 12) +
    path("M 12 12 L 24 22 L 24 78 L 12 88 Z", GLOW, None, 0) +
    "".join(stud(5, 24, y, 1.2) + rect(12, y - 3, 12, 6, ALUM, HW, 0.8, ' rx="1"') for y in (30, 70)) +
    rect(24, 18, 2.4, 64, ACR, ACR_S, 0.6) +
    rect(26.4, 16.5, 22, 2.6, ALUM, INK, 0.6) + rect(26.4, 80.9, 22, 2.6, ALUM, INK, 0.6) +
    rect(48.4, 16.5, 3.4, 67, "#5A5A5A", INK, 0.6) +
    "".join(led(45, y) + rays(45, y + 3, 26.6, 3, 4) for y in (31, 47, 63)) +
    hdim(24, 51.8, 10, "{RETURN DEPTH|RETURN}") +
    call(50, 30, 60, 22, ["ALUM.", "FACE"], INK, bold=True) +
    call(46.6, 50, 60, 41, "LEDS", "#B07F00") +
    call(25.2, 60, 60, 56, ["CLEAR", "BACK"], ACR_S, bold=True) +
    call(18, 70, 60, 72, ["STAND-OFF", "{STANDOFFS}"], HW, bold=True) +
    call(14, 84, 17, 96, "HALO GLOW", "#B07F00"))

add("LTR_TRIMCAP", "Letter Construction", "TRIM CAP & RETURN", "CHANNEL_LETTERS_FL", "",
    "Close-up of the letter edge: trim cap holds the acrylic face to the return.",
    rect(6, 36, 54, 6, ACR, ACR_S, 0.8) +
    rect(54, 42, 4, 54, ALUM, INK, 0.8) +
    path("M 46 33 L 61 33 L 61 62 L 58 62 L 58 36 L 46 36 Z", INK, None) +
    circ(59.5, 54, 1.4, HW, None) +
    text(30, 70, ["LETTER", "INTERIOR"], HATCH, "middle") +
    call(52, 34.5, 70, 22, ["TRIM CAP", "{TRIM CAP}"], INK, bold=True) +
    call(22, 39, 22, 28, "ACRYLIC FACE", ACR_S, "middle", True) +
    call(59.5, 54, 70, 50, "SCREW", HW, bold=True) +
    call(56, 82, 70, 80, ["RETURN", "{RETURN}"]))

# =====================================================================  CABINET CONSTRUCTION
_cab_inside = "".join(led(23.5, y) + rays(26.7, y + 3, 50, 3, 5) for y in (28, 47, 66))
add("CAB_EXTRUSION", "Cabinet Construction", "EXTRUSION CABINET", "CABINET", "CONSTRUCTION=Extrusion",
    "Side section: extruded aluminum body with built-in face retainer.",
    wall(3, 12) +
    path("M 12 12 L 54 12 L 54 20 L 50 20 L 50 17 L 20 17 L 20 83 L 50 83 L 50 80 L 54 80 L 54 88 L 12 88 Z", ALUM, INK, 0.8) +
    line(16, 12, 16, 88, INK, 0.35) + line(12, 14.5, 50, 14.5, INK, 0.35) + line(12, 85.5, 50, 85.5, INK, 0.35) +
    rect(20, 17, 2.4, 66, "#FFFFFF", INK, 0.4) + _cab_inside +
    rect(50.5, 20, 3, 60, ACR, ACR_S, 0.7) +
    rect(52, 11, 5, 10, INK, None) + rect(52, 79, 5, 10, INK, None) +
    call(33, 13.5, 64, 10, ["EXTRUDED", "ALUM. BODY"], INK, bold=True) +
    call(55, 16, 64, 27, "RETAINER", INK) +
    call(52, 46, 64, 47.5, ["POLY", "FACE"], ACR_S, bold=True) +
    call(25, 70, 64, 72, "LED MODULES", "#B07F00"))

add("CAB_STICK", "Cabinet Construction", "STICK BUILT CABINET", "CABINET", "CONSTRUCTION~=Stick Built",
    "Side section: aluminum angle frame wrapped in aluminum skin; separate screwed retainer.",
    wall(3, 12) +
    rect(12, 12, 40, 1.2, "#FFFFFF", INK, 0.6) + rect(12, 86.8, 40, 1.2, "#FFFFFF", INK, 0.6) + rect(12, 12, 1.2, 76, "#FFFFFF", INK, 0.6) +
    path("M 13.2 13.2 L 21 13.2 L 21 15.6 L 15.6 15.6 L 15.6 21 L 13.2 21 Z", HW, None) +
    path("M 13.2 86.8 L 21 86.8 L 21 84.4 L 15.6 84.4 L 15.6 79 L 13.2 79 Z", HW, None) +
    path("M 50.8 13.2 L 43 13.2 L 43 15.6 L 48.4 15.6 L 48.4 21 L 50.8 21 Z", HW, None) +
    path("M 50.8 86.8 L 43 86.8 L 43 84.4 L 48.4 84.4 L 48.4 79 L 50.8 79 Z", HW, None) +
    _cab_inside.replace('x="23.5"', 'x="16.5"') +
    rect(50.8, 18, 3, 64, ACR, ACR_S, 0.7) +
    path("M 46 11 L 57 11 L 57 21 L 53.8 21 L 53.8 12.2 L 46 12.2 Z", INK, None) +
    path("M 46 89 L 57 89 L 57 79 L 53.8 79 L 53.8 87.8 L 46 87.8 Z", INK, None) +
    call(15, 20, 64, 22, ["ANGLE", "FRAME"], HW, bold=True) +
    call(30, 12.6, 64, 8.5, "ALUM. SKIN", INK) +
    call(55.4, 88, 64, 90, "RETAINER", INK) +
    call(52.3, 50, 64, 51.5, ["POLY", "FACE"], ACR_S, bold=True) +
    call(18, 70, 64, 72, "LED MODULES", "#B07F00"))

_ret_base = (rect(6, 40, 52, 5, ACR, ACR_S, 0.8) + rect(54, 45, 4.5, 51, ALUM, INK, 0.8) +
             text(28, 66, ["CABINET", "INTERIOR"], HATCH, "middle"))
add("CAB_RET_FLAT", "Cabinet Construction", "FLAT RETAINER", "CABINET,PANEL_FRAME",
    "RETAINER TYPE=Standard (Flat) OR RETAINERS~=Flat",
    "Flat aluminum angle retainer screwed to the cabinet side.",
    _ret_base +
    path("M 42 36.5 L 62 36.5 L 62 62 L 58.5 62 L 58.5 40 L 42 40 Z", INK, None) +
    circ(60.25, 55, 1.4, HW, None) +
    call(50, 38.2, 68, 24, ["FLAT", "RETAINER", "{RETAINER SIZE|}"], INK, bold=True) +
    call(20, 42.5, 20, 30, "POLY FACE", ACR_S, "middle", True) +
    call(60.25, 55, 68, 52, "SCREW", HW, bold=True) +
    call(56, 82, 68, 80, ["CABINET", "SIDE"]))

add("CAB_RET_FORMED", "Cabinet Construction", "FORMED RETAINER", "CABINET,PANEL_FRAME",
    "RETAINER TYPE=Formed OR RETAINERS~=Formed",
    "Formed (radius) retainer: bent profile gives a finished, beveled edge.",
    _ret_base +
    path("M 38 40 L 38 36.5 L 44 36.5 Q 50 36.5 52 30 L 54 26.5 L 62 26.5 L 62 62 L 58.5 62 L 58.5 30 L 56 30 "
         "L 55 32.5 Q 52 40 44 40 Z", INK, None) +
    circ(60.25, 55, 1.4, HW, None) +
    call(55, 28.2, 68, 18, ["FORMED", "RETAINER", "{RETAINER SIZE|}"], INK, bold=True) +
    call(20, 42.5, 20, 30, "POLY FACE", ACR_S, "middle", True) +
    call(60.25, 55, 68, 52, "SCREW", HW, bold=True) +
    call(56, 82, 68, 80, ["CABINET", "SIDE"]))

# =====================================================================  FOOTERS AND POLES
def _pole(y_bottom, top=4):
    return rect(45, top, 10, y_bottom - top, ALUM, INK, 0.8) + line(47.5, top, 47.5, y_bottom, "#FFFFFF", 0.6)


add("FTG_CONCRETE", "Footers and Poles", "CONCRETE FOOTER", "POLE",
    "FOOTER=Concrete (80 lb Bags)|Engineered Concrete Footer",
    "Pole set in a concrete footer. Embed depth comes from the spec.",
    earth(40) + concrete(34, 40, 32, 52) + _pole(86) +
    path("M 34 40 L 30 37 M 66 40 L 70 37", stroke=INK, sw=0.5) +
    vdim(73, 40, 86, ["EMBED", "{EMBED DEPTH}"], INK) +
    text(3, 37, "GRADE", LBL) +
    call(50, 14, 60, 12, "POLE", INK, bold=True) +
    call(38, 70, 3, 60, ["CONCRETE", "FOOTER"], INK, bold=True))

add("FTG_DIRECT", "Footers and Poles", "DIRECT BURIAL", "POLE", "FOOTER=Direct Burial",
    "Pole set directly in compacted gravel / soil (no concrete).",
    earth(40) + rect(36, 40, 28, 52, "#E6E1D8", INK, 0.6, ' stroke-dasharray="1.5,1"') +
    "".join(circ(x, y, 1.1, "#FFFFFF", "#8A8A8A", 0.35) for y in range(45, 90, 5)
            for x in range(39 + (y % 2) * 2, 62, 5)) + _pole(86) +
    vdim(71, 40, 86, ["EMBED", "{EMBED DEPTH}"], INK) +
    text(3, 37, "GRADE", LBL) +
    call(50, 14, 60, 12, "POLE", INK, bold=True) +
    call(39, 70, 3, 60, ["GRAVEL", "BACKFILL"], INK, bold=True))

add("FTG_BASEPLATE", "Footers and Poles", "BASE PLATE MOUNT", "POLE", "FOOTER=Surface Mount Base Plate",
    "Pole welded to a base plate, bolted to anchor bolts in a concrete pier or slab.",
    earth(58) + concrete(28, 54, 44, 46) +
    "".join(rect(x - 0.8, 42, 1.6, 50, HW, None) + rect(x - 2.4, 46, 4.8, 2.4, HW, None) for x in (33, 67)) +
    rect(28, 50.6, 44, 3.4, HW, None) +
    path("M 45 50.6 L 38 50.6 L 45 40 Z M 55 50.6 L 62 50.6 L 55 40 Z", HW, None) +
    _pole(50.6) +
    text(3, 56, "GRADE", LBL) +
    call(50, 14, 60, 12, "POLE", INK, bold=True) +
    call(70, 52.3, 76, 40, ["BASE", "PLATE"], HW, bold=True) +
    call(67, 70, 76, 74, ["ANCHOR", "BOLTS"], HW, bold=True) +
    call(68, 92, 76, 90, ["CONCRETE", "PIER"], INK, bold=True))

# =====================================================================  PANEL FINISHING  (front views)
_corner = lambda x, y, dx, dy: path(f"M {x + dx * 6} {y} L {x + dx * 6} {y + dy * 6} L {x} {y + dy * 6}", stroke=HW, sw=0.5)
add("PNL_SQUARE", "Panel Finishing", "SQUARE CUT", "SIGN_PANEL,ACM_PANEL,PVC_PANEL,CORO_SIGN,ACRYLIC_PANEL",
    "CUSTOM SHAPE=No (Square Cut) & CORNERS=Square OR ROUTING=No & CORNERS=Square",
    "Straight-cut rectangle, square corners.",
    rect(14, 24, 72, 50) + _corner(14, 24, 1, 1) + _corner(86, 24, -1, 1) + _corner(14, 74, 1, -1) + _corner(86, 74, -1, -1) +
    text(50, 47, "STRAIGHT CUT", LBL, "middle", True) + text(50, 54, "EDGES", LBL, "middle", True) +
    call(84, 26, 86, 14, "90\u00b0 CORNERS", HW, "end", True) +
    hdim(14, 86, 84, "W", above=False) + vdim(91, 24, 74, ["H"]))

add("PNL_ROUTED", "Panel Finishing", "ROUTED SHAPE", "SIGN_PANEL,ACM_PANEL,PVC_PANEL,CORO_SIGN,ACRYLIC_PANEL",
    "CUSTOM SHAPE~=Yes OR ROUTING~=Yes",
    "Panel CNC-routed to a custom outline.",
    path("M 14 80 L 14 44 C 14 14 86 14 86 44 L 86 80 Z", "#FFFFFF", INK, 1) +
    path("M 11.5 82.5 L 11.5 44 C 11.5 10.5 88.5 10.5 88.5 44 L 88.5 82.5 Z", stroke=HW, sw=0.6, extra=' stroke-dasharray="2,1.3"') +
    text(50, 52, "CUSTOM", LBL, "middle", True) + text(50, 59, "SHAPE", LBL, "middle", True) +
    call(88.5, 60, 72, 92, "CNC ROUTER PATH", HW, "end", True))

add("PNL_ROUNDED", "Panel Finishing", "ROUNDED CORNERS", "", "CORNERS~=Rounded",
    "Corners radiused; size from the CORNERS value.",
    rect(14, 24, 72, 50, "#FFFFFF", INK, 1, ' rx="7"') +
    path("M 79 24 A 7 7 0 0 1 86 31", stroke=HW, sw=1.4) +
    text(50, 47, "RADIUS", LBL, "middle", True) + text(50, 54, "CORNERS", LBL, "middle", True) +
    call(84, 26, 86, 14, "{CORNERS}", HW, "end", True) +
    hdim(14, 86, 84, "W", above=False) + vdim(91, 24, 74, ["H"]))


def _banner(grom):
    out = rect(8, 24, 84, 52) + rect(11, 27, 78, 46, "none", HATCH, 0.4, ' stroke-dasharray="1.4,1"')
    return out + "".join(circ(x, y, 1.7, "#FFFFFF", INK, 0.7) + circ(x, y, 0.7, ALUM, None) for x, y in grom)


_edge = [(x, 26.5) for x in range(11, 90, 13)] + [(x, 73.5) for x in range(11, 90, 13)] + \
        [(10.5, y) for y in (39, 50, 61)] + [(89.5, y) for y in (39, 50, 61)]
_edge = [(min(max(x, 10.5), 89.5), y) for x, y in _edge]
add("PNL_GROMMET_EDGE", "Panel Finishing", "GROMMET SPACING", "BANNER", "GROMMETS=Yes & GROMMET SPACING~=Every",
    "Grommets at corners and evenly spaced along hemmed edges.",
    _banner(_edge) +
    text(50, 14, "{GROMMET SPACING}", INK, "middle", True) +
    hdim(37, 50, 19.5, "") +
    text(50, 52, "BANNER", HATCH, "middle", True, 6) +
    call(30, 73, 30, 88, "HEMMED EDGE", LBL, "middle"))

add("PNL_GROMMET_CORNERS", "Panel Finishing", "GROMMETS - CORNERS", "BANNER", "GROMMETS=Yes & GROMMET SPACING=Corners Only",
    "Grommets at the four corners only.",
    _banner([(10.5, 26.5), (89.5, 26.5), (10.5, 73.5), (89.5, 73.5)]) +
    text(50, 52, "BANNER", HATCH, "middle", True, 6) +
    call(89.5, 26.5, 88, 14, "CORNER GROMMETS", INK, "end", True) +
    call(30, 73, 30, 88, "HEMMED EDGE", LBL, "middle"))

add("PNL_POLE_POCKET", "Panel Finishing", "POLE POCKETS", "BANNER", "POLE POCKETS=Yes",
    "Sewn pockets for poles; locations from POCKET LOCATIONS.",
    rect(20, 22, 60, 56) +
    rect(20, 22, 60, 9, "#EDEDED", INK, 0.8) + rect(20, 69, 60, 9, "#EDEDED", INK, 0.8) +
    line(20, 31, 80, 31, INK, 0.45, ' stroke-dasharray="1.2,0.9"') + line(20, 69, 80, 69, INK, 0.45, ' stroke-dasharray="1.2,0.9"') +
    rect(12, 24.5, 76, 4, ALUM, INK, 0.6, ' rx="2"') + rect(12, 71.5, 76, 4, ALUM, INK, 0.6, ' rx="2"') +
    text(50, 52, "BANNER", HATCH, "middle", True, 6) +
    call(30, 26.5, 30, 14, "POLE POCKET", INK, "middle", True) +
    call(64, 69, 76, 88, "STITCHED", LBL, "end") +
    text(50, 96, "{POCKET LOCATIONS}", INK, "middle", True))

SAMPLE = {"EMBED DEPTH": '36"', "RETURN": '5" .040', "TRIM CAP": '1"', "RETURN DEPTH": '3"', "STANDOFFS": '1.5" ALUMINUM',
          "RETAINER SIZE": '1.5"', "CORNERS": 'ROUNDED 1/2"', "GROMMET SPACING": 'CORNERS & EVERY 18"~24"',
          "POCKET LOCATIONS": "TOP AND BOTTOM", "MOUNTING DETAIL": ""}


def fill(markup, values):
    import re

    def rep(m):
        var, _, fb = m.group(1).partition("|")
        v = values.get(var.strip(), "")
        return (v or fb).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    return re.sub(r"\{([^{}]+)\}", rep, markup)


if __name__ == "__main__":
    import cairosvg
    S = "/tmp/claude-0/-home-claude/acc1ae59-fc94-5c54-82d5-acb68bbab5a0/scratchpad/"
    T, CAP, G, NC = 220, 26, 16, 6
    rows = (len(D) + NC - 1) // NC
    W, H = NC * (T + G) + G, rows * (T + CAP + G) + G + 40
    parts = [f'<rect width="{W}" height="{H}" fill="#F3F4F6"/>',
             f'<text x="{G}" y="30" font-family="Arial" font-size="20" font-weight="bold" fill="{INK}">DETAIL DRAWINGS ({len(D)})</text>']
    for i, (did, cat, title, comps, rule, notes, body) in enumerate(D):
        x, y = G + (i % NC) * (T + G), 44 + (i // NC) * (T + CAP + G)
        parts.append(f'<g transform="translate({x},{y})"><rect width="{T}" height="{T + CAP}" fill="#FFFFFF" stroke="#BCBEC0"/>'
                     f'<g transform="translate(6,6) scale({(T - 12) / 100})">{fill(body, SAMPLE)}</g>'
                     f'<rect y="{T}" width="{T}" height="{CAP}" fill="{INK}"/>'
                     f'<text x="{T / 2}" y="{T + 17}" font-family="Arial" font-size="12" font-weight="bold" fill="#FFFFFF" text-anchor="middle">{title.replace("&", "&amp;")}</text></g>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(parts) + "</svg>"
    open(S + "details_sheet.svg", "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "details_sheet.png", output_width=W)
    print("ok", len(D), W, H)
