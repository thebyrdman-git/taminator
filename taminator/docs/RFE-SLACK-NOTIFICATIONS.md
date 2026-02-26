# RFE: Slack notifications when reports are updated

**Source:** TAM feedback (jbyrd) — notify when reports have been updated in Slack.

**One-liner:** Send a Slack notification when a report is updated (manual or scheduled) so TAMs know without opening the tool.

---

## Problem

- When reports are updated (manually or by a scheduler), there is no lightweight way to know without opening the app or checking files.

## Proposed direction

- **Slack notifications:** After a report update (and optionally after a scheduled run), post a short message to a configurable Slack channel or DM (e.g. "Report X for Account Y updated; N cases changed").

## Scope

**In scope**

- Configurable Slack webhook (or app).
- One message per update with report name, account, and brief summary.
- Optional: "only notify on schedule" or "only if changes."

**Out of scope (for this RFE)**

- Full Slack bot or approval workflows.
- Rich interactive messages (can be a later enhancement).

## Implementation notes

*(To be filled when scoping implementation.)*

- Incoming webhook is the minimal integration; no bot install required.
- Natural fit with [RFE-REPORT-SCHEDULER.md](RFE-REPORT-SCHEDULER.md): "Report X was updated by the 8am schedule."
