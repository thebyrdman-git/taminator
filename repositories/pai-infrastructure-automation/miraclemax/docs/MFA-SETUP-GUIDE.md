# Multi-Factor Authentication Setup Guide
## Authelia Integration with Traefik

### 🔐 **Overview**

Authelia provides multi-factor authentication for all miraclemax services including:
- **TOTP (Time-based One-Time Password)** - Compatible with any RFC 6238 compliant app:
  - ✅ FreeOTP (Open Source)
  - ✅ Google Authenticator
  - ✅ Microsoft Authenticator
  - ✅ Authy
  - ✅ 1Password
  - ✅ Bitwarden
  - ✅ Any other TOTP app
- **WebAuthn** (Hardware Security Keys & Biometrics):
  - YubiKey
  - TouchID
  - Windows Hello
  - Android Fingerprint
- Session management with configurable timeouts

### 🌐 **Protected Services**

All services require two-factor authentication:
- **Traefik Dashboard**: https://traefik.jbyrd.org
- **Home Assistant**: https://ha.jbyrd.org
- **Actual Budget**: https://budget.jbyrd.org
- **n8n Workflows**: https://n8n.jbyrd.org
- **cAdvisor**: https://cadvisor.jbyrd.org
- **Prometheus**: https://metrics.jbyrd.org

### 📱 **Initial Setup**

1. **Access Authelia Portal**: https://auth.jbyrd.org
2. **Login Credentials**:
   - Username: `jbyrd`
   - Password: `TempPass123!` (change immediately after first login)
3. **Configure TOTP** (choose any app):
   
   **Option A: FreeOTP (Recommended - Open Source)**
   - Install FreeOTP from [F-Droid](https://f-droid.org/packages/org.fedorahosted.freeotp/) or Play Store
   - Tap "+" to add new token
   - Scan QR code from Authelia
   - Enter generated 6-digit code to verify
   
   **Option B: Other TOTP Apps**
   - Open your preferred authenticator app
   - Scan QR code displayed by Authelia
   - Enter 6-digit verification code
   
   **Manual Entry** (if QR scan fails):
   - Issuer: `miraclemax.jbyrd.org`
   - Algorithm: SHA1
   - Digits: 6
   - Period: 30 seconds
   
4. **Optional: Register Security Key**:
   - Insert YubiKey or use biometric device
   - Follow WebAuthn registration flow

### 🔄 **Authentication Flow**

1. Visit protected service (e.g., https://budget.jbyrd.org)
2. Redirected to Authelia login portal
3. Enter username and password
4. Provide second factor (TOTP or WebAuthn)
5. Authenticated and redirected to service

### ⏱️ **Session Configuration**

- **Session Expiration**: 1 hour of activity
- **Inactivity Timeout**: 15 minutes
- **Remember Me**: 1 month (optional)

### 🛡️ **Security Features**

- **Rate Limiting**: 5 failed attempts in 10 minutes = 15 minute ban
- **IP Whitelisting**: Internal network bypass available
- **Audit Logging**: All authentication attempts logged
- **Password Policy**: Argon2id hashing

### 🔧 **Password Reset**

1. Visit https://auth.jbyrd.org
2. Click "Forgot Password?"
3. Check `/config/notifications.txt` for reset link (filesystem notifier)
4. Follow link to set new password

### 📊 **Monitoring**

- **Logs**: `ssh jbyrd@192.168.1.34 'sudo podman logs authelia'`
- **Status**: Check Traefik dashboard for Authelia health
- **Database**: SQLite at `~/miraclemax-infrastructure/config/authelia/db.sqlite3`

### 🚨 **Troubleshooting**

**Issue**: Can't access Authelia portal
- **Fix**: Verify Authelia container running: `sudo podman ps | grep authelia`

**Issue**: TOTP code not working
- **Fix**: Ensure device time is synchronized (NTP)

**Issue**: Locked out after failed attempts
- **Wait**: 15 minutes, or clear bans: `rm ~/miraclemax-infrastructure/config/authelia/db.sqlite3`

### 🔄 **Changing Default Password**

**IMPORTANT**: Change the default password immediately:

```bash
# On miraclemax
ssh jbyrd@192.168.1.34

# Generate new password hash
sudo podman run --rm docker.io/authelia/authelia:4.38.10 \
  authelia crypto hash generate argon2 --password "YOUR_NEW_PASSWORD"

# Copy the hash starting with $argon2id...
# Edit users file
nano ~/miraclemax-infrastructure/config/authelia/users.yml

# Replace the password hash
# Restart Authelia
sudo podman restart authelia
```

### 🎯 **Next Steps**

1. ✅ Change default password
2. ✅ Set up TOTP on your phone
3. ✅ Test logging into all services
4. ⚙️ Optional: Configure email notifications (replace filesystem notifier)
5. 🔐 Optional: Register hardware security key (YubiKey)

---

**Status**: ✅ Deployed and Operational
**Version**: Authelia 4.38.10
**Deployment Date**: 2025-10-12

