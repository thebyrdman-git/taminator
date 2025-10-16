#!/bin/bash
# Copy bundled RFE automation tool to a local VM
# Usage: ./copy-rfe-to-vm.sh [alma9|fedora41]

set -e

VM_NAME=${1:-alma9}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📦 Copying RFE automation tool to $VM_NAME..."
echo ""

# Check if VM is running
if ! VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant status "$VM_NAME" 2>/dev/null | grep -q "running"; then
    echo "❌ VM $VM_NAME is not running"
    echo "Start it with: VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant up $VM_NAME"
    exit 1
fi

# Get VM IP
echo "Getting VM IP address..."
VM_IP=$(VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant ssh "$VM_NAME" -c "hostname -I | awk '{print \$1}'" 2>/dev/null | tr -d '\r\n')

if [ -z "$VM_IP" ]; then
    echo "❌ Could not get VM IP address"
    exit 1
fi

echo "✅ VM IP: $VM_IP"
echo ""

# Check if bundled installer exists
if [ ! -f "/tmp/rfe-automation-bundled.tar.gz" ]; then
    echo "❌ Bundled installer not found"
    echo "Run: ./setup-local-vm.sh first"
    exit 1
fi

# Copy to VM
echo "Copying bundled installer to VM..."
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    /tmp/rfe-automation-bundled.tar.gz testuser@$VM_IP:/tmp/

echo ""
echo "Installing in VM..."
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null testuser@$VM_IP << 'ENDSSH'
cd ~
if [ -d "rfe-and-bug-tracker-automation" ]; then
    echo "Backing up old version..."
    mv rfe-and-bug-tracker-automation rfe-and-bug-tracker-automation.backup.$(date +%s)
fi

echo "Extracting installer..."
mkdir -p rfe-and-bug-tracker-automation
tar xzf /tmp/rfe-automation-bundled.tar.gz -C rfe-and-bug-tracker-automation
cd rfe-and-bug-tracker-automation

echo ""
echo "Running offline installer..."
./install-offline.sh

echo ""
echo "✅ Installation complete!"
echo ""
echo "To use the tool:"
echo "  cd ~/rfe-and-bug-tracker-automation"
echo "  source .venv/bin/activate"
echo "  ./bin/tam-rfe-chat"
ENDSSH

echo ""
echo "✅ RFE automation tool installed successfully!"
echo ""
echo "Access the VM GUI to test:"
echo "  sudo virt-manager"
echo "  (Double-click: rfe-test-$VM_NAME-local)"
echo ""
echo "Login: testuser / testpass"

