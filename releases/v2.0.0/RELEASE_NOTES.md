# Taminator v2.0.0 — Tech preview

**Release date:** TBD  
**Repo:** https://gitlab.cee.redhat.com/jbyrd/taminator (official; GitLab only)  
**Project title on GitLab:** TAMINATOR - RFE and Bug Report Generator

This is a **tech preview**. We welcome feedback via [GitLab issues](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues); it drives what we do next.

---

## What's in this release

v2.0.0 aligns the project with the updated product direction and adds a **browser-based UI** alongside the CLI.

### What's in v2.0
- **Desktop app (recommended):** One-window app — AppImage on Linux (x86_64 + ARM64). Double-click to open; no terminal required. Windows and macOS builds not in this release.
- **Browser-based UI from repo:** Run `tam-rfe serve` to start a local web app; use the same report actions (check, update) in your browser.
- **CLI:** `tam-rfe check`, `tam-rfe update`, `tam-rfe post`, `tam-rfe config`, `tam-rfe onboard`, `tam-rfe report-issue`. Full feature parity with the UI.
- **Direction:** Phase 1 focus (generate and maintain RFE/bug reports), GitLab only, feedback-driven.
- **Auth:** Auth-Box, VPN check, JIRA token, and portal token behavior unchanged.

### No breaking changes
- Same CLI commands and behavior. Same config and token flow. Existing workflows continue to work.

---

## How to run the browser UI

Install the repo to `~/taminator` (Mac: `/Users/<you>/taminator`, Linux: `/home/<you>/taminator`). Then from the app directory:

```bash
cd ~/taminator/taminator
./tam-rfe serve
```

A browser opens at http://127.0.0.1:8765. Enter a customer name (or check “Use test data”) and use **Check report** or **Update report**. Use `./tam-rfe serve --no-browser` to start the server without opening a browser, or `--port 9000` to use a different port.

---

## How to get v2.0.0

- **Clone:** `git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git`
- **Releases / downloads:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases (AppImage links on the v2.0.0 release)
- **Issues / feedback:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues

Requires Red Hat VPN and GitLab CEE access.
