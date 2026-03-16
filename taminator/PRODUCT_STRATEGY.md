# Taminator Product Strategy

## North star

1. **Do one thing really well:** Generate RFE reports that are correct, consistent, and useful. Everything else is secondary until this is proven.
2. **Let feedback drive development:** Add or change features when real use and feedback justify them—not ahead of demand.

---

## Phase 1: Core (current focus)

**Goal:** A tool for generating and maintaining RFE and bug reports that TAMs trust and use.

- **In scope**
  - Ingest source data (e.g. JIRA, cases) needed for the report.
  - Produce a single, well-formatted RFE (and bug) report (e.g. markdown) every time.
  - Consistent structure, fields, and links so reports are predictable and easy to read.
  - Reliable runs (clear errors, no silent failures).
- **Out of scope for "v1 proven"**
  - Posting to portal, email notifications, chat UI, multiple automation scripts, optional integrations. These stay available but are not part of the "core" promise until report generation is validated.

**Definition of "really well":** Reports are accurate (statuses match JIRA), consistent (same format every time), and TAMs choose to use them. Feedback and usage are the measure.

---

## Phase 2 and beyond: Feedback-driven

- New features (portal post, notifications, new data sources, UX improvements) are added **when**:
  - Someone asks for them or reports a pain, or
  - Usage shows a clear gap (e.g. "I always do X after generating the report").
- Prioritization: impact and frequency of the ask, not size of the feature.
- If a feature gets no use or negative feedback, simplify or remove it rather than maintaining it "in case."

---

## UI direction: Browser-based GUI + terminal feature parity

- **GUI:** Browser-based. No Electron or desktop app as the primary UI. Run a small web app (e.g. local or internal server) and use it in the browser. Easier to deploy, update, and use on any machine with VPN.
- **Terminal:** Feature parity with the browser. Every capability in the browser (generate report, check status, config, pick customer, etc.) is available via the CLI (`tam-rfe`). The terminal is not a second-class path—power users and automation use the same features as the GUI.
- **Implication:** Build one core (report generation, auth, customer list, etc.) and expose it via (1) browser UI and (2) CLI. New features are added to both so parity is maintained.
- **Enterprise UX standard:** All UI and CLI UX must meet the developer standard for enterprise-grade experience. See [docs/ENTERPRISE_UX_STANDARDS.md](docs/ENTERPRISE_UX_STANDARDS.md) for clarity, accessibility, errors, security, performance, and consistency.

---

## What "strip down" means in practice

- **Keep and improve:** Report generation pipeline (data → template → output). One clear path: e.g. `tam-rfe update <customer>` (and optionally `check`) as the main way to get a report.
- **Treat as secondary for now:** Portal post, chat, monitor scripts, onboarding flows, multiple entry points. Don't remove them necessarily, but don't expand them until core report generation is validated.
- **Simplify over time:** Prefer one CLI entry, one report format, one primary data path. Cut or consolidate code paths that duplicate "generate a report" without adding proven value.
- **Document the core first:** "How to generate an RFE report" is the main doc; other docs support that or are clearly marked "optional/advanced."

---

## Feedback loop

- **Get the tool (coworkers):** Official repo only: https://gitlab.cee.redhat.com/jbyrd/taminator — clone and share this link. GitLab only for now.
- **Collect:** Usage (which commands/customers), support questions, and explicit asks ("I wish it did X") via GitLab issues or direct contact.
- **Decide:** Does this support "report generation really well" (Phase 1) or a later phase? If later, park it in a backlog until Phase 1 is solid.
- **Build:** Small, shippable changes. Prefer "make the report better" over "add another integration" until feedback says otherwise.

---

## One-line summary

**Nail RFE report generation; let user feedback decide what comes next.**
