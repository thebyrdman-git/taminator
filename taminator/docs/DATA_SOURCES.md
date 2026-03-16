# How Taminator Pulls Data

Taminator uses two data sources for RFE and bug report generation. Both require Red Hat VPN and appropriate credentials.

---

## 1. JIRA (issues.redhat.com)

**Purpose:** Fetch current status (and summary, assignee) for JIRA issues that are already listed in the report.

**Used by:** `tam-rfe check` and `tam-rfe update`.

**Flow:**

- The report file is a markdown document that contains tables of JIRA issue keys (e.g. `AAPRFE-762`, `AAP-53458`). `CustomerReportParser.extract_jira_issues()` reads the file and collects those keys.
- `JIRAClient` (in `src/taminator/commands/check.py`) calls the JIRA REST API for each key:
  - **Endpoint:** `GET https://issues.redhat.com/rest/api/2/issue/{issue_key}`
  - **Auth:** Bearer token (`JIRA_TOKEN_API_TOKEN` or token from UI/config).
- **Response used:** `fields.status.name`, `fields.summary`, `fields.assignee`, `fields.updated`. These are used to compare “report status” vs “current status” (check) and to update the Status/Notes column in the report (update).

**What JIRA does *not* do:** It does not discover which cases or issues exist for a customer. It only refreshes status for issue keys that are already present in the report.

---

## 2. Hydra SOLR API (case discovery) — primary

**Purpose:** Discover which RFE and bug cases exist for a customer so the report can be populated with initial rows (case number, summary, status, and when available JIRA ID).

**Used by:** `tam-rfe update` when the report has **no** JIRA issues yet. The code path `_try_populate_from_rhcase()` runs:

- Resolve **account number** from the report or from `~/.config/taminator/accounts.json` (Report Manager).
- **Preferred:** Call the **Hydra SOLR API** (`https://access.redhat.com/hydra/rest/search/cases`) with a Bearer token (Portal or Hydra token). Build query via `hydra_search.build_solr_query()`, then `search_cases()`; normalize with `format_doc_for_report()`. Same API as **rhcase** (case search). See `docs/RHCASE_REPURPOSE.md`.
- **Fallback:** If no Hydra/Portal token or API fails, run `rhcase list <account> --months 1` (subprocess) and parse output.
- Insert new table rows (RFE and Bug sections). JIRA ID from summary pattern AAPRFE-xxx/AAP-xxx when present; otherwise TBD.

**Prerequisites:**

- **Hydra path:** Portal or Hydra token configured in Taminator (Settings / env). VPN required.
- **Fallback:** `rhcase` CLI installed and configured (Red Hat internal).
- Account number must be set (in the report or in Report Manager).

**What case discovery does *not* do:** It does not update existing rows’ JIRA status; that is done by the JIRA API. Discovery is only used for the initial “empty report → populated report” step.

---

## 3. Case groups under individual customer accounts

**Purpose:** Determine which SBR/product "groups" have cases for a given account, and optionally restrict discovery to those groups.

**How the API finds case groups:**

1. **By account** — Cases are tied to an account via `case_accountNumber`. The Hydra query uses `(case_accountNumber:123 OR case_accountNumber:456)` so only cases for that customer's account(s) are returned.

2. **SBR and product on each case** — Each case document has `case_sbr` (Strategic Business Relationship / team) and `case_product` (product name). These are the "case groups" (e.g. Ansible, Ansible Automation Platform). They can be lists or single values.

3. **Discovering which groups exist** — Call `hydra_search.discover_case_groups_for_account(token, account_numbers, months_back, max_rows)`. It runs a Hydra search filtered by account (and date), then collects unique `case_sbr` and `case_product` values from the returned docs. Returns `{"sbr": ["Ansible", ...], "product": ["Ansible Automation Platform", ...]}`. Use this to show the user which groups have cases or to drive filtering.

4. **Filtering discovery by group** — When populating a report, Taminator can restrict to specific SBR/product groups. In Report Manager, set **SBR groups** on the account (e.g. Ansible, Ansible Automation Platform). That list is passed as `products` to `discover_cases()`; `build_solr_query()` adds `case_product:*Ansible*` (etc.) so only cases in those groups are returned. So "case groups under the account" are both **discoverable** (what SBR/product values appear) and **filterable** (only pull cases for selected groups).

**Code:** `src/taminator/core/hydra_search.py` — `discover_case_groups_for_account()`, `build_solr_query(..., products=)`. `src/taminator/commands/update.py` — `_get_account_and_sbr_groups()` loads account and SBR groups from report + `~/.config/taminator/accounts.json` and passes `products=sbr_groups` into `discover_cases()`.

**Note:** Customer portal **discussion groups** (access.redhat.com/groups/XXX for posting reports) are a different concept and are configured per customer (e.g. `group_id` in config), not derived from the Hydra case search API.

**Case group (optional) in report generation:** When building a new report (Report Manager → Build new report), you can optionally set **Case group** (e.g. `Distsys-Maint-Unix`). This is the customer-created case group for the account, often visible in the Salesforce UI when inspecting that account. It is stored in the report under Customer Information as **Case group:** and is for reference; filtering of cases by SBR/product is still done via the account’s SBR groups in Report Manager.

---

## End-to-end data flow

| Step | Data source | What happens |
|------|-------------|----------------|
| New report (template) | None | Report is created with empty tables and placeholders. |
| First update (empty report) | **Hydra SOLR** (or rhcase CLI) | Account resolved → Hydra search (or `rhcase list`) → insert RFE/Bug rows (case #, summary, status; JIRA ID if in summary). |
| Check / later update | **JIRA** | Extract JIRA IDs from report → `GET /rest/api/2/issue/{key}` for each → compare or update Status/Notes column. |

So: **Hydra** (or rhcase CLI) pulls the list of cases; **JIRA** pulls current status for known issue keys. Both are required for a fully populated, up-to-date report.

---

## Code locations

- **JIRA:** `src/taminator/commands/check.py` — `JIRAClient`, `CustomerReportParser.extract_jira_issues()`; `update.py` uses the same client and parser.
- **Case discovery (Hydra):** `src/taminator/core/hydra_search.py` — `build_solr_query()`, `search_cases()`, `format_doc_for_report()`, `discover_cases()`, `discover_case_groups_for_account()`.
- **Population:** `src/taminator/commands/update.py` — `_try_populate_from_rhcase()` (tries Hydra first, then rhcase CLI fallback; account resolution and table injection).
- **Case discovery (standalone):** `src/active_case_report_system.py` — `ActiveCaseReportSystem.discover_cases()` runs `rhcase list`; optional alternative.
