#!/bin/bash
# Create GUI Test VMs for RFE Automation Installer Testing
# Target: RHEL 9.5 and Fedora 42 with GNOME desktop

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ${NC}  $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC}  $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

# VM Configuration
VM_DIR="${HOME}/VMs"
ISO_DIR="${VM_DIR}/isos"
DISK_SIZE="50G"
RAM="4096"
VCPUS="2"

# VM Names
RHEL9_VM="rfe-test-rhel9"
FEDORA_VM="rfe-test-fedora41"

# ISO URLs (will need manual download for RHEL)
FEDORA_ISO_URL="https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-41-1.4.iso"
FEDORA_ISO_NAME="Fedora-Workstation-Live-x86_64-41-1.4.iso"

echo "🖥️  RFE Automation Test VM Creator"
echo "===================================="
echo ""

# Create directories
log_info "Creating VM directories..."
mkdir -p "$VM_DIR"
mkdir -p "$ISO_DIR"

# Check if VMs already exist
if virsh list --all | grep -q "$RHEL9_VM"; then
    log_warning "VM $RHEL9_VM already exists"
    read -p "Delete and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Destroying $RHEL9_VM..."
        virsh destroy "$RHEL9_VM" 2>/dev/null || true
        virsh undefine "$RHEL9_VM" --remove-all-storage 2>/dev/null || true
    else
        log_info "Skipping RHEL 9 VM creation"
        SKIP_RHEL9=1
    fi
fi

if virsh list --all | grep -q "$FEDORA_VM"; then
    log_warning "VM $FEDORA_VM already exists"
    read -p "Delete and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Destroying $FEDORA_VM..."
        virsh destroy "$FEDORA_VM" 2>/dev/null || true
        virsh undefine "$FEDORA_VM" --remove-all-storage 2>/dev/null || true
    else
        log_info "Skipping Fedora 41 VM creation"
        SKIP_FEDORA=1
    fi
fi

# Download/Check Fedora ISO
if [[ ! ${SKIP_FEDORA:-0} == 1 ]]; then
    FEDORA_ISO="$ISO_DIR/$FEDORA_ISO_NAME"
    if [ ! -f "$FEDORA_ISO" ]; then
        log_info "Downloading Fedora 41 Workstation ISO..."
        log_info "This will take a while (2-3 GB)..."
        wget -O "$FEDORA_ISO" "$FEDORA_ISO_URL" || {
            log_error "Failed to download Fedora ISO"
            log_info "You can manually download from:"
            log_info "$FEDORA_ISO_URL"
            log_info "Save to: $FEDORA_ISO"
            exit 1
        }
        log_success "Fedora ISO downloaded"
    else
        log_success "Fedora ISO already downloaded"
    fi
fi

# Check for RHEL 9 ISO
if [[ ! ${SKIP_RHEL9:-0} == 1 ]]; then
    RHEL9_ISO=$(find "$ISO_DIR" -name "rhel-*-9.*-x86_64-dvd.iso" | head -1)
    if [ -z "$RHEL9_ISO" ]; then
        log_warning "RHEL 9 ISO not found in $ISO_DIR"
        log_info "Download from: https://access.redhat.com/downloads/content/479/ver=/rhel---9/9.5/x86_64/product-software"
        log_info "Save as: $ISO_DIR/rhel-9.5-x86_64-dvd.iso"
        echo ""
        read -p "Press Enter when RHEL ISO is ready, or Ctrl-C to skip..."
        RHEL9_ISO=$(find "$ISO_DIR" -name "rhel-*-9.*-x86_64-dvd.iso" | head -1)
        if [ -z "$RHEL9_ISO" ]; then
            log_error "RHEL ISO still not found, skipping RHEL VM"
            SKIP_RHEL9=1
        fi
    else
        log_success "Found RHEL 9 ISO: $(basename $RHEL9_ISO)"
    fi
fi

# Create Fedora 41 VM
if [[ ! ${SKIP_FEDORA:-0} == 1 ]]; then
    log_info "Creating Fedora 41 VM..."
    virt-install \
        --name "$FEDORA_VM" \
        --ram "$RAM" \
        --vcpus "$VCPUS" \
        --disk path="$VM_DIR/${FEDORA_VM}.qcow2",size=50,format=qcow2 \
        --os-variant fedora41 \
        --cdrom "$FEDORA_ISO" \
        --network network=default \
        --graphics spice \
        --video qxl \
        --channel spicevmc \
        --noautoconsole \
        --boot uefi
    
    log_success "Fedora 41 VM created: $FEDORA_VM"
    log_info "Connect with: virt-manager or virt-viewer $FEDORA_VM"
fi

# Create RHEL 9 VM
if [[ ! ${SKIP_RHEL9:-0} == 1 ]]; then
    log_info "Creating RHEL 9 VM..."
    virt-install \
        --name "$RHEL9_VM" \
        --ram "$RAM" \
        --vcpus "$VCPUS" \
        --disk path="$VM_DIR/${RHEL9_VM}.qcow2",size=50,format=qcow2 \
        --os-variant rhel9.5 \
        --cdrom "$RHEL9_ISO" \
        --network network=default \
        --graphics spice \
        --video qxl \
        --channel spicevmc \
        --noautoconsole \
        --boot uefi
    
    log_success "RHEL 9 VM created: $RHEL9_VM"
    log_info "Connect with: virt-manager or virt-viewer $RHEL9_VM"
fi

echo ""
log_success "VM Creation Complete!"
echo ""
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. Open virt-manager to access the VMs:"
echo "   $ virt-manager"
echo ""
echo "2. Complete installation on each VM:"
echo "   - Select 'Workstation' or 'Server with GUI'"
echo "   - Create user account"
echo "   - Complete installation"
echo ""
echo "3. Once installed, in each VM:"
echo "   a) git clone your RFE automation repo"
echo "   b) cd rfe-and-bug-tracker-automation"
echo "   c) ./install-improved.sh"
echo "   d) Test the tool"
echo ""
echo "4. Take snapshots after installation for quick reset:"
echo "   $ virsh snapshot-create-as $FEDORA_VM clean-install"
echo "   $ virsh snapshot-create-as $RHEL9_VM clean-install"
echo ""
echo "VM Details:"
echo "-----------"
if [[ ! ${SKIP_FEDORA:-0} == 1 ]]; then
    echo "Fedora 41: $FEDORA_VM"
    echo "  - RAM: ${RAM}MB"
    echo "  - CPUs: $VCPUS"
    echo "  - Disk: $DISK_SIZE"
fi
if [[ ! ${SKIP_RHEL9:-0} == 1 ]]; then
    echo "RHEL 9:    $RHEL9_VM"
    echo "  - RAM: ${RAM}MB"
    echo "  - CPUs: $VCPUS"
    echo "  - Disk: $DISK_SIZE"
fi
echo ""

