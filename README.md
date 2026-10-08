# Sign Proof Generator

**Current version: v5.5.3** · The Sign Store Online, Inc. · Design Department

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
- **Special notes per section:** check **Add Special Notes** on any section and type. The notes print in a gold-edged **SPECIAL NOTES** column beside that section's table on the proof sheet. Unchecking hides them but keeps the text.
- **Artwork placement:** add a screenshot or JPEG to any proof page with a button, by dropping it, or by pasting with Ctrl+V. You can move and resize it, and it is embedded in the SVG and PNG exports.
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
3_Samples/           sample export zip, cover, proof pages (incl. special notes),
                     QA pages and PDF
4_Source_Builders/   Python scripts that rebuild the workbook (optional)
README.md            this page
README.txt           full setup guide
CHANGELOG.md         version history
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

See [CHANGELOG.md](CHANGELOG.md) for the version history.
