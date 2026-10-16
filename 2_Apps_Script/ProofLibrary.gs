/**
 * SIGN PROOF GENERATOR - Proof Library
 *
 * Saves a whole proof package (every product, section, field value, custom table, letter line, color,
 * note, customer field, image and measurement) so it can be reopened and edited later.
 *
 *   Drive:  "Proof Library" folder (next to this Google Sheet)
 *             <Ticket - Customer - Project> [Proof ID]/
 *               rev01.json, rev02.json ...      one file per save; every revision is kept
 *               images/<hash>.jpg               artwork, stored once and shared by all revisions
 *               draft.json                      autosave: ONE file per proof, overwritten in place (not a revision)
 *             _Drafts/                          autosaves of packages that were never saved (one file each, overwritten)
 *   Sheet:  "Saved_Proofs" tab, one row per revision (the list the app shows), with an approval Status
 *   Script Properties: DRAFT_<id> = where each autosave draft is and when it was saved
 *
 * The web app runs as the owner (Deploy > Execute as: Me), so every designer can save and open proofs
 * without needing their own access to the folder.
 *
 * The JSON is plain data (no Apps Script types), ready to import into a database later.
 */
const PROOF_TAB = 'Saved_Proofs';
const PROOF_HEAD = ['Proof_ID', 'Rev', 'Ticket', 'Customer', 'Sub_Customer', 'Project', 'Designer', 'Products', 'Note',
                    'Saved_At', 'Saved_By', 'File_ID', 'Folder_ID', 'App_Version', 'Status', 'Status_By', 'Status_At', 'Search'];
const PROOF_STATUSES = ['Draft', 'Sent to Customer', 'Changes Requested', 'Approved', 'Cancelled'];

function proofLibraryFolder_() {
  const props = PropertiesService.getScriptProperties();
  const id = props.getProperty('PROOF_LIBRARY_ID');
  if (id) {
    try { const f = DriveApp.getFolderById(id); if (!f.isTrashed()) return f; } catch (e) { /* deleted: make a new one */ }
  }
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const parents = DriveApp.getFileById(ss.getId()).getParents();
  const parent = parents.hasNext() ? parents.next() : DriveApp.getRootFolder();
  const found = parent.getFoldersByName('Proof Library');
  const folder = found.hasNext() ? found.next() : parent.createFolder('Proof Library');
  props.setProperty('PROOF_LIBRARY_ID', folder.getId());
  return folder;
}

function proofTab_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(PROOF_TAB);
  if (!sh) {
    sh = ss.insertSheet(PROOF_TAB);
    sh.appendRow(PROOF_HEAD);
    sh.setFrozenRows(1);
    return sh;
  }
  // tabs made by an older version: add any missing columns at the end (existing rows keep their values)
  const head = sh.getDataRange().getValues()[0].map(String);
  PROOF_HEAD.filter(h => head.indexOf(h) === -1).forEach(h => { head.push(h); sh.getRange(1, head.length).setValue(h); });
  return sh;
}

function now_() {
  const tz = Session.getScriptTimeZone(), d = new Date();
  return { date: d, minute: Utilities.formatDate(d, tz, 'yyyy-MM-dd HH:mm'), second: Utilities.formatDate(d, tz, 'yyyy-MM-dd HH:mm:ss') };
}
function user_() { try { return Session.getActiveUser().getEmail() || ''; } catch (e) { return ''; } }

function proofRows_() {
  const values = proofTab_().getDataRange().getValues();
  const head = values.shift().map(String);
  const tz = Session.getScriptTimeZone();
  return values.map((r, i) => [r, i + 2]).filter(x => x[0][0]).map(([r, row]) => {
    const o = { _row: row };
    head.forEach((h, i) => {
      const v = r[i];
      o[h] = v instanceof Date ? Utilities.formatDate(v, tz, 'yyyy-MM-dd HH:mm') : (v === null || v === undefined ? '' : String(v));
    });
    o.Rev = Number(o.Rev) || 0;
    o.Status = o.Status || 'Draft';
    return o;
  });
}

function proofFolderName_(meta, id) {
  const clean = s => String(s || '').replace(/[\\/:*?"<>|]+/g, ' ').replace(/\s+/g, ' ').trim();
  const name = [meta.ticket, meta.customer, meta.sub, meta.project].map(clean).filter(String).join(' - ') || 'Untitled proof';
  return (name.length > 90 ? name.slice(0, 90).trim() : name) + ' [' + id + ']';
}

/**
 * req = { proofId: string|null (null = new proof), meta: {ticket, customer, sub, project, designer, products, note, appVersion},
 *         state: JSON string, images: [{hash, data (base64), mime}] }
 */
function saveProof(req) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const meta = req.meta || {};
    const rows = proofRows_();
    const tz = Session.getScriptTimeZone();
    const now = new Date();
    let proofId = req.proofId || '', rev = 1, folder = null;
    const mine = proofId ? rows.filter(r => r.Proof_ID === proofId) : [];
    if (mine.length) {
      rev = Math.max.apply(null, mine.map(r => r.Rev)) + 1;
      try { folder = DriveApp.getFolderById(mine[mine.length - 1].Folder_ID); } catch (e) { folder = null; }
    } else {
      proofId = 'P' + Utilities.formatDate(now, tz, 'yyMMdd-HHmmss') + '-' + Math.floor(Math.random() * 9000 + 1000);
    }
    if (!folder) folder = proofLibraryFolder_().createFolder(proofFolderName_(meta, proofId));

    const imgs = req.images || [];
    if (imgs.length) {
      const it = folder.getFoldersByName('images');
      const imgFolder = it.hasNext() ? it.next() : folder.createFolder('images');
      imgs.forEach(im => {
        const name = String(im.hash).replace(/[^a-z0-9]/gi, '') + '.jpg';
        if (imgFolder.getFilesByName(name).hasNext()) return;              // already stored by an earlier revision
        imgFolder.createFile(Utilities.newBlob(Utilities.base64Decode(im.data), im.mime || 'image/jpeg', name));
      });
    }
    const file = folder.createFile('rev' + (rev < 10 ? '0' : '') + rev + '.json', req.state, 'application/json');
    const savedAt = Utilities.formatDate(now, tz, 'yyyy-MM-dd HH:mm');
    const user = user_(), status = PROOF_STATUSES.indexOf(meta.status) !== -1 ? meta.status : 'Draft';
    appendProofRow_({ Proof_ID: proofId, Rev: rev, Ticket: meta.ticket, Customer: meta.customer, Sub_Customer: meta.sub, Project: meta.project,
                      Designer: meta.designer, Products: meta.products, Note: meta.note, Saved_At: savedAt, Saved_By: user,
                      File_ID: file.getId(), Folder_ID: folder.getId(), App_Version: meta.appVersion, Status: status, Status_By: user, Status_At: savedAt,
                      Search: meta.search || '' });
    // the revision now holds the latest work: its autosave draft (and the never-saved draft it came from) are no longer needed
    dropDraft_('DRAFT_' + proofId);
    if (req.draftId) dropDraft_('DRAFT_' + req.draftId);
    return { proofId: proofId, rev: rev, savedAt: savedAt, status: status, folderUrl: folder.getUrl() };
  } finally {
    lock.releaseLock();
  }
}

function appendProofRow_(o) {
  const sh = proofTab_(), head = sh.getDataRange().getValues()[0].map(String);
  sh.appendRow(head.map(h => (o[h] === undefined || o[h] === null ? '' : (h === 'Rev' ? o[h] : String(o[h])))));
}

/** Approval status of one revision (Draft, Sent to Customer, Changes Requested, Approved, Cancelled). */
function setProofStatus(proofId, rev, status) {
  if (PROOF_STATUSES.indexOf(status) === -1) throw new Error('Unknown status: ' + status);
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const sh = proofTab_(), head = sh.getDataRange().getValues()[0].map(String);
    const row = proofRows_().filter(r => r.Proof_ID === proofId && r.Rev === Number(rev))[0];
    if (!row) throw new Error('Version v' + rev + ' of ' + proofId + ' was not found.');
    const t = now_(), user = user_();
    [['Status', status], ['Status_By', user], ['Status_At', t.minute]].forEach(([h, v]) => sh.getRange(row._row, head.indexOf(h) + 1).setValue(v));
    return { proofId: proofId, rev: Number(rev), status: status, statusBy: user, statusAt: t.minute };
  } finally { lock.releaseLock(); }
}

/** Every saved proof, newest first, with its revisions (newest first). */
function listProofs() {
  const byId = {}, rows = proofRows_();
  backfillSearch_(rows);
  rows.forEach(r => {
    const p = byId[r.Proof_ID] = byId[r.Proof_ID] || { proofId: r.Proof_ID, revs: [] };
    p.revs.push({ rev: r.Rev, savedAt: r.Saved_At, savedBy: r.Saved_By, note: r.Note, designer: r.Designer,
                  status: r.Status, statusBy: r.Status_By, statusAt: r.Status_At });
    if (!p.latest || r.Rev >= p.latest) {
      p.latest = r.Rev; p.savedAt = r.Saved_At; p.ticket = r.Ticket; p.customer = r.Customer; p.sub = r.Sub_Customer;
      p.project = r.Project; p.designer = r.Designer; p.products = r.Products; p.status = r.Status; p.search = r.Search;
    }
  });
  const list = Object.keys(byId).map(k => byId[k]);
  list.forEach(p => p.revs.sort((a, b) => b.rev - a.rev));
  list.sort((a, b) => (a.savedAt < b.savedAt ? 1 : a.savedAt > b.savedAt ? -1 : 0));
  const drafts = drafts_();
  list.forEach(p => { const d = drafts['DRAFT_' + p.proofId]; if (d) p.draft = { key: 'DRAFT_' + p.proofId, savedAt: d.savedAt, savedBy: d.savedBy }; });
  return list;
}

/** One revision (latest when rev is empty): its saved state plus the images it uses, as data URLs. */
function loadProof(proofId, rev) {
  const mine = proofRows_().filter(r => r.Proof_ID === proofId);
  if (!mine.length) throw new Error('Saved proof ' + proofId + ' was not found in the Saved_Proofs tab.');
  const want = Number(rev) || Math.max.apply(null, mine.map(r => r.Rev));
  const row = mine.filter(r => r.Rev === want)[0];
  if (!row) throw new Error('Version v' + want + ' of ' + proofId + ' was not found.');
  const state = DriveApp.getFileById(row.File_ID).getBlob().getDataAsString('UTF-8');
  const images = {};
  const hashes = [];
  try {
    const st = JSON.parse(state);
    Object.keys(st.art || {}).forEach(k => (st.art[k] || []).forEach(a => { if (a.img && hashes.indexOf(a.img) === -1) hashes.push(a.img); }));
  } catch (e) { throw new Error('Version v' + want + ' of ' + proofId + ' could not be read: ' + e.message); }
  if (hashes.length) {
    const folder = DriveApp.getFolderById(row.Folder_ID);
    const it = folder.getFoldersByName('images');
    const imgFolder = it.hasNext() ? it.next() : null;
    hashes.forEach(h => {
      const files = imgFolder ? imgFolder.getFilesByName(h + '.jpg') : null;
      if (files && files.hasNext()) {
        const blob = files.next().getBlob();
        images[h] = 'data:' + (blob.getContentType() || 'image/jpeg') + ';base64,' + Utilities.base64Encode(blob.getBytes());
      }
    });
  }
  return { proofId: proofId, rev: want, savedAt: row.Saved_At, state: state, images: images };
}

// =====================================================================  AUTOSAVE DRAFTS
// One draft per proof (draft.json in its folder) or per never-saved package (_Drafts/<id>.json), always
// overwritten in place. Script Properties DRAFT_<id> = { fileId, folderId, savedAt, savedBy, label, products, proofId, draftId }.

function drafts_() {
  const all = PropertiesService.getScriptProperties().getProperties(), out = {};
  Object.keys(all).filter(k => k.indexOf('DRAFT_') === 0).forEach(k => { try { out[k] = JSON.parse(all[k]); } catch (e) { /* skip */ } });
  return out;
}

function dropDraft_(key) {
  const props = PropertiesService.getScriptProperties(), raw = props.getProperty(key);
  if (!raw) return;
  try { DriveApp.getFileById(JSON.parse(raw).fileId).setTrashed(true); } catch (e) { /* already gone */ }
  props.deleteProperty(key);
}

function draftsFolder_() {
  const lib = proofLibraryFolder_(), it = lib.getFoldersByName('_Drafts');
  return it.hasNext() ? it.next() : lib.createFolder('_Drafts');
}

function imagesFolder_(folder) {
  const it = folder.getFoldersByName('images');
  return it.hasNext() ? it.next() : folder.createFolder('images');
}

/**
 * req = { proofId (saved proof) | draftId (never-saved package, null the first time), meta: {label, products, ...},
 *         state: JSON string, images: [{hash, data, mime}] (only ones not sent before) }
 * Overwrites the single draft file for this proof / package; never adds a revision.
 */
function saveDraft(req) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const props = PropertiesService.getScriptProperties(), t = now_(), meta = req.meta || {};
    let key, folder, name, draftId = req.draftId || '';
    if (req.proofId) {
      const row = proofRows_().filter(r => r.Proof_ID === req.proofId).pop();
      if (!row) throw new Error('Saved proof ' + req.proofId + ' was not found.');
      key = 'DRAFT_' + req.proofId; folder = DriveApp.getFolderById(row.Folder_ID); name = 'draft.json';
    } else {
      if (!draftId) draftId = 'D' + Utilities.formatDate(t.date, Session.getScriptTimeZone(), 'yyMMdd-HHmmss') + '-' + Math.floor(Math.random() * 9000 + 1000);
      key = 'DRAFT_' + draftId; folder = draftsFolder_(); name = draftId + '.json';
    }
    (req.images || []).forEach(im => {
      const f = imagesFolder_(folder), n = String(im.hash).replace(/[^a-z0-9]/gi, '') + '.jpg';
      if (!f.getFilesByName(n).hasNext()) f.createFile(Utilities.newBlob(Utilities.base64Decode(im.data), im.mime || 'image/jpeg', n));
    });
    let info = null, file = null;
    try { info = JSON.parse(props.getProperty(key) || 'null'); } catch (e) { info = null; }
    if (info && info.fileId) { try { file = DriveApp.getFileById(info.fileId); if (file.isTrashed()) file = null; } catch (e) { file = null; } }
    if (file) file.setContent(req.state);                                   // same file, new content
    else file = folder.createFile(name, req.state, 'application/json');
    info = { fileId: file.getId(), folderId: folder.getId(), savedAt: t.second, savedBy: user_(), label: String(meta.label || ''),
             products: String(meta.products || ''), proofId: req.proofId || '', draftId: draftId };
    ['ticket', 'customer', 'sub', 'project', 'designer', 'search'].forEach(k => { info[k] = String(meta[k] || ''); });   // v4.3: searchable
    props.setProperty(key, JSON.stringify(info));
    return { key: key, draftId: draftId, savedAt: t.second };
  } finally { lock.releaseLock(); }
}

/** Autosaves of packages that were never saved, newest first. */
function listDrafts() {
  backfillDraftSearch_();
  const d = drafts_();
  return Object.keys(d).filter(k => !d[k].proofId).map(k => Object.assign({ key: k }, d[k]))
    .sort((a, b) => (a.savedAt < b.savedAt ? 1 : a.savedAt > b.savedAt ? -1 : 0));
}

/** Every draft (saved proofs' and never-saved packages'), newest first: lets the app offer one back after a closed tab. */
function listAllDrafts() {
  const d = drafts_();
  return Object.keys(d).map(k => Object.assign({ key: k }, d[k])).sort((a, b) => (a.savedAt < b.savedAt ? 1 : a.savedAt > b.savedAt ? -1 : 0));
}

/** One draft's state plus its images (looked up in its own folder, then its proof's folder). */
function loadDraft(key) {
  const d = drafts_()[key];
  if (!d) throw new Error('This draft no longer exists.');
  const state = DriveApp.getFileById(d.fileId).getBlob().getDataAsString('UTF-8'), images = {};
  const st = JSON.parse(state), hashes = [];
  Object.keys(st.art || {}).forEach(k => (st.art[k] || []).forEach(a => { if (a.img && hashes.indexOf(a.img) === -1) hashes.push(a.img); }));
  if (hashes.length) {
    const it = DriveApp.getFolderById(d.folderId).getFoldersByName('images'), f = it.hasNext() ? it.next() : null;
    hashes.forEach(h => {
      const files = f ? f.getFilesByName(h + '.jpg') : null;
      if (files && files.hasNext()) { const b = files.next().getBlob(); images[h] = 'data:' + (b.getContentType() || 'image/jpeg') + ';base64,' + Utilities.base64Encode(b.getBytes()); }
    });
  }
  let latest = null;
  if (d.proofId) {
    const mine = proofRows_().filter(r => r.Proof_ID === d.proofId).sort((a, b) => b.Rev - a.Rev)[0];
    if (mine) latest = { rev: mine.Rev, savedAt: mine.Saved_At, status: mine.Status };
  }
  return { key: key, proofId: d.proofId, draftId: d.draftId, savedAt: d.savedAt, latest: latest, state: state, images: images };
}

function discardDraft(key) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try { dropDraft_(key); return true; } finally { lock.releaseLock(); }
}


// =====================================================================  SEARCH (v4.3)
// Saved projects and drafts are searchable by ticket, customer, project, designer, product and component names.
// Projects saved before v4.3 get their "Search" text filled in from their saved file the first time the list is opened.

/** Product + component (section) names of a saved state, plus its job info. */
function searchFromState_(json) {
  const st = JSON.parse(json), names = [], add = n => { n = String(n || '').trim(); if (n && !/^MISSING/i.test(n) && names.indexOf(n) === -1) names.push(n); };
  const reg = componentNames_(), custom = st.customComps || {};
  (st.items || []).forEach(it => add(it.name));
  (st.parts || []).forEach(p => {
    if (p.enabled === false) return;
    const it = (st.items || []).filter(i => i.iid === p.iid)[0], d = it && it.defs ? it.defs[p.di] || {} : {};
    add(p.custom || d.title || (custom[d.component] || {}).name || reg[d.component] || '');
  });
  const c = st.customer || {}, v = k => String((c[k] || {}).v || '').trim();
  return { search: names.join(', '), ticket: v('cf-ticket'), customer: v('cf-name'), sub: v('cf-sub'), project: v('cf-project'), designer: v('cf-designer') };
}
let COMPONENT_NAMES_ = null;
function componentNames_() {
  if (COMPONENT_NAMES_) return COMPONENT_NAMES_;
  COMPONENT_NAMES_ = {};
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Component_Registry');
  if (sh) {
    const v = sh.getDataRange().getValues(), h = v.shift().map(String), id = h.indexOf('Component_ID'), nm = h.indexOf('Display_Name');
    v.forEach(r => { if (r[id]) COMPONENT_NAMES_[String(r[id])] = String(r[nm] || r[id]); });
  }
  return COMPONENT_NAMES_;
}
/** Fill the Search column of older saved projects (latest version of each), a batch per call. */
function backfillSearch_(rows) {
  const latest = {};
  rows.forEach(r => { if (!latest[r.Proof_ID] || r.Rev > latest[r.Proof_ID].Rev) latest[r.Proof_ID] = r; });
  const todo = Object.keys(latest).map(k => latest[k]).filter(r => !r.Search && r.File_ID).slice(0, 60);
  if (!todo.length) return;
  const sh = proofTab_(), head = sh.getDataRange().getValues()[0].map(String), col = head.indexOf('Search') + 1;
  if (!col) return;
  todo.forEach(r => {
    let text = '-';                                                        // "-" = looked at, nothing to add (not retried)
    try { text = searchFromState_(DriveApp.getFileById(r.File_ID).getBlob().getDataAsString('UTF-8')).search || '-'; } catch (e) { /* file gone */ }
    sh.getRange(r._row, col).setValue(text);
    r.Search = text;
  });
}
/** Drafts saved before v4.3: add job info + names from their file once. */
function backfillDraftSearch_() {
  const props = PropertiesService.getScriptProperties(), d = drafts_();
  Object.keys(d).filter(k => d[k].search === undefined).slice(0, 40).forEach(k => {
    const info = d[k];
    try { Object.assign(info, searchFromState_(DriveApp.getFileById(info.fileId).getBlob().getDataAsString('UTF-8'))); }
    catch (e) { info.search = ''; }
    props.setProperty(k, JSON.stringify(info));
  });
}

// =====================================================================
//  FRESHDESK (v4.8): read the job's ticket and add the hand-off note, from the server.
//  The API key lives ONLY in Script Properties (Apps Script > Project Settings > Script properties:
//  FRESHDESK_API_KEY). It is never sent to the browser. Notes are posted as the key's owner.
// =====================================================================
const FD_HOST = 'signstoremacon.freshdesk.com';
const FD_STATUS = { 2: 'Open', 3: 'Pending', 4: 'Resolved', 5: 'Closed', 6: 'Waiting on Customer', 7: 'Waiting on Third Party' };
function fdKey_() { return PropertiesService.getScriptProperties().getProperty('FRESHDESK_API_KEY') || ''; }
function fdTicketUrl_(id) { return 'https:' + '/' + '/' + FD_HOST + '/a/tickets/' + id; }
function fdFetch_(path, opts) {
  const key = fdKey_();
  if (!key) throw new Error('Freshdesk is not connected: add FRESHDESK_API_KEY in Script properties.');
  opts = Object.assign({ method: 'get', muteHttpExceptions: true }, opts || {});
  opts.headers = Object.assign({}, opts.headers || {}, { Authorization: 'Basic ' + Utilities.base64Encode(key + ':X') });
  const r = UrlFetchApp.fetch('https:' + '/' + '/' + FD_HOST + '/api/v2' + path, opts), code = r.getResponseCode(), txt = r.getContentText();
  if (code >= 300) {
    let msg = txt;
    try { const j = JSON.parse(txt); msg = (j.errors || []).map(e => (e.field ? e.field + ': ' : '') + e.message).join('; ') || j.description || j.message || txt; } catch (e) { /* not JSON */ }
    if (code === 401) msg = 'the API key was not accepted (check FRESHDESK_API_KEY)';
    if (code === 404) msg = 'that ticket was not found';
    throw new Error('Freshdesk ' + code + ': ' + String(msg).slice(0, 300));
  }
  return txt ? JSON.parse(txt) : null;
}
// every agent (name + email), cached for 6 hours
function fdAgents_() {
  const cache = CacheService.getScriptCache(), hit = cache.get('FD_AGENTS');
  if (hit) return JSON.parse(hit);
  let all = [];
  for (let page = 1; page <= 5; page++) {
    const a = fdFetch_('/agents?per_page=100&page=' + page) || [];
    all = all.concat(a.map(x => ({ id: x.id, name: (x.contact && x.contact.name) || '', email: (x.contact && x.contact.email) || '' })));
    if (a.length < 100) break;
  }
  cache.put('FD_AGENTS', JSON.stringify(all), 21600);
  return all;
}
// "Will Bagwell" -> the agent with that name (full name first, then first + last, then a unique first name)
function fdMatchAgent_(name, agents) {
  const n = String(name || '').trim().toLowerCase().replace(/\s+/g, ' ');
  if (!n) return null;
  agents = agents || fdAgents_();
  let hit = agents.filter(a => a.name.toLowerCase().replace(/\s+/g, ' ') === n);
  if (!hit.length) { const w = n.split(' '); hit = agents.filter(a => { const an = a.name.toLowerCase(); return w.every(x => an.indexOf(x) !== -1); }); }
  if (!hit.length) { const f = n.split(' ')[0]; const byFirst = agents.filter(a => a.name.toLowerCase().split(/\s+/)[0] === f); if (byFirst.length === 1) hit = byFirst; }
  return hit.length === 1 && hit[0].email ? hit[0] : null;
}
/** The ticket for the Approve and export panel: subject, status, people and the latest activity. */
function fdTicket(ticketId, salesName) {
  const id = String(ticketId || '').replace(/\D/g, '');
  if (!id) throw new Error('No ticket number.');
  if (!fdKey_()) return { noKey: true, id: id, url: fdTicketUrl_(id) };
  const t = fdFetch_('/tickets/' + id + '?include=requester,conversations'), agents = fdAgents_();
  const agentName = uid => { const a = agents.filter(x => x.id === uid)[0]; return a ? a.name : ''; };
  const req = t.requester || {};
  const convs = (t.conversations || []).slice(-5).reverse().map(c => ({
    private: !!c.private, incoming: !!c.incoming, at: c.created_at || '',
    from: agentName(c.user_id) || (c.user_id === t.requester_id ? (req.name || 'Requester') : (c.from_email || '')),
    text: String(c.body_text || '').replace(/\s+/g, ' ').trim().slice(0, 260), files: (c.attachments || []).length
  }));
  const sales = fdMatchAgent_(salesName, agents);
  return { id: id, url: fdTicketUrl_(id), subject: t.subject || '', status: FD_STATUS[t.status] || String(t.status || ''),
           requester: req.name || '', requesterEmail: req.email || '', agent: agentName(t.responder_id), created: t.created_at || '',
           updated: t.updated_at || '', convs: convs, notify: sales ? { name: sales.name, email: sales.email } : null };
}
// multipart/form-data body as bytes (Freshdesk needs multipart for attachments)
function fdMultipart_(fields, files) {
  const b = 'SignStudio' + Date.now(), nl = '\r\n';
  let bytes = [];
  const add = s => { bytes = bytes.concat(Utilities.newBlob(s).getBytes()); };
  fields.forEach(f => add('--' + b + nl + 'Content-Disposition: form-data; name="' + f[0] + '"' + nl + nl + f[1] + nl));
  files.forEach(f => {
    add('--' + b + nl + 'Content-Disposition: form-data; name="attachments[]"; filename="' + String(f.name).replace(/["\r\n]/g, '') + '"' + nl +
        'Content-Type: ' + (f.mime || 'application/octet-stream') + nl + nl);
    bytes = bytes.concat(Utilities.base64Decode(f.data));
    add(nl);
  });
  add('--' + b + '--' + nl);
  return { contentType: 'multipart/form-data; boundary=' + b, payload: bytes };
}
/** Adds the hand-off note to the ticket: req = { ticket, html, notify (salesperson name), files: [{ name, mime, data (base64) }] } */
function fdAddNote(req) {
  const id = String(req.ticket || '').replace(/\D/g, '');
  if (!id) throw new Error('No ticket number.');
  const agent = req.notify ? fdMatchAgent_(req.notify) : null;
  const fields = [['body', String(req.html || '')], ['private', 'true']];
  if (agent) fields.push(['notify_emails[]', agent.email]);
  const mp = fdMultipart_(fields, req.files || []);
  const n = fdFetch_('/tickets/' + id + '/notes', { method: 'post', contentType: mp.contentType, payload: mp.payload });
  return { id: n && n.id, url: fdTicketUrl_(id), notified: agent ? agent.name : '', attachments: ((n && n.attachments) || []).length || (req.files || []).length };
}
