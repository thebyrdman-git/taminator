#!/usr/bin/env bash
# Build DMG (macOS) and RPM (Linux) for Taminator tech preview.
# Run from: redhat/taminator/taminator (this directory).
# DMG: run on macOS. RPM: run on Linux, or use Docker (see below).

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUI_DIR="$SCRIPT_DIR/gui"
DIST_DIR="$GUI_DIR/dist"

echo "Building Taminator tech preview from $SCRIPT_DIR"
echo ""

# Use VERSION file if present
if [ -f "$SCRIPT_DIR/VERSION" ]; then
  VERSION=$(cat "$SCRIPT_DIR/VERSION")
  echo "Version: $VERSION"
fi

cd "$GUI_DIR"
if [ ! -f package.json ]; then
  echo "Error: gui/package.json not found. Run from redhat/taminator/taminator."
  exit 1
fi

echo "Installing npm dependencies..."
npm ci 2>/dev/null || npm install

echo ""
echo "--- Building macOS DMG (x64 + arm64) ---"
npm run build:mac

if [ -d "$DIST_DIR" ]; then
  echo ""
  echo "macOS DMG artifacts:"
  ls -la "$DIST_DIR"/*.dmg 2>/dev/null || true
fi

echo ""
echo "--- RHEL/Fedora (same app: one window, web UI) ---"
echo "x86_64: on a Linux host: cd $GUI_DIR && npm ci && npm run build:linux"
echo "        Output: gui/dist/*.rpm, gui/dist/*.AppImage, gui/dist/*.deb"
echo "aarch64: use containers/README.md (Podman): build image, run build-rpm.sh"
echo ""
echo "Tech Preview artifacts: $DIST_DIR (DMG); gui/dist (RPM/AppImage when built on Linux)"
