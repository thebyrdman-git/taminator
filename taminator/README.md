# Taminator — Full User Guide

This is the full user guide for Taminator. It is available in the app (User Guide panel) and on GitLab.

**GitLab repository:** https://gitlab.cee.redhat.com/jbyrd/taminator

---

## What is Taminator?

Taminator generates and maintains RFE and bug reports for Red Hat TAMs. It uses JIRA and case data to produce consistent markdown reports and can post to customer portal groups. Typical use saves 2–3 hours per customer per week compared to manual tracking.

- **Desktop app (recommended for UI)** — Double-click the Taminator app; it opens in its own window with the full UI. No terminal required.
- **CLI** — Optional, for automation and advanced users.
- **Report workflow** — Create reports, check status against JIRA, update reports, and optionally post to the customer portal.

---

## Where to get Taminator

**Official (Red Hat coworkers only):** https://gitlab.cee.redhat.com/jbyrd/taminator

Requires Red Hat VPN and GitLab CEE access.

- **Desktop app (recommended):** Download AppImage (Linux) or DMG (macOS) from the [GitLab releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases) page. Double-click to open Taminator in its own app window. No terminal required.
- **From repo:** `git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git ~/taminator` (for CLI or development).

---

## Prerequisites

- **Red Hat VPN** — Required for JIRA and internal APIs.
- **JIRA API token** — From issues.redhat.com → Personal Access Tokens. Configure in the app under Settings.
- **Customer Portal token** (optional, for posting) — From access.redhat.com/management/api → Generate Token.
- **Python 3.7+** — Only if running from repo (CLI/development). Not required for the desktop app.

---

## Installation

### Desktop app (no terminal required)

Double-click the Taminator app; it opens in its own window with the Taminator UI. No terminal commands needed.

- **Linux:** Download the AppImage from GitLab releases, then double-click (or run from file manager).
- **macOS:** Download the DMG, drag Taminator to Applications, then double-click. First time: right-click → Open to bypass Gatekeeper if prompted.

### From repo (optional)

For CLI or to run the UI from source: `git clone ...`, then `cd taminator/taminator && ./tam-rfe serve`. Desktop app is easier for UI users.

---

## CLI commands

| Command | Description |
|---------|-------------|
| `tam-rfe check <customer>` | Compare report to JIRA; no file changes. |
| `tam-rfe update <customer>` | Fetch JIRA statuses and write to the report file. |
| `tam-rfe post <customer>` | Post report to Red Hat Customer Portal. |
| `tam-rfe onboard <customer>` | Onboard a new customer (interactive). |
| `tam-rfe config` | Manage tokens and configuration. |
| `tam-rfe docs` | Show full user guide in the terminal. |
| `tam-rfe serve` | Start browser-based UI (default http://127.0.0.1:8765). |
| `tam-rfe serve --no-browser --port 9000` | Serve UI without opening a browser. |

Options: `--test-data` (use sample data), `--help`, `--version` / `-V`.

---

## Browser UI

1. **Start** — Double-click the Taminator desktop app. It opens in its own window. (No terminal required.)
2. **Report Manager** (landing page) — Create new reports, customize the template, add accounts.
3. **Check/Update Reports** — Enter a customer and run Check report or Update report.
4. **Library** — View and manage report files.
5. **Settings** — VPN check, tokens (JIRA, Portal, Hydra), Google Drive/Docs, report paths.
6. **User Guide** — In-app documentation (this guide).

Reports are markdown files. The app looks for them in:

- `~/taminator-test-data`
- `~/Documents/rh/customers`
- `/tmp/taminator-test-data`

---

## Authentication

- **VPN** — Connect to Red Hat VPN before using real customer data. Verify in Settings → Check VPN. (VPN check is skipped when JIRA Cloud is configured.)
- **JIRA token** — Required for Check and Update. Add in Settings. See **JIRA Cloud** below if you use an Atlassian Cloud site.
- **Portal token** — Required for posting to the customer portal. Add in Settings.
- **Hydra** — Uses Portal token or Red Hat username/password (env or Settings).

Tokens are stored locally in `~/.config/taminator/ui_tokens.json`. Environment variables `REDHAT_USERNAME` / `REDHAT_PASSWORD` override if set.

---

## JIRA Cloud

Taminator can use **Red Hat JIRA** (issues.redhat.com) or **JIRA Cloud** (e.g. `https://your-tenant.atlassian.net`). The same Check and Update flow works for both.

**Red Hat JIRA (default)**  
Leave **JIRA base URL** as `https://issues.redhat.com` (or leave the field blank). In Settings → Token configuration, set **Red Hat JIRA token** (Personal Access Token from issues.redhat.com → View Profile → Personal Access Tokens).

**JIRA Cloud**  
1. In Settings → Token configuration → **JIRA instance**, set **JIRA base URL** to your Atlassian site, e.g. `https://your-tenant.atlassian.net`.
2. The **JIRA Cloud** section appears. Enter your **Email** (Atlassian account) and **API token** (create one at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)).
3. Click **Save JIRA settings**. Report links and Check/Update will use this instance.

**Environment variables (optional)**  
- `JIRA_BASE_URL` — Override JIRA base (e.g. `https://your-tenant.atlassian.net`).
- `JIRA_TOKEN_API_TOKEN` — Bearer token for Red Hat JIRA.
- `JIRA_EMAIL` and `JIRA_API_TOKEN` — For JIRA Cloud (when base URL is `*.atlassian.net`).

**In-app guidance**  
When your configured JIRA base URL is a Cloud site (`*.atlassian.net`), the app shows Cloud-specific instructions for obtaining a token: the "How to obtain" steps in Settings and in CLI (`tam-rfe config --add-token`) point to [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens) and the email + API token flow. When the base URL is Red Hat (default), the same screens point to issues.redhat.com and the Personal Access Token flow.

Full plan and technical details: [docs/JIRA_CLOUD_INTEGRATION.md](taminator/docs/JIRA_CLOUD_INTEGRATION.md) (in the repo).

---

## Credentials & Vault

- **Local storage** — JIRA, Portal, and Hydra credentials saved from Settings are stored in `~/.config/taminator/ui_tokens.json` in **encoded form** (base64 payload), not as plaintext. The file is still protected by normal filesystem permissions (mode 0600). Existing plaintext files are still read; the next save upgrades them to the encoded format.
- **Optional: HashiCorp Vault** — If your team uses HashiCorp Vault, you can set `VAULT_ADDR` and `VAULT_TOKEN` (and optionally `VAULT_NAMESPACE`) before starting the app or `tam-rfe`. Tokens are then read from Vault when available, and saving a token from Settings syncs it to Vault as well. For setup, migration, and security notes, see **[Vault integration](taminator/docs/VAULT_INTEGRATION.md)** (in the repo: `taminator/docs/VAULT_INTEGRATION.md`).

---

## Report workflow

1. **Create a report** — Report Manager → Build new report (add account with SBR Group and account numbers first).
2. **Check report** — Compare the report to JIRA; see differences without changing the file.
3. **Update report** — Write current JIRA statuses into the report file (creates a backup first).
4. **Post** — Optionally post the report to the customer portal (CLI: `tam-rfe post <customer>`).

Report structure uses standard section headings and table columns so the app can reliably find and update statuses. The onboarding template creates this structure.

---

## Customer Portal Groups

Customer Portal Groups are private Red Hat Customer Portal spaces where you can post RFE and bug reports as discussions for a specific customer. Taminator can create new discussions in a group so the customer sees the latest tracker in one place.

- **What you need** — A Red Hat Customer Portal API token (Settings → Token configuration → Red Hat Customer Portal). The token must have access to the group.
- **Adding a portal group** — In Report Manager, when you add or edit an account, you can set the **Portal group ID** for that customer (the numeric ID from the group's URL, e.g. `https://access.redhat.com/groups/4357341` → group ID `4357341`). You can also add multiple groups per customer if your workflow requires it.
- **Posting a report** — Use **Check/Update Reports** or the CLI: `tam-rfe post <customer>`. Taminator posts the report as a **new discussion** in the customer's configured portal group(s). New discussions are created in **markdown** format by default so tables and headings render correctly in the portal.
- **Where to configure** — Settings → Customer Portal Groups (overview); Report Manager → Configured accounts (add or edit an account to set its Portal group ID).

---

## Documentation and support

- **Full user guide (this file):** Also in [USER-GUIDE.md](USER-GUIDE.md). View on GitLab: https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/USER-GUIDE.md
- **Getting started:** [GETTING-STARTED.md](taminator/GETTING-STARTED.md)
- **Releases:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- **Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Contact:** jbyrd@redhat.com

---

*Taminator — RFE and Bug Report Generator for Red Hat TAMs.*
