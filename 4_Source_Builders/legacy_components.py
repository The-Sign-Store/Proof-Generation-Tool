# The 10 original Product_Schema products, rebuilt as components so they can be
# combined with anything else in a proof package.  Same options as the live tool.
# Field tuple: (zone, variable, label, type, default, options, show_if, required, signos_ref, notes, hide_values)

C1, C2, C3, C4 = "COLUMN 1", "COLUMN 2", "COLUMN 3", "COLUMN 4"
GT = "None|Direct Print|Digital Print Vinyl|Digital Print Contour Cut Vinyl|Contour Cut Vinyl|Paint"
LAMS = "Arlon 3210 Premium Laminate|3M 8518 Wrap Gloss Laminate|3M 8519 Wrap Luster Laminate|3M 8520 Wrap Matte Laminate"
MOUNT = "None|Tape|Stud Mount - Flush|Stud Mount - Spacer|Stand-offs"

def panel(thick_def, thick_opts, side_def, color_opts, lam_def, extra_c3):
    """Shared layout used by ACM, PVC Panel, Coroplast."""
    lam_opts = LAMS if lam_def != "None" else "None|" + LAMS
    return [
        (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", "", ""),
        (C1, "SIZE", "DIMENSIONS", "dims", "", "W|H", "", "Yes", "", "", ""),
        (C1, "THICKNESS", "THICKNESS", "select", thick_def, thick_opts, "", "Yes", "", "", ""),
        (C2, "SIDEDNESS", "SIDEDNESS", "select", side_def, "Single Sided|Double Sided", "", "Yes", "", "", ""),
        (C2, "MATERIAL COLOR", "MATERIAL COLOR", "color", "White", color_opts, "", "Yes", "", "", ""),
        (C2, "GRAPHIC TYPE", "GRAPHIC", "select", "Direct Print", GT, "", "Yes", "", "", ""),
        (C3, "OVERLAMINATE", "OVERLAMINATE", "select", lam_def, lam_opts, "GRAPHIC TYPE~=Print", "Yes", "Master_Mat_Vinyl_Print: VIN_ROL_LAM_*", "", ""),
        (C3, "PRINT COLOR", "COLOR", "fullcolor", "Full Color Digital", "", "GRAPHIC TYPE~=Print", "", "", "", ""),
        (C3, "VINYL COLOR", "COLOR", "vinyl", "751RA", "951|751RA|651|631", "GRAPHIC TYPE=Contour Cut Vinyl", "Yes", "Master_Mat_Vinyl_Cut", "", ""),
        (C3, "PAINT COLOR", "COLOR", "paint", "", "", "GRAPHIC TYPE=Paint", "Yes", "SW_Colors / PMS_Colors", "", ""),
        (C3, "ROUTING", "ROUTING", "select", "No", "No|Yes - Simple|Yes - Complex", "", "Yes", "Master_Services: SRV_CNC_SETUP_SMP / CPL", "", ""),
        (C3, "CORNERS", "CORNERS", "select", "Square", 'Square|Rounded 1/4"|Rounded 1/2"|Rounded 1"', "", "", "", "Rounded corners print a detail drawing", "Square"),
    ] + extra_c3

MOUNT_ROWS = [
    (C3, "MOUNTING", "MOUNTING", "select", "None", MOUNT, "", "", "", "", "None"),
    (C3, "MOUNTING DETAIL", "MOUNT DETAIL", "text", "", "", "MOUNTING~=Spacer|Stand-offs", "Yes", "", 'e.g. 1/2" spacer, brushed standoffs', ""),
]

LEGACY = {}

LEGACY["ACM_PANEL"] = ("ACM", "ACM panel with print, vinyl or paint.",
    [r if r[1] != "SIZE" else (C1, "SIZE", "DIMENSIONS", "dims", "48|96", "W|H", "", "Yes", "", "", "") for r in
     panel("3mm", "3mm|6mm", "Single Sided", "White|Black", "Arlon 3210 Premium Laminate", MOUNT_ROWS)])

LEGACY["PVC_PANEL"] = ("PVC Panel", "PVC panel with print, vinyl or paint.",
    [r if r[1] != "SIZE" else (C1, "SIZE", "DIMENSIONS", "dims", "48|96", "W|H", "", "Yes", "", "", "") for r in
     panel("3mm", '3mm|6mm|1/2"|1"|1.5"|2"', "Single Sided", "White|Black", "None", MOUNT_ROWS)])

LEGACY["CORO_SIGN"] = ("Coroplast", "Coroplast sign with optional step stakes.",
    [r if r[1] != "SIZE" else (C1, "SIZE", "DIMENSIONS", "dims", "24|18", "W|H", "", "Yes", "", "", "") for r in
     panel("4mm", "4mm|10mm", "Double Sided", "White|Custom", "None",
           [(C3, "STEP STAKE", "STEP STAKE", "select", "No", "No|Yes", "", "", "Master_Mat_Hardware: INS_HRD_STK_H / HD", "", "")])])

LEGACY["ACRYLIC_PANEL"] = ("Acrylic", "Acrylic panel; second surface print on clear.", [
    (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", "", ""),
    (C1, "SIZE", "DIMENSIONS", "dims", "48|96", "W|H", "", "Yes", "", "", ""),
    (C1, "THICKNESS", "THICKNESS", "select", '3/16"', '3/16"|1/4"|1/2"|1"|1.5"', "", "Yes", "Master_Mat_Rigid: SUB_ACR_*", "", ""),
    (C2, "MATERIAL COLOR", "MATERIAL COLOR", "color", "Clear", "Clear|White|Black|Red", "", "Yes", "", "", ""),
    (C2, "SIDEDNESS (CLEAR)", "SIDEDNESS", "select", "Single Sided", "Single Sided|Double Sided|Second Surface Print", "MATERIAL COLOR=Clear", "Yes", "", "", ""),
    (C2, "SIDEDNESS", "SIDEDNESS", "select", "Single Sided", "Single Sided|Double Sided", "MATERIAL COLOR!=Clear", "Yes", "", "", ""),
    (C2, "GRAPHIC TYPE", "GRAPHIC", "select", "Direct Print", GT, "", "Yes", "", "", ""),
    (C3, "OVERLAMINATE", "OVERLAMINATE", "select", "None", "None|" + LAMS, "GRAPHIC TYPE~=Print", "Yes", "", "", ""),
    (C3, "PRINT COLOR", "COLOR", "fullcolor", "Full Color Digital", "", "GRAPHIC TYPE~=Print", "", "", "", ""),
    (C3, "VINYL COLOR", "COLOR", "vinyl", "751RA", "951|751RA|651|631", "GRAPHIC TYPE=Contour Cut Vinyl", "Yes", "", "", ""),
    (C3, "PAINT COLOR", "COLOR", "paint", "", "", "GRAPHIC TYPE=Paint", "Yes", "", "", ""),
    (C3, "ROUTING", "ROUTING", "select", "No", "No|Yes - Simple|Yes - Complex|Push-Thru", "", "Yes", "", "", ""),
    (C3, "CORNERS", "CORNERS", "select", "Square", 'Square|Rounded 1/4"|Rounded 1/2"|Rounded 1"', "", "", "", "Rounded corners print a detail drawing", "Square"),
    (C3, "MOUNTING", "MOUNTING", "select", "None", MOUNT + "|Push-Thru", "", "", "PROD_Acrylic_Signs: Retail_Price_Standoff", "", "None"),
    (C3, "MOUNTING DETAIL", "MOUNT DETAIL", "text", "", "", "MOUNTING~=Spacer|Stand-offs", "Yes", "", "", ""),
])

LEGACY["PVC_ROUTED_LETTERS"] = ("PVC - Routed Letters", "Routed PVC dimensional letters.", [
    (C1, "QUANTITY", "QTY", "autoqty", "6", "LETTER HEIGHT", "", "Yes", "", "Counts letters in TEXT", ""),
    (C1, "LETTER HEIGHT", "LETTER HEIGHT", "number", "12", "", "", "Yes", "", "", ""),
    (C1, "THICKNESS", "THICKNESS", "select", '1/2"', '3mm|6mm|1/4"|1/2"|3/4"|1"|1.5"|2"', "", "Yes", "", "", ""),
    (C1, "TEXT", "TEXT", "text", "SAMPLE", "", "", "Yes", "", "", ""),
    (C2, "MATERIAL COLOR", "MATERIAL COLOR", "color", "White", "White|Black", "", "Yes", "", "", ""),
    (C2, "FINISH", "FINISH", "select", "Paint", "Paint|None", "", "Yes", "", "", "None"),
    (C2, "PAINT COLOR", "COLOR", "paint", "", "", "FINISH=Paint", "Yes", "", "", ""),
    (C3, "MOUNTING", "MOUNTING", "select", "Stud Mount - Flush", "None|Tape|Stud Mount - Flush|Stud Mount - Spacer|Custom", "", "", "", "", "None"),
    (C3, "MOUNTING DETAIL", "MOUNT DETAIL", "text", "", "", "MOUNTING~=Spacer|Custom", "Yes", "", "", ""),
])

LEGACY["CUT_VINYL_DECAL"] = ("Cut Vinyl Decal", "Oracal cut vinyl with weeding and masking.", [
    (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", "", ""),
    (C1, "SIZE", "DIMENSIONS", "dims", "12|12", "W|H", "", "Yes", "", "", ""),
    (C2, "VINYL COLOR", "VINYL", "vinyl", "751RA", "751RA|951|8800|8500|8810|8510|7510|6510|651|631", "", "Yes", "Master_Mat_Vinyl_Cut", "", ""),
    (C3, "WEEDING", "WEEDING", "select", "Easy", "No|Easy|Complex", "", "Yes", "", "", ""),
    (C3, "MASK", "MASK", "select", "Yes", "No|Yes", "", "Yes", "", "", ""),
])

PRINT_MEDIA = ("Arlon 4500GLX Print Vinyl|GF226 Smooth Wall Vinyl|3M IJ8624 Textured Wall Vinyl|3M IJ180 Wrap Vinyl|"
               "Oralite 5400 Commercial Grade Reflective Vinyl|Oracal 3640 Gloss Clear Vinyl|Brightline Window Perf 60/40|Brightline Window Perf 70/30")
LEGACY["DIGITAL_PRINT_VINYL"] = ("Digital Print Vinyl", "Printed vinyl; laminate choices follow the media.", [
    (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", "", ""),
    (C1, "SIZE", "DIMENSIONS", "dims", "24|24", "W|H", "", "Yes", "", "", ""),
    (C2, "MEDIA", "MEDIA", "select", "Arlon 4500GLX Print Vinyl", PRINT_MEDIA, "", "Yes", "Master_Mat_Vinyl_Print", "", ""),
    (C2, "LAMINATE (ARLON)", "OVERLAMINATE", "select", "Arlon 3210 Premium Laminate", "Arlon 3210 Premium Laminate",
     "MEDIA=Arlon 4500GLX Print Vinyl|GF226 Smooth Wall Vinyl", "Yes", "", "", ""),
    (C2, "LAMINATE (TEXTURED)", "OVERLAMINATE", "select", "3M 8524 Textured Luster Wall Laminate", "3M 8524 Textured Luster Wall Laminate",
     "MEDIA=3M IJ8624 Textured Wall Vinyl", "Yes", "", "", ""),
    (C2, "LAMINATE (WRAP)", "OVERLAMINATE", "select", "3M 8518 Wrap Gloss Laminate",
     "3M 8518 Wrap Gloss Laminate|3M 8519 Wrap Luster Laminate|3M 8520 Wrap Matte Laminate", "MEDIA=3M IJ180 Wrap Vinyl", "Yes", "", "", ""),
    (C2, "LAMINATE (REFLECTIVE)", "OVERLAMINATE", "select", "Arlon 3210 Premium Laminate", LAMS,
     "MEDIA=Oralite 5400 Commercial Grade Reflective Vinyl", "Yes", "", "", ""),
    (C2, "LAMINATE (CLEAR)", "OVERLAMINATE", "select", "None", "None|Arlon 3210 Premium Laminate", "MEDIA=Oracal 3640 Gloss Clear Vinyl", "Yes", "", "", ""),
    (C2, "LAMINATE (PERF)", "OVERLAMINATE", "select", "None", "None", "MEDIA~=Perf", "Yes", "", "", ""),
    (C3, "CONTOUR CUT", "CONTOUR CUT", "select", "No", "No|Yes", "", "Yes", "Master_Services: SRV_FIN_CONTOUR", "", ""),
    (C3, "WEEDING", "WEEDING", "select", "No", "No|Easy|Complex", "CONTOUR CUT=Yes", "Yes", "", "", ""),
    (C3, "MASK", "MASK", "select", "No", "No|Yes", "CONTOUR CUT=Yes", "Yes", "", "", ""),
])

LEGACY["BANNER"] = ("Banner", "Vinyl banner with hems, grommets and pole pockets.", [
    (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", "", ""),
    (C1, "SIZE", "DIMENSIONS", "dims", "48|24", "W|H", "", "Yes", "PROD_Vinyl_Banners: Printer_Max_Roll_Width 64\"", "", ""),
    (C2, "MEDIA", "MEDIA", "select", "13oz Standard", "13oz Standard|8oz Mesh|18oz", "", "Yes", "Master_Mat_Vinyl_Print: VIN_ROL_BAN_*", "", ""),
    (C2, "SIDEDNESS (18OZ)", "SIDEDNESS", "select", "Single Sided", "Single Sided|Double Sided", "MEDIA=18oz", "Yes", "", "", ""),
    (C2, "SIDEDNESS", "SIDEDNESS", "select", "Single Sided", "Single Sided", "MEDIA!=18oz", "Yes", "", "13oz and mesh are single sided only", ""),
    (C3, "GROMMETS", "GROMMETS", "select", "Yes", "Yes|No", "", "Yes", "Master_Mat_Hardware: VIN_SUP_GRM_NI", "", ""),
    (C3, "GROMMET SPACING", "GROMMET SPACING", "select", 'Corners & Every 18"~24"', 'Corners & Every 18"~24"|Corners Only', "GROMMETS=Yes", "Yes", "", "", ""),
    (C3, "GROMMET COLOR", "GROMMET COLOR", "color", "Nickel", "Nickel|Brass|Black", "GROMMETS=Yes", "Yes", "", "", ""),
    (C4, "HEMS", "HEMS", "select", "All 4 Sides", "All 4 Sides|None", "", "Yes", "Master_Mat_Hardware: VIN_SUP_HEM_TPE", "", ""),
    (C4, "POLE POCKETS", "POLE POCKETS", "select", "No", "No|Yes", "", "Yes", "", "", ""),
    (C4, "POCKET LOCATIONS", "POCKET LOCATIONS", "select", "Top and Bottom",
     "Top Only|Bottom Only|Left Only|Right Only|Top and Bottom|Left and Right|All 4 Sides", "POLE POCKETS=Yes", "Yes", "", "", ""),
])

LEGACY["CHANNEL_LETTERS_FL"] = ("Channel Letters - Front Lit", "Front lit channel letters, one line of copy per block.", [
    (C1, "QUANTITY", "QTY", "autoqty", "1", "LETTER HEIGHT", "", "Yes", "", "Counts letters in TEXT", ""),
    (C1, "LETTER HEIGHT", "LETTER HEIGHT", "number", "18", "", "", "Yes", "", "", ""),
    (C1, "TEXT", "TEXT", "text", "", "", "", "Yes", "", "", ""),
    (C2, "FACE MATERIAL", "FACE", "select", '3/16" Acrylic', '3/16" Acrylic|3/16" Polycarbonate', "", "Yes", "", "", ""),
    (C2, "FACE COLOR", "FACE COLOR", "color", "White", "Clear|White|Red", "", "Yes", "", "", ""),
    (C2, "FACE VINYL", "VINYL", "select", "None", "None|Translucent Vinyl|Translucent Digital Print", "", "Yes", "", "", "None"),
    (C2, "VINYL COLOR", "VINYL COLOR", "vinyl", "8500", "8500|8800", "FACE VINYL=Translucent Vinyl", "Yes", "Master_Mat_Vinyl_Cut: VIN_ROL_TRN_8500 / 8800", "", ""),
    (C3, "RETURN", "RETURN", "select", '5" .040', '5" .040|3" .040', "", "Yes", "Master_Mat_Fab_Channel: CLD-COM-COIL-5 / -3", "", ""),
    (C3, "RETURN COLOR", "RETURN COLOR", "db", "Gloss Black", "COIL", "", "Yes", "Coil_Colors", "", ""),
    (C3, "TRIM CAP", "TRIM CAP", "select", '1"', '1"|2"', "", "Yes", "Master_Mat_Fab_Channel: CLD-COM-TRIM-1", "", ""),
    (C3, "TRIM CAP COLOR", "TRIM CAP COLOR", "db", '1 Black"', "TRIMCAP", "", "Yes", "TrimCap_Colors", "", ""),
    (C4, "LED COLOR", "LED COLOR", "db", "White (6500K)", "LED", "", "Yes", "Master_Mat_Fab_Channel: CLD-SUP-LED-WHT", "", ""),
    (C4, "MOUNTING", "MOUNTING", "select", "Flush Mount", "Flush Mount|Raceway|Panel", "", "Yes", "", "", ""),
    (C4, "MOUNTING PAINT", "MOUNTING COLOR", "paint", "", "", "MOUNTING=Raceway|Panel", "Yes", "", "", ""),
])

LEGACY["HDU_SIGN"] = ("HDU Sign", "Routed / sandblasted HDU sign, painted.", [
    (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", "", ""),
    (C1, "SIZE", "DIMENSIONS", "dims", "48|48", "W|H", "", "Yes", "", "", ""),
    (C1, "THICKNESS", "THICKNESS", "select", '1.5"', '1"|1.5"|2"', "", "Yes", "Master_Mat_Rigid: SUB_HDU_*", "", ""),
    (C2, "SIDEDNESS", "SIDEDNESS", "select", "Single Sided", "Single Sided|Double Sided", "", "Yes", "", "", ""),
    (C2, "BACKGROUND PAINT", "BACKGROUND", "paint", "", "", "", "Yes", "", "", ""),
    (C2, "FOREGROUND PAINT", "FOREGROUND", "paint", "", "", "", "Yes", "", "", ""),
    (C2, "ACCENT PAINT 1", "ACCENT", "paint", "", "", "", "", "", "Optional", ""),
    (C2, "ACCENT PAINT 2", "ACCENT", "paint", "", "", "", "", "", "Optional", ""),
    (C3, "ROUTING", "ROUTING", "select", "Shape Only", "Shape Only|Standard Wash Out|Textured", "", "Yes", "", "", ""),
    (C3, "TEXTURE", "TEXTURE", "text", "", "", "ROUTING=Textured", "Yes", "", "e.g. wood grain, pebble", ""),
    (C3, "MOUNTING", "MOUNTING", "select", "Stud Mount - Flush",
     "None|Stud Mount - Flush|Stud Mount - Spacer|Stand-offs|Hanging Bracket - Swinging|Hanging Bracket - Fixed|Blade Bracket|Custom", "", "", "", "", "None"),
    (C3, "MOUNTING DETAIL", "MOUNT DETAIL", "text", "", "", "MOUNTING~=Bracket|Spacer|Stand-offs|Custom", "Yes", "", "", ""),
    (C3, "BRACKET PAINT", "BRACKET COLOR", "paint", "", "", "MOUNTING~=Bracket", "Yes", "", "", ""),
])

# Single-component assemblies so each appears under "Products" with its original name
LEGACY_ASSEMBLIES = [(name, 1, cid, name, "Required", "Yes", "", 1) for cid, (name, _d, _f) in LEGACY.items()]

EXTRA_FINISH = [("Clear", "transparent"), ("Red", "#C1272D"), ("Nickel", "#A8A9AD"), ("Brass", "#C5A059"), ("Custom", "")]
