"""v2.1: Monument Letters - permanent 3D dimensional letters on a low-profile, ground-fixed monument or
free-standing sign. Usually set on TOP of the monument (letters stand on their bottoms, pinned or bonded);
face mounting with studs is also offered.

  MONUMENT_LETTERS: own component (blue Letters family) and an optional section of Monument Signs.
  LIGHTING picks the construction: non-lit (flat cut / cast / HDU plate THICKNESS, or fabricated FACE and
  RETURN GAUGE + DEPTH), front lit (channel letter: acrylic / poly face, trim cap, returns, LEDs) or halo lit
  (reverse channel: aluminum face, returns, clear back, LEDs).
"""
from legacy_components import standoff_rows
C1, C2, C3, C4, C5 = "COLUMN 1", "COLUMN 2", "COLUMN 3", "COLUMN 4", "COLUMN 5"
# LIGHTING decides the construction:
#   Non-Lit / Ground Lit  -> flat cut, cast, routed or fabricated letters (plate thickness, or gauges + depth)
#   Front Lit             -> front lit channel letters: acrylic / poly face, trim cap, aluminum returns, LEDs
#   Halo Lit              -> reverse channel letters: aluminum face, returns, clear back, LEDs
UNLIT = "LIGHTING=Non-Lit|Ground Lit (by others)"
FRONT, HALO, LIT = "LIGHTING=Front Lit", "LIGHTING=Halo Lit", "LIGHTING=Front Lit|Halo Lit"
FAB_NL = "Fabricated Aluminum"
TYPES = f"Flat Cut Aluminum|{FAB_NL}|Cast Aluminum|Flat Cut Stainless Steel|Flat Cut Brass|Flat Cut Acrylic|Flat Cut PVC|HDU (Routed)"
UNLIT_FAB, UNLIT_FLAT = f"{UNLIT}&LETTER TYPE={FAB_NL}", f"{UNLIT}&LETTER TYPE!={FAB_NL}"
GAUGES, RET_GAUGES = ".040|.050|.063|.080|.090|.125", ".040|.050|.063"

# (zone, variable, label, type, default, options, show_if, required, signos_ref, notes, hide_values)
FIELDS = [
    (C1, "TEXT", "TEXT", "text", "", "", "", "Yes", "", "What the letters say", ""),
    (C1, "QTY & SIZES", "QTY / SIZE", "text", "", "", "", "Yes", "", "Quantity @ letter height; separate sizes with commas, e.g. 10 @ 18\", 4 @ 12\"", ""),
    (C1, "FONT", "FONT", "text", "", "", "", "", "", "Typeface name", ""),

    # ---- construction (depends on LIGHTING)
    (C2, "LIGHTING", "LIGHTING", "select", "Non-Lit", "Non-Lit|Front Lit|Halo Lit|Ground Lit (by others)", "", "Yes", "",
     "Front lit = channel letters; halo lit = reverse channel letters", ""),
    (C2, "LETTER TYPE", "TYPE", "select", "Flat Cut Aluminum", TYPES, UNLIT, "Yes", "", "", ""),
    (C2, "MATERIAL THICKNESS", "THICKNESS", "select", '1/2"', '1/8"|3/16"|1/4"|3/8"|1/2"|3/4"|1"|1-1/2"|2"', UNLIT_FLAT, "Yes", "",
     "Plate thickness of flat cut, cast or routed letters", ""),
    (C2, "FACE MATERIAL", "FACE", "select", '3/16" Acrylic', '3/16" Acrylic|3/16" Polycarbonate', FRONT, "Yes", "", "Translucent lit face", ""),
    (C2, "FACE GAUGE", "FACE", "select", ".063", GAUGES, HALO, "Yes", "", "Aluminum face of the reverse channel letter", ""),
    (C2, "FACE GAUGE - UNLIT", "FACE", "select", ".063", GAUGES, UNLIT_FAB, "Yes", "", "Aluminum sheet thickness of the letter face", ""),
    (C2, "RETURN GAUGE", "RETURN", "select", ".040", RET_GAUGES, LIT, "Yes", "", "Aluminum thickness of the letter sides", ""),
    (C2, "RETURN GAUGE - UNLIT", "RETURN", "select", ".040", RET_GAUGES, UNLIT_FAB, "Yes", "", "", ""),
    (C2, "LETTER DEPTH", "DEPTH", "select", '5"', '2"|3"|4"|5"|6"', LIT, "Yes", "", "Return depth of the lit letters", ""),
    (C2, "LETTER DEPTH - UNLIT", "DEPTH", "select", '3"', '1-1/2"|2"|3"|4"|5"|6"', UNLIT_FAB, "Yes", "", "", ""),
    (C2, "TRIM CAP", "TRIM CAP", "select", '1"', '3/4"|1"|2"', FRONT, "Yes", "", "", ""),
    (C2, "BACKS", "BACKS", "select", '3/16" Clear Polycarbonate', '3/16" Clear Polycarbonate|1/4" Clear Acrylic', HALO, "Yes", "", "Clear back lets the halo out", ""),

    # ---- colors and finish
    (C3, "FINISH", "FINISH", "select", "Painted", "Painted|Brushed|Polished|Anodized|Natural / Mill", "LIGHTING!=Front Lit", "Yes", "", "", ""),
    (C3, "LETTER COLOR", "COLOR", "paint", "", "", "LIGHTING!=Front Lit&FINISH=Painted", "Yes", "", "", ""),
    (C3, "FACE COLOR", "FACE COLOR", "color", "White", "White|Clear|Red", FRONT, "Yes", "", "", ""),
    (C3, "FACE VINYL", "VINYL", "select", "None", "None|Translucent Vinyl|Translucent Digital Print", FRONT, "", "", "", "None"),
    (C3, "VINYL COLOR", "VINYL COLOR", "vinyl", "8500", "8500|8800", f"{FRONT}&FACE VINYL=Translucent Vinyl", "Yes", "", "", ""),
    (C3, "TRIM CAP COLOR", "TRIM CAP COLOR", "db", "", "TRIMCAP", FRONT, "Yes", "", "", ""),
    (C3, "RETURN COLOR - COIL", "RETURN COLOR", "db", "", "COIL", FRONT, "Yes", "", "", ""),
    (C3, "RETURN COLOR", "RETURN COLOR", "finish", "Match Face", "Match Face|Black|Bronze|White", f"{HALO}&FINISH=Painted", "", "", "", ""),
    (C3, "RETURN COLOR - UNLIT", "RETURN COLOR", "finish", "Match Face", "Match Face|Black|Bronze|White", f"{UNLIT_FAB}&FINISH=Painted", "", "", "", ""),

    # ---- mounting
    (C4, "MOUNTING", "MOUNTING", "select", "Top Mount - Pinned",
     "Top Mount - Pinned|Top Mount - Adhesive|Stud Mount - Flush|Stud Mount - Spacer|Standoffs", "", "Yes", "",
     "Top mount: letters stand on the monument cap, touching on their bottoms", ""),
    (C4, "PIN SIZE", "PINS", "select", '1/4"-20 Threaded Rod', '#10-24 Stud|1/4"-20 Threaded Rod|3/8"-16 Threaded Rod',
     "MOUNTING=Top Mount - Pinned|Stud Mount - Flush|Stud Mount - Spacer", "Yes", "", "", ""),
    (C4, "PIN EMBED", "PIN EMBED", "select", '2"', '1"|1-1/2"|2"|3"|4"', "MOUNTING=Top Mount - Pinned", "Yes", "",
     "Depth the pins go into the monument", ""),
    (C4, "SPACER DEPTH", "SPACER", "select", '1"', '1/2"|3/4"|1"|1-1/2"', "MOUNTING=Stud Mount - Spacer", "Yes", "", "", ""),
] + standoff_rows(C4, "MOUNTING=Standoffs") + [
    (C4, "MONUMENT SURFACE", "SURFACE", "select", "Concrete Cap",
     "Concrete Cap|Stone Cap|Brick|Stucco / EIFS|Aluminum Cabinet Top|HDU", "", "Yes", "", "", ""),
    (C4, "MOUNTING PATTERN", "PATTERN", "select", "Yes", "Yes|No", "", "", "", "Full-size paper pattern for pin / stud holes", "No"),

    # ---- illumination (front or halo lit)
    (C5, "LED COLOR", "LED COLOR", "db", "White (6500K)", "LED", LIT, "Yes", "", "", ""),
    (C5, "DIFFUSER VINYL", "DIFFUSER", "select", "No", "No|Yes", HALO, "", "", "", "No"),
    (C5, "POWER SUPPLY", "POWER SUPPLY", "select", "Remote, inside monument", "Remote, inside monument|Per Production", LIT, "", "", "", ""),
    (C5, "PHOTO CELL", "PHOTO CELL", "select", "Yes", "Yes|No", LIT, "", "", "", ""),
]

REGISTRY = ("MONUMENT_LETTERS", "Monument Letters", "Yes", "Yes",
            "3D dimensional letters on a monument or free-standing sign: non-lit, front lit or halo lit; thickness or gauges and depth, colors, top or face mounting.")
ASSEMBLY = ("Monument Signs", 8, "MONUMENT_LETTERS", "Monument Letters", "Optional-Off", "Yes", "")

GUIDE = ("L08", "CHANNEL LETTERS AND HALO LETTERS", "MONUMENT_LETTERS", "",
         "Monument letters: draw them standing on the monument cap in the elevation at real size (qty / size {QTY & SIZES|per spec}), "
         "{LIGHTING|Non-Lit}, {MATERIAL THICKNESS|}{LETTER DEPTH|}{LETTER DEPTH - UNLIT|} thick / deep. "
         "Note the mounting ({MOUNTING|per spec}) and that a full-size pin / stud pattern goes with the letters.",
         "Installers set pins from the pattern; the cap must be wide enough for the letter depth plus pin edge distance.",
         "Show a side view on the proof with the cap, letter thickness and pin embed. Pattern: letters 1:1 on the CUT page with pin holes as 1/4 in. circles.",
         "House")


def drawings(add, rect, line, call, hdim, vdim, concrete, HW, HATCH, INK, LBL):
    """Two side-section details for letters set on top of a monument cap."""
    cap = concrete(6, 64, 88, 28) + line(6, 64, 94, 64, INK, 1.1)
    letter = rect(22, 14, 10, 50)
    cap_label = call(70, 78, 40, 99, "{MONUMENT SURFACE|MONUMENT CAP}")
    add("MNT_TOP_PINNED", "Mounting", "TOP MOUNT - PINNED", "MONUMENT_LETTERS", "MOUNTING=Top Mount - Pinned",
        "Letters stand on the monument cap; threaded pins in the letter bottoms set into drilled, epoxied holes.",
        cap + letter +
        "".join(rect(x - 1.6, 64, 3.2, 15, "#FFFFFF", HATCH, 0.4) + rect(x - 0.8, 58, 1.6, 20, HW, None) for x in (25, 29)) +
        call(27, 34, 40, 34, "LETTER") +
        call(29.8, 72, 40, 52, ["{PIN SIZE|PINS}", "+ EPOXY"], HW, bold=True) +
        cap_label +
        hdim(22, 32, 10, "{MATERIAL THICKNESS|}{LETTER DEPTH|}{LETTER DEPTH - UNLIT|}") +
        vdim(14, 64, 79, ["{PIN EMBED|EMBED}"]))
    add("MNT_TOP_ADHESIVE", "Mounting", "TOP MOUNT - ADHESIVE", "MONUMENT_LETTERS", "MOUNTING=Top Mount - Adhesive",
        "Letters stand on the monument cap, bonded with structural adhesive / silicone along the bottom.",
        cap + letter + rect(20.5, 61.6, 13, 2.4, "#BDBDBD", None, 0, ' rx="1.2"') +
        call(27, 34, 40, 34, "LETTER") +
        call(33, 63, 40, 52, ["STRUCTURAL", "ADHESIVE"], HW, bold=True) +
        cap_label +
        hdim(22, 32, 10, "{MATERIAL THICKNESS|}{LETTER DEPTH|}{LETTER DEPTH - UNLIT|}"))
