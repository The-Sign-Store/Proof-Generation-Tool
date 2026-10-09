function doGet() {
  // Use createTemplateFromFile instead of createHtmlOutput so we can pull in our CSS/JS files
  return HtmlService.createTemplateFromFile('Index')
      .evaluate()
      .setTitle('Sign Proof Generator')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// Stitches the HTML files together
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

function getAppData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // ---------- LEGACY PRODUCTS (unchanged) ----------
  const schemaSheet = ss.getSheetByName('Product_Schema');
  const schemaData = schemaSheet.getDataRange().getValues();
  schemaData.shift();

  let products = {};
  schemaData.forEach(row => {
    let [product, zone, variable, def, options] = row;
    if (!product || String(product).trim() === 'Product') return; // skip blanks + repeated header rows
    if (!products[product]) products[product] = [];
    products[product].push({ zone: String(zone).trim(), variable: String(variable).trim(), default: String(def), options: String(options) });
  });

  function fetchColorTab(tabName) {
    let sheet = ss.getSheetByName(tabName);
    if (!sheet) return [];
    let data = sheet.getDataRange().getValues();
    if (data.length < 2) return [];

    let headers = data.shift().map(h => String(h).toUpperCase());

    let nameIdx = headers.findIndex(h => h.includes('NAME') || h.includes('PMS'));
    let hexIdx = headers.findIndex(h => h.includes('HEX'));
    let seriesIdx = headers.findIndex(h => h.includes('SERIES'));
    let codeIdx = headers.findIndex(h => h === 'COLOR_CODE' || h === 'COLOR CODE');

    if (nameIdx === -1) nameIdx = 1;
    if (hexIdx === -1) hexIdx = 2;

    return data.map(row => ({
        series: seriesIdx !== -1 ? String(row[seriesIdx]).trim() : "",
        code: codeIdx !== -1 ? String(row[codeIdx]).trim() : "",
        name: String(row[nameIdx]).trim(),
        hex: String(row[hexIdx]).trim()
    })).filter(c => c.name !== "");
  }

  // ---------- MODULAR ENGINE (components + assemblies) ----------
  // Reads a tab into an array of objects keyed by header name.
  function readTable(tabName) {
    let sheet = ss.getSheetByName(tabName);
    if (!sheet) return [];
    let data = sheet.getDataRange().getDisplayValues(); // display values keep 3/16" etc. as typed
    if (data.length < 2) return [];
    let headers = data.shift().map(h => String(h).trim());
    return data
      .filter(r => String(r[0]).trim() !== '' && String(r[0]).trim() !== headers[0])
      .map(r => {
        let o = {};
        headers.forEach((h, i) => o[h] = String(r[i] === undefined ? '' : r[i]).trim());
        return o;
      });
  }

  let components = {};
  readTable('Component_Registry').forEach(r => {
    components[r.Component_ID] = {
      id: r.Component_ID,
      name: r.Display_Name || r.Component_ID,
      tool: String(r.Show_As_Tool).toUpperCase() === 'YES',
      repeatable: String(r.Repeatable).toUpperCase() === 'YES',
      description: r.Description || '',
      fields: []
    };
  });
  readTable('Component_Schema').forEach(r => {
    let c = components[r.Component_ID];
    if (!c) return;
    c.fields.push({
      zone: r.Zone || 'COLUMN 1',
      variable: r.Variable,
      label: r.Label || r.Variable,
      type: (r.Type || 'text').toLowerCase(),
      def: r.Default,
      options: r.Options,
      showIf: r.Show_If,
      required: String(r.Required).toUpperCase() === 'YES',
      notes: r.Notes || '',
      hideValues: r.Hide_Values || ''
    });
  });

  let assemblies = {};
  readTable('Product_Assembly').forEach(r => {
    if (!assemblies[r.Product]) assemblies[r.Product] = [];
    assemblies[r.Product].push({
      order: Number(r.Order) || 0,
      component: r.Component_ID,
      title: r.Section_Title || '',
      include: r.Include || 'Required',
      repeatable: String(r.Repeatable).toUpperCase() === 'YES',
      overrides: r.Default_Overrides || '',
      pageGroup: Number(r.Page_Group) || Number(r.Order) || 0
    });
  });
  Object.keys(assemblies).forEach(p => assemblies[p].sort((a, b) => a.order - b.order));

  let pictograms = readTable('ADA_Pictograms')
    .filter(r => String(r.Is_Active).toUpperCase() !== 'FALSE')
    .map(r => ({ code: r.Item_Code, category: r.Category, name: r.Name, viewBox: r.ViewBox, path: r.SVG_Path }));

  // Fixed text printed on every proof page (title, ETL, legal, copyright)
  let template = {};
  readTable('Proof_Template').forEach(r => template[r.Key] = r.Value);

  // Detail drawings: printed bottom-right of the art board when a page's specs match Match_Rule
  let drawings = readTable('Detail_Drawings')
    .filter(r => String(r.Active).toUpperCase() !== 'NO' && r.SVG_Markup)
    .map(r => ({
      id: r.Drawing_ID,
      category: r.Category || '',
      title: r.Title || r.Drawing_ID,
      components: String(r.Components || '').split(',').map(s => s.trim()).filter(s => s),
      rule: r.Match_Rule || '',
      order: Number(r.Order) || 999,
      svg: r.SVG_Markup
    }));

  // Design standards for the Help Center pop-up (step 2)
  let guide = readTable('Design_Guide')
    .filter(r => String(r.Active).toUpperCase() !== 'NO' && r.Standard)
    .map(r => ({
      id: r.Rule_ID,
      section: r.Section || 'GENERAL',
      components: String(r.Components || '').split(',').map(s => s.trim()).filter(s => s),
      rule: r.Match_Rule || '',
      text: r.Standard,
      why: r.Why || '',
      how: r.CorelDRAW_How_To || '',
      basis: r.Basis || '',
      order: Number(r.Order) || 9999
    }));

  // Returned as a JSON string: Apps Script silently drops results containing Dates or other
  // unsupported values, which leaves the page stuck on "Loading...".
  return JSON.stringify({
    template: template,
    products: products,
    components: components,
    assemblies: assemblies,
    pictograms: pictograms,
    drawings: drawings,
    guide: guide,
    colors_oracal: fetchColorTab('Oracal_Colors'),
    colors_sw: fetchColorTab('SW_Colors'),
    colors_pms: fetchColorTab('PMS_Colors'),
    colors_acm: fetchColorTab('ACM_Colors'),
    colors_acrylic: fetchColorTab('Acrylic_Colors'),
    colors_pvc: fetchColorTab('PVC_Colors'),
    colors_coro: fetchColorTab('Coro_Colors'),
    colors_coil: fetchColorTab('Coil_Colors'),
    colors_trimcap: fetchColorTab('TrimCap_Colors'),
    colors_led: fetchColorTab('LED_Colors'),
    colors_finish: fetchColorTab('Finish_Colors'),
    colors_rowmark: fetchColorTab('Rowmark_Colors')
  });
}
