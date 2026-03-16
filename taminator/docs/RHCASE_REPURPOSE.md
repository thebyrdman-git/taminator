# Repurposing rhcase Code for Taminator

This document summarizes the **rhcase** repo (`https://gitlab.cee.redhat.com/gvaughn/rhcase`) and what can be reused in Taminator for RFE/bug report data.

**Important:** The current rhcase CLI uses **case search** (Hydra SOLR API), not a `rhcase list` subcommand. Taminator’s existing code assumed `rhcase list <account> --months 1` (subprocess). Repurposing means either calling the **Hydra REST API** directly from Taminator (using rhcase’s logic) or invoking `rhcase case search --account N` and parsing output.

---

## 1. Repo layout (relevant parts)

| Path | Purpose |
|------|---------|
| `src/rhcase/cli.py` | Entry point; routes to `case`, `jira`, `kcs`, `attachments`, `accounts`. |
| `src/rhcase/scripts/rh_case.py` | Case **search** and **fetch** via Hydra SOLR; comments API. |
| `src/rhcase/scripts/rh_jira.py` | JIRA **search** and **fetch** (issues.redhat.com); PAT or basic auth. |
| `src/rhcase/config.py` | Config path; credentials from env (REDHAT_USERNAME, REDHAT_PASSWORD). |

---

## 2. Case discovery: Hydra SOLR (rh_case.py)

**API:** `GET https://access.redhat.com/hydra/rest/search/cases`  
**Auth:** Bearer token (from Red Hat SSO).

**Token:** Same as Taminator’s Portal/Hydra token. rhcase gets it via:

- `get_bearer_token(username, password)` → `https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token` with `client_id=hydra-client-cli`, `grant_type=password`.

Taminator already has Portal/Hydra token (env or UI). If that token works for Hydra search, use it; otherwise use the same SSO token flow as rhcase.

**Query building:** `build_solr_query()` in `rh_case.py` (lines ~407–488).

- **Required:** `account_numbers` → `(case_accountNumber:123 OR case_accountNumber:456)`.
- **Optional:** `products`, `exclude_products`, `severities`, `statuses`, `include_closed`, `owner`, `created_after`, `modified_after`, `text_search`.
- **Exclude closed (default):** `NOT case_status:Closed`.
- **Date window:** `created_after` / `modified_after` in `YYYY-MM-DD` → SOLR date range.

For Taminator “cases in last N months” use `modified_after` (or `created_after`) set to N months ago.

**Search call:** `search_cases(token, query, start=0, rows=100)` → GET with `q`, `start`, `rows`. Returns SOLR JSON: `response.docs[]`.

**Per-doc fields (list):** `format_case_for_list(doc)` normalizes a SOLR doc to:

- `case_number`, `summary` (case_summary), `status` / `status_full`, `sbr` (case_sbr), `product`, `severity`, `owner`, `contact`, `opened_date`, `created_date`, `modified_date`, etc.

**Repurpose for Taminator:**

- Use **Bearer token** (Portal/Hydra token or obtain via SSO as in rhcase).
- Build SOLR query with `build_solr_query(account_numbers=[...], include_closed=False, modified_after=<N months ago>)` (and optional `products` for SBR/product filter).
- Call `search_cases(token, query, start=0, rows=500)` (or page as needed).
- Map each `doc` with `format_case_for_list(doc)` (or a minimal version) to get `case_number`, `summary`, `status`; classify RFE vs Bug from `summary` (e.g. `[RFE]` / `[BUG]`) and optionally from `product`/`sbr`.
- Optionally **fetch full case** with `fetch_case_from_solr(case_number, token)` to get `linked_resources` (JIRA refs) or other detail.

**Copy/adapt:**

- `build_solr_query()` (and any date helpers).
- `search_cases()`.
- `format_case_for_list()` (or a slim variant: `case_number`, `case_summary`, `case_status`, `case_sbr`).
- `get_bearer_token()` if Taminator will use username/password for Hydra instead of an existing token.

---

## 3. JIRA (rh_jira.py)

**Auth:** `JIRA_API_TOKEN` (PAT) or `REDHAT_USERNAME` / `REDHAT_PASSWORD` (basic auth). Taminator already uses JIRA Bearer token; rhcase uses PAT or basic. Both hit `https://issues.redhat.com`.

**Use in Taminator:**

- **Search:** `JiraClient.search(query, max_results, fields, filters)` — builds JQL from text or `jql:` prefix; returns `issues[]` with `key`, `summary`, `status`, etc. Useful if you want to discover JIRA issues by JQL (e.g. by project/account) instead of only refreshing status for keys from the report.
- **Fetch:** `JiraClient.fetch(issue_key, include_comments, fields)` — get full issue. Taminator’s `JIRAClient.get_issue_status()` already fetches one issue; rhcase’s fetch is richer (comments, more fields).

**Repurpose:**

- If Taminator stays with “report has JIRA IDs → refresh status only,” the existing Taminator JIRA client is enough.
- If you want “find JIRA issues linked to account/cases,” consider reusing `JiraClient.search()` and `_build_jql()` (e.g. filter by project, labels, or text) and/or use Hydra’s full case fetch to read `linked_resources` for JIRA keys.

---

## 4. Config and credentials

- **rhcase:** `~/.config/rhcase/config.yaml`; env `REDHAT_USERNAME`, `REDHAT_PASSWORD`; optional `~/.config/tamscripts/tamscripts.config` for account aliases (YAML).
- **Taminator:** `~/.config/taminator/` (accounts.json, report_structure.json, ui_tokens.json). Token types: JIRA, Portal, Hydra.

**Repurpose:** Use Taminator’s existing Portal/Hydra token for Hydra search. If rhcase’s SSO token flow is needed (e.g. no stored Hydra token), port `get_credentials()` and `get_bearer_token()` from `rh_case.py` and call them when Hydra is used and no token is set.

---

## 5. Suggested integration steps

1. **Case discovery in Taminator**
   - Add a **Hydra case search** path next to (or instead of) the current subprocess `rhcase list`:
     - Get Hydra Bearer token (from Taminator config/env or SSO as in rhcase).
     - Build SOLR query from account number(s) and “modified in last N months” (and optional product/SBR filter).
     - Call Hydra `search/cases` and normalize with a `format_case_for_list`-style function.
   - Use this in `_try_populate_from_rhcase()` (or rename to `_try_populate_from_hydra()`): when report is empty, call Hydra search, then inject rows (case number, summary, status; JIRA ID from summary or from full-case `linked_resources` if you fetch per case).

2. **Optional: call rhcase CLI**
   - Alternatively run `rhcase case search --account <N> --include-closed` (and `-o json` if supported) and parse JSON. Then you depend on rhcase being installed and its output format; the API approach above keeps Taminator independent and reuses the same contract as the official tool.

3. **JIRA**
   - Keep using Taminator’s JIRA client for status refresh. Add rhcase’s `JiraClient.search()` only if you need JIRA-side discovery (e.g. by JQL) for reports.

4. **Docs**
   - Update `docs/DATA_SOURCES.md` to state that case discovery uses the **Hydra SOLR API** (and optionally rhcase CLI), with reference to this repurpose doc and to the rhcase repo.

---

## 6. Key code references (rhcase repo)

| Need | File | Functions / logic |
|------|------|-------------------|
| Hydra token | `rh_case.py` | `get_credentials()`, `get_bearer_token()` |
| SOLR query | `rh_case.py` | `build_solr_query()` |
| Case search | `rh_case.py` | `search_cases()` |
| Case list shape | `rh_case.py` | `format_case_for_list()` |
| Full case (JIRA links) | `rh_case.py` | `fetch_case_from_solr()`, `format_case_for_display()` (has `linked_resources`) |
| JIRA search/fetch | `rh_jira.py` | `JiraClient`, `JiraCredentials`, `search()`, `fetch()`, `_build_jql()` |

---

## 7. SOLR response shape (minimal)

From `search_cases()`:

- `response.docs[]` — each doc has at least: `case_number`, `case_summary`, `case_status`, `case_sbr` (list), `case_product` (list), `case_createdDate`, `case_lastModifiedDate`, `case_accountNumber`, `case_owner`, `case_contactName`, etc. Full case fetch adds `case_linked_resource` and other fields.

This gives you everything needed to build RFE/Bug table rows (case number, summary, status, SBR/product for filter) and optionally to resolve JIRA IDs via full-case fetch or by parsing summary.
