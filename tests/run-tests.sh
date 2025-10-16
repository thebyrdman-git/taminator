#!/bin/bash
# Wrapper script to run Ansible-based installation tests

set -euo pipefail

cd "$(dirname "$0")"

echo "🧪 RFE Automation Installation Testing (Ansible)"
echo "=================================================="
echo ""

# Check for ansible-playbook
if ! command -v ansible-playbook &> /dev/null; then
    echo "❌ ansible-playbook not found"
    echo "   Install with: sudo dnf install ansible-core"
    exit 1
fi

# Check for podman
if ! command -v podman &> /dev/null; then
    echo "❌ podman not found"
    echo "   Install with: sudo dnf install podman"
    exit 1
fi

# Check for rsync (needed for synchronize module)
if ! command -v rsync &> /dev/null; then
    echo "❌ rsync not found"
    echo "   Install with: sudo dnf install rsync"
    exit 1
fi

echo "✅ All test prerequisites available"
echo ""

# Run ansible playbook
ansible-playbook test-installation.yml -v

echo ""
echo "=================================================="
echo "Test results saved in: ~/.cache/rfe-tests/"
echo "=================================================="

