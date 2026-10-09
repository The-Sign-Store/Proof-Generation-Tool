import sys, copy
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
sys.path.insert(0, "/home/claude/proofgen")
from modular_data import REGISTRY, F, ASSEMBLIES, FINISH_COLORS
from legacy_components import LEGACY, LEGACY_ASSEMBLIES, EXTRA_FINISH
from detail_drawings import D as DRAWINGS
from design_guide import G as GUIDE
NEW_PRODUCTS = {a[0] for a in ASSEMBLIES}          # the 6 stub products (+ Pole Sign) to retire
REGISTRY = list(REGISTRY) + [(cid, name, "No", "Yes", desc) for cid, (name, desc, _f) in LEGACY.items()]
F = dict(F); F.update({cid: f for cid, (_n, _d, f) in LEGACY.items()})
ASSEMBLIES = list(ASSEMBLIES) + LEGACY_ASSEMBLIES
FINISH_COLORS = list(FINISH_COLORS) + EXTRA_FINISH

UP = "/root/.claude/uploads/acc1ae59-fc94-5c54-82d5-acb68bbab5a0/"
SRC = UP + "5fae4e44-Sign_Proof_Specifications_App_Data.xlsx"
DEV = UP + "c5356ff4-SignOS_DEV_Backend.xlsx"
OUT = "/home/claude/proofgen/out/Sign_Proof_Specifications_App_Data.xlsx"

wb = load_workbook(SRC)
dev = load_workbook(DEV, data_only=True)

HDR_FILL = PatternFill("solid", fgColor="3C5F90")
HDR_FONT = Font(name="Arial", bold=True, color="FFFFFF")
BODY = Font(name="Arial", size=10)
thin = Side(style="thin", color="D0D0D0")

def sheet(name, headers, rows, widths, index=None):
    if name in wb.sheetnames:
        del wb[name]
    ws = wb.create_sheet(name, index) if index is not None else wb.create_sheet(name)
    ws.append(headers)
    for c in ws[1]:
        c.fill = HDR_FILL; c.font = HDR_FONT; c.alignment = Alignment(vertical="center")
    for r in rows:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = BODY; c.alignment = Alignment(vertical="top", wrap_text=False)
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws

# ---------- 1. Retire stub rows for the 6 products now driven by assemblies ----------
ps = wb["Product_Schema"]
moved_products = NEW_PRODUCTS
stub_rows, keep_idx = [], []
for i, row in enumerate(ps.iter_rows(min_row=2, values_only=True), start=2):
    if row[0] in moved_products:
        stub_rows.append(row)
        keep_idx.append(i)
for i in sorted(keep_idx, reverse=True):
    ps.delete_rows(i)
sheet("Retired_Schema_Stubs", ["Product", "Zone", "Variable", "Default", "Options"], stub_rows, [36, 22, 24, 40, 30])

# ---------- 2. Component registry ----------
sheet("Component_Registry", ["Component_ID", "Display_Name", "Show_As_Tool", "Repeatable", "Description"],
      REGISTRY, [18, 26, 14, 12, 70])

# ---------- 3. Component schema ----------
rows = []
for cid, *_ in REGISTRY:
    for row in F[cid]:
        z, var, label, typ, d, opts, show, req, ref, note = row[:10]
        hide = row[10] if len(row) > 10 else ""
        rows.append((cid, z, var, label, typ, d, opts, show, req, ref, note, hide))
cs = sheet("Component_Schema",
           ["Component_ID", "Zone", "Variable", "Label", "Type", "Default", "Options", "Show_If", "Required", "SignOS_Ref", "Notes", "Hide_Values"],
           rows, [20, 11, 22, 18, 10, 30, 60, 34, 9, 46, 34, 14])
types = '"text,number,select,dims,paint,finish,color,vinyl,db,rowmark,pictogram,autoqty,fullcolor"'
dv = DataValidation(type="list", formula1=types, allow_blank=False); cs.add_data_validation(dv); dv.add(f"E2:E{len(rows)+200}")
dv2 = DataValidation(type="list", formula1='"Yes,"', allow_blank=True); cs.add_data_validation(dv2); dv2.add(f"I2:I{len(rows)+200}")
# light band per component
band = PatternFill("solid", fgColor="F2F5FA"); last, on = None, False
for r in range(2, cs.max_row + 1):
    cid = cs.cell(r, 1).value
    if cid != last: on, last = (not on), cid
    if on:
        for c in range(1, 13): cs.cell(r, c).fill = band

# ---------- 4. Product assemblies ----------
asm = sheet("Product_Assembly",
            ["Product", "Order", "Component_ID", "Section_Title", "Include", "Repeatable", "Default_Overrides", "Page_Group"],
            ASSEMBLIES, [36, 8, 18, 24, 14, 12, 80, 12])
dv3 = DataValidation(type="list", formula1='"Required,Optional-On,Optional-Off"'); asm.add_data_validation(dv3); dv3.add("E2:E300")
dv4 = DataValidation(type="list", formula1='"Yes,No"'); asm.add_data_validation(dv4); dv4.add("F2:F300")
dv5 = DataValidation(type="list", formula1="=Component_Registry!$A$2:$A$100"); asm.add_data_validation(dv5); dv5.add("C2:C300")

# ---------- 5. Finish colors ----------
sheet("Finish_Colors", ["Color Name", "HEX Code"], FINISH_COLORS, [24, 12])

# ---------- 6. Rowmark colors from SignOS ----------
rm_rows = []
for r in dev["REF_Colors_Rowmark"].iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    code, series, thick, cap, core, caphex = r[0], r[1], r[2], r[3], r[4], r[5]
    rm_rows.append((series, code, f"{code} {cap}" + (f" / {core}" if core and series != "ADA Alternative" else ""), caphex, thick, cap, core))
sheet("Rowmark_Colors", ["Series", "Color_Code", "Display_Name", "Hex_Code", "Thickness", "Cap_Color", "Core_Color"],
      rm_rows, [24, 12, 32, 10, 10, 18, 14])

# ---------- 7. ADA pictograms from SignOS ----------
pic = [r for r in dev["REF_Pictograms"].iter_rows(min_row=2, values_only=True) if r[0]]
sheet("ADA_Pictograms", ["Item_Code", "Category", "Name", "ViewBox", "SVG_Path", "Is_Active", "Notes"],
      pic, [14, 16, 30, 14, 60, 10, 34])

# ---------- 8. SignOS reference (materials behind the options) ----------
ref = []
def take(tab, prefixes, cols=(0, 4, 3)):
    ws = dev[tab]
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] and any(str(r[0]).startswith(p) for p in prefixes):
            ref.append((tab, r[cols[0]], r[cols[1]], r[cols[2]]))
take("Master_Mat_Metals", ["STL_", "ALM_", "Cost_Post", "Cost_Frame"])
take("Master_Mat_Rigid", ["SUB_ACM", "SUB_HDU", "SUB_PVC", "SUB_ACR", "CNC_SUB_ACR"])
take("Master_Mat_Fab_Channel", ["CLD", "FAB"])
take("Master_Mat_Hardware", ["HRD_", "FAB_", "LBR_", "4x4", "VIN_SUP_VHB", "MNT_"])
take("Master_Mat_Vinyl_Cut", ["VIN_"])
take("Master_Mat_Vinyl_Print", ["VIN_ROL_PRT", "VIN_ROL_LAM"])
seen = set(); ADA = []
for r in dev["Master_Mat_ADA"].iter_rows(min_row=2, values_only=True):
    if r[0] and r[0] not in seen:
        seen.add(r[0]); ADA.append(("Master_Mat_ADA", r[0], r[4], r[3]))
ref += ADA
for r in dev["INV_Sheets"].iter_rows(min_row=2, values_only=True):
    if r[0] and r[1] in ("Polycarbonate", "Aluminum", "HDU"):
        ref.append(("INV_Sheets", r[0], f"{r[1]} {r[2]} ({r[3]:g}\" x {r[4]:g}\")", "Sheet"))
for r in dev["Master_Services"].iter_rows(min_row=2, values_only=True):
    if r[0] and str(r[0]).startswith(("SRV_CNC", "SRV_FEE_PAINT")):
        ref.append(("Master_Services", r[0], r[0].replace("SRV_", "").replace("_", " ").title(), "Service"))
sheet("SignOS_Reference", ["SignOS Tab", "SKU / Key", "Description", "UOM"], ref, [24, 32, 44, 10])

# ---------- 8b. Proof sheet template text (fixed content on every page) ----------
TEMPLATE = [
 ("Title", "DESIGN PROOF"),
 ("ETL_Text", "ETL Listed for Safety (USA & Canada) This product proudly bears the ETL Listed Mark. This certification from Intertek \u2014 an OSHA-recognized Nationally Recognized Testing Laboratory (NRTL) \u2014 proves that this item has been independently tested and meets all applicable U.S. and Canadian product safety standards. The ETL mark is accepted by inspectors, retailers, and regulatory authorities across North America."),
 ("Legal_Text", "This design and engineering is submitted as our proposal, and the right to use or exhibit in any form, is not authorized without written permission by The Sign Store Online, Inc."),
 ("Copyright_Text", "Copyright {YEAR}. All Design/Images for The Sign Store Online, Inc."),
 ("Approval_Label", "Customer Approval Signature"),
 ("Date_Label", "Date"),
 ("Watermark", "On"),
 ("Watermark_Opacity", "2"),
 ("Detail_Drawings", "On"),
 ("Cover_Page", "On"),
 ("Cover_Title", "DESIGN PROOF PACKAGE"),
 ("QA_Checklist", "On"),
 ("QA_Final_Checks", "Finished work matches the signed proof (every page)|Overall dimensions verified against the proof|Colors match the callouts (vinyl / paint / print)|Mounting hardware, patterns and templates included|Lit signs: ETL label applied and power supply tested|Clean, protected and labeled for install / pickup"),
]
TEMPLATE = [(k, v.encode().decode("unicode_escape") if "\\u" in v else v) for k, v in TEMPLATE]
sheet("Proof_Template", ["Key", "Value"], TEMPLATE, [20, 140])

# ---------- 8c. Detail drawings (bottom-right of the art board, when the specs match) ----------
dd_rows = [(did, cat, title, comps, rule, (i + 1) * 10, "Yes", markup, notes)
           for i, (did, cat, title, comps, rule, notes, markup) in enumerate(DRAWINGS)]
dd = sheet("Detail_Drawings", ["Drawing_ID", "Category", "Title", "Components", "Match_Rule", "Order", "Active", "SVG_Markup", "Notes"],
           dd_rows, [20, 20, 26, 30, 56, 8, 8, 60, 60])
dv6 = DataValidation(type="list", formula1='"Yes,No"'); dd.add_data_validation(dv6); dv6.add("G2:G300")
band = PatternFill("solid", fgColor="F2F5FA"); last, on = None, False
for r in range(2, dd.max_row + 1):
    cat = dd.cell(r, 2).value
    if cat != last: on, last = (not on), cat
    if on:
        for c in range(1, 10): dd.cell(r, c).fill = band

# ---------- 8d. Design guide (Help Center pop-up in step 2) ----------
dg_rows = [(rid, sec, comps, rule, std, why, how, basis, (i + 1) * 10, "Yes")
           for i, (rid, sec, comps, rule, std, why, how, basis) in enumerate(GUIDE)]
dg = sheet("Design_Guide", ["Rule_ID", "Section", "Components", "Match_Rule", "Standard", "Why", "CorelDRAW_How_To", "Basis", "Order", "Active"],
           dg_rows, [9, 34, 30, 44, 90, 60, 70, 10, 8, 8])
dv7 = DataValidation(type="list", formula1='"Yes,No"'); dg.add_data_validation(dv7); dv7.add("J2:J400")
dv8 = DataValidation(type="list", formula1='"SignOS,Industry,House"'); dg.add_data_validation(dv8); dv8.add("H2:H400")
last, on = None, False
for r in range(2, dg.max_row + 1):
    sec = dg.cell(r, 2).value
    if sec != last: on, last = (not on), sec
    for c in range(1, 11):
        if on: dg.cell(r, c).fill = PatternFill("solid", fgColor="F2F5FA")
        if c in (5, 6, 7): dg.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")

# ---------- 9. README ----------
readme = [
 ("VERSION 1.3 (PROOF PACKAGES)", ""),
 ("Flow", "1) Select any mix of products and components on the dashboard  2) Fill in specs  3) Add customer info  4) Generate Proof Package (zip of editable SVG + PNG per page)."),
 ("All products migrated", "The 10 original products are now components too (ACM_PANEL, CORO_SIGN, BANNER ...), each with a one-line Product_Assembly row. Product_Schema is kept for reference only; the current app does not read it."),
 ("Proof_Template", "Fixed text printed on every proof page (title, ETL text, legal text, copyright). {YEAR} becomes the current year."),
 ("Hide_Values", "Component_Schema column. Values listed here (e.g. None) are not printed on the proof."),
 ("color / fullcolor types", "color = dropdown of color names with a swatch (colors from Finish_Colors). fullcolor = fixed 'Full Color Digital' with a rainbow swatch."),
 ("", ""),
 ("WHAT CHANGED FROM THE ORIGINAL APP", ""),
 ("New engine", "Complex products are now ASSEMBLIES of reusable COMPONENTS. The 10 existing Product_Schema products (ACM, Acrylic, Banner, Channel Letters - Front Lit, Coroplast, Cut Vinyl Decal, Digital Print Vinyl, HDU Sign, PVC Panel, PVC - Routed Letters) still run exactly as before."),
 ("Products moved", "ADA Signs, Directional Signs, Lighted Cabinets, Monument Signs, Post and Panel Sign, Reverse / Halo Lit Channel Letters. Their old stub rows are kept in Retired_Schema_Stubs."),
 ("New product", "Pole Sign = Pole + Pole Cover + Cabinet + Polycarbonate Face + Illumination (+ optional EMC)."),
 ("Component tools", "Every component with Show_As_Tool = Yes appears in the dropdown under 'Components' and can be proofed on its own."),
 ("", ""),
 ("TABS", ""),
 ("Component_Registry", "One row per component: ID, display name, tool on/off, repeatable, description."),
 ("Component_Schema", "The fields of each component. Zone = preview column. Label = text shown on the proof. Type controls the input (see TYPES)."),
 ("Product_Assembly", "Which components make up each product, in order. Include = Required / Optional-On / Optional-Off (checkbox in the app). Repeatable = Yes adds an '+ Add another' button. Default_Overrides change a component's defaults for that product only."),
 ("Page_Group", "Product_Assembly column. Sections with the same Page_Group number share a proof page. Max 2 sections per page; a group with more is split across pages. Leftover single sections from neighboring groups are paired together."),
 ("Finish_Colors", "Standard finishes (Black, Bronze, White...) and their swatch color. Any 'finish' field also offers 'Custom Paint' (SW / PMS picker)."),
 ("Rowmark_Colors", "Copied from SignOS REF_Colors_Rowmark. Used by ADA background and tactile color pickers."),
 ("ADA_Pictograms", "Copied from SignOS REF_Pictograms. The proof draws the selected pictogram."),
 ("SignOS_Reference", "SignOS SKUs behind the material options (posts, frames, sheet stock, LEDs, vinyl, ADA, hardware). The SignOS_Ref column in Component_Schema points here."),
 ("", ""),
 ("TYPES", ""),
 ("text / number", "Free entry."),
 ("select", "Dropdown from Options. A '-- Custom Input --' choice is added automatically."),
 ("dims", "Dimension boxes. Options = box labels (e.g. W|H|D). Default = values (e.g. 96|36|8). Proof shows 96\"W x 36\"H x 8\"D."),
 ("paint", "Sherwin-Williams / PMS / Custom swatch picker."),
 ("finish", "Options = standard finishes from Finish_Colors, plus 'Custom Paint' which opens the SW / PMS picker."),
 ("vinyl", "Oracal series dropdown (Options = allowed series) + swatch picker from Oracal_Colors."),
 ("db", "Swatch picker from a color tab. Options = LED, COIL, TRIMCAP, ACM, ACRYLIC, PVC or CORO."),
 ("rowmark", "Rowmark swatch picker. Options = series to show (e.g. ADA Alternative)."),
 ("pictogram", "ADA pictogram picker from ADA_Pictograms."),
 ("autoqty", "Letter count calculated from the TEXT field. Options = the letter-height variable to merge into 'QTY / HEIGHT'."),
 ("", ""),
 ("RULES", ""),
 ("Options separator", "Use | between options in the NEW tabs (lets values contain commas). Product_Schema still uses commas."),
 ("Show_If", "Hide a field unless a condition is met, within the same component.  VAR=a|b  (equals one of)   VAR!=a|b  (not)   VAR~=text  (contains).  Join conditions with &."),
 ("Required", "Yes = the proof shows a yellow MISSING flag if the field is empty or a swatch isn't chosen."),
 ("Default_Overrides", "VAR=value; VAR=value   (dims use the | format, e.g. CABINET SIZE=120|48|12)."),
 ("Do not rename", "Tab names and header names are read by Code.gs."),
 ("Proof pages", "Assembled products print as numbered pages (max 2 sections per page). 'Generate Proof Package' saves one PNG per page: product_specs_1.png, product_specs_2.png ..."),
 ("Add Components", "Every assembled product and component has an 'Add Components' checklist. Each checked component adds a section to the proof. 'Custom Proof' in the dropdown starts blank."),
 ("Proof fit", "Large assemblies automatically step down text size to fit the 11 x 8.5 proof."),
 ("", ""),
 ("DETAIL DRAWINGS", ""),
 ("What they do", "Small construction drawings (mounting, letter sections, cabinets, footers, panel finishing) drawn in the bottom-right of the art board when a page's specs match. Up to 3 per page in one column (6 in two). Turn all of them off with Proof_Template > Detail_Drawings = Off, or one at a time with Active = No."),
 ("Components", "Detail_Drawings column. Component_IDs the drawing may appear on, comma separated. Blank = any component that has the field named in Match_Rule."),
 ("Match_Rule", "Same syntax as Show_If (VAR=a|b, VAR!=a|b, VAR~=text, join with &), plus OR between alternatives, e.g.  MOUNTING=Stud Mount - Flush OR BACKER MOUNTING=Stud Mount.  Blank = always (for the listed Components)."),
 ("SVG_Markup", "The drawing itself: plain SVG shapes on a 100 x 100 grid (no <svg> wrapper). {VARIABLE} prints that field's current value, e.g. {EMBED DEPTH} -> 36\". {VARIABLE|text} uses text when the field is blank. Keep labels about 5 units tall."),
 ("Order", "Detail_Drawings column. Lower numbers print first (bottom of the column) when several drawings match one page."),
 ("In the app", "Each product in the Specs panel lists the drawings that matched; uncheck one to leave it off that product's pages."),
 ("", ""),
 ("DESIGN HELP CENTER", ""),
 ("What it does", "The ? button on step 2 (Specs) opens a plain-text list of the design standards and CorelDRAW how-to's that apply to the products in the current proof package. Copy, download or print it."),
 ("Design_Guide", "One row per rule. Section groups rules in the pop-up (sections print in the order they first appear). Order sorts rules. Active = No hides a rule."),
 ("Components / Match_Rule", "Same as Detail_Drawings: Components limits the rule to those Component_IDs (blank = any); Match_Rule uses Show_If syntax with OR. COMPONENT=ID|ID tests the component itself. Both blank = the rule applies to every package."),
 ("Standard / Why / How", "Standard = the rule. Why = the reason (shown to new designers). CorelDRAW_How_To = the steps. {VARIABLE} in Standard prints the spec value, e.g. {RETAINER SIZE}."),
 ("Basis", "SignOS = from our SignOS equipment / material data. Industry = sign industry standard. House = our design department standard."),
 ("", ""),
 ("COVER PAGE + QA CHECKLIST", ""),
 ("Cover page", "Page 1 of every package: logo, customer, project, installation location, project info and the list of every product / component with the sections it includes and its proof pages. Proof_Template: Cover_Page On/Off, Cover_Title."),
 ("QA checklist", "Exported in the zip's QA_Checklist folder (not for the customer): portrait 8.5 x 11 pages listing every spec of every section with a checkbox and initials line, detail drawings to build to, final checks and the QA Manager sign-off, plus qa_checklist.csv for Excel / Sheets. Proof_Template: QA_Checklist On/Off, QA_Final_Checks (separate checks with |)."),
]
rm = sheet("README", ["Item", "Description"], readme, [26, 130], index=0)
for r in range(2, rm.max_row + 1):
    if rm.cell(r, 2).value == "" and rm.cell(r, 1).value:
        rm.cell(r, 1).font = Font(name="Arial", bold=True, size=11, color="3C5F90")
    rm.cell(r, 2).alignment = Alignment(wrap_text=True, vertical="top")

# order tabs: README first, new config tabs right after Product_Schema
order = ["README", "Product_Schema", "Product_Assembly", "Component_Registry", "Component_Schema", "Detail_Drawings", "Design_Guide"]
pos = {id(s): i for i, s in enumerate(wb._sheets)}
wb._sheets.sort(key=lambda s: order.index(s.title) if s.title in order else 100 + pos[id(s)])
wb.active = 0
wb.save(OUT)
print("saved", OUT, wb.sheetnames, "stubs moved:", len(stub_rows), "schema rows:", len(rows), "ref:", len(ref), "rowmark:", len(rm_rows), "pics:", len(pic))
