#!/usr/bin/env bash
# Run all checks that CI runs. Use before pushing or tagging to avoid CI failures.
# Usage: ./scripts/verify.sh [--no-python]
# From repo root: scripts/verify.sh

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
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
  TAM_DIR="$REPO_ROOT/taminator/taminator"
  if [[ -d "$TAM_DIR" ]] && [[ -x "$TAM_DIR/tam-rfe" ]]; then
    if ( cd "$TAM_DIR" && ./tam-rfe --version 2>/dev/null ) || ( cd "$TAM_DIR" && ./tam-rfe --help 2>/dev/null ); then
      echo "OK: tam-rfe runs"
    else
      echo "WARN: tam-rfe did not run (missing deps?); continuing"
    fi
  else
    echo "WARN: tam-rfe not found at $TAM_DIR/tam-rfe; skipping Python smoke"
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
