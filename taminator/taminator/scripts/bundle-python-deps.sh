#!/bin/bash
# Build a relocatable Python venv with runtime deps for the packaged Taminator app.
# Run from taminator/ (parent of gui/, tam-rfe, src/). Output: taminator/python-bundle/

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUNDLE_DIR="$ROOT/python-bundle"
REQUIREMENTS="$ROOT/requirements-bundle.txt"

if [[ ! -f "$ROOT/requirements-bundle.txt" ]]; then
  echo "Missing $REQUIREMENTS. Run from taminator repo root." >&2
  exit 1
fi

# Remove existing bundle so we start clean
rm -rf "$BUNDLE_DIR"

# Prefer --copies so the venv is portable (no symlinks). Some Python builds (e.g. macOS framework)
# don't support it; then try virtualenv --always-copy, then fall back to venv without --copies.
echo "[bundle] Creating venv at $BUNDLE_DIR ..."
if python3 -m venv "$BUNDLE_DIR" --copies 2>/dev/null; then
  echo "[bundle] Created venv with --copies (portable)."
elif command -v virtualenv &>/dev/null && virtualenv --always-copy "$BUNDLE_DIR" 2>/dev/null; then
  echo "[bundle] Created venv with virtualenv --always-copy (portable)."
elif python3 -c "import virtualenv" 2>/dev/null; then
  python3 -m virtualenv --always-copy "$BUNDLE_DIR" && echo "[bundle] Created venv with virtualenv --always-copy (portable)."
else
  echo "[bundle] Trying venv without --copies (this Python may not support --copies)." >&2
  if ! python3 -m venv "$BUNDLE_DIR"; then
    echo "[bundle] Failed. Install Python that supports 'venv --copies' (e.g. Homebrew: brew install python) or install virtualenv (pip install virtualenv)." >&2
    exit 1
  fi
  echo "[bundle] WARNING: Venv uses symlinks. Bundled app may only run on machines with the same Python path." >&2
fi

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  PIP="$BUNDLE_DIR/Scripts/pip.exe"
  PYTHON="$BUNDLE_DIR/Scripts/python.exe"
else
  PIP="$BUNDLE_DIR/bin/pip"
  PYTHON="$BUNDLE_DIR/bin/python"
fi

echo "[bundle] Installing runtime deps from requirements-bundle.txt ..."
"$PIP" install --upgrade pip
"$PIP" install -r "$REQUIREMENTS"

echo "[bundle] Done. Use $PYTHON and add python-bundle to electron-builder extraResources."
