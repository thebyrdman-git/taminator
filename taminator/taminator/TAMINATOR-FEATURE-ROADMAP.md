# Taminator Feature Roadmap

**Scope:** Only features directly related to **feature request (RFE) and bug report generation** are in scope. No other features are planned.

See [PRODUCT_STRATEGY.md](../PRODUCT_STRATEGY.md) for the product direction. See [FEEDBACK.md](../FEEDBACK.md) for how requests are collected and prioritized.

---

## Phase 1: Report generation (current focus)

**Goal:** Generate and maintain RFE and bug reports that are correct, consistent, and useful. TAMs trust and use them.

**In scope:**

- **Report pipeline:** Ingest source data (JIRA, cases), produce a single well-formatted RFE and bug report (e.g. markdown). Consistent structure, fields, and links.
- **Browser UI:** Primary interface. Run `tam-rfe serve`; use the web app for check, update, config, library. Meets [Enterprise UX Standards](../docs/ENTERPRISE_UX_STANDARDS.md).
- **CLI parity:** Every capability in the browser is available via `tam-rfe` (check, update, config, etc.). Same features, same behavior.
- **Reliability:** Clear errors, no silent failures. Auth (VPN, tokens) and status indicators that reflect real state.

**Done when:** Reports are accurate (statuses match JIRA), consistent (same format every time), and TAMs choose to use them. Feedback and usage are the measure.

**Existing work (reference):**

- Browser-based web UI and `web_server.py`; CLI `tam-rfe` with check/update/config.
- Electron desktop build exists but is not the primary UI; browser is primary per product strategy.

---

## Phase 2: Feedback-driven (report generation only)

Next work is chosen **only** when it directly improves or extends RFE/bug report generation, and when feedback or usage justifies it.

**Candidate areas (all report-related):**

- **Update command:** Auto-update existing reports from current JIRA/case data. Already partially present; improvements as needed.
- **Post command:** Publish the generated report to Red Hat Customer Portal (delivery of the report).
- **Portal API integration:** Support needed for post and any report-related portal features.
- **Onboard command:** Customer onboarding wizard so a new customer is set up for report generation (e.g. config, template, search paths).
- **Report structure and templates:** Customization of section titles, defaults, and template content so the generated report matches how TAMs work.
- **Portal preview:** Preview the report as it will appear on the Customer Portal before posting (template testing, layout). Spec: `../docs/FEATURE-PORTAL-PREVIEW-SANDBOX.md` (preview portions only; no general “theme” or non-report features).

**Process:** Log requests in FEEDBACK.md or GitLab issues. Prioritize by impact and frequency of the ask. Add to roadmap only when it’s clearly about report generation and we decide to build it.

---

## Out of scope (not planned)

The following are **not** in scope. They are not related to RFE/bug report generation and are not on the roadmap.

- Clippy email assistant, AI email composition, email tone options
- Windows XP (or any cosmetic) theme system
- SkiFree or any easter-egg / game
- KAB (Knowledge Article Builder) integration
- T3 (Ticket Tracking Tool) integration
- Analytics dashboard, multi-language support, direct email sending (as a general feature)
- GitHub issue submission (tooling for the project itself, not report generation)

Specs for some of the above may exist in `docs/` for historical or reference use only; they are not planned work.

---

## Success metrics (report generation)

- TAMs use Taminator regularly for RFE/bug reports.
- Reports are accurate and consistent; fewer manual fixes.
- Time to produce or update a report decreases.
- Feedback indicates the tool is trusted for report generation.

---

## One-line summary

**Roadmap: RFE and bug report generation only. Everything else is out of scope unless feedback later justifies a report-related addition.**
