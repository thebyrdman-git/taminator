#!/bin/bash
# Dynamic VPN package installation for multiple distributions
# Supports EPEL 8/9/10 and Fedora 40/41/42/43

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS_ID="$ID"
        OS_VERSION_ID="$VERSION_ID"
        OS_NAME="$NAME"
    else
        echo -e "${RED}❌ Cannot detect OS version${NC}"
        exit 1
    fi
}

get_copr_release() {
    case "$OS_ID" in
        rhel|almalinux|rocky)
            # RHEL-based systems use EPEL
            echo "epel-${OS_VERSION_ID%%.*}"
            ;;
        fedora)
            # Fedora uses its version number
            if [ "$OS_VERSION_ID" = "rawhide" ]; then
                echo "fedora-rawhide"
            else
                echo "fedora-${OS_VERSION_ID}"
            fi
            ;;
        *)
            echo "unsupported"
            ;;
    esac
}

check_supported() {
    local release=$1
    case "$release" in
        epel-8|epel-9|epel-10)
            return 0
            ;;
        fedora-40|fedora-41|fedora-42|fedora-43|fedora-rawhide)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

install_vpn_packages() {
    local copr_release=$(get_copr_release)
    
    echo -e "${BLUE}📦 Detected: $OS_NAME $OS_VERSION_ID${NC}"
    echo -e "   COPR release: $copr_release"
    echo ""
    
    if [ "$copr_release" = "unsupported" ]; then
        echo -e "${RED}❌ OS not supported by COPR repo${NC}"
        echo "   Supported: RHEL/Alma/Rocky 8-10, Fedora 40-43"
        echo ""
        echo "Manual VPN setup required:"
        echo "  1. Install openvpn manually"
        echo "  2. Follow VPN-SETUP-GUIDE.md"
        return 1
    fi
    
    # Check if version is known to be supported
    if check_supported "$copr_release"; then
        echo -e "${GREEN}✅ $copr_release is supported${NC}"
    else
        echo -e "${YELLOW}⚠️  $copr_release may not be supported${NC}"
        echo "   Attempting installation anyway..."
    fi
    
    if [ "$copr_release" = "fedora-rawhide" ]; then
        echo -e "${YELLOW}⚠️  Rawhide detected - using at your own risk${NC}"
    fi
    
    echo ""
    echo "Installing COPR plugin..."
    if ! dnf install -y 'dnf-command(copr)' 2>/dev/null; then
        echo -e "${RED}❌ Failed to install COPR plugin${NC}"
        return 1
    fi
    
    echo "Enabling VPN packages repository..."
    if ! dnf copr enable -y copr.devel.redhat.com/@endpoint-systems-sysadmins/unsupported-fedora-packages 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Failed to enable COPR repo${NC}"
        echo "   Repo may not have packages for $copr_release"
        echo ""
        echo "Check available releases at:"
        echo "   https://copr.devel.redhat.com/coprs/g/endpoint-systems-sysadmins/unsupported-fedora-packages/"
        return 1
    fi
    
    echo "Installing VPN packages..."
    if ! dnf install -y NetworkManager-openvpn openvpn; then
        echo -e "${RED}❌ Failed to install VPN packages${NC}"
        echo "   Packages may not be available for $copr_release"
        return 1
    fi
    
    # Try to install GUI components (optional)
    if dnf install -y NetworkManager-openvpn-gnome 2>/dev/null; then
        echo "  + GUI components installed"
    fi
    
    echo ""
    echo -e "${GREEN}✅ VPN packages installed successfully${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Import VPN profile: sudo nmcli connection import type openvpn file /path/to/profile.ovpn"
    echo "  2. Connect: sudo nmcli connection up <connection-name>"
    echo "  3. Get Kerberos ticket: kinit user@REDHAT.COM"
    return 0
}

# Main
echo "================================================"
echo "  RFE Tools - Dynamic VPN Package Installer"
echo "================================================"
echo ""

detect_os
install_vpn_packages

