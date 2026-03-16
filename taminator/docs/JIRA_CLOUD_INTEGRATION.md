# JIRA Cloud integration plan

This document outlines how to add support for **JIRA Cloud** (Atlassian, e.g. `*.atlassian.net`) alongside the existing **Red Hat JIRA** (issues.redhat.com) integration.

---

## Current behavior

- **Base URL:** Hardcoded `https://issues.redhat.com/rest/api/2`.
- **Auth:** Bearer token (Red Hat Personal Access Token from issues.redhat.com).
- **Usage:** Check/update (fetch issue status), report generation (Hydra + JIRA keys), browse links in reports.
- **Config:** Token from Settings UI or `JIRA_TOKEN_API_TOKEN`; no configurable JIRA host.

---

## Goals

1. Support JIRA Cloud instances (e.g. customer or partner Atlassian) with minimal change to report flow.
2. Keep Red Hat JIRA as the default; make Cloud opt-in via configuration.
3. Use the same report pipeline (check, update, status comparison, browse links); only the JIRA backend (URL + auth) changes.

---

## Differences: Red Hat JIRA vs JIRA Cloud

| Aspect | Red Hat JIRA (current) | JIRA Cloud |
|--------|------------------------|------------|
| Base URL | `https://issues.redhat.com` | `https://<tenant>.atlassian.net` |
| REST API | `/rest/api/2` | `/rest/api/2` or `/rest/api/3` |
| Auth | Bearer token (PAT) | Email + API token (no password) |
| Browse URL | `https://issues.redhat.com/browse/{id}` | `https://<tenant>.atlassian.net/browse/{id}` |

JIRA Cloud [deprecated](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-basic-auth/) basic auth with password; API token is required.

---

## Implementation plan

### 1. Configurable JIRA base URL

- **Where:** User config (e.g. `~/.config/taminator/config.json` or existing accounts/structure config) or env var `JIRA_BASE_URL`.
- **Default:** `https://issues.redhat.com` (no change for existing users).
- **Values:** Any HTTPS base, e.g. `https://mycompany.atlassian.net`. No trailing slash.
- **Code:** 
  - `JIRAClient` (e.g. in `check.py`) takes `base_url` (and optional API path); default `base_url = "https://issues.redhat.com"` and path `/rest/api/2`.
  - All callers (check, update, web_server VPN check, etc.) resolve base URL from config/env and pass into client.

### 2. Browse URL generation

- **Current:** `JIRA_BROWSE_URL = "https://issues.redhat.com/browse/{id}"` in `update.py`; same pattern in `auth_types.py`, `tam_call_notes_poster.py`, etc.
- **Change:** Derive browse URL from configured base URL: `f"{base_url.rstrip('/')}/browse/{id}"`. Centralize in one helper (e.g. `jira_helpers.py` or on a small config object) so check/update/report rendering all use it.

### 3. Auth for JIRA Cloud

- **Red Hat:** Keep existing Bearer token (PAT). Header: `Authorization: Bearer <token>`.
- **JIRA Cloud:** Use [Atlassian API token](https://id.atlassian.com/manage-profile/security/api-tokens). Auth options:
  - **Option A (recommended):** HTTP Basic with email + API token. `Authorization: Basic base64(email:api_token)`. Supported by JIRA Cloud REST API.
  - **Option B:** OAuth 2.0 (more setup; optional later).
- **Config:** For “JIRA type” Cloud, store either:
  - `jira_email` + `jira_api_token`, or
  - a single “JIRA API token” and prompt for email when Cloud is selected (or store both in keyring/env).
- **UI/CLI:** In Settings (and CLI config), when user selects “JIRA Cloud” or base URL is `*.atlassian.net`, show fields for email + API token; otherwise keep single token field for Red Hat.

### 4. Detecting Cloud vs Red Hat

- **Heuristic:** If configured base URL contains `atlassian.net`, treat as JIRA Cloud (email + API token). Otherwise treat as Red Hat (Bearer token).
- **Explicit (optional):** Config key `jira_type: "redhat" | "cloud"` to override.

### 5. API compatibility

- Use same endpoints: `GET /rest/api/2/issue/{key}`, response `fields.status`, `fields.summary`, `fields.assignee`, `fields.updated`. JIRA Cloud’s REST API 2 is compatible for these.
- If a Cloud instance uses API 3 only for new features, add optional `JIRA_API_PATH=/rest/api/3` and handle any field renames in one place (adapter or small if/else on response).

### 6. Files to touch (summary)

| Area | Files | Change |
|------|--------|--------|
| Config | `~/.config/taminator` (or env) | Add `jira_base_url`, optional `jira_email`, `jira_api_token` for Cloud. |
| Check | `src/taminator/commands/check.py` | `JIRAClient(base_url, auth)` from config; build headers for Bearer vs Basic. |
| Update | `src/taminator/commands/update.py` | Use configurable browse URL; pass base_url/auth into any JIRA usage. |
| Auth | `src/taminator/core/hybrid_auth.py`, `auth_types.py` | Support “jira_cloud” or second token type; resolve token(s) for Cloud. |
| Web server | `web_server.py` | VPN check stays issues.redhat.com; token status/config UI: add JIRA URL and Cloud fields when applicable. |
| Report links | `update.py`, `tam_call_notes_poster.py`, etc. | Use centralized browse URL from config. |
| Hydra / prefixes | `hydra_search.py`, `jira_prefixes.txt` | No change for Cloud; project keys remain user-defined. |

### 7. Phasing

- **Phase A (configurable URL + links):** Add `JIRA_BASE_URL` (and optional config file). `JIRAClient` and browse URL use it. Auth unchanged (Bearer). Allows power users to point at a Cloud instance if they have a token that works (e.g. same PAT-style if their Cloud supports it; many don’t, so Phase B needed).
- **Phase B (JIRA Cloud auth):** Add email + API token storage and Basic auth path. When base URL is Cloud, use Basic auth. Same check/update and report flow.
- **Phase C:** Any Cloud-specific behavior (e.g. rate limits, different field IDs, API 3) as needed.

---

## Environment variables (proposed)

| Variable | Purpose |
|----------|---------|
| `JIRA_BASE_URL` | Override JIRA base (e.g. `https://mycompany.atlassian.net`). Default: Red Hat. |
| `JIRA_TOKEN_API_TOKEN` | Unchanged: Bearer token for Red Hat (or when Cloud uses Bearer). |
| `JIRA_EMAIL` | For Cloud: email for API token auth. |
| `JIRA_API_TOKEN` | For Cloud: Atlassian API token (when using Basic auth). |

(If both `JIRA_EMAIL` and `JIRA_API_TOKEN` are set and base URL is Cloud, use Basic auth; otherwise Bearer with `JIRA_TOKEN_API_TOKEN`.)

---

## In-app guidance (obtain token URL and steps)

When the configured JIRA base URL is Cloud (`*.atlassian.net`), the app shows **Cloud-specific** instructions for obtaining a token. When the base URL is Red Hat (default), it shows **Red Hat** instructions.

**Behavior**

- **Red Hat JIRA (default):** “How to obtain” URL is `https://issues.redhat.com/secure/ViewProfile.jspa`; steps describe Personal Access Tokens.
- **JIRA Cloud:** “How to obtain” URL is `https://id.atlassian.com/manage-profile/security/api-tokens`; steps describe creating an API token and using it with your Atlassian email in Settings.

**Where this appears**

- **Settings** — Token configuration and any guidance that references “how to get” the JIRA token.
- **CLI `tam-rfe config --add-token`** — When you choose JIRA, the panel shows the appropriate URL and steps for the currently configured base (Red Hat or Cloud).
- **Auth errors** — If the JIRA token is missing, the error message includes the matching “How to obtain” steps.
- **Auth audit** — The token name shown is “JIRA API Token (Cloud)” when Cloud is configured, otherwise “JIRA API Token”.

**Implementation**

- `auth_types.get_token_metadata(token_type)` returns metadata (name, obtain_url, obtain_steps) for each token type. For `JIRA_TOKEN` it calls `jira_config.is_jira_cloud()`; if true it returns Cloud-specific metadata (`_JIRA_CLOUD_METADATA`), otherwise `TOKEN_REGISTRY[AuthType.JIRA_TOKEN]`. All consumers that display “how to obtain” or the token name use `get_token_metadata()` so the guidance matches the configured instance.

---

## Testing

- **Red Hat:** Existing check/update and report flow; ensure default base URL and Bearer token still work.
- **Cloud:** Configure base URL to a test Atlassian site; set email + API token; run check/update and confirm status fetch and browse links work.
- **Mixed:** Not in initial scope (single JIRA per run).

---

## References

- [Atlassian REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Deprecation notice for basic auth with password](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-basic-auth/)
