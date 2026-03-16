# Taminator — Step-by-Step Testing Guide

Use these steps to test the browser UI, report actions, Library, and (optionally) Google Drive integration.

**Install path:** Use `~/taminator` on all machines (Mac: `/Users/<you>/taminator`, Linux: `/home/<you>/taminator`). See [INSTALL_PATH.md](INSTALL_PATH.md).

---

## Prerequisites

- Python 3.7+ with dependencies installed from the repo:
  ```bash
  cd ~/taminator/taminator
  pip install -r requirements.txt   # or use a venv
  ```
- For **real** check/update (not test data): Red Hat VPN and JIRA token configured (`tam-rfe config --add-token jira_token`).

---

## 1. Start the web UI

1. Open a terminal.
2. Go to the taminator app directory (`~/taminator/taminator` — on Mac this is `/Users/<you>/taminator/taminator`, on Linux `/home/<you>/taminator/taminator`):
   ```bash
   cd ~/taminator/taminator
   ```
3. Start the server:
   ```bash
   ./tam-rfe serve
   ```
4. A browser should open at `http://127.0.0.1:8765`. If not, open that URL manually.
5. You should see the Taminator page with **Reports** and **Library** at the top.

---

## 2. Test Reports (with test data)

1. On the **Reports** tab, leave the Customer field empty.
2. Check **Use test data (no JIRA)**.
3. Click **Check report**.
   - Expected: Output appears (test data is created if needed; you may see auth/JIRA messages if test data path still triggers auth).
4. Click **Update report**.
   - Expected: Output shows update result or errors. With test data, a report file may be created under `~/taminator-test-data/`.

**If you have JIRA configured and VPN:**

5. Clear the checkbox and enter a customer name (e.g. `wellsfargo`).
6. Click **Check report** — expect JIRA status comparison.
7. Click **Update report** — expect report file updated from JIRA.

---

## 3. Test the Library

1. Click **Library** in the top navigation.
2. The page should show either:
   - A table of reports (Account, File, Actions) if any `.md` files exist in the search paths, or
   - “No report files found…” if none exist.
3. **To get at least one report in the list:**
   - Create a test report:
     ```bash
     mkdir -p ~/taminator-test-data
     echo "# Test Report\n\n| JIRA | Case | Desc | Status |\n| AAP-1 | 123 | Test | New |" > ~/taminator-test-data/testcustomer.md
     ```
   - Reload the Library tab (click **Library** again or refresh the page).
4. You should see a row for `testcustomer` (or another account).
5. Click **View** on that row.
   - Expected: Report content appears in the viewer below the table.
6. Click **Open in Google Docs** on the same row.
   - If Google is not connected: You should see an error or status message explaining that client ID/secret are required.
   - If Google is connected: A new browser tab opens with the new Google Doc containing the report.

---

## 4. Test Google Drive integration (optional)

**4a. Configure Google (one-time)**

1. Create a Google Cloud project and OAuth 2.0 Desktop client (see [GOOGLE_DRIVE_INTEGRATION.md](GOOGLE_DRIVE_INTEGRATION.md)).
2. Set environment variables (or add `~/.config/taminator/google_credentials.json`):
   ```bash
   export TAMINATOR_GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
   export TAMINATOR_GOOGLE_CLIENT_SECRET="your-client-secret"
   ```
3. In the same terminal, run:
   ```bash
   ./tam-rfe google-connect
   ```
4. A browser opens; sign in to Google and allow access. The CLI should print “Google Drive connected.”

**4b. Test from the UI**

1. With the web UI open, go to the **Library** tab.
2. Under the table, the status line should indicate “Google Drive connected.”
3. Click **View** on a report, then click **Open in Google Docs** (or click **Open in Google Docs** directly on a row).
4. Expected: A new tab opens with a Google Doc containing that report’s content.

---

## 5. Test the CLI (sanity check)

Run these from `~/taminator/taminator`:

```bash
./tam-rfe --help
./tam-rfe check --test-data
./tam-rfe config
```

Expected: Help text, check output (or auth message), and config token status.

---

## 6. Quick checklist

| Step | What to do | Pass? |
|------|------------|-------|
| 1 | Start server with `./tam-rfe serve`; browser opens | |
| 2 | Reports tab: run Check and Update with test data | |
| 3 | Library tab: list appears (after adding a test report if needed) | |
| 4 | Library: View shows report content | |
| 5 | Library: Open in Google Docs (with or without Google configured) | |
| 6 | Optional: Configure Google, run `google-connect`, then Open in Google Docs opens a Doc | |
| 7 | CLI: `./tam-rfe --help` and `./tam-rfe check --test-data` work | |

---

## Troubleshooting

- **“Web directory not found”** — Run `./tam-rfe serve` from `~/taminator/taminator` (where `web/index.html` and `tam-rfe` live).
- **Library is empty** — Add a `.md` report under `~/taminator-test-data/` or `~/Documents/rh/customers/` and refresh Library.
- **Check/Update fails with “JIRA token required”** — Use “Use test data” or configure JIRA (`tam-rfe config --add-token jira_token`) and VPN.
- **Open in Google Docs fails** — Ensure `TAMINATOR_GOOGLE_CLIENT_ID` and `TAMINATOR_GOOGLE_CLIENT_SECRET` are set and you’ve run `./tam-rfe google-connect` once.
- **Port in use** — Run `./tam-rfe serve --port 9000 --no-browser` and open `http://127.0.0.1:9000`.
