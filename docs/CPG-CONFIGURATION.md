# 📤 Customer Portal Private Groups (CPG) Configuration

## 🎯 Overview

Taminator can automatically post content to Red Hat Customer Portal Private Groups (CPG). This allows TAMs to share agendas, T3 articles, and announcements directly with customers.

**What You Can Post:**
- 📋 TAM call agendas (`tam-generate-agenda --post-cpg`)
- 📰 T3 article recommendations (`tam-t3-reader --post-cpg`)
- 📢 Coverage announcements (`tam-coverage --post-cpg`)

**Note:** CPG integration requires authentication to Red Hat Customer Portal API.

---

## ⚡ Quick Start

### Option 1: Kerberos Authentication (Red Hat Internal - Recommended)

```bash
# Ensure you have a valid Kerberos ticket
kinit jbyrd@REDHAT.COM
klist  # Verify ticket

# Set environment variable (optional)
export CPG_USE_KERBEROS="true"

# Post content
tam-t3-reader --customer jpmc --post-cpg
```

### Option 2: Username/Password Authentication

```bash
# Add to ~/.bashrc or ~/.zshrc
export CPG_USERNAME="jbyrd@redhat.com"
export CPG_PASSWORD="your-password"
export CPG_USE_KERBEROS="false"

# Reload shell
source ~/.bashrc

# Post content
tam-t3-reader --customer jpmc --post-cpg
```

### Option 3: Configuration File (Most Secure)

```bash
# Create config directory
mkdir -p ~/.config/rfe-automation

# Create CPG config
cat > ~/.config/rfe-automation/cpg.conf << 'EOF'
{
  "use_kerberos": true,
  "api_base_url": "https://api.access.redhat.com/rs",
  "sso_url": "https://sso.redhat.com"
}
EOF

# For non-Kerberos:
cat > ~/.config/rfe-automation/cpg.conf << 'EOF'
{
  "use_kerberos": false,
  "username": "jbyrd@redhat.com",
  "password": "your-password",
  "api_base_url": "https://api.access.redhat.com/rs",
  "sso_url": "https://sso.redhat.com"
}
EOF

# Secure the file
chmod 600 ~/.config/rfe-automation/cpg.conf
```

---

## 🔐 Authentication Methods

### Method 1: Kerberos (Recommended for Red Hat TAMs)

**Requirements:**
- Valid Kerberos ticket
- On Red Hat VPN (for internal access)
- `requests-kerberos` Python package

**Setup:**
```bash
# Install Kerberos Python support
pip install requests-kerberos

# Get Kerberos ticket
kinit jbyrd@REDHAT.COM

# Verify ticket
klist

# Should show:
# Ticket cache: KEYRING:persistent:1000:krb_ccache_xxxxxx
# Default principal: jbyrd@REDHAT.COM
```

**Configuration:**
```bash
# Set in ~/.bashrc
export CPG_USE_KERBEROS="true"
```

---

### Method 2: Username/Password

**Requirements:**
- Red Hat Customer Portal account
- Valid credentials

**Configuration:**
```bash
export CPG_USERNAME="jbyrd@redhat.com"
export CPG_PASSWORD="your-password"
export CPG_USE_KERBEROS="false"
```

**Security Note:** Prefer Kerberos or config file over environment variables for password storage.

---

## 🧪 Testing CPG Configuration

### Test 1: Check Authentication

```bash
# For Kerberos
klist
# Should show valid ticket

# For username/password
echo $CPG_USERNAME
# Should show your username
```

### Test 2: Post Test Content

```bash
# Generate test agenda and post to CPG
tam-generate-agenda --customer test --post-cpg

# Check output for:
# ✅ Posted to test's private group  (success)
# ⚠️  CPG posting failed              (failure)
```

### Test 3: Python Test

```bash
cat > /tmp/test-cpg.py << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.cpg_handler import CPGConfig

config = CPGConfig()
print(f"API Base URL: {config.api_base_url}")
print(f"Use Kerberos: {config.use_kerberos}")
print(f"Username: {config.username}")
print(f"\nConfigured: {config.is_configured()}")
EOF

python3 /tmp/test-cpg.py
```

---

## 🛠️ Troubleshooting

### Issue: "CPG not configured"

**Problem:** Authentication not set up

**Solution:**
```bash
# Check Kerberos ticket (if using Kerberos)
klist

# If expired, renew
kinit jbyrd@REDHAT.COM

# Or set username/password
export CPG_USERNAME="jbyrd@redhat.com"
export CPG_PASSWORD="your-password"
export CPG_USE_KERBEROS="false"
```

---

### Issue: "No private groups found"

**Problem:** Customer doesn't have a private group or API access issue

**Solution:**
1. Verify customer has a private group on Customer Portal
2. Check if you have access to the customer's private group
3. Verify customer name/account number is correct

---

### Issue: "Authentication failed"

**Problem:** Invalid credentials or expired Kerberos ticket

**For Kerberos:**
```bash
# Check ticket status
klist

# If expired, renew
kinit jbyrd@REDHAT.COM

# Verify you're on VPN
ping gitlab.cee.redhat.com
```

**For Username/Password:**
```bash
# Verify credentials
echo "Username: $CPG_USERNAME"

# Check if password is set (don't echo it)
[ -z "$CPG_PASSWORD" ] && echo "Password NOT set" || echo "Password set"

# Try logging into Customer Portal manually:
# https://access.redhat.com
```

---

### Issue: "requests-kerberos not found"

**Problem:** Kerberos Python package not installed

**Solution:**
```bash
# Install the package
pip install requests-kerberos

# Or install in user directory
pip install --user requests-kerberos

# Verify installation
python3 -c "import requests_kerberos; print('✅ Installed')"
```

---

### Issue: "Connection refused" or "API error"

**Problem:** Network/VPN/API access issue

**Check:**
1. **VPN:** Must be on Red Hat VPN for internal API
2. **Network:** Check internet connectivity
3. **API Status:** Verify Customer Portal is accessible

**Solution:**
```bash
# Test VPN connection
ping gitlab.cee.redhat.com

# Test Customer Portal API
curl -I https://api.access.redhat.com

# Should return HTTP 200 or 301
```

---

## 📋 Complete Examples

### Example 1: Kerberos Setup (Recommended)

```bash
# Step 1: Install Kerberos support
pip install requests-kerberos

# Step 2: Get Kerberos ticket
kinit jbyrd@REDHAT.COM
# Enter password when prompted

# Step 3: Verify ticket
klist
# Should show valid ticket

# Step 4: Set config (optional)
export CPG_USE_KERBEROS="true"

# Step 5: Test
tam-t3-reader --customer jpmc --post-cpg

# Expected output:
# 📤 Posting 4 articles to CPG...
# ✅ Posted 4 article(s) to jpmc's private group
```

### Example 2: Config File Setup (Most Secure)

```bash
# Create config directory
mkdir -p ~/.config/rfe-automation

# Create CPG config with Kerberos
cat > ~/.config/rfe-automation/cpg.conf << 'EOF'
{
  "use_kerberos": true,
  "api_base_url": "https://api.access.redhat.com/rs",
  "sso_url": "https://sso.redhat.com"
}
EOF

# Secure it
chmod 600 ~/.config/rfe-automation/cpg.conf

# Get Kerberos ticket
kinit jbyrd@REDHAT.COM

# Test
tam-t3-reader --customer jpmc --post-cpg
```

### Example 3: Username/Password Setup

```bash
# Create config file
mkdir -p ~/.config/rfe-automation

cat > ~/.config/rfe-automation/cpg.conf << 'EOF'
{
  "use_kerberos": false,
  "username": "jbyrd@redhat.com",
  "password": "your-password-here",
  "api_base_url": "https://api.access.redhat.com/rs",
  "sso_url": "https://sso.redhat.com"
}
EOF

# Secure it (IMPORTANT!)
chmod 600 ~/.config/rfe-automation/cpg.conf

# Test
tam-coverage --customer jpmc --post-cpg
```

---

## 🎯 Usage Examples

### Post TAM Call Agenda

```bash
# Generate agenda and post to CPG
tam-generate-agenda --customer jpmc --post-cpg

# Expected output:
# 📤 Posting agenda to CPG...
# ✅ Posted to jpmc's private group
```

### Post T3 Articles

```bash
# Get T3 recommendations and post to CPG
tam-t3-reader --customer jpmc --recommend --post-cpg

# Expected output:
# 📤 Posting 4 articles to CPG...
# ✅ Posted 4 article(s) to jpmc's private group
```

### Post Coverage Announcement

```bash
# Generate coverage announcement and post to CPG
tam-coverage --tam "Jimmy Byrd" --tam-email jbyrd@redhat.com \
  --backup "Mike Johnson" --backup-email mjohnson@redhat.com \
  --start 2025-11-04 --end 2025-11-15 --customer jpmc \
  --post-cpg

# Expected output:
# 📤 Posting announcement to CPG...
# ✅ Posted to jpmc's private group
```

---

## 🔒 Security Best Practices

### 1. Prefer Kerberos Over Passwords

```bash
# ✅ DO: Use Kerberos (more secure, no password storage)
kinit jbyrd@REDHAT.COM
export CPG_USE_KERBEROS="true"

# ❌ AVOID: Storing passwords in environment variables
export CPG_PASSWORD="MyPassword123"
```

### 2. Secure Config Files

```bash
# ✅ Config file should be readable only by you
chmod 600 ~/.config/rfe-automation/cpg.conf

# ❌ Never commit passwords to git
# (cpg.conf is already in .gitignore)
```

### 3. Renew Kerberos Tickets Regularly

```bash
# Check ticket expiration
klist

# Renew if needed
kinit jbyrd@REDHAT.COM

# Or set up auto-renewal
# (See: k5start or krenew)
```

### 4. Use VPN for Internal API Access

```bash
# ✅ Connect to Red Hat VPN first
# Then use Kerberos authentication

# ❌ Don't expose internal APIs
# (Customer Portal API is public, but internal endpoints are not)
```

---

## 📊 Configuration Priority

Taminator checks for CPG configuration in this order:

1. **Environment variables** (`CPG_*`)
2. **Config file** (`~/.config/rfe-automation/cpg.conf`)
3. **Alternative config** (`~/.config/pai/cpg.conf`)

**Recommendation:** Use config file with Kerberos for best security.

---

## ⚠️ Important Notes

### API Endpoints

**Note:** The CPG API endpoints in this framework are placeholders. Actual Red Hat Customer Portal API endpoints need to be verified and updated.

**To Update:**
1. Consult Red Hat Customer Portal API documentation
2. Update `foundation/cpg_handler.py` with correct endpoints
3. Test with actual customer private groups

### Customer Private Groups

- Not all customers have private groups
- TAMs must have access to post to customer groups
- Verify customer has enabled private group access

### VPN Requirement

- Kerberos authentication typically requires Red Hat VPN
- Some Customer Portal APIs may be accessible without VPN
- Check your network requirements

---

## 📞 Need Help?

### Still Having Issues?

1. **Check Kerberos:** Ensure valid ticket with `klist`
2. **Check VPN:** Verify connection to Red Hat network
3. **Check API:** Verify Customer Portal is accessible
4. **Check Customer:** Confirm customer has private group
5. **Ask for help:** Slack #tam-automation

### Common Solutions

| Problem | Solution |
|---------|----------|
| Not configured | Get Kerberos ticket or set username/password |
| Authentication failed | Renew Kerberos ticket or check credentials |
| No private groups | Verify customer has CPG enabled |
| Connection refused | Check VPN connection |
| Package not found | Install requests-kerberos |

---

## ✅ Verification Checklist

Before using CPG in production:

- [ ] Authentication configured (Kerberos OR username/password)
- [ ] Kerberos ticket valid (if using Kerberos)
- [ ] Config file secured (`chmod 600`)
- [ ] Test post successful
- [ ] Customer private group verified
- [ ] VPN connected (for internal API)

---

**"I'll be back"** — with content posted to your customer portal! 📤🤖

*Taminator CPG Configuration Guide*  
*Terminate manual portal posting*


