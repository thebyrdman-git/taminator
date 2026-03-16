# Tech Preview release checklist

Use this before announcing or demoing the 2.0.0-tech-preview.

## Docs and messaging

- [x] **USER-GUIDE.md** — Desktop app is primary; double-click opens in its own app window; no terminal required for UI users.
- [x] **TECH-PREVIEW-TESTING.md** — Mentions desktop app first, then repo/CLI.
- [x] **CHANGELOG-TECH-PREVIEW.md** — "How to run" lists desktop app first.
- [ ] **README** (repo root or taminator/) — If it still says "run from repo" as the main path, add a line that the desktop app (releases) is for UI users and requires no terminal.

## Builds and releases

- [ ] **Desktop builds** — AppImage (Linux), DMG (macOS) built and uploaded to GitLab releases (or release tag/instructions point to them). Windows is not offered.
- [ ] **Version** — `taminator/VERSION` or equivalent shows `2.0.0-tech-preview` (already set).
- [ ] **Release notes** — GitLab release description or CHANGELOG linked; one-line summary for demos.

## Pre-demo smoke test

- [ ] **Desktop app** — Double-click launches; Taminator opens in its own window. Report Manager is the landing page.
- [ ] **Check/Update** — Use test data or one real customer; Check and Update run without crash.
- [ ] **User Guide** — In-app User Guide loads and renders (markdown); no blank or broken panel.
- [ ] **Settings** — Token status and VPN check work; no console errors.

## Announcement

- [ ] **Audience** — Decide where to post (Slack, email, GitLab, etc.).
- [ ] **Message** — "Tech Preview ready: desktop app, double-click to open in browser, no terminal needed. Please try and send feedback (GitLab issues or Slack)."
- [ ] **Link** — GitLab releases URL and/or USER-GUIDE link.

---

**Sign-off:** _____________________ **Date:** _____________________
