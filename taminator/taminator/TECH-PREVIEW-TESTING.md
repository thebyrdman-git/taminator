# Tech Preview Testing Checklist

Use this list to validate the 2.0.0-tech-preview before wider rollout.

**To run the UI:** Double-click the Taminator desktop app (AppImage on Linux, DMG on macOS); it opens in its own window. No terminal required. Alternatively, from repo: `cd taminator/taminator && ./tam-rfe serve` (or use CLI only).

---

## Prerequisites

- [ ] Red Hat VPN connected
- [ ] JIRA token configured (Settings in UI or env)
- [ ] Portal token (or REDHAT_USERNAME/REDHAT_PASSWORD) for Hydra/case discovery
- [ ] At least one customer/account with a report or use “Use test data” for smoke tests

---

## Web UI — Check and Update

- [ ] **Check report** — Enter customer (or account) or check “Use test data”; run Check. Result shows comparison or output; no crash.
- [ ] **Update report** — Same; run Update. Result shows success or error; report file (if present) is updated.
- [ ] **Full refresh** — Check “Full refresh”, run Update. Discovery runs (Hydra or rhcase); report is repopulated when applicable.
- [ ] **Summary counts** — After Update, report “Summary: N total cases (X RFE, Y Bug)” matches actual table row counts.

---

## Debug options (UI)

- [ ] **Debug checkbox** — Check “Debug: include Hydra/JIRA diagnostics in result”, run Check or Update. Result includes extra lines (e.g. `[hydra]`, `[jira]`, `[rhcase]` when relevant).
- [ ] **Download debug report** — After any run with result, click “Download debug report”. File downloads (e.g. `taminator-debug-YYYYMMDD-HHMMSS.txt`) with same content as result.
- [ ] **Report issue in GitLab** — Click “Report issue in GitLab”. Clipboard gets result; GitLab new-issue page opens in browser. Paste into description and submit (optional).

---

## CLI

- [ ] **Check** — `./tam-rfe check <customer>` or `./tam-rfe check --test-data`. Exits 0 and prints table or output.
- [ ] **Update** — `./tam-rfe update <customer> -y`. Exits 0 and updates report when applicable.
- [ ] **Report issue (GitLab)** — `./tam-rfe report-issue --gitlab`. Browser opens GitLab new-issue URL.
- [ ] **Report issue with debug file** — `./tam-rfe report-issue --gitlab --debug-report ./path/to/debug.txt`. Content of file is printed; browser opens. You can paste into issue.

---

## JIRA and discovery

- [ ] **Multiple JIRA prefixes** — Report or discovery includes at least one of: AAPRFE-, AAP-, ANSTRAT-, RHEL-, OCPBUGS- (or other mapped project). Rows are found and status is refreshed (Check/Update).
- [ ] **External trackers** — For a case whose JIRA appears only in external trackers (not in summary), run Update with Full refresh + Debug. Case appears in report with correct JIRA; debug output shows external tracker data when JIRA was missing in earlier logic.
- [ ] **Links** — Report table shows JIRA IDs as links to `https://issues.redhat.com/browse/<KEY>` and case numbers as links to `https://access.redhat.com/support/cases/#/case/<number>` where applicable.

---

## Report Manager and Library

- [ ] **Build report** — Report Manager: add or select account, build new report. Report is created; account appears in configured list.
- [ ] **Library** — Library lists report files that have been created. Open a report; “Copy to clipboard”, “Open in Google Docs” (if configured; opens as formatted Doc with headings/sections) work.
- [ ] **Delete** — Delete a report from Library; list updates.

---

## Regression / stability

- [ ] **No crash** — Check and Update with invalid customer name show clear error, no traceback.
- [ ] **Tokens** — Settings shows token status (VPN, JIRA, Portal, Hydra, Google). Refresh works.
- [ ] **Fix tables** — `./tam-rfe fix-tables --dry-run` runs without error on repo with sample reports.

---

## Sign-off

- **Tester:** _____________________  
- **Date:** _____________________  
- **Notes / issues:** (paste GitLab issue links or one-line summaries)
