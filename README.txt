SIGN PROOF GENERATOR  v2.3  (October 13, 2026)
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
   App_Data.json      the same data tabs as plain text, read by
                      Proof Generator > Update from GitHub

2_Apps_Script/                               One file per Apps Script file.
   Code.gs            server: reads the sheet (getAppData)
   Index.html         page layout + startup watchdog
   Stylesheet.html    styles
   JavaScript.html    the app (builder, proof sheets, drawings, help center)
   Assets.html        logo + ETL artwork (image data, split into short lines)
   Updater.gs         server: Proof Generator menu (update / import, v2.3)
   appsscript.json    project manifest (permissions, Drive service, V8)
   ProofPages_CorelDRAW_Macro.bas   CorelDRAW macros (not for Apps Script).
                      See CORELDRAW below.

3_Samples/
   Sample_Proof_Package_Export.zip          what "Generate Proof Package" downloads
   Sample_Cover_Page.png                    page 1 of every package
   Sample_QA_Checklist_p1.png               first QA checklist page
   Sample_QA_Checklist_PRINT.pdf            the multi-page QA print PDF
   Sample_QA_Checklist_Final_Checks.png     last QA page: red Final Checks box
   Sample_Page_*.png                        single exported pages
   Sample_Page_With_Artwork_Image.png       a page with a placed screenshot
   Sample_Page_Special_Notes.png            a section with special notes
   Sample_Page_Measurement_Lines.png        a page with a measurement line
   Sample_Custom_Color_CMYK_RGB.png         the custom color panel
   Sample_Standoff_Fields.png               standoff model / size / finish
   CorelDRAW_Text_Test.svg                  open in CorelDRAW to check that
                                            inch marks, & and degree signs
                                            import as plain text
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
     ProofLibrary (Script)  paste ProofLibrary.gs   (+ > Script; saves / opens proofs)
     Updater      (Script)  paste Updater.gs        (+ > Script; Proof Generator menu)
   For each HTML file: + > HTML > type the name, select all, delete, paste.

4. Check Assets pasted completely: its last two lines must be
       PROOF_ASSETS.loaded = true;
     </script>

5. Manifest (required from v2.3): Project Settings > check "Show
   appsscript.json manifest file in editor", then paste appsscript.json over
   it. It lists the permissions and turns on the Drive service.

6. Save (Ctrl+S). Deploy > New deployment > type Web app.
     Execute as: Me      Who has access: your company / as needed
   Authorize when asked (it only reads this spreadsheet).
   From v2.0 it also asks for Google Drive: saved proofs go to a
   "Proof Library" folder next to this sheet, listed in a Saved_Proofs tab.
   Because the app runs as you (Execute as: Me), every designer can save and
   open proofs without their own access to that folder.
   For testing, use Deploy > Test deployments (the /dev link always runs the
   latest saved code). The regular link only changes when you
   Manage deployments > Edit > Version: New version > Deploy.


UPDATE AN EXISTING COPY
-----------------------------------------------------------------------------
From v2.3 the sheet has a Proof Generator menu (reload the sheet to see it).

- Proof Generator > Update from GitHub: reads the latest release and updates
  THIS sheet (never a new one):
    1. Component_Registry, Component_Schema, Product_Assembly, Detail_Drawings
       and Design_Guide are copied to hidden "(backup <date>)" tabs (the last
       3 per tab are kept; View > Hidden sheets), then replaced in place.
       These five tabs are release-managed: change them through a release.
    2. Proof_Template: new keys are added; your own values are kept. Values
       you never edited that the release changed are listed to accept / skip.
    3. The Apps Script code: written into the project, saved as a new
       version and the web app deployment moved to it (same link). This
       needs, ONCE per Google account:
         script.google.com/home/usersettings > Google Apps Script API: On
       Without it (or if your Workspace blocks it) the summary lists the
       files that changed since your version, to paste by hand.
- Proof Generator > Import workbook from Drive: the same tab update from a
  Sign_Proof_Specifications_App_Data .xlsx uploaded to Drive (the newest, or
  pick one). Afterwards the .xlsx and its temporary converted copy are moved
  to the Drive trash (recoverable 30 days); older copies can go too. If the
  import fails, nothing is trashed.
- Never touched by either: Saved_Proofs, the color tabs, Product_Schema,
  README and any tab you added.
- First time on v2.3 (the menu cannot install itself): paste Updater.gs and
  appsscript.json (and the other changed files) by hand once, as above.
- Code by hand: paste the changed files over the old ones, save, hard refresh
  the /dev link (Ctrl+Shift+R), then publish a New version for the live link.


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


CORELDRAW: PROOF TEMPLATE + IMPORT MACRO
-----------------------------------------------------------------------------
One-time setup
1. Macro: CorelDRAW > Alt+F11 (Tools > Scripts > Script Editor) > click
   GlobalMacros > File > Import File > ProofPages_CorelDRAW_Macro.bas >
   Ctrl+S. Optional toolbar button: Tools > Options > Customization >
   Commands > Macros, drag ImportProofPackage onto a toolbar.
2. Template: File > New, Letter 8.5 x 11 (either orientation), one page.
   Add your standard layers (NOTES, PRODUCTION, ART, MOCKUP, PROOF
   TEMPLATE) and color settings if you like. File > Save As Template
   (name it e.g. "Sign Store Proof Package"). It then appears under
   File > New from Template > My Templates.

Every job
1. Unzip the proof package from the Proof Generator.
2. File > New from Template > Sign Store Proof Package.
3. Run ImportProofPackage (Tools > Scripts > Run Script, or the button).
   In the "Browse for Folder" window click the unzipped package folder
   (or its SVG folder) and click OK (a path can also be pasted in the box).
   - One page per SVG in order (p01 cover, p02 ...). The template's blank
     page is used first; pages are added as needed.
   - Each sheet is scaled to fill its page and centered; the page turns
     landscape (proof pages) or portrait (QA pages) to match. Pages are
     named from the files (COVER, POLE SIGN SPECS 1 ...).
   - Asks whether to add the QA checklist pages at the end.
   - One Edit > Undo removes the whole import.
4. It then offers to save the file as
       Ticket# - Customer - Project.cdr
   (e.g. 47391 - Macon Housing Authority - Central City Apartments.cdr)
   in the job folder from the proof's File Location (or the unzipped
   package folder). Edit the name / folder in the box, or Cancel to save
   later. The values come from package_info.txt in the zip; anything
   missing is asked for.
Other macros: BuildFromPackage (same import into a new document),
AddProofPages (add blank pages up to a total).
If SVG import shows an options window, click OK; the sheets are exact size.


THE GOOGLE SHEET (tab names and headers are read by the code; do not rename)
-----------------------------------------------------------------------------
README               full reference for every tab and column
Product_Assembly     which components make up each product, page grouping
Component_Registry   the 23 components
Component_Schema     every field: type, options, defaults, Show_If, Required
Detail_Drawings      26 construction drawings + the spec rule that shows each
Design_Guide         91 design standards for the Help Center pop-up
Proof_Template       fixed text on every page; switches (On / Off) for
                     Watermark, Detail_Drawings, Cover_Page, QA_Checklist;
                     Watermark_Opacity = percent gray (default 2);
                     Company_Name / _Address / _Phone / _Website / _Email
                     for the cover's contact line (blank = not printed)
Color tabs           Oracal, SW, PMS, ACM, Acrylic, PVC, Coro, Coil, TrimCap,
                     LED, Finish_Colors, Rowmark_Colors
ADA_Pictograms       from SignOS REF_Pictograms
SignOS_Reference     SignOS SKUs behind the material options
Product_Schema       original products, kept for reference (the current app does not read it)


WHAT THE APP DOES (v2.3)
-----------------------------------------------------------------------------
Step 1  Select: any mix of 19 products and 11 stand-alone components.
Step 2  Specs: fields driven by the sheet; sections paginate 2 per page.
        - Section names (red titles, e.g. "Acrylic 2") are editable: click
          and type "Front Menu". The name prints on the proof, cover and
          QA checklist. Clear it to go back to the default name.
        - Special notes: check "Add Special Notes" at the bottom of any
          section and type; the notes print in a gold SPECIAL NOTES column
          beside that section's table on the proof (proof sheets only).
        - New page: check "New page" on a section to start its table on a
          new proof page. "+ Add Blank Page" under a product adds a page
          with the sidebar and watermark but no table (title editable,
          default "Page"; listed in the cover's Package Contents).
        - Custom colors: Custom on a color field (or the "Custom color"
          checkbox under a swatch picker) takes a name plus CMYK or RGB;
          the other set is calculated and printed as "(approx.)".
        - + Add Letters (channel letters): adds a quantity /
          letter height / text line inside the section, for mixed letter
          sizes. "+ Add Another ..." still copies the whole section.
        - Calculated fields (green, read-only), e.g. EMC display size from
          modules wide x high at 9.45", and overall / cabinet depth.
        - Build Custom Table (main screen, under Custom): a product with
          your own spec table. Each row is a title + description; pick
          the description type (text, size, paint, finish, vinyl, ACM /
          acrylic / PVC / coro / trim cap / coil / LED color, Rowmark,
          pictogram) and the table column. + Add Row, + Add Section,
          + Add Component (any existing component) and a detail drawings
          checklist per section. Kept with this package only.
        - Cloud signs (front lit / halo lit) are their own products, with
          a quantity and size instead of letters. Letters on a cloud:
          select both the channel letters and the cloud sign.
        - Dashboard: each product has an icon and a color family outline
          (blue = channel letters and cloud signs, purple = cabinets and
          digital, orange = pole / monument / ground, green = panels,
          pink = vinyl and banners, teal = ADA, red = custom).
        - + Add Color (vinyl fields): adds another vinyl color to the same
          section, each with its own series, swatch, custom input or
          CMYK / RGB. Prints as VINYL COLOR 1, 2, 3 ... on the proof.
        - Vinyl fields: "-- Custom Input --" at the end of the Oracal
          series list takes any vinyl typed in (other brands / colors).
        - Save (top bar): stores the whole package (every section, value,
          custom table, letter line, color, note, customer field, image and
          measurement) in the shared Proof Library. Each save is a new
          revision (Rev 1, Rev 2 ...); older revisions are kept. "Save as a
          new proof" makes a copy with its own revisions.
        - Saved proofs: search the library and open any revision to keep
          editing. New starts an empty package.
        - Autosave (v2.2): about every 30 seconds after a change the package is
          saved as a draft - ONE file per proof, overwritten each time (never a
          new version). Top bar: "Draft saved 2:14 PM". Closing the tab with
          unsaved changes asks first; the next visit offers "Restore". Drafts
          also show in Saved proofs (Open / Discard).
        - Saved versions are numbered v1, v2, v3 ...
        - Status (v2.2): Draft, Sent to Customer, Changes Requested, Approved,
          Cancelled. Set it when saving or change it in Saved proofs; filter
          the library by status.
        - New from this (Saved proofs): starts a new proof with the same
          products, specs, images and measurements; customer info cleared.
        - Dashboard: the color key above the cards is also a filter; click
          families on / off (with the search box), "Show all" to reset.
        - Download page / Download table (right end of each page's bar):
          that one page as an SVG (same file and name as in the zip), or
          just its spec table, cropped, at true size (pages with a table).
        - Every product / component section has "+ Add Another".
        - Custom colors: type CMYK, RGB or HEX; "Closest matches" lists the
          3 nearest Sherwin-Williams, Pantone (and Oracal on vinyl) colors
          by Delta E 2000. Click one to use it. Screen colors only: confirm
          with a physical swatch.
        - Swatch libraries have a search box (name, number or series);
          Enter picks the first result.
          series list takes any vinyl typed in (other brands / colors).
        - Detail drawings print bottom-right when specs match (uncheck any
          per product). Live values fill in (embed depth, return, trim cap).
        - Design Help (? button): plain-text standards + CorelDRAW how-to's
          for this package only. Copy / Download .txt / Print.
        - Artwork: + Add image / drop / Ctrl+V screenshots onto any proof
          page; drag to move, - / + to size. Kept until the page is closed.
          Click a page's bar to select it for Ctrl+V (gold outline); click
          it again, press Esc or click the background to deselect.
        - Measure (page toolbar): click, drag and release to draw a red
          dimension line (Shift = straight), type its value in inches; drag
          the line or its ends to adjust, x to remove. Exported as editable
          SVG lines + text. Kept until the page is closed, like images.
Step 3  Customer info (customer and project are separate fields; check
        "Sub-customer" for a Sub-Customer Name: printed as "Customer -
        Sub-Customer" on every page and added to the file names after
        the customer): blanks
        print as yellow MISSING tags.
Export  One zip (Chrome / Edge ask where to save it when they can; inside
        Apps Script the browser usually blocks that window, so the zip goes
        to Downloads. Chrome > Settings > Downloads > "Ask where to save each
        file before downloading" makes every download ask):
          File names: "Ticket - Customer - [Sub-Customer -] Project - p01"
          (Sub-Customer only when its box is checked; shortened to 80
          characters if needed), e.g.
            47391 - Macon Housing Authority - Central City Apartments - p01.svg
          SVG/  PNG/                p01 = cover (logo, customer, project,
                                    project info, package contents, project
                                    notes, company contact info), p02 ... =
                                    proof pages (SVG editable, PNG 300 ppi)
          QA_Checklist/SVG/ + PNG/  "... - qa01" ... for the QA manager
          QA_Checklist/"PRINT - ... - QA checklist.pdf"   all QA pages in one
                                    letter-size PDF, ready to print
          QA_Checklist/"... - QA checklist.csv"   (Excel / Sheets)
          package_info.txt          ticket, customer, project, file location,
                                    page names (read by the CorelDRAW macro)
          The zip itself is "Ticket - Customer - Project.zip".
        Every yellow MISSING tag in an SVG is its own group with an empty
        text box underneath in the matching style: delete the tag, type.
        SVG text is Arial and editable; drawings are vector; the watermark
        is a flat image on its own layer.
        Added images are cropped to the art board in the SVG (no clipping
        paths), so CorelDRAW imports them as plain images, not PowerClips.
        Proof_Template switches: Cover_Page, Cover_Title, QA_Checklist,
        QA_Final_Checks (checks separated by |).


CHANGELOG
-----------------------------------------------------------------------------
v2.3  (2026-10-13)
  Added
    - Proof Generator menu in the Google Sheet (new Apps Script file
      Updater): Update from GitHub, Import workbook from Drive and About this
      version (code, sheet data and latest release versions).
    - Update from GitHub: reads the latest release and updates this sheet in
      place; no new spreadsheet. It backs up Component_Registry,
      Component_Schema, Product_Assembly, Detail_Drawings and Design_Guide as
      hidden "(backup ...)" tabs (the last 3 per tab), then replaces them
      with the release's rows. These five tabs are release-managed: edit them
      through a release, not by hand.
    - Proof_Template merge: new keys are added, and your own wording is kept.
      A value you never changed that the release updated (e.g. DESIGN PROOF
      to SALES PROOF) is listed for you to accept or skip.
    - Code updates itself (when the Apps Script API is on for your Google
      account, a one-time switch): changed files are written into the
      project, saved as a new script version, and the web app deployment
      moves to it, with the same link. If Google blocks it, the summary lists
      exactly which files changed since your version and how to paste them.
    - Import workbook from Drive: finds the newest
      Sign_Proof_Specifications_App_Data .xlsx in your Drive (or pick from a
      list), converts it in the background and updates the tabs the same way.
      Afterwards the .xlsx and its temporary converted copy are moved to the
      Drive trash (recoverable for 30 days); you can trash older copies in
      the same step. If anything fails, nothing is trashed.
    - Each release now includes 1_Google_Sheet/App_Data.json: the app's data
      tabs as plain text, which the update reads.
  Never
    - Saved_Proofs, the color tabs (Paint, vinyl, Pantone ...),
      Product_Schema, README and any tab of your own.
  Setup
    - New Apps Script file Updater (script) and the new appsscript.json
      (Project Settings > Show "appsscript.json" manifest file in editor,
      then paste). Reload the sheet: the Proof Generator menu appears; the
      first run asks for permission (Sheets, Drive, external requests,
      managing this script and its deployments).
    - One-time, for automatic code updates:
      script.google.com/home/usersettings > Google Apps Script API: On.

v2.2  (2026-10-13)
  Added
    - Autosave: about every 30 seconds after a change, the package is saved
      as a draft. Each proof has one draft file that is overwritten in place
      (a never-saved package gets one file in Proof Library/_Drafts), so no
      files pile up, and drafts never become versions: only Save makes v1,
      v2, v3 ... The top bar shows "Draft saved 2:14 PM".
    - Unsaved changes are protected: closing the tab with unsaved changes
      shows the browser's "Leave site?" warning; the next visit offers
      Restore for the unsaved work. Drafts are listed in Saved proofs (Open /
      Discard), and opening a proof that has autosaved changes offers them
      first. Saving a version clears its draft.
    - Approval status: every saved version has a status: Draft, Sent to
      Customer, Changes Requested, Approved or Cancelled. Choose it in the
      Save dialog or change it in Saved proofs without opening the proof; it
      shows as a colored chip in the library and the top bar, the library can
      be filtered by status, and the Saved_Proofs tab records who changed it
      and when (Status, Status_By, Status_At columns, added automatically to
      existing tabs).
    - New from this: a button in Saved proofs that starts a new proof from
      any version, keeping every product, section, spec, image and
      measurement line and clearing the customer info. Its first save is v1
      of a new proof.
  Changed
    - Versions instead of revisions: saved proofs are numbered v1, v2, v3 ...
      everywhere in the app (top bar, Save dialog, Saved proofs, messages).
      The Saved_Proofs tab keeps its Rev column name so existing rows keep
      working. The Revision Date on the proof pages is unchanged.

v2.1.2  (2026-10-13)
  Changed
    - Monument Letters can be front lit or halo lit. Lighting is now the
      first construction choice (Non-Lit, Front Lit, Halo Lit or Ground Lit
      by others), and it decides which material fields appear:
      - Non-lit / ground lit: letter type (flat cut aluminum, fabricated
        aluminum, cast, stainless, brass, acrylic, PVC, HDU), plate
        thickness, or face / return gauge and depth for fabricated letters;
        finish and paint color.
      - Front lit (built like channel letters): 3/16" acrylic or
        polycarbonate face, face color, translucent vinyl and its color, trim
        cap size and color, return gauge, depth (2" to 6") and return (coil)
        color, LED color, power supply and photo cell.
      - Halo lit (reverse channel): aluminum face gauge, return gauge, depth,
        clear polycarbonate or acrylic back, finish and paint color, return
        color, LED color, diffuser vinyl, power supply and photo cell.
    - Front lit monument letters show the Front Lit Section and Trim Cap &
      Return detail drawings, halo lit ones the Halo Lit Section, and both
      get the lit-sign Design Help rules. The top-mount drawings label the
      thickness or depth that applies.
    - Cleaner field labels: fields that exist in two versions (e.g. FACE
      GAUGE for halo and unlit letters, OVERALL DEPTH for single / double
      sided EMCs) show just the plain name in the form.

v2.1.1  (2026-10-13)
  Changed
    - Download page / Download table: the single Download SVG button is now
      two deep blue buttons at the right end of each page's bar.
      - Download page saves the whole page as an SVG, identical to and named
        like the file in the package zip (also on the cover and QA pages).
      - Download table saves only that page's spec table with its product
        label, as an SVG cropped to the table at true size (1 unit = 0.01"),
        named ... - p02 - table.svg. It appears on every page that has a spec
        table.

v2.1  (2026-10-13)
  Added
    - Monument Letters: a new component (blue Letters family, with its own
      icon) and an optional section in Monument Signs, for permanent 3D
      letters on a monument or free-standing sign.
      - Letters: quantity counted from the text, letter height, text, font,
        and + Add Letters for more sizes.
      - Material: flat cut aluminum, fabricated aluminum (reverse channel),
        cast aluminum, flat cut stainless, brass, acrylic or PVC, or routed
        HDU. Flat cut, cast and HDU letters list their plate thickness (1/8"
        to 2"); fabricated letters list face gauge (.040 to .125), return
        gauge (.040 to .063) and depth (1-1/2" to 6").
      - Finish (painted, brushed, polished, anodized, natural) with a paint
        color picker, and return color on painted fabricated letters.
      - Mounting: Top Mount - Pinned (default: letters stand on the cap with
        threaded pins set in epoxy, with pin size and embed depth), Top Mount
        - Adhesive, face mounted with studs (flush or with spacers), or
        Standoffs (model AL25-30A or AL16-25A, size and finish, as on
        panels). Monument surface and a full-size mounting pattern.
      - Lighting: non-lit, halo lit (LED color, power supply, photo cell) or
        ground lit by others.
      - Two new detail drawings, TOP MOUNT - PINNED and TOP MOUNT - ADHESIVE;
        face mounting uses the existing stud and stand-off drawings and halo
        lit letters the halo section. New Design Help rule L08.
    - Color matching: the custom color panel takes a HEX code as well as CMYK
      and RGB, and lists Closest matches: the 3 nearest Sherwin-Williams
      colors, the 3 nearest Pantone colors and, on vinyl fields, the 3
      nearest Oracal colors in that field's series, ranked by Delta E 2000.
      Clicking a match selects that swatch where the field offers the
      library, otherwise it names the custom color after it. Matches are
      based on screen colors; confirm with a physical swatch.
    - Swatch search: every color and pictogram library has a search box
      (name, number or series; several words narrow it down). Enter picks the
      first result; Esc closes.
    - Download SVG per page: a deep blue Download SVG button at the right end
      of every page's bar (cover, proof pages and QA pages) saves that page
      alone, identical to and named like the file in the package zip.
    - + Add Another everywhere: every section of every product and component
      can now be added again (Pole Cover and others were missing it). The
      added copy of an optional section is always included.
  Changed
    - Sales Proof: the proof is now called a Sales Proof. The button reads
      Generate Sales Proof Package, the cover title is SALES PROOF PACKAGE
      and each page's sidebar says SALES PROOF (Proof_Template: Title,
      Cover_Title).

v2.0  (2026-10-13)
  Added
    - Proof Library (saved, editable proofs): Save in the top bar stores the
      whole package in a shared Proof Library folder in Google Drive, next to
      the Google Sheet. That covers every product and section, field value,
      custom table, letter line, vinyl color list, special note, blank page,
      unchecked detail drawing, customer field, artwork image (with its size
      and position) and measurement line. A Saved_Proofs tab in the sheet
      lists every save.
    - Revisions: each save of an opened proof becomes the next revision (Rev
      1, Rev 2 ...) with an optional note; earlier revisions are never
      overwritten. Save as a new proof makes a copy with its own revision
      history.
    - Saved proofs: a searchable list (customer, project, ticket, designer or
      product) with a revision picker. Open rebuilds the package exactly as
      saved so it can be edited and exported again. New starts an empty
      package. Also on the dashboard as Open a saved proof.
    - Images are stored once per proof and shared by all its revisions.
      Proofs are saved as plain JSON, ready to move into a database later.
    - Dashboard filter: the color key above the cards toggles sign families
      on and off (several at once, combined with the search box); Show all
      resets it. Sections with no matches hide.
  Changed
    - New look (Material style): light tonal surfaces, Roboto, pill buttons,
      a segmented step control, outlined fields with a focus ring, rounded
      dialogs, a snackbar for messages and a light grey canvas behind the
      proof pages. Proof pages and exports are unchanged.
    - Dashboard cards: an even outline in the family color all the way around
      each card, with the product name and icon in the same color. Selected
      cards are tinted and show their order number.
  Setup
    - New Apps Script file ProofLibrary (script). Approve the Google Drive
      permission the first time someone saves. The web app must stay Execute
      as: Me so every designer can use the library.

v1.9.5  (2026-10-13)
  Added
    - Multiple vinyl colors: every vinyl color field has a + Add Color
      button, like + Add Letters on channel letters, so one vinyl proof can
      list all of its colors. Each added color has its own Oracal series,
      swatch picker, -- Custom Input -- and Custom CMYK / RGB panel, and
      starts on the series chosen above it.
    - On the proof, QA checklist and CSV the colors print as numbered rows
      (e.g. VINYL COLOR 1, VINYL COLOR 2, VINYL COLOR 3), each with its color
      chip. An added color left unpicked prints as MISSING; [x] Remove takes
      one out and the rest renumber.
    - Works on every vinyl field, including Cut Vinyl Decal, channel letter
      face vinyl and vinyl rows in custom tables. + Add Another on channel
      letter and custom sections copies the color list; a field that lists
      several colors widens to the full row.

v1.9.4  (2026-10-13)
  Changed
    - Cloud signs replace cloud letters: the Cloud Letters products and the
      separate Cloud section are gone. In their place are two products of
      their own, Cloud Sign - Front Lit and Cloud Sign - Halo Lit, completely
      separate from channel letters. A customer can order a cloud sign
      without channel letters; for letters on a cloud, select both the
      channel letters and the cloud sign.
    - Cloud sign specs: a cloud sign has a typed QUANTITY and CLOUD SIZE (W x
      H) instead of letter count, letter height and text. Everything else
      matches the channel letters: face, face color and vinyl, return, return
      color, trim cap, LED, mounting and raceway size on the front lit sign;
      face, face graphics, return, backs, diffuser, standoffs and wall
      surface plus the illumination fields (photo cell defaults to Yes) on
      the halo lit sign. + Add Letters stays on channel letters only.
    - Drawings and help rules: the front lit, halo lit, trim cap, raceway and
      flush mount drawings apply to cloud signs, as do the lit-sign Design
      Help rules. The letter-only rules (letter cap height, letter cut files,
      halo letter stroke) don't. The flush mount drawing is now titled "FLUSH
      MOUNT (LETTERS / CLOUD)".
  Added
    - Dashboard icons: every product and component card has a one-color icon
      showing the general shape of that sign type (letters, cloud, pole sign,
      monument, cabinet, EMC module grid, panels, banner, decal, ADA and
      more).
    - Color families: each card is outlined in its family color, with a
      legend above the list: blue for channel letters and cloud signs, purple
      for cabinets and digital, orange for pole, monument and ground signs,
      green for panels, pink for vinyl and banners, teal for ADA, and red for
      custom tables. Selected cards are tinted in their family color.

v1.9.3  (2026-10-13)
  Added
    - Build Custom Table: a new Custom area on the main screen, below
      Products and Components. Click + Build Custom Table, name the product
      (e.g. "Pylon Topper"), and it is added to the package like any other
      product. The name can be changed on the main screen or on the specs
      step.
    - Title + description rows: each row of a custom table has a title you
      type (printed as the label on the proof) and a description. A new table
      starts with QUANTITY, SIZE and two blank rows; + Add Row adds more and
      × removes one. Fully blank rows are left off the proof, and a row with
      a title but no description prints as MISSING.
    - Description types: text, size (W x H or W x H x D), paint
      (Sherwin-Williams / PMS / custom CMYK and RGB), finish, Oracal vinyl,
      ACM, acrylic, PVC, Coroplast, trim cap, return / coil and LED colors,
      Rowmark and ADA pictogram. They use the same swatch pickers and custom
      color panel as the rest of the app.
    - Columns: each row has a column picker (Col 1 to 6) that sets where it
      prints in the proof table.
    - Sections and components: + Add Section adds another custom table to the
      same product, + Add Component... adds any existing component (poles,
      illumination, footer, EMC and more), and + Add Another copies a custom
      section with its values. Sections can be removed.
    - Detail drawings: each custom section has a Detail drawings checklist of
      all detail drawings; checked ones print on that section's proof page.
    - Custom vinyl: every vinyl field's Oracal series dropdown has a --
      Custom Input -- choice with a text box for any vinyl not in the list
      (e.g. 3M 3630-33 Red). The Custom checkbox can add CMYK / RGB values to
      it.
    - Custom tables work with everything else: New page, blank pages, special
      notes, quantity tags on the cover, measurement lines, the QA checklist
      and CSV, and the SVG / PNG export.
  Notes
    - Custom tables are kept with the current package only, like images and
      measurement lines. Index.html changed in this version (the new Custom
      area).

v1.9.2  (2026-10-13)
  Added
    - Cloud letter components: Cloud Letters - Front Lit and Cloud Letters -
      Halo Lit can now be added as stand-alone components. Each one has every
      face, trim cap, return, back, illumination, mounting and raceway option
      of the matching channel letters, plus the cloud fields (size, depth,
      material, color, lighting). The halo version also includes the
      illumination fields (power supply, photo cell, timer). Letter detail
      drawings and Design Help rules apply to them as they do to channel
      letters.
    - + Add Letters: front-lit, halo-lit and cloud letter sections have a +
      Add Letters button that adds a simple Quantity / Letter Height / Text
      line inside the section. The quantity is counted from the text, the
      height carries over from the line above, and each line prints on the
      proof as its own QTY / HEIGHT and TEXT rows. Lines can be removed with
      ×.
    - EMC specs from production: the Digital Sign (EMC) section now uses
      9.45" x 9.45" modules. Enter modules wide and high to get the display
      size. Pixel pitch offers FLEX Ultra Resolution (5, 6, 8, 10mm) and FLEX
      Enhanced Resolution (12, 16, 20mm). Depths default to 1.5" modules, a
      5" LED cabinet and a 3" back angle. The overall depth and the cabinet
      depth are calculated, with modules extending past the cabinet: single
      sided is 9.5" overall in an 8" cabinet, and double sided on a 4" pole
      is 23" overall in a 20" cabinet.
    - Calculated fields: a new calc field type in Component_Schema shows a
      read-only value worked out from other fields in the same section.
      Number fields can show a unit (e.g. ") set in Options.
  Changed
    - The section button is + Add Another … again; it copies the whole
      section with its settings.
    - The custom color checkbox under swatch pickers is labelled Custom, so
      it no longer gets cut off.
    - Cloud is no longer offered on its own in the component list. Use the
      two cloud letter components, or add Cloud to a cloud letter product.

v1.9.1  (2026-10-13)
  Fixed
    - Measurement lines stay out of the way: lines can now only be selected,
      moved or resized while that page's Measure mode is on. Outside Measure
      mode they ignore the mouse, so dragging an image underneath a line
      moves the image and never the line. Lines are still removed with the x
      beside their value in the page toolbar.

v1.9  (2026-10-12)
  Added
    - Custom colors with CMYK and RGB: choosing Custom on a color field
      (material, face, paint, vinyl, return, trim cap, LED and Rowmark
      colors) opens a panel for a color name plus CMYK and RGB values. Type
      either set and the other is calculated and marked "(approx.)"; the
      proof prints the name and both sets.
    - New page toggle: each section card has a "New page" checkbox that
      starts that section's table on a new proof page.
    - Blank pages: "+ Add Blank Page" under each product adds a page with the
      sidebar, watermark and an empty art board, for elevations, mockups or
      site photos. Each blank page has an editable title (default "Page")
      shown in its footer and in the cover's Package Contents.
    - Standoffs: ACM, PVC, Acrylic, HDU and ADA signs with standoff mounting
      now have STANDOFF MODEL (AL25-30A, AL16-25A or Custom), STANDOFF SIZE
      (filled in from the model, editable) and STANDOFF FINISH (Brushed
      Aluminum, Satin Aluminum, Black, Chrome, Gold or Custom). Halo-lit and
      front-lit channel letters keep their existing standoff options.
    - Cloud letters: new products Cloud Letters - Front Lit and Cloud Letters
      - Halo Lit use the same letter settings and detail drawings as their
      channel letter counterparts, plus a Cloud section (size, depth,
      material, color, lighting). Cloud is also available as a stand-alone
      component.
    - Raceway size: front-lit channel letters and front-lit cloud letters
      mounted on a raceway get a RACEWAY SIZE field (L x H x D).
    - + Add Letters: on front-lit and halo-lit letters (including cloud
      letters), adds another letter set that copies the previous set's
      settings, for mixed letter sizes in one project. Every set stays
      editable.
    - Measurement lines: a Measure button on each page's toolbar. Click, drag
      and release to draw a red dimension line (hold Shift to keep it
      straight), type its value in inches, then move it or drag its ends.
      Lines export as editable SVG lines and text in a Measurements group.
  Changed
    - SVG export: added images are cropped to the art board instead of
      clipped, so CorelDRAW imports them as plain images rather than locked
      PowerClips.
    - Mounting detail: on ACM, PVC, Acrylic and HDU, the MOUNT DETAIL text
      box no longer appears for standoffs; the new standoff fields replace
      it.

v1.8  (2026-10-08)
  Added
    - Special notes per section: every section in the proof builder has an
      Add Special Notes checkbox and text box. The notes print in a
      gold-edged SPECIAL NOTES column to the right of that section's table on
      the proof sheet. This restores the special notes from the original app,
      now one per section.
    - Unchecking Add Special Notes hides the notes from the proof but keeps
      the text, so checking it again brings them back.
    - Quantities on the cover page: Package Contents rows show the quantity
      from each section's Quantity field in bold red, e.g. (x2) Main Menu
      Boards. Single-section items show it on the main row, e.g. (x1) Banner.
      The tag appears on the cover only.
  Changed
    - Cover page: the proof pages column in Package Contents now reads "Page
      2", or "Pages 3 - 5" for a range.
    - Sections with a blank quantity show no tag, and sections with the same
      name have their quantities added together.
    - Pages with special notes add a notes column to the spec table. Sections
      without notes on the same page get a plain gray cell, and the table
      scales to fit.

v1.7  (2026-10-08)
  Added
    - Editable section names: the red section title on each part card in the
      proof builder (e.g. "Acrylic 2") is now a plain-text field. Type a
      specific name such as "Front Menu" or "Side Menu".
    - Renamed sections carry through to the proof sheet section heading, the
      cover page's package contents sub-rows, the QA checklist pages and the
      QA .csv.
    - Clearing the field and pressing Enter (or clicking away) returns the
      section to its default name.
  Changed
    - Section numbering: a single section keeps its plain name ("Acrylic").
      Once + Add Another is used, sections are numbered ("Acrylic 1",
      "Acrylic 2", "Acrylic 3"). Sections that haven't been renamed renumber
      automatically when one is removed (Acrylic 3 becomes Acrylic 2), while
      renamed sections keep their names.

v1.6  (2026-10-08)
  Added
    - QA checklist print PDF: all QA pages are combined into one multi-page
      letter-size PDF, saved as QA_Checklist/PRINT - … - QA checklist.pdf
      next to the SVG, PNG and CSV versions. The PDF is built in the browser,
      so nothing extra is required.
    - Sub-customer field: a Sub-customer checkbox on the Customer Info step
      shows a Sub-Customer Name field. A blank sub-customer is flagged as
      MISSING.
    - File names include the sub-customer right after the customer: Ticket -
      Customer - Sub-Customer - Project - p01. The same names are used for
      the zip, the QA files and the CorelDRAW .cdr.
    - package_info.txt now records SubCustomer= and FileBase=.
    - When Sub-customer is checked, the sub-customer name prints next to the
      customer name as Customer - Sub-Customer. This applies to every proof
      sheet (the red sidebar box), the cover page and the QA checklist
      header.
    - The QA checklist header text shrinks to fit long customer and
      sub-customer names, so it no longer gets cut off.
  Changed
    - Cover page: the "This design and engineering…" legal text and the
      copyright line now sit on the same baseline.
    - CorelDRAW macro: the folder picker is back to the classic Browse for
      Folder window. The Explorer-style picker was tried and removed because
      it only let you select single files, not a folder. A typed-path box
      appears only if the Windows Shell is unavailable.

v1.5  (2026-10-08)
  Added
    - Cover page:
      - A project notes summary box, filled from a new Project Notes field.
      - A company contact line (name, address, phone, website, email). It
        comes from the Company_ keys on the Proof_Template tab, and blank
        keys are skipped.
    - Page selection for pasting can now be cleared. You can click the page
      bar again, press Esc or click the background to deselect the
      gold-outlined page.
    - Choose where to save: Chrome and Edge open a save dialog for the zip
      when the browser allows it. It falls back to a normal download inside
      the Apps Script frame.
    - MISSING tags in SVGs: each tag is its own group, with an empty text box
      underneath in the matching style. Delete the tag and type, with no need
      to edit the label.
    - New export file names: Ticket - Customer - Project - p01.svg (QA: -
      qa01), and the zip is named Ticket - Customer - Project.zip.
    - package_info.txt in the zip holds the ticket, customer, project, file
      location and page names.
    - CorelDRAW macro module (ProofPages_CorelDRAW_Macro.bas):
      - ImportProofPackage creates one page per SVG in the open 8.5 × 11
        template. Each sheet is scaled to fill and the orientation is
        matched.
      - Pages are named from the files, and the QA pages are optional.
      - One Undo reverses the whole import.
      - The file is saved automatically as Ticket# - Customer - Project.cdr,
        in the job folder taken from the proof's File Location.
      - BuildFromPackage and AddProofPages from v1.2 are kept in the same
        module.
  Changed
    - Export folders: SVGs and PNGs are in separate SVG/ and PNG/ folders,
      and QA_Checklist/ has its own SVG/ and PNG/ subfolders.
  Fixed
    - CorelDRAW macro: fixed the "Can't assign to read-only property" compile
      error. The macro no longer sets doc.Title, and version-specific members
      are late-bound so it works across CorelDRAW versions.

v1.4  (2026-10-08)
  Changed
    - Cover contents list: each product is a bold row, with its sections as
      indented sub-rows (1.1, 1.2 …) that list their proof pages. Large
      packages flow into two columns.
    - Watermark:
      - Now one flat, non-editable image instead of text.
      - Covers the whole art board, cropped at the art board edges.
      - Set to 2% gray through the new Proof_Template › Watermark_Opacity
        setting.
      - Has no transparency, so CorelDRAW shows exactly what the preview
        shows.
    - QA checklist:
      - One checkbox beside each product or component title.
      - An OK / INIT line to the right of every individual spec.
      - Final Checks and QA Manager sign-off moved into a separate
        red-outlined section at the bottom of the last page.
      - Notes area expanded from 2 to 10 lines.

v1.3  (2026-10-08)
  Added
    - Artwork images on proof pages: use the + Add image bar above any page,
      drop a file on it, or select the page and paste a screenshot (Ctrl+V).
      - Images fit the open art board space and can be dragged, sized with −
        / + / Fit, or removed with ×.
      - They are embedded in the SVG (on an Artwork layer) and in the PNG.
  Changed
    - Cover page: the customer approval block was removed, leaving only the
      legal and copyright line.
    - Watermark: lightened, and changed to a solid tint because CorelDRAW
      ignores SVG opacity.
    - Detail drawings: the halo glow is now solid, with no transparency.
  Fixed
    - SVG text showed entity codes such as &quot; in CorelDRAW. Text is now
      written as plain UTF-8: inch marks are kept as-is, and lines containing
      & or < are wrapped in CDATA.
    - Uploading several artwork files at once no longer drops images, caused
      by a timing issue between the uploads.

v1.2  (2026-10-08)
  Added
    - Cover page (page 1): Sign Store logo, customer name, project name,
      project info and a full list of products and components with their page
      numbers.
    - QA checklist:
      - Exported in its own QA_Checklist/ folder, with every spec and its
        checkbox and initials, the detail drawings, final checks and QA
        Manager sign-off.
      - Also exported as a .csv for Excel and Sheets.
      - Can be switched on or off with Proof_Template › QA_Checklist.
    - A separate Project Name field, also shown under the customer in the red
      sidebar box.
    - An × button that clears a chosen ADA pictogram.
    - First CorelDRAW page macros: AddProofPages adds blank pages up to a
      total, and BuildFromPackage builds a document with one page per SVG.

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
