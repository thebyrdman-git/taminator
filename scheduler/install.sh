#!/bin/bash

# TAM RFE Report Scheduler - Installation Script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"

echo "Installing TAM RFE Report Scheduler (Phase 2)"
echo "=============================================="
echo ""

# Ensure install directory exists
mkdir -p "$INSTALL_DIR"

# Install main command
echo "Installing commands..."
cp "$SCRIPT_DIR/bin/tam-rfe-schedule" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/tam-rfe-schedule"

# Install daemon
cp "$SCRIPT_DIR/bin/tam-rfe-scheduler-daemon" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/tam-rfe-scheduler-daemon"

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
echo "Daemon installed:"
echo "  tam-rfe-scheduler-daemon"
echo ""
echo "Get started:"
echo "  tam-rfe-schedule --help"
echo ""
echo "Phase 2 Features:"
echo "  tam-rfe-schedule add \"Report\" --command \"...\" --frequency \"...\" --email ..."
echo "  tam-rfe-schedule start    # Start automatic execution"
echo "  tam-rfe-schedule status   # Check daemon status"
echo "  tam-rfe-schedule logs     # View execution history"
echo ""

