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
                    'Saved_At', 'Saved_By', 'File_ID', 'Folder_ID', 'App_Version', 'Status', 'Status_By', 'Status_At'];
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
                      File_ID: file.getId(), Folder_ID: folder.getId(), App_Version: meta.appVersion, Status: status, Status_By: user, Status_At: savedAt });
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
  const byId = {};
  proofRows_().forEach(r => {
    const p = byId[r.Proof_ID] = byId[r.Proof_ID] || { proofId: r.Proof_ID, revs: [] };
    p.revs.push({ rev: r.Rev, savedAt: r.Saved_At, savedBy: r.Saved_By, note: r.Note, designer: r.Designer,
                  status: r.Status, statusBy: r.Status_By, statusAt: r.Status_At });
    if (!p.latest || r.Rev >= p.latest) {
      p.latest = r.Rev; p.savedAt = r.Saved_At; p.ticket = r.Ticket; p.customer = r.Customer; p.sub = r.Sub_Customer;
      p.project = r.Project; p.designer = r.Designer; p.products = r.Products; p.status = r.Status;
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
    props.setProperty(key, JSON.stringify(info));
    return { key: key, draftId: draftId, savedAt: t.second };
  } finally { lock.releaseLock(); }
}

/** Autosaves of packages that were never saved, newest first. */
function listDrafts() {
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
