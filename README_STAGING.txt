SIGNSTUDIO (SIGN PROOF GENERATOR)  -  STAGING 11  (v3.0-staging.11, October 15, 2026)
=============================================================================
A test build for a SEPARATE Google Sheet + Apps Script project. It does not
touch GitHub, the live Apps Script project or the live Google Sheet.


SET UP THE STAGING COPY (once)
-----------------------------------------------------------------------------
1. Open the LIVE Google Sheet > File > Make a copy. Name it e.g.
   "Sign Proof Generator - STAGING". The copy has the same data tabs
   (the source of truth) and its own Apps Script project.
   (Saved projects stay behind: the copy starts its own Saved_Proofs tab
   and its own "Proof Library" folder next to the copied sheet.)
2. In the COPY: Extensions > Apps Script. Paste each file in 1_Apps_Script
   over the file with the same name (Code, ProofLibrary, Updater = script
   files; Index, JavaScript, Stylesheet, Assets = HTML files). Project
   Settings > show appsscript.json > paste appsscript.json.
3. Deploy > New deployment > Web app (Execute as: Me; Who has access: as you
   need) > Deploy, and open that link. Test from this link, not the live one.
4. Reload the copied sheet: its menu reads "Proof Generator (STAGING)".
   "Update from GitHub" is turned OFF there on purpose, so the live release
   can never overwrite the staging code. Import workbook still works.
   The app shows a yellow STAGING tag next to its name.

Next staging rounds: paste only the files listed as changed, save, then
Deploy > Manage deployments > edit > Version: New version (same link).


STAGING 11: WHAT CHANGED SINCE STAGING 10  (paste Index.html, JavaScript.html, Stylesheet.html; macro: ProofPages.bas)
-----------------------------------------------------------------------------
Layout
- Design and Production tabs share one layout: 30% menu | 60% proof pages |
  10% Pages + Layers. Specs stay in one column.
- Pages and Layers each take half of the right column, with dark headings
  like "Add products & components" and a fold arrow: fold one to give the
  other the whole column.
- Page bars above each proof use the blue-gray of the products window.

Step guide and exports
- Step guide: red with yellow on the Design tab, purple with white on the
  Production tab. Design | Production switch in the top bar.
- "Approve and export" (step 3) opens a review window: large previews of
  every page exactly as it will be exported, the page count, how many
  MISSING tags are left, and one big button: Export Design Package (red) or
  Export Production Package (purple). The Export button is gone from the
  top bar; the combined export is gone.
- Design package (zip): SVG/ and PNG/ folders + package_info.txt (the
  CorelDRAW macro names the pages from it).
- Production package (zip): SVG/ and PNG/ folders (QA sheets, production
  proofs, snapshot, department sheets) + ONE PDF with every page.

Cover page
- Built into the Design tab as page 1 (new projects start with it):
  "Remove cover page" on its bar, "+ Add cover page" to bring it back. It
  can take images and measurements like any page. No cover question at
  export. Projects saved before this open without a cover.

Watermark
- True 2-5% opacity (3% default; the sheet setting is limited to 2-5).
  Dark text with a faint light edge, so it marks light and dark artwork.
  Design proof only, cropped to the artboard; production pages have none.

Production
- No design ticket # anywhere in the production package (sheets or file
  names). Files are named Customer - Project.
- Production proofs: border half as thick, no white labels on it, larger
  table (up to about 20% bigger) and a larger artwork area.
- QA sheet in production purple; every table header reads
  "CUSTOMER - PRODUCT"; blank WORK ORDER # box at the top.
- Production snapshot: larger text for the shop floor (bigger title, tiles,
  one column of large color swatches, materials with where they go) and a
  blank WORK ORDER # box.
- Department sheets: no ticket #.

Fixes
- With an image selected, clicking a page-bar button (e.g. + Add image)
  was lost; it works now.

CorelDRAW macro (ProofPages.bas)
- Import Production Proofs reads the SVG folder of the new Production
  package (older packages still work); QA pages are named QA SHEET 1, 2...


STAGING 10: WHAT CHANGED SINCE STAGING 9  (paste Index.html, JavaScript.html, Stylesheet.html; macro: ProofPages.bas)
-----------------------------------------------------------------------------
Navigation
- Back chevron left of the logo (Production > Design > Home). Name: SignStudio.
- Red step guide under the top bar, every step clickable:
    Design tab:      Create project > Design proof > Approve and export
    Production tab:  Create project > Production proof > Approve and export
  The current step is yellow; finished steps get a white check. "Approve and
  export" exports the package of the tab you are in (design: asks about the
  cover page first) and ticks once it is done. Design / Production switch
  in the top bar.
- "Saved projects" button is in the top bar on the home screen only.

Home
- Clean two-card layout: "Create a new project" (red) with the job info
  fields + Create project, and "Open a saved project" (blue), which opens the
  same Saved projects popup. The saved list is no longer on the page.

Job info / saving
- Job info moved out of the Design sidebar into "Save Project" (the Save
  button), with every field (sub-customer, location, sales, designer,
  invoice, ticket, dates, file location, notes).
- "Draft saved 13:31" text is now light gray/white on the dark bar.

Design tab
- Layout: wide specs menu on the left (specs flow into 2+ columns), proof
  pages in the middle, Pages + Layers panel on the far right.
- Pages panel: live thumbnails of every page (Proof Summary stays last);
  click to jump, drag to reorder. The order is saved with the project.
- Layers panel: the selected page's images (click to select, x to remove)
  and measurements (edit the value, x to remove). Images and measurements
  always sit UNDER the spec table and the watermark.
- Page bar: "+ Add image" and "+ Add measurement" are back; click the bar to
  select the page; drop or Ctrl+V a screenshot onto it. No download buttons.
- Images: click one to get a bounding box; drag to move, drag a corner to
  scale (keeps proportions). Delete key removes the selected image.
- Click any cell of a spec table on a page: the specs menu scrolls to that
  field and flashes a red outline around it.
- "+ Add Blank Page" is back on each product.
- The "New page" checkbox is replaced by a small connector between section
  boxes: "Same page" / "New page" - click to split or combine.
- "+ Add Color" on EVERY color field (vinyl, color lists, paint, finish,
  database swatches, Rowmark): each extra color prints as its own row.
- Custom color is one field (like the Sherwin Williams / Pantone picker)
  with a CMYK | RGB | HEX switch inside it (CMYK by default). The other
  values are calculated, and the closest Sherwin-Williams / Pantone
  (and Oracal on vinyl fields) matches still show under it.

Production tab
- Production proofs have their own "+ Add image" / "+ Add measurement",
  bounding boxes and Pages + Layers panel. These images are separate from
  the design pages (each phase shows different images).
- Table tab reads "CUSTOMER NAME - PRODUCT" (e.g. CENTER PARC - PVC PANEL);
  the customer name no longer sits beside the table.
- Color chart replaced by the PRODUCTION SNAPSHOT: large, clean page with
  the five departments (Vinyl, Metal fabrication, CNC / routing,
  Electrical, Paint: involved or not), every color with its swatch and
  what it is for, and every material.
- A DEPARTMENT SHEET for each department involved: what it needs (product /
  section, spec, value, done box), notes lines and a supervisor sign-off
  with date and a "complete" box.
- Left menu trimmed (no description, export button or "later" box).

Export menu
- 1 Design package, 2 Production package. The combined "export all" was
  removed: the two phases are exported separately.

CorelDRAW macro (ProofPages.bas)
- Page names for the new files: "PRODUCTION SNAPSHOT" and
  "<DEPARTMENT> DEPARTMENT". Re-import it (File > Import in the VBA editor)
  if you use Import Production Proofs.


STAGING 9: WHAT CHANGED SINCE STAGING 8  (paste Index.html, JavaScript.html, Stylesheet.html, Assets.html)
-----------------------------------------------------------------------------
- Top bar is a dark charcoal hub (#2B2F36) that stands apart from the pages
  below: The Sign Store logo (small, transparent) replaces the red square,
  "Proof Generator" in white, white pill for the open tab, light buttons on
  dark, red Save, white Export.
  The logo is stored in Assets.html (PROOF_ASSETS.navLogo), so Assets.html
  must be pasted this time.


STAGING 8: WHAT CHANGED SINCE STAGING 7  (paste JavaScript.html, Stylesheet.html)
-----------------------------------------------------------------------------
- Under every section: "+ Add More Info" (was "+ Add Row"; also on custom
  tables), "+ Add Color" and "+ Add Special Notes" on one row - solid light
  gray, no outline until hovered, smaller than and a different color from
  the "+ Add Another ..." button. "+ Add Special Notes" turns light gold while
  notes are on; click it again to turn them off.
- The "Add products & components" list sits on a light blue-gray
  background under its dark title bar, so it reads apart from the specs.
- Scrollbars: the product list's own scrollbar is thin and quiet (light
  blue-gray, no arrows); the whole left panel's is a slim neutral gray, so the
  two no longer clash.


STAGING 7: WHAT CHANGED SINCE STAGING 6  (paste JavaScript.html)
-----------------------------------------------------------------------------
- Custom products and their components start with NO name ("Name this
  product" / "Name this component" placeholders). "Custom Product" and
  "Custom Component" never print. Until named, the proof shows a yellow
  "MISSING: PRODUCT NAME" tag on the product tab and "MISSING: COMPONENT
  NAME" on component header rows (a single unnamed component gets no header
  row), each with an editable text box underneath in the SVG. Name them in
  the header / Product Name box and in each component's title field.
  Projects saved with the old default names show the MISSING tags too, until
  renamed.


STAGING 6: WHAT CHANGED SINCE STAGING 5  (paste Index.html, JavaScript.html, Stylesheet.html)
-----------------------------------------------------------------------------
- Save window: the project's name is built from Ticket #, Customer and
  Project ("47601 - Center Parc - Monument"). Those three fields are now right
  in the Save window (the cursor starts in the first empty one); typing there
  fills the same Job info fields. No more "Untitled proof".


STAGING 5: WHAT CHANGED SINCE STAGING 4  (paste JavaScript.html, Stylesheet.html)
-----------------------------------------------------------------------------
- "+ Add Row" on every product / component section (next to "+ Add Color"):
  a row of your own for that table - a title (e.g. PERMIT #), a value and the
  table column (Col 1, Col 2 ...; last column by default). A title with no
  value prints a yellow MISSING tag. x removes it. Saved with the project and
  copied by "+ Add Another ...".
- Custom products ("Build a custom table"): the boxes under the product name
  are CUSTOM COMPONENTS - "Custom Component", "+ Add Custom Component" (was
  "+ Add Section"), "+ Add Another Custom Component". A single component with
  its default name prints no extra header row on the table. Custom tables
  keep their own "+ Add Row" (no second one). The custom product's title in
  its header bar is editable (click it and type); it stays in sync with the
  Product Name box.
- Special notes is now a plain, subtle checkbox (no yellow box); checking it
  still shows the notes field and prints the gold SPECIAL NOTES column.


STAGING 4: WHAT CHANGED SINCE STAGING 3  (paste Index.html, JavaScript.html, Stylesheet.html)
-----------------------------------------------------------------------------
- Design proof sidebar: larger text (labels 11 pt-units, values bold), fields
  spaced 20 apart, 2-line installation location, 3-line file location; the
  description area is shorter (10 lines) with larger text. Approval labels,
  legal and ETL text are a bit larger too.
- SVG export: every MISSING tag has an empty editable text box under it, and
  every description line is its own text box (filled or empty), ready to type
  into in CorelDRAW.
- Spec tables: larger value and label text, darker labels and lines for print.
  Tables still shrink when a page has a lot of information.
- Production proofs: the customer / sub-customer name is right-aligned on the
  same row as the product tab, above the table.
- QA sheet: two columns, larger text; the final checks / sign-off box spans
  the full width at the bottom of the last page.
- Picking a product or component no longer scrolls down to its specs, so
  several can be picked in a row.
- "Add products & components" bar is dark with a big round arrow and
  "Hide list" / "Show list", so it is clear it opens and closes.


STAGING 3: WHAT CHANGED SINCE STAGING 2  (paste JavaScript.html)
-----------------------------------------------------------------------------
- "+ Add Color" on EVERY product / component section (and custom tables),
  under its specs. Each additional color has:
    What it is for   e.g. "Accent stripe", "Logo red" (printed as the row
                     label; blank = "ADDITIONAL COLOR 1")
    Color            Sherwin Williams, PMS, Oracal vinyl (every series,
                     searchable) or a custom CMYK / RGB color
  Each prints as its own row in the section's spec table (last column), on
  the QA sheet and on the production color chart. A color not picked yet
  prints as a yellow MISSING tag. [x] Remove deletes it. Saved with the
  project; "+ Add Another ..." copies them with the section.
  (The existing "+ Add Color" on vinyl fields still works as before.)


STAGING 2: WHAT CHANGED SINCE STAGING 1  (paste Index.html and JavaScript.html)
-----------------------------------------------------------------------------
- Tabs read "Design" and "Production" (no numbers).
- Export menu: Design proof and Production package only (no data-table SVGs).
- Production proofs: no inner border, no PRODUCTION title at the top. The
  artboard fills the page inside a thick (0.28") purple border; the tables
  are drawn larger when there is room, with the customer / sub-customer
  name just above them. White labels on the bottom border:
  "PRODUCTION PROOF 1 / 4" (left) and "TICKET 47601 - MONUMENT SIGNS 2/3"
  (right). The color chart page uses the same border and labels.
  (The production artboard is now bigger than the design proof's, so art
  copied from the design file needs scaling / moving to fit.)


WHAT CHANGED IN STAGING 1
-----------------------------------------------------------------------------
Start screen   Unchanged: Create a new project / open a saved project.

Two tabs       1 Design and 2 Production. The separate Tables tab is gone.

Design tab     Left: search, products & components, and the specs below
               (same sidebar as the v3.0 Tables tab).
               Center: the proof pages, built live as specs are keyed in.
               Right: Job info.
               Removed: "+ Add Blank Page", Add image (paste / drop),
               Measure. Pages show the blank artboard with the watermark.
               The sidebar title reads DESIGN PROOF (instead of SALES PROOF).
               To use another title, set Title in the Proof_Template tab.

Export menu    Design proof        SVG only, ready for CorelDRAW:
                                   "Ticket - Customer - Project - Design Proof.zip"
                                   with  47601 - p01.svg ... + package_info.txt.
                                   Asks first: "Add a cover page?"
                                   Cover page = the proof template with no
                                   tables (blank artboard + watermark, job info
                                   sidebar, customer approval, ETL, logo). It
                                   is page 1; page numbers count it. The Proof
                                   Summary is still the last page.
               Production package  QA sheet + production proofs + color chart.

Production tab QA sheet (as before) + PRODUCTION PROOFS + COLOR CHART.
               Production proof = the same pages as the Design tab, but only
               the artboard and the tables: no customer approval, sidebar,
               ETL or logo, no watermark. PRODUCTION at the top left, the
               customer / sub-customer at the top right, the whole page
               outlined in purple, tables in purple (instead of black).
               Color chart (always included, its own page): every color in
               the job with its swatch, name / code / HEX and what it is for
               (product, section and field). Colors still to be picked show
               as yellow MISSING.
               "Spec tables to print" and "Proof pages (reference copy)" are
               replaced by the production proofs.

Production zip "Ticket - Customer - Project - Production.zip":
                 QA/SVG, QA/PNG, PRINT - 47601 - QA sheet.pdf, 47601 - QA sheet.csv
                 Production proofs/SVG and /PNG  (prod01 ... + color chart last)
                 PRINT - 47601 - Production proofs.pdf  (landscape letter)


CORELDRAW MACRO  (2_CorelDRAW_Macro\ProofPages.bas, refreshed)
-----------------------------------------------------------------------------
Install: in CorelDRAW, Alt+F11 (VBA editor) > GlobalMacros > right-click >
Import File... > ProofPages.bas (remove the old ProofPages module first).

ImportDesignProof       Unzip the Design Proof zip (right-click > Extract All),
                        run the macro, pick the unzipped folder. It creates ONE
                        new CorelDRAW file with one 11 x 8.5 page per SVG
                        (cover if exported, every proof page, Proof Summary),
                        in order, each page named (COVER, MONUMENT SIGNS 1/3,
                        PROOF SUMMARY ...), and saves it as
                            47601 - Center Parc.cdr
                        in the job's File Location folder when that folder
                        exists on the computer, otherwise in the unzipped
                        folder. You can edit the name / folder before saving.
ImportProductionProofs  Same for the Production zip: production proofs + color
                        chart into "47601 - Center Parc - PRODUCTION.cdr".


SAMPLES  (3_Samples)
-----------------------------------------------------------------------------
Sample - Design Proof (with cover).zip, Sample - Production.zip, and
screenshots of the Design and Production tabs.


NOT CHANGED
-----------------------------------------------------------------------------
Sheet data and tabs, Code.gs, ProofLibrary.gs (saving / opening projects),
field menu (TBD by Production / MISSING / remove), autosave drafts, the
QA sheet itself. Projects saved by the live app open here too (any images,
measurement lines or blank pages saved in them are not shown in this build).
