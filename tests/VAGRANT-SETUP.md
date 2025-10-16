# Vagrant GUI Testing Setup for miraclemax

## Why Vagrant?

**Much faster than manual VMs:**
- ✅ Code-based VM definitions (repeatable)
- ✅ One command to create/destroy
- ✅ Built-in snapshot support
- ✅ Automatic provisioning
- ✅ Remote execution on miraclemax

**vs Manual VMs:**
- ❌ Manual ISO downloads
- ❌ Manual OS installation (20+ min per VM)
- ❌ Manual network configuration
- ❌ No version control for VM config

---

## Prerequisites

### 1. Install Vagrant Locally
```bash
# Fedora/RHEL
sudo dnf install -y vagrant vagrant-libvirt

# Check version
vagrant --version
```

### 2. Setup miraclemax Connection
```bash
# Ensure you can SSH to miraclemax
ssh jbyrd@192.168.1.34

# Install libvirt on miraclemax (if not already)
ssh jbyrd@192.168.1.34 'sudo dnf install -y libvirt libvirt-daemon-kvm qemu-kvm'
ssh jbyrd@192.168.1.34 'sudo systemctl enable --now libvirtd'
```

### 3. Configure Vagrant to Use miraclemax
```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests

# Test connection
vagrant status
```

---

## Quick Start

### Create Fedora 41 GUI VM
```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests

# Create and provision VM (5-10 minutes)
vagrant up fedora41

# Access the GUI
ssh -X jbyrd@192.168.1.34 virt-viewer rfe-test-fedora41

# Or use virt-manager on miraclemax
ssh jbyrd@192.168.1.34
sudo virt-manager
```

### Create RHEL 9 GUI VM
```bash
vagrant up rhel9

# Access
ssh -X jbyrd@192.168.1.34 virt-viewer rfe-test-rhel9
```

---

## Testing Workflow

### 1. Create VM
```bash
vagrant up fedora41
```

### 2. Access GUI
**Option A: virt-viewer (remote X11)**
```bash
ssh -X jbyrd@192.168.1.34 virt-viewer rfe-test-fedora41
```

**Option B: virt-manager on miraclemax**
```bash
ssh jbyrd@192.168.1.34
sudo virt-manager
# Double-click VM in the list
```

**Option C: Web-based VNC (if configured)**
```bash
# From miraclemax
virt-viewer --connect qemu:///system rfe-test-fedora41
```

### 3. Test RFE Installer

Login to VM GUI:
- **User**: `testuser`
- **Pass**: `testpass`

Open Terminal in VM:
```bash
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation
./install-improved.sh

# Test
./bin/tam-rfe-chat --help
```

### 4. Save Snapshot
```bash
# After successful OS install but before RFE install
vagrant snapshot save fedora41 clean-os

# After RFE install
vagrant snapshot save fedora41 post-install
```

### 5. Restore to Clean State
```bash
vagrant snapshot restore fedora41 clean-os

# Re-test installer
# (login to GUI, run installer again)
```

### 6. Destroy When Done
```bash
vagrant destroy -f fedora41
```

---

## Common Commands

### VM Management
```bash
# Create VM
vagrant up fedora41

# Show status
vagrant status

# SSH into VM (console only, not GUI)
vagrant ssh fedora41

# Restart VM
vagrant reload fedora41

# Shutdown VM
vagrant halt fedora41

# Delete VM
vagrant destroy -f fedora41
```

### Snapshots
```bash
# List snapshots
vagrant snapshot list fedora41

# Save snapshot
vagrant snapshot save fedora41 snapshot-name

# Restore snapshot
vagrant snapshot restore fedora41 snapshot-name

# Delete snapshot
vagrant snapshot delete fedora41 snapshot-name
```

### Troubleshooting
```bash
# Get VM info
vagrant ssh-config fedora41

# View provisioning logs
vagrant up fedora41 --provision --debug

# Re-run provisioning
vagrant provision fedora41
```

---

## Alternative: Quick VM Templates

If Vagrant doesn't work well, use **virt-builder** for instant VMs:

```bash
# On miraclemax
ssh jbyrd@192.168.1.34

# List available templates
sudo virt-builder --list | grep -E "fedora-41|rhel-9"

# Create Fedora 41 VM (2 minutes)
sudo virt-builder fedora-41 \
  --size 50G \
  --format qcow2 \
  --output /var/lib/libvirt/images/rfe-test-fedora41.qcow2 \
  --install @workstation-product-environment \
  --root-password password:testpass \
  --hostname rfe-test-fedora41

# Import as VM
sudo virt-install \
  --name rfe-test-fedora41 \
  --ram 4096 \
  --vcpus 2 \
  --disk /var/lib/libvirt/images/rfe-test-fedora41.qcow2 \
  --import \
  --os-variant fedora41 \
  --network network=default \
  --graphics spice \
  --noautoconsole

# Access
sudo virt-viewer rfe-test-fedora41
```

---

## Accessing GUI from Local Machine

### Option 1: X11 Forwarding
```bash
# From your laptop
ssh -X jbyrd@192.168.1.34 virt-viewer rfe-test-fedora41
```

### Option 2: VNC Tunnel
```bash
# Create SSH tunnel
ssh -L 5900:localhost:5900 jbyrd@192.168.1.34

# In another terminal on miraclemax
sudo virsh domdisplay rfe-test-fedora41
# Note the VNC port

# Connect with VNC client to localhost:5900
vncviewer localhost:5900
```

### Option 3: SPICE Client
```bash
# Install remote-viewer locally
sudo dnf install virt-viewer

# From miraclemax, get connection info
ssh jbyrd@192.168.1.34 'sudo virsh domdisplay rfe-test-fedora41'

# Connect (may need tunnel)
remote-viewer spice://192.168.1.34:5900
```

---

## Testing Checklist

For each VM:

- [ ] VM created successfully
- [ ] GUI desktop accessible
- [ ] Can login (testuser/testpass)
- [ ] Git installed
- [ ] Can clone RFE repo
- [ ] Run `./install-improved.sh`
- [ ] Document installation method (UV vs pip)
- [ ] Document installation time
- [ ] Document any errors
- [ ] Test tool: `./bin/tam-rfe-chat --help`
- [ ] Take snapshot after successful install
- [ ] Document in test report

---

## Test Results Location

Save test results in: `rfe-automation-clean/tests/results/`

Example: `fedora41-vagrant-test-2025-10-15.md`

---

**Vagrant gives you reproducible, code-based GUI test VMs on miraclemax in minutes instead of the 30+ minutes of manual ISO installs.**

