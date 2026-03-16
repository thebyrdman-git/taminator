# Continue: Upload v2.1.4 assets to GitLab (one at a time)

After the GitLab clone finishes (or if you clone manually):

## 1. Ensure clone is ready

```bash
cd /Users/jbyrd/redhat/taminator-gitlab
git fetch origin
git checkout main
ls releases/
```

## 2. Run the one-by-one upload script

From the **redhat** repo (script uses the clone path and artifacts path):

```bash
/Users/jbyrd/redhat/taminator/scripts/upload-release-assets-one-by-one.sh \
  /Users/jbyrd/redhat/taminator-gitlab \
  /Users/jbyrd/redhat/taminator/artifacts
```

This will, for each of the 4 files: copy → `git add` → `git commit` → `git push origin main` → `git lfs push origin main`.

## 3. Add asset links on the release page

On https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.1.4 add these as **asset links** (Link URL):

- `https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.4/Taminator-2.1.4-arm64.dmg`
- `https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.4/Taminator-2.1.4.dmg`
- `https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.4/Taminator-2.1.4-arm64.AppImage`
- `https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.4/Taminator-2.1.4.AppImage`

## 4. Verify links (on VPN)

```bash
/Users/jbyrd/redhat/taminator/scripts/verify-gitlab-release-links.sh
```

If the GitLab repo root is the full tree (has `taminator/` at top level), use the URLs with `taminator/releases/...` instead of `releases/...`.
