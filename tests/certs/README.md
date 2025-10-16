# Red Hat CA Certificates

This directory contains Red Hat internal CA certificates for VPN testing.

## Files

### `2015-RH-IT-Root-CA.pem`
**Purpose:** Red Hat IT Root Certificate Authority  
**Issued:** 2015  
**Type:** Root CA  
**Usage:** Trust Red Hat internal services

### `RH_ITW.crt`
**Purpose:** Red Hat ITW Certificate  
**Type:** Intermediate/Service CA  
**Usage:** Additional trust for Red Hat services

---

## Usage

### Automatic (Vagrant)

Certificates are automatically installed during VM provisioning:

```bash
vagrant up alma9
# Copies certs to /etc/pki/ca-trust/source/anchors/
# Runs update-ca-trust extract
```

### Manual Installation

```bash
# Copy certificates
sudo cp *.pem *.crt /etc/pki/ca-trust/source/anchors/

# Update trust store
sudo update-ca-trust force-enable
sudo update-ca-trust extract

# Verify
curl -I https://gitlab.cee.redhat.com
# Should return HTTP 200/302 without SSL errors
```

---

## Verification

**Check installed certs:**
```bash
ls -la /etc/pki/ca-trust/source/anchors/ | grep -i rh
```

**Test SSL trust:**
```bash
openssl s_client -connect gitlab.cee.redhat.com:443 -CApath /etc/pki/ca-trust/extracted/pem/
# Should show "Verify return code: 0 (ok)"
```

---

## Security Notes

- ✅ Certificates are public keys (safe to commit)
- ✅ No private keys in this directory
- ✅ Standard Red Hat IT distribution
- ⚠️  Only trust for Red Hat internal services

---

*Red Hat CA Certificates for VPN Testing*
