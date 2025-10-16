#!/bin/bash
# Copy RFE automation tool to VM (without Vagrant)

set -e

VM_NAME=${1:-rfe-test-alma9-local}

echo "📦 Copying RFE automation tool to $VM_NAME..."
echo ""

# Get VM IP
echo "Getting VM IP address..."
VM_IP=$(sudo virsh domifaddr "$VM_NAME" | grep -oP '192\.168\.\d+\.\d+' | head -1)

if [ -z "$VM_IP" ]; then
    echo "❌ Could not get VM IP. Is it running and logged in?"
    echo ""
    echo "Try:"
    echo "  sudo virsh domifaddr $VM_NAME"
    exit 1
fi

echo "✅ VM IP: $VM_IP"
echo ""

# Create bundled installer if needed
if [ ! -f "/tmp/rfe-automation-bundled.tar.gz" ]; then
    echo "Creating bundled installer..."
    cd "$(dirname "$0")/.."
    tar czf /tmp/rfe-automation-bundled.tar.gz \
      --exclude=.git --exclude=tests --exclude=__pycache__ \
      --exclude=.venv --exclude='*.pyc' .
fi

# Copy to VM
echo "Copying to VM..."
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    /tmp/rfe-automation-bundled.tar.gz testuser@$VM_IP:/tmp/

echo ""
echo "Installing in VM..."
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null testuser@$VM_IP << 'ENDSSH'
cd ~
if [ -d "rfe-and-bug-tracker-automation" ]; then
    mv rfe-and-bug-tracker-automation rfe-and-bug-tracker-automation.backup.$(date +%s)
fi

mkdir -p rfe-and-bug-tracker-automation
tar xzf /tmp/rfe-automation-bundled.tar.gz -C rfe-and-bug-tracker-automation
cd rfe-and-bug-tracker-automation
./install-offline.sh
ENDSSH

echo ""
echo "✅ Installation complete!"
echo ""
echo "Access the VM GUI to test Cursor IDE"

