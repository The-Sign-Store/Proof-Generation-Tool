/**
 * SIGN PROOF GENERATOR - GitHub -> Google Drive / Docs sync
 *
 * Runs under your Google account (no Google API keys needed). Right after every push to GitHub
 * (the release workflow calls this script's web app URL), and once an hour as a backup, it:
 *   1. copies each new GitHub Release zip into the Drive folder "Sign Generation Tool":
 *        Sign_Proof_Generator_v1.8.zip, Sign_Proof_Generator_v1.9.zip ...
 *   2. rewrites the Google Doc "Sign Proof Generator - README & Changelog" from README.md
 *      (headings, bullets, bold), only when README.md changed on GitHub.
 *
 * Setup (once) - full steps in .github/drive-sync/SETUP.md:
 *   - script.google.com > New project > paste this file over Code.gs
 *   - Project Settings > tick 'Show "appsscript.json"' > paste appsscript.json
 *   - select setup in the function list > Run > approve the permissions
 *   - Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone)
 *   - add the web app URL and the key from the setup log as GitHub secrets
 *     DRIVE_SYNC_URL and DRIVE_SYNC_KEY
 * The repository is public, so no GitHub token is needed. (If it is ever made private:
 * Project Settings > Script Properties > GITHUB_TOKEN = a read-only fine-grained token.)
 */
const CFG = {
  OWNER: 'The-Sign-Store',
  REPO: 'Proof-Generation-Tool',
  BRANCH: 'main',
  FOLDER_ID: '155X-81-DK17PNrbT1kJOPrzK2tRC-d90',       // Drive folder "Sign Generation Tool"
  DOCS: [
    { path: 'README.md', name: 'Sign Proof Generator - README & Changelog' },
  ],
  NOTIFY_EMAIL: true,          // email yourself when a new release has been backed up
};

// ---------------------------------------------------------------- entry points
function setup() {
  gh_(`/repos/${CFG.OWNER}/${CFG.REPO}`);                       // fails early with a clear message if the repo / token is wrong
  ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'syncAll').forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('syncAll').timeBased().everyHours(1).create();
  syncAll();
  Logger.log('Setup done. Folder: %s', folder_().getUrl());
  showSyncKey();
}

/** The secret GitHub sends with each call. Made once; run this again any time to see it. */
function showSyncKey() {
  const props = PropertiesService.getScriptProperties();
  let key = props.getProperty('SYNC_KEY');
  if (!key) { key = Utilities.getUuid().replace(/-/g, ''); props.setProperty('SYNC_KEY', key); }
  Logger.log('GitHub secret DRIVE_SYNC_KEY = %s', key);
  Logger.log('GitHub secret DRIVE_SYNC_URL = the Web app URL from Deploy > Manage deployments (ends in /exec)');
  return key;
}

/** Copies new releases and refreshes the README doc. Returns the release tags it added. */
function syncAll(wait) {
  const lock = LockService.getScriptLock();
  if (wait ? !lock.tryLock(wait) : !lock.tryLock(1000)) return null;       // another sync is already running
  try {
    const added = syncReleases();
    syncDocs();
    return added;
  } finally { lock.releaseLock(); }
}

// ---------------------------------------------------------------- web app: GitHub calls this after every push
function doPost(e) {
  const key = PropertiesService.getScriptProperties().getProperty('SYNC_KEY');
  const sent = (e && e.parameter && e.parameter.key) || '';
  if (!key || sent !== key) return json_({ ok: false, error: 'Wrong or missing key. Run showSyncKey and update the DRIVE_SYNC_KEY secret on GitHub.' });
  const added = syncAll(240000);                                        // wait up to 4 min if the hourly sync is mid-run
  if (added === null) return json_({ ok: false, error: 'Another sync is still running; the hourly sync will pick this up.' });
  return json_({ ok: true, added: added, folder: folder_().getUrl() });
}

function doGet() {
  return json_({ ok: true, message: 'Sign Proof Generator Drive sync is running. GitHub posts here after each push.' });
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

/** Re-copy everything (e.g. after deleting the Drive folder). */
function resetAndResync() {
  PropertiesService.getScriptProperties().deleteProperty('SYNCED_RELEASES');
  CFG.DOCS.forEach(d => PropertiesService.getScriptProperties().deleteProperty('SHA_' + d.path));
  syncAll();
}

// ---------------------------------------------------------------- releases -> Drive
function syncReleases() {
  const props = PropertiesService.getScriptProperties();
  const done = JSON.parse(props.getProperty('SYNCED_RELEASES') || '[]');
  const releases = gh_(`/repos/${CFG.OWNER}/${CFG.REPO}/releases?per_page=50`).filter(r => !r.draft);
  const root = folder_(), added = [];
  releases.reverse().forEach(r => {                              // oldest first
    if (done.indexOf(r.tag_name) !== -1) return;
    r.assets.filter(a => /\.zip$/i.test(a.name)).forEach(a => {
      if (root.getFilesByName(a.name).hasNext()) return;          // already in the folder (uploaded by hand or synced before)
      root.createFile(asset_(a).setName(a.name));
    });
    done.push(r.tag_name); added.push(r);
    props.setProperty('SYNCED_RELEASES', JSON.stringify(done));  // saved per release, so a timeout never repeats work
  });
  if (added.length && CFG.NOTIFY_EMAIL) {
    MailApp.sendEmail(Session.getEffectiveUser().getEmail(),
      `Sign Proof Generator: ${added.map(r => r.tag_name).join(', ')} backed up to Drive`,
      added.map(r => `${r.name || r.tag_name}\n${r.html_url}\n\n${r.body || ''}`).join('\n\n------\n\n') + `\n\nDrive folder: ${root.getUrl()}`);
  }
  return added.map(r => r.tag_name);
}

function asset_(a) {
  // GitHub answers with a redirect to signed storage; follow it WITHOUT the GitHub token
  const res = UrlFetchApp.fetch(a.url, { headers: headers_({ Accept: 'application/octet-stream' }), followRedirects: false, muteHttpExceptions: true });
  const code = res.getResponseCode();
  if (code === 200) return res.getBlob();
  const loc = res.getHeaders().Location || res.getHeaders().location;
  if (code >= 300 && code < 400 && loc) return UrlFetchApp.fetch(loc).getBlob();
  throw new Error(`Download of ${a.name} failed (${code}): ${res.getContentText().slice(0, 200)}`);
}

// ---------------------------------------------------------------- markdown files -> Google Docs
function syncDocs() {
  const props = PropertiesService.getScriptProperties();
  CFG.DOCS.forEach(d => {
    const f = gh_(`/repos/${CFG.OWNER}/${CFG.REPO}/contents/${encodeURI(d.path)}?ref=${CFG.BRANCH}`);
    if (props.getProperty('SHA_' + d.path) === f.sha && doc_(d.name, false)) return;   // unchanged
    const md = Utilities.newBlob(Utilities.base64Decode(f.content.replace(/\s/g, ''))).getDataAsString('UTF-8');
    const doc = doc_(d.name, true);
    writeMarkdown_(doc.getBody(), md, `Synced automatically from GitHub (${CFG.OWNER}/${CFG.REPO}, ${d.path}) on ${new Date().toLocaleString()}. Edit the file on GitHub, not this doc - changes here are overwritten.`);
    doc.saveAndClose();
    props.setProperty('SHA_' + d.path, f.sha);
  });
}

/** Small Markdown renderer: # headings, - bullets (nested), ``` code, | tables (as text), ---, **bold**, `code`, [links](url). */
function writeMarkdown_(body, md, banner) {
  body.clear();
  const first = body.getParagraphs()[0];
  first.setText(banner).setItalic(true).setFontSize(8).setForegroundColor('#888888');
  let inCode = false;
  md.replace(/\r/g, '').split('\n').forEach(line => {
    if (/^```/.test(line)) { inCode = !inCode; return; }
    if (inCode) { body.appendParagraph(line || ' ').setFontFamily('Courier New').setFontSize(9).setItalic(false).setForegroundColor('#000000'); return; }
    if (/^\s*$/.test(line)) return;
    if (/^-{3,}\s*$/.test(line)) { body.appendHorizontalRule(); return; }
    if (/^\|[\s:|-]+\|\s*$/.test(line)) return;                  // table separator row
    let h = line.match(/^(#{1,6})\s+(.*)$/), b = line.match(/^(\s*)[-*]\s+(.*)$/), el;
    if (h) {
      el = body.appendParagraph('');
      el.setHeading([null, DocumentApp.ParagraphHeading.TITLE, DocumentApp.ParagraphHeading.HEADING1, DocumentApp.ParagraphHeading.HEADING2,
                     DocumentApp.ParagraphHeading.HEADING3, DocumentApp.ParagraphHeading.HEADING4, DocumentApp.ParagraphHeading.HEADING5][h[1].length]);
      inline_(el, h[2]);
    } else if (b) {
      el = body.appendListItem('');
      el.setNestingLevel(Math.min(4, Math.floor(b[1].replace(/\t/g, '  ').length / 2))).setGlyphType(DocumentApp.GlyphType.BULLET);
      inline_(el, b[2]);
    } else if (/^\|/.test(line)) {
      el = body.appendParagraph(''); inline_(el, line.replace(/^\||\|\s*$/g, '').split('|').map(c => c.trim()).join('   •   '));
    } else {
      el = body.appendParagraph(''); inline_(el, line.replace(/^>\s?/, ''));
    }
  });
}

/** Writes text with **bold**, `code` and [text](url) applied as formatting. */
function inline_(el, src) {
  const parts = parseInline_(src);
  const t = el.editAsText();
  t.setText(parts.map(p => p.text).join('') || ' ');
  t.setItalic(false).setFontFamily('Arial').setForegroundColor('#000000');
  let pos = 0;
  parts.forEach(p => {
    const end = pos + p.text.length - 1;
    if (p.text.length) {
      if (p.bold) t.setBold(pos, end, true);
      if (p.code) t.setFontFamily(pos, end, 'Courier New').setBackgroundColor(pos, end, '#F1F3F4');
      if (p.url) t.setLinkUrl(pos, end, p.url);
    }
    pos = end + 1;
  });
}

/** Pure function (tested outside Apps Script): splits inline Markdown into styled runs. */
function parseInline_(s) {
  const out = [], re = /\*\*(.+?)\*\*|`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)/g;
  let last = 0, m;
  while ((m = re.exec(s))) {
    if (m.index > last) out.push({ text: s.slice(last, m.index) });
    if (m[1] !== undefined) parseInline_(m[1]).forEach(p => out.push(Object.assign(p, { bold: true })));
    else if (m[2] !== undefined) out.push({ text: m[2], code: true });
    else out.push({ text: m[3], url: m[4] });
    last = re.lastIndex;
  }
  if (last < s.length) out.push({ text: s.slice(last) });
  return out;
}

// ---------------------------------------------------------------- helpers
function headers_(extra) {
  const tok = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  const h = Object.assign({ 'X-GitHub-Api-Version': '2022-11-28', Accept: 'application/vnd.github+json' }, extra || {});
  if (tok && tok !== 'none') h.Authorization = 'Bearer ' + tok;
  return h;
}

function gh_(path) {
  const res = UrlFetchApp.fetch('https://api.github.com' + path, { headers: headers_(), muteHttpExceptions: true });
  const code = res.getResponseCode();
  if (code === 404) throw new Error(`GitHub says "not found" for ${path}. Check CFG.OWNER / CFG.REPO, and for a private repo add a GITHUB_TOKEN script property.`);
  if (code === 401) throw new Error('GitHub rejected GITHUB_TOKEN (expired or wrong). Make a new one and update the script property.');
  if (code >= 300) throw new Error(`GitHub ${code} for ${path}: ${res.getContentText().slice(0, 300)}`);
  return JSON.parse(res.getContentText());
}

function folder_() {
  try { return DriveApp.getFolderById(CFG.FOLDER_ID); }
  catch (e) { throw new Error('Cannot open the Drive folder "Sign Generation Tool" (' + CFG.FOLDER_ID + '). Run this script with an account that can edit that folder.'); }
}


function doc_(name, create) {
  const props = PropertiesService.getScriptProperties(), key = 'DOC_' + name, id = props.getProperty(key);
  if (id) { try { if (!DriveApp.getFileById(id).isTrashed()) return DocumentApp.openById(id); } catch (e) { /* deleted */ } }
  if (!create) return null;
  const doc = DocumentApp.create(name);
  DriveApp.getFileById(doc.getId()).moveTo(folder_());
  props.setProperty(key, doc.getId());
  return doc;
}
