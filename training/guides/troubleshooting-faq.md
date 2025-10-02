# ❓ Troubleshooting FAQ
## Common Issues and Solutions for TAM RFE Automation

### 🎯 **Overview**
This comprehensive FAQ addresses the most common issues encountered with TAM RFE automation. Each entry includes symptoms, root causes, step-by-step solutions, and prevention strategies.

---

## 🔐 **AUTHENTICATION & ACCESS ISSUES**

### **Q1: "rhcase command failed" or "Authentication Failed"**

**Symptoms:**
- Error message: "rhcase command failed: Authentication Failed"
- Error message: "Decryption failed: Check your credentials"
- Automation fails during case discovery phase

**Root Causes:**
- Expired Red Hat SSO session
- Incorrect username/password
- Missing or corrupted rhcase configuration
- Network connectivity issues

**Solution:**
```bash
# Step 1: Reconfigure rhcase authentication
rhcase config setup

# Step 2: Enter credentials when prompted
# Username: rhn-support-[your-username]
# Password: [your Red Hat password]

# Step 3: Test authentication
rhcase list --help

# Step 4: Verify with test query
rhcase list 838043 --months 1
```

**Prevention:**
- Set up credential refresh reminders
- Use environment variables for automation
- Monitor authentication status regularly

---

### **Q2: "403 Forbidden" or "Access denied" to customer portal**

**Symptoms:**
- Cannot access customer portal group pages
- Error 403 when trying to edit portal content
- Portal updates fail with permission errors

**Root Causes:**
- Insufficient portal group permissions
- Incorrect group ID or URL
- Customer removed TAM access
- Portal group privacy settings changed

**Solution:**
```bash
# Step 1: Verify group URL and ID
echo "Group URL: [paste customer portal URL]"
echo "Group ID: [extracted from URL]"

# Step 2: Test manual access
# Open browser and navigate to portal URL
# Verify you can see the group content

# Step 3: Check edit permissions
# Try to access the edit URL manually
# URL format: https://access.redhat.com/groups/node/[GROUP_ID]/edit

# Step 4: Contact customer if needed
# Request portal group access restoration
```

**Prevention:**
- Maintain regular communication with customers
- Document portal access requirements
- Set up access monitoring alerts

---

### **Q3: JIRA API connection timeouts or failures**

**Symptoms:**
- "JIRA API timeout" errors
- "Connection refused" to JIRA
- JIRA status enrichment fails

**Root Causes:**
- VPN connection issues
- JIRA API rate limiting
- Incorrect JIRA credentials
- Network firewall blocking

**Solution:**
```bash
# Step 1: Check VPN connection
# Ensure connected to Red Hat VPN

# Step 2: Test JIRA access manually
# Open https://issues.redhat.com in browser
# Verify you can access JIRA tickets

# Step 3: Check JIRA credentials (if using PAT)
# Verify Personal Access Token is valid
# Test with simple JIRA API call

# Step 4: Check rate limiting
pai-alerts --jira-status
# Look for rate limit warnings
```

**Prevention:**
- Monitor JIRA API usage
- Implement proper rate limiting
- Use VPN connection monitoring

---

## 🔧 **SYSTEM & CONFIGURATION ISSUES**

### **Q4: Template rendering errors or malformed content**

**Symptoms:**
- Portal content appears malformed
- Missing data in generated tables
- Template syntax errors
- Inconsistent formatting

**Root Causes:**
- Invalid customer configuration
- Template syntax errors
- Data format mismatches
- Missing required fields

**Solution:**
```bash
# Step 1: Validate system configuration
pai-rfe-deploy --validate

# Step 2: Check customer configuration
cat ~/.config/pai/customers/[customer].yaml
# Verify all required fields are present

# Step 3: Test template rendering
pai-test-[customer] --template-only

# Step 4: Check template syntax
# Review customer_templates.yaml for syntax errors
```

**Prevention:**
- Test all template changes in sandbox
- Use configuration validation tools
- Maintain template version control

---

### **Q5: Case discovery missing or incomplete**

**Symptoms:**
- Known RFE cases not appearing in reports
- Case count lower than expected
- Specific customers' cases missing

**Root Causes:**
- Incorrect account numbers
- Wrong product filters
- SBR Group filtering issues
- rhcase query limitations

**Solution:**
```bash
# Step 1: Verify account numbers
rhcase list [account_number] --months 3
# Check if cases appear in manual query

# Step 2: Check SBR Group filtering
rhcase list [account_number] --includefilter 'sbrGroup,Ansible'

# Step 3: Verify case product assignments
# Check Salesforce for correct product tagging

# Step 4: Expand search criteria if needed
rhcase list [account_number] --months 6 --includefilter 'sbrGroup,Ansible'
```

**Prevention:**
- Regularly audit case discovery accuracy
- Monitor account number changes
- Validate product tagging with customers

---

### **Q6: Automation scheduling not working**

**Symptoms:**
- Scheduled automation doesn't run
- Cron jobs not executing
- Inconsistent automation timing

**Root Causes:**
- Cron service not running
- Incorrect cron job syntax
- Path or permission issues
- System timezone problems

**Solution:**
```bash
# Step 1: Check cron service status
systemctl status cron
# or
systemctl status crond

# Step 2: Verify cron jobs installed
crontab -l | grep pai-rfe

# Step 3: Check cron job syntax
pai-rfe-schedule --status

# Step 4: Test manual execution
pai-rfe-[customer] --test

# Step 5: Reinstall cron jobs if needed
pai-rfe-schedule --install
```

**Prevention:**
- Monitor cron job execution
- Set up scheduling alerts
- Regular cron job validation

---

## 🚨 **CRITICAL SAFETY ISSUES**

### **Q7: Customers receiving unwanted email notifications**

**Symptoms:**
- Customers report receiving email notifications
- Portal subscription emails being sent
- Customer complaints about spam

**Root Causes:**
- "Send Subscription Notifications" checkbox checked
- Portal notification settings changed
- Browser automation failure
- Manual portal editing without unchecking

**CRITICAL SOLUTION:**
```bash
# STEP 1: IMMEDIATE ACTION - STOP AUTOMATION
pai-rfe-schedule --disable

# STEP 2: Verify notification settings
# Manually check each customer portal page
# Ensure "Send Subscription Notifications" is UNCHECKED

# STEP 3: Contact affected customers
# Send apology email explaining the issue
# Assure them it won't happen again

# STEP 4: Fix notification settings
# Manually uncheck notification boxes
# Test notification handling

# STEP 5: Resume automation only after verification
pai-rfe-schedule --enable
```

**Prevention:**
- Always verify notification settings
- Implement notification monitoring
- Test notification handling regularly
- Use API posting when available

---

### **Q8: Portal content corruption or data loss**

**Symptoms:**
- Portal page content appears corrupted
- Previous content overwritten
- Missing customer information

**Root Causes:**
- Browser automation interference
- Portal editing conflicts
- Template rendering errors
- Concurrent editing issues

**Solution:**
```bash
# Step 1: Stop automation immediately
pai-rfe-schedule --disable

# Step 2: Assess damage
# Review portal page content
# Identify what was lost or corrupted

# Step 3: Restore from backup if available
# Check if portal has revision history
# Restore previous version if possible

# Step 4: Manual content reconstruction
# Recreate content using automation tools
# Verify accuracy before publishing

# Step 5: Implement prevention measures
# Add content backup procedures
# Improve error handling
```

**Prevention:**
- Regular content backups
- Implement content validation
- Use API posting when possible
- Monitor portal changes

---

## 📊 **PERFORMANCE & MONITORING ISSUES**

### **Q9: Slow automation performance or timeouts**

**Symptoms:**
- Automation takes longer than usual
- Timeout errors during execution
- System becomes unresponsive

**Root Causes:**
- High system load
- Network latency issues
- Large case volumes
- Resource constraints

**Solution:**
```bash
# Step 1: Check system resources
pai-maintenance --health

# Step 2: Monitor automation performance
pai-rfe-monitor [customer] --performance

# Step 3: Optimize automation schedule
# Stagger customer automation times
# Reduce concurrent operations

# Step 4: Check network connectivity
# Test rhcase and portal response times
# Verify VPN performance
```

**Prevention:**
- Monitor system performance regularly
- Implement performance alerting
- Optimize automation schedules
- Plan for capacity scaling

---

### **Q10: Alert system not working or missing alerts**

**Symptoms:**
- No alerts for known issues
- Alert emails not being sent
- Alert dashboard showing stale data

**Root Causes:**
- Email configuration issues
- Alert system configuration errors
- Log file permissions
- Monitoring service failures

**Solution:**
```bash
# Step 1: Check alert system status
pai-alerts --system-status

# Step 2: Test alert generation
pai-alerts --test-alert

# Step 3: Verify email configuration
# Check email settings in alert configuration
# Test email delivery manually

# Step 4: Check log file permissions
ls -la /tmp/rfe-alerts/
# Ensure proper read/write permissions
```

**Prevention:**
- Regular alert system testing
- Monitor alert delivery
- Maintain email configuration
- Set up alert redundancy

---

## 🔄 **WORKFLOW & PROCESS ISSUES**

### **Q11: Inconsistent customer communication**

**Symptoms:**
- Different formatting across customers
- Inconsistent update timing
- Varying quality of communications

**Root Causes:**
- Template configuration differences
- Manual intervention inconsistencies
- Automation schedule variations
- Customer-specific customizations

**Solution:**
```bash
# Step 1: Audit customer configurations
pai-rfe-deploy --config-audit

# Step 2: Standardize templates
# Review customer_templates.yaml
# Ensure consistent base formatting

# Step 3: Synchronize schedules
pai-rfe-schedule --synchronize

# Step 4: Document customizations
# Record customer-specific requirements
# Maintain customization rationale
```

**Prevention:**
- Regular configuration audits
- Template standardization reviews
- Customer communication guidelines
- Change management processes

---

### **Q12: Customer feedback not being incorporated**

**Symptoms:**
- Repeated customer requests for changes
- Customer dissatisfaction with format
- Requests for different information

**Root Causes:**
- Lack of feedback collection process
- Inflexible template system
- Poor customer communication
- Change management gaps

**Solution:**
```bash
# Step 1: Collect customer feedback systematically
# Create feedback collection process
# Schedule regular customer check-ins

# Step 2: Analyze feedback patterns
# Identify common requests
# Prioritize high-impact changes

# Step 3: Implement template flexibility
# Add customization options
# Test changes in sandbox first

# Step 4: Communicate changes to customers
# Explain improvements made
# Ask for additional feedback
```

**Prevention:**
- Regular customer feedback sessions
- Flexible template system
- Change tracking and communication
- Customer satisfaction monitoring

---

## 🛠️ **TECHNICAL TROUBLESHOOTING TOOLS**

### **Diagnostic Commands**
```bash
# System health check
pai-rfe-deploy --validate

# Detailed system status
pai-rfe-deploy --status --verbose

# Customer-specific diagnostics
pai-rfe-[customer] --diagnose

# Log analysis
pai-alerts --analyze-logs

# Performance monitoring
pai-rfe-monitor --performance-report
```

### **Debug Mode**
```bash
# Enable debug logging
export PAI_DEBUG=true

# Run automation with debug output
pai-rfe-[customer] --debug

# Check debug logs
tail -f /tmp/pai-debug.log
```

### **Configuration Validation**
```bash
# Validate all configurations
pai-rfe-deploy --validate-config

# Test customer configuration
pai-test-[customer] --config-only

# Verify template syntax
pai-rfe-deploy --validate-templates
```

---

## 📞 **ESCALATION PROCEDURES**

### **When to Escalate**
- **Critical customer impact** (unwanted emails, data loss)
- **System-wide failures** affecting multiple customers
- **Security concerns** or data exposure
- **Repeated issues** not resolved by standard procedures

### **Escalation Contacts**
- **Level 1**: Self-service troubleshooting (this FAQ)
- **Level 2**: rfe-automation-support@redhat.com
- **Level 3**: Critical escalation (include "URGENT" in subject)
- **Emergency**: Customer impact requiring immediate response

### **Escalation Information to Include**
- **Customer(s) affected**
- **Issue description and symptoms**
- **Steps already taken**
- **Log files and error messages**
- **Business impact assessment**
- **Timeline for resolution needed**

---

## 📚 **ADDITIONAL RESOURCES**

### **Documentation References**
- [System Architecture](../docs/tam-deployment/03-SYSTEM-ARCHITECTURE.md)
- [Troubleshooting Guide](../docs/tam-deployment/04-TROUBLESHOOTING-GUIDE.md)
- [Best Practices Guide](tam-automation-best-practices.md)
- [Quick Reference Cards](quick-reference-cards.md)

### **Training Resources**
- **Sandbox Environment**: `pai-sandbox`
- **Video Training**: `/training/videos/`
- **Interactive Tutorials**: Available in sandbox

### **Community Support**
- **TAM Community**: tam-automation-community@redhat.com
- **Success Stories**: tam-success-stories@redhat.com
- **Feature Requests**: rfe-enhancement-requests@redhat.com

---

## 🎯 **PREVENTION CHECKLIST**

### **Daily Prevention**
- [ ] Check alert dashboard
- [ ] Verify automation success
- [ ] Monitor system performance
- [ ] Review customer feedback

### **Weekly Prevention**
- [ ] Run system maintenance
- [ ] Audit configuration changes
- [ ] Review performance metrics
- [ ] Update documentation

### **Monthly Prevention**
- [ ] Comprehensive system review
- [ ] Customer satisfaction survey
- [ ] Configuration backup
- [ ] Training updates

---

**Remember: Most issues can be prevented with proper monitoring and maintenance. When in doubt, test in sandbox first!**

---

*Troubleshooting FAQ v1.0*  
*For additional support: rfe-automation-support@redhat.com*
