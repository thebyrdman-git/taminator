# RFE ideas for Taminator

Implementation and scope for each idea are in separate docs under `taminator/docs/`. See [ROADMAP.md](ROADMAP.md) for what’s implemented and near-term; see [taminator/docs/RFE-IDEA-INDEX.md](taminator/docs/RFE-IDEA-INDEX.md) for the index and how to add new ideas.

---

## 1. Reduce manual editing (KAB / starting-point workflow)

Support KAB (or similar) as a starting point and reduce manual editing before sending to customers.

- **Doc:** [taminator/docs/RFE-REDUCE-MANUAL-EDITING-KAB.md](taminator/docs/RFE-REDUCE-MANUAL-EDITING-KAB.md)

---

## 2. Template library

Template library for reports and customer-facing content.

- **Doc:** [taminator/docs/RFE-TEMPLATE-LIBRARY.md](taminator/docs/RFE-TEMPLATE-LIBRARY.md)

---

## 3. Ansible orchestration

Orchestrate template library and report operations via Ansible playbooks.

- **Doc:** [taminator/docs/RFE-ANSIBLE-ORCHESTRATION.md](taminator/docs/RFE-ANSIBLE-ORCHESTRATION.md)

---

## 4. Report scheduler

Run report updates on a configurable schedule (e.g. weekly).

- **Doc:** [taminator/docs/RFE-REPORT-SCHEDULER.md](taminator/docs/RFE-REPORT-SCHEDULER.md)

---

## 5. Slack notifications when reports updated

Notify in Slack when reports have been updated (manual or scheduled).

- **Doc:** [taminator/docs/RFE-SLACK-NOTIFICATIONS.md](taminator/docs/RFE-SLACK-NOTIFICATIONS.md)

---

## Other ideas (existing)

- **JIRA watchers + cloned/backport tracking** — [taminator/docs/RFE-JIRA-WATCHERS-AND-CLONES.md](taminator/docs/RFE-JIRA-WATCHERS-AND-CLONES.md)
- **Slack feedback bot** — Optional bot to collect TAM feedback in Slack. See [ROADMAP.md](ROADMAP.md) → Near term.

---

*Add new ideas in [taminator/docs/](taminator/docs/) as RFE-*.md and list them here and in [ROADMAP.md](ROADMAP.md). [Open an issue in GitLab](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues) to track.*
