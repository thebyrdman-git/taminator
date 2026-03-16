# CI workflows for Taminator (GitHub)

Two GitHub repos use workflows from this tree:

---

## thebyrdman-git/taminator (main repo)

**Workflow:** `.github/workflows/electron-build.yml` (at repo root, i.e. one level up from this `ci-workflows/` directory).

- **Repo:** [https://github.com/thebyrdman-git/taminator](https://github.com/thebyrdman-git/taminator)
- **Layout:** Repo root must contain `taminator/` and `scripts/`. Paths in the workflow: `taminator/gui/`, `taminator/gui/build/icon.png`, etc.
- **Trigger:** Push a version tag (e.g. `v2.0.1`) or **Actions → Electron Build & Release → Run workflow**.
- **On tag:** Creates a GitHub Release and attaches Linux (x64 + ARM64), macOS, and Windows artifacts. Releases: https://github.com/thebyrdman-git/taminator/releases

---

## thebyrdman-git/taminator-ci (build-only, for testers)

Workflow files in **ci-workflows/** (and a copy under **taminator/.github/workflows/**) are for [thebyrdman-git/taminator-ci](https://github.com/thebyrdman-git/taminator-ci). That repo produces Mac and Linux builds for sharing with testers (artifacts only, no release).

### Setup (thebyrdman-git/taminator-ci)

1. **Repo layout**  
   The taminator-ci repo root must have: `gui/`, `web/`, `tam-rfe`, `web_server.py`, `src/`. Optionally: `scripts/`, `requirements-bundle.txt`, `USER-GUIDE.md`. (Same layout as the `taminator/` directory in this repo—e.g. sync or copy the contents of `taminator/` into the root of taminator-ci.)

2. **Add the workflow**  
   The workflow lives at `taminator/.github/workflows/build-taminator-app.yml`. When you sync the **contents** of the `taminator/` directory to the root of taminator-ci, you get `.github/workflows/build-taminator-app.yml` in the right place. Or copy `ci-workflows/build-taminator-app.yml` into the taminator-ci repo as `.github/workflows/build-taminator-app.yml`.

3. **Push or run manually**  
   - Push to `main` (or `master`) to trigger a build, or  
   - In GitHub: **Actions** → **Build Taminator (Linux + macOS)** → **Run workflow**.

4. **Download artifacts**  
   When the run finishes, open the run and download:
   - **taminator-linux-x64** — AppImage (and deb/rpm if produced) for Linux testers.
   - **taminator-macos** — DMG(s) for Mac testers (Intel and Apple Silicon).

Share the appropriate artifact with each OS group; they can download from the Actions run or you can attach the files in your preferred channel.

---

## What gets built

| Job            | Runner        | Artifacts                          |
|----------------|---------------|------------------------------------|
| Linux (AppImage)| `ubuntu-latest` | AppImage, .deb, .rpm (in one artifact) |
| macOS (DMG)    | `macos-latest`  | .dmg (x64 + arm64 when supported)  |

Artifacts are kept for 30 days. For longer-term sharing, copy the built files to releases or another store.

---

## Optional: Python bundle

If the repo has `scripts/bundle-python-deps.sh` and `requirements-bundle.txt` at root, the workflow runs the script to create a portable Python env used by the packaged app. If not, it creates an empty `python-bundle/` so the build succeeds; the app will then use system Python when available.
