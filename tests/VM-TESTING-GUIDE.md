# RFE Automation Installer - VM Testing Guide

## Created VMs

### ✅ Fedora 41 Workstation
- **Name**: `rfe-test-fedora41`
- **RAM**: 4GB
- **CPUs**: 2
- **Disk**: 50GB
- **Status**: Ready for installation

### 📋 RHEL 9.5 (Optional)
To add RHEL 9 testing:
1. Download RHEL 9.5 ISO from: https://access.redhat.com/downloads/content/479/ver=/rhel---9/9.5/x86_64/product-software
2. Save to: `~/VMs/isos/rhel-9.5-x86_64-dvd.iso`
3. Run:
```bash
sudo virt-install \
    --name rfe-test-rhel9 \
    --ram 4096 \
    --vcpus 2 \
    --disk path=/var/lib/libvirt/images/rfe-test-rhel9.qcow2,size=50,format=qcow2 \
    --os-variant rhel9.5 \
    --cdrom ~/VMs/isos/rhel-9.5-x86_64-dvd.iso \
    --network network=default \
    --graphics spice \
    --video qxl \
    --channel spicevmc \
    --noautoconsole \
    --boot uefi
```

## 🚀 Quick Start

### 1. Open virt-manager
```bash
sudo virt-manager
```

### 2. Connect to Fedora 41 VM
- Double-click `rfe-test-fedora41` in virt-manager
- Or use: `sudo virt-viewer rfe-test-fedora41`

### 3. Install Fedora
1. Boot from ISO (should start automatically)
2. Click "Install to Hard Drive"
3. Select installation destination (50GB disk)
4. Create user account (e.g., `testuser`)
5. Set root password
6. Complete installation and reboot

### 4. After OS Installation

Once logged into the Fedora VM:

```bash
# Install git (should already be there)
sudo dnf install -y git

# Clone your RFE automation tool
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation

# Run the automated installer
./install-improved.sh

# Test the tool
./bin/tam-rfe-chat --help
```

## 📸 Snapshots (Recommended)

After completing OS installation, take a snapshot for quick reset:

```bash
# Fedora 41
sudo virsh snapshot-create-as rfe-test-fedora41 clean-os "Clean Fedora installation"

# RHEL 9 (if created)
sudo virsh snapshot-create-as rfe-test-rhel9 clean-os "Clean RHEL installation"
```

### Revert to Snapshot
```bash
sudo virsh snapshot-revert rfe-test-fedora41 clean-os
```

### List Snapshots
```bash
sudo virsh snapshot-list rfe-test-fedora41
```

## 🧪 Testing Workflow

### First-Time Install Test
1. Boot VM
2. Complete OS installation
3. Take "clean-os" snapshot
4. Clone RFE automation repo
5. Run `./install-improved.sh`
6. Document any errors
7. Test the tool: `./bin/tam-rfe-chat`
8. Take "post-install" snapshot

### Repeat Testing
```bash
# Reset to clean OS
sudo virsh snapshot-revert rfe-test-fedora41 clean-os

# Start VM
sudo virsh start rfe-test-fedora41

# Connect
sudo virt-viewer rfe-test-fedora41

# Re-test installer
# (inside VM: git clone, ./install-improved.sh)
```

## 🎮 VM Management

### Start VM
```bash
sudo virsh start rfe-test-fedora41
```

### Stop VM
```bash
sudo virsh shutdown rfe-test-fedora41
# Or force stop:
sudo virsh destroy rfe-test-fedora41
```

### Delete VM
```bash
sudo virsh destroy rfe-test-fedora41
sudo virsh undefine rfe-test-fedora41 --remove-all-storage
```

### VM Console Access
```bash
# GUI
sudo virt-viewer rfe-test-fedora41

# Or use virt-manager
sudo virt-manager
```

## 📝 Installation Test Checklist

For each platform, document:

- [ ] OS version installed
- [ ] Python version: `python3 --version`
- [ ] Installer method used (UV vs pip+venv)
- [ ] Installation time (minutes)
- [ ] Any errors encountered
- [ ] Tool functionality verification:
  - [ ] `./bin/tam-rfe-chat --help`
  - [ ] `./bin/tam-rfe-monitor`
  - [ ] `rhcase --version`

## 🐛 Common Issues

### Issue: "Network default not found"
**Fix**: Use `sudo virt-install` instead of user-mode libvirt

### Issue: "Permission denied" accessing ISO
**Fix**: Copy ISO to `/var/lib/libvirt/images/` or use sudo

### Issue: VM won't start
**Check**:
```bash
sudo virsh list --all
sudo virsh start rfe-test-fedora41
sudo virsh dominfo rfe-test-fedora41
```

## 📊 Test Results Format

Create test reports in: `rfe-automation-clean/tests/results/`

Example: `fedora41-test-YYYY-MM-DD.md`

```markdown
# RFE Installer Test - Fedora 41

**Date**: 2025-10-15
**Tester**: jbyrd
**Platform**: Fedora 41 Workstation

## Environment
- Python Version: 3.12.5
- Installed Packages: git, python3

## Installation
- Method: UV package manager
- Duration: 3 minutes
- Errors: None
- Result: ✅ Success

## Verification
- `tam-rfe-chat --help`: ✅ Works
- `rhcase --version`: ✅ Works
- Generate report: ✅ Works

## Notes
- Installation was smooth
- No build dependencies needed
- UV method worked perfectly
```

---

**VM Location**: `/var/lib/libvirt/images/`
**ISO Location**: `~/VMs/isos/`
**Created**: 2025-10-15

