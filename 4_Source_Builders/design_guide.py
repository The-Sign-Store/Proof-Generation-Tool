"""Design department standards (Design_Guide tab) shown in the Proof Generator's Help Center.

Each rule: (Rule_ID, Section, Components, Match_Rule, Standard, Why, CorelDRAW_How_To, Basis)
  Components  comma list of Component_IDs, blank = any
  Match_Rule  Show_If syntax + OR; COMPONENT=ID|ID tests the component itself; blank = always
  Standard    may use {VARIABLE} or {VARIABLE|fallback} placeholders filled from the matching part
  Basis       SignOS (from our SignOS data), Industry (sign industry standard), House (our standard)
Plain ASCII only.
"""

PRINT = ("COMPONENT=DIGITAL_PRINT_VINYL|BANNER OR GRAPHIC TYPE~=Print OR COVER GRAPHICS~=Print "
         "OR FACE GRAPHICS~=Print OR FACE VINYL~=Print")
CUTV = ("COMPONENT=CUT_VINYL_DECAL OR GRAPHIC TYPE=Cut Vinyl|Contour Cut Vinyl|Translucent Cut Vinyl "
        "OR COVER GRAPHICS~=Cut Vinyl OR FACE GRAPHICS~=Cut Vinyl OR FACE VINYL=Translucent Vinyl "
        "OR COMPONENT=ROUTED_FACE & DIFFUSER=White Diffuser Vinyl")
WHITE = ("PRINT LAYERS~=White|Layer OR SIDEDNESS (CLEAR)=Second Surface Print OR GRAPHIC TYPE=2nd Surface Direct Print "
         "OR MATERIAL COLOR=Clear & GRAPHIC TYPE~=Print OR MEDIA~=Clear")
CNC = ("CUSTOM SHAPE~=Yes OR ROUTING~=Yes OR ROUTING=Push-Thru OR BACKER TYPE=Custom Shape (Routed) "
       "OR COMPONENT=PVC_ROUTED_LETTERS|HDU_SIGN|ROUTED_FACE")
RIGID = "SIGN_PANEL,ACM_PANEL,PVC_PANEL,CORO_SIGN,ACRYLIC_PANEL,BACKER_PANEL"
LETTERS = "CHANNEL_LETTERS_FL,HALO_LETTERS"
LIT = "COMPONENT=CHANNEL_LETTERS_FL|ILLUMINATION|ROUTED_FACE OR LETTER TYPE=Reverse Lit (Halo)"
DOUBLE = "SIDEDNESS=Double Sided OR SIDEDNESS (CLEAR)=Double Sided OR SIDEDNESS (18OZ)=Double Sided"
PAINT = ("GRAPHIC TYPE=Paint OR FINISH=Paint OR COMPONENT=HDU_SIGN|MONUMENT_BASE "
         "OR CABINET FINISH~=Custom OR POLE FINISH~=Custom OR RETURN FINISH~=Custom")

G = []


def r(rid, section, comps, rule, std, why="", how="", basis="House"):
    G.append((rid, section, comps, rule, std, why, how, basis))


# ======================================================================  1. EVERY PROOF
S = "EVERY PROOF"
r("G01", S, "", "", "Start every proof from the Proof Generator export. Artwork goes inside the art board only; never cover the spec table, detail drawings, sidebar or approval footer.",
  "The spec table is the work order production builds from. If it is hidden or edited by hand, the proof and the work order stop matching.",
  "File > Import (Ctrl+I) the page SVG at 100%. Put it on layer PROOF TEMPLATE and lock it. Change spec text in the Generator and re-export; do not retype it in CorelDRAW.")
r("G02", S, "", "", "Draw to scale and dimension every item: overall width x height, plus depth for anything 3D. Under 10 ft use inches (96\"); 10 ft and over use feet-inches (12'-6\").",
  "Customers approve size from the proof. Production and install check their work against these numbers.",
  "Toolbox > Dimension tool > Parallel Dimension. Property bar: Units = in, Precision = 0.00, Show units on. Dimension text Arial 8 pt minimum.")
r("G03", S, "", "", "Every color on the art has a callout that matches the spec table exactly: vinyl = brand + number + name (Oracal 751-031 Red), paint = SW or PMS number, print = Full Color Digital. Never 'red' or 'match logo'.",
  "Production orders and mixes from the callout, not from the screen color.",
  "Use the hex from the Generator swatch: select object > Edit Fill (Shift+F11) > Uniform > type the hex in the Hex box.")
r("G04", S, "", "", "Clear every yellow MISSING tag before a proof goes to the customer. A proof with MISSING tags goes back to the salesperson only, with the missing fields listed on the FreshDesk ticket.",
  "Gaps from intake are caught at the proof, not on the shop floor.")
r("G05", S, "", "", "When the install location is known, show the sign in context: site photo mockup, scaled from a known size (standard door = 80\" tall, 3 courses of modular brick = 8\"). Label it 'Placement approximate - verify on site'.",
  "Customers judge size and color in context, and install sees where the sign goes before the truck leaves.",
  "Import the photo to layer MOCKUP. Draw a line over the door height, read its length, then scale the photo with Object > Transform > Scale (Alt+F9) so the line equals 80\". Lock the layer.")
r("G06", S, "", "", "Use the customer's brand fonts or our approved library (Arimo, Liberation Sans, Montserrat, Open Sans). Write the font names in the Description box so reorders match.",
  "Approved fonts are installed on every station and in SignOS (REF_Fonts), so files open the same everywhere.", "", "SignOS")
r("G07", S, "", "", "Plan readable copy at 1\" of capital letter height for every 10 ft of viewing distance. If the main copy is under 1\" per 25 ft, flag it in the proof notes.",
  "This is the common sign industry legibility guideline. Undersized copy is the most common complaint after install.", "", "Industry")
r("G08", S, "", "", "File name: <Ticket#>_<Customer>_<Product>_R<rev>.cdr, saved in the folder shown under File Location. Every revision is Save As with the next number (R0, R1, R2). Never overwrite an approved file.",
  "Anyone can find the file that matches the signed proof.",
  "File > Save As (Ctrl+Shift+S). Export the proof PDF with the same base name.")
r("G09", S, "", "", "Nothing goes to production without a signed proof (signature + date) or the customer's written approval attached to the FreshDesk ticket.",
  "Approval is the handoff point between design and production.")
r("G10", S, "", DOUBLE, "Double sided: proof both sides, or note 'Side 2 identical'. Check that side 2 reads correctly (no mirrored logos) and that both faces line up when built back to back.",
  "Back-to-back faces are a common reprint because the second side was flipped.")

# ======================================================================  2. PROOF COLOR STANDARDS
S = "PROOF COLOR STANDARDS (how materials look on proofs)"
r("C01", S, "", "", "Clear glass / storefront windows: solid baby blue #CFE6F3 (R207 G230 B243), full fill, no transparency. Add two thin white diagonal glare lines at 60% opacity.",
  "Gives every proof the same look for glass, so vinyl applied to glass is easy to read.",
  "Edit Fill > Hex CFE6F3. Glare: 2 pt white lines; Transparency tool > Uniform 40.")
r("C02", S, "", "", "Tinted glass: blue-grey #9DAFBB (R157 G175 B187). Mirrored / reflective glass: #7D8C96 with the same white glare lines.")
r("C03", S, "", "", "Frosted / etched glass vinyl (Oracal 8510, GF 790): #EEF3F6 over the glass blue with a hairline #B0BEC5 edge. Label it FROSTED VINYL.",
  "Frosted film is nearly white on screen; the edge line keeps the shape readable.", "", "SignOS")
r("C04", S, "", "", "Clear acrylic / clear polycarbonate: #E3F2F9 with a 1 pt #7FB3CC edge. Clear vinyl (Oracal 3640): show only the printed art, with a dashed hairline at the film edge.")
r("C05", S, "", "", "White material on a white page (white ACM, PVC, Coroplast, poly faces): fill white with a 0.5 pt #B1B1B3 keyline on the PROOF only so the edge shows. Never put that keyline in production art.",
  "Without it a white panel disappears on the proof; with it in production it would print or cut.")
r("C06", S, "", "", "Metals: brushed aluminum = linear gradient #E6E8EA to #A7ADB2; mill aluminum = #C3C7CA flat; stainless = #D0D4D8. Painted finishes use the Finish_Colors / SW / PMS hex from the Generator.",
  "", "Interactive Fill tool (G) > Linear gradient; set the two node colors by hex.")
r("C07", S, "", "MEDIA~=Perf", "Perforated window film (60/40, 70/30): show the printed art at 75% opacity over the glass blue and note 'PERF - see-through from inside'.", "", "", "SignOS")
r("C08", S, "", LIT, "Lit signs: the daytime view is the default proof. Add a night view: background #1C2230, lit faces at full color with a soft outer glow; halo lit = #FFF3B0 glow on the wall behind the letters.",
  "Shows the customer what they are paying for after dark and catches dark faces that will not glow.",
  "Duplicate the art to a second page. Effects > Drop Shadow tool, preset Glow; color = face color, opacity 60, feather 20.")
r("C09", S, "", "", "Surroundings with no site photo: wall #EDEDED, brick #A0524A, stucco #E8E1D3, concrete / grade #D3D3D3, soil #EFE6D6, sky #E6F2FA, grass #7BAA5A. Keep surroundings lighter and duller than the sign.",
  "Same palette as the detail drawings, so every proof reads the same way.")
r("C10", S, "", "MEDIA~=Reflective", "Reflective vinyl (Oralite 5400): show it in its normal daytime color and add the note REFLECTIVE. Do not simulate shine.", "", "", "SignOS")

# ======================================================================  3. COREL FILE SETUP + HANDOFF
S = "COREL FILE SETUP AND PRODUCTION HANDOFF"
r("F01", S, "", "", "Standard layers, top to bottom: NOTES (non-printing), PRODUCTION (non-printing on the proof page), ART, MOCKUP (locked), PROOF TEMPLATE (locked).",
  "Anyone opening the file knows what prints, what is reference, and what is a production line.",
  "Window > Dockers > Objects. New Layer; click the printer icon to make it non-printing, the lock icon to lock it.")
r("F02", S, "", "", "Production art is built 1:1 at real size on its own page, one page per machine, named PRINT, CUT or ROUTE.",
  "Each operator opens one page that matches their machine, with nothing to scale or delete.",
  "Layout > Insert Page, then right-click the page tab > Rename Page. Set the page size to the part size + 2\".")
r("F03", S, "", "", "Before converting text to curves, copy the live text to a hidden non-printing layer named EDITABLE TEXT. Production pages carry curves only.",
  "Curves cannot change font on the shop computers; the hidden copy keeps future revisions quick.",
  "Ctrl+C the text, select the EDITABLE TEXT layer, Edit > Paste in Place. Hide the layer (eye icon).")
r("F04", S, "", "", "Handoff in the job folder \\PRODUCTION: approved proof PDF + one file per machine: _PRINT.pdf (HP Latex), _CUT (Graphtec), _ROUTE.dxf (MultiCAM). Same base name as the proof.",
  "Matches our equipment list in SignOS (Master_Machines_Fleet) so every file has an owner.", "", "SignOS")
r("F05", S, "", "", "Print art is built in CMYK. Brand matches are named spot colors with the PMS / SW number. Large black areas = rich black C60 M40 Y40 K100; text under 1\" and thin lines = 100 K only.",
  "Rich black prints deep on large areas; small black text in 4 colors blurs from registration.", "", "Industry")
r("F06", S, "", "", "Production line colors, hairline weight: RED = CNC cut outside (profile); BLUE = CNC cut inside (holes, counters); GREEN = CNC pocket / v-carve / drill points; MAGENTA spot 'CutContour' = print-and-cut path; BLACK = plotter (vinyl) cut. One purpose per color.",
  "CNC and cutter operators set up toolpaths by color instead of guessing.",
  "Outline Pen (F12) > Width = Hairline. Set the outline color by right-clicking a palette swatch.")
r("F07", S, "", "", "Before export, preflight: no MISSING tags, all text on production pages converted to curves, no hidden objects off the page, images linked or embedded at size.",
  "", "File > Document Properties shows fonts and images. Edit > Select All > Text finds stray text (then Ctrl+Q).")

# ======================================================================  4. CUT VINYL (Graphtec 64)
S = "CUT VINYL (Graphtec 64 plotter)"
r("V01", S, "", CUTV, "Convert ALL text to curves and give every cut shape a hairline BLACK outline. The fill may stay for the visual; the plotter follows the outline.",
  "Live text changes font on another computer, and the cutter only reads outlines.",
  "Edit > Select All > Text, then Ctrl+Q (Object > Convert to Curves). Select all cut art > F12 Outline Pen: Width Hairline, Color Black (or right-click the black swatch).")
r("V02", S, "", CUTV, "Weld overlapping letters and shapes (scripts, outlined text, tight kerning) so each piece is one clean closed path. No lines crossing inside a letter.",
  "Overlaps make the blade cut through the letter and the shop weeds it out by mistake.",
  "Ctrl+Q, Ungroup All, select the pieces, Object > Shaping > Weld. Check in View > Wireframe: any line inside a letter will be cut.")
r("V03", S, "", CUTV, "Minimum sizes: letters 1/2\" cap height and lines / details 1/16\" wide. Anything smaller is printed instead. Thin scripts or serifs under 1/8\" = mark WEEDING Complex on the spec.",
  "Small cut detail lifts and tears when weeded; SignOS prices complex weeding separately.", "", "Industry")
r("V04", S, "", CUTV, "One layer per vinyl color, named with the exact callout (e.g. 751-031 RED). Each color layer gets the same 2 registration marks (1/4\" crosses) outside the art.",
  "Each color is cut and weeded on its own; the marks line the colors up at application.",
  "Objects docker > New Layer > rename. Draw one + mark, copy it to every color layer with Edit > Paste in Place.")
r("V05", S, "", CUTV, "Layered colors overlap 1/16\" (trap). Never butt two colors edge to edge.",
  "Butted vinyl opens a gap as it shrinks; the overlap hides it.",
  "Contour tool > Outside, 0.0625\", 1 step. Ctrl+K to break the contour apart and use it as the bottom color shape.")
r("V06", S, "", CUTV, "Add a hairline weed box 1/4\" outside each separate graphic.",
  "The shop weeds and masks each piece cleanly (SignOS TASK_WEED_VINYL / TASK_MASK_VINYL).",
  "Rectangle tool around the piece; Property bar size = piece size + 0.5\".", "SignOS")
r("V07", S, "", CUTV, "Every cut path is closed and node-reduced. No open paths, no duplicate stacked objects.",
  "Open paths do not cut out; stacked duplicates cut twice and shred the vinyl.",
  "Shape tool (F10) > Ctrl+A selects all nodes > Reduce Nodes. Object > Join Curves closes gaps. Edit > Find and Replace finds duplicates.")
r("V08", S, "", CUTV, "Graphics applied to the inside of glass but read from outside are mirrored on the CUT page, and the page is named CUT - MIRRORED 2ND SURFACE.",
  "", "Select the art > Property bar > Mirror Horizontally.")
r("V09", S, "", CUTV, "Keep each cut job inside the roll width in use, minus a 1\" margin each side. Letters taller than the roll are split with a 1/2\" overlap at a straight edge, never through a counter.",
  "The plotter tracks best with margins, and seams on straight edges disappear when applied.", "", "SignOS")
r("V10", S, "POLY_FACE,CHANNEL_LETTERS_FL,ROUTED_FACE", "", "Lit faces get translucent vinyl only (Oracal 8500 / 8800). Opaque vinyl (651 / 751 / 951) goes on a lit face only when it is meant to block light (outlines, blockout).",
  "Opaque vinyl shows as dark blotches at night.", "", "SignOS")
r("V11", S, "", CUTV, "The vinyl series on the proof matches the spec: 651 intermediate (flat, short to mid term); 751 / 951 cast (long term, curves, rivets); 631 matte (indoor walls); 8500 / 8800 translucent (lit faces).",
  "Series choice is a durability promise to the customer (SignOS Master_Mat_Vinyl_Cut).", "", "SignOS")

# ======================================================================  5. DIGITAL PRINT (HP Latex)
S = "DIGITAL PRINT (HP Latex 300 roll / HP Latex R1000 flatbed)"
r("P01", S, "", PRINT, "Raster images at 150 ppi at final print size (100 ppi is fine for banners and signs read from 15 ft+; 300 ppi for decals and anything read up close). Rebuild low-res logos as vectors.",
  "Low resolution is the top cause of reprints in large format.",
  "Select the image; the status bar shows its ppi at the current size. Bitmaps > Resample shows the effective resolution.", "Industry")
r("P02", S, "", PRINT, "Bleed: direct print to rigid (R1000 flatbed) 1/8\" past trim; printed vinyl that is mounted then trimmed 1/2\". Safe zone: keep text and logos 1/2\" inside trim (1\" on anything over 4 ft).",
  "Trimming drifts slightly; bleed stops white edges and the safe zone keeps copy from being cut.",
  "Put a trim rectangle on the PRODUCTION layer. Extend backgrounds past it. Contour tool > Inside 0.5\" for a non-printing safe line.", "Industry")
r("P03", S, "", PRINT, "Maximum print width is 64\" (HP R1000 and HP 300 media limit). Larger graphics are tiled in panels up to 60\" wide with a 1/2\" overlap. Seams fall on solid color, never through faces or small text, and the seam is shown on the proof.",
  "64\" is the printer limit in SignOS (MACH_HP_R1000 BED_WIDTH, Printer_Max_Roll_Width).",
  "Draw panel rectangles 60\" wide with 0.5\" overlap; Object > PowerClip > Place Inside Frame to clip a copy of the art into each.", "SignOS")
r("P04", S, "", PRINT, "Laminate printed vinyl per the spec ({OVERLAMINATE|see spec table}). Cast print (3M IJ180) gets cast laminate (3M 8518 / 8519 / 8520); calendered gets Arlon 3210 or Oraguard 210. Note gloss / luster / matte on the proof.",
  "Laminate pairs are matched in SignOS so they shrink together.", "", "SignOS")
r("P05", S, "", "GRAPHIC TYPE=Digital Print Contour Cut Vinyl OR CONTOUR CUT=Yes",
  "Print-and-cut: the contour is a spot color named CutContour (100% magenta), hairline, set to overprint, 1/16\" outside the art (or a designed white border). Leave 1\" around the job for the cutter registration marks.",
  "The RIP and the Graphtec read the CutContour line as the cut path, not as ink.",
  "Contour tool > Outside 0.0625\", 1 step > Ctrl+K. Window > Color Palettes > Palette Editor: new color CutContour C0 M100 Y0 K0, Treat as Spot. Hairline outline, no fill, right-click > Overprint Outline.", "Industry")
r("P06", S, "", PRINT, "Export print files with File > Publish to PDF, preset PDF/X-4, 'Export all text as curves' on, images embedded, bleed included. Name it _PRINT.pdf.",
  "One consistent print format for the RIP; no missing fonts.",
  "Publish to PDF > Settings: General = PDF/X-4; Objects = Export all text as curves; Prepress = Bleed limit 0.5\".", "Industry")
r("P07", S, "", PRINT, "Brand-critical colors: the PMS / SW number goes on the proof and as the spot color name in the file. Print a color swatch strip for approval on first orders.",
  "Screens and printers differ; the strip shows the customer the real print color before the full run.")
r("P08", S, "", "MEDIA~=Perf", "Window perf (60/40, 70/30): text at least 3\" tall, no hairlines (the holes eat detail), keep key copy off window mullions. Exterior perf gets optically clear laminate.",
  "", "", "SignOS")
r("P09", S, "", "MEDIA~=Wall", "Wall graphics (GF 226, 3M IJ8624 textured): tile in panels with a 1/2\" overlap and keep faces and copy off the seams. Textured wall vinyl gets 3M 8524 laminate.", "", "", "SignOS")

# ======================================================================  6. WHITE INK + CLEAR
S = "WHITE INK AND CLEAR MATERIALS (HP R1000)"
r("W01", S, "", WHITE, "White ink is its own object on its own layer named WHITE INK: a spot color named WHITE at 100%, set to overprint, sitting exactly over the art.",
  "The RIP builds the white channel from that spot; mixing it into the art prints white over color.",
  "Palette Editor: new color WHITE, Treat as Spot. Duplicate the art (Ctrl+D, then align), weld, fill WHITE, right-click > Overprint Fill.")
r("W02", S, "", WHITE, "Choke the white 1/32\" (0.03\") inside the color edges.",
  "Stops a white halo around the art from slight registration shift.",
  "Contour tool > Inside, 0.03\", 1 step > Ctrl+K, keep the inner shape as the white.", "Industry")
r("W03", S, "", WHITE, "Second surface (printed on the back of clear acrylic / poly, read from the front): mirror the art. Print order Color then White. Lit day/night faces use 3-Layer (Color-White-Color); blockout uses 5-Layer. Match the spec: {PRINT LAYERS|see spec table}.",
  "Layer order and mirroring decide how the face reads by day and by night.",
  "Property bar > Mirror Horizontally on the PRINT page. Name the page PRINT - MIRRORED 2ND SURFACE.", "SignOS")
r("W04", S, "", WHITE, "Use white only where needed. On the R1000, white prints at 6 LF/hr, 3-layer at 3.1 and 5-layer at 1.6, against 18 LF/hr for a standard print.",
  "Every white layer multiplies press time (SignOS MACH_HP_R1000 speeds).", "", "SignOS")

# ======================================================================  7. RIGID PANELS + CNC
S = "RIGID PANELS AND CNC (MultiCAM 5x10)"
r("R01", S, RIGID + ",POLY_FACE", "", "Plan art on stock sheet sizes: Coroplast 48x96, ACM 48x96 / 48x120 / 60x120, PVC 48x96, acrylic 48x96, polycarbonate 52x120. Anything larger needs a seam; show the seam on the proof. Nest small signs to the sheet.",
  "Sheet sizes come from SignOS INV_Sheets; a design that fits the sheet avoids a seam and saves material.", "", "SignOS")
r("R02", S, RIGID, "", "Square-cut panels go to the shear / saw: dimension the exact trim size. Rounded corners use the corner rounder radii only (1/4\", 1/2\", 1\"); any other shape is a CNC route.",
  "SignOS times corner rounding separately from routing; standard radii keep it a quick shop step.",
  "Rectangle tool > Property bar corner radius, or Window > Dockers > Corners (Fillet).", "SignOS")
r("R03", S, "", CNC, "Inside corners carry the bit radius: standard 1/4\" bit = 1/8\" minimum inside radius. Keep 1/4\" minimum between routed parts and letters; smallest routed stroke 3/16\" (1/4\" for PVC / acrylic letters).",
  "A router cannot cut a sharp inside corner; designing for it avoids hand finishing.", "", "Industry")
r("R04", S, "", CNC, "Route file: closed hairline curves only, color coded (RED outside, BLUE inside, GREEN pocket / drill), welded, nodes reduced, 1:1, no fills, no text objects. Export as _ROUTE.dxf.",
  "Clean geometry imports straight into the CAM software with no cleanup.",
  "Select the route art > File > Export > DXF, Selected only, version R14, units inches, export text as curves.")
r("R05", S, "", CNC, "Nest parts on the 5x10 bed (60\" x 120\") with 1/2\" between parts and 1\" from the sheet edge.",
  "Matches the MultiCAM 5x10 tables (SignOS Master_Machines_Fleet).",
  "Draw a 60x120 rectangle on PRODUCTION as the bed; Arrange > Align and Distribute (Ctrl+Shift+A) to space parts.", "SignOS")
r("R06", S, "", "MOUNTING~=Stud OR BACKER MOUNTING=Stud Mount",
  "Stud mounts: 2 studs minimum per letter or part, 3 or more for parts over 24\". Mark them as GREEN drill points on the route file and on a 1:1 paper install pattern page.",
  "Install drills the wall from the pattern; production drills the parts from the same points.")

# ======================================================================  8. BANNERS
S = "BANNERS"
r("B01", S, "BANNER", "", "Add a 1\" hem on every hemmed side and bleed the background through the hem. Keep text and logos 2\" inside the finished edge. The proof shows the FINISHED size.",
  "SignOS hem allowance is 1\" (Allow_Hem_Inch); copy too close to the edge gets folded or punched.", "", "SignOS")
r("B02", S, "BANNER", "GROMMETS=Yes", "Grommets: {GROMMET SPACING|corners and every 18-24 in}. Mark each grommet as a 1/2\" circle on the PRODUCTION layer and keep art 1\" clear around them.",
  "The shop punches where marked, and nothing important lands under a grommet.",
  "Draw one 0.5\" circle; Edit > Step and Repeat (Ctrl+Shift+D) with the spacing as the offset.")
r("B03", S, "BANNER", "POLE POCKETS=Yes", "Pole pockets: standard 3\" finished pocket unless the spec says otherwise, at {POCKET LOCATIONS|the spec locations}. Add the pocket fold allowance to the art and keep copy out of the pocket area.",
  "Copy inside the pocket is sewn over and hidden.")
r("B04", S, "BANNER", "", "Media: 13 oz standard (single sided), 18 oz blockout (double sided: each side its own PRINT page, check orientation), 8 oz mesh for fences and wind (no text under 2\" on mesh). Banners wider than 64\" in both directions need a seam; show it on the proof.",
  "64\" is the roll limit in SignOS; mesh holes break up small text.", "", "SignOS")

# ======================================================================  9. CHANNEL + HALO LETTERS
S = "CHANNEL LETTERS AND HALO LETTERS"
r("L01", S, "CHANNEL_LETTERS_FL", "", "Lit letter size: 12\" minimum cap height with 5\" returns, 8\" minimum with 3\" returns; stroke at least 1.5\" wide (2\" preferred) so LED modules fit. Thinner fonts go halo lit or non-lit.",
  "LED modules need room inside the stroke or the letter shows hot spots.", "", "Industry")
r("L02", S, LETTERS, "", "Bender-friendly shapes: no razor-sharp inside points (give them at least a 1/8\" radius). Script copy is either welded into one piece per word or split so no strokes touch.",
  "The channel letter bender (SignOS MACH_CHL_BEND) forms returns around the outline; sharp inside points crack or need hand work.",
  "Ctrl+Q, Weld; Shape tool > select a sharp node > Property bar Fillet / Corners docker 0.125\".", "SignOS")
r("L03", S, LETTERS, "", "Letter files: 1:1 face outlines (hairline, welded, closed) on the ROUTE / CUT page with counters as separate inside paths, plus a full-size install pattern page with stud and wire hole locations (or raceway position).",
  "Fabrication cuts faces and backs from the same outlines; install mounts from the pattern.")
r("L04", S, "CHANNEL_LETTERS_FL", "", "Call out face, return and trim cap colors on the proof (return {RETURN|per spec}, trim cap {TRIM CAP|per spec}). Trim cap matches the return unless the spec says otherwise.",
  "Trim cap color is the most common missing callout on letter sets.")
r("L05", S, "CHANNEL_LETTERS_FL", "MOUNTING=Raceway", "Raceway: draw it on the proof at real size behind the letters, painted to match the wall (give the SW number), shorter than the letter set, and centered under the copy.",
  "The raceway is visible on the building; customers must approve its color and length.")
r("L06", S, "HALO_LETTERS", "", "Halo letters: stroke at least 1.5\". Standoff {STANDOFFS|1.5 in} gives an even halo. Note the wall surface; halo reads best on a solid, light wall. Show the night view.",
  "Halo depends on the wall it lights; dark or broken surfaces swallow it.")
r("L07", S, "", LIT, "Lit signs: note the power supply location (remote, in raceway, or in cabinet), the primary electrical by others or by us, and where the ETL label goes.",
  "Electricians and inspectors look for this; ETL listing is on our proof template.")

# ======================================================================  10. CABINETS + FACES
S = "CABINETS AND FACES"
r("K01", S, "CABINET,PANEL_FRAME", "", "Copy safe area: the retainer covers {RETAINER SIZE|1.5 in} of the face on every side. Keep copy at least the retainer size + 1\" inside the cabinet edge, and show the visible face area on the proof.",
  "Copy designed to the cabinet edge disappears under the retainer.")
r("K02", S, "POLY_FACE,CABINET", "", "Face stock: 3/16\" polycarbonate sheets are 52\" x 120\". Faces larger than that need a split bar, a pan face or a flex face; show the split on the proof.",
  "From SignOS INV_Sheets (SHT_POL_316_52X120).", "", "SignOS")
r("K03", S, "POLY_FACE,ROUTED_FACE,CABINET", "", "Lit faces: light copy on a dark background needs a blockout or day/night print (it costs more press time); dark copy on a light face is the default.",
  "Dark backgrounds glow unevenly unless they are blocked out.")
r("K04", S, "", "COPY TYPE=Push-Thru Acrylic OR MOUNTING=Push-Thru OR ROUTING=Push-Thru", "Push-thru: copy is 1/2\" or 3/4\" acrylic, minimum stroke 3/8\", inside corners 1/8\" radius. Design gives the copy outline; fabrication offsets the face opening.",
  "Thin push-thru strokes snap and cannot be routed cleanly.", "", "Industry")
r("K05", S, "CABINET", "", "Cabinets: show depth on the proof, the side / return color, and the mounting ({MOUNTING|per spec}). Double sided cabinets: proof both faces.",
  "Depth and side color are part of what the customer sees from the street.")

# ======================================================================  11. POLES, MONUMENTS, STRUCTURE
S = "POLES, MONUMENTS AND STRUCTURE"
r("S01", S, "POLE,MONUMENT_BASE", "", "Elevation drawing: grade line, overall height above grade, clearance to the sign bottom, cabinet size, pole size and quantity, and embed depth ({EMBED DEPTH|per spec}). Heights in feet-inches.",
  "This is the drawing the permit office and the install crew both use.")
r("S02", S, "POLE", "", "Clearance to verify with local code: plan at least 8'-0\" from grade to sign bottom over walkways and 14'-6\" over drive lanes. Add 'Verify clearances and setbacks with Permitting' to the notes.",
  "Common code minimums; local codes vary, so Permitting confirms.", "", "Industry")
r("S03", S, "POLE", "FOOTER=Engineered Concrete Footer OR EMBED DEPTH=Per Engineering", "Engineered footer: route the proof to Permitting before final approval and mark the proof 'Footer per engineering'. Do not show a footer size until the engineering is back.",
  "The footer comes from the engineer, not from design.")
r("S04", S, "POLE", "", "Any proof with a footer or ground anchor includes the note 'Call 811 before digging'.",
  "Utility locates are required before digging in the US.", "", "Industry")
r("S05", S, "MONUMENT_BASE", "", "Monument bases: show the base material and the reveal. Bases built by others (brick, stone, stucco) are labeled BY OTHERS with the size they must build to.",
  "Makes the scope split clear to the customer and their contractor.")
r("S06", S, "POLE_COVER", "COVER GRAPHICS~=Address", "Address numbers: contrasting color, sized for street reading (commonly 6\" minimum on commercial sites; verify local fire code).",
  "Fire departments enforce address visibility.", "", "Industry")

# ======================================================================  12. PAINT + FINISHES
S = "PAINT AND FINISHES (paint booth / HVLP)"
r("N01", S, "", PAINT, "Paint callouts: Sherwin-Williams number + name (e.g. SW 7069 Iron Ore) or PMS 'painted to match'. Sheen: satin unless the spec says otherwise.",
  "The paint booth mixes from the number; sheen changes how the color reads.")
r("N02", S, "", PAINT, "On the proof, paint colors use the SW / PMS hex from the Generator, with the note 'Screen colors approximate - paint mixed to SW / PMS number'.",
  "Sets customer expectations; screens cannot show paint exactly.")
r("N03", S, "", "GRAPHIC TYPE=Paint", "Painted graphics need a cut mask: put the mask art on a CUT page, following the cut vinyl rules (curves, hairline, welded, weed box).",
  "The mask is cut on the plotter like vinyl.")

# ======================================================================  13. HDU
S = "HDU (Precision Board)"
r("H01", S, "HDU_SIGN", "", "HDU is 1\" or 1.5\" Precision Board on 48x96 sheets. Raised copy stroke at least 3/8\"; routed background depth 1/4\" to 1/2\"; note texture ({ROUTING|per spec}) and that edges are painted.",
  "Thin raised strokes break off in foam.", "", "SignOS")
r("H02", S, "HDU_SIGN", "", "HDU route file: outline RED, raised copy / v-carve GREEN, texture area as its own closed shape named TEXTURE on the ROUTE page.",
  "The CNC operator assigns a different tool to each.")

# ======================================================================  14. ADA
S = "ADA SIGNS"
r("A01", S, "ADA_SIGN", "", "Tactile copy: UPPERCASE, sans serif, raised 1/32\" (Rowmark ADA Alternative), cap height 5/8\" to 2\" measured on the uppercase I, at least 1/8\" between characters. Use an ADA-set font (Arial Medium, Helvetica Medium, Futura Medium...).",
  "ADA 2010 standards as summarized in our ADA reference guide.", "", "Industry")
r("A02", S, "ADA_SIGN", "", "Braille: Grade 2, 3/8\" to 1/2\" below the last line of text. On the proof show it as a labeled placeholder line (GRADE 2 BRAILLE) with the text it translates; production places the raster beads.",
  "Braille dots drawn by hand are never accurate; production uses the braille translator.", "", "Industry")
r("A03", S, "ADA_SIGN", "", "Pictograms: 6\" minimum high pictogram field with no text inside it; the text description goes directly below the field.",
  "Required whenever a pictogram is used.", "", "Industry")
r("A04", S, "ADA_SIGN", "", "Non-glare (matte) surfaces with strong light-on-dark or dark-on-light contrast. The Generator flags LOW CONTRAST; never use brushed or metallic as the background.",
  "Glare and low contrast fail inspection.", "", "Industry")
r("A05", S, "ADA_SIGN", "", "Add the mounting note to every ADA proof: latch side of the door, 48\" minimum to the baseline of the lowest tactile line, 60\" maximum to the highest, centered on an 18\" x 18\" clear floor space.",
  "Install mounts from this note.", "", "Industry")
r("A06", S, "ADA_SIGN", "", "Size signs to fit our equipment: engraver beds 18x12 and 24x18, router 24x48, Rowmark sheets 24x48. Keep like sign types the same size across a building.",
  "From SignOS Master_Workstations and Master_Mat_ADA.", "", "SignOS")

# ======================================================================  15. EMC
S = "ELECTRONIC MESSAGE CENTERS"
r("E01", S, "EMC", "", "EMC: draw the display at the vendor's cabinet size and pixel matrix ({PIXEL PITCH|per spec} pitch), with sample content labeled SAMPLE CONTENT. Attach the vendor drawing to the job folder.",
  "The vendor drawing controls the cabinet opening and the power / data requirements.")


if __name__ == "__main__":
    import collections
    c = collections.Counter(x[1] for x in G)
    for k, v in c.items():
        print(f"{v:3d}  {k}")
    print(len(G), "rules;", "non-ascii:", sum(1 for x in G for s in x for ch in s if ord(ch) > 127))
    assert len({x[0] for x in G}) == len(G)
