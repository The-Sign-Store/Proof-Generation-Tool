SIGN PROOF GENERATOR  v1.1  (October 8, 2026)
The Sign Store Online, Inc. - Design Department
=============================================================================

A Google Apps Script web app, bound to a Google Sheet, that builds 11" x 8.5"
proof packages: pick products and components, fill in specs, add customer info,
then download a zip with an editable SVG (Illustrator / CorelDRAW) and a
300 ppi PNG for every page.


WHAT IS IN THIS PACKAGE
-----------------------------------------------------------------------------
1_Google_Sheet/
   Sign_Proof_Specifications_App_Data.xlsx   The database the app reads.

2_Apps_Script/                               One file per Apps Script file.
   Code.gs            server: reads the sheet (getAppData)
   Index.html         page layout + startup watchdog
   Stylesheet.html    styles
   JavaScript.html    the app (builder, proof sheets, drawings, help center)
   Assets.html        logo + ETL artwork (image data, split into short lines)
   appsscript.json    project manifest (time zone, V8 runtime, no libraries)

3_Samples/
   Sample_Proof_Package_Export.zip          what "Generate Proof Package" downloads
   Sample_Page_*.png                        single exported pages
   Detail_Drawings_Reference.png            all 26 detail drawings
   Sample_Design_Help_*.txt                 Help Center text for one package

4_Source_Builders/  (optional, for rebuilding the workbook with Python)
   modular_data.py, legacy_components.py   components, fields, assemblies
   detail_drawings.py                       the 26 detail drawings
   design_guide.py                          the 91 design standards
   build_appdata.py                         writes the workbook (needs the
                                            original App_Data + SignOS DEV files)


SET UP FROM SCRATCH (about 10 minutes)
-----------------------------------------------------------------------------
1. Google Drive > New > File upload > Sign_Proof_Specifications_App_Data.xlsx.
   Open it, then File > Save as Google Sheets. Use the Google Sheet from now on.

2. In that Google Sheet: Extensions > Apps Script. This creates a project
   bound to the sheet (the app reads "the active spreadsheet").

3. Create the files, named EXACTLY as below (Apps Script adds .gs / .html):
     Code         (Script)  paste Code.gs   (replace the starter function)
     Index        (HTML)    paste Index.html
     Stylesheet   (HTML)    paste Stylesheet.html
     JavaScript   (HTML)    paste JavaScript.html
     Assets       (HTML)    paste Assets.html
   For each HTML file: + > HTML > type the name, select all, delete, paste.

4. Check Assets pasted completely: its last two lines must be
       PROOF_ASSETS.loaded = true;
     </script>

5. Optional manifest: Project Settings > check "Show appsscript.json in editor",
   then paste appsscript.json. Libraries must be empty.

6. Save (Ctrl+S). Deploy > New deployment > type Web app.
     Execute as: Me      Who has access: your company / as needed
   Authorize when asked (it only reads this spreadsheet).
   For testing, use Deploy > Test deployments (the /dev link always runs the
   latest saved code). The regular link only changes when you
   Manage deployments > Edit > Version: New version > Deploy.


UPDATE AN EXISTING COPY
-----------------------------------------------------------------------------
- Code changes: paste the changed files over the old ones, save, hard refresh
  the /dev link (Ctrl+Shift+R), then publish a New version for the live link.
- New tabs only (keep your own edits): upload this workbook as a separate
  Google Sheet, right-click the tab > Copy to > Existing spreadsheet, and
  rename the copy to the exact tab name (e.g. "Detail_Drawings").


IF THE PAGE WILL NOT LOAD
-----------------------------------------------------------------------------
The page shows a red message within 20 seconds that names the file at fault.
- "Assets did not load"  -> Assets was cut off when pasted; re-paste it.
- "JavaScript did not load" -> check the file is named exactly JavaScript.
- "Google Sheet has not answered" -> Apps Script > Executions > open the
  failed getAppData run for the error.
- Library error -> remove it under Libraries (the app uses none).
Two Apps Script quirks the code already works around; avoid them in edits:
  * never type the characters  <?  or  ?>  in an HTML file (Apps Script
    treats them as its own tags);
  * never put two slashes in a row inside a JavaScript string, e.g. a web
    address (Apps Script reads it as a comment and cuts the line).


THE GOOGLE SHEET (tab names and headers are read by the code; do not rename)
-----------------------------------------------------------------------------
README               full reference for every tab and column
Product_Assembly     which components make up each product, page grouping
Component_Registry   the 23 components
Component_Schema     every field: type, options, defaults, Show_If, Required
Detail_Drawings      26 construction drawings + the spec rule that shows each
Design_Guide         91 design standards for the Help Center pop-up
Proof_Template       fixed text on every page; Watermark and Detail_Drawings
                     switches (On / Off)
Color tabs           Oracal, SW, PMS, ACM, Acrylic, PVC, Coro, Coil, TrimCap,
                     LED, Finish_Colors, Rowmark_Colors
ADA_Pictograms       from SignOS REF_Pictograms
SignOS_Reference     SignOS SKUs behind the material options
Product_Schema       original products, kept for reference (the current app does not read it)


WHAT THE APP DOES (v1.1)
-----------------------------------------------------------------------------
Step 1  Select: any mix of 17 products and 10 stand-alone components.
Step 2  Specs: fields driven by the sheet; sections paginate 2 per page.
        - Detail drawings print bottom-right when specs match (uncheck any
          per product). Live values fill in (embed depth, return, trim cap).
        - Design Help (? button): plain-text standards + CorelDRAW how-to's
          for this package only. Copy / Download .txt / Print.
Step 3  Customer info: blanks print as yellow MISSING tags.
Export  One zip: p01_<product>_specs_1.svg + .png per page. SVG text is Arial
        and editable; drawings and watermark are vector.


CHANGELOG
-----------------------------------------------------------------------------
v1.1  (2026-10-08)
  Added
    - Proof packages:
      - A dashboard, modular components and multi-page 11 × 8.5 proof sheets
        that match the company template.
      - A customer info form, with MISSING tags for blanks.
      - SVG and PNG zip export.
      - 10 legacy products migrated to components.
    - Detail_Drawings tab: 26 vector construction drawings covering:
      - mounting
      - letter construction
      - cabinet construction
      - footers and poles
      - panel finishing
    - Each drawing appears when the product's specs match its rule, and you
      can uncheck any drawing per product.
    - New CORNERS field on ACM, PVC, Coro, Acrylic and Sign Panel.
    - Design Help Center: a ? button on the specs step opens a plain-text
      pop-up of design department procedures and CorelDRAW how-to's. It draws
      on 91 rules in the Design_Guide tab (from SignOS data, industry
      standards and house standards) and shows only the rules for the current
      package.
    - New COMPONENT= keyword for Match_Rule and Show_If rules.
    - A startup watchdog: if a file fails to load, the page shows a red
      message naming that file within 20 seconds.
  Fixed
    - The app hung on "Loading Database from Google Sheets…". This was caused
      by Apps Script mangling <?xml and // inside JavaScript strings, and by
      an overlong line in Assets.
    - Assets.html shrunk from 325 KB to 40 KB, split into short lines.
    - Hidden fields no longer trigger drawing or help rules.
