# RFE: Report scheduler

**Source:** TAM feedback (jbyrd) — report scheduler would be nice.

**One-liner:** Allow report updates to run on a configurable schedule (e.g. weekly) without manual action.

---

## Problem

- Reports are only updated when someone runs Check/Update manually.
- No way to run "every Monday" or "refresh before QBR" without manual action.

## Proposed direction

- **Report scheduler:** Define schedules (e.g. cron-like or "weekly on Monday 8am") per account or per report.
- The tool runs the same logic as "Update report" (and optionally full refresh) on that schedule.

## Scope

**In scope**

- Defining and storing schedules (per account or report).
- A runner: cron job, systemd timer, or built-in scheduler that executes updates.
- Logging and basic "last run" status.

**Out of scope (for this RFE)**

- UI for editing cron on the server.
- Complex dependencies between reports.
- Mandatory Slack/email (see [RFE-SLACK-NOTIFICATIONS.md](RFE-SLACK-NOTIFICATIONS.md) for optional notifications).

## Implementation notes

*(To be filled when scoping implementation.)*

- Could be implemented as a wrapper that runs `tam-rfe update <customer>` on a schedule, or a small daemon that reads a config file and triggers updates.
- Optional: integrate with Slack so TAMs are notified when a scheduled run completes (separate RFE).
