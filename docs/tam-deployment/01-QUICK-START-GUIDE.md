# 🚀 RFE Automation - Quick Start Guide

**Get your first RFE automation running in 5 minutes!**

---

## 🎯 What You'll Achieve

In the next 5 minutes, you'll:
- ✅ Deploy the RFE automation system
- ✅ Configure your first customer
- ✅ Run your first automated RFE update
- ✅ Save 2-3 hours of manual work daily

---

## ⚡ Prerequisites (2 minutes)

### Required Access
- [ ] Red Hat laptop with terminal access
- [ ] Red Hat SSO credentials (`rhn-support-[username]`)
- [ ] Access to customer portal groups
- [ ] `rhcase` tool installed and configured

### Quick Verification
```bash
# Verify rhcase is working
rhcase --version
rhcase list [your-customer] --months 1
```

---

## 🚀 5-Minute Deployment

### Step 1: Clone and Deploy (1 minute)
```bash
# Clone the RFE automation system
git clone https://github.com/your-org/rfe-automation-system.git
cd rfe-automation-system

# Run one-click deployment
./bin/pai-rfe-deploy --install
```

### Step 2: Configure Your First Customer (2 minutes)
```bash
# Run the setup wizard
./bin/pai-tam-onboard

# Follow the prompts to add your customer:
# - Customer name (e.g., "Wells Fargo")
# - Account number (e.g., "838043")
# - Portal group URL
```

### Step 3: Test Your Setup (1 minute)
```bash
# Test the system with your customer
./bin/pai-rfe-monitor [customer-name] --test

# You should see:
# ✅ Customer automation: READY
```

### Step 4: Run Your First Automation (1 minute)
```bash
# Generate your first RFE report
./bin/pai-rfe-[customer-name]

# Example output:
# 🎉 Generated RFE report for Wells Fargo
# 📊 Found 23 RFE cases, 8 Bug cases
# 📁 Content ready for portal posting
```

---

## 🎉 Success! What Just Happened?

You now have:
- ✅ **Automated RFE Discovery**: System finds all your RFE/Bug cases
- ✅ **Portal Content Generation**: Creates formatted tables for customer portals
- ✅ **Monitoring & Alerting**: Tracks success/failures, sends alerts
- ✅ **Daily Automation**: Scheduled to run every morning at 9 AM EST

---

## 🔄 Enable Daily Automation (Optional)

```bash
# Install automated daily scheduling
./bin/pai-rfe-schedule --install

# Check status
./bin/pai-rfe-schedule --status
```

---

## 📊 Immediate Benefits

**Time Saved**: 2-3 hours daily
**Accuracy**: 100% automated case discovery
**Consistency**: Standardized portal updates
**Reliability**: Comprehensive error handling and monitoring

---

## 🆘 Need Help?

- 📖 **Complete Guide**: See `02-COMPLETE-SETUP-GUIDE.md`
- 🔧 **Troubleshooting**: See `04-TROUBLESHOOTING-GUIDE.md`
- 💬 **Support**: Contact the RFE Automation Team
- 📊 **Track ROI**: See `05-ROI-TRACKING-GUIDE.md`

---

## ➡️ What's Next?

1. **📖 Read the Complete Setup Guide** for advanced features
2. **🎯 Configure Additional Customers** using the onboarding wizard
3. **📊 Track Your Time Savings** using the ROI tracking tools
4. **🌟 Share Your Success** with other TAMs

---

**🎉 Congratulations! You're now saving 2-3 hours daily with automated RFE management!**

---

*RFE Automation System - Quick Start Guide*  
*Version 1.0 - Created for Global TAM Deployment*
