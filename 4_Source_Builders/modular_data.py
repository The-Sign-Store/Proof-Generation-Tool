# Modular component + assembly definitions for the Sign Proof Generator.
# Options use "|" as separator (allows commas and inch marks inside values).
#
# Field tuple: (zone, variable, label, type, default, options, show_if, required, signos_ref, notes)
# Types:
#   text      free text                 number   numeric input
#   select    dropdown (+ Custom Input)  dims     W/H/D boxes; options = sub-labels, default = values
#   paint     SW / PMS / Custom swatch   finish   standard finishes (options) + "Custom Paint" -> SW/PMS
#   vinyl     Oracal series + swatch; options = allowed series
#   db        swatch from a color tab; options = LED | COIL | TRIMCAP | ACM | ACRYLIC | PVC | CORO
#   rowmark   Rowmark swatch; options = series filter
#   pictogram ADA pictogram picker
#   autoqty   letter count from TEXT; options = name of the letter-height variable
# Show_If: VAR=a|b   VAR!=a|b   VAR~=text (contains)   join several with  &

C1, C2, C3, C4 = "COLUMN 1", "COLUMN 2", "COLUMN 3", "COLUMN 4"
YN, NY = "Yes|No", "No|Yes"

STEEL_POLES = ('3" Square, 1/8" Wall|3" Square, 3/16" Wall|4" Square, 1/8" Wall|4" Square, 3/16" Wall|'
               '6" Square, 3/16" Wall|6" Square, 1/4" Wall|8" Square, 3/16" Wall|8" Square, 1/4" Wall|'
               '10" Square, 1/4" Wall|12" Square, 1/4" Wall')
ALUM_POLES = '2" Square, 1/8" Wall|3" Square, 1/8" Wall|4" Square, 1/8" Wall|6" Square, 1/8" Wall|6" Square, 1/4" Wall'
WOOD_POSTS = '4" x 4" Treated|4" x 4" Treated, Painted'
LAMS = "Arlon 3210 Premium Laminate|3M 8518 Wrap Gloss Laminate|3M 8519 Wrap Luster Laminate|3M 8520 Wrap Matte Laminate"
PRINT_MEDIA = "Arlon 4500GLX Print Vinyl|3M IJ180 Wrap Vinyl|Oralite 5400 Commercial Grade Reflective Vinyl"

# id, display name, show as tool, repeatable default, description
REGISTRY = [
 ("POLE", "Pole", "Yes", "No", "Steel, aluminum or wood poles/posts with footer and finish."),
 ("POLE_COVER", "Pole Cover", "Yes", "No", "Aluminum pole cover / pylon skirt with optional address graphics."),
 ("CABINET", "Cabinet", "Yes", "No", "Lighted sign cabinet: size, construction, finish, retainers, mounting."),
 ("POLY_FACE", "Polycarbonate Face", "Yes", "No", "Cabinet face (polycarbonate, acrylic, pan or flex) and its graphics."),
 ("ILLUMINATION", "Illumination", "No", "No", "LEDs, power, controls, disconnect and ETL."),
 ("EMC", "Digital Sign (EMC)", "Yes", "No", "Electronic message center by vendor."),
 ("MONUMENT_BASE", "Monument Base", "Yes", "No", "Monument base/columns, reveal, cap and install plan."),
 ("ROUTED_FACE", "Routed Aluminum Face", "Yes", "No", "Routed aluminum face with push-thru or backed copy."),
 ("SIGN_PANEL", "Sign Panel", "Yes", "No", "Flat panel (ACM, aluminum, PVC, HDU) with graphics."),
 ("PANEL_FRAME", "Panel Frame", "Yes", "No", "Frame for post & panel and directional signs."),
 ("HALO_LETTERS", "Halo Letters", "No", "Yes", "Reverse / halo lit channel letters (one line of copy per block)."),
 ("BACKER_PANEL", "Backer Panel", "Yes", "No", "Panel behind letters (flat, framed or routed shape)."),
 ("ADA_SIGN", "ADA Sign", "No", "Yes", "Tactile / Braille ADA sign (one message per block)."),
]

F = {}

F["POLE"] = [
 (C1, "QUANTITY", "QTY", "number", "2", "", "", "Yes", "", ""),
 (C1, "POLE MATERIAL", "MATERIAL", "select", "Steel", "Steel|Aluminum|Wood", "", "Yes", "", ""),
 (C1, "STEEL POLE SIZE", "POLE SIZE", "select", '4" Square, 3/16" Wall', STEEL_POLES, "POLE MATERIAL=Steel", "Yes",
  "Master_Mat_Metals: Cost_Post_Steel_* / STL_POLE_*", "Final size per engineering"),
 (C1, "ALUMINUM POLE SIZE", "POLE SIZE", "select", '3" Square, 1/8" Wall', ALUM_POLES, "POLE MATERIAL=Aluminum", "Yes",
  "Master_Mat_Metals: Cost_Post_Aluminum_* / ALM_TUBE_*", ""),
 (C1, "WOOD POST SIZE", "POST SIZE", "select", '4" x 4" Treated', WOOD_POSTS, "POLE MATERIAL=Wood", "Yes",
  "Master_Mat_Hardware: 4x4x*_Nat / 4x4x*_Pnt / LBR_WOOD_4X4_8", ""),
 (C2, "OVERALL LENGTH", "LENGTH", "select", "10'", "8'|10'|12'|14'|16'|20'|24'|Per Engineering", "", "Yes",
  "Wood stock: 8' / 10' / 12' / 16'", "Above grade + embed"),
 (C2, "EMBED DEPTH", "EMBED", "select", '36"', '24"|30"|36"|48"|60"|Per Engineering', "", "Yes", "", ""),
 (C2, "FOOTER", "FOOTER", "select", "Concrete (80 lb Bags)",
  "Concrete (80 lb Bags)|Engineered Concrete Footer|Direct Burial|Surface Mount Base Plate", "", "Yes",
  "Master_Mat_Hardware: FAB_SUP_CON_BAG", ""),
 (C3, "POLE FINISH", "FINISH", "finish", "Black", "Black|Bronze|White|Mill / Unpainted|Natural Wood", "", "Yes", "", ""),
 (C3, "POLE CAP", "POLE CAP", "select", "Yes", YN, "POLE MATERIAL!=Wood", "", "Master_Mat_Hardware: HRD_CAP_ALUM_3", ""),
]

F["POLE_COVER"] = [
 (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", ""),
 (C1, "COVER SIZE", "DIMENSIONS", "dims", "24|18|102", "W|D|H", "", "Yes", "", "W x D x H"),
 (C2, "COVER MATERIAL", "MATERIAL", "select", '.040 Aluminum over 1.5" Angle Frame',
  '.040 Aluminum over 1.5" Angle Frame|.063 Aluminum over 1.5" Angle Frame|Brick / Stone by Others|Stucco by Others',
  "", "Yes", "Master_Mat_Metals: ALM_SHT_040 / ALM_SHT_063, Cost_Frame_AlumAngle_1.5_1/8", ""),
 (C2, "COVER FINISH", "FINISH", "finish", "Match Cabinet", "Match Cabinet|Black|Bronze|White", "", "Yes", "", ""),
 (C3, "COVER GRAPHICS", "GRAPHICS", "select", "None", "None|Cut Vinyl Address|Cut Vinyl Logo / Text|Digital Print Vinyl", "", "", "", ""),
 (C3, "ADDRESS TEXT", "ADDRESS", "text", "", "", "COVER GRAPHICS=Cut Vinyl Address", "Yes", "", ""),
 (C3, "COVER VINYL", "VINYL", "vinyl", "751RA", "751RA|951|651", "COVER GRAPHICS~=Cut Vinyl", "Yes", "Master_Mat_Vinyl_Cut", ""),
]

F["CABINET"] = [
 (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", ""),
 (C1, "CABINET SIZE", "DIMENSIONS", "dims", "96|36|8", "W|H|D", "", "Yes", "", "Overall cabinet O.D."),
 (C1, "SIDEDNESS", "SIDEDNESS", "select", "Single Sided", "Single Sided|Double Sided", "", "Yes", "", ""),
 (C2, "CONSTRUCTION", "CONSTRUCTION", "select", "Extrusion", "Extrusion|Stick Built (Angle Frame)|Fabricated Aluminum", "", "Yes", "", ""),
 (C2, "SKIN", "SKIN", "select", ".040 Aluminum", ".040 Aluminum|.063 Aluminum", "CONSTRUCTION!=Extrusion", "Yes",
  "Master_Mat_Metals: ALM_SHT_040 / ALM_SHT_063", ""),
 (C2, "CABINET FINISH", "CABINET COLOR", "finish", "Black", "Black|Bronze|White", "", "Yes", "", ""),
 (C3, "RETAINER SIZE", "RETAINER", "select", '1.5"', '1.5"|2"', "", "Yes", "Fold-out: Retainer Size", 'Flange = retainer + 1"'),
 (C3, "RETAINER TYPE", "RETAINER TYPE", "select", "Standard (Flat)", "Standard (Flat)|Formed", "", "Yes", "", ""),
 (C3, "RETAINER FINISH", "RETAINER COLOR", "finish", "Match Cabinet", "Match Cabinet|Black|Bronze|White", "", "Yes", "", ""),
 (C4, "MOUNTING", "MOUNTING", "select", "Wall Mount", "Wall Mount|Pole Mount|Monument Base|Pole Cover / Pylon", "", "Yes", "", ""),
 (C4, "WALL MOUNT DETAIL", "MOUNT DETAIL", "text", "Lag to wall, pattern by installer", "", "MOUNTING=Wall Mount", "", "", ""),
]

F["POLY_FACE"] = [
 (C1, "FACE QTY", "FACES", "number", "1", "", "", "Yes", "", "1 = single sided, 2 = double sided"),
 (C1, "FACE MATERIAL", "FACE", "select", '3/16" White Polycarbonate',
  '3/16" White Polycarbonate|1/4" White Polycarbonate|3/16" Clear Polycarbonate|3/16" White Acrylic|Pan Face - Flat|Pan Face - Embossed|Flex Face',
  "", "Yes", "INV_Sheets: SHT_POL_316_52X120 (52\" x 120\" max)", "Use Pan Face Worksheet for pan faces"),
 (C1, "FACE SIZE", "FACE SIZE", "dims", "", "W|H", "", "", "", 'Cabinet minus 0.25" (pan face)'),
 (C2, "GRAPHIC TYPE", "GRAPHIC", "select", "Translucent Cut Vinyl",
  "Translucent Cut Vinyl|Translucent Digital Print|2nd Surface Direct Print|None", "", "Yes", "", ""),
 (C2, "FACE VINYL", "VINYL", "vinyl", "8500", "8500|8800", "GRAPHIC TYPE=Translucent Cut Vinyl", "Yes", "Master_Mat_Vinyl_Cut: VIN_ROL_TRN_8500 / 8800", ""),
 (C2, "PRINT MEDIA", "MEDIA", "select", "Oracal 3850 Translucent", "Oracal 3850 Translucent", "GRAPHIC TYPE=Translucent Digital Print", "Yes",
  "Master_Mat_Vinyl_Print: VIN_ROL_PRT_3850", ""),
 (C2, "PRINT LAYERS", "PRINT", "select", "Color + White", "Color + White|3-Layer (Day / Night)|5-Layer Blockout",
  "GRAPHIC TYPE=2nd Surface Direct Print", "Yes", "PROD_Acrylic_Signs: Speed_Print_White / 3Layer / 5Layer", "HP R1000"),
 (C3, "ADDITIONAL COLORS", "ALSO", "text", "", "", "GRAPHIC TYPE=Translucent Cut Vinyl", "", "", "e.g. 8500-031 Red (logo)"),
]

F["ILLUMINATION"] = [
 (C1, "LIGHT SOURCE", "ILLUMINATION", "select", "LED Modules", "LED Modules|LED Strip|Non-Illuminated", "", "Yes",
  "Master_Mat_Fab_Channel: CLD-SUP-LED-WHT", ""),
 (C1, "LED COLOR", "LED COLOR", "db", "White (6500K)", "LED", "LIGHT SOURCE!=Non-Illuminated", "Yes", "LED_Colors tab", ""),
 (C2, "POWER SUPPLY", "POWER SUPPLY", "select", "Per Production", "Per Production|60W|120W",
  "LIGHT SOURCE!=Non-Illuminated", "", "Master_Mat_Fab_Channel: CLD-SUP-PSU-60 / CLD-SUP-PSU-120", ""),
 (C2, "PHOTO CELL", "PHOTO CELL", "select", "Yes", YN, "LIGHT SOURCE!=Non-Illuminated", "Yes", "", ""),
 (C2, "TIMER", "TIMER", "select", "No", NY, "LIGHT SOURCE!=Non-Illuminated", "", "", ""),
 (C3, "DISCONNECT SWITCH", "DISCONNECT", "select", "Yes", YN, "LIGHT SOURCE!=Non-Illuminated", "Yes", "NEC 600", "Required on lit signs"),
 (C3, "ETL LABEL", "ETL / UL", "select", "Yes", YN, "LIGHT SOURCE!=Non-Illuminated", "Yes", "UL 48", "Required on lit signs"),
 (C3, "PRIMARY ELECTRICAL", "ELECTRICAL", "select", "120V by Customer's Electrician",
  "120V by Customer's Electrician|277V by Customer's Electrician|Existing Circuit at Sign", "LIGHT SOURCE!=Non-Illuminated", "Yes", "", ""),
]

F["EMC"] = [
 (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", ""),
 (C1, "EMC SIZE", "DIMENSIONS", "dims", "94.5|47.25", "W|H", "", "Yes", "", "Per vendor spec"),
 (C1, "SIDEDNESS", "SIDEDNESS", "select", "Single Sided", "Single Sided|Double Sided", "", "Yes", "", ""),
 (C2, "PIXEL PITCH", "PITCH", "select", "10mm", "10mm|16mm|20mm", "", "Yes", "", ""),
 (C2, "COLOR TYPE", "DISPLAY", "select", "Full Color", "Full Color|Monochrome Amber|Monochrome Red", "", "Yes", "", ""),
 (C3, "VENT FINISH", "VENTS", "finish", "Black", "Black|Bronze|Match Cabinet", "", "", "", ""),
 (C3, "VENDOR", "VENDOR", "text", "Farm Out", "", "", "", "", ""),
]

F["MONUMENT_BASE"] = [
 (C1, "BASE SIZE", "BASE SIZE", "dims", "132|24|16", "W|H|D", "", "Yes", "", ""),
 (C1, "BASE MATERIAL", "MATERIAL", "select", "Fabricated Aluminum",
  "Fabricated Aluminum|Foam w/ Stucco Coating|Brick by Others|Stone by Others|Stucco by Others", "", "Yes",
  "Master_Mat_Metals: ALM_SHT_*, Cost_Frame_AlumAngle_*", ""),
 (C2, "BASE FINISH", "BASE COLOR", "finish", "Black", "Black|Bronze|White|Brushed Aluminum|By Others",
  "", "Yes", "", ""),
 (C2, "REVEAL", "REVEAL", "select", '2" Reveal', 'None|2" Reveal|3" Reveal', "", "", "", ""),
 (C2, "REVEAL FINISH", "REVEAL COLOR", "finish", "Black", "Black|Bronze|White|Brushed Aluminum", "REVEAL!=None", "Yes", "", ""),
 (C3, "CAP / TOPPER", "CAP", "select", "Aluminum Cap", "None|Aluminum Cap|Stucco Cap", "", "", "", ""),
 (C3, "CAP FINISH", "CAP COLOR", "finish", "Match Cabinet", "Match Cabinet|Black|Bronze|White", "CAP / TOPPER!=None", "Yes", "", ""),
 (C4, "INSTALL PLAN", "INSTALL", "select", "Set Poles, Return Trip to Set Cabinet",
  "Set Poles, Return Trip to Set Cabinet|Customer Builds Base, We Install Cabinet|Complete Install in One Trip", "", "Yes", "", ""),
]

F["ROUTED_FACE"] = [
 (C1, "FACE QTY", "FACES", "number", "2", "", "", "Yes", "", ""),
 (C1, "FACE GAUGE", "FACE", "select", ".080 Aluminum", ".080 Aluminum|.063 Aluminum|.125 Aluminum", "", "Yes",
  "Master_Mat_Metals: ALM_SHT_080 / ALM_SHT_063", ""),
 (C1, "FACE PAINT", "FACE COLOR", "paint", "", "", "", "Yes", "SW_Colors / PMS_Colors", ""),
 (C2, "COPY TYPE", "COPY", "select", "Push-Thru Acrylic", "Push-Thru Acrylic|Routed w/ Acrylic Backer|Routed - Open (Non-Lit)", "", "Yes", "", ""),
 (C2, "PUSH-THRU", "PUSH-THRU", "select", '1/2" Clear Acrylic', '1/2" Clear Acrylic|3/4" Clear Acrylic|1/2" White Acrylic|3/4" White Acrylic',
  "COPY TYPE=Push-Thru Acrylic", "Yes", "Master_Mat_Rigid: SUB_ACR_12C_4X8 / SUB_ACR_34C_4X8", ""),
 (C2, "BACKER", "BACKER", "select", '3/16" White Polycarbonate', '3/16" White Polycarbonate|3/16" White Acrylic',
  "COPY TYPE=Routed w/ Acrylic Backer", "Yes", "INV_Sheets: SHT_POL_316_52X120", ""),
 (C3, "DIFFUSER", "DIFFUSER", "select", "White Diffuser Vinyl", "White Diffuser Vinyl|None", "COPY TYPE!=Routed - Open (Non-Lit)", "", "", ""),
 (C3, "COPY VINYL", "COPY COLOR", "vinyl", "8500", "8500|8800", "COPY TYPE!=Routed - Open (Non-Lit)", "", "Master_Mat_Vinyl_Cut", "Leave blank for white copy"),
]

F["SIGN_PANEL"] = [
 (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", ""),
 (C1, "PANEL SIZE", "DIMENSIONS", "dims", "48|36", "W|H", "", "Yes", "INV_Sheets (ACM max 60\" x 120\")", ""),
 (C1, "SIDEDNESS", "SIDEDNESS", "select", "Double Sided", "Single Sided|Double Sided", "", "Yes", "", ""),
 (C2, "PANEL MATERIAL", "MATERIAL", "select", "3mm ACM",
  '3mm ACM|6mm ACM|3mm Brushed ACM|.080 Aluminum|.063 Aluminum|6mm PVC|1.5" HDU', "", "Yes",
  "INV_Sheets: SHT_ACM_* / SHT_ALM_* / SHT_PVC_* / SHT_HDU_*", ""),
 (C2, "PANEL FINISH", "MATERIAL COLOR", "finish", "White", "White|Black|Brushed Aluminum", "", "Yes", "ACM_Colors", ""),
 (C2, "CUSTOM SHAPE", "SHAPE", "select", "No (Square Cut)", "No (Square Cut)|Yes - Simple Route|Yes - Complex Route", "", "",
  "Master_Services: SRV_CNC_SETUP_SMP / SRV_CNC_SETUP_CPL", ""),
 (C2, "CORNERS", "CORNERS", "select", "Square", 'Square|Rounded 1/4"|Rounded 1/2"|Rounded 1"', "", "", "", "Rounded corners print a detail drawing", "Square"),
 (C3, "GRAPHIC TYPE", "GRAPHIC", "select", "Digital Print Vinyl", "Digital Print Vinyl|Direct Print|Cut Vinyl|Paint|None", "", "Yes", "", ""),
 (C3, "MEDIA", "MEDIA", "select", "Arlon 4500GLX Print Vinyl", PRINT_MEDIA, "GRAPHIC TYPE=Digital Print Vinyl", "Yes",
  "Master_Mat_Vinyl_Print: VIN_ROL_PRT_4500 / IJ180 / 5400", ""),
 (C3, "OVERLAMINATE", "LAMINATE", "select", "Arlon 3210 Premium Laminate", LAMS, "GRAPHIC TYPE=Digital Print Vinyl", "Yes",
  "Master_Mat_Vinyl_Print: VIN_ROL_LAM_3210 / 8518 / 8519 / 8520", ""),
 (C3, "CUT VINYL", "VINYL", "vinyl", "751RA", "751RA|951|651", "GRAPHIC TYPE=Cut Vinyl", "Yes", "Master_Mat_Vinyl_Cut", ""),
 (C3, "GRAPHIC PAINT", "PAINT", "paint", "", "", "GRAPHIC TYPE=Paint", "Yes", "", ""),
]

F["PANEL_FRAME"] = [
 (C1, "FRAME POSITION", "FRAME", "select", "Interior (Between Posts)",
  "Interior (Between Posts)|Behind Panel|Perimeter Cabinet Frame", "", "Yes", "", ""),
 (C1, "FRAME MATERIAL", "FRAME MATERIAL", "select", '2" Aluminum Angle',
  '1.5" Aluminum Angle|2" Aluminum Angle|2" Aluminum Square Tube|2" Steel Angle|2" x 4" Wood', "", "Yes",
  "Master_Mat_Metals: Cost_Frame_AlumAngle_* / Cost_Frame_AlumTube_* / Cost_Frame_SteelAngle_*", ""),
 (C1, "FRAME DEPTH", "DEPTH", "select", '2"', '1.5"|2"|3"', "", "", "", ""),
 (C2, "ASSEMBLY", "ASSEMBLY", "select", "Glued (Lord's Adhesive)", "Glued (Lord's Adhesive)|Welded|Screwed|Riveted", "", "Yes",
  "Master_Mat_Hardware: HRD_ADH_TUBE", ""),
 (C2, "RETAINERS", "RETAINERS", "select", "None", 'None|1.5" Flat|1.5" Formed', "", "", "", ""),
 (C2, "FRAME FINISH", "FRAME COLOR", "finish", "Black", "Black|Bronze|White|Mill / Unpainted", "", "Yes", "", ""),
]

F["HALO_LETTERS"] = [
 (C1, "QUANTITY", "QTY", "autoqty", "6", "LETTER HEIGHT", "", "Yes", "", "Counts letters in TEXT"),
 (C1, "LETTER HEIGHT", "LETTER HEIGHT", "number", "18", "", "", "Yes", "", "Inches, tallest letter"),
 (C1, "TEXT", "TEXT", "text", "SAMPLE", "", "", "Yes", "", ""),
 (C1, "LETTER TYPE", "TYPE", "select", "Reverse Lit (Halo)", "Reverse Lit (Halo)|Reverse Non-Lit", "", "Yes", "", ""),
 (C2, "FACE", "FACE", "select", ".080 Aluminum", ".080 Aluminum|.063 Aluminum|.125 Aluminum|Brushed Aluminum|Stainless Steel", "", "Yes",
  "Master_Mat_Metals: ALM_SHT_080 / ALM_SHT_063", '.063 OK under 12"'),
 (C2, "FACE PAINT", "FACE COLOR", "paint", "", "", "FACE!=Brushed Aluminum&FACE!=Stainless Steel", "Yes", "", ""),
 (C2, "FACE GRAPHICS", "FACE GRAPHICS", "select", "None", "None|Cut Vinyl Accent|Digital Print", "", "", "", ""),
 (C3, "RETURN DEPTH", "RETURN", "select", '3"', '2"|3"|5"', "", "Yes", "Master_Mat_Fab_Channel: CLD-COM-COIL-3 / -5", ""),
 (C3, "RETURN GAUGE", "GAUGE", "select", ".063", ".063|.080|.040", "", "Yes", "", ".063 standard for halo"),
 (C3, "RETURN FINISH", "RETURN COLOR", "finish", "Match Face", "Match Face|Black|Bronze|White", "", "Yes", "", ""),
 (C4, "BACKS", "BACKS", "select", '3/16" Clear Polycarbonate', '3/16" Clear Polycarbonate|1/4" Clear Acrylic|Aluminum (Non-Lit)', "", "Yes", "", ""),
 (C4, "DIFFUSER VINYL", "DIFFUSER", "select", "No", NY, "LETTER TYPE=Reverse Lit (Halo)", "", "", "Smoother halo"),
 (C4, "STANDOFFS", "STANDOFFS", "select", '1.5" Aluminum', '1" Aluminum|1.5" Aluminum|2" Aluminum', "", "Yes", "", "Pattern needed"),
 (C4, "WALL SURFACE", "WALL", "text", "", "", "", "Yes", "", "e.g. Painted stucco, light beige"),
]

F["BACKER_PANEL"] = [
 (C1, "BACKER SIZE", "DIMENSIONS", "dims", "120|36", "W|H", "", "Yes", "", ""),
 (C1, "BACKER TYPE", "TYPE", "select", "Flat", "Flat|Framed|Custom Shape (Routed)", "", "Yes", "", ""),
 (C2, "BACKER MATERIAL", "MATERIAL", "select", "3mm ACM", '3mm ACM|6mm ACM|.063 Aluminum over 2" Angle Frame|.080 Aluminum', "", "Yes",
  "INV_Sheets: SHT_ACM_*; Master_Mat_Metals", ""),
 (C2, "BACKER FINISH", "COLOR", "finish", "White", "White|Black|Brushed Aluminum", "", "Yes", "", ""),
 (C3, "BACKER MOUNTING", "MOUNTING", "select", "Stud Mount", "Stud Mount|Lag to Wall|Z-Clips", "", "Yes", "", ""),
]

F["ADA_SIGN"] = [
 (C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", ""),
 (C1, "SIGN SIZE", "SIZE", "select", '8" x 8"', '4" x 4"|6" x 8"|8" x 8"|12" x 8"', "", "Yes",
  "PROD_ADA_Signs: RET_ADA_0404 / 0608 / 0808 / 1208", ""),
 (C1, "MESSAGE", "MESSAGE", "text", "RESTROOM", "", "", "Yes", "", ""),
 (C1, "PICTOGRAM", "PICTOGRAM", "pictogram", "", "", "", "", "REF_Pictograms", ""),
 (C2, "CONSTRUCTION", "CONSTRUCTION", "select", 'Ultra-Mattes Reverse 1/16"',
  'Ultra-Mattes Reverse 1/16"|Ultra-Mattes Reverse 1/8"|Mattes Front 1/16"', "", "Yes",
  "Master_Mat_ADA: ADA_SUB_116_CORE / ADA_SUB_18_CORE", ""),
 (C2, "BACKGROUND COLOR", "BACKGROUND", "rowmark", "", "Ultra-Mattes Reverse|Mattes (Front)", "", "Yes", "REF_Colors_Rowmark", ""),
 (C2, "CORNERS", "CORNERS", "select", "Square", "Square|Rounded", "", "", "", ""),
 (C2, "BACKER", "BACKER", "select", "None", 'None|3mm Black PVC|3mm White PVC|3/16" Clear Acrylic', "", "",
  "PROD_ADA_Signs: Cost_Sub_PVC / Cost_Sub_Acrylic", ""),
 (C3, "TACTILE COPY", "TACTILE", "select", 'Rowmark ADA Alternative 1/32"', 'Rowmark ADA Alternative 1/32"', "", "Yes",
  "Master_Mat_ADA: ADA_APP_132_TACT", '1/32" min raise (ADA 703.2.1)'),
 (C3, "TACTILE COLOR", "TACTILE COLOR", "rowmark", "", "ADA Alternative", "", "Yes", "REF_Colors_Rowmark", "Must contrast with background"),
 (C3, "BRAILLE", "BRAILLE", "select", "Grade 2 - Clear Raster", "Grade 2 - Clear Raster|Grade 2 - Color Raster", "", "Yes",
  "Master_Mat_ADA: ADA_RAS_BEAD", "ADA 703.3"),
 (C4, "WINDOW / INSERT", "INSERT", "select", "None", "None|Paper Insert w/ Clear Lens|Engraved Slider (Occupied / Vacant)", "", "",
  "Master_Mat_ADA: ADA_SUB_116_LENS", ""),
 (C4, "MOUNTING", "MOUNTING", "select", "VHB Tape + Silicone", "VHB Tape + Silicone|Screws|Standoffs", "", "Yes",
  "Master_Mat_Hardware: VIN_SUP_VHB_TPE", ""),
 (C4, "LOCATION", "LOCATION", "text", 'Latch side, 48"-60" AFF to baseline', "", "", "Yes", "ADA 703.4.1", ""),
]

# Product, order, component, section title, include, repeatable, overrides
ASSEMBLIES = [
 ("Pole Sign", 1, "POLE", "Poles", "Required", "No", ""),
 ("Pole Sign", 2, "POLE_COVER", "Pole Cover", "Optional-On", "No", ""),
 ("Pole Sign", 3, "CABINET", "Cabinet", "Required", "No", "SIDEDNESS=Double Sided; MOUNTING=Pole Mount"),
 ("Pole Sign", 4, "POLY_FACE", "Faces", "Required", "No", "FACE QTY=2"),
 ("Pole Sign", 5, "ILLUMINATION", "Illumination", "Required", "No", ""),
 ("Pole Sign", 6, "EMC", "Digital Sign (EMC)", "Optional-Off", "No", ""),

 ("Lighted Cabinets", 1, "CABINET", "Cabinet", "Required", "No", "MOUNTING=Wall Mount"),
 ("Lighted Cabinets", 2, "POLY_FACE", "Face", "Required", "No", ""),
 ("Lighted Cabinets", 3, "ILLUMINATION", "Illumination", "Required", "No", ""),
 ("Lighted Cabinets", 4, "EMC", "Digital Sign (EMC)", "Optional-Off", "No", ""),

 ("Monument Signs", 1, "MONUMENT_BASE", "Base", "Required", "No", ""),
 ("Monument Signs", 2, "CABINET", "Cabinet", "Required", "No",
  "CONSTRUCTION=Fabricated Aluminum; SIDEDNESS=Double Sided; MOUNTING=Monument Base; CABINET SIZE=120|48|12"),
 ("Monument Signs", 3, "ROUTED_FACE", "Routed Faces", "Optional-On", "No", ""),
 ("Monument Signs", 4, "POLY_FACE", "Polycarbonate Faces", "Optional-Off", "No", "FACE QTY=2"),
 ("Monument Signs", 5, "POLE", "Internal Poles", "Optional-On", "No", "QUANTITY=2; OVERALL LENGTH=8'; EMBED DEPTH=36\""),
 ("Monument Signs", 6, "ILLUMINATION", "Illumination", "Optional-On", "No", ""),
 ("Monument Signs", 7, "EMC", "Digital Sign (EMC)", "Optional-Off", "No", ""),

 ("Post and Panel Sign", 1, "SIGN_PANEL", "Panel", "Required", "No",
  "MEDIA=3M IJ180 Wrap Vinyl; OVERLAMINATE=3M 8518 Wrap Gloss Laminate"),
 ("Post and Panel Sign", 2, "PANEL_FRAME", "Frame", "Required", "No", ""),
 ("Post and Panel Sign", 3, "POLE", "Posts", "Required", "No",
  "POLE MATERIAL=Aluminum; ALUMINUM POLE SIZE=3\" Square, 1/8\" Wall; OVERALL LENGTH=8'; EMBED DEPTH=24\""),

 ("Directional Signs", 1, "SIGN_PANEL", "Panel", "Required", "No", "PANEL SIZE=24|18; GRAPHIC TYPE=Direct Print"),
 ("Directional Signs", 2, "PANEL_FRAME", "Frame", "Required", "No",
  "FRAME POSITION=Perimeter Cabinet Frame; FRAME MATERIAL=1.5\" Aluminum Angle"),
 ("Directional Signs", 3, "POLE", "Post", "Required", "No",
  "QUANTITY=1; POLE MATERIAL=Aluminum; ALUMINUM POLE SIZE=3\" Square, 1/8\" Wall; OVERALL LENGTH=8'; EMBED DEPTH=24\""),
 ("Directional Signs", 4, "POLE_COVER", "Pole Cover", "Optional-Off", "No", ""),
 ("Directional Signs", 5, "ILLUMINATION", "Illumination", "Optional-Off", "No", ""),

 ("Reverse / Halo Lit Channel Letters", 1, "HALO_LETTERS", "Letters", "Required", "Yes", ""),
 ("Reverse / Halo Lit Channel Letters", 2, "BACKER_PANEL", "Backer Panel", "Optional-Off", "No", ""),
 ("Reverse / Halo Lit Channel Letters", 3, "ILLUMINATION", "Illumination", "Required", "No", "PHOTO CELL=Yes"),

 ("ADA Signs", 1, "ADA_SIGN", "ADA Sign", "Required", "Yes", ""),
]

FINISH_COLORS = [
 ("Black", "#000000"), ("Bronze", "#3B312B"), ("White", "#FFFFFF"), ("Mill / Unpainted", "#BFC1C2"),
 ("Brushed Aluminum", "#C9CCCE"), ("Natural Wood", "#A47A4F"), ("Match Cabinet", ""), ("Match Face", ""),
 ("By Others", ""),
]

# Page_Group: sections with the same number share a proof page (max 2 sections per page)
PAGE_GROUPS = {('Pole Sign', 1): 1, ('Pole Sign', 2): 1, ('Pole Sign', 3): 2, ('Pole Sign', 4): 2, ('Pole Sign', 5): 3, ('Pole Sign', 6): 3, ('Lighted Cabinets', 1): 1, ('Lighted Cabinets', 2): 1, ('Lighted Cabinets', 3): 2, ('Lighted Cabinets', 4): 2, ('Monument Signs', 1): 1, ('Monument Signs', 2): 2, ('Monument Signs', 3): 2, ('Monument Signs', 4): 2, ('Monument Signs', 5): 1, ('Monument Signs', 6): 3, ('Monument Signs', 7): 3, ('Post and Panel Sign', 1): 1, ('Post and Panel Sign', 2): 1, ('Post and Panel Sign', 3): 2, ('Directional Signs', 1): 1, ('Directional Signs', 2): 1, ('Directional Signs', 3): 2, ('Directional Signs', 4): 2, ('Directional Signs', 5): 3, ('Reverse / Halo Lit Channel Letters', 1): 1, ('Reverse / Halo Lit Channel Letters', 2): 2, ('Reverse / Halo Lit Channel Letters', 3): 2, ('ADA Signs', 1): 1}
ASSEMBLIES = [a + (PAGE_GROUPS.get((a[0], a[1]), a[1]),) for a in ASSEMBLIES]
