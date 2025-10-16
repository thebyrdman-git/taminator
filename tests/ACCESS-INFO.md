# Test VM Access Information

## Created VMs

Both VMs are running on **miraclemax** (`192.168.1.34`) with full GNOME desktop environments:

| VM Name   | OS                      | Status  | User      | Password   | Desktop |
|-----------|-------------------------|---------|-----------|------------|---------|
| fedora41  | Fedora 41 Workstation   | Running | testuser  | testpass   | GNOME   |
| alma9     | AlmaLinux 9 Workstation | Running | testuser  | testpass   | GNOME   |

## Access Methods

### Method 1: virt-manager (Recommended)
From your **local workstation** (fedora-workstation):

```bash
# Open virt-manager
sudo virt-manager &

# Add connection to miraclemax:
# File -> Add Connection
#   - Hypervisor: QEMU/KVM
#   - Connect to remote host over SSH: checked
#   - Username: jbyrd
#   - Hostname: 192.168.1.34

# Double-click VMs in the list to access their consoles
```

### Method 2: virt-viewer (Direct Console)
From your **local workstation**:

```bash
# For Fedora 41
virt-viewer --connect qemu+ssh://jbyrd@192.168.1.34/system tests_fedora41 &

# For AlmaLinux 9
virt-viewer --connect qemu+ssh://jbyrd@192.168.1.34/system tests_alma9 &
```

### Method 3: SSH (Command-line access)
```bash
# SSH via Vagrant
vagrant ssh fedora41
vagrant ssh alma9

# Or get IP addresses for direct SSH
vagrant ssh fedora41 -- ip a
vagrant ssh alma9 -- ip a

# Then SSH directly as testuser
ssh testuser@<VM_IP>
```

## Vagrant Management

From your **local workstation** in `/home/jbyrd/pai/rfe-automation-clean/tests`:

```bash
# Check status
vagrant status

# SSH into VMs
vagrant ssh fedora41
vagrant ssh alma9

# Take snapshots before testing (HIGHLY RECOMMENDED)
vagrant snapshot save fedora41 clean-install
vagrant snapshot save alma9 clean-install

# Restore after testing
vagrant snapshot restore fedora41 clean-install
vagrant snapshot restore alma9 clean-install

# Shutdown
vagrant halt fedora41 alma9

# Start VMs
vagrant up fedora41 alma9

# Delete VMs
vagrant destroy -f fedora41 alma9
```

## Testing Workflow

### 1. Take Snapshots First (Important!)
```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests
vagrant snapshot save fedora41 clean-install
vagrant snapshot save alma9 clean-install
```

### 2. Access GUI Console
Use `virt-viewer` or `virt-manager` to access the graphical desktop.

### 3. Test RFE Installer
Login to the VM console as **testuser / testpass**, open Terminal:

```bash
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation
./install-improved.sh
```

### 4. Test Cursor IDE Install
In the same GUI session, follow Cursor's installation steps (download AppImage or use their installer).

### 5. Restore to Clean State
After testing, restore the snapshot:

```bash
vagrant snapshot restore fedora41 clean-install
vagrant snapshot restore alma9 clean-install
```

## Current Status

✅ **fedora41**: Fedora 41 with git installed (minimal GUI - can install full Workstation if needed)
✅ **alma9**: AlmaLinux 9 with full GNOME Workstation and git installed

Both VMs are ready for testing your RFE automation installer and Cursor IDE.

## Network Configuration

- **VMs use NAT networking** via libvirt's default network
- **DHCP range**: 192.168.121.0/24
- **Host access**: VMs can reach internet and miraclemax
- **Inter-VM**: VMs can communicate with each other
- **VNC Port**: Automatically assigned (check `vagrant ssh-config`)

## VM Details:

| VM Name         | OS                      | RAM  | CPUs | Disk | GUI     |
|-----------------|-------------------------|------|------|------|---------|
| `tests_fedora41`| Fedora 41 Cloud Base    | 4GB  | 2    | 50GB | Minimal |
| `tests_alma9`   | AlmaLinux 9 Workstation | 4GB  | 2    | 50GB | GNOME   |

**Note**: Fedora VM uses minimal cloud base. To install full GNOME desktop:
```bash
vagrant ssh fedora41
sudo dnf groupinstall -y "Fedora Workstation"
sudo reboot
```

## Performance Notes
- **Graphics**: VNC (compatible with virt-viewer and virt-manager)
- **Disk**: 50GB thin provisioned (grows as needed)
- **Network**: NAT with DHCP (192.168.121.0/24)

