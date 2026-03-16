# Rethinking Taminator – Development & Architecture

A concise snapshot of how the tool is built today and axes you can use to rethink it. No prescriptions—just structure for the conversation.

**Current product direction:** [PRODUCT_STRATEGY.md](PRODUCT_STRATEGY.md) — Nail RFE report generation first; let feedback drive what comes next. [FEEDBACK.md](FEEDBACK.md) tracks requests and decisions.

---

## What Exists Today

### Entry points (multiple)

| Entry | Role | Notes |
|-------|------|--------|
| `tam-rfe` | Main CLI script | Hand-parses argv, dispatches to `taminator.commands.*`. No argparse. |
| `src/taminator/cli.py` | Full CLI with argparse | Subparsers, help, examples. Not used by `tam-rfe` (different dispatch). |
| `tam-rfe-standalone.py` | Standalone script | ~527 lines; alternate path. |
| `bin/tam-rfe-*` | Many bash wrappers | e.g. `tam-rfe-chat` (1000+ lines), `tam-rfe-monitor-simple`, `tam-rfe-onboard-intelligent`, etc. |
| GUI (Electron) | `gui/` + releases | AppImage, DMG, exe; wraps the tool for desktop use. |

So there are several ways to “run Taminator,” and the “official” CLI is a small script that doesn’t use the richer `cli.py`.

### Two automation pipelines

1. **CLI pipeline (`tam-rfe`)**  
   - Commands: `check`, `update`, `post`, `onboard`, `config`, `report-issue`.  
   - Implemented under `src/taminator/commands/` (e.g. `check.py` has its own `JIRAClient`, parses markdown reports, compares to JIRA).  
   - Auth: `auth_box` + `hybrid_auth`; preflight runs even for `--test-data`, so JIRA token is required for check.

2. **“Ultimate” pipeline (bin scripts)**  
   - `bin/tam-rfe-monitor-simple` (and similar) call `src/ultimate_rfe_portal_system.py`.  
   - That composes: `ActiveCaseReportSystem`, `CustomerTemplateRenderer`, `RedHatCPPGAPIClient`, `RFEDiscussionAPIClient`.  
   - Different stack (e.g. case discovery, template rendering, portal/CPPG APIs).

So: one path is “taminator package + JIRA + auth_box”; the other is “ultimate system + active case report + CPPG/discussion APIs.” They can duplicate or overlap in purpose (e.g. “generate/update report” and “post to portal”) while differing in data sources and code paths.

### Source layout

- **Package:** `src/taminator/` — `commands/`, `core/` (auth_box, vault, auth types), `cli.py`, tests.
- **Top-level scripts in `src/`:** Many files with `def main()` and `if __name__ == '__main__'` that are both importable and runnable (e.g. `active_case_report_system.py`, `ultimate_rfe_portal_system.py`, `redhat_portal_api_client.py`, `weekly_discussion_poster.py`). So “library” and “script” are mixed.
- **Bin:** Bash scripts that set env, find `PROJECT_ROOT`, call Python or other tools; some are very long (chat, monitor).

### Auth and testability

- Auth is centralized and required: preflight runs before commands, and `check --test-data` still requires a JIRA token.
- There’s no explicit “offline” or “demo-only” mode that skips JIRA for local/test runs.

### Distribution and docs

- Releases: AppImage (x86_64 + arm64), DMG, Windows exe (Electron).
- Many markdown docs (GETTING-STARTED, PURPOSE, BUILDING, PREREQUISITES, FEATURE-*, DESIGN-*, etc.), which can make it hard to know the single source of truth.

---

## Axes You Can Use to Rethink

1. **One path vs two**  
   - Do you want a single “blessed” flow (e.g. only `tam-rfe` + taminator package) and migrate everything else into it, or keep “CLI” and “ultimate/monitor” as two supported paths and document when to use which?

2. **CLI surface**  
   - Single entry: one script (e.g. `tam-rfe`) that uses one parser (e.g. migrate to `cli.py`’s argparse) and one set of subcommands.  
   - Or keep `tam-rfe` as the main CLI but have it delegate to `cli.main()` so help and flags are consistent and extensible.

3. **Layering**  
   - Clear layers: CLI → application (orchestration) → services (JIRA, portal, case discovery, template rendering) → auth/config.  
   - That might mean: one “report generation” service used by both `update` and the “ultimate” flow, and one “post to portal” service used by `post` and by the monitor scripts.

4. **Auth and testability**  
   - Optional preflight for `--test-data` or `--offline`: skip JIRA (and maybe portal) when only testing report parsing, templates, or local output.  
   - Or a dedicated “demo” mode that never hits real APIs.

5. **Scripts vs library**  
   - Prefer “library first”: move logic from `src/*.py` main blocks into callable functions/classes under `taminator.*`, and keep `src/` scripts as thin wrappers or deprecate them in favor of `tam-rfe` subcommands.

6. **Bin scripts**  
   - Decide which bin scripts are essential (e.g. chat, monitor, onboard). Either fold their behavior into `tam-rfe` subcommands (e.g. `tam-rfe chat`, `tam-rfe monitor`) or document them as “advanced” and keep them as thin wrappers around the same Python APIs.

7. **Docs and onboarding**  
   - One “start here” doc (e.g. GETTING-STARTED) that points to PURPOSE, auth, and “first command”; treat the rest as deep-dives or legacy so the mental model is simple.

8. **Distribution**  
   - Whether Electron remains the primary distribution or you want “CLI-first” (pip/install script) with GUI optional; that affects how much you invest in packaging and which code path is “default.”

---

## Next Step

Pick one or two axes that matter most (e.g. “single pipeline” and “testability without JIRA”), and we can turn that into a concrete plan (refactors, deprecations, or new behaviors) without rewriting everything at once.
