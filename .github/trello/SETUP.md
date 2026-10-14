# Trello issue sync: one-time setup

Every GitHub issue in this repo gets a card on the Trello board:

| Issue event | Card |
| --- | --- |
| opened | new card at the top of the **Inbox** column, named `#12 Issue title`, with the issue text and a link |
| edited | title and description updated |
| closed | moved to **Done** |
| reopened | moved back to **Inbox** |

## 1. Trello key and token

1. Go to https://trello.com/power-ups/admin and create a Power-Up (any name, e.g. "GitHub sync") in your workspace.
2. Open its **API key** tab and generate a key. Copy the **API key**.
3. Next to the key, click **Token**, allow access, and copy the **token**.

## 2. Board and column IDs

Open the board in the browser, add `.json` to the end of its address (e.g. `https://trello.com/b/AbC123/dev-board.json`) and search the page:

- the board ID: the short code in the board address works (`AbC123`)
- each column's ID: under `"lists"`, the `"id"` next to `"name": "Inbox"` and `"name": "Done"` (use your own column names)

## 3. Add them to GitHub

Repository **Settings > Secrets and variables > Actions**:

- **Secrets** tab: `TRELLO_KEY`, `TRELLO_TOKEN`
- **Variables** tab: `TRELLO_BOARD`, `TRELLO_INBOX_LIST`, `TRELLO_DONE_LIST`

## 4. Try it

- Open a test issue: a card appears in Inbox within about 30 seconds. Close it: the card moves to Done.
- Existing open issues: **Actions > Trello issue sync > Run workflow** adds a card for each one that has none.
- If nothing happens: **Actions > Trello issue sync**, open the run, and read the step's message (a missing secret or variable is named there).

Cards are matched by the `#<number> ` at the start of their name, so keep that prefix if you rename a card.
