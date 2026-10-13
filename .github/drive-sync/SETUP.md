# GitHub → Google Drive: release zips land in Drive on every push

Each time a version commit (`vX.Y: …`) reaches `main`, the **Release versions** workflow builds
`Sign_Proof_Generator_vX.Y.zip`, publishes it as a GitHub Release, then calls this Apps Script.
The script copies every release zip that isn't in Drive yet into the **Sign Generation Tool** folder.
It also rewrites the **Sign Proof Generator - README & Changelog** Google Doc when README.md changes,
and emails you a summary. An hourly check runs as a backup.

Pushes without a version (README edits and so on) only refresh the Google Doc; no zip is made.
The saved-proofs Proof Library is separate and is not touched by this.

## One-time setup (about 10 minutes)

### 1. Create the script (in the Google account that owns the Drive folder)
1. Go to <https://script.google.com> › **New project**. Name it `Sign Proof Generator - GitHub to Drive`.
2. Replace everything in `Code.gs` with [`DriveSync.gs`](DriveSync.gs).
3. **Project Settings** (gear) › tick **Show "appsscript.json" manifest file in editor**.
   Back in the editor, open `appsscript.json` and replace it with [`appsscript.json`](appsscript.json).
4. Save. Choose **setup** in the function list › **Run** › **Review permissions** › approve.
   The first run copies every existing release (v1.1 to now) into the folder; that can take a few minutes.
   If it stops with "Exceeded maximum execution time", run **syncAll** once more: it keeps what was copied and continues.
5. Open **Executions** (left menu) › the setup run. Copy the value after `DRIVE_SYNC_KEY =`.

### 2. Publish it as a web app
1. **Deploy › New deployment** › gear › **Web app**.
2. Execute as: **Me**. Who has access: **Anyone**.
3. **Deploy** and copy the **Web app URL** (ends in `/exec`).

   If "Anyone" isn't offered, your Google Workspace admin has turned off public web apps.
   The hourly sync still works; zips just arrive within the hour instead of right away.

### 3. Give GitHub the URL and key
GitHub › the repository › **Settings › Secrets and variables › Actions › New repository secret**:

| Name | Value |
|---|---|
| `DRIVE_SYNC_URL` | the Web app URL from step 2 |
| `DRIVE_SYNC_KEY` | the key from step 1.5 |

### 4. Check it
**Actions › Release versions › Run workflow**. The **Copy new release zips to Google Drive** step
prints `{"ok":true,…}`, and the folder has a zip for every release.

## Later
- **Changed the script?** Deploy › Manage deployments › edit › Version: **New version** (the URL stays the same).
- **Lost the key?** Run `showSyncKey` and read it in Executions.
- **Start over** (e.g. after emptying the folder): run `resetAndResync`.
- The key only lets GitHub start a sync; it can't read or change anything else.
