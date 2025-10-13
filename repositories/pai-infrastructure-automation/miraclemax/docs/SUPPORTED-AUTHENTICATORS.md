# Supported Authenticator Apps
## Complete Compatibility List for Authelia TOTP

### ✅ **Fully Tested & Supported**

#### **Open Source** (Recommended)
1. **FreeOTP** 
   - Platform: Android, iOS
   - Source: [GitHub - FreeOTP](https://github.com/freeotp)
   - Install: [F-Droid](https://f-droid.org/packages/org.fedorahosted.freeotp/), Play Store, App Store
   - Features: Offline, no account required, open source
   - ✅ **Best for privacy-conscious users**

2. **Aegis Authenticator**
   - Platform: Android only
   - Source: [GitHub - Aegis](https://github.com/beemdevelopment/Aegis)
   - Install: [F-Droid](https://f-droid.org/packages/com.beemdevelopment.aegis/), Play Store
   - Features: Encrypted backups, biometric unlock, offline

3. **andOTP** (Deprecated, use Aegis)
   - Replaced by Aegis Authenticator

#### **Commercial / Proprietary**
4. **Google Authenticator**
   - Platform: Android, iOS
   - Features: Simple, widely known
   - Note: No backup feature (codes lost if phone lost)

5. **Microsoft Authenticator**
   - Platform: Android, iOS, Windows
   - Features: Cloud backup, push notifications

6. **Authy**
   - Platform: Android, iOS, Desktop (Windows, Mac, Linux)
   - Features: Multi-device sync, cloud backup
   - Note: Requires phone number

7. **1Password**
   - Platform: All platforms
   - Features: Password manager + TOTP
   - Note: Requires subscription

8. **Bitwarden**
   - Platform: All platforms
   - Features: Password manager + TOTP (Premium feature)

9. **LastPass Authenticator**
   - Platform: Android, iOS
   - Features: Cloud backup

10. **Duo Mobile**
    - Platform: Android, iOS
    - Features: Push notifications, TOTP

### 🔧 **Technical Specifications**

All compatible authenticators must support:
```yaml
Standard: RFC 6238 (TOTP)
Algorithm: SHA1 (for maximum compatibility)
Digits: 6
Period: 30 seconds
```

### 📱 **Setup Instructions**

#### **For FreeOTP:**
1. Install FreeOTP from F-Droid or app store
2. Open FreeOTP
3. Tap "+" or QR code icon
4. Point camera at QR code from Authelia
5. Token automatically added
6. Tap token to generate code

**Manual Entry in FreeOTP:**
1. Tap "+" → Enter key manually
2. **Issuer**: miraclemax.jbyrd.org
3. **Username**: jbyrd
4. **Secret Key**: (from Authelia setup page)
5. **Type**: Time-based (TOTP)
6. **Algorithm**: SHA1
7. **Interval**: 30
8. **Digits**: 6

#### **For Other Apps:**
Most apps follow similar flow:
1. Open app → Add new token
2. Scan QR code OR enter manually
3. Verify with generated 6-digit code

### 🛡️ **Hardware Security Keys (WebAuthn)**

Also supported as second factor:
- **YubiKey** (5 Series, Security Key Series)
- **Titan Security Key** (Google)
- **Thetis FIDO2**
- **SoloKeys**
- **Nitrokey FIDO2**
- **Platform authenticators**:
  - Touch ID (macOS/iOS)
  - Windows Hello
  - Android Fingerprint

### 🔄 **Backup Recommendations**

**Best Practice - 2FA Backup Strategy:**
1. **Primary**: FreeOTP on phone
2. **Backup**: Export QR code during setup and store securely
3. **Recovery**: Keep recovery codes in password manager

**Alternative Multi-Device Setup:**
- Use Authy for cross-device sync
- Or save QR code to add to multiple devices

### ❌ **Not Supported**

- SMS-based authentication (not secure)
- Email-based codes (configured as filesystem for now)
- Proprietary non-standard OTP implementations

### 📊 **Comparison Matrix**

| App | Open Source | Backup | Multi-Device | Offline | Biometric Lock |
|-----|-------------|--------|--------------|---------|----------------|
| **FreeOTP** | ✅ | Manual | ❌ | ✅ | ❌ |
| **Aegis** | ✅ | Encrypted | ❌ | ✅ | ✅ |
| **Google Auth** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **MS Auth** | ❌ | Cloud | ✅ | ✅ | ✅ |
| **Authy** | ❌ | Cloud | ✅ | ✅ | ✅ |
| **1Password** | ❌ | Cloud | ✅ | ✅ | ✅ |
| **Bitwarden** | ✅ | Cloud | ✅ | ✅ | ✅ |

### 🎯 **Recommendation**

**For personal use**: **FreeOTP** or **Aegis**
- Open source, auditable code
- No account/phone number required
- Complete privacy
- Works offline

**For convenience**: **Authy** or **Microsoft Authenticator**
- Cross-device sync
- Cloud backup
- Multi-platform support

**For integration**: **Bitwarden** or **1Password**
- Combined with password manager
- Centralized security management
- Family sharing features

---

**All apps listed work with Authelia's TOTP implementation** - choose based on your privacy, backup, and convenience preferences.

