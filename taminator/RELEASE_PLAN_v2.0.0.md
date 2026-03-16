# Release plan: Taminator v2.0.0

**Theme:** Strategy release — Phase 1 focus, GitLab only, CLI-first, browser-based direction.

**Target:** Align the project with [PRODUCT_STRATEGY.md](PRODUCT_STRATEGY.md): nail RFE report generation; single official repo (GitLab); terminal feature parity when GUI exists; future GUI will be browser-based.

---

## Scope for v2.0.0

### In scope
- [x] Document and communicate new product direction (already in PRODUCT_STRATEGY, SHARING, FEEDBACK).
- [x] Version bump to 2.0.0 and release notes.
- [x] README and version history updated to v2.0.0; GitLab as only official source.
- [x] GUI package.json: version 2.0.0, repository/homepage point to GitLab.
- [x] Create `releases/v2.0.0/` with release notes; existing AppImage can be copied or re-tagged when you build.
- [x] **Browser-based UI** for v2.0: local web app (run `tam-rfe serve`), feature parity with CLI for check/update.
- [ ] Optional: Add a single source of truth for version (e.g. `VERSION` file or `taminator/__init__.py` version) for CLI.

### Out of scope for this release
- No removal of Electron (still available); browser UI is the primary web interface for v2.0.
- No change to report generation logic beyond what already exists.

---

## Checklist

- [x] RELEASE_PLAN_v2.0.0.md (this file) and RELEASE_NOTES updated.
- [x] Version 2.0.0 in `taminator/gui/package.json`.
- [x] README: Download section and Version History show v2.0.0 as current.
- [x] README: Project Status shows version 2.0.0 and one-line theme.
- [x] `releases/v2.0.0/RELEASE_NOTES.md` created.
- [x] GUI package.json `homepage` and `repository.url` point to GitLab.
- [ ] Tag and/or create GitLab release for v2.0.0 when ready (manual step).
- [ ] If building new artifacts: build AppImage/DMG/exe and place in `releases/v2.0.0/` (manual step).

---

## After release

- Collect feedback on report generation (Phase 1). Use [FEEDBACK.md](FEEDBACK.md) and GitLab issues.
- Plan browser-based UI and terminal parity when feedback justifies it.
