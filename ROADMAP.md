# Taminator Roadmap

Planned and possible future improvements. You can also view the roadmap on GitLab (set `GITLAB_ROADMAP_URL` when starting the server to see the link in the app).

---

## Implemented (recent)

- **Report formats** — Markdown, HTML, plain text, and CSV export. Implemented.
- **Roadmap in app** — View this roadmap in the UI (Roadmap nav) and optionally via CLI; optional GitLab link at bottom.
- **Gmail draft** — Create Gmail draft from report with HTML body (Google Docs–style formatting), not raw markdown. From Check/Update Reports and Library.
- **Google Drive & Docs** — Backup reports to Drive, open report as Google Doc, Create Gmail draft. One-time OAuth setup in Settings.
- **Trimmed UI copy** — Report Manager, Check/Update Reports, Library, and Settings use short copy and "See User Guide: …" links; extended instructions live in the User Guide.
- **User Guide** — Single place for long explanations; other panels link to it with anchor scroll.
- **Refresh behavior** — Hash-based panel restore so refreshing the browser keeps you on the same page.
- **Red Hat look and feel** — Red Hat color scheme for all elements; no blue links; Docs-style formatting for Gmail drafts.
- **JIRA Cloud integration** — Use Red Hat JIRA (default) or JIRA Cloud (`*.atlassian.net`). In Settings: set **JIRA base URL** (default `https://issues.redhat.com`); for Cloud, set email + API token. Check, Update, and report links use the configured instance. See User Guide → JIRA Cloud and [docs/JIRA_CLOUD_INTEGRATION.md](taminator/docs/JIRA_CLOUD_INTEGRATION.md).
- **HashiCorp Vault** — Optional secret store when `VAULT_ADDR` and `VAULT_TOKEN` are set. Settings → HashiCorp Vault: connection status, list/add/view/delete tokens, migrate from Auth Box, test connection. Hybrid auth: Vault first, fallback to local Auth Box. CLI: `tam-vault` (status, list, get/set/delete, migrate, test). See [docs/VAULT_INTEGRATION.md](taminator/docs/VAULT_INTEGRATION.md).

---

## Near term

- **Credential storage & secret management** — **Done (encoded):** JIRA/Portal/Hydra tokens in `~/.config/taminator/ui_tokens.json` are stored as a base64-encoded payload (pull-secret style), not plaintext. **Done (Vault):** Optional HashiCorp Vault integration (Settings + `tam-vault` CLI). See [SECURITY-PROTECTION-LAYERS.md](taminator/SECURITY-PROTECTION-LAYERS.md).
- **JIRA watchers and clones** — Track watchers and clone/backport links. See [RFE-JIRA-WATCHERS-AND-CLONES.md](RFE-JIRA-WATCHERS-AND-CLONES.md).
- **Slack feedback bot** — Optional bot to collect feedback in Slack (idea doc).

---

## Future ideas

- **Additional integrations** — Considered as TAMs suggest them.
- **RFE ideas (TAM sync / feedback):** See [RFE-IDEAS.md](RFE-IDEAS.md) for each idea and its scope/implementation doc.
  - [Reduce manual editing (KAB / starting-point workflow)](taminator/docs/RFE-REDUCE-MANUAL-EDITING-KAB.md)
  - [Template library](taminator/docs/RFE-TEMPLATE-LIBRARY.md)
  - [Ansible orchestration](taminator/docs/RFE-ANSIBLE-ORCHESTRATION.md)
  - [Report scheduler](taminator/docs/RFE-REPORT-SCHEDULER.md)
  - [Slack notifications when reports updated](taminator/docs/RFE-SLACK-NOTIFICATIONS.md)

---

*Last updated: 2026. This file lives in the repo; update it as plans change.*
