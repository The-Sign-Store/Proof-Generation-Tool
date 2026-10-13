"""v2.1: Monument Letters - permanent 3D dimensional letters on a low-profile, ground-fixed monument or
free-standing sign. Usually set on TOP of the monument (letters stand on their bottoms, pinned or bonded);
face mounting with studs is also offered.

  MONUMENT_LETTERS: own component (blue Letters family) and an optional section of Monument Signs.
  Flat cut / cast / HDU letters list their plate THICKNESS; fabricated (reverse channel) letters list
  FACE and RETURN GAUGE (.040, .063 ...) and their DEPTH.
"""
from legacy_components import standoff_rows
C1, C2, C3, C4, C5 = "COLUMN 1", "COLUMN 2", "COLUMN 3", "COLUMN 4", "COLUMN 5"
FAB = "Fabricated Aluminum (Reverse Channel)"
FLAT_TYPES = "Flat Cut Aluminum|Cast Aluminum|Flat Cut Stainless Steel|Flat Cut Brass|Flat Cut Acrylic|Flat Cut PVC|HDU (Routed)"
NOT_FAB = f"LETTER TYPE!={FAB}"
IS_FAB = f"LETTER TYPE={FAB}"

# (zone, variable, label, type, default, options, show_if, required, signos_ref, notes, hide_values)
FIELDS = [
    (C1, "QUANTITY", "QTY", "autoqty", "1", "LETTER HEIGHT", "", "Yes", "", "Counted from TEXT", ""),
    (C1, "LETTER HEIGHT", "LETTER HEIGHT", "number", "12", '"', "", "Yes", "", "Cap height, inches", ""),
    (C1, "TEXT", "TEXT", "text", "", "", "", "Yes", "", "", ""),
    (C1, "FONT", "FONT", "text", "", "", "", "", "", "Typeface name", ""),

    (C2, "LETTER TYPE", "TYPE", "select", "Flat Cut Aluminum", FLAT_TYPES.split("|")[0] + "|" + FAB + "|" + "|".join(FLAT_TYPES.split("|")[1:]),
     "", "Yes", "", "", ""),
    (C2, "MATERIAL THICKNESS", "THICKNESS", "select", '1/2"', '1/8"|3/16"|1/4"|3/8"|1/2"|3/4"|1"|1-1/2"|2"', NOT_FAB, "Yes", "",
     "Plate thickness of flat cut, cast or routed letters", ""),
    (C2, "FACE GAUGE", "FACE", "select", ".063", ".040|.050|.063|.080|.090|.125", IS_FAB, "Yes", "", "Aluminum sheet thickness of the letter face", ""),
    (C2, "RETURN GAUGE", "RETURN", "select", ".040", ".040|.050|.063", IS_FAB, "Yes", "", "Aluminum thickness of the letter sides", ""),
    (C2, "LETTER DEPTH", "DEPTH", "select", '3"', '1-1/2"|2"|3"|4"|5"|6"', IS_FAB, "Yes", "", "Overall depth of fabricated letters", ""),

    (C3, "FINISH", "FINISH", "select", "Painted", "Painted|Brushed|Polished|Anodized|Natural / Mill", "", "Yes", "", "", ""),
    (C3, "LETTER COLOR", "COLOR", "paint", "", "", "FINISH=Painted", "Yes", "", "", ""),
    (C3, "RETURN COLOR", "RETURN COLOR", "finish", "Match Face", "Match Face|Black|Bronze|White", f"{IS_FAB}&FINISH=Painted", "", "", "", ""),

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

    (C5, "LIGHTING", "LIGHTING", "select", "Non-Lit", "Non-Lit|Halo Lit|Ground Lit (by others)", "", "Yes", "",
     "Halo lit = fabricated reverse channel letters", ""),
    (C5, "LED COLOR", "LED COLOR", "db", "White (6500K)", "LED", "LIGHTING=Halo Lit", "Yes", "", "", ""),
    (C5, "POWER SUPPLY", "POWER SUPPLY", "select", "Remote, inside monument", "Remote, inside monument|Per Production", "LIGHTING=Halo Lit", "", "", "", ""),
    (C5, "PHOTO CELL", "PHOTO CELL", "select", "Yes", "Yes|No", "LIGHTING=Halo Lit", "", "", "", ""),
]

REGISTRY = ("MONUMENT_LETTERS", "Monument Letters", "Yes", "Yes",
            "3D dimensional letters on a monument or free-standing sign: letter type, thickness or gauge and depth, finish, top or face mounting, lighting.")
ASSEMBLY = ("Monument Signs", 8, "MONUMENT_LETTERS", "Monument Letters", "Optional-Off", "Yes", "")

GUIDE = ("L08", "CHANNEL LETTERS AND HALO LETTERS", "MONUMENT_LETTERS", "",
         "Monument letters: draw them standing on the monument cap in the elevation at real size (cap height {LETTER HEIGHT|per spec}), "
         "{MATERIAL THICKNESS|per spec} thick for flat cut letters or {LETTER DEPTH|per spec} deep for fabricated letters. "
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
        hdim(22, 32, 10, "{MATERIAL THICKNESS|THICKNESS}") +
        vdim(14, 64, 79, ["{PIN EMBED|EMBED}"]))
    add("MNT_TOP_ADHESIVE", "Mounting", "TOP MOUNT - ADHESIVE", "MONUMENT_LETTERS", "MOUNTING=Top Mount - Adhesive",
        "Letters stand on the monument cap, bonded with structural adhesive / silicone along the bottom.",
        cap + letter + rect(20.5, 61.6, 13, 2.4, "#BDBDBD", None, 0, ' rx="1.2"') +
        call(27, 34, 40, 34, "LETTER") +
        call(33, 63, 40, 52, ["STRUCTURAL", "ADHESIVE"], HW, bold=True) +
        cap_label +
        hdim(22, 32, 10, "{MATERIAL THICKNESS|THICKNESS}"))
