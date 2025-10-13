# Red Hat Insights Setup Guide
## Enterprise System Monitoring & Proactive Issue Detection

### 🎯 **Overview**

Red Hat Insights provides:
- **Proactive Issue Detection**: Identify problems before they cause outages
- **Security Vulnerability Scanning**: CVE detection and remediation
- **Performance Analysis**: System health and optimization recommendations
- **Patch Management**: Automated patch recommendations
- **Compliance Reporting**: Security policy compliance
- **Drift Detection**: Configuration drift analysis

**Cost**: FREE with RHEL subscription (included with Developer Subscription)

---

### 📋 **Prerequisites**

1. **Active Red Hat Subscription**
   ```bash
   # Check subscription status
   sudo subscription-manager status
   ```

2. **Network Access**
   - Outbound HTTPS to `cert-api.access.redhat.com` (port 443)
   - Outbound HTTPS to `cloud.redhat.com` (port 443)

3. **Insights Client Package**
   ```bash
   # Check if installed
   rpm -qa | grep insights-client
   ```

---

### 🚀 **Installation & Setup**

#### Step 1: Install Insights Client

```bash
# SSH to miraclemax
ssh jbyrd@192.168.1.34

# Install insights-client (if not already installed)
sudo dnf install -y insights-client

# Verify installation
insights-client --version
```

#### Step 2: Register System with Insights

```bash
# Register miraclemax with Red Hat Insights
sudo insights-client --register

# Expected output:
# Successfully registered host miraclemax.local
# Automatic scheduling for Insights has been enabled.
```

#### Step 3: Run Initial Analysis

```bash
# Run first insights collection and upload
sudo insights-client --check-results

# This will:
# 1. Collect system data
# 2. Upload to Red Hat cloud (encrypted)
# 3. Analyze for known issues
# 4. Display results URL
```

#### Step 4: Configure Automatic Updates

```bash
# Enable daily automatic checks (already enabled by default)
sudo systemctl enable insights-client.timer
sudo systemctl start insights-client.timer

# Verify timer is active
sudo systemctl status insights-client.timer

# Check when next run is scheduled
sudo systemctl list-timers | grep insights
```

---

### 🔧 **Configuration**

#### Configure Insights Client

```bash
# Edit configuration file
sudo vi /etc/insights-client/insights-client.conf
```

**Recommended settings:**

```ini
[insights-client]
# Basic settings
loglevel=INFO
auto_config=True
auto_update=True

# Proxy settings (if needed)
# proxy=http://proxy.example.com:3128

# GPG signature verification
gpg=True

# Display name in Red Hat Insights portal
display_name=miraclemax

# Collection frequency (handled by systemd timer)
# Default: daily
```

#### Privacy & Data Collection Settings

**What Insights collects:**
- System facts (CPU, memory, disk, packages)
- Configuration files (sanitized, no passwords)
- Log excerpts (errors only)
- Installed packages and versions
- Running services

**What it does NOT collect:**
- User data
- Passwords or secrets
- Full log files
- Personal information

**Customize data collection:**
```bash
# View what will be collected
sudo insights-client --payload

# Redact specific patterns (optional)
sudo vi /etc/insights-client/remove.conf

# Example: Redact hostnames, IPs, MAC addresses
[remove]
patterns=hostname,ip,mac
```

---

### 📊 **Access Red Hat Insights Portal**

#### Step 1: Access Web Console

1. Go to: https://console.redhat.com/insights/
2. Login with Red Hat account
3. Navigate to: **Inventory** → Find `miraclemax`

#### Step 2: Review Dashboard

**Main sections:**

1. **Advisor**: Proactive recommendations
   - Performance optimization
   - Stability improvements
   - Configuration best practices

2. **Vulnerability**: Security CVEs
   - Critical vulnerabilities
   - Available patches
   - Remediation playbooks

3. **Compliance**: Policy adherence
   - PCI-DSS
   - HIPAA
   - STIGs (Security Technical Implementation Guides)

4. **Patch**: Available updates
   - Security patches
   - Bug fixes
   - Enhancement updates

5. **Drift**: Configuration changes
   - System drift detection
   - Baseline comparison

---

### 🔔 **Configure Email Notifications**

#### Enable Insights Notifications

1. Go to: https://console.redhat.com/settings/notifications
2. Click "Integrations"
3. Add email: `jimmykbyrd@gmail.com`
4. Configure notification preferences:

**Recommended settings:**
```
☑ New recommendations (Advisor)
☑ Critical vulnerabilities (Vulnerability)
☑ High-risk issues
☑ Patch availability (weekly digest)
☑ Compliance policy failures
```

---

### 🤖 **Ansible Integration**

Red Hat Insights generates Ansible playbooks for automated remediation.

#### Enable Remediations

```bash
# Install Ansible (if not already installed)
sudo dnf install -y ansible-core

# Download remediation playbook from Insights portal
# Example: Fix CVE-2024-12345

# 1. Go to Insights → Vulnerability
# 2. Select vulnerability
# 3. Click "Remediate with Ansible"
# 4. Download playbook

# Run remediation playbook
ansible-playbook -i localhost, --connection=local remediation-playbook.yml
```

---

### 📈 **Monitoring & Dashboards**

#### View System Health

```bash
# Check insights status
sudo insights-client --status

# View last upload
sudo insights-client --check-results

# Force immediate upload
sudo insights-client --force-upload
```

#### Integration with Grafana (Optional)

Create Grafana dashboard showing Insights metrics:

```yaml
# Prometheus scraper for Insights metrics
# /etc/prometheus/prometheus.yml

scrape_configs:
  - job_name: 'redhat-insights'
    static_configs:
      - targets: ['localhost:9090']
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: 'redhat_insights_.*'
        action: keep
```

---

### 🔒 **Security & Compliance**

#### Data Transmission Security

- **TLS 1.2+**: All data encrypted in transit
- **Certificate-based auth**: Uses Red Hat certificate
- **No plaintext secrets**: Passwords automatically redacted
- **SOC 2 Type II**: Red Hat Insights is certified

#### Firewall Configuration

```bash
# Allow outbound HTTPS to Red Hat
sudo firewall-cmd --permanent --add-rich-rule='
  rule family="ipv4"
  destination address="cert-api.access.redhat.com"
  port port="443" protocol="tcp" accept'

sudo firewall-cmd --permanent --add-rich-rule='
  rule family="ipv4"
  destination address="cloud.redhat.com"
  port port="443" protocol="tcp" accept'

sudo firewall-cmd --reload
```

#### Audit Logging

```bash
# Enable audit logging for Insights
sudo systemctl enable auditd
sudo systemctl start auditd

# View Insights-related audit events
sudo ausearch -k insights | grep insights-client
```

---

### 🚨 **Critical Issues Alerts**

#### Slack Integration (Optional)

1. Go to: https://console.redhat.com/settings/integrations
2. Click "Add Integration"
3. Select "Webhook"
4. Configure webhook URL for Slack/Teams/Email

Example webhook for n8n:
```
https://n8n.jbyrd.org/webhook/insights-alerts
```

---

### 📊 **Metrics & KPIs**

Track Insights effectiveness:

```yaml
KPIs to Monitor:
  - Critical issues identified: Target <5
  - High-severity CVEs: Target 0
  - Patch lag time: Target <7 days
  - Compliance score: Target >95%
  - System uptime: Target >99.9%
  - Mean time to remediation: Target <24 hours
```

---

### 🔧 **Troubleshooting**

#### Insights client not uploading?

```bash
# Check connectivity
sudo insights-client --test-connection

# Check logs
sudo journalctl -u insights-client.timer -f

# Manual run with debug
sudo insights-client --verbose --force-upload
```

#### Registration issues?

```bash
# Unregister and re-register
sudo insights-client --unregister
sudo insights-client --register

# Check subscription
sudo subscription-manager status
```

#### Firewall blocking?

```bash
# Test connectivity to Red Hat
curl -v https://cert-api.access.redhat.com
curl -v https://cloud.redhat.com

# Check firewall rules
sudo firewall-cmd --list-all
```

---

### 🎯 **Quick Start Checklist**

- [ ] Install `insights-client`
- [ ] Register system: `sudo insights-client --register`
- [ ] Run initial analysis: `sudo insights-client --check-results`
- [ ] Access portal: https://console.redhat.com/insights/
- [ ] Configure email notifications (jimmykbyrd@gmail.com)
- [ ] Enable automatic daily scans
- [ ] Review and remediate initial findings
- [ ] Set up Ansible for automated remediation
- [ ] Configure compliance policies (if needed)
- [ ] Integrate with existing monitoring (Prometheus/Grafana)

---

### 📚 **Additional Resources**

- **Official Docs**: https://access.redhat.com/products/red-hat-insights
- **API Documentation**: https://console.redhat.com/docs/api
- **Ansible Remediation**: https://access.redhat.com/articles/4417801
- **Compliance Guide**: https://access.redhat.com/articles/6956315

---

*Red Hat Insights Setup Guide for miraclemax*  
*Enterprise-Grade Proactive System Monitoring*  
*Part of Phase 1.2: Monitoring & Observability*

