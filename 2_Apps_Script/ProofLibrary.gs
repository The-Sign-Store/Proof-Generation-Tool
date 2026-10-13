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
 *   Sheet:  "Saved_Proofs" tab, one row per revision (the list the app shows)
 *
 * The web app runs as the owner (Deploy > Execute as: Me), so every designer can save and open proofs
 * without needing their own access to the folder.
 *
 * The JSON is plain data (no Apps Script types), ready to import into a database later.
 */
const PROOF_TAB = 'Saved_Proofs';
const PROOF_HEAD = ['Proof_ID', 'Rev', 'Ticket', 'Customer', 'Sub_Customer', 'Project', 'Designer', 'Products', 'Note',
                    'Saved_At', 'Saved_By', 'File_ID', 'Folder_ID', 'App_Version'];

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
  }
  return sh;
}

function proofRows_() {
  const values = proofTab_().getDataRange().getValues();
  const head = values.shift().map(String);
  const tz = Session.getScriptTimeZone();
  return values.filter(r => r[0]).map(r => {
    const o = {};
    head.forEach((h, i) => {
      const v = r[i];
      o[h] = v instanceof Date ? Utilities.formatDate(v, tz, 'yyyy-MM-dd HH:mm') : (v === null || v === undefined ? '' : String(v));
    });
    o.Rev = Number(o.Rev) || 0;
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
    let user = '';
    try { user = Session.getActiveUser().getEmail() || ''; } catch (e) { user = ''; }
    proofTab_().appendRow([proofId, rev, String(meta.ticket || ''), String(meta.customer || ''), String(meta.sub || ''),
                           String(meta.project || ''), String(meta.designer || ''), String(meta.products || ''), String(meta.note || ''),
                           savedAt, user, file.getId(), folder.getId(), String(meta.appVersion || '')]);
    return { proofId: proofId, rev: rev, savedAt: savedAt, folderUrl: folder.getUrl() };
  } finally {
    lock.releaseLock();
  }
}

/** Every saved proof, newest first, with its revisions (newest first). */
function listProofs() {
  const byId = {};
  proofRows_().forEach(r => {
    const p = byId[r.Proof_ID] = byId[r.Proof_ID] || { proofId: r.Proof_ID, revs: [] };
    p.revs.push({ rev: r.Rev, savedAt: r.Saved_At, savedBy: r.Saved_By, note: r.Note, designer: r.Designer });
    if (!p.latest || r.Rev >= p.latest) {
      p.latest = r.Rev; p.savedAt = r.Saved_At; p.ticket = r.Ticket; p.customer = r.Customer; p.sub = r.Sub_Customer;
      p.project = r.Project; p.designer = r.Designer; p.products = r.Products;
    }
  });
  const list = Object.keys(byId).map(k => byId[k]);
  list.forEach(p => p.revs.sort((a, b) => b.rev - a.rev));
  list.sort((a, b) => (a.savedAt < b.savedAt ? 1 : a.savedAt > b.savedAt ? -1 : 0));
  return list;
}

/** One revision (latest when rev is empty): its saved state plus the images it uses, as data URLs. */
function loadProof(proofId, rev) {
  const mine = proofRows_().filter(r => r.Proof_ID === proofId);
  if (!mine.length) throw new Error('Saved proof ' + proofId + ' was not found in the Saved_Proofs tab.');
  const want = Number(rev) || Math.max.apply(null, mine.map(r => r.Rev));
  const row = mine.filter(r => r.Rev === want)[0];
  if (!row) throw new Error('Revision ' + want + ' of ' + proofId + ' was not found.');
  const state = DriveApp.getFileById(row.File_ID).getBlob().getDataAsString('UTF-8');
  const images = {};
  const hashes = [];
  try {
    const st = JSON.parse(state);
    Object.keys(st.art || {}).forEach(k => (st.art[k] || []).forEach(a => { if (a.img && hashes.indexOf(a.img) === -1) hashes.push(a.img); }));
  } catch (e) { throw new Error('Revision ' + want + ' of ' + proofId + ' could not be read: ' + e.message); }
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
