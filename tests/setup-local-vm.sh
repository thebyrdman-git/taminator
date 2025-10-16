#!/bin/bash
# Quick script to create and setup local test VMs
# Usage: ./setup-local-vm.sh [alma9|fedora41|both]

set -e

VM_CHOICE=${1:-alma9}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RFE_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Setting up local test VM(s)..."
echo ""

# Create bundled installer if it doesn't exist
if [ ! -f "/tmp/rfe-automation-bundled.tar.gz" ]; then
    echo "📦 Creating bundled RFE automation installer..."
    cd "$RFE_ROOT"
    tar czf /tmp/rfe-automation-bundled.tar.gz \
      --exclude=.git --exclude=tests --exclude=__pycache__ \
      --exclude=.venv --exclude='*.pyc' .
    echo "✅ Bundled installer created"
    echo ""
fi

# Create VMs
cd "$SCRIPT_DIR"

if [ "$VM_CHOICE" = "both" ]; then
    echo "Creating both VMs..."
    VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant up
elif [ "$VM_CHOICE" = "alma9" ] || [ "$VM_CHOICE" = "fedora41" ]; then
    echo "Creating $VM_CHOICE VM..."
    VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant up "$VM_CHOICE"
else
    echo "❌ Invalid choice. Use: alma9, fedora41, or both"
    exit 1
fi

echo ""
echo "✅ VM(s) created!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Access the GUI:"
echo "   sudo virt-manager"
echo "   (Double-click the VM: rfe-test-$VM_CHOICE-local)"
echo ""
echo "2. Login: testuser / testpass"
echo ""
echo "3. Copy installer to VM (from your laptop terminal):"
echo "   cd $SCRIPT_DIR"
echo "   ./copy-rfe-to-vm.sh $VM_CHOICE"
echo ""
echo "Or open virt-manager now?"
read -p "Launch virt-manager? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo virt-manager &
fi

