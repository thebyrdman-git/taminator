# RFE Automation Tool - VM Testing Guide

## Overview

Your RFE automation tool is now installed on both test VMs with **pre-bundled offline support** (no VPN required).

## VMs Ready for Testing

| VM | OS | GUI | Installer | Status |
|----|----|----|-----------|--------|
| **alma9** | AlmaLinux 9 | ✅ GNOME | ✅ Installed | Ready |
| **fedora41** | Fedora 41 | ⚠️ Minimal | ✅ Ready | Needs GUI |

## Quick Access

### AlmaLinux 9 (Recommended - Full GUI)

```bash
# From your local workstation
virt-viewer --connect qemu+ssh://jbyrd@192.168.1.34/system tests_alma9

# Login: testuser / testpass
# Already installed and working!
```

### Fedora 41 (Needs GUI First)

```bash
# Install GNOME desktop first
cd /home/jbyrd/pai/rfe-automation-clean/tests
vagrant ssh fedora41 -c "sudo dnf groupinstall -y 'Fedora Workstation' && sudo reboot"

# Wait 60 seconds, then access
virt-viewer --connect qemu+ssh://jbyrd@192.168.1.34/system tests_fedora41
```

## Testing the RFE Installer (Already Done on alma9!)

The **offline installer** has already been successfully tested on alma9:

```bash
cd ~/rfe-and-bug-tracker-automation
./install-offline.sh
```

**Results:**
- ✅ Platform detected correctly (RHEL)
- ✅ Found pre-bundled rhcase (no VPN required)
- ✅ Installed via pip with virtual environment
- ✅ Created activation scripts

**To use the installed tool:**
```bash
cd ~/rfe-and-bug-tracker-automation
source .venv/bin/activate
./bin/tam-rfe-chat
```

## Testing Cursor IDE

Now that the RFE installer works, test Cursor:

1. **Access the GUI** (virt-viewer command above)
2. **Open Firefox/browser** in the VM
3. **Download Cursor**: https://cursor.sh
4. **Install and test** the IDE

## What's Included

### Offline Installer (`install-offline.sh`)
- Pre-bundled with `rhcase` - no GitLab/VPN required
- Works completely offline
- User-space installation (no sudo needed)
- Creates virtual environment automatically

### Regular Installer (`install-improved.sh`)
- Clones rhcase from GitLab (requires VPN)
- Auto-updates to latest version
- Falls back to pip if UV fails

## File Locations in VMs

```
/home/testuser/rfe-and-bug-tracker-automation/
├── install-offline.sh          # Offline installer (bundled rhcase)
├── install-improved.sh         # Online installer (requires VPN)
├── rhcase/                     # Pre-bundled rhcase package
├── bin/                        # Tools and scripts
├── .venv/                      # Python virtual environment (after install)
├── activate-rfe                # Quick activation script
└── log-offline.out             # Installation log (alma9)
```

## Vagrant Snapshot Workflow

**Take snapshots before testing:**
```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests
vagrant snapshot save alma9 clean-with-rfe
vagrant snapshot save fedora41 clean-install
```

**After testing, restore to clean state:**
```bash
vagrant snapshot restore alma9 clean-with-rfe
vagrant snapshot restore fedora41 clean-install
```

**Test again with fresh environment:**
```bash
# The snapshot includes the bundled installer, so you can re-test quickly
vagrant snapshot restore alma9 clean-with-rfe
# Access GUI and test again
```

## Troubleshooting

### Can't see GUI in virt-viewer
- Make sure GDM is running: `sudo systemctl status gdm`
- Reboot the VM if needed: `vagrant reload alma9`

### Installation fails
- Check logs: `cat /tmp/rfe-*.log`
- Verify Python 3.8+: `python3 --version`
- Check rhcase exists: `ls -la ~/rfe-and-bug-tracker-automation/rhcase/`

### Permission denied errors
```bash
# Fix permissions
sudo chmod 755 /home/testuser
sudo chmod -R u+rwX /home/testuser/rfe-and-bug-tracker-automation
sudo chown -R testuser:testuser /home/testuser/rfe-and-bug-tracker-automation
```

## What's Been Tested

✅ **Platform detection** - Correctly identifies RHEL/AlmaLinux
✅ **Offline mode** - Pre-bundled rhcase works without VPN
✅ **Virtual environment** - pip+venv installation successful
✅ **User-space install** - No sudo required
✅ **Activation scripts** - Helper scripts created

## Next Steps

1. ✅ **RFE Installer** - Tested and working on alma9
2. 🎯 **Cursor IDE** - Test installation and functionality
3. 📸 **Take snapshots** - Save clean states for repeated testing
4. 🔄 **Iterate** - Use snapshots to quickly reset and re-test

## Summary

Both VMs have the **offline-capable** RFE automation tool ready:
- **alma9**: Fully installed and working (GUI ready)
- **fedora41**: Bundled and ready (needs GUI install)

The offline installer successfully bypasses VPN/GitLab requirements by including a pre-bundled copy of `rhcase`. You can now test both the RFE tool and Cursor IDE in isolated VM environments.

