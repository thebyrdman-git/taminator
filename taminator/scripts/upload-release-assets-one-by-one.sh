#!/usr/bin/env bash
# Upload v2.1.4 release assets to GitLab one at a time.
# Run this from a fresh clone of the GitLab repo (so history matches):
#
#   git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git taminator-gitlab
#   cd taminator-gitlab
#   git lfs install
#   git lfs track "releases/**/*.dmg" "releases/**/*.AppImage"
#   mkdir -p releases/v2.1.4
#   cp /path/to/artifacts/Taminator-2.1.4-* releases/v2.1.4/
#   bash /path/to/upload-release-assets-one-by-one.sh
#
# Or run from this repo and pass the path to the GitLab clone and artifacts:
#   ./scripts/upload-release-assets-one-by-one.sh /path/to/taminator-gitlab /path/to/artifacts

set -e
GITLAB_REPO="${1:-.}"
ARTIFACTS="${2:-/Users/jbyrd/redhat/taminator/artifacts}"
FILES=(
  "Taminator-2.1.4-arm64.dmg"
  "Taminator-2.1.4.dmg"
  "Taminator-2.1.4-arm64.AppImage"
  "Taminator-2.1.4.AppImage"
)

cd "$GITLAB_REPO"
# Ensure we're on main and LFS is set up
git fetch origin 2>/dev/null || true
git checkout main 2>/dev/null || true
git lfs install
if ! grep -q 'releases/\*\*' .gitattributes 2>/dev/null; then
  git lfs track "releases/**/*.dmg" "releases/**/*.AppImage"
  git add .gitattributes
  git commit -m "Track release assets with LFS" || true
  git push origin main 2>/dev/null || true
fi
mkdir -p releases/v2.1.4

for f in "${FILES[@]}"; do
  src="$ARTIFACTS/$f"
  dst="releases/v2.1.4/$f"
  if [ ! -f "$src" ]; then
    echo "Skip $f (not found at $src)"
    continue
  fi
  cp "$src" "$dst"
  git add "$dst"
  git commit -m "Add v2.1.4 release asset: $f"
  echo "Pushing $f..."
  git push origin main
  git lfs push origin main
  echo "Done: $f"
  echo ""
done

echo "All assets pushed. Add these links to the release page:"
echo "  https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.4/Taminator-2.1.4-arm64.dmg"
echo "  https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.4/Taminator-2.1.4.dmg"
echo "  https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.4/Taminator-2.1.4-arm64.AppImage"
echo "  https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.4/Taminator-2.1.4.AppImage"
