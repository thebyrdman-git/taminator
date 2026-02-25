# RFE: JIRA watchers + cloned/backport tracking (Matt Robson)

**Source:** Senior TAM feedback — Matt Robson  
**Summary:** Two "killer" features: (1) track cloned JIRAs when backports are generated; (2) detect when a TAM is not watching a JIRA and let them watch it from the app.

**Scope / impact:**  
There is a wide spread in how many JIRAs TAMs watch; many watch relatively few issues. Surfacing "you're not watching this issue" and offering one-click Watch could significantly improve effective tracking without requiring TAMs to hunt in JIRA. This feature set is a candidate for a post–tech-preview release.

**Do not delay tech preview.** Ship the tech preview so folks can start using it and you can demo it. Implement watchers + clones in a follow-on release after the preview is out.

---

## Feature 1: Track cloned JIRAs when backports are generated

**Idea:** When a JIRA is cloned for a backport, Taminator should show that relationship (e.g. "Cloned by: OCPBUGS-12345") so TAMs see the full picture.

**How to achieve it**

- JIRA exposes **issue links** on each issue. When you clone an issue or create a backport, JIRA creates a link (e.g. "Cloners", "is cloned by", or similar depending on project).
- Use the same REST API Taminator already uses: `GET /rest/api/2/issue/{issueKey}` and request the `issuelinks` field (or use the Fields enum that includes links).
- Response shape is like:
  - `fields.issuelinks` → list of `{ "type": { "name": "Cloners", "inward": "is cloned by", "outward": "clones" }, "inwardIssue" or "outwardIssue": { "key": "OCPBUGS-12345", "fields.summary": "..." } }`
- In Taminator:
  - **Where:** In the same place you already fetch issue status (e.g. `JIRAClient.get_issue_status()` in `taminator/commands/check.py`, or a small helper that calls `GET .../issue/{key}?fields=status,summary,issuelinks`).
  - **What to do:** When building the report or the Check/Update result, for each issue key also fetch `issuelinks`. Filter for link types that mean "clone" or "backport" (e.g. type name containing "lon" or "ackport", or use your project's link type names). Then either:
    - **In the report:** Add a column or a line per issue like "Backports: OCPBUGS-12345, OCPBUGS-12346".
    - **In the UI:** In the Check/Update or report view, show "Clones/backports: …" with links to those issues.
  - **No new credentials** — same JIRA token you already use for status checks.

**Concrete steps**

1. Extend `JIRAClient` (or add a method) to call `GET /rest/api/2/issue/{key}?fields=issuelinks` (and any other fields you need).
2. Parse `issuelinks` and map link type names to "clone/backport" (e.g. "Cloners", "Backport", "is backported by" — check your JIRA project's link types).
3. Add the list of related clone/backport keys to the data you already pass to the report or UI.
4. In the report template or UI, render that list (and optionally links to those issues).

---

## Feature 2: Note if a TAM is not watching a JIRA and let them watch it

**Idea:** If a TAM isn't watching an issue, they're not tracking it effectively. The app should detect "you're not watching this issue" and offer a "Watch" action.

**How to achieve it**

- JIRA exposes **watchers** per issue: who is watching the issue.
- You need the **current user's JIRA username** (or accountId for JIRA Cloud). Red Hat's JIRA (issues.redhat.com) is likely Server/Data Center, so the watchers list is usually usernames.
- **Endpoints (typical JIRA Server):**
  - `GET /rest/api/2/issue/{issueKey}/watchers` — returns something like `{ "watchers": [ { "name": "jbyrd", "displayName": "..." }, ... ], "isWatching": true/false }`.  
    Some versions also have `isWatching` on the issue when you request the right field.
  - To add the current user as watcher: `POST /rest/api/2/issue/{issueKey}/watchers` with body `"jbyrd"` (raw string) or `{ "name": "jbyrd" }` depending on API version.
- In Taminator:
  - **Current user:** You need the TAM's JIRA username. Options: (a) from the same token (decode or call something like "current user" if the API provides it), (b) from config (e.g. "JIRA username" in Settings, or from REDHAT_USERNAME if that matches), or (c) from a small JIRA endpoint like "myself" if available.
  - **Where:** When you already fetch issue status for Check/Update (or when building the report), also call `GET .../issue/{key}/watchers` (or include watchers in the issue request if the API allows).
  - **Logic:** Compare the current user to the watchers list. If the user is not in the list, mark the issue as "Not watching" in the UI/report.
  - **UI:** In the report view or Check result, for each issue show an indicator: "You're not watching" and a button "Watch". The button calls your backend; the backend does `POST .../issue/{key}/watchers` with the current user, then refreshes or shows "Watching".
  - **Permissions:** The JIRA token must be allowed to add the current user as a watcher (normal for one's own user).

**Concrete steps**

1. **Resolve current JIRA user**  
   - Option A: Add a "JIRA username" (or "Red Hat username") in Taminator Settings and use that.  
   - Option B: If the JIRA API exposes "current user" (e.g. `GET /rest/api/2/myself` or similar), call it once with the same token and store the username.

2. **For each issue in the report (or in Check/Update):**  
   - Call `GET /rest/api/2/issue/{issueKey}/watchers`.  
   - If the current user is not in `watchers`, add a flag to that issue in the data you send to the UI (e.g. `not_watching: true`).

3. **In the UI:**  
   - For issues with `not_watching: true`, show a short line: "You're not watching this issue" and a "Watch" button.

4. **Backend endpoint for Watch:**  
   - Add a small endpoint in the web server (e.g. `POST /api/jira/watch`) that takes `{ "issue_key": "AAPRFE-123" }`, uses the same JIRA token and current user, and calls `POST /rest/api/2/issue/{issueKey}/watchers` with the username. Return success/failure so the UI can update.

5. **Rate limiting:**  
   - If you have many issues, consider batching watcher checks or doing them on demand when the user expands an issue, to avoid too many requests.

---

## Where in the codebase

| Feature            | Where to add logic                          | What's already there              |
|--------------------|---------------------------------------------|-----------------------------------|
| Cloned/backport    | `taminator/commands/check.py` (and/or update)| `JIRAClient`, `get_issue_status()`|
| Cloned/backport    | Report template or UI                       | Report table, Check result view   |
| Watchers check     | Same place you fetch issue status           | Same `JIRAClient` + token         |
| Watchers check     | Config / "current user"                     | Settings, tokens                  |
| "Watch" button     | Web UI (e.g. report or Check result)        | `index.html`, result panel        |
| "Watch" API        | `taminator/web_server.py`                   | Other `/api/` handlers             |

---

## References

- JIRA REST API (adjust base URL to `https://issues.redhat.com/rest/api/2`):
  - Issue: `GET /issue/{key}` — use `fields=issuelinks,...` for links.
  - Watchers: `GET /issue/{key}/watchers`, `POST /issue/{key}/watchers`.
- Taminator already uses: `JIRAClient` in `src/taminator/commands/check.py` with `issues.redhat.com` and Bearer token.

Once you have "current JIRA user" and one extra field (issuelinks or watchers) per issue, the rest is wiring in the report and UI.
