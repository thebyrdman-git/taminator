# COPR Repository Support Matrix

**Repository:** `@endpoint-systems-sysadmins/unsupported-fedora-packages`  
**URL:** https://copr.devel.redhat.com/coprs/g/endpoint-systems-sysadmins/unsupported-fedora-packages/

## Supported Distributions

### RHEL-Based (EPEL)

| Distribution | Version | COPR Release | Status | Notes |
|--------------|---------|--------------|--------|-------|
| **RHEL** | 8 | epel-8 | ✅ Supported | NetworkManager-openvpn available |
| **RHEL** | 9 | epel-9 | ✅ Supported | Primary target for RFE tools |
| **RHEL** | 10 | epel-10 | ✅ Supported | Beta/preview |
| **Alma Linux** | 8 | epel-8 | ✅ Supported | Uses EPEL 8 packages |
| **Alma Linux** | 9 | epel-9 | ✅ Supported | **Default for VPN testing** |
| **Rocky Linux** | 8 | epel-8 | ✅ Supported | Uses EPEL 8 packages |
| **Rocky Linux** | 9 | epel-9 | ✅ Supported | Compatible with Alma 9 |

### Fedora

| Distribution | Version | COPR Release | Status | Notes |
|--------------|---------|--------------|--------|-------|
| **Fedora** | 40 | fedora-40 | ✅ Supported | Stable |
| **Fedora** | 41 | fedora-41 | ✅ Supported | Current stable |
| **Fedora** | 42 | fedora-42 | ✅ Supported | Beta/testing |
| **Fedora** | 43 | fedora-43 | ✅ Supported | Beta/testing |
| **Fedora** | rawhide | fedora-rawhide | ⚠️  Unstable | Development branch |

## Dynamic Detection

The Vagrantfile and setup scripts automatically detect the OS and enable the appropriate COPR release:

```bash
# Detection logic
case "$ID" in
  rhel|almalinux|rocky)
    COPR_RELEASE="epel-${VERSION_ID%%.*}"
    ;;
  fedora)
    COPR_RELEASE="fedora-${VERSION_ID}"
    ;;
esac
```

**Example outputs:**
- Alma Linux 9.4 → `epel-9`
- Fedora 41 → `fedora-41`
- RHEL 8.9 → `epel-8`

## Usage

### Automatic (Vagrant)

```bash
vagrant up alma9
# Detects OS, enables correct COPR release
```

### Manual Installation

```bash
# Run dynamic setup script
cd tests/scripts
sudo ./setup-vpn-packages.sh
```

### Manual (Step-by-Step)

```bash
# 1. Detect your OS
. /etc/os-release
echo "OS: $ID $VERSION_ID"

# 2. Enable COPR (automatically uses correct release)
sudo dnf install -y 'dnf-command(copr)'
sudo dnf copr enable -y copr.devel.redhat.com/@endpoint-systems-sysadmins/unsupported-fedora-packages

# 3. Install VPN packages
sudo dnf install -y NetworkManager-openvpn openvpn
```

## Fallback Strategy

If COPR repo doesn't have packages for your OS:

1. **Try standard repos:** VPN packages may be available in default repos
2. **Manual VPN setup:** Download OpenVPN client directly
3. **Alternative method:** Use different VPN client (e.g., openconnect)

## Package Availability

**Primary package:** `NetworkManager-openvpn`

Check availability for your release:
```bash
dnf copr enable -y copr.devel.redhat.com/@endpoint-systems-sysadmins/unsupported-fedora-packages
dnf search NetworkManager-openvpn
```

## Troubleshooting

### COPR repo not available for my version

```bash
❌ Error: This repository does not provide any version for epel-7
```

**Solution:** Your OS version is not supported. Use manual VPN setup or upgrade OS.

### Package not found after enabling COPR

```bash
❌ No match for argument: NetworkManager-openvpn
```

**Solution:** Check if packages exist for your release at COPR URL above.

### Vagrantfile provision fails

Check provisioning logs:
```bash
vagrant up alma9 --provision 2>&1 | grep -A 10 "VPN"
```

## Testing Different Distributions

```ruby
# In Vagrantfile, change:
config.vm.box = "almalinux/9"      # Alma 9 (epel-9)
config.vm.box = "generic/rhel8"    # RHEL 8 (epel-8)
config.vm.box = "fedora/41-cloud"  # Fedora 41 (fedora-41)
```

Each will automatically use the correct COPR release.

## Reference

**COPR Repository Page:**  
https://copr.devel.redhat.com/coprs/g/endpoint-systems-sysadmins/unsupported-fedora-packages/

**Supported Architectures:**
- x86_64 (all distributions)
- aarch64 (EPEL 10, Fedora 40/41/42)

---

*COPR Support Matrix for RFE VPN Testing*  
*Auto-detection ensures correct packages for your distribution*
