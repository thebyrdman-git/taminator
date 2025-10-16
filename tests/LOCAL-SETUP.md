# Running Test VMs Locally on Your Laptop

## Overview

This guide shows you how to create the same test VMs on your **local laptop** instead of on miraclemax.

## Prerequisites

Your laptop already has:
- ✅ Vagrant installed
- ✅ `vagrant-libvirt` plugin installed
- ✅ `virt-manager` available

## Quick Start

```bash
# From your laptop
cd /home/jbyrd/pai/rfe-automation-clean/tests

# Create VMs locally (not on miraclemax)
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant up alma9

# Access the GUI
sudo virt-manager
# Double-click the VM in the list
```

## Commands

### Creating VMs

```bash
# AlmaLinux 9 with GNOME (recommended)
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant up alma9

# Fedora 41 with GNOME
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant up fedora41

# Both VMs
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant up
```

### Managing VMs

```bash
# Check status
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant status

# SSH into VMs
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant ssh alma9
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant ssh fedora41

# Stop VMs
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant halt

# Delete VMs
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant destroy -f
```

### Snapshots

```bash
# Save snapshot
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant snapshot save alma9 clean-install

# Restore snapshot
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant snapshot restore alma9 clean-install

# List snapshots
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant snapshot list
```

## Accessing the GUI

### Option 1: virt-manager (Easiest)

```bash
sudo virt-manager

# VMs will appear as:
# - rfe-test-alma9-local
# - rfe-test-fedora41-local

# Double-click to open console
```

### Option 2: virt-viewer (Direct)

```bash
# For AlmaLinux
virt-viewer rfe-test-alma9-local

# For Fedora
virt-viewer rfe-test-fedora41-local
```

### Option 3: SPICE Remote Viewer

```bash
# Get SPICE connection details
virsh domdisplay rfe-test-alma9-local

# Use remote-viewer with the displayed URI
remote-viewer spice://localhost:5900
```

## Installing the RFE Tool

After the VM boots into GUI:

1. **Login**: `testuser` / `testpass`

2. **Open Terminal** and copy the bundled installer:

```bash
# Option A: Copy from your laptop's filesystem
# (You'll need to mount a shared folder or use scp)

# Option B: Recreate the tarball on your laptop
cd /home/jbyrd/pai/rfe-automation-clean
tar czf /tmp/rfe-automation-bundled.tar.gz \
  --exclude=.git --exclude=tests --exclude=__pycache__ \
  --exclude=.venv --exclude='*.pyc' .

# Then copy into VM (from your laptop terminal)
# Get the VM's IP first
vagrant ssh alma9 --vagrantfile=Vagrantfile.local -c "ip -4 addr show | grep inet"

# Copy the tarball
scp /tmp/rfe-automation-bundled.tar.gz testuser@<VM_IP>:/tmp/

# In the VM's GUI terminal
cd ~
tar xzf /tmp/rfe-automation-bundled.tar.gz
cd rfe-and-bug-tracker-automation
./install-offline.sh
```

## Simplified Install Script

Or create a quick install script:

```bash
# From your laptop
cd /home/jbyrd/pai/rfe-automation-clean/tests

# Create install helper
cat > install-to-vm.sh << 'EOF'
#!/bin/bash
# Quick installer for local VMs

VM_NAME=${1:-alma9}

echo "Creating bundled installer..."
cd /home/jbyrd/pai/rfe-automation-clean
tar czf /tmp/rfe-automation-bundled.tar.gz \
  --exclude=.git --exclude=tests --exclude=__pycache__ \
  --exclude=.venv --exclude='*.pyc' .

echo "Getting VM IP..."
VM_IP=$(vagrant ssh $VM_NAME --vagrantfile=Vagrantfile.local -c "hostname -I | awk '{print \$1}'" 2>/dev/null | tr -d '\r')

if [ -z "$VM_IP" ]; then
    echo "❌ Could not get VM IP. Is it running?"
    exit 1
fi

echo "Copying to VM at $VM_IP..."
scp -o StrictHostKeyChecking=no /tmp/rfe-automation-bundled.tar.gz testuser@$VM_IP:/tmp/

echo "Installing in VM..."
ssh -o StrictHostKeyChecking=no testuser@$VM_IP << 'ENDSSH'
cd ~
mkdir -p rfe-and-bug-tracker-automation
tar xzf /tmp/rfe-automation-bundled.tar.gz -C rfe-and-bug-tracker-automation
cd rfe-and-bug-tracker-automation
./install-offline.sh
ENDSSH

echo "✅ Installation complete! Access GUI and test."
EOF

chmod +x install-to-vm.sh

# Use it
./install-to-vm.sh alma9
```

## Differences from Remote (miraclemax) Setup

| Feature | Remote (miraclemax) | Local (laptop) |
|---------|-------------------|----------------|
| **Vagrantfile** | `Vagrantfile` | `VAGRANT_VAGRANTFILE=Vagrantfile.local` |
| **Connection** | SSH to miraclemax | localhost |
| **Graphics** | VNC (tunneled) | SPICE (direct) |
| **Video** | virtio (headless) | qxl (optimized) |
| **Access** | `virt-viewer --connect qemu+ssh://...` | `virt-manager` (localhost) |
| **Performance** | Network latency | Native speed |

## VM Specifications

Both VMs have the same specs as remote:

| Spec | Value |
|------|-------|
| **RAM** | 4GB |
| **CPUs** | 2 cores |
| **Disk** | 50GB (thin provisioned) |
| **Network** | NAT (default libvirt) |
| **User** | testuser / testpass |

## Troubleshooting

### libvirt not running

```bash
sudo systemctl start libvirtd
sudo systemctl enable libvirtd
```

### Permission issues

```bash
# Add yourself to libvirt group
sudo usermod -a -G libvirt $USER

# Logout and login again
```

### Can't access GUI

```bash
# Check if VM is running
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant status
virsh list --all

# Verify graphics are enabled
virsh domdisplay rfe-test-alma9-local
```

### Network issues in VM

```bash
# Check default network is active
sudo virsh net-list --all
sudo virsh net-start default
sudo virsh net-autostart default
```

## Performance Tips

Local VMs will be **much faster** than remote:
- Native graphics (SPICE)
- No network latency
- Direct disk I/O
- Better for Cursor IDE testing

## Summary

**To run the same VMs locally:**

1. Use `Vagrantfile.local` via the `VAGRANT_VAGRANTFILE` environment variable
2. Prepend `VAGRANT_VAGRANTFILE=Vagrantfile.local` to all vagrant commands
3. Access via local `virt-manager` (no SSH needed)
4. Copy the bundled RFE installer into the VMs

**Quick command:**
```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests
VAGRANT_VAGRANTFILE=Vagrantfile.local vagrant up alma9
sudo virt-manager
# Double-click "rfe-test-alma9-local"
# Login: testuser / testpass
```

🎯 **Much faster and more responsive for GUI testing!**

