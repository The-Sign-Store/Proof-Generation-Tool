# Changelog

All notable changes to the Sign Proof Generator are listed here, newest first.

---

## [5.5] – 2026-10-08
### Added
- When **Sub-customer** is checked, the sub-customer name prints next to the customer name as `Customer - Sub-Customer`. This applies to every proof sheet (the red sidebar box), the cover page and the QA checklist header.
- The QA checklist header text shrinks to fit long customer and sub-customer names, so it no longer gets cut off.

### Changed
- **CorelDRAW macro:** the folder picker is back to the classic **Browse for Folder** window. The Explorer-style picker was tried and removed because it only let you select single files, not a folder. A typed-path box appears only if the Windows Shell is unavailable.

---

## [5.4.3] – 2026-10-08
### Added
- **QA checklist print PDF:** all QA pages are combined into one multi-page letter-size PDF, saved as `QA_Checklist/PRINT - … - QA checklist.pdf` next to the SVG, PNG and CSV versions. The PDF is built in the browser, so nothing extra is required.
- **Sub-customer field:** a **Sub-customer** checkbox on the Customer Info step shows a *Sub-Customer Name* field. A blank sub-customer is flagged as MISSING.
- File names include the sub-customer right after the customer: `Ticket - Customer - Sub-Customer - Project - p01`. The same names are used for the zip, the QA files and the CorelDRAW `.cdr`.
- `package_info.txt` now records `SubCustomer=` and `FileBase=`.

### Changed
- **Cover page:** the "This design and engineering…" legal text and the copyright line now sit on the same baseline.

---

## [5.4.2] – 2026-10-08
### Added
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
  - `BuildFromPackage` and `AddProofPages` from v5.2 are kept in the same module.

### Changed
- **Export folders:** SVGs and PNGs are in separate `SVG/` and `PNG/` folders, and `QA_Checklist/` has its own `SVG/` and `PNG/` subfolders.

### Fixed
- **CorelDRAW macro:** fixed the *"Can't assign to read-only property"* compile error. The macro no longer sets `doc.Title`, and version-specific members are late-bound so it works across CorelDRAW versions.

---

## [5.4.1] – 2026-10-08
### Changed
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

## [5.3] – 2026-10-08
### Added
- **Artwork images on proof pages:** use the **+ Add image** bar above any page, drop a file on it, or select the page and paste a screenshot (Ctrl+V).
  - Images fit the open art board space and can be dragged, sized with − / + / Fit, or removed with ×.
  - They are embedded in the SVG (on an *Artwork* layer) and in the PNG.

### Changed
- **Cover page:** the customer approval block was removed, leaving only the legal and copyright line.
- **Watermark:** lightened, and changed to a solid tint because CorelDRAW ignores SVG opacity.
- **Detail drawings:** the halo glow is now solid, with no transparency.

### Fixed
- SVG text showed entity codes such as `&quot;` in CorelDRAW. Text is now written as plain UTF-8: inch marks are kept as-is, and lines containing `&` or `<` are wrapped in CDATA.
- Uploading several artwork files at once no longer drops images, caused by a timing issue between the uploads.

---

## [5.2] – 2026-10-08
### Added
- **Cover page (page 1):** Sign Store logo, customer name, project name, project info and a full list of products and components with their page numbers.
- **QA checklist:**
  - Exported in its own `QA_Checklist/` folder, with every spec and its checkbox and initials, the detail drawings, final checks and QA Manager sign-off.
  - Also exported as a `.csv` for Excel and Sheets.
  - Can be switched on or off with `Proof_Template › QA_Checklist`.
- A separate **Project Name** field, also shown under the customer in the red sidebar box.
- An **×** button that clears a chosen ADA pictogram.
- First CorelDRAW page macros: `AddProofPages` adds blank pages up to a total, and `BuildFromPackage` builds a document with one page per SVG.

### Changed
- Version numbering moved from 2.x to 5.x.

---

## [5.1] – 2026-10-08
*Released internally as v2.0–v2.2.*

### Added
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

### Fixed
- The app hung on "Loading Database from Google Sheets…". This was caused by Apps Script mangling `<?xml` and `//` inside JavaScript strings, and by an overlong line in Assets.
- `Assets.html` shrunk from 325 KB to 40 KB, split into short lines.
- Hidden fields no longer trigger drawing or help rules.
