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

---

## Near term

- **Credential storage & secret management** — **Done (encoded):** JIRA/Portal/Hydra tokens in `~/.config/taminator/ui_tokens.json` are now stored as a base64-encoded payload (pull-secret style), not plaintext. Legacy plain JSON is still read so existing files keep working. **Longer term:** Optional support for a proper secret store (e.g. HashiCorp Vault). See [SECURITY-PROTECTION-LAYERS.md](taminator/SECURITY-PROTECTION-LAYERS.md).
- **JIRA watchers and clones** — Track watchers and clone/backport links (see RFE doc).
- **Slack feedback bot** — Optional bot to collect feedback in Slack (idea doc).

---

## Future ideas

- **Additional integrations** — Considered as TAMs suggest them.

---

*Last updated: 2026. This file lives in the repo; update it as plans change.*
