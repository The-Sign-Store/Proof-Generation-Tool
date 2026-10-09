# Sign Proof Generator

**Current version: v1.7** · The Sign Store Online, Inc. · Design Department

The Sign Proof Generator is a Google Apps Script web app that builds complete, print-ready sign proof packages from a Google Sheet. Designers pick products and components and fill in the specs. They add customer and project info, then download one zip with these files:

- a branded cover page
- 11" × 8.5" proof sheets
- a QA checklist for production

Each page comes as an editable SVG (for CorelDRAW or Illustrator) and as a 300 ppi PNG. A companion CorelDRAW macro imports the package into the house proof template and saves it with the right file name.

---

## Features

### Proof builder
- **Data-driven:** every product, component, field, option, default, rule, drawing and design standard lives in the Google Sheet. You change the sheet, not the code.
- **17 products and 23 modular components:** pole signs, channel letters, cabinets, monuments, banners, decals, ADA and more. You can mix products and stand-alone components in one package.
- **Conditional specs:** `Show_If` rules, required fields, and live color and material pickers. The pickers cover Oracal, Sherwin-Williams, PMS, ACM, acrylic, LED, trim cap and ADA pictograms.
- **26 vector detail drawings:** mounting, letter construction, cabinets, footers/poles and panel finishing. Each drawing is added automatically when its specs match, with live values such as embed depth, return depth and trim cap.
- **Editable section names:** rename any section, e.g. "Acrylic 2" to "Front Menu". The new name carries through to the proof sheet, cover contents and QA checklist.
- **Artwork placement:** add a screenshot or JPEG to any proof page with a button, by dropping it, or by pasting with Ctrl+V. You can move and resize it, and it is embedded in the SVG and PNG exports.
- **Missing info flagged:** blank fields print as yellow **MISSING** tags. In the SVG, each tag has an empty matching text box underneath, ready to type in.

### Design Help Center
- A **?** button opens the design department's procedures and CorelDRAW how-to's. The pop-up shows only the standards for the products in the current package.
- 91 standards in all. Examples: convert cut-vinyl text to curves with a hairline black outline, show clear glass in baby blue, show tinted glass in blue-grey.
- You can copy, download as .txt, or print the guide.

### Cover page and QA checklist
- **Cover page:** company logo, customer (plus an optional sub-customer), project, project info and a full contents list. The contents list shows each product with indented component sub-rows. The cover also has project notes and the company contact line.
- **QA checklist:**
  - every spec, with OK / INIT boxes
  - a checkbox on each product header
  - the detail drawings
  - a red-outlined **Final Checks** section with QA Manager sign-off and 10 note lines
- The checklist is exported as SVG, PNG, CSV and one multi-page **PRINT** PDF.

### Export
```
47391 - Macon Housing Authority - Central City Apartments.zip
├── SVG/                      p01 = cover, p02… = proof pages (editable)
├── PNG/                      same pages, 300 ppi
├── QA_Checklist/
│   ├── SVG/  PNG/            … - qa01, qa02…
│   ├── PRINT - … - QA checklist.pdf
│   └── … - QA checklist.csv
└── package_info.txt          ticket, customer, project, page names (read by the macro)
```
- **File names:** `Ticket - Customer - [Sub-Customer -] Project - pNN`. Names are Windows-safe and shortened to 80 characters if needed.
- **Watermark:** a flat 2% gray image on its own layer. **Text:** plain UTF-8 Arial, with no entity codes, so it imports cleanly into CorelDRAW.

### CorelDRAW macro (`ProofPages_CorelDRAW_Macro.bas`)
| Macro | What it does |
|---|---|
| `ImportProofPackage` | Fills the open proof template with one page per SVG, scaled to fill the page, with orientation matched and pages named. It can add the QA pages, then saves the file as `Ticket - Customer - [Sub-Customer -] Project.cdr`. One Undo reverses the whole import. |
| `BuildFromPackage` | Does the same import into a new document. |
| `AddProofPages` | Adds blank pages up to a total you choose. |

---

## Repository layout
```
1_Google_Sheet/      Sign_Proof_Specifications_App_Data.xlsx  (the database)
2_Apps_Script/       Code.gs, Index.html, Stylesheet.html, JavaScript.html,
                     Assets.html, appsscript.json, ProofPages_CorelDRAW_Macro.bas
3_Samples/           sample export zip, cover, proof pages, QA pages and PDF
4_Source_Builders/   Python scripts that rebuild the workbook (optional)
README.md            this page: overview + changelog
README.txt           full setup guide
```

## Setup
1. Upload the `.xlsx` to Google Drive, then choose **File › Save as Google Sheets**.
2. In the sheet, open **Extensions › Apps Script**. Create `Code`, `Index`, `Stylesheet`, `JavaScript` and `Assets`, named exactly as shown, and paste in the matching files.
3. Check that the last line of `Assets` is `PROOF_ASSETS.loaded = true;`.
4. Choose **Deploy › New deployment › Web app** with Execute as: *Me*. Use **Test deployments** (the `/dev` link) while you are testing.
5. **CorelDRAW:** press Alt+F11, select **GlobalMacros**, then **File › Import** the `.bas` file and save. Add `ImportProofPackage` to a toolbar.

`README.txt` has the full step-by-step guide, troubleshooting and the sheet reference.

> **Apps Script editing rules:** never type `<?` or `?>` in an HTML file, and never put `//` inside a JavaScript string. Apps Script mangles both, and the page will hang on "Loading…".

## Tech
Google Apps Script (V8) · HtmlService · vanilla JavaScript · SVG (1 unit = 0.01") · Canvas PNG/JPEG rendering · an in-browser PDF writer · JSZip · CorelDRAW VBA · Python and openpyxl (workbook builders)

The full version history is in the [Changelog](#changelog) below.

---

## Changelog

All notable changes, newest first.

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
