#!/usr/bin/env bash
# Copy taminator into the test user's home so you can run it from that account.
# Usage: ./copy-taminator-for-testuser.sh
#   Copies to /Users/testuser/taminator (username: testuser).
# To copy into testuser's home you need sudo: sudo ./scripts/copy-taminator-for-testuser.sh

set -e
TESTUSER="testuser"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="/Users/${TESTUSER}/taminator"

RSYNC_EXCLUDE=(
  --exclude 'taminator/gui/node_modules'
  --exclude 'taminator/gui/dist'
  --exclude 'taminator/gui/out'
  --exclude 'taminator/gui/build-info.json'
  --exclude '.git'
  --exclude 'releases'
)

if [[ "$(whoami)" == "root" ]]; then
  mkdir -p "$DEST"
  rsync -a "${RSYNC_EXCLUDE[@]}" "$REPO_ROOT/" "$DEST/"
  chown -R "${TESTUSER}:staff" "$DEST"
  echo "Copied taminator to $DEST (owned by testuser)."
else
  DEST_REAL="${REPO_ROOT}/taminator-copy-for-testuser"
  mkdir -p "$DEST_REAL"
  rsync -a "${RSYNC_EXCLUDE[@]}" "$REPO_ROOT/" "$DEST_REAL/"
  echo "Copied to $DEST_REAL"
  echo "To put it in testuser's home, run:"
  echo "  sudo cp -r $DEST_REAL /Users/testuser/taminator && sudo chown -R testuser:staff /Users/testuser/taminator"
fi

echo ""
echo "As user 'testuser', run the GUI from source:"
echo "  cd ${DEST}/taminator/gui && npm install && npm run start"
echo "Or run the web UI:"
echo "  cd ${DEST}/taminator/taminator && ./tam-rfe serve"
echo ""
