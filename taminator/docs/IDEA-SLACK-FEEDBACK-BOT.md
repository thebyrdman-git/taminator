# Idea: Slack bot for Taminator feedback

**Concept:** A Slack bot that lets TAMs (or anyone in the channel) submit feedback on Taminator without leaving Slack — feature ideas, bugs, “this would be killer” suggestions, quick votes, etc.

**Why it would help:**
- Feedback lands where the team already is (e.g. #tam-automation-tools or a dedicated #taminator-feedback).
- No context switching: “oh man, if I had a slack bot for feedback on the tool, wow” — capture that moment in-channel.
- Can tie into existing workflows (e.g. create GitLab issues, log to a sheet, or post to a feedback repo).
- Optional: slash commands (e.g. `/taminator feedback <message>`), shortcuts, or a simple “reply to this message with feedback” flow.

**Possible scope (for later):**
- Slash command or app mention: e.g. `/taminator feedback &lt;text&gt;` or `@TaminatorBot feedback &lt;text&gt;`.
- Optional: prompt for type (bug / idea / praise) and optionally customer or area (e.g. “reports”, “JIRA”).
- Backend: receive webhook from Slack, optionally create GitLab issue or append to a feedback log, post confirmation in thread.
- No PII/customer data in Slack — keep feedback high-level or anonymized per policy.

**Status:** Idea only; not scheduled. Useful to have when prioritizing “listen to users” improvements post–tech preview.
