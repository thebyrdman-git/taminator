#!/usr/bin/env bash
# Verify GitLab release asset URLs (run on VPN).
# Usage: ./scripts/verify-gitlab-release-links.sh

set -e
BASE="https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main"

# If the GitLab repo root is the full repo (taminator/ at root):
PREFIX_FULL="taminator/releases/v2.1.4"
# If the GitLab repo root is only the taminator tree:
PREFIX_TAM="releases/v2.1.4"

FILES=(
  "Taminator-2.1.4-arm64.dmg"
  "Taminator-2.1.4.dmg"
  "Taminator-2.1.4-arm64.AppImage"
  "Taminator-2.1.4.AppImage"
)

echo "Testing URLs with path: $PREFIX_FULL (repo root = full redhat tree)"
echo "---"
for f in "${FILES[@]}"; do
  url="${BASE}/${PREFIX_FULL}/${f}"
  code=$(curl -s -o /dev/null -w "%{http_code}" -L "$url" 2>/dev/null || echo "000")
  if [ "$code" = "200" ]; then
    echo "  OK  $f (HTTP $code)"
  else
    echo "  FAIL $f (HTTP $code) - $url"
  fi
done

echo ""
echo "Testing URLs with path: $PREFIX_TAM (repo root = taminator tree only)"
echo "---"
for f in "${FILES[@]}"; do
  url="${BASE}/${PREFIX_TAM}/${f}"
  code=$(curl -s -o /dev/null -w "%{http_code}" -L "$url" 2>/dev/null || echo "000")
  if [ "$code" = "200" ]; then
    echo "  OK  $f (HTTP $code)"
  else
    echo "  FAIL $f (HTTP $code) - $url"
  fi
done
