# Red Hat VPN Setup for RFE Testing

## Overview

This guide configures the Alma Linux 9 VM with Red Hat VPN access to test the online installation method that clones directly from GitLab CEE.

## Prerequisites

- ✅ Vagrant installed (`sudo dnf install vagrant`)
- ✅ vagrant-libvirt plugin (`vagrant plugin install vagrant-libvirt`)
- ✅ Red Hat VPN credentials
- ✅ VPN guide: `~/Downloads/KB0005449 - OpenVPN User Guide.pdf`

## Quick Start

```bash
cd /home/jbyrd/pai/rfe-bug-tracker-automation/tests
./setup-vpn-testing.sh
```

## Manual Setup Steps

### 1. Start the VM

```bash
cd /home/jbyrd/pai/rfe-bug-tracker-automation/tests
vagrant up alma9
```

### 2. Obtain VPN Configuration

**Option A: Red Hat Self-Service Portal**
1. Go to: https://access.redhat.com/management/vpn
2. Download your OpenVPN profile (`.ovpn` file)
3. Save to a known location

**Option B: IT Knowledge Base**
- Reference: `KB0005449 - OpenVPN User Guide`
- Location: `~/Downloads/KB0005449 - OpenVPN User Guide.pdf`
- Follow instructions to download your specific VPN profile

### 3. SSH into the VM

```bash
vagrant ssh alma9
```

### 4. Configure VPN in the VM

The VM is pre-configured with:
- ✅ NetworkManager-openvpn
- ✅ openvpn client
- ✅ Kerberos workstation tools
- ✅ Red Hat CA certificates

**Transfer VPN config:**

From your workstation (in a new terminal):
```bash
# Find the VM IP
cd /home/jbyrd/pai/rfe-bug-tracker-automation/tests
vagrant ssh-config alma9 | grep HostName

# Copy VPN file to VM
vagrant scp /path/to/your/redhat-profile.ovpn alma9:/tmp/
```

Inside the VM:
```bash
# Import VPN connection
sudo nmcli connection import type openvpn file /tmp/redhat-profile.ovpn

# Connect to VPN
sudo nmcli connection up redhat-profile

# Verify connection
curl -I https://gitlab.cee.redhat.com
```

### 5. Test Kerberos Authentication

```bash
# Inside VM
kinit jbyrd@REDHAT.COM

# Verify ticket
klist

# Test GitLab access
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
```

### 6. Run Online Installation Test

```bash
# Inside VM, on VPN
cd rfe-and-bug-tracker-automation

# Time the online installation
time ./install.sh

# Verify installation
ls -lh bin/tam-rfe-*
./bin/tam-rfe-hydra-api --help
```

## Expected Results

### Installation Timeline (Online)
- Git clone from GitLab: ~5-10 seconds
- Submodule initialization: ~5-10 seconds
- rhcase installation: ~20-30 seconds
- **Total**: ~40-50 seconds (with network)

### Comparison
| Method | Time | Requirements |
|--------|------|--------------|
| **Offline** | 18 seconds | None (bundled) |
| **Online** | 40-50 seconds | VPN + GitLab access |

## Troubleshooting

### VPN Connection Issues

**Problem:** `curl: (6) Could not resolve host: gitlab.cee.redhat.com`
```bash
# Check VPN status
nmcli connection show --active

# Reconnect VPN
sudo nmcli connection down redhat-profile
sudo nmcli connection up redhat-profile

# Check DNS
cat /etc/resolv.conf
```

**Problem:** `SSL certificate problem: self-signed certificate`
```bash
# Update CA trust
sudo update-ca-trust force-enable
sudo update-ca-trust extract
```

### Git/GitLab Access Issues

**Problem:** `fatal: unable to access 'https://gitlab.cee.redhat.com/'`
```bash
# Verify VPN is connected
nmcli connection show --active | grep redhat

# Test network access
curl -v https://gitlab.cee.redhat.com 2>&1 | head -20

# Check Kerberos ticket
klist
```

### Installation Issues

**Problem:** `rhcase` installation fails
```bash
# Ensure you're on VPN
nmcli connection show --active

# Try manual clone of rhcase submodule
cd rfe-and-bug-tracker-automation
git submodule update --init --recursive

# Retry installation
./install.sh
```

## VM Management

```bash
# Check VM status
vagrant status alma9

# SSH into VM
vagrant ssh alma9

# Stop VM
vagrant halt alma9

# Restart VM
vagrant up alma9

# Destroy VM (clean slate)
vagrant destroy alma9
```

## Security Notes

- ✅ VPN credentials stored securely (not in Git)
- ✅ VM uses NAT networking (isolated)
- ✅ VPN disconnects when VM is halted
- ✅ Kerberos tickets expire (default 24h)

## Reference Documentation

- **VPN Guide**: `~/Downloads/KB0005449 - OpenVPN User Guide.pdf`
- **Red Hat VPN Portal**: https://access.redhat.com/management/vpn
- **GitLab CEE**: https://gitlab.cee.redhat.com
- **Kerberos Setup**: https://source.redhat.com/departments/it/identity-access-management

---

*VPN Setup Guide for RFE Bug Tracker Automation*  
*Testing Online Installation with GitLab CEE Access*


## Additional Setup Notes

### COPR Repository (Included in VM)

The Alma 9 VM automatically configures the Red Hat COPR repository for VPN packages during provisioning:

```bash
sudo dnf copr enable copr.devel.redhat.com/@endpoint-systems-sysadmins/unsupported-fedora-packages
```

This provides NetworkManager-openvpn and related packages. The Vagrantfile handles this automatically, but if you're setting up VPN on a different system, you'll need to enable this repo first.

### Manual COPR Setup (if needed)

If setting up VPN on a non-VM system:

```bash
# Install COPR plugin
sudo dnf install -y 'dnf-command(copr)'

# Enable VPN packages repo
sudo dnf copr enable -y copr.devel.redhat.com/@endpoint-systems-sysadmins/unsupported-fedora-packages

# Install VPN tools
sudo dnf install -y NetworkManager-openvpn openvpn
```

