# Code audit — what else could be fixed

Summary of findings from a pass over the latest code. Items are ordered by impact and ease of fix.

---

## 1. ESLint warnings (main.js) — fixed

All six warnings addressed: unused args prefixed with `_`, unused `cliPath` removed, unused `stdout` accumulation replaced with a no-op listener. Lint is clean.

---

## 2. Hardcoded path in rfe_verification_system.py — fixed

**File:** `taminator/src/rfe_verification_system.py` (lines 229, 237)

Two test cases previously used `/home/jbyrd/pai/src`. **Fixed:** They now use `PAI_SRC` env var; when unset, no path is appended and the test will fail unless the module is on the default path. Set `PAI_SRC` to your PAI src directory to run these tests.

---

## 3. Vault client SSL and default address — fixed

**File:** `taminator/src/taminator/core/vault_client.py`

- **Fixed:** SSL verification now respects `VAULT_CACERT` (path to CA bundle), `VAULT_SKIP_VERIFY=1` (disable verify for dev/self-signed), or defaults to `True` for production.
- **Fixed:** Default `addr` is now `""`; `VAULT_ADDR` is required. `is_available()` returns `False` when addr is empty. Document in VAULT_INTEGRATION.md that `VAULT_ADDR` is required.

---

## 4. auth_box.py TODO — fixed

**File:** `taminator/src/taminator/core/auth_box.py`

Removed the Kerberos "TODO: Parse expiration time"; added a short comment that we only check presence. Help/contact in token-missing error now points to GitLab issues.

---

## 5. Default contact / TAM name in web_server — fixed

**File:** `taminator/web_server.py`

`default_tam_name` and `default_contact` are now empty strings. Report and onboarding logic already fall back to "TAM" / "TBD" when blank.

---

## 6. Contact references in error messages and docs — fixed

**Files:** `auth_box.py`, `onboard.py`, `tam_call_notes_poster.py`, `weekly_discussion_poster.py`, `gui/index.html`, `check.py`, `update.py`

User-facing contact text now uses generic wording ("your TAM", "Red Hat TAM", "TAM") or the GitLab issues link. Onboarding default TAM name is "TAM". Settings and onboarding email inputs use a blank value with placeholder "your.email@redhat.com". Feedback link in Settings points to GitLab issues. Update logic uses a date-based pattern for the report header line instead of a hardcoded name.

---

## 7. Optional / later

- **Tests** — No unit or integration tests for token_store, hybrid_auth, or main.js paths. Adding minimal tests would catch regressions.
- **Duplicate/copy dirs** — **Fixed:** `taminator-copy-for-test/` and `gui/dist-arm64-build/` are in `.gitignore` (root and taminator/.gitignore).
- **Vault sync from Electron** — Documented in [VAULT_INTEGRATION.md](VAULT_INTEGRATION.md): when using the desktop app, set `VAULT_ADDR` (and `VAULT_TOKEN`) in the environment before launching (e.g. from a terminal or a wrapper) so token save can sync to Vault.

---

*Audit date: 2026. Re-run or extend as the codebase changes.*
