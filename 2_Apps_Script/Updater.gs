function myFunction() {}

/**
 * v2.3: "Proof Generator" menu in the Google Sheet.
 *
 *   Update from GitHub   - reads the latest release (1_Google_Sheet/App_Data.json on the main branch),
 *                          backs up and replaces the five app tabs IN PLACE, merges Proof_Template,
 *                          then updates the Apps Script code + web app (Apps Script API) or lists the
 *                          files to paste by hand.
 *   Import workbook      - same tab update from a Sign_Proof_Specifications_App_Data .xlsx in Drive;
 *                          the .xlsx (and the temporary converted copy) go to the trash afterwards.
 *
 * Never touched: Saved_Proofs, the color tabs, Product_Schema, README or any other tab.
 */
const UPD_REPO = 'The-Sign-Store/Proof-Generation-Tool';
const UPD_RAW = 'https:' + '//raw.githubusercontent.com/' + UPD_REPO + '/main/';
const UPD_WEB = 'https:' + '//github.com/' + UPD_REPO;
const UPD_API = 'https:' + '//script.googleapis.com/v1/projects/';
const UPD_SETTINGS = 'https:' + '//script.google.com/home/usersettings';
const MANAGED_TABS = ['Component_Registry', 'Component_Schema', 'Product_Assembly', 'Detail_Drawings', 'Design_Guide'];
const TEMPLATE_TAB = 'Proof_Template';
const BACKUPS_KEPT = 3;            // per tab; older backups are deleted
const WORKBOOK_NAME = 'Sign_Proof_Specifications_App_Data';

function onOpen() {
  let ui;
  try { ui = SpreadsheetApp.getUi(); }
  catch (e) {   // run from the script editor: there is no sheet window to add a menu to
    console.log('The Proof Generator menu is added when the Google Sheet opens. Reload the sheet to see it.');
    return;
  }
  ui.createMenu('Proof Generator')
    .addItem('Update from GitHub', 'updateFromGitHub')
    .addItem('Import workbook from Drive', 'importWorkbook')
    .addSeparator()
    .addItem('About this version', 'aboutVersion')
    .addToUi();
}

// ---------------------------------------------------------------- versions
function updVer_(v) { return String(v || '0').replace(/^v/, '').split('.').map(n => parseInt(n, 10) || 0); }
function updNewer_(a, b) {                 // a > b
  const x = updVer_(a), y = updVer_(b);
  for (let i = 0; i < Math.max(x.length, y.length); i++) { if ((x[i] || 0) !== (y[i] || 0)) return (x[i] || 0) > (y[i] || 0); }
  return false;
}
/** Version of the pasted / installed code, read from JavaScript.html (the packager writes it there). */
function installedCodeVersion_() {
  try {
    const m = HtmlService.createHtmlOutputFromFile('JavaScript').getContent().match(/const APP_VERSION = '([^']+)'/);
    return m ? m[1] : 'unknown';
  } catch (e) { return 'unknown'; }
}
/** v2.3.1: the version open proof tool tabs compare themselves with (cached 10 minutes; only reads JavaScript.html). */
function getLiveVersion() {
  const cache = CacheService.getScriptCache(), hit = cache.get('LIVE_VERSION');
  if (hit) return hit;
  const v = installedCodeVersion_();
  cache.put('LIVE_VERSION', v, 600);
  return v;
}
function dataVersion_() { return PropertiesService.getScriptProperties().getProperty('DATA_VERSION') || 'unknown'; }
function label_(v) { return /^\d/.test(v) ? 'v' + v : v; }

function aboutVersion() {
  const ui = SpreadsheetApp.getUi();
  let latest = '(could not reach GitHub)';
  try { latest = label_(fetchRelease_().version); } catch (e) {}
  ui.alert('Sign Proof Generator',
    'Apps Script code: ' + label_(installedCodeVersion_()) + '\n' +
    'Sheet data tabs: ' + label_(dataVersion_()) + '\n' +
    'Latest release on GitHub: ' + latest, ui.ButtonSet.OK);
}

// ---------------------------------------------------------------- Update from GitHub
function fetchRelease_() {
  const r = UrlFetchApp.fetch(UPD_RAW + '1_Google_Sheet/App_Data.json?t=' + Date.now(), { muteHttpExceptions: true });
  if (r.getResponseCode() !== 200) throw new Error('GitHub answered ' + r.getResponseCode() + ' for App_Data.json');
  const rel = JSON.parse(r.getContentText());
  if (!rel.version || !rel.tabs) throw new Error('App_Data.json is not in the expected format');
  return rel;
}

function updateFromGitHub() {
  const ui = SpreadsheetApp.getUi();
  let rel;
  try { rel = fetchRelease_(); }
  catch (e) { ui.alert('Update from GitHub', 'Could not read the latest release from GitHub.\n\n' + e.message, ui.ButtonSet.OK); return; }
  const code = installedCodeVersion_(), data = dataVersion_();
  const current = code === rel.version && data === rel.version;
  const msg = 'Latest release: v' + rel.version + '\n' +
    'This sheet\'s data tabs: ' + label_(data) + '\nApps Script code: ' + label_(code) + '\n\n' +
    (current ? 'Everything is already on v' + rel.version + '. Run the update again anyway?\n\n' : '') +
    'What happens:\n' +
    '  1. ' + MANAGED_TABS.join(', ') + ' are backed up (hidden tabs), then replaced in place.\n' +
    '  2. Proof_Template: new keys added, your values kept (you are asked about release changes).\n' +
    '  3. The Apps Script code and web app are updated (or you get a list of files to paste).\n\n' +
    'Saved_Proofs, the color tabs and every other tab are not touched.';
  if (ui.alert('Update from GitHub', msg, ui.ButtonSet.YES_NO) !== ui.Button.YES) return;

  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) { ui.alert('Update from GitHub', 'Someone is saving a proof or running an update. Try again in a minute.', ui.ButtonSet.OK); return; }
  try {
    const report = applyData_(rel.tabs, rel.template, false);
    PropertiesService.getScriptProperties().setProperty('DATA_VERSION', rel.version);
    const codeReport = updateCode_(rel, code);
    showSummary_('Updated to v' + rel.version, report.concat([''], codeReport));
  } catch (e) {
    ui.alert('Update from GitHub', 'The update stopped: ' + e.message + '\n\nBackups of any tab already changed are the hidden "(backup ...)" tabs (View > Hidden sheets).', ui.ButtonSet.OK);
  } finally { lock.releaseLock(); }
}

// ---------------------------------------------------------------- tabs
/**
 * tabs: {Tab: [[header...], [row...]...]}; template: {rows: [[Key, Value]...], previous: {Key: [older defaults]}}.
 * askAll: true for a workbook import (no release history) - every differing Proof_Template value is offered.
 * Returns summary lines.
 */
function applyData_(tabs, template, askAll) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd HH.mm.ss');
  const lines = [];
  MANAGED_TABS.forEach(name => {
    const rows = tabs[name];
    if (!rows || !rows.length) { lines.push(name + ': not in the update, left as is'); return; }
    let sh = ss.getSheetByName(name), was = -1;
    if (sh) { was = Math.max(sh.getLastRow() - 1, 0); backupTab_(ss, sh, stamp); }
    else sh = ss.insertSheet(name);
    writeTab_(sh, rows);
    lines.push(name + ': ' + (rows.length - 1) + ' rows' + (was < 0 ? ' (new tab)' : ' (was ' + was + ')'));
  });
  if (template && template.rows && template.rows.length) lines.push.apply(lines, mergeTemplate_(ss, template, askAll, stamp));
  return lines;
}

function writeTab_(sh, rows) {
  const w = Math.max.apply(null, rows.map(r => r.length));
  const data = rows.map(r => {
    const x = r.map(v => {
      const s = v === null || v === undefined ? '' : String(v);
      return s.charAt(0) === '=' ? '\'' + s : s;          // never let a value turn into a formula
    });
    while (x.length < w) x.push('');
    return x;
  });
  sh.clearContents();                                      // keeps column widths, header styling, dropdowns
  if (sh.getMaxColumns() < w) sh.insertColumnsAfter(sh.getMaxColumns(), w - sh.getMaxColumns());
  if (sh.getMaxRows() < data.length + 1) sh.insertRowsAfter(sh.getMaxRows(), data.length + 1 - sh.getMaxRows());
  if (sh.getMaxRows() > 1) sh.getRange(2, 1, sh.getMaxRows() - 1, sh.getMaxColumns()).setBackground(null);  // old row banding
  const rng = sh.getRange(1, 1, data.length, w);
  rng.setNumberFormat('@');                                // plain text: 1/2" and 3/16 stay as typed, not dates
  rng.setValues(data);
  sh.setFrozenRows(1);
}

function backupTab_(ss, sh, stamp) {
  const name = sh.getName(), prefix = name + ' (backup ';
  const copy = sh.copyTo(ss);
  copy.setName(prefix + stamp + ')');
  copy.hideSheet();
  ss.getSheets().filter(s => s.getName().indexOf(prefix) === 0)
    .sort((a, b) => a.getName() < b.getName() ? 1 : -1)
    .slice(BACKUPS_KEPT).forEach(s => ss.deleteSheet(s));
}

function mergeTemplate_(ss, template, askAll, stamp) {
  const ui = SpreadsheetApp.getUi(), prev = template.previous || {};
  const rel = template.rows.slice(1).filter(r => String(r[0] || '').trim());
  let sh = ss.getSheetByName(TEMPLATE_TAB);
  if (!sh) { sh = ss.insertSheet(TEMPLATE_TAB); writeTab_(sh, template.rows); return [TEMPLATE_TAB + ': created (' + rel.length + ' keys)']; }
  const cur = sh.getDataRange().getDisplayValues(), at = {};
  cur.forEach((r, i) => { const k = String(r[0]).trim(); if (i && k && !(k in at)) at[k] = i; });
  const added = [], offer = [], kept = [];
  rel.forEach(r => {
    const k = String(r[0]).trim(), v = String(r[1] === undefined ? '' : r[1]);
    if (!(k in at)) { added.push([k, v]); return; }
    const mine = String(cur[at[k]][1]);
    if (mine === v) return;
    if (askAll || (prev[k] || []).indexOf(mine) >= 0) offer.push({ k: k, from: mine, to: v, row: at[k] + 1 });
    else kept.push(k);
  });
  let take = false;
  if (offer.length) {
    const cut = s => s.length > 70 ? s.slice(0, 67) + '...' : s;
    take = ui.alert('Proof_Template changes',
      (askAll ? 'The workbook has different values for:' : 'This release changed these Proof_Template values (your sheet still has the old ones):') + '\n\n' +
      offer.map(o => o.k + ':\n   "' + cut(o.from) + '"  ->  "' + cut(o.to) + '"').join('\n') +
      '\n\nUse the new values? (No keeps yours.)', ui.ButtonSet.YES_NO) === ui.Button.YES;
  }
  if (!added.length && !(take && offer.length)) {
    return [TEMPLATE_TAB + ': no changes' + (offer.length ? ' (kept your ' + offer.length + ' value' + (offer.length > 1 ? 's' : '') + ')' : '') +
            (kept.length ? '; your own values kept for ' + kept.join(', ') : '')];
  }
  backupTab_(ss, sh, stamp);
  if (take) offer.forEach(o => { const c = sh.getRange(o.row, 2); c.setNumberFormat('@'); c.setValue(o.to); });
  if (added.length) {
    const r = sh.getRange(sh.getLastRow() + 1, 1, added.length, 2);
    r.setNumberFormat('@'); r.setValues(added);
  }
  const out = [];
  if (added.length) out.push('added ' + added.map(a => a[0]).join(', '));
  if (offer.length) out.push((take ? 'updated ' : 'kept your values for ') + offer.map(o => o.k).join(', '));
  if (kept.length) out.push('your own values kept for ' + kept.join(', '));
  return [TEMPLATE_TAB + ': ' + out.join('; ')];
}

// ---------------------------------------------------------------- code (Apps Script API)
function scriptApi_(method, path, body) {
  const opt = { method: method, muteHttpExceptions: true, contentType: 'application/json',
                headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() } };
  if (body) opt.payload = JSON.stringify(body);
  const r = UrlFetchApp.fetch(UPD_API + ScriptApp.getScriptId() + path, opt);
  const text = r.getContentText();
  if (r.getResponseCode() >= 300) {
    let m = text;
    try { m = JSON.parse(text).error.message; } catch (e) {}
    const err = new Error(m); err.status = r.getResponseCode(); throw err;
  }
  return text ? JSON.parse(text) : {};
}

/** Keep this project's own manifest settings (web app access, time zone); take scopes, services and runtime from the release. */
function mergeManifest_(mine, theirs) {
  let a = {}, b = JSON.parse(theirs);
  try { a = JSON.parse(mine || '{}'); } catch (e) {}
  const out = Object.assign({}, a, { runtimeVersion: b.runtimeVersion || a.runtimeVersion, oauthScopes: b.oauthScopes });
  if (!out.timeZone) out.timeZone = b.timeZone;
  if (!out.exceptionLogging) out.exceptionLogging = b.exceptionLogging;
  const svc = ((a.dependencies || {}).enabledAdvancedServices || []).slice();
  ((b.dependencies || {}).enabledAdvancedServices || []).forEach(s => {
    const i = svc.findIndex(x => x.userSymbol === s.userSymbol);
    if (i >= 0) svc[i] = s; else svc.push(s);
  });
  out.dependencies = Object.assign({}, a.dependencies || {}, { enabledAdvancedServices: svc });
  if (!out.oauthScopes) delete out.oauthScopes;
  return JSON.stringify(out, null, 2);
}

function updateCode_(rel, installed) {
  const files = (rel.code && rel.code.files) || [];
  if (!files.length) return ['Apps Script code: not part of this update'];
  try {
    const content = scriptApi_('get', '/content');
    const list = (content.files || []).map(f => ({ name: f.name, type: f.type, source: f.source }));
    const idx = {};
    list.forEach((f, i) => idx[f.name.toLowerCase()] = i);
    const changed = [];
    files.forEach(f => {
      const r = UrlFetchApp.fetch(UPD_RAW + f.path + '?t=' + Date.now(), { muteHttpExceptions: true });
      if (r.getResponseCode() !== 200) throw new Error('could not download ' + f.path + ' (' + r.getResponseCode() + ')');
      let src = r.getContentText();
      const i = idx[f.name.toLowerCase()];
      if (f.type === 'JSON') src = mergeManifest_(i === undefined ? '' : list[i].source, src);
      if (i === undefined) { list.push({ name: f.name, type: f.type, source: src }); changed.push(f.name + ' (new)'); }
      else if (list[i].source !== src) { list[i].source = src; changed.push(list[i].name); }
    });
    if (!changed.length) return ['Apps Script code: already up to date.'];
    scriptApi_('put', '/content', { files: list });
    CacheService.getScriptCache().remove('LIVE_VERSION');   // open proof tool tabs see the new version at their next check
    const ver = scriptApi_('post', '/versions', { description: 'v' + rel.version + ' (Update from GitHub)' });
    const deps = (scriptApi_('get', '/deployments').deployments || []).filter(d =>
      d.deploymentConfig && d.deploymentConfig.versionNumber && (d.entryPoints || []).some(e => e.entryPointType === 'WEB_APP'));
    deps.forEach(d => scriptApi_('put', '/deployments/' + d.deploymentId, {
      deploymentConfig: { scriptId: ScriptApp.getScriptId(), versionNumber: ver.versionNumber, manifestFileName: 'appsscript',
                          description: 'v' + rel.version } }));
    return ['Apps Script code: updated ' + changed.join(', ') + '.',
            'Saved as script version ' + ver.versionNumber + '. ' +
            (deps.length ? 'The web app now runs v' + rel.version + ' (same link). Reload any open proof tool tabs.'
                         : 'No web app deployment found: Deploy > Manage deployments > Edit > Version: New version.')];
  } catch (e) {
    return manualCode_(rel, installed, e);
  }
}

function manualCode_(rel, installed, e) {
  const m = String(e.message || e);
  let why;
  if (/has not enabled the Apps Script API|not enabled.*Apps Script API/i.test(m))
    why = 'Your Google account has the Apps Script API turned off. Turn it on once at ' + UPD_SETTINGS + ' (Google Apps Script API: On), then run Update from GitHub again.';
  else if (/has not been used in project|it is disabled|SERVICE_DISABLED/i.test(m))
    why = 'The Apps Script API is not enabled for this script\'s Google Cloud project (' + m + ').';
  else if (e.status === 403 || /insufficient|permission/i.test(m))
    why = 'Google did not allow the code update (' + m + '). Check that appsscript.json has the v2.3 scopes and that you can edit this script.';
  else why = 'The code update did not run: ' + m;
  const known = /^\d/.test(installed);
  const todo = (rel.code.files || []).filter(f => !known || updNewer_(f.since, installed));
  return ['Apps Script code: NOT updated automatically.', why, '',
          'Paste these files from ' + UPD_WEB + '/tree/main/2_Apps_Script' +
          (known ? ' (changed since v' + installed + ')' : '') + ':']
    .concat(todo.map(f => '   ' + f.path.split('/').pop() + '  ->  ' + f.name + (f.type === 'JSON' ? ' (Project Settings > show appsscript.json)' : '')))
    .concat(['Then Deploy > Manage deployments > Edit > Version: New version > Deploy.']);
}

function showSummary_(title, lines) {
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const link = s => esc(s).replace(/(https:\/\/[^\s)]+)/g, '<a href="$1" target="_blank">$1</a>');
  const html = '<div style="font:14px/1.5 Roboto,Arial,sans-serif;color:#1C1B1F">' +
    lines.map(l => l === '' ? '<div style="height:10px"></div>' : '<div style="white-space:pre-wrap">' + link(l) + '</div>').join('') +
    '<p style="color:#49454F;font-size:12px;margin-top:14px">Backups: hidden tabs named "(backup ...)", the last ' + BACKUPS_KEPT +
    ' per tab (View &gt; Hidden sheets).</p></div>';
  SpreadsheetApp.getUi().showModalDialog(HtmlService.createHtmlOutput(html).setWidth(620).setHeight(420), title);
}

// ---------------------------------------------------------------- Import workbook
function findWorkbooks_() {
  const it = DriveApp.searchFiles('title contains \'' + WORKBOOK_NAME + '\' and trashed = false and mimeType = \'' + MimeType.MICROSOFT_EXCEL + '\'');
  const out = [];
  while (it.hasNext() && out.length < 50) out.push(it.next());
  return out.sort((a, b) => b.getLastUpdated() - a.getLastUpdated());
}

function convertToSheet_(file) {
  const meta = { name: 'TEMP import - ' + file.getName(), mimeType: MimeType.GOOGLE_SHEETS };
  if (typeof Drive !== 'undefined' && Drive.Files && Drive.Files.copy) return Drive.Files.copy(meta, file.getId()).id;
  const r = UrlFetchApp.fetch('https:' + '//www.googleapis.com/drive/v3/files/' + file.getId() + '/copy', {
    method: 'post', contentType: 'application/json', payload: JSON.stringify(meta), muteHttpExceptions: true,
    headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() } });
  if (r.getResponseCode() >= 300) throw new Error('could not convert the workbook (' + r.getContentText().slice(0, 200) + ')');
  return JSON.parse(r.getContentText()).id;
}

function readWorkbookTabs_(id) {
  const book = SpreadsheetApp.openById(id), tabs = {};
  const read = name => {
    const sh = book.getSheetByName(name);
    if (!sh) return null;
    const v = sh.getDataRange().getDisplayValues();
    while (v.length && v[v.length - 1].every(c => c === '')) v.pop();
    return v;
  };
  MANAGED_TABS.forEach(n => { const v = read(n); if (v) tabs[n] = v; });
  const readme = read('README'), tpl = read(TEMPLATE_TAB);
  let version = '';
  (readme || []).some(r => { const m = String(r[0]).match(/^VERSION ([\d.]+)/); if (m) version = m[1]; return !!m; });
  return { tabs: tabs, template: tpl ? { rows: tpl, previous: {} } : null, version: version };
}

function importWorkbook() {
  const ui = SpreadsheetApp.getUi();
  const files = findWorkbooks_();
  if (!files.length) {
    ui.alert('Import workbook', 'No ' + WORKBOOK_NAME + ' .xlsx file was found in your Drive. Upload one, then run Import workbook again.', ui.ButtonSet.OK);
    return;
  }
  const tz = Session.getScriptTimeZone();
  const when = f => Utilities.formatDate(f.getLastUpdated(), tz, 'MMM d, yyyy h:mm a');
  let pick = 0;
  if (files.length > 1) {
    const shown = files.slice(0, 9);
    const res = ui.prompt('Import workbook',
      'Which workbook? (blank = 1, the newest)\n\n' + shown.map((f, i) => (i + 1) + '.  ' + f.getName() + '   ' + when(f)).join('\n'),
      ui.ButtonSet.OK_CANCEL);
    if (res.getSelectedButton() !== ui.Button.OK) return;
    const n = parseInt(res.getResponseText(), 10);
    if (res.getResponseText().trim() && !(n >= 1 && n <= shown.length)) { ui.alert('Import workbook', 'Pick a number from 1 to ' + shown.length + '.', ui.ButtonSet.OK); return; }
    pick = n ? n - 1 : 0;
  }
  const file = files[pick];
  if (ui.alert('Import workbook', 'Import ' + file.getName() + ' (' + when(file) + ')?\n\n' +
      MANAGED_TABS.join(', ') + ' are backed up (hidden tabs), then replaced in place. Proof_Template: new keys added; you are asked before any of your values change. ' +
      'Saved_Proofs, the color tabs and every other tab are not touched.\n\nAfterwards the .xlsx is moved to the Drive trash.', ui.ButtonSet.YES_NO) !== ui.Button.YES) return;

  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) { ui.alert('Import workbook', 'Someone is saving a proof or running an update. Try again in a minute.', ui.ButtonSet.OK); return; }
  let tmpId = null;
  try {
    tmpId = convertToSheet_(file);
    const wb = readWorkbookTabs_(tmpId);
    const found = MANAGED_TABS.filter(n => wb.tabs[n]);
    if (!found.length) throw new Error(file.getName() + ' has none of the app tabs (' + MANAGED_TABS.join(', ') + ')');
    const lines = applyData_(wb.tabs, wb.template, true);
    if (wb.version) PropertiesService.getScriptProperties().setProperty('DATA_VERSION', wb.version);
    DriveApp.getFileById(tmpId).setTrashed(true);
    file.setTrashed(true);
    lines.push('', 'Moved ' + file.getName() + ' and its temporary converted copy to the Drive trash.');
    const others = files.filter(f => f !== file);
    if (others.length && ui.alert('Import workbook', others.length + ' other ' + WORKBOOK_NAME + ' .xlsx file' + (others.length > 1 ? 's are' : ' is') +
        ' still in your Drive:\n\n' + others.slice(0, 12).map(f => f.getName() + '   ' + when(f)).join('\n') + (others.length > 12 ? '\n...' : '') +
        '\n\nMove ' + (others.length > 1 ? 'them' : 'it') + ' to the trash too?', ui.ButtonSet.YES_NO) === ui.Button.YES) {
      others.forEach(f => f.setTrashed(true));
      lines.push('Also moved ' + others.length + ' older .xlsx file' + (others.length > 1 ? 's' : '') + ' to the trash.');
    }
    if (wb.version && updNewer_(wb.version, installedCodeVersion_()))
      lines.push('', 'This workbook is v' + wb.version + ' but the Apps Script code is ' + label_(installedCodeVersion_()) + ': run Update from GitHub (or paste the v' + wb.version + ' code) too.');
    showSummary_('Workbook imported', lines);
  } catch (e) {
    ui.alert('Import workbook', 'The import stopped: ' + e.message + '\n\nNothing was moved to the trash' +
      (tmpId ? ' (the temporary copy "TEMP import - ' + file.getName() + '" is still in your Drive)' : '') +
      '. Backups of any tab already changed are the hidden "(backup ...)" tabs.', ui.ButtonSet.OK);
  } finally { lock.releaseLock(); }
}
