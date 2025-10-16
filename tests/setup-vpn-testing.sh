#!/bin/bash
# Setup script for Alma Linux 9 VM with Red Hat VPN for online installation testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Alma Linux 9 VM - VPN Setup for RFE Online Installation Test ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Vagrant is installed
if ! command -v vagrant &> /dev/null; then
    echo "❌ Vagrant not installed"
    echo "   Install: sudo dnf install vagrant"
    exit 1
fi

# Check if libvirt provider is available
if ! vagrant plugin list | grep -q vagrant-libvirt; then
    echo "⚠️  vagrant-libvirt plugin not installed"
    echo "   Install: vagrant plugin install vagrant-libvirt"
    exit 1
fi

echo "📦 Step 1: Starting Alma Linux 9 VM"
echo "-----------------------------------"
vagrant up alma9

echo ""
echo "✅ VM Started"
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  VPN Configuration Required                                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "You need to obtain Red Hat VPN credentials from:"
echo "  📄 KB0005449 - OpenVPN User Guide"
echo "  🔗 https://redhat.service-now.com/help?id=kb_article&sysparm_article=KB0005449"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Download your VPN profile from Red Hat IT:"
echo "   https://access.redhat.com/management/vpn"
echo ""
echo "2. SSH into the VM:"
echo "   vagrant ssh alma9"
echo ""
echo "3. Inside the VM, configure VPN:"
echo "   # Copy VPN config from host"
echo "   # (You'll need to download .ovpn file from Red Hat portal)"
echo ""
echo "4. Test GitLab access:"
echo "   curl -I https://gitlab.cee.redhat.com"
echo ""
echo "5. Clone and install:"
echo "   git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git"
echo "   cd rfe-and-bug-tracker-automation"
echo "   ./install.sh"
echo ""
echo "⚠️  Note: You need to be on Red Hat VPN for GitLab CEE access"
echo ""

