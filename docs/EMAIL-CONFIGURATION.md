# 📧 Email Configuration Guide

## 🎯 Overview

Taminator can automatically email reports, agendas, and announcements. This guide shows you how to configure SMTP email delivery.

**What You Can Email:**
- 📋 TAM call agendas (`tam-generate-agenda --email`)
- 🧹 Backlog cleanup reports (`tam-backlog-cleanup --email`)
- 📰 T3 article recommendations (`tam-t3-reader --email`)
- 📢 Coverage announcements (`tam-coverage --email`)

---

## ⚡ Quick Start

### Option 1: Environment Variables (Easiest)

```bash
# Add to ~/.bashrc or ~/.zshrc
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export SMTP_FROM_NAME="Red Hat TAM"
export SMTP_USE_TLS="true"

# Reload shell
source ~/.bashrc
```

### Option 2: Configuration File (Recommended)

```bash
# Create config directory
mkdir -p ~/.config/rfe-automation

# Create email config
cat > ~/.config/rfe-automation/email.conf << 'EOF'
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "your-email@gmail.com",
  "smtp_password": "your-app-password",
  "from_name": "Red Hat TAM",
  "use_tls": true
}
EOF

# Secure the file (contains password)
chmod 600 ~/.config/rfe-automation/email.conf
```

---

## 🔐 SMTP Providers

### Gmail (Personal or @gmail.com)

**Requirements:**
- Gmail account
- App Password (not your regular password)

**Setup App Password:**
1. Go to: https://myaccount.google.com/security
2. Enable 2-Factor Authentication (required)
3. Go to: https://myaccount.google.com/apppasswords
4. Create app password for "Mail"
5. Copy the 16-character password

**Configuration:**
```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="yourname@gmail.com"
export SMTP_PASSWORD="your-16-char-app-password"
export SMTP_FROM_NAME="Red Hat TAM"
export SMTP_USE_TLS="true"
```

**Example:**
```bash
# With app password: jbsr jwdt aqeq sueq
export SMTP_USER="jimmykbyrd@gmail.com"
export SMTP_PASSWORD="jbsr jwdt aqeq sueq"
```

---

### Red Hat Email (@redhat.com)

**Option A: Internal SMTP (On VPN)**

```bash
export SMTP_SERVER="smtp.corp.redhat.com"
export SMTP_PORT="25"
export SMTP_USER="jbyrd@redhat.com"
export SMTP_PASSWORD=""  # Kerberos auth (no password needed)
export SMTP_FROM_NAME="Red Hat TAM"
export SMTP_USE_TLS="false"
```

**Option B: Gmail for @redhat.com**

Many Red Hatters use Gmail for corporate email:

```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="jbyrd@redhat.com"
export SMTP_PASSWORD="your-google-workspace-app-password"
export SMTP_FROM_NAME="Red Hat TAM"
export SMTP_USE_TLS="true"
```

---

### Office 365 / Outlook.com

```bash
export SMTP_SERVER="smtp.office365.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@outlook.com"
export SMTP_PASSWORD="your-password"
export SMTP_FROM_NAME="Red Hat TAM"
export SMTP_USE_TLS="true"
```

---

### Custom SMTP Server

```bash
export SMTP_SERVER="mail.yourcompany.com"
export SMTP_PORT="587"  # or 25, 465, 2525
export SMTP_USER="your-username"
export SMTP_PASSWORD="your-password"
export SMTP_FROM_NAME="Your Name"
export SMTP_USE_TLS="true"  # or "false" for non-TLS
```

---

## 🧪 Testing Email Configuration

### Test 1: Check Configuration

```bash
# Create a test script
cat > /tmp/test-email.py << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.email_handler import EmailConfig

config = EmailConfig()
print(f"SMTP Server: {config.smtp_server}")
print(f"SMTP Port: {config.smtp_port}")
print(f"SMTP User: {config.smtp_user}")
print(f"SMTP Password: {'*' * len(config.smtp_password) if config.smtp_password else '(not set)'}")
print(f"From Name: {config.from_name}")
print(f"Use TLS: {config.use_tls}")
print(f"\nConfigured: {config.is_configured()}")
EOF

python3 /tmp/test-email.py
```

### Test 2: Send Test Email

```bash
# Send a test agenda email
tam-generate-agenda --customer test --email your-email@example.com

# Check output for:
# ✅ Email sent successfully!  (success)
# ⚠️  Email failed              (failure)
```

### Test 3: Python Test Email

```bash
# Create detailed test
cat > /tmp/send-test-email.py << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.email_handler import send_email

success = send_email(
    to_email="your-email@example.com",
    subject="Taminator Test Email",
    body="This is a test email from Taminator. If you receive this, email is working!",
    html=False
)

if success:
    print("✅ Test email sent successfully!")
else:
    print("❌ Test email failed. Check configuration.")
EOF

python3 /tmp/send-test-email.py
```

---

## 🛠️ Troubleshooting

### Issue: "Email not configured"

**Problem:** SMTP settings not found

**Solution:**
```bash
# Check if variables are set
echo $SMTP_SERVER
echo $SMTP_USER

# If empty, set them:
export SMTP_SERVER="smtp.gmail.com"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"

# Or create config file
mkdir -p ~/.config/rfe-automation
# (create email.conf as shown above)
```

---

### Issue: "Authentication failed"

**Problem:** Wrong username or password

**For Gmail:**
- ❌ Don't use your regular Gmail password
- ✅ Must use App Password (16 characters)
- ✅ Enable 2-Factor Authentication first

**For Red Hat:**
- Check if on VPN (for smtp.corp.redhat.com)
- Check if using correct Google Workspace password

**Solution:**
```bash
# Double-check credentials
echo "User: $SMTP_USER"
echo "Password length: ${#SMTP_PASSWORD}"  # Gmail app password = 16 chars

# Test login manually
python3 << 'EOF'
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'your-app-password')
print("✅ Login successful!")
server.quit()
EOF
```

---

### Issue: "Connection refused" or "Connection timed out"

**Problem:** Network/firewall blocking SMTP

**Check:**
1. **Firewall:** Port 587 might be blocked
2. **VPN:** Red Hat internal SMTP requires VPN
3. **Port:** Try alternative ports (25, 465, 2525)

**Solution:**
```bash
# Test connection
telnet smtp.gmail.com 587
# Should connect (Ctrl+C to exit)

# Try alternate port (SSL/TLS)
export SMTP_PORT="465"

# Check firewall
sudo firewall-cmd --list-all | grep 587
```

---

### Issue: "TLS/SSL Error"

**Problem:** TLS configuration mismatch

**Solution:**
```bash
# For servers that don't support TLS
export SMTP_USE_TLS="false"

# For servers requiring SSL (port 465)
export SMTP_PORT="465"
export SMTP_USE_TLS="true"
```

---

### Issue: Email sent but not received

**Problem:** Email in spam or rejected

**Check:**
1. **Spam folder:** Check recipient's spam/junk
2. **From address:** Must match SMTP_USER
3. **SPF/DKIM:** Email might be rejected (corporate policy)

**Solution:**
```bash
# Use same email as sender and SMTP user
export SMTP_USER="jbyrd@redhat.com"
# Send FROM this email too (automatic)

# Check if email was sent (logs)
journalctl | grep -i smtp
```

---

## 📋 Complete Examples

### Example 1: Gmail Setup (Easiest)

```bash
# Step 1: Get Gmail app password
# Go to: https://myaccount.google.com/apppasswords
# Create password, copy it (example: jbsr jwdt aqeq sueq)

# Step 2: Set environment variables
cat >> ~/.bashrc << 'EOF'

# Taminator Email Configuration (Gmail)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="jimmykbyrd@gmail.com"
export SMTP_PASSWORD="jbsr jwdt aqeq sueq"
export SMTP_FROM_NAME="Jimmy Byrd - Red Hat TAM"
export SMTP_USE_TLS="true"
EOF

# Step 3: Reload
source ~/.bashrc

# Step 4: Test
tam-generate-agenda --customer test --email jimmykbyrd@gmail.com
```

### Example 2: Red Hat Email (On VPN)

```bash
# Requires: Connected to Red Hat VPN

# Add to ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# Taminator Email Configuration (Red Hat Internal)
export SMTP_SERVER="smtp.corp.redhat.com"
export SMTP_PORT="25"
export SMTP_USER="jbyrd@redhat.com"
export SMTP_FROM_NAME="Jimmy Byrd - Red Hat TAM"
export SMTP_USE_TLS="false"
EOF

# Reload and test
source ~/.bashrc
tam-generate-agenda --customer test --email jbyrd@redhat.com
```

### Example 3: Config File (Most Secure)

```bash
# Create config directory
mkdir -p ~/.config/rfe-automation

# Create config file
cat > ~/.config/rfe-automation/email.conf << 'EOF'
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "jimmykbyrd@gmail.com",
  "smtp_password": "jbsr jwdt aqeq sueq",
  "from_name": "Jimmy Byrd - Red Hat TAM",
  "use_tls": true
}
EOF

# Secure it (only you can read)
chmod 600 ~/.config/rfe-automation/email.conf

# Test
tam-generate-agenda --customer test --email jimmykbyrd@gmail.com

# No environment variables needed!
```

---

## 🔒 Security Best Practices

### 1. Use App Passwords (Not Regular Passwords)
```bash
# ❌ DON'T: Use regular Gmail password
export SMTP_PASSWORD="MyGmailPassword123"

# ✅ DO: Use app-specific password
export SMTP_PASSWORD="jbsr jwdt aqeq sueq"
```

### 2. Secure Config File
```bash
# ✅ Config file should be readable only by you
chmod 600 ~/.config/rfe-automation/email.conf

# ❌ Never commit passwords to git
# (email.conf is already in .gitignore)
```

### 3. Use Config File Over Environment Variables
```bash
# ❌ Environment variables visible in process list
ps aux | grep -i smtp

# ✅ Config file is more secure
# Only loaded when needed
```

### 4. Rotate Passwords Regularly
```bash
# Gmail: Revoke and create new app passwords quarterly
# Corporate: Follow company password policy
```

---

## 📊 Configuration Priority

Taminator checks for configuration in this order:

1. **Environment variables** (`SMTP_*`)
2. **Config file** (`~/.config/rfe-automation/email.conf`)
3. **Alternative config** (`~/.config/pai/email.conf`)

**Recommendation:** Use config file for security.

---

## 🎯 Usage Examples

### Send Agenda Email
```bash
tam-generate-agenda --customer jpmc --email jbyrd@redhat.com
```

### Send Backlog Report
```bash
tam-backlog-cleanup --customer jpmc --auto-clean --email jbyrd@redhat.com
```

### Send T3 Recommendations
```bash
tam-t3-reader --customer jpmc --recommend --email jbyrd@redhat.com
```

### Send Coverage Announcement
```bash
tam-coverage --tam "Jimmy Byrd" --tam-email jbyrd@redhat.com \
  --backup "Mike Johnson" --backup-email mjohnson@redhat.com \
  --start 2025-11-04 --end 2025-11-15 --customer jpmc \
  --email customer@jpmc.com
```

---

## 📞 Need Help?

### Still Having Issues?

1. **Check logs:** Look for error messages in tool output
2. **Test connection:** Use `telnet smtp.server.com 587`
3. **Verify credentials:** Double-check username/password
4. **Try Gmail first:** Easiest to set up and test
5. **Ask for help:** Slack #tam-automation

### Common Solutions

| Problem | Solution |
|---------|----------|
| Authentication failed | Use app password (not regular password) |
| Connection refused | Check firewall, VPN, port number |
| Email not received | Check spam folder, verify FROM address |
| Config not found | Create `~/.config/rfe-automation/email.conf` |
| TLS error | Try `SMTP_USE_TLS="false"` or different port |

---

## ✅ Verification Checklist

Before using email in production:

- [ ] SMTP credentials configured (env vars OR config file)
- [ ] Test email sent successfully
- [ ] Test email received (not in spam)
- [ ] Config file secured (`chmod 600`)
- [ ] App password used (not regular password)
- [ ] FROM address matches SMTP_USER

---

**"I'll be back"** — with your reports delivered via email! 📧🤖

*Taminator Email Configuration Guide*  
*Terminate manual report distribution*


