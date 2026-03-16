# Feature verification against open-source and official practices

This document verifies Taminator features against known working examples from the open-source community and official vendor documentation.

---

## 1. JIRA integration

### 1.1 JIRA Cloud Basic auth (email + API token)

**Our implementation** (`taminator/src/taminator/core/jira_config.py`):

- For base URL `*.atlassian.net`: build `Authorization: Basic base64(email:api_token)`.
- Credentials from env (`JIRA_EMAIL`, `JIRA_API_TOKEN`) or token store (`jira_email`, `jira_api_token`).

**Official reference:**

- [Atlassian: Basic auth for REST APIs](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/):
  - "Basic auth requires API tokens. You generate an API token for your Atlassian account and use it to authenticate anywhere where you would have used a password."
  - Example: `curl -u fred@example.com:freds_api_token` or construct header: BASE64 encode `user@example.com:api_token_string`, then `Authorization: Basic <encoded>`.

**Verification:** Implementation matches Atlassian docs: email + API token, Base64-encoded string, `Basic ` prefix. No password auth (deprecated for Cloud).

### 1.2 Red Hat JIRA Bearer token

**Our implementation:** `Authorization: Bearer <token>` when base URL is not Cloud; token from `JIRA_TOKEN_API_TOKEN` or `jira_token` in config.

**Community / vendor:**

- Atlassian and Red Hat JIRA support Bearer (Personal Access Token) for server/Data Center.
- Common pattern: `headers = {'Authorization': f'Bearer {token}'}` (e.g. [Atlassian Support – Jira Align Bearer token](https://support.atlassian.com/jira-align/kb/how-to-pass-a-bearer-token-when-making-a-jira-align-rest-api-call-via-python/)).

**Verification:** Matches standard Bearer usage.

### 1.3 JIRA REST API: get issue

**Our implementation** (`check.py` – `JIRAClient`):

- `GET {base_url}/issue/{issue_key}` with `Content-Type: application/json`, `timeout=10`.
- Response: `data['fields']['status']['name']`, `data['fields']['summary']`, `data['fields']['assignee']`, `data['fields']['updated']`.

**Official reference:**

- JIRA REST API v2: [Get issue](https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/#api-rest-api-2-issue-issueidorkey-get) – `GET /rest/api/2/issue/{issueIdOrKey}`.
- Response includes `fields.status`, `fields.summary`, `fields.assignee`, `fields.updated`.

**Community example** (typical Python usage):

```python
url = "https://your-domain.atlassian.net/rest/api/2/issue/ISSUE-123"
headers = {"Accept": "application/json"}
auth = ("email@example.com", "API_TOKEN")
response = requests.get(url, headers=headers, auth=auth)
issue_data = response.json()
# issue_data['fields']['summary'], etc.
```

**Verification:** We use the same path (`/rest/api/2` + `/issue/{key}`), same fields. We send auth via header (Basic or Bearer) instead of `auth=` tuple; both are valid. Timeout (10s) is set.

### 1.4 JIRA “myself” (config test)

**Our implementation** (`config.py` – `_test_jira_connection()`):

- `GET {api_url}/myself` with auth header from `jira_config.get_jira_auth()`.

**Verification:** Standard endpoint for “current user”; used in community examples and Atlassian docs for testing auth.

### 1.5 Browse URL

**Our implementation:** `get_jira_browse_url(issue_id)` → `{base_url}/browse/{issue_id}`.

**Verification:** Matches JIRA UI convention for both Red Hat and Cloud (`/browse/{key}`).

---

## 2. Token and secret storage

### 2.1 Keyring (OS credential store)

**Our implementation** (`auth_box.py`):

- Optional `keyring`: `keyring.set_password(KEYRING_SERVICE, token_type.value, token)` and `keyring.get_password(...)`.
- Fallback order: keyring → env → config file.

**Community best practice:**

- [Use keyring to store your credentials](https://alexwlchan.net/2016/you-should-use-keyring/) and [Securely Storing Credentials in Python with Keyring](https://www.allscient.com/post/securely-storing-credentials-in-python-with-keyring): keyring is the recommended approach; it uses OS stores (macOS Keychain, Windows Credential Locker, Linux Secret Service).
- Stack Overflow / Python best practices: avoid plaintext files and code; prefer keyring or env; keyring gives encryption at rest.

**Verification:** We use keyring when available and degrade to env then file, which aligns with “keyring first, then env” practices.

### 2.2 File-based token store (UI tokens)

**Our implementation** (`token_store.py`):

- Path: `~/.config/taminator/ui_tokens.json`.
- Format: JSON with `v: 1` and base64-encoded `payload` (decoded payload is JSON with token keys).
- File mode: `0o600` on save.

**Community context:**

- Best practice is keyring > env > file; files should not be plaintext.
- Base64 is encoding, not encryption; it avoids casual viewing and accidental commits of plain JSON. Many tools use similar “obfuscated” storage for non-keyring fallback.
- Restricting to user-only (`0o600`) is standard.

**Verification:** Approach is consistent with “secure file fallback”: encoded payload + strict file permissions. For higher assurance, consider encrypting the payload (e.g. with a key derived from keyring or user secret).

### 2.3 Never log or expose token values

**Our implementation:** `web_server.py` comment for `api/config/set-token`: “Never log or expose token values (enterprise UX standard: security).” Responses return only success/error messages, not tokens.

**Verification:** Aligns with common security guidance (no tokens in logs or API responses).

---

## 3. HTTP and API usage

### 3.1 Timeouts on outbound requests

**Our implementation:**

- JIRA: `timeout=10` in `check.py` and `config.py`.
- VPN check: `timeout=8` in `web_server.py`.
- Hydra: `timeout=15` in `web_server.py`.
- Subprocess (tam-rfe): `timeout=120` for check/update; `timeout=90` for rhcase in `update.py`.
- Auth checks (auth_box, auth_audit): 2–5s timeouts.

**Verification:** All observed `requests` and subprocess calls use timeouts, reducing hang risk and matching common “always set a timeout” guidance.

### 3.2 Path safety (report files, library delete)

**Our implementation:** `web_server.py`:

- Report paths resolved with `Path(path_str).expanduser().resolve()`.
- Allowed bases: `REPORT_SEARCH_PATHS` (e.g. `~/taminator-test-data`, `~/Documents/rh/customers`, `/tmp/taminator-test-data`).
- Delete: `report_path` must be under one of the resolved bases (`report_path.parent == base or base in report_path.parents`).
- Build report: `report_dir` must be in `allowed_resolved` set.

**Verification:** Path traversal is constrained to allowed directories; consistent with “resolve and check containment” patterns.

---

## 4. Web server and API design

### 4.1 JSON API and error handling

**Our implementation:** JSON responses with `ok`, `error`, or `message`; 400/404/500 where appropriate; no token or secret in responses.

**Verification:** Matches common REST/JSON API style and safe error messaging.

### 4.2 Token type allowlist

**Our implementation:** `api/config/set-token`: `allowed = ("jira", "portal", "jira_token", "portal_token")`; reject other types.

**Verification:** Reduces risk of writing arbitrary keys into the token store.

### 4.3 JIRA settings API

**Our implementation:** `api/config/set-jira-settings` accepts only `jira_base_url`, `jira_email`, `jira_api_token`, `jira_token` and merges into existing token dict.

**Verification:** Limited key set and merge-only updates are in line with “minimal privilege” config APIs.

---

## 5. Summary table

| Feature | Our implementation | Reference / practice | Status |
|--------|---------------------|----------------------|--------|
| JIRA Cloud Basic auth | Email + API token, Base64, `Basic ` header | Atlassian Basic auth docs | Matches |
| JIRA Red Hat auth | Bearer token | Common PAT/Bearer usage | Matches |
| JIRA GET issue | `/rest/api/2/issue/{key}`, fields status/summary/assignee/updated | JIRA REST v2, community examples | Matches |
| JIRA browse URL | `{base}/browse/{id}` | JIRA UI convention | Matches |
| Token storage | Keyring → env → file | Keyring best practice (e.g. keyring lib, blog posts) | Aligned |
| File token store | Base64 payload, 0o600 | “No plaintext” fallback + permissions | Aligned |
| No token in logs/responses | Comment + behavior in set-token and APIs | Common security practice | Aligned |
| HTTP timeouts | All requests and subprocesses use timeouts | “Always use timeout” guidance | Aligned |
| Path safety | Resolve + allowlist for report paths | Path traversal prevention | Aligned |
| Config allowlist | Token type and JIRA keys restricted | Least privilege config | Aligned |

---

## 6. References

- [Atlassian – Basic auth for REST APIs](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/)
- [Atlassian – JIRA REST API v2 (Issues)](https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Use keyring to store your credentials](https://alexwlchan.net/2016/you-should-use-keyring/)
- [Python best practices – where to store API keys/tokens](https://stackoverflow.com/questions/56995350/best-practices-python-where-to-store-api-keys-tokens)
- Internal: `docs/JIRA_CLOUD_INTEGRATION.md`
