# Taminator build pipeline (Ansible)

This directory defines a **consistent, Ansible-driven build pipeline** for the Taminator Electron app. It keeps paths, versions, and steps in one place and aligns with GitHub Actions. It also keeps **content up-to-date and consistent** (version, USER-GUIDE, icon) so builds and docs stay in sync.

## Layout

- **`vars/build-pipeline.yml`** — Build: `gui_path`, `node_version`, build targets, artifact patterns.
- **`vars/content-consistency.yml`** — Content: `app_version` (single source of truth), paths for VERSION, package.json, USER-GUIDE, icon.
- **`roles/taminator_build/`** — Build role: ensure icon, `npm ci`, `electron-builder`.
- **`roles/taminator_content_sync/`** — Sync role: write `app_version` to VERSION and package.json; copy USER-GUIDE and icon from canonical locations.
- **`roles/taminator_verify_consistency/`** — Verify role: assert VERSION and package.json version match (for CI or pre-release).
- **`playbooks/build-mac.yml`** — Build macOS DMGs; optionally runs content sync first (`sync_content_before_build: true`).
- **`playbooks/build-linux.yml`** — Build Linux AppImage (CI or local testing).
- **`playbooks/ensure-content-consistent.yml`** — Sync and verify content (run before releases or in CI).
- **`inventory-build.yml`** — Localhost-only inventory.

## Quick start (Mac build)

From the **repo root** (parent of the outer `taminator/`):

```bash
ansible-playbook -i taminator/taminator/ansible/inventory-build.yml \
  taminator/taminator/ansible/playbooks/build-mac.yml
```

From **`taminator/taminator/ansible/`**:

```bash
ansible-playbook -i inventory-build.yml playbooks/build-mac.yml
```

Prerequisites: Node.js 20 (or the version in `vars/build-pipeline.yml`), `npm`, and the build icon at `taminator/gui/build/icon.png`.

## Alignment with GitHub Actions

- **`.github/workflows/electron-build.yml`** runs the same logical steps: ensure icon, `npm ci`, `electron-builder --mac` (or `--linux` / `--win`). Variables in `vars/build-pipeline.yml` (e.g. `node_version`, `gui_path`, artifact patterns) are the reference; the workflow can be updated to match or to call these playbooks in CI later.
- **Linux release builds** remain in GitHub Actions only (see `.cursor/rules/linux-builds-github-actions.mdc`). The Ansible `build-linux.yml` playbook is for CI or local testing, not for producing release Linux artifacts by hand.

## Keeping content up-to-date and consistent

- **Single version:** Set `app_version` in `vars/content-consistency.yml`. Run the content playbook to write it to the VERSION file and `gui/package.json`, and to copy USER-GUIDE and icon so the app and docs stay in sync.
- **Sync and verify (before release or in CI):**
  ```bash
  ansible-playbook -i inventory-build.yml playbooks/ensure-content-consistent.yml
  ```
- **Verify only (no changes, e.g. in CI):**
  ```bash
  ansible-playbook -i inventory-build.yml playbooks/ensure-content-consistent.yml --tags verify
  ```
- **Build with sync:** `build-mac.yml` runs content sync by default. To build without syncing: `-e sync_content_before_build=false`.

## Customizing

- **App version:** Set `app_version` in `vars/content-consistency.yml`; then run `ensure-content-consistent.yml` or run a build (which syncs first).
- **Node version:** Set `node_version` in `vars/build-pipeline.yml` or override with `-e node_version=20`.
- **Retries:** Role default `npm_ci_retries: 3`; override with `-e npm_ci_retries=5` if needed.
- **Platform:** Use `build-mac.yml` or `build-linux.yml`, or pass `-e build_platform=mac` when calling the role.
