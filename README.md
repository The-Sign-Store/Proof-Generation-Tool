# SignStudio (Sign Proof Generator)

**Current version: v4.8** · The Sign Store Online, Inc. · Design Department

The Sign Proof Generator is a Google Apps Script web app that builds complete, print-ready sign proof packages from a Google Sheet. Designers pick products and components and fill in the specs. They add customer and project info, then download one zip with these files:

- a branded cover page
- 11" × 8.5" proof sheets
- a QA checklist for production

Each page comes as an editable SVG (for CorelDRAW or Illustrator) and as a 300 ppi JPG.

---

## Features

**v4.0 (SignStudio):** a home screen and two phases, guided by a 3-step bar under the top menu (red on Design, purple on Production):

1. **Create project:** type the job info and create the project, or open a saved project or draft (the Saved projects popup).
2. **Design proof / Production proof:** a 30% specs menu, the proof pages in the middle (60%) and a Pages + Layers panel on the right (10%). Pages show live thumbnails (drag to reorder); Layers lists the selected page's images and measurements. Images get bounding boxes (drag, resize by the corners) and always sit under the spec table and the watermark. Click any cell of a table on a page to jump to its field. The design proof starts with a cover page (Remove / Add back). Production proofs have their own images.
3. **Approve and export:** large previews of every page exactly as it will be exported, step-by-step instructions for this job (where to save, the Freshdesk ticket link, a hand-off note to copy into the ticket), then one button: **Export Design Package** (SVG/ + JPG/) or **Export Production Package** (SVG/ + JPG/ + one PDF: production proofs, Production Snapshot with department tasks, QA sheet).

Job info is edited in **Save Project**. Production pages never show the design ticket #.

### Proof builder
- **Data-driven:** every product, component, field, option, default, rule, drawing and design standard lives in the Google Sheet. You change the sheet, not the code.
- **19 products and 26 modular components:** pole signs, channel letters, cloud signs, cabinets, monuments, banners, decals, ADA and more. You can mix products and stand-alone components in one package.
- **Conditional specs:** `Show_If` rules, required fields, and live color and material pickers. The pickers cover Oracal, Sherwin-Williams, PMS, ACM, acrylic, LED, trim cap and ADA pictograms.
- **26 vector detail drawings:** mounting, letter construction, cabinets, footers/poles and panel finishing. Each drawing is added automatically when its specs match, with live values such as embed depth, return depth and trim cap.
- **Editable section names:** rename any section, e.g. "Acrylic 2" to "Front Menu". The new name carries through to the proof sheet, cover contents and QA checklist.
- **Special notes per section:** check **Add Special Notes** on any section and type. The notes print in a gold-edged **SPECIAL NOTES** column beside that section's table on the proof sheet. Unchecking hides them but keeps the text.
- **Custom colors:** any color field takes a custom color by name plus CMYK or RGB; the other set is calculated and marked "(approx.)".
- **Page control:** a "New page" toggle per section, and blank pages per product (sidebar and watermark, empty art board, editable title).
- **Mixed letter sizes:** "+ Add Letters" on channel letters adds a Quantity / Letter Height / Text line inside the section; "+ Add Another ..." copies the whole section.
- **Calculated fields:** e.g. EMC display size from 9.45" modules, and overall vs. cabinet depth (modules extend past the cabinet).
- **Build Custom Table:** a custom product whose spec table you build on screen: type each row's title and description, or make the description a swatch, material, finish, size or pictogram picker; add sections, existing components and detail drawings.
- **Measurement lines:** draw red dimension lines over images on any page, type the value in inches, move and resize them; they export as editable SVG.
- **Proof Library:** Save stores the whole package in a shared Drive folder (every value, custom table, color, note, image and measurement); reopen any revision from **Saved proofs** and keep editing. Every save is a new revision.
- **Material-style interface:** tonal surfaces, Roboto, a color key that filters the dashboard by sign family.
- **Color matching:** a custom color typed as CMYK, RGB or HEX lists its closest Sherwin-Williams, Pantone and Oracal colors (Delta E 2000); click one to use it. Every swatch library is searchable.
- **Single-page SVG:** download any one page (cover, proof or QA), or just a page's spec table, without exporting the whole package.
- **Self-updating sheet:** a **Proof Generator** menu updates the sheet's data tabs in place from the latest GitHub release (with backups, keeping your Proof_Template wording) or from an uploaded workbook (then trashes the .xlsx), and updates the Apps Script code and web app when the Apps Script API is on.
- **Artwork placement:** add a screenshot or JPEG to any proof page with a button, by dropping it, or by pasting with Ctrl+V. You can move and resize it, and it is embedded in the SVG and JPG exports.
- **Missing info flagged:** blank fields print as yellow **MISSING** tags. In the SVG, each tag has an empty matching text box underneath, ready to type in.

### Design Help Center
- A **?** button opens the design department's procedures and CorelDRAW how-to's. The pop-up shows only the standards for the products in the current package.
- 91 standards in all. Examples: convert cut-vinyl text to curves with a hairline black outline, show clear glass in baby blue, show tinted glass in blue-grey.
- You can copy, download as .txt, or print the guide.

### Cover page and QA checklist
- **Cover page:** company logo, customer (plus an optional sub-customer), project, project info, project notes and the company contact line.
- **Package Contents table** (on the cover):
  - each product, with its sections as indented sub-rows
  - quantities in bold red, taken from each section's Quantity field, e.g. **(x2)** Main Menu Boards
  - page references written as "Page 2", or "Pages 3 - 5" for a range
- **QA checklist:**
  - every spec, with OK / INIT boxes
  - a checkbox on each product header
  - the detail drawings
  - a red-outlined **Final Checks** section with QA Manager sign-off and 10 note lines
- The checklist is exported as SVG, PNG, CSV and one multi-page **PRINT** PDF.

### Export
```
47391 - Macon Housing Authority - Central City Apartments - Design Proof.zip
├── SVG/                      p01 = cover, p02… = proof pages (editable)
└── JPG/                      same pages, 300 ppi

47391 - … - Production.zip
├── SVG/                      production proofs, snapshot, QA sheet (editable)
├── JPG/                      same pages, 300 ppi
└── … - Production package.pdf
```
- **Where to save:** `P:\[first letter]\[customer]\[ticket] - [customer] - [project]\Proof` (design) or `…\Production` (production). The Approve and export window shows the exact path for the job.
- **File names:** `Ticket - Customer - [Sub-Customer -] Project - pNN`. Names are Windows-safe and shortened to 80 characters if needed.
- **Watermark:** a flat 2% gray image on its own layer. **Text:** plain UTF-8 Arial, with no entity codes, so it imports cleanly into CorelDRAW.

---

## Repository layout
```
1_Google_Sheet/      Sign_Proof_Specifications_App_Data.xlsx  (the database)
2_Apps_Script/       Code.gs, ProofLibrary.gs, Updater.gs, Index.html, Stylesheet.html, JavaScript.html,
                     Assets.html, appsscript.json
3_Samples/           sample export zip, cover, proof pages (incl. special notes),
                     QA pages and PDF
4_Source_Builders/   Python scripts that rebuild the workbook (optional)
README.md            this page: overview + changelog
README.txt           full setup guide
```

## Setup
1. Upload the `.xlsx` to Google Drive, then choose **File › Save as Google Sheets**.
2. In the sheet, open **Extensions › Apps Script**. Create `Code`, `ProofLibrary`, `Updater` (script files), `Index`, `Stylesheet`, `JavaScript` and `Assets` (HTML files), named exactly as shown, and paste in the matching files. Approve the Google Drive permission when asked; saved proofs go to a **Proof Library** folder next to the sheet.
3. Project Settings › show `appsscript.json`, and paste the manifest (permissions and the Drive service). Turn on the Apps Script API once at script.google.com/home/usersettings for automatic code updates. Check that the last line of `Assets` is `PROOF_ASSETS.loaded = true;`.
4. Choose **Deploy › New deployment › Web app** with Execute as: *Me*. Use **Test deployments** (the `/dev` link) while you are testing.

`README.txt` has the full step-by-step guide, troubleshooting and the sheet reference.

> **Apps Script editing rules:** never type `<?` or `?>` in an HTML file, and never put `//` inside a JavaScript string. Apps Script mangles both, and the page will hang on "Loading…".

## Tech
Google Apps Script (V8) · HtmlService · vanilla JavaScript · SVG (1 unit = 0.01") · Canvas JPEG rendering · an in-browser PDF writer · JSZip · Python and openpyxl (workbook builders)

The full version history is in the [Changelog](#changelog) below.

---

## Changelog

All notable changes, newest first.

### [4.8] – 2026-10-16
#### Added
- **Freshdesk inside Approve and export.** The right half now shows the job's ticket through the Freshdesk API: number, subject, status, requester, assigned agent and the latest replies / notes (private notes highlighted), with **Open in Freshdesk** for the full ticket.
  - **Add note to ticket** (on after the export) posts the hand-off note as a private note headed "Sent from SignStudio by {designer}", attaches the exported JPGs (production: the JPGs and the package PDF) and notifies the salesperson when they match a Freshdesk agent.
  - Notes show the API key owner as the author. Over ~18 MB the pages are attached smaller (and the PDF left for you to attach by hand).
  - **Setup (once):** in Apps Script open **Project Settings › Script properties** and add `FRESHDESK_API_KEY` with the Freshdesk API key. Until then the panel explains this and keeps the **Open Ticket** button. The key stays on the server: it is never sent to the browser or saved to GitHub.
#### Changed
- **Job info window** is wider with two columns, so every field fits without scrolling (even on a 1366 × 768 screen).

---

### [4.7.1] – 2026-10-16
#### Changed
- **Approve and export** is now a split screen under a full-width top bar (package, customer · project, page count; red X on design, purple on production; it stays open until the X):
  - **Left: the steps.** Design: 1 Export and save (**Copy path**, then **Export Design Proof Package** in the step: paste the path into the Save window), 2 Unzip and file the JPGs to `P:\JPEGS`, 3 Notify the salesperson (the note with **Copy note** inside it, and every page as a JPG with **Copy image** / drag). Production: the same without the JPEG step, plus the .cdr reminder and the package PDF.
  - **Right: the Freshdesk ticket.** **Open Ticket** opens it in its own window over the right half (Freshdesk cannot be shown inside another app).
  - No ticket # yet: a bar asks for it and Export stays off until it is added.
  - The production note lists products work-order style: `Qty: 1 - Product` then its specs joined with " / " (open items as `( LABEL )`).
- **Every export saves a new version** ("Exported the design / production package").
- **Design JPGs are named** `Ticket - Customer - Project - pNN.jpg`.
- **Edit Job Info** (top bar) opens job info in its own window; **Save Project** is just the version, a job-info check and a big Save button.
- **Layers:** Ctrl+click picks one at a time, Shift+click a run; a picked group gets one box whose corners scale every image and measurement in it together; copy / paste keeps each image's exact size and spot on any page.
- A spinning loader while SignStudio starts.

#### Fixed
- Page images and an export could run at the same time and make the export fail.

---

### [4.7] – 2026-10-16
#### Added
- **Layers: select and group.** Ctrl+click (or Shift+click) picks several images and measurements in the Layers panel; **Group** (Ctrl+G) nests them as "Group 1"… and dragging any of them on the page moves the whole group. **Ungroup** (Ctrl+Shift+G). Clicking a group selects all of it. Groups are saved with the project.
- **Copy / paste layers** between any pages, Design or Production: pick layers, **Copy** (Ctrl+C), click another page, **Paste** (Ctrl+V). Pasted layers keep their spot and their groups; a paste over an identical layer is nudged so it does not hide it.
- **One measurement box can be MISSING:** hover a W / H / D box and click **?** to flag just that measurement (blank boxes on a required size are flagged one by one). It prints as `132"W x [MISSING H] x 16"D` on the proof, QA sheet and snapshot, and is listed in Missing information as e.g. "BASE SIZE (H)"; the answer fills only that box on the production pages.

#### Fixed
- **Measurements now show in Layers** (and can be typed there) right after they are drawn, on the Design and Production tabs.

#### Changed
- The TBD / MISSING key in Missing information sits in a gray bubble with more space below it; "0 of 0 answered" is no longer shown.

---

### [4.6.1] – 2026-10-16
#### Fixed
- **The app would not start after v4.6** ("Could not start the Proof Generator … Invalid or unexpected token"): a `//` inside a JavaScript string, which Apps Script cuts off. The build now checks every file for `//` in strings and `<?` / `?>` before release.

---

### [4.6] – 2026-10-16
#### Changed
- **Missing information** on the Production tab replaces "TBD by Production": every field marked TBD by Production (purple TBD tag) or left blank (yellow MISSING tag) has an answer box, plus the job info still missing with a Fill in job info button. Answers print on the production pages only; the design proof keeps its TBD and MISSING tags. Exporting the production package no longer asks about missing job info.
- **Department tasks on the Production Snapshot:** the separate department sheets (with their supervisor sign-off) are gone. The snapshot lists colors and materials, then one concise task table per department (one row per product section) for the pre-production coordinator to check. The department tiles are gone; a big job continues on a second snapshot page.
- **Approve and export instructions:** five steps with icons, filled in from the job info: who the package goes to, the exact folder to save in (`P:\[letter]\[customer]\[ticket] - [customer] - [project]\Proof` or `\Production`), the Freshdesk ticket link, and a hand-off note with a **Copy note** button to paste into the ticket's note (design: for the salesperson to send to the customer; production: for the salesperson to create the work order).
- **JPG instead of PNG:** the design package is SVG/ + JPG/; the production package is SVG/ + JPG/ + one PDF.

#### Removed
- **Shop info** (work order #, due date, install date) on the Production tab and on every production page, QA sheet and snapshot.
- The description under "Production package".
- The **CorelDRAW macro** (`ProofPages_CorelDRAW_Macro.bas`) and the `package_info.txt` it read.

---

### [4.5] – 2026-10-15
#### Added
- **Magnetics** (Vinyl family): vehicle and indoor magnets. QTY (1 pair default), dimensions, application (vehicle door / tailgate / indoor), substrate (30 mil vehicle, 20 / 15 mil indoor), magnet face (white / black), graphic (Arlon 4500GLX mounted print, direct print or Oracal 751 cut vinyl), overlaminate and full color for printed graphics, vinyl color for cut vinyl, corners (1" rounded default). Every magnet spec goes to the Vinyl department sheet.
- Design help rules M01-M03: steel only and flat area, 30 mil and rounded corners for vehicles, customer care.

#### Data
- Component_Registry, Component_Schema, Product_Assembly and Design_Guide gain the Magnetics rows (source: `4_Source_Builders/magnetics.py`). SignOS_Ref is blank until a magnetic sheeting SKU is set up.

---

### [4.4] – 2026-10-15
#### Changed
- **Shop info on the Production tab:** work order #, due date and install date, typed once. Printed on every production proof (a strip at the top right), the QA sheet (work order # box, QA due / ship date), the Production Snapshot and the department sheets. Blank fields print as empty boxes. The work order # is searchable in Saved projects.
- **Answer "TBD by Production" fields on the Production tab:** every TBD field is listed with an answer box; answers print on the production proofs, QA sheet, snapshot and department sheets. The design proof keeps "TBD by Production".
- Shop info and answers are saved with the project.

#### Data
- No changes to the data tabs or Proof_Template.

---

### [4.3] – 2026-10-15
#### Changed
- **Next button** under Pages + Layers (red with yellow text on Design, purple with white on Production) opens Approve and export; the review window has **Back to proof pages**.
- **Search every project** in Saved projects by ticket #, customer, project, product, component (section) names and designer initials; several words narrow it down (e.g. `47601 cabinet`). Unsaved drafts are searchable the same way. Projects and drafts saved before v4.3 are indexed automatically the first time Saved projects is opened (new **Search** column on the Saved_Proofs tab).
- **QA sheet comes last** on the Production tab, in the review window, in the PDF and in the export folders (after the production proofs, snapshot and department sheets).

#### Data
- No changes to the data tabs or Proof_Template.

---

### [4.2] – 2026-10-15
#### Changed
- Home screen: wider, four-column job info form that fits on one screen, more space under the top bar, and a copyright line pinned to the bottom (Property of The Sign Store, current year, designed by Evan Zebley and Victoria Hawkins).

#### Data
- No changes to the data tabs or Proof_Template.

---

### [4.1] – 2026-10-15
#### Changed
- The step guide (Create project > Design / Production proof > Approve and export) is hidden on the home screen; it shows once a project is created or opened.

#### Data
- No changes to the data tabs or Proof_Template.

---

### [4.0] – 2026-10-15
#### Changed
- **SignStudio:** new home screen (create a project with job info, or open a saved one), back chevron, and a clickable 3-step guide: Create project > Design proof / Production proof > Approve and export (red and yellow on Design, purple and white on Production).
- **Job info lives in Save Project** (the Save button), not in a sidebar.
- **Layout on both tabs:** 30% specs menu (one column) | 60% proof pages | 10% Pages + Layers (each half folds open or closed).
- **Pages panel:** live thumbnails; drag to reorder (saved with the project). **Layers panel:** images and measurements of the selected page.
- **Images and measurements are back** on design and production pages (separate per phase): + Add image, paste or drop, bounding box with corner handles, + Add measurement. They sit under the spec table and the watermark.
- **Click a table cell on a page** to scroll to that field on the left (it flashes red).
- **Cover page built into the Design tab** (page 1, Remove cover page / + Add cover page); no cover question at export. Older saved projects open without a cover.
- **+ Add Blank Page** is back; the "New page" checkbox became a Same page / New page connector between sections.
- **+ Add Color on every color field**; custom colors are one field with a CMYK / RGB / HEX switch (closest Sherwin-Williams / Pantone / Oracal matches below).
- **Approve and export review window** replaces the Export button: large previews, missing-tag count, one big export button.
- **Design package:** SVG/ and PNG/ folders (+ package_info.txt for the CorelDRAW macro). **Production package:** SVG/ and PNG/ folders + one PDF with every page.
- **Production proofs:** half-width purple border with no labels on it, larger tables and artwork area, table tabs read CUSTOMER - PRODUCT.
- **QA sheet in production purple**, CUSTOMER - PRODUCT headers, blank WORK ORDER # box.
- **Production Snapshot** replaces the color chart: departments involved (Vinyl, Metal fabrication, CNC / routing, Electrical, Paint), every color and material in large text, WORK ORDER # box. **Department sheets** for each department involved, with notes and a supervisor sign-off.
- **No design ticket #** anywhere in the production package (sheets or file names).
- **Watermark** at true 2-5% opacity (Proof_Template Watermark_Opacity, 3% default), design proof only, cropped to the artboard.
- CorelDRAW macro: Import Production Proofs reads the new SVG/ folder (older packages still work).

#### Data
- No changes to the data tabs or Proof_Template.

---

### [3.0] – 2026-10-15
#### Changed
- **New layout in three tabs: 1 · Tables, 2 · Proof pages, 3 · Production.** The working panel is always on the left: products and specs on Tables, job info on Proof pages, package options on Production.
- **Start screen:** "Create a new project" or open a saved project or draft (search included). The Sign Proof Generator name in the top bar returns to it.
- **Tables tab:** add and remove products and components from the "Add products & components" list at the top of the left panel (search plus a family filter). Each spec table is drawn live on the right while you type.
- **Every field has a ⋮ menu:** use the default options, type a custom answer, **Mark TBD by Production** (solid purple on the proof and QA sheet), **Leave blank** (yellow MISSING tag), or **Remove from this table** (Restore brings it back).
- **Letters (channel, halo, PVC routed, monument letters, cloud signs):** a TEXT field (what the letters say) and a separate **QTY & SIZES** field, e.g. `10 @ 18", 4 @ 12"`. Projects saved before v3.0 are converted when opened (quantity, height and extra letter lines become one QTY & SIZES entry).
- **Export button in the top bar** (right of Save): data tables as one SVG or one SVG per table (zip), the proof package, or the production package.
- **The cover is now the Proof Summary, always the last page** of the proof package, so customers see the proof pages first.
- **Production package:** the QA sheet (SVG, PNG, print PDF, CSV) plus each spec table to print; proof page PNGs optional. Always available. Department sheets come later.
- Cleaner look with the Figtree font.

#### Removed
- Project statuses (Draft, Sent, Approved and so on). The project manager tracks status.
- The Design help button and detail drawings, for now.
- The floating export box.


---

### [2.3.2] – 2026-10-14
#### Fixed
- **QA checklist files no longer fail to unpack on Windows ("Error 0x80010135: Path too long").** Every file in the zip repeated the full job name, which was already in the folder name, so the QA_Checklist files (the PDF, PNGs and SVGs) could pass Windows' 260-character path limit, especially when copied straight out of the zip in File Explorer.

#### Changed
- **Shorter file names inside the zip:** files now start with the ticket number (or the first words of the job name when there is no ticket), e.g. `PNG/47601 - p02.png`, `QA_Checklist/PRINT - 47601 - QA checklist.pdf`. The zip itself keeps the full name, e.g. `47601 - Center Parc Covington - Monument Cabinet Replacement.zip`, and so does the folder Windows unpacks it to. The CorelDRAW macro works unchanged (it reads the `- p02` / `- qa01` endings and the page names in package_info.txt).
- Download page / Download table use the same short names as the zip (`47601 - p02.svg`, `47601 - p02 - table.svg`).

---

### [2.3.1] – 2026-10-14
#### Fixed
- **A tab left open across an update no longer shows "Could not start the Proof Generator".** That screen is now only for real start-up failures. An error after the app is running shows a small notice at the bottom instead, and the app stays usable.
- **Stale tabs stop autosaving cleanly.** If an open tab's copy of the app no longer matches the server (for example after an update), autosave stops and the notice asks you to reload, instead of throwing a saveDraft error.

#### Added
- **New-version notice:** open tabs check every 15 minutes, and when you come back to the tab, whether a newer version is live. If one is, a notice offers **Reload now**: your work is saved as a draft first, and the reloaded tab offers to restore it.
- New server function getLiveVersion (Updater), cached for 10 minutes; Update from GitHub clears the cache so tabs see the new version at their next check.

---

### [2.3] – 2026-10-13
#### Added
- **Proof Generator menu in the Google Sheet** (new Apps Script file **Updater**): **Update from GitHub**, **Import workbook from Drive** and **About this version** (code, sheet data and latest release versions).
- **Update from GitHub:** reads the latest release and updates **this** sheet in place; no new spreadsheet. It backs up Component_Registry, Component_Schema, Product_Assembly, Detail_Drawings and Design_Guide as hidden "(backup ...)" tabs (the last 3 per tab), then replaces them with the release's rows. These five tabs are release-managed: edit them through a release, not by hand.
- **Proof_Template merge:** new keys are added, and your own wording is kept. A value you never changed that the release updated (e.g. DESIGN PROOF to SALES PROOF) is listed for you to accept or skip.
- **Code updates itself** (when the Apps Script API is on for your Google account, a one-time switch): changed files are written into the project, saved as a new script version, and the web app deployment moves to it, with the same link. If Google blocks it, the summary lists exactly which files changed since your version and how to paste them.
- **Import workbook from Drive:** finds the newest Sign_Proof_Specifications_App_Data .xlsx in your Drive (or pick from a list), converts it in the background and updates the tabs the same way. Afterwards the .xlsx and its temporary converted copy are **moved to the Drive trash** (recoverable for 30 days); you can trash older copies in the same step. If anything fails, nothing is trashed.
- Each release now includes **1_Google_Sheet/App_Data.json**: the app's data tabs as plain text, which the update reads.

#### Never touched by either menu
- Saved_Proofs, the color tabs (Paint, vinyl, Pantone ...), Product_Schema, README and any tab of your own.

#### Setup
- New Apps Script file **Updater** (script) and the new **appsscript.json** (Project Settings > Show "appsscript.json" manifest file in editor, then paste). Reload the sheet: the **Proof Generator** menu appears; the first run asks for permission (Sheets, Drive, external requests, managing this script and its deployments).
- One-time, for automatic code updates: **script.google.com/home/usersettings** > Google Apps Script API: **On**.

---

### [2.2] – 2026-10-13
#### Added
- **Autosave:** about every 30 seconds after a change, the package is saved as a draft. Each proof has **one** draft file that is overwritten in place (a never-saved package gets one file in Proof Library/_Drafts), so no files pile up, and drafts never become versions: only **Save** makes v1, v2, v3 ... The top bar shows "Draft saved 2:14 PM".
- **Unsaved changes are protected:** closing the tab with unsaved changes shows the browser's "Leave site?" warning; the next visit offers **Restore** for the unsaved work. Drafts are listed in **Saved proofs** (Open / Discard), and opening a proof that has autosaved changes offers them first. Saving a version clears its draft.
- **Approval status:** every saved version has a status: **Draft**, **Sent to Customer**, **Changes Requested**, **Approved** or **Cancelled**. Choose it in the Save dialog or change it in Saved proofs without opening the proof; it shows as a colored chip in the library and the top bar, the library can be filtered by status, and the Saved_Proofs tab records who changed it and when (Status, Status_By, Status_At columns, added automatically to existing tabs).
- **New from this:** a button in Saved proofs that starts a new proof from any version, keeping every product, section, spec, image and measurement line and clearing the customer info. Its first save is v1 of a new proof.

#### Changed
- **Versions instead of revisions:** saved proofs are numbered **v1, v2, v3 ...** everywhere in the app (top bar, Save dialog, Saved proofs, messages). The Saved_Proofs tab keeps its Rev column name so existing rows keep working. The Revision Date on the proof pages is unchanged.

---

### [2.1.2] – 2026-10-13
#### Changed
- **Monument Letters can be front lit or halo lit.** **Lighting** is now the first construction choice (Non-Lit, Front Lit, Halo Lit or Ground Lit by others), and it decides which material fields appear:
  - **Non-lit / ground lit:** letter type (flat cut aluminum, fabricated aluminum, cast, stainless, brass, acrylic, PVC, HDU), plate thickness, or face / return gauge and depth for fabricated letters; finish and paint color.
  - **Front lit** (built like channel letters): 3/16" acrylic or polycarbonate face, face color, translucent vinyl and its color, trim cap size and color, return gauge, depth (2" to 6") and return (coil) color, LED color, power supply and photo cell.
  - **Halo lit** (reverse channel): aluminum face gauge, return gauge, depth, clear polycarbonate or acrylic back, finish and paint color, return color, LED color, diffuser vinyl, power supply and photo cell.
- Front lit monument letters show the **Front Lit Section** and **Trim Cap & Return** detail drawings, halo lit ones the **Halo Lit Section**, and both get the lit-sign Design Help rules. The top-mount drawings label the thickness or depth that applies.
- **Cleaner field labels:** fields that exist in two versions (e.g. FACE GAUGE for halo and unlit letters, OVERALL DEPTH for single / double sided EMCs) show just the plain name in the form.

---

### [2.1.1] – 2026-10-13
#### Changed
- **Download page / Download table:** the single Download SVG button is now two deep blue buttons at the right end of each page's bar.
  - **Download page** saves the whole page as an SVG, identical to and named like the file in the package zip (also on the cover and QA pages).
  - **Download table** saves only that page's spec table with its product label, as an SVG cropped to the table at true size (1 unit = 0.01"), named `... - p02 - table.svg`. It appears on every page that has a spec table.

---

### [2.1] – 2026-10-13
#### Added
- **Monument Letters:** a new component (blue Letters family, with its own icon) and an optional section in Monument Signs, for permanent 3D letters on a monument or free-standing sign.
  - Letters: quantity counted from the text, letter height, text, font, and **+ Add Letters** for more sizes.
  - Material: flat cut aluminum, fabricated aluminum (reverse channel), cast aluminum, flat cut stainless, brass, acrylic or PVC, or routed HDU. Flat cut, cast and HDU letters list their plate **thickness** (1/8" to 2"); fabricated letters list **face gauge** (.040 to .125), **return gauge** (.040 to .063) and **depth** (1-1/2" to 6").
  - Finish (painted, brushed, polished, anodized, natural) with a paint color picker, and return color on painted fabricated letters.
  - Mounting: **Top Mount - Pinned** (default: letters stand on the cap with threaded pins set in epoxy, with pin size and embed depth), **Top Mount - Adhesive**, face mounted with studs (flush or with spacers), or **Standoffs** (model AL25-30A or AL16-25A, size and finish, as on panels). Monument surface and a full-size mounting pattern.
  - Lighting: non-lit, halo lit (LED color, power supply, photo cell) or ground lit by others.
  - Two new detail drawings, TOP MOUNT - PINNED and TOP MOUNT - ADHESIVE; face mounting uses the existing stud and stand-off drawings and halo lit letters the halo section. New Design Help rule L08.
- **Color matching:** the custom color panel takes a **HEX** code as well as CMYK and RGB, and lists **Closest matches**: the 3 nearest Sherwin-Williams colors, the 3 nearest Pantone colors and, on vinyl fields, the 3 nearest Oracal colors in that field's series, ranked by Delta E 2000. Clicking a match selects that swatch where the field offers the library, otherwise it names the custom color after it. Matches are based on screen colors; confirm with a physical swatch.
- **Swatch search:** every color and pictogram library has a search box (name, number or series; several words narrow it down). Enter picks the first result; Esc closes.
- **Download SVG per page:** a deep blue **Download SVG** button at the right end of every page's bar (cover, proof pages and QA pages) saves that page alone, identical to and named like the file in the package zip.
- **+ Add Another everywhere:** every section of every product and component can now be added again (Pole Cover and others were missing it). The added copy of an optional section is always included.

#### Changed
- **Sales Proof:** the proof is now called a Sales Proof. The button reads **Generate Sales Proof Package**, the cover title is **SALES PROOF PACKAGE** and each page's sidebar says **SALES PROOF** (Proof_Template: Title, Cover_Title).

---

### [2.0] – 2026-10-13
#### Added
- **Proof Library (saved, editable proofs):** **Save** in the top bar stores the whole package in a shared **Proof Library** folder in Google Drive, next to the Google Sheet. That covers every product and section, field value, custom table, letter line, vinyl color list, special note, blank page, unchecked detail drawing, customer field, artwork image (with its size and position) and measurement line. A **Saved_Proofs** tab in the sheet lists every save.
- **Revisions:** each save of an opened proof becomes the next revision (Rev 1, Rev 2 ...) with an optional note; earlier revisions are never overwritten. **Save as a new proof** makes a copy with its own revision history.
- **Saved proofs:** a searchable list (customer, project, ticket, designer or product) with a revision picker. **Open** rebuilds the package exactly as saved so it can be edited and exported again. **New** starts an empty package. Also on the dashboard as **Open a saved proof**.
- Images are stored once per proof and shared by all its revisions. Proofs are saved as plain JSON, ready to move into a database later.
- **Dashboard filter:** the color key above the cards toggles sign families on and off (several at once, combined with the search box); **Show all** resets it. Sections with no matches hide.

#### Changed
- **New look (Material style):** light tonal surfaces, Roboto, pill buttons, a segmented step control, outlined fields with a focus ring, rounded dialogs, a snackbar for messages and a light grey canvas behind the proof pages. Proof pages and exports are unchanged.
- **Dashboard cards:** an even outline in the family color all the way around each card, with the product name and icon in the same color. Selected cards are tinted and show their order number.

#### Setup
- New Apps Script file **ProofLibrary** (script). Approve the Google Drive permission the first time someone saves. The web app must stay **Execute as: Me** so every designer can use the library.

---

### [1.9.5] – 2026-10-13
#### Added
- **Multiple vinyl colors:** every vinyl color field has a **+ Add Color** button, like **+ Add Letters** on channel letters, so one vinyl proof can list all of its colors. Each added color has its own Oracal series, swatch picker, **-- Custom Input --** and **Custom** CMYK / RGB panel, and starts on the series chosen above it.
- On the proof, QA checklist and CSV the colors print as numbered rows (e.g. VINYL COLOR 1, VINYL COLOR 2, VINYL COLOR 3), each with its color chip. An added color left unpicked prints as MISSING; **[x] Remove** takes one out and the rest renumber.
- Works on every vinyl field, including Cut Vinyl Decal, channel letter face vinyl and vinyl rows in custom tables. **+ Add Another** on channel letter and custom sections copies the color list; a field that lists several colors widens to the full row.

---

### [1.9.4] – 2026-10-13
#### Changed
- **Cloud signs replace cloud letters:** the Cloud Letters products and the separate Cloud section are gone. In their place are two products of their own, **Cloud Sign - Front Lit** and **Cloud Sign - Halo Lit**, completely separate from channel letters. A customer can order a cloud sign without channel letters; for letters on a cloud, select both the channel letters and the cloud sign.
- **Cloud sign specs:** a cloud sign has a typed **QUANTITY** and **CLOUD SIZE** (W x H) instead of letter count, letter height and text. Everything else matches the channel letters: face, face color and vinyl, return, return color, trim cap, LED, mounting and raceway size on the front lit sign; face, face graphics, return, backs, diffuser, standoffs and wall surface plus the illumination fields (photo cell defaults to Yes) on the halo lit sign. **+ Add Letters** stays on channel letters only.
- **Drawings and help rules:** the front lit, halo lit, trim cap, raceway and flush mount drawings apply to cloud signs, as do the lit-sign Design Help rules. The letter-only rules (letter cap height, letter cut files, halo letter stroke) don't. The flush mount drawing is now titled "FLUSH MOUNT (LETTERS / CLOUD)".

#### Added
- **Dashboard icons:** every product and component card has a one-color icon showing the general shape of that sign type (letters, cloud, pole sign, monument, cabinet, EMC module grid, panels, banner, decal, ADA and more).
- **Color families:** each card is outlined in its family color, with a legend above the list: blue for channel letters and cloud signs, purple for cabinets and digital, orange for pole, monument and ground signs, green for panels, pink for vinyl and banners, teal for ADA, and red for custom tables. Selected cards are tinted in their family color.

---

### [1.9.3] – 2026-10-13
#### Added
- **Build Custom Table:** a new **Custom** area on the main screen, below Products and Components. Click **+ Build Custom Table**, name the product (e.g. "Pylon Topper"), and it is added to the package like any other product. The name can be changed on the main screen or on the specs step.
- **Title + description rows:** each row of a custom table has a title you type (printed as the label on the proof) and a description. A new table starts with QUANTITY, SIZE and two blank rows; **+ Add Row** adds more and × removes one. Fully blank rows are left off the proof, and a row with a title but no description prints as MISSING.
- **Description types:** text, size (W x H or W x H x D), paint (Sherwin-Williams / PMS / custom CMYK and RGB), finish, Oracal vinyl, ACM, acrylic, PVC, Coroplast, trim cap, return / coil and LED colors, Rowmark and ADA pictogram. They use the same swatch pickers and custom color panel as the rest of the app.
- **Columns:** each row has a column picker (Col 1 to 6) that sets where it prints in the proof table.
- **Sections and components:** **+ Add Section** adds another custom table to the same product, **+ Add Component...** adds any existing component (poles, illumination, footer, EMC and more), and **+ Add Another** copies a custom section with its values. Sections can be removed.
- **Detail drawings:** each custom section has a **Detail drawings** checklist of all detail drawings; checked ones print on that section's proof page.
- **Custom vinyl:** every vinyl field's Oracal series dropdown has a **-- Custom Input --** choice with a text box for any vinyl not in the list (e.g. 3M 3630-33 Red). The **Custom** checkbox can add CMYK / RGB values to it.
- Custom tables work with everything else: New page, blank pages, special notes, quantity tags on the cover, measurement lines, the QA checklist and CSV, and the SVG / PNG export.

#### Notes
- Custom tables are kept with the current package only, like images and measurement lines. Index.html changed in this version (the new Custom area).

---

### [1.9.2] – 2026-10-13
#### Added
- **Cloud letter components:** Cloud Letters - Front Lit and Cloud Letters - Halo Lit can now be added as stand-alone components. Each one has every face, trim cap, return, back, illumination, mounting and raceway option of the matching channel letters, plus the cloud fields (size, depth, material, color, lighting). The halo version also includes the illumination fields (power supply, photo cell, timer). Letter detail drawings and Design Help rules apply to them as they do to channel letters.
- **+ Add Letters:** front-lit, halo-lit and cloud letter sections have a **+ Add Letters** button that adds a simple Quantity / Letter Height / Text line inside the section. The quantity is counted from the text, the height carries over from the line above, and each line prints on the proof as its own QTY / HEIGHT and TEXT rows. Lines can be removed with ×.
- **EMC specs from production:** the Digital Sign (EMC) section now uses 9.45" x 9.45" modules. Enter modules wide and high to get the display size. Pixel pitch offers FLEX Ultra Resolution (5, 6, 8, 10mm) and FLEX Enhanced Resolution (12, 16, 20mm). Depths default to 1.5" modules, a 5" LED cabinet and a 3" back angle. The overall depth and the cabinet depth are calculated, with modules extending past the cabinet: single sided is 9.5" overall in an 8" cabinet, and double sided on a 4" pole is 23" overall in a 20" cabinet.
- **Calculated fields:** a new `calc` field type in Component_Schema shows a read-only value worked out from other fields in the same section. Number fields can show a unit (e.g. `"`) set in Options.

#### Changed
- The section button is **+ Add Another …** again; it copies the whole section with its settings.
- The custom color checkbox under swatch pickers is labelled **Custom**, so it no longer gets cut off.
- Cloud is no longer offered on its own in the component list. Use the two cloud letter components, or add Cloud to a cloud letter product.

---

### [1.9.1] – 2026-10-13
#### Fixed
- **Measurement lines stay out of the way:** lines can now only be selected, moved or resized while that page's Measure mode is on. Outside Measure mode they ignore the mouse, so dragging an image underneath a line moves the image and never the line. Lines are still removed with the x beside their value in the page toolbar.

---

### [1.9] – 2026-10-12
#### Added
- **Custom colors with CMYK and RGB:** choosing Custom on a color field (material, face, paint, vinyl, return, trim cap, LED and Rowmark colors) opens a panel for a color name plus CMYK and RGB values. Type either set and the other is calculated and marked "(approx.)"; the proof prints the name and both sets.
- **New page toggle:** each section card has a "New page" checkbox that starts that section's table on a new proof page.
- **Blank pages:** "+ Add Blank Page" under each product adds a page with the sidebar, watermark and an empty art board, for elevations, mockups or site photos. Each blank page has an editable title (default "Page") shown in its footer and in the cover's Package Contents.
- **Standoffs:** ACM, PVC, Acrylic, HDU and ADA signs with standoff mounting now have STANDOFF MODEL (AL25-30A, AL16-25A or Custom), STANDOFF SIZE (filled in from the model, editable) and STANDOFF FINISH (Brushed Aluminum, Satin Aluminum, Black, Chrome, Gold or Custom). Halo-lit and front-lit channel letters keep their existing standoff options.
- **Cloud letters:** new products Cloud Letters - Front Lit and Cloud Letters - Halo Lit use the same letter settings and detail drawings as their channel letter counterparts, plus a Cloud section (size, depth, material, color, lighting). Cloud is also available as a stand-alone component.
- **Raceway size:** front-lit channel letters and front-lit cloud letters mounted on a raceway get a RACEWAY SIZE field (L x H x D).
- **+ Add Letters:** on front-lit and halo-lit letters (including cloud letters), adds another letter set that copies the previous set's settings, for mixed letter sizes in one project. Every set stays editable.
- **Measurement lines:** a Measure button on each page's toolbar. Click, drag and release to draw a red dimension line (hold Shift to keep it straight), type its value in inches, then move it or drag its ends. Lines export as editable SVG lines and text in a Measurements group.

#### Changed
- **SVG export:** added images are cropped to the art board instead of clipped, so CorelDRAW imports them as plain images rather than locked PowerClips.
- **Mounting detail:** on ACM, PVC, Acrylic and HDU, the MOUNT DETAIL text box no longer appears for standoffs; the new standoff fields replace it.

---

### [1.8] – 2026-10-08
#### Added
- **Special notes per section:** every section in the proof builder has an **Add Special Notes** checkbox and text box. The notes print in a gold-edged **SPECIAL NOTES** column to the right of that section's table on the proof sheet. This restores the special notes from the original app, now one per section.
- Unchecking **Add Special Notes** hides the notes from the proof but keeps the text, so checking it again brings them back.
- **Quantities on the cover page:** Package Contents rows show the quantity from each section's Quantity field in bold red, e.g. `(x2) Main Menu Boards`. Single-section items show it on the main row, e.g. `(x1) Banner`. The tag appears on the cover only.

#### Changed
- **Cover page:** the proof pages column in Package Contents now reads "Page 2", or "Pages 3 - 5" for a range.
- Sections with a blank quantity show no tag, and sections with the same name have their quantities added together.
- Pages with special notes add a notes column to the spec table. Sections without notes on the same page get a plain gray cell, and the table scales to fit.

---

### [1.7] – 2026-10-08
#### Added
- **Editable section names:** the red section title on each part card in the proof builder (e.g. "Acrylic 2") is now a plain-text field. Type a specific name such as "Front Menu" or "Side Menu".
- Renamed sections carry through to the proof sheet section heading, the cover page's package contents sub-rows, the QA checklist pages and the QA `.csv`.
- Clearing the field and pressing Enter (or clicking away) returns the section to its default name.

#### Changed
- **Section numbering:** a single section keeps its plain name ("Acrylic"). Once **+ Add Another** is used, sections are numbered ("Acrylic 1", "Acrylic 2", "Acrylic 3"). Sections that haven't been renamed renumber automatically when one is removed (Acrylic 3 becomes Acrylic 2), while renamed sections keep their names.

---

### [1.6] – 2026-10-08
#### Added
- **QA checklist print PDF:** all QA pages are combined into one multi-page letter-size PDF, saved as `QA_Checklist/PRINT - … - QA checklist.pdf` next to the SVG, PNG and CSV versions. The PDF is built in the browser, so nothing extra is required.
- **Sub-customer field:** a **Sub-customer** checkbox on the Customer Info step shows a *Sub-Customer Name* field. A blank sub-customer is flagged as MISSING.
- File names include the sub-customer right after the customer: `Ticket - Customer - Sub-Customer - Project - p01`. The same names are used for the zip, the QA files and the CorelDRAW `.cdr`.
- `package_info.txt` now records `SubCustomer=` and `FileBase=`.
- When **Sub-customer** is checked, the sub-customer name prints next to the customer name as `Customer - Sub-Customer`. This applies to every proof sheet (the red sidebar box), the cover page and the QA checklist header.
- The QA checklist header text shrinks to fit long customer and sub-customer names, so it no longer gets cut off.

#### Changed
- **Cover page:** the "This design and engineering…" legal text and the copyright line now sit on the same baseline.
- **CorelDRAW macro:** the folder picker is back to the classic **Browse for Folder** window. The Explorer-style picker was tried and removed because it only let you select single files, not a folder. A typed-path box appears only if the Windows Shell is unavailable.

---

### [1.5] – 2026-10-08
#### Added
- **Cover page:**
  - A **project notes** summary box, filled from a new Project Notes field.
  - A **company contact line** (name, address, phone, website, email). It comes from the `Company_*` keys on the `Proof_Template` tab, and blank keys are skipped.
- **Page selection for pasting** can now be cleared. You can click the page bar again, press **Esc** or click the background to deselect the gold-outlined page.
- **Choose where to save:** Chrome and Edge open a save dialog for the zip when the browser allows it. It falls back to a normal download inside the Apps Script frame.
- **MISSING tags in SVGs:** each tag is its own group, with an empty text box underneath in the matching style. Delete the tag and type, with no need to edit the label.
- **New export file names:** `Ticket - Customer - Project - p01.svg` (QA: `- qa01`), and the zip is named `Ticket - Customer - Project.zip`.
- **`package_info.txt`** in the zip holds the ticket, customer, project, file location and page names.
- **CorelDRAW macro module** (`ProofPages_CorelDRAW_Macro.bas`):
  - `ImportProofPackage` creates one page per SVG in the open 8.5 × 11 template. Each sheet is scaled to fill and the orientation is matched.
  - Pages are named from the files, and the QA pages are optional.
  - One Undo reverses the whole import.
  - The file is saved automatically as `Ticket# - Customer - Project.cdr`, in the job folder taken from the proof's File Location.
  - `BuildFromPackage` and `AddProofPages` from v1.2 are kept in the same module.

#### Changed
- **Export folders:** SVGs and PNGs are in separate `SVG/` and `PNG/` folders, and `QA_Checklist/` has its own `SVG/` and `PNG/` subfolders.

#### Fixed
- **CorelDRAW macro:** fixed the *"Can't assign to read-only property"* compile error. The macro no longer sets `doc.Title`, and version-specific members are late-bound so it works across CorelDRAW versions.

---

### [1.4] – 2026-10-08
#### Changed
- **Cover contents list:** each product is a bold row, with its sections as indented sub-rows (1.1, 1.2 …) that list their proof pages. Large packages flow into two columns.
- **Watermark:**
  - Now one flat, non-editable image instead of text.
  - Covers the whole art board, cropped at the art board edges.
  - Set to 2% gray through the new `Proof_Template › Watermark_Opacity` setting.
  - Has no transparency, so CorelDRAW shows exactly what the preview shows.
- **QA checklist:**
  - One checkbox beside each product or component title.
  - An OK / INIT line to the right of every individual spec.
  - **Final Checks** and QA Manager sign-off moved into a separate red-outlined section at the bottom of the last page.
  - Notes area expanded from 2 to 10 lines.

---

### [1.3] – 2026-10-08
#### Added
- **Artwork images on proof pages:** use the **+ Add image** bar above any page, drop a file on it, or select the page and paste a screenshot (Ctrl+V).
  - Images fit the open art board space and can be dragged, sized with − / + / Fit, or removed with ×.
  - They are embedded in the SVG (on an *Artwork* layer) and in the PNG.

#### Changed
- **Cover page:** the customer approval block was removed, leaving only the legal and copyright line.
- **Watermark:** lightened, and changed to a solid tint because CorelDRAW ignores SVG opacity.
- **Detail drawings:** the halo glow is now solid, with no transparency.

#### Fixed
- SVG text showed entity codes such as `&quot;` in CorelDRAW. Text is now written as plain UTF-8: inch marks are kept as-is, and lines containing `&` or `<` are wrapped in CDATA.
- Uploading several artwork files at once no longer drops images, caused by a timing issue between the uploads.

---

### [1.2] – 2026-10-08
#### Added
- **Cover page (page 1):** Sign Store logo, customer name, project name, project info and a full list of products and components with their page numbers.
- **QA checklist:**
  - Exported in its own `QA_Checklist/` folder, with every spec and its checkbox and initials, the detail drawings, final checks and QA Manager sign-off.
  - Also exported as a `.csv` for Excel and Sheets.
  - Can be switched on or off with `Proof_Template › QA_Checklist`.
- A separate **Project Name** field, also shown under the customer in the red sidebar box.
- An **×** button that clears a chosen ADA pictogram.
- First CorelDRAW page macros: `AddProofPages` adds blank pages up to a total, and `BuildFromPackage` builds a document with one page per SVG.

---

### [1.1] – 2026-10-08
#### Added
- **Proof packages:**
  - A dashboard, modular components and multi-page 11 × 8.5 proof sheets that match the company template.
  - A customer info form, with MISSING tags for blanks.
  - SVG and PNG zip export.
  - 10 legacy products migrated to components.
- **`Detail_Drawings` tab:** 26 vector construction drawings covering:
  - mounting
  - letter construction
  - cabinet construction
  - footers and poles
  - panel finishing
  
  Each drawing appears when the product's specs match its rule, and you can uncheck any drawing per product.
- New **CORNERS** field on ACM, PVC, Coro, Acrylic and Sign Panel.
- **Design Help Center:** a **?** button on the specs step opens a plain-text pop-up of design department procedures and CorelDRAW how-to's. It draws on 91 rules in the `Design_Guide` tab (from SignOS data, industry standards and house standards) and shows only the rules for the current package.
- New `COMPONENT=` keyword for Match_Rule and Show_If rules.
- A startup watchdog: if a file fails to load, the page shows a red message naming that file within 20 seconds.

#### Fixed
- The app hung on "Loading Database from Google Sheets…". This was caused by Apps Script mangling `<?xml` and `//` inside JavaScript strings, and by an overlong line in Assets.
- `Assets.html` shrunk from 325 KB to 40 KB, split into short lines.
- Hidden fields no longer trigger drawing or help rules.
