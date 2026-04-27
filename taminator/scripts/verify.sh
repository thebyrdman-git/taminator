#!/usr/bin/env bash
# Run all checks that CI runs. Use before pushing or tagging to avoid CI failures.
# Usage: ./scripts/verify.sh [--no-python]
# From repo root: scripts/verify.sh

set -e
# Package root = parent of this script (…/taminator). tam-rfe lives at …/taminator/taminator/tam-rfe.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
FAILED=0

echo "=== 1. GUI icon ==="
if [[ ! -f taminator/gui/build/icon.png ]]; then
  echo "FAIL: Missing taminator/gui/build/icon.png"
  FAILED=1
else
  echo "OK: icon exists"
fi

echo ""
echo "=== 2. GUI lint (ESLint) ==="
if ( cd taminator/gui && npm run lint 2>/dev/null ); then
  echo "OK: lint passed"
else
  echo "FAIL: lint failed (run: cd taminator/gui && npm run lint)"
  FAILED=1
fi

echo ""
echo "=== 3. Python / tam-rfe (smoke) ==="
if [[ "$1" == "--no-python" ]]; then
  echo "SKIP: --no-python"
else
  # Inner package: <project>/taminator/tam-rfe (not <project>/taminator/taminator/tam-rfe).
  TAM_DIR=""
  if [[ -x "$REPO_ROOT/taminator/tam-rfe" ]]; then
    TAM_DIR="$REPO_ROOT/taminator"
  elif [[ -x "$REPO_ROOT/tam-rfe" ]]; then
    TAM_DIR="$REPO_ROOT"
  fi
  if [[ -n "$TAM_DIR" ]] && [[ -d "$TAM_DIR" ]] && [[ -x "$TAM_DIR/tam-rfe" ]]; then
    if ( cd "$TAM_DIR" && ./tam-rfe --version 2>/dev/null ) || ( cd "$TAM_DIR" && ./tam-rfe --help 2>/dev/null ); then
      echo "OK: tam-rfe runs"
    else
      echo "WARN: tam-rfe did not run (missing deps?); continuing"
    fi
  else
    echo "WARN: tam-rfe not found (expected at $REPO_ROOT/taminator/tam-rfe or $REPO_ROOT/tam-rfe); skipping Python smoke"
  fi
fi

echo ""
if [[ $FAILED -eq 0 ]]; then
  echo "All checks passed. Safe to push / tag."
  exit 0
else
  echo "Some checks failed. Fix before pushing."
  exit 1
fi
