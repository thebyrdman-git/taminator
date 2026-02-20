# Taminator — RFE and Bug Report Generator

A tool for generating and maintaining RFE and bug reports for TAMs. Uses JIRA and case data; supports desktop app and CLI.

---

## Summary

**What:** A tool for generating and maintaining RFE and bug reports for TAMs  
**Why:** Saves 2–3 hours per customer per week  
**How:** Desktop app (recommended for UI) or CLI — report generation, JIRA/case data, optional portal posting

---

## Where to get Taminator

**Official (Red Hat coworkers only):** https://gitlab.cee.redhat.com/jbyrd/taminator

Requires Red Hat VPN and GitLab CEE access.

- **Desktop app (recommended):** Download AppImage (Linux) or DMG (macOS) from the [GitLab releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases) page. Double-click to open Taminator in its own app window. No terminal required.
- **From repo:** `git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git ~/taminator` (for CLI or development).

---

## Prerequisites

- **Red Hat VPN** — Required for JIRA and internal APIs.
- **JIRA API token** — From issues.redhat.com → Personal Access Tokens. Configure in the app under Settings.
- **Customer Portal token** (optional, for posting) — From access.redhat.com/management/api → Generate Token.
- **Python 3.7+** — Only if running from repo (CLI/development). Not required for the desktop app.

---

## Installation

### Desktop app (no terminal required)

Double-click the Taminator app; it opens in its own window. No terminal commands needed.

- **Linux:** Download the AppImage from [GitLab releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases), then double-click. Choose x86_64 or ARM64 to match your system (`uname -m`).
- **macOS:** Download the DMG from GitLab releases, drag Taminator to Applications, then double-click. First time: right-click → Open to bypass Gatekeeper if prompted.

### From repo (optional)

For CLI or to run the UI from source: `cd ~/taminator/taminator && ./tam-rfe serve`. Desktop app is easier for UI users.

### Windows

Desktop builds are for Linux and macOS only. On Windows, run from the repo (e.g. WSL or Python): `./tam-rfe serve`.

---

## Documentation

- **[Full user guide](USER-GUIDE.md)** — Canonical guide (in app and on GitLab)
- **[Getting started](taminator/GETTING-STARTED.md)** — Quick setup
- **Releases:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- **Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues

---

*Taminator — RFE and Bug Report Generator for Red Hat TAMs.*
