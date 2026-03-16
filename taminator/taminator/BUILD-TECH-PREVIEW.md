# Building tech preview (from redhat subdir)

Most users run **RHEL/Fedora or macOS**; on Linux, most are **x86_64**. The packaged app is the **same on all platforms**: one window that runs the browser-based UI (no separate browser tab).

Builds are produced from the **redhat/taminator** tree (sanitized, no .git/.cursor/.env).

## Run from source (no install)

From this directory (`redhat/taminator/taminator`):

```bash
./tam-rfe serve
```

Browser opens at http://127.0.0.1:8765. Or double-click **Taminator.command** in Finder (keep the Terminal window open).

## Build installers (same app on every platform)

**macOS (x64 + arm64)** — from this directory:

```bash
./build-tech-preview.sh
```

**Output:** `gui/dist/Taminator-2.0.0.dmg` (Intel), `gui/dist/Taminator-2.0.0-arm64.dmg` (Apple Silicon). Install by dragging to Applications; same app experience (one window, web UI).

**RHEL/Fedora (RPM, AppImage)** — same concept: one window, web UI. **Primary Linux target: x86_64** (most users).

- **x86_64 (RPM, AppImage, deb)** — build on a Linux x86_64 host or in CI:
  ```bash
  cd gui && npm ci && npm run build:linux
  ```
  Output: `gui/dist/*.x86_64.rpm`, `gui/dist/*.AppImage`, `gui/dist/*.deb`. This is the main Linux build for most users.

- **aarch64 RPM** (e.g. from a Mac via Podman): see [containers/README.md](containers/README.md).

## Version

Set `gui/package.json` `version` and/or `VERSION` in this directory before building if you want a different tech preview version (e.g. `2.0.0-tech-preview`).
