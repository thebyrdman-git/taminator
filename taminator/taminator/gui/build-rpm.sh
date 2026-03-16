#!/usr/bin/env bash
# Build Taminator Linux RPM. Run inside the taminator-rpm-builder container
# with the repo mounted at /app (so this script is at /app/gui/build-rpm.sh).
# Uses system fpm (gem install fpm) when available so native arch works.

set -e
echo "Building Taminator Linux RPM..."
npm ci --prefer-offline --no-audit 2>/dev/null || npm install
# Use system fpm (gem install fpm) to avoid downloaded x86 binary on arm64
export USE_SYSTEM_FPM=true
export USE_HARD_LINKS=false
npx electron-builder --linux rpm
echo "Done. RPM(s) in dist/:"
ls -la dist/*.rpm 2>/dev/null || true
