#!/bin/bash

# TAM RFE Report Scheduler - Installation Script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"

echo "Installing TAM RFE Report Scheduler"
echo "===================================="
echo ""

# Ensure install directory exists
mkdir -p "$INSTALL_DIR"

# Install main command
echo "Installing commands..."
cp "$SCRIPT_DIR/bin/tam-rfe-schedule" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/tam-rfe-schedule"

# Create aliases (symlinks)
ln -sf "$INSTALL_DIR/tam-rfe-schedule" "$INSTALL_DIR/tam-rfe-scheduler"
ln -sf "$INSTALL_DIR/tam-rfe-schedule" "$INSTALL_DIR/active-case-report-scheduler"

echo "✅ Installation complete"
echo ""
echo "Available commands (all same tool):"
echo "  tam-rfe-schedule"
echo "  tam-rfe-scheduler"
echo "  active-case-report-scheduler"
echo ""
echo "Get started:"
echo "  tam-rfe-schedule --help"
echo "  tam-rfe-schedule add \"My Report\" --command \"tam-rfe-chat 'query'\" --frequency \"0 8 * * 1\" --email you@redhat.com"
echo ""

