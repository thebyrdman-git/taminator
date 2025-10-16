# Test Configuration Files

This directory contains configuration templates for Red Hat VPN testing.

## Files

### `krb5.conf.template`
**Purpose:** Kerberos realm configuration for Red Hat  
**Source:** Red Hat IT standard configuration  
**Usage:** Automatically deployed to VMs during provisioning

**Realms configured:**
- `REDHAT.COM` - Legacy Red Hat realm
- `IPA.REDHAT.COM` - Identity Management realm

**Features:**
- DNS-based KDC discovery
- 24-hour ticket lifetime
- Forwardable tickets
- Proper auth_to_local mapping

**Reference:** https://mojo.redhat.com/docs/DOC-1166841

---

## Deployment

These configs are automatically deployed by Vagrant:

```bash
vagrant up alma9
# Copies krb5.conf to /etc/krb5.conf
# Installs Red Hat CA certificates
# Configures Git for GitLab SSH
```

---

## Manual Deployment

If setting up a non-VM system:

```bash
# Copy Kerberos config
sudo cp krb5.conf.template /etc/krb5.conf

# Install CA certificates
sudo cp ../certs/*.pem /etc/pki/ca-trust/source/anchors/
sudo cp ../certs/*.crt /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust extract

# Test Kerberos
kinit jbyrd@REDHAT.COM
klist
```

---

*Test Configuration for RFE VPN Testing*
