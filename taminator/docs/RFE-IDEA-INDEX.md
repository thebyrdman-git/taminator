# RFE idea index: implementation and scope

This index points to **implementation and scope details** for each RFE idea. Use it to find the full write-up for an idea; use [ROADMAP.md](../ROADMAP.md) for release timing and [GitLab issues](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues) for tracking.

**Where to store details**

- **One doc per idea** in `docs/`: `RFE-<short-name>.md` (e.g. `RFE-TEMPLATE-LIBRARY.md`).
- Each doc contains: problem, proposed solution, scope (in/out), one-liner, and (when ready) implementation notes.
- **ROADMAP.md** lists ideas and links to these docs under "Near term" or "Future ideas."
- **GitLab issues** can hold the one-liner and link to the doc: *"Full implementation/scope: see `docs/RFE-<name>.md`."*

---

## Index of RFE ideas (TAM sync / feedback)

| RFE | Doc | One-line summary |
|-----|-----|------------------|
| 1 | [RFE-REDUCE-MANUAL-EDITING-KAB.md](RFE-REDUCE-MANUAL-EDITING-KAB.md) | KAB (or similar) as starting point; reduce manual editing before sending to customers. |
| 2 | [RFE-TEMPLATE-LIBRARY.md](RFE-TEMPLATE-LIBRARY.md) | Template library for reports and customer-facing content. |
| 3 | [RFE-ANSIBLE-ORCHESTRATION.md](RFE-ANSIBLE-ORCHESTRATION.md) | Orchestrate template library and report operations via Ansible playbooks. |
| 4 | [RFE-REPORT-SCHEDULER.md](RFE-REPORT-SCHEDULER.md) | Report scheduler: run report updates on a schedule. |
| 5 | [RFE-SLACK-NOTIFICATIONS.md](RFE-SLACK-NOTIFICATIONS.md) | Notify in Slack when reports have been updated. |

---

*Add new ideas as a row in the table and a new `RFE-*.md` in `docs/`. Update ROADMAP.md when something moves to "Near term" or "Implemented".*
