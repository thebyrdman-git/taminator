#!/usr/bin/env bash
# Sign the unpacked Taminator.app and repack a new DMG.
# The mounted DMG is read-only, so we sign the app in dist/ then create a new DMG.
#
# Prereqs:
#   - Apple Developer ID Application certificate in Keychain
#   - Already ran: npm run build:mac (so dist/mac and dist/mac-arm64 exist)
#
# Usage:
#   export CSC_NAME="Developer ID Application: Your Name (TEAMID)"
#   ./sign-and-repack-dmg.sh
#   # Or inline:
#   CSC_NAME="Developer ID Application: Your Name (TEAMID)" ./sign-and-repack-dmg.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -z "$CSC_NAME" ]; then
  echo "Set CSC_NAME to your Developer ID Application identity."
  echo "Example: export CSC_NAME=\"Developer ID Application: Your Name (TEAMID)\""
  echo "List identities: security find-identity -v -p codesigning"
  exit 1
fi

VERSION="${npm_package_version:-2.1.4}"

for ARCH in mac mac-arm64; do
  APP="dist/${ARCH}/Taminator.app"
  if [ ! -d "$APP" ]; then
    echo "Skipping $ARCH (not found: $APP). Run npm run build:mac first."
    continue
  fi
  echo "Signing $APP ..."
  codesign --force --deep --sign "$CSC_NAME" "$APP"
  DMG_NAME="Taminator-${VERSION}-$(echo $ARCH | sed 's/mac-arm64/arm64/;s/mac/x64/')-signed.dmg"
  echo "Creating $DMG_NAME ..."
  hdiutil create -volname Taminator -srcfolder "dist/${ARCH}" -ov -format UDZO "$DMG_NAME"
  echo "Created $DMG_NAME"
done

echo "Done. Signed DMGs are in $SCRIPT_DIR"
