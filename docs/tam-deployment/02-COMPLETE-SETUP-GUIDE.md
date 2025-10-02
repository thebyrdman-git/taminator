# 📖 RFE Automation - Complete Setup Guide

**Comprehensive deployment guide for TAMs**

---

## 🎯 Overview

This guide provides complete instructions for deploying the RFE Automation System in your environment. After following this guide, you'll have a fully automated system that saves 2-3 hours daily.

---

## 📋 Table of Contents

1. [Prerequisites & Requirements](#prerequisites--requirements)
2. [System Installation](#system-installation)
3. [Customer Configuration](#customer-configuration)
4. [Portal Integration Setup](#portal-integration-setup)
5. [Automation Scheduling](#automation-scheduling)
6. [Monitoring & Alerting](#monitoring--alerting)
7. [Testing & Validation](#testing--validation)
8. [Advanced Configuration](#advanced-configuration)

---

## 🔧 Prerequisites & Requirements

### System Requirements
- **OS**: Red Hat Enterprise Linux 8+ or Fedora 35+
- **Python**: 3.8 or higher
- **Memory**: 2GB RAM minimum
- **Disk**: 5GB free space
- **Network**: Access to Red Hat internal networks

### Required Tools
```bash
# Verify required tools
python3 --version    # Should be 3.8+
rhcase --version     # Red Hat case management tool
git --version        # For cloning repositories
crontab -l          # For scheduling (should not error)
```

### Red Hat Access Requirements
- [ ] Red Hat SSO account (`rhn-support-[username]`)
- [ ] Access to Customer Portal Groups
- [ ] JIRA access (optional, for enhanced features)
- [ ] VPN access for internal APIs

### Customer Information Needed
For each customer you want to automate:
- [ ] Customer name
- [ ] Account number(s)
- [ ] Customer Portal Group URL
- [ ] Portal Group ID (discoverable via system)

---

## 🚀 System Installation

### Step 1: Clone Repository
```bash
# Create working directory
mkdir -p ~/rfe-automation
cd ~/rfe-automation

# Clone the system (replace with actual repository)
git clone https://github.com/redhat-tam/rfe-automation-system.git
cd rfe-automation-system

# Make scripts executable
chmod +x bin/*
```

### Step 2: Run Installation
```bash
# Run the comprehensive installer
./install.sh

# Or manual installation:
./bin/pai-rfe-deploy --install --validate
```

### Step 3: Verify Installation
```bash
# Check system status
./bin/pai-rfe-deploy --status

# Expected output:
# ✅ Environment validation PASSED
# ✅ Component testing PASSED
# ✅ System ready for customer configuration
```

---

## 👥 Customer Configuration

### Using the Onboarding Wizard (Recommended)
```bash
# Start the interactive wizard
./bin/pai-tam-onboard

# The wizard will guide you through:
# 1. Customer basic information
# 2. Account number configuration
# 3. Portal group discovery
# 4. Template customization
# 5. Testing and validation
```

### Manual Configuration
If you prefer manual setup:

#### 1. Create Customer Configuration
```bash
# Copy example configuration
cp config/example-tam-config.yaml config/my-customers.yaml

# Edit with your customer details
vim config/my-customers.yaml
```

#### 2. Example Configuration
```yaml
customers:
  wellsfargo:
    name: "Wells Fargo"
    account_numbers: ["838043"]
    portal_group_url: "https://access.redhat.com/groups/4357341"
    portal_group_id: "4357341"
    template: "enterprise"
    priority_management: true
    
  mybank:
    name: "My Bank"
    account_numbers: ["123456"]
    portal_group_url: "https://access.redhat.com/groups/XXXXXXX"
    portal_group_id: null  # Will be discovered
    template: "standard"
    priority_management: false
```

#### 3. Validate Configuration
```bash
# Test customer configuration
./bin/pai-rfe-deploy --validate-customers
```

---

## 🌐 Portal Integration Setup

### Discover Portal Group IDs
```bash
# Automated discovery
./bin/pai-portal-discover [customer-name]

# Manual discovery process:
# 1. Navigate to customer portal page
# 2. Look for group ID in URL
# 3. Update configuration file
```

### Test Portal Access
```bash
# Test portal connectivity
./bin/pai-portal-test [customer-name]

# Expected output:
# ✅ Portal access: VERIFIED
# ✅ Group permissions: CONFIRMED
# ✅ Content posting: READY
```

### Configure Portal Templates
```bash
# Customize portal templates
./bin/pai-template-editor [customer-name]

# Or manually edit:
vim config/customer_templates.yaml
```

---

## ⏰ Automation Scheduling

### Install Automated Scheduling
```bash
# Install cron jobs for daily automation
./bin/pai-rfe-schedule --install

# Verify installation
./bin/pai-rfe-schedule --status
```

### Default Schedule
- **Daily RFE Updates**: 9:00 AM EST (14:00 UTC)
- **System Health Check**: 8:30 AM EST (13:30 UTC)
- **Weekly Reports**: Wednesday 9:00 AM EST
- **Alert Cleanup**: Sunday 2:00 AM EST
- **Monthly Maintenance**: First Sunday 3:00 AM EST

### Customize Schedule
```bash
# Edit cron configuration
vim config/rfe-automation-cron.txt

# Reinstall with changes
./bin/pai-rfe-schedule --remove
./bin/pai-rfe-schedule --install
```

---

## 📊 Monitoring & Alerting

### Configure Alerting
```bash
# Test alert system
./bin/pai-alerts --test

# View alert dashboard
./bin/pai-alerts --summary
```

### Alert Types
- **🔴 Failure Alerts**: Immediate notification of automation failures
- **⚠️ Warning Alerts**: Timeouts and non-critical issues
- **✅ Success Alerts**: Daily summary of successful operations
- **📊 Weekly Reports**: Comprehensive system health reports

### Alert Destinations
- **File-based**: Guaranteed delivery to `/tmp/rfe-alerts/`
- **Email**: Attempts delivery to configured email address
- **Dashboard**: Web-based alert management interface

---

## 🧪 Testing & Validation

### Test Individual Customers
```bash
# Test customer automation (dry run)
./bin/pai-rfe-monitor [customer-name] --test

# Test with actual portal posting
./bin/pai-rfe-monitor [customer-name] --daily
```

### Test Complete System
```bash
# Run comprehensive system test
./bin/pai-rfe-deploy --test-all

# Test scheduled automation
./bin/pai-rfe-schedule --test
```

### Validate Results
```bash
# Check automation logs
tail -f /tmp/rfe-automation-cron.log

# View generated content
ls -la /tmp/rfe-*

# Check portal updates (manual verification required)
```

---

## ⚙️ Advanced Configuration

### Enable Priority Management
```bash
# Configure customer priority system
./bin/pai-priority-manager --setup [customer-name]

# Assign priorities to cases
./bin/pai-priority-manager --assign [customer-name]
```

### JIRA Integration (Optional)
```bash
# Configure JIRA Personal Access Token
export JIRA_PAT_TOKEN="your-token-here"

# Test JIRA connectivity
./bin/pai-jira-test
```

### Custom Templates
```bash
# Create custom template
cp config/customer_templates.yaml config/my-templates.yaml

# Edit template
vim config/my-templates.yaml

# Apply template
./bin/pai-template-apply [customer-name] my-templates
```

### API Integration
```bash
# Enable API-based portal posting (if available)
./bin/pai-api-setup [customer-name]

# Test API connectivity
./bin/pai-api-test [customer-name]
```

---

## 🔧 Maintenance

### Daily Maintenance
```bash
# Run daily cleanup
./bin/pai-maintenance --daily
```

### Weekly Maintenance
```bash
# Run weekly maintenance
./bin/pai-maintenance --weekly
```

### System Health Monitoring
```bash
# Check system health
./bin/pai-rfe-deploy --health-check

# View system metrics
./bin/pai-metrics --dashboard
```

---

## 📈 Success Metrics

After deployment, you should see:
- **⏱️ Time Savings**: 2-3 hours daily per customer
- **📊 Accuracy**: 100% case discovery rate
- **🔄 Reliability**: >99% automation success rate
- **📧 Alerting**: <5 minute notification of issues

---

## 🆘 Troubleshooting

Common issues and solutions:

### Authentication Issues
```bash
# Re-authenticate with Red Hat services
rhcase config setup
./bin/pai-auth-refresh
```

### Portal Access Issues
```bash
# Test portal connectivity
./bin/pai-portal-debug [customer-name]

# Check group permissions
./bin/pai-portal-permissions [customer-name]
```

### Automation Failures
```bash
# Check automation logs
./bin/pai-logs --recent

# Run diagnostic tests
./bin/pai-diagnostics --full
```

---

## 📞 Support

- **📧 Email**: rfe-automation-support@redhat.com
- **💬 Slack**: #rfe-automation-support
- **📖 Documentation**: Full troubleshooting guide available
- **🎥 Training**: Video tutorials and webinars

---

## ➡️ Next Steps

1. **🎯 Configure All Customers**: Use onboarding wizard for each customer
2. **📊 Track ROI**: Monitor time savings and efficiency gains
3. **🔧 Customize**: Adjust templates and priorities as needed
4. **🌟 Share Success**: Help other TAMs deploy the system

---

**🎉 Congratulations! You now have a fully automated RFE management system!**

---

*RFE Automation System - Complete Setup Guide*  
*Version 1.0 - Created for Global TAM Deployment*
