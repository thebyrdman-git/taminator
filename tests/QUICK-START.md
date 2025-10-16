# Quick Start: Testing RFE Installer with Vagrant

## ✅ Setup Complete!

You now have Vagrant configured to create GUI test VMs on miraclemax.

---

## Create Test VMs

### Option 1: Create Fedora 42 VM
```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests

# Create and provision VM (10-15 minutes)
vagrant up fedora42

# Check status
vagrant status fedora42
```

### Option 2: Create RHEL 9.6 VM
```bash
vagrant up rhel96
```

### Create Both VMs
```bash
vagrant up
```

---

## Access the GUI

### From miraclemax (Easiest)
```bash
# SSH to miraclemax
ssh jbyrd@192.168.1.34

# Launch virt-manager
sudo virt-manager
# Double-click the VM: rfe-test-fedora42 or rfe-test-rhel96
```

### From Your Laptop (X11 Forwarding)
```bash
# Enable X11 forwarding
ssh -X jbyrd@192.168.1.34

# View VM
virt-viewer rfe-test-fedora42
```

---

## Login to VM

- **Username**: `testuser`
- **Password**: `testpass`

---

## Test RFE Installer

Once logged into the VM GUI, open Terminal:

```bash
# Clone the repo
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation

# Run installer
./install-improved.sh

# Verify
./bin/tam-rfe-chat --help
rhcase --version
```

---

## Manage VMs

```bash
# Stop VM
vagrant halt fedora42

# Start VM
vagrant up fedora42

# Restart VM
vagrant reload fedora42

# Delete VM
vagrant destroy -f fedora42

# SSH to VM (console only)
vagrant ssh fedora42
```

---

## Snapshots

### Save Clean State
```bash
# After OS install, before RFE install
vagrant snapshot save fedora42 clean-os

# After successful RFE install
vagrant snapshot save fedora42 post-install
```

### Restore
```bash
vagrant snapshot restore fedora42 clean-os
```

### List Snapshots
```bash
vagrant snapshot list fedora42
```

---

## Testing Workflow

1. **Create VM**: `vagrant up fedora42`
2. **Access GUI**: `ssh jbyrd@192.168.1.34`, then `sudo virt-manager`
3. **Login**: testuser / testpass
4. **Take Snapshot**: `vagrant snapshot save fedora42 clean-os`
5. **Test Installer**: Clone repo, run `./install-improved.sh`
6. **Document Results**: Note installation method, time, errors
7. **Reset for Retest**: `vagrant snapshot restore fedora42 clean-os`
8. **Cleanup**: `vagrant destroy -f fedora42`

---

## Troubleshooting

### VM Won't Start
```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests
vagrant up fedora42 --debug
```

### Check VM on miraclemax
```bash
ssh jbyrd@192.168.1.34
sudo virsh list --all
sudo virsh console rfe-test-fedora42
```

### Network Issues
```bash
# On miraclemax
sudo virsh net-list
sudo virsh net-start default
```

### Re-provision VM
```bash
vagrant provision fedora42
```

---

**Ready to test!** Just run `vagrant up fedora42` to create your first test VM.

