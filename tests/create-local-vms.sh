#!/bin/bash
# Create test VMs directly with virt-install (no Vagrant)
# Much simpler and more reliable than vagrant-libvirt

set -e

VM_DIR="/var/lib/libvirt/images"
ISO_DIR="$HOME/Downloads"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

VM_CHOICE=${1:-menu}

echo "🚀 Creating Test VMs (No Vagrant)"
echo "=================================="
echo ""

# Menu if no argument provided
if [ "$VM_CHOICE" = "menu" ]; then
    echo "Which VM do you want to create?"
    echo ""
    echo "1) AlmaLinux 9 (RHEL compatible)"
    echo "2) Fedora 41 Workstation"
    echo "3) Both"
    echo ""
    read -p "Choice (1/2/3): " VM_CHOICE
fi

case "$VM_CHOICE" in
    1|alma|almalinux)
        CREATE_ALMA=true
        CREATE_FEDORA=false
        ;;
    2|fedora)
        CREATE_ALMA=false
        CREATE_FEDORA=true
        ;;
    3|both)
        CREATE_ALMA=true
        CREATE_FEDORA=true
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""

# Check for AlmaLinux ISO
if [ "$CREATE_ALMA" = true ]; then
    ALMA_ISO="$ISO_DIR/AlmaLinux-9-latest-x86_64-dvd.iso"
    if [ ! -f "$ALMA_ISO" ]; then
        echo -e "${YELLOW}📥 AlmaLinux ISO not found${NC}"
        echo "Download from: https://almalinux.org/get-almalinux/"
        echo ""
        echo "Command:"
        echo "  cd ~/Downloads"
        echo "  wget https://repo.almalinux.org/almalinux/9/isos/x86_64/AlmaLinux-9-latest-x86_64-dvd.iso"
        echo ""
        read -p "Press Enter when ISO is downloaded..."
    fi
fi

# Check for Fedora ISO (try Fedora 42 first, then 41)
if [ "$CREATE_FEDORA" = true ]; then
    FEDORA_ISO_42="$ISO_DIR/Fedora-Workstation-Live-x86_64-42"
    FEDORA_ISO_41="$ISO_DIR/Fedora-Workstation-Live-x86_64-41-1.4.iso"
    
    # Find Fedora 42 ISO (any format/beta/release)
    FEDORA_ISO=$(find "$ISO_DIR" -name "Fedora-Workstation-Live-*42*.iso" 2>/dev/null | head -1)
    
    # Fall back to Fedora 41
    if [ -z "$FEDORA_ISO" ] || [ ! -f "$FEDORA_ISO" ]; then
        FEDORA_ISO=$(find "$ISO_DIR" -name "Fedora-Workstation-Live-*41*.iso" 2>/dev/null | head -1)
        if [ -n "$FEDORA_ISO" ] && [ -f "$FEDORA_ISO" ]; then
            FEDORA_VERSION="41"
        else
            FEDORA_ISO="$FEDORA_ISO_41"
            FEDORA_VERSION="41"
        fi
    else
        FEDORA_VERSION="42"
    fi
    
    if [ ! -f "$FEDORA_ISO" ]; then
        echo -e "${YELLOW}📥 Fedora ISO not found${NC}"
        echo "Download Fedora 42 from: https://fedoraproject.org/workstation/download"
        echo ""
        echo "Save it to: ~/Downloads/"
        echo ""
        read -p "Press Enter when ISO is downloaded..."
        
        # Try to find it again
        FEDORA_ISO=$(find "$ISO_DIR" -name "Fedora-Workstation-Live-*42*.iso" 2>/dev/null | head -1)
        if [ -z "$FEDORA_ISO" ]; then
            FEDORA_ISO=$(find "$ISO_DIR" -name "Fedora-Workstation-Live-*41*.iso" 2>/dev/null | head -1)
            FEDORA_VERSION="41"
        else
            FEDORA_VERSION="42"
        fi
    fi
    
    echo "Found: $(basename "$FEDORA_ISO")"
fi

# Create AlmaLinux VM
if [ "$CREATE_ALMA" = true ]; then
    echo -e "${BLUE}Creating AlmaLinux 9 VM...${NC}"
    sudo virt-install \
      --name rfe-test-alma9-local \
      --memory 4096 \
      --vcpus 2 \
      --disk size=50 \
      --cdrom "$ALMA_ISO" \
      --os-variant almalinux9 \
      --network network=default \
      --graphics spice \
      --video qxl \
      --noautoconsole
    
    echo -e "${GREEN}✅ AlmaLinux 9 VM Created!${NC}"
    echo ""
fi

# Create Fedora VM
if [ "$CREATE_FEDORA" = true ]; then
    echo -e "${BLUE}Creating Fedora $FEDORA_VERSION VM...${NC}"
    
    # Use appropriate os-variant (fall back to fedora-unknown if F42 not recognized)
    OS_VARIANT="fedora$FEDORA_VERSION"
    
    sudo virt-install \
      --name rfe-test-fedora${FEDORA_VERSION}-local \
      --memory 4096 \
      --vcpus 2 \
      --disk size=50 \
      --cdrom "$FEDORA_ISO" \
      --os-variant "$OS_VARIANT" \
      --network network=default \
      --graphics spice \
      --video qxl \
      --noautoconsole 2>&1 || \
    sudo virt-install \
      --name rfe-test-fedora${FEDORA_VERSION}-local \
      --memory 4096 \
      --vcpus 2 \
      --disk size=50 \
      --cdrom "$FEDORA_ISO" \
      --os-variant fedora-unknown \
      --network network=default \
      --graphics spice \
      --video qxl \
      --noautoconsole
    
    echo -e "${GREEN}✅ Fedora $FEDORA_VERSION VM Created!${NC}"
    echo ""
fi

echo ""
echo "📋 Next steps:"
echo ""
echo "1. Open virt-manager:"
echo "   sudo virt-manager"
echo ""
echo "2. Double-click the VM(s) to complete OS installation:"
if [ "$CREATE_ALMA" = true ]; then
    echo "   - rfe-test-alma9-local (Select 'Server with GUI')"
fi
if [ "$CREATE_FEDORA" = true ]; then
    echo "   - rfe-test-fedora${FEDORA_VERSION}-local (Install Fedora Workstation)"
fi
echo ""
echo "3. During installation:"
echo "   - Create user: testuser / testpass"
echo "   - Complete installation and reboot"
echo ""
echo "4. After OS install, copy the RFE tool:"
echo "   ./copy-rfe-direct.sh <vm-name>"
echo ""
echo "Launch virt-manager now?"
read -p "(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo virt-manager &
fi

