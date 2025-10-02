# 📋 Quick Reference Cards
## Essential Commands and Workflows for TAM RFE Automation

### 🎯 **Overview**
These quick reference cards provide instant access to the most commonly used commands, workflows, and troubleshooting steps. Print these cards or keep them handy for quick reference during daily operations.

---

## 🚀 **CARD 1: ESSENTIAL COMMANDS**

### **Core Automation Commands**
```bash
# Daily automation
pai-rfe-[customer]              # Run full automation for customer
pai-test-[customer]             # Test automation safely
pai-rfe-[customer] --daily      # Run with daily scheduling

# System management
pai-rfe-deploy --validate       # Check system health
pai-rfe-deploy --status         # Show system status
pai-alerts --summary           # View alert dashboard
pai-maintenance --daily        # Daily system maintenance
```

### **Setup and Configuration**
```bash
# Initial setup
pai-tam-onboard                # Interactive customer setup
pai-cursor-setup               # AI development environment
pai-sandbox                    # Safe learning environment

# Configuration management
pai-rfe-deploy --config        # Show configuration
pai-rfe-schedule --status      # View automation schedule
pai-rfe-schedule --install     # Install cron jobs
```

### **Monitoring and Troubleshooting**
```bash
# Health monitoring
pai-alerts --recent            # Recent alerts
pai-alerts --clean             # Clean old alerts
pai-rfe-monitor [customer]     # Monitor specific customer

# Troubleshooting
pai-rfe-deploy --validate      # Comprehensive system check
rhcase config setup            # Fix authentication
pai-maintenance --health       # System health check
```

---

## 🛠️ **CARD 2: DAILY WORKFLOW**

### **Morning Routine (5 minutes)**
```bash
# 1. Check system health
pai-alerts --summary

# 2. Run automation for each customer
pai-rfe-wellsfargo
pai-rfe-tdbank
pai-rfe-jpmc

# 3. Verify success
pai-alerts --recent

# 4. Review any issues
pai-alerts --details [if needed]
```

### **Weekly Review (15 minutes)**
```bash
# 1. Generate weekly reports
pai-rfe-wellsfargo --weekly-report
pai-weekly-troubleshooting

# 2. System maintenance
pai-maintenance --weekly

# 3. Review performance
pai-alerts --weekly-summary

# 4. Plan improvements
# Review customer feedback and optimization opportunities
```

### **Monthly Tasks (30 minutes)**
```bash
# 1. Comprehensive maintenance
pai-maintenance --monthly

# 2. Performance analysis
pai-alerts --monthly-report

# 3. Configuration review
pai-rfe-deploy --config-review

# 4. Update planning
# Plan system updates and enhancements
```

---

## 🎯 **CARD 3: CUSTOMER ONBOARDING CHECKLIST**

### **Pre-Onboarding (5 minutes)**
- [ ] **Customer relationship established** (6+ months recommended)
- [ ] **Customer communication** about automation benefits
- [ ] **Portal group access** confirmed
- [ ] **Account numbers** identified and verified
- [ ] **Customer preferences** discussed (update frequency, format)

### **Onboarding Process (15 minutes)**
```bash
# 1. Start onboarding wizard
pai-tam-onboard

# 2. Follow interactive prompts:
#    - Customer name and key
#    - Account numbers
#    - Portal group URL
#    - Template preferences
#    - Automation schedule

# 3. Complete testing and validation
#    - System validates all settings
#    - Test case discovery
#    - Verify portal access
#    - Confirm safety settings
```

### **Post-Onboarding (10 minutes)**
- [ ] **Test automation**: `pai-test-[customer]`
- [ ] **Verify portal content** accuracy
- [ ] **Check notification settings** (should be OFF)
- [ ] **Customer communication** about go-live
- [ ] **Schedule first automation** run
- [ ] **Monitor initial results** closely

---

## 🧪 **CARD 4: SANDBOX LEARNING PATH**

### **Quick Start (10 minutes)**
```bash
pai-sandbox
# Select: 1. Quick Start Tutorial
```
**Learn**: Basic concepts, mock customers, sample cases

### **Customer Onboarding Simulation (20 minutes)**
```bash
pai-sandbox
# Select: 2. Customer Onboarding Simulation
```
**Learn**: Complete onboarding process with Acme Financial

### **RFE Automation Workshop (25 minutes)**
```bash
pai-sandbox
# Select: 3. RFE Automation Workshop
```
**Learn**: Full automation workflow with realistic scenarios

### **AI Development Training (30 minutes)**
```bash
pai-sandbox
# Select: 4. AI Development Training
```
**Learn**: AI-powered development with Cursor IDE

### **Advanced Scenarios (35 minutes)**
```bash
pai-sandbox
# Select: 5. Advanced Scenarios
```
**Learn**: Complex use cases and expert techniques

---

## 🚨 **CARD 5: TROUBLESHOOTING QUICK FIXES**

### **Authentication Issues**
```bash
# Symptoms: "rhcase command failed", "Authentication error"
# Solution:
rhcase config setup
# Re-enter credentials when prompted
```

### **Portal Access Problems**
```bash
# Symptoms: "403 Forbidden", "Access denied"
# Solution:
1. Verify customer group permissions
2. Check portal URL accuracy
3. Confirm group ID extraction
4. Contact Red Hat support if needed
```

### **JIRA Connection Issues**
```bash
# Symptoms: "JIRA API timeout", "Connection refused"
# Solution:
1. Check VPN connection
2. Verify JIRA credentials
3. Test JIRA access manually
4. Check firewall settings
```

### **Template Rendering Errors**
```bash
# Symptoms: Malformed portal content, missing data
# Solution:
1. Validate customer configuration:
   pai-rfe-deploy --validate
2. Check template syntax
3. Verify case data format
4. Test in sandbox first
```

### **Notification Checkbox Issues**
```bash
# Symptoms: Customers receiving unwanted emails
# CRITICAL SOLUTION:
1. STOP automation immediately:
   pai-rfe-schedule --disable
2. Check portal notification settings
3. Verify checkbox is UNCHECKED
4. Contact affected customers
5. Fix settings before resuming
```

---

## 📊 **CARD 6: PERFORMANCE MONITORING**

### **Daily Health Checks**
```bash
# System health indicators
pai-alerts --summary
# Look for: Green status, no critical alerts

pai-rfe-deploy --status
# Look for: All components operational

# Customer-specific health
pai-rfe-[customer] --health
# Look for: Successful runs, no errors
```

### **Performance Metrics**
**Time Savings Tracking:**
- Manual time before automation: _____ hours/day
- Automated time after: _____ minutes/day
- Daily savings: _____ hours
- Weekly savings: _____ hours
- Monthly savings: _____ hours

**Quality Metrics:**
- Case discovery accuracy: _____%
- Update consistency: _____%
- Error rate: _____%
- Customer satisfaction: _____%

### **Alert Thresholds**
- **Green**: No issues, normal operation
- **Yellow**: Minor issues, monitor closely
- **Red**: Critical issues, immediate attention required

---

## 🎯 **CARD 7: CUSTOMER COMMUNICATION TEMPLATES**

### **Initial Automation Announcement**
```
Subject: Enhanced RFE Status Updates - Automated Tracking

Hello [Customer Team],

I'm implementing an enhanced RFE tracking system that will provide more frequent, accurate, and comprehensive status updates.

Benefits:
• Daily updates instead of weekly
• 100% accurate case discovery
• Consistent professional formatting
• Real-time JIRA status information

Updates will appear on your Red Hat Customer Portal page with no email notifications.

Questions? Contact me at [email]

Best regards,
[Your Name]
```

### **Issue Resolution Communication**
```
Subject: RFE Automation - Issue Resolved

Hello [Customer Team],

I wanted to update you on a brief issue with our RFE automation system that has now been resolved.

What happened: [Brief description]
Impact: [Minimal/None expected]
Resolution: [What was fixed]
Prevention: [Steps taken to prevent recurrence]

Your RFE updates will continue as normal. Please let me know if you notice any issues.

Best regards,
[Your Name]
```

### **Success Celebration**
```
Subject: RFE Automation Success - Improved Service Delivery

Hello [Customer Team],

I wanted to share some positive results from our RFE automation implementation:

• Update frequency: Daily (vs weekly previously)
• Accuracy: 100% case discovery
• Consistency: Standardized professional format
• Time savings: 2+ hours daily for strategic work

This allows me to focus more on strategic discussions and proactive support for your initiatives.

Thank you for your patience during the implementation!

Best regards,
[Your Name]
```

---

## 🔧 **CARD 8: CONFIGURATION QUICK REFERENCE**

### **Customer Configuration Template**
```yaml
customers:
  [customer_key]:
    name: "[Customer Name]"
    account_numbers: ["123456"]
    portal_group_url: "https://access.redhat.com/groups/123456"
    portal_group_id: "123456"
    template_style: "standard"
    priority_management: false
    automation_schedule: "daily_9am_est"
    enabled: true
```

### **Template Customization Options**
- **template_style**: `enterprise`, `standard`, `minimal`
- **priority_management**: `true`, `false`
- **automation_schedule**: `daily_9am_est`, `weekly_friday`, `custom`
- **notification_settings**: Always `disabled` for safety

### **Common File Locations**
```bash
# Configuration files
~/.config/pai/customers/
~/.config/pai/templates/

# Log files
/tmp/pai-logs/
/tmp/rfe-alerts/

# Documentation
~/hatter-pai/docs/tam-deployment/
~/hatter-pai/training/
```

---

## 📞 **CARD 9: SUPPORT CONTACTS**

### **Technical Support**
- **Email**: rfe-automation-support@redhat.com
- **Response Time**: 4 hours (business hours)
- **Escalation**: Critical issues get immediate attention

### **Community Support**
- **Best Practices**: tam-automation-community@redhat.com
- **Success Stories**: tam-success-stories@redhat.com
- **Feature Requests**: rfe-enhancement-requests@redhat.com

### **Emergency Procedures**
1. **Stop automation**: `pai-rfe-schedule --disable`
2. **Contact support**: rfe-automation-support@redhat.com
3. **Document issue**: Include logs and error messages
4. **Customer communication**: If customer impact occurred

---

## 🎓 **CARD 10: LEARNING RESOURCES**

### **Documentation**
- **Quick Start**: `docs/tam-deployment/01-QUICK-START-GUIDE.md`
- **Complete Setup**: `docs/tam-deployment/02-COMPLETE-SETUP-GUIDE.md`
- **Troubleshooting**: `docs/tam-deployment/04-TROUBLESHOOTING-GUIDE.md`
- **Best Practices**: `training/guides/tam-automation-best-practices.md`

### **Training Materials**
- **Video Library**: `training/videos/`
- **Interactive Sandbox**: `pai-sandbox`
- **Success Stories**: `training/guides/success-stories-case-studies.md`

### **Advanced Learning**
- **AI Development**: `pai-cursor-setup`
- **System Architecture**: `docs/tam-deployment/03-SYSTEM-ARCHITECTURE.md`
- **ROI Tracking**: `docs/tam-deployment/05-ROI-TRACKING-GUIDE.md`

---

## 💡 **CARD 11: PRO TIPS**

### **Efficiency Tips**
- **Use aliases**: Create shell aliases for frequent commands
- **Batch operations**: Group similar tasks together
- **Monitor proactively**: Check alerts before issues escalate
- **Document customizations**: Keep notes on customer preferences

### **Relationship Tips**
- **Communicate benefits**: Help customers understand value
- **Be transparent**: Share automation details openly
- **Gather feedback**: Regularly ask for improvement suggestions
- **Celebrate success**: Share positive results with customers

### **Technical Tips**
- **Test in sandbox first**: Always validate changes safely
- **Keep backups**: Save working configurations
- **Monitor performance**: Watch for system degradation
- **Stay updated**: Keep system components current

---

**Print these cards and keep them handy for quick reference during daily operations!**

---

*Quick Reference Cards v1.0*  
*For updates and additional cards: rfe-automation-support@redhat.com*
