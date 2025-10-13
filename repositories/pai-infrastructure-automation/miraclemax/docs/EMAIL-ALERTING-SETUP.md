# Email Alerting Setup Guide
## Gmail SMTP Configuration for Alertmanager

### 📧 **Overview**

Alertmanager is configured to send email notifications to `jimmykbyrd@gmail.com` for all infrastructure alerts with priority-based routing:

- **CRITICAL** (🚨): Immediate email (repeat every 30 min)
- **WARNING** (⚠️): Batched email (repeat every 2 hours)
- **INFO** (ℹ️): Daily digest (repeat every 24 hours)

---

### 🔐 **Gmail App Password Setup**

Gmail requires an "App Password" for SMTP authentication (not your regular password).

#### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification" if not already enabled

#### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Enter name: `miraclemax-alertmanager`
4. Click "Generate"
5. **Copy the 16-character password** (format: `xxxx xxxx xxxx xxxx`)

#### Step 3: Store Password Securely on miraclemax
```bash
# SSH to miraclemax
ssh jbyrd@192.168.1.34

# Create secrets directory
mkdir -p /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax/config/alertmanager/secrets

# Store the password (replace with your actual app password)
echo "your-16-char-app-password" > /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax/config/alertmanager/secrets/smtp_password

# Secure the file
chmod 600 /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax/config/alertmanager/secrets/smtp_password
```

---

### 🚀 **Deployment**

Deploy Alertmanager with email configuration:

```bash
# Deploy Alertmanager
cd /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax
podman-compose -f compose/alertmanager.yml up -d

# Verify it's running
podman logs alertmanager

# Test email notification (optional)
curl -X POST http://localhost:9093/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '[{
    "labels": {
      "alertname": "TestAlert",
      "severity": "info"
    },
    "annotations": {
      "summary": "Test email notification",
      "description": "This is a test alert to verify email delivery"
    }
  }]'
```

Check `jimmykbyrd@gmail.com` inbox for test alert.

---

### 📊 **Alert Priority Levels**

#### 🚨 **CRITICAL** (P0)
**When**: Service completely down, data loss risk, security incident  
**Action**: Immediate notification, high-priority email  
**Repeat**: Every 30 minutes until resolved  
**Examples**:
- Traefik down (all services unreachable)
- Authelia down (authentication broken)
- Disk >95% full
- CPU >90% for 2+ minutes
- Memory >90% (OOM risk)

#### ⚠️ **WARNING** (P1/P2)
**When**: Service degraded, capacity concerns, non-critical issues  
**Action**: Batched notification (wait 2 min for grouping)  
**Repeat**: Every 2 hours  
**Examples**:
- CPU >75% for 5+ minutes
- Memory >80%
- Disk >85%
- Container restarting frequently
- Network errors increasing

#### ℹ️ **INFO** (P3)
**When**: Informational, trending, non-urgent  
**Action**: Daily digest  
**Repeat**: Every 24 hours  
**Examples**:
- Configuration changes
- Backup completion status
- Capacity trending reports

---

### 🔧 **Troubleshooting**

#### Emails not sending?

**Check Alertmanager logs:**
```bash
podman logs alertmanager | grep -i smtp
```

**Common issues:**

1. **Invalid credentials**: Verify app password is correct
   ```bash
   cat /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax/config/alertmanager/secrets/smtp_password
   ```

2. **Gmail blocking**: Check https://myaccount.google.com/notifications for security alerts

3. **Firewall**: Ensure outbound SMTP allowed
   ```bash
   sudo firewall-cmd --list-all | grep 587
   ```

4. **Test SMTP directly:**
   ```bash
   podman exec -it alertmanager sh
   wget --debug -O- \
     --post-data='EHLO localhost' \
     smtp://smtp.gmail.com:587
   ```

#### Test alert delivery:
```bash
# Send test critical alert
curl -X POST http://192.168.1.34:9093/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '[{
    "labels": {
      "alertname": "TestCriticalAlert",
      "severity": "critical",
      "instance": "miraclemax"
    },
    "annotations": {
      "summary": "Test critical alert",
      "description": "This is a test to verify email delivery works",
      "runbook": "Check your inbox for this alert"
    }
  }]'
```

Check email within 30 seconds.

---

### 📧 **Email Format Examples**

#### Critical Alert Email:
```
Subject: 🚨 CRITICAL: HighCPUUsage on miraclemax
From: miraclemax-alerts@jbyrd.org
To: jimmykbyrd@gmail.com
Priority: High

🚨 CRITICAL ALERT

Environment: miraclemax production
Alert: HighCPUUsage
Time: 2025-10-12 23:45:00

Summary: High CPU usage on miraclemax
Description: CPU usage is 92.5% (threshold: 75%)
Runbook: ssh miraclemax 'top -b -n 1 | head -20'
Component: host
Status: firing

---
Alertmanager: https://alerts.jbyrd.org
Grafana: https://grafana.jbyrd.org
```

#### Warning Alert Email:
```
Subject: ⚠️  WARNING: HighDiskUsage on miraclemax
[HTML formatted with orange styling]
```

#### Daily Digest Email:
```
Subject: ℹ️  Daily Digest: miraclemax monitoring summary
[HTML formatted with blue styling, summary list]
```

---

### 🔒 **Security Best Practices**

1. **Never commit SMTP password to Git**
   - Already in `.gitignore`
   - Store in `/config/alertmanager/secrets/`

2. **Use Gmail App Password** (not account password)

3. **Rotate password quarterly**

4. **Monitor for unauthorized access**
   - Check Gmail "Recent security activity"

5. **Backup alertmanager config**
   ```bash
   sudo cp -r /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax/config/alertmanager /mnt/backup/
   ```

---

### 🎯 **Next Steps**

1. **Set up Gmail App Password** (see Step 2 above)
2. **Store password on miraclemax** (Step 3)
3. **Deploy Alertmanager** with updated config
4. **Send test alert** to verify email delivery
5. **Configure smartphone notifications** (Gmail app)

---

*Email Alerting Setup Guide for miraclemax - Enterprise-Grade Monitoring*

