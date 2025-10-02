# 🔧 RFE Automation - Troubleshooting Guide

**Comprehensive troubleshooting for TAMs and administrators**

---

## 🎯 Quick Diagnostic Commands

Before diving into specific issues, run these diagnostic commands:

```bash
# System health check
./bin/pai-rfe-deploy --validate

# Check recent alerts
./bin/pai-alerts --summary

# View system status
./bin/pai-rfe-schedule --status

# Check logs
tail -50 /tmp/rfe-automation-cron.log
```

---

## 🚨 Common Issues & Solutions

### 1. Authentication Issues

#### Problem: `rhcase` Authentication Failed
```
Error: Authentication Failed: Decryption failed
```

**Solution:**
```bash
# Re-authenticate with rhcase
rhcase config setup

# Verify authentication
rhcase --version
rhcase list [customer] --months 1

# If still failing, check VPN connection
ping access.redhat.com
```

#### Problem: Red Hat SSO Issues
```
Error: SSO authentication failed
```

**Solution:**
```bash
# Clear browser cache and cookies
# Re-authenticate in browser
# Verify SSO credentials are active

# Test SSO connectivity
curl -I https://access.redhat.com/
```

---

### 2. Customer Configuration Issues

#### Problem: Customer Not Found
```
Error: Unknown customer: mycustomer
```

**Solution:**
```bash
# Check customer configuration
cat config/my-customers.yaml

# Verify customer name matches exactly (case-sensitive)
# Re-run onboarding wizard if needed
./bin/pai-tam-onboard
```

#### Problem: No Cases Found for Customer
```
Warning: No RFE/Bug cases found for customer
```

**Solution:**
```bash
# Verify account numbers are correct
rhcase list [customer] --months 3

# Check SBR Group filtering
rhcase list [customer] --includefilter 'sbrGroup,Ansible'

# Verify customer has Ansible cases
rhcase analyze [case-number] --save-raw
```

---

### 3. Portal Access Issues

#### Problem: Portal Group Access Denied
```
Error: 403 Access denied to portal group
```

**Solution:**
```bash
# Verify you have access to the customer portal group
# Check group URL is correct
# Confirm group ID matches the URL

# Test portal access manually:
# 1. Open browser
# 2. Navigate to portal group URL
# 3. Verify you can view/edit content
```

#### Problem: Portal Content Not Updating
```
Warning: Portal update appeared successful but content unchanged
```

**Solution:**
```bash
# Check for UI overlays blocking interaction
./bin/pai-portal-debug [customer]

# Verify notification settings are disabled
# Check browser automation logs
tail -50 /tmp/pai-rfe-monitor-*.log

# Try manual portal update
./bin/pai-rfe-monitor [customer] --test
```

---

### 4. Automation Scheduling Issues

#### Problem: Cron Jobs Not Running
```
Error: Scheduled automation not executing
```

**Solution:**
```bash
# Check cron service status
systemctl status crond

# Verify cron jobs are installed
crontab -l | grep pai-rfe

# Check cron logs
tail -50 /var/log/cron

# Test manual execution
./bin/pai-rfe-monitor --all-daily
```

#### Problem: Automation Running But Failing
```
Error: Daily automation completing with failures
```

**Solution:**
```bash
# Check automation logs
tail -100 /tmp/rfe-automation-cron.log

# Run diagnostic test
./bin/pai-rfe-schedule --test

# Check individual customer status
./bin/pai-rfe-monitor [customer] --test
```

---

### 5. Performance Issues

#### Problem: Automation Taking Too Long
```
Warning: Automation execution time > 10 minutes
```

**Solution:**
```bash
# Check system resources
top
df -h

# Optimize case discovery
# Reduce time window for case queries
# Check network connectivity to Red Hat services

# Monitor execution time
./bin/pai-rfe-monitor [customer] --test | grep "execution_time"
```

#### Problem: High Memory Usage
```
Warning: System memory usage > 90%
```

**Solution:**
```bash
# Run maintenance cleanup
./bin/pai-maintenance --daily

# Check for memory leaks
ps aux | grep python | head -10

# Restart automation if needed
./bin/pai-rfe-schedule --remove
./bin/pai-rfe-schedule --install
```

---

### 6. Content Generation Issues

#### Problem: Malformed Portal Content
```
Error: Generated content contains formatting errors
```

**Solution:**
```bash
# Check template configuration
cat config/customer_templates.yaml

# Validate template syntax
./bin/pai-template-validate [customer]

# Test content generation
./bin/pai-rfe-monitor [customer] --test
cat /tmp/rfe-manual-post-[customer]-*.md
```

#### Problem: Missing JIRA Information
```
Warning: JIRA status not available for cases
```

**Solution:**
```bash
# Check if JIRA PAT token is configured
echo $JIRA_PAT_TOKEN

# Test JIRA connectivity
./bin/pai-jira-test

# Verify external trackers in case data
rhcase analyze [case-number] --save-raw | grep -A5 externalTrackers
```

---

### 7. Alert System Issues

#### Problem: Not Receiving Alerts
```
Issue: No email alerts for automation failures
```

**Solution:**
```bash
# Check alert system
./bin/pai-alerts --test

# Verify file-based alerts are working
ls -la /tmp/rfe-alerts/

# Check email configuration
# Note: System uses file-based alerts as primary method

# View recent alerts
./bin/pai-alerts --summary
```

#### Problem: Too Many Alerts
```
Issue: Receiving excessive alert notifications
```

**Solution:**
```bash
# Check alert frequency settings
cat src/rfe_monitoring_system.py | grep alert_thresholds

# Clean up old alerts
./bin/pai-alerts --clean

# Adjust alert sensitivity if needed
# Edit monitoring configuration
```

---

## 🔍 Advanced Diagnostics

### System Component Testing

```bash
# Test all components
./bin/pai-rfe-deploy --test-all

# Test individual components
python3 src/rfe_monitoring_system.py  # Test monitoring
python3 src/rfe_error_handler.py      # Test error handling
./bin/pai-maintenance --daily         # Test maintenance
```

### Network Connectivity Testing

```bash
# Test Red Hat service connectivity
ping access.redhat.com
curl -I https://access.redhat.com/hydra/rest/

# Test JIRA connectivity (if configured)
curl -I https://issues.redhat.com/

# Test internal network access
# (Requires VPN for some services)
```

### Configuration Validation

```bash
# Validate all configurations
./bin/pai-config-validate

# Check file permissions
ls -la bin/pai-*
ls -la config/
ls -la src/

# Verify Python dependencies
python3 -c "import selenium, requests, yaml, json; print('Dependencies OK')"
```

---

## 📊 Log Analysis

### Important Log Files

| Log File | Purpose | Location |
|----------|---------|----------|
| `rfe-automation-cron.log` | Daily automation | `/tmp/` |
| `pai-rfe-monitor-*.log` | Manual executions | `/tmp/` |
| `rfe-monitoring-*.log` | System monitoring | `/tmp/` |
| `pai-maintenance-*.log` | System maintenance | `/tmp/` |
| `alert-summary.json` | Alert dashboard | `/tmp/rfe-alerts/` |

### Log Analysis Commands

```bash
# Find recent errors
grep -i error /tmp/rfe-*.log | tail -20

# Check success rates
grep -c "✅" /tmp/rfe-automation-cron.log
grep -c "❌" /tmp/rfe-automation-cron.log

# Monitor real-time logs
tail -f /tmp/rfe-automation-cron.log

# Analyze performance
grep "execution_time" /tmp/pai-rfe-monitor-*.log | sort -n
```

---

## 🚨 Emergency Procedures

### Complete System Reset

```bash
# Stop all automation
./bin/pai-rfe-schedule --remove

# Clean up temporary files
./bin/pai-maintenance --monthly

# Reinstall system
./bin/pai-rfe-deploy --install --validate

# Reconfigure customers
./bin/pai-tam-onboard

# Restart automation
./bin/pai-rfe-schedule --install
```

### Rollback to Manual Process

If automation completely fails:

1. **Disable Automation**:
   ```bash
   ./bin/pai-rfe-schedule --remove
   ```

2. **Generate Manual Content**:
   ```bash
   ./bin/pai-rfe-monitor [customer] --test
   # Copy content from generated files in /tmp/
   ```

3. **Manual Portal Update**:
   - Navigate to customer portal page
   - Edit page content manually
   - **IMPORTANT**: Uncheck "Send Subscription Notifications"
   - Save changes

4. **Report Issue**:
   - Document the failure
   - Contact support team
   - Provide log files and error details

---

## 📞 Getting Help

### Self-Service Resources

1. **Documentation**: Check all guides in `docs/tam-deployment/`
2. **System Status**: Run `./bin/pai-rfe-deploy --status`
3. **Recent Alerts**: Check `./bin/pai-alerts --summary`
4. **Log Analysis**: Review relevant log files

### Support Escalation

When self-service doesn't resolve the issue:

1. **Gather Information**:
   ```bash
   # Create support bundle
   ./bin/pai-support-bundle
   ```

2. **Contact Support**:
   - **Email**: rfe-automation-support@redhat.com
   - **Slack**: #rfe-automation-support
   - **Include**: Support bundle, error description, steps to reproduce

3. **Emergency Contact**:
   - For critical issues affecting customer deliverables
   - Escalate through normal TAM management channels

---

## 🔧 Preventive Maintenance

### Daily Checks

```bash
# Quick health check (automated)
./bin/pai-rfe-deploy --validate

# Review alerts
./bin/pai-alerts --latest
```

### Weekly Maintenance

```bash
# Comprehensive maintenance
./bin/pai-maintenance --weekly

# Review system performance
./bin/pai-metrics --weekly-report
```

### Monthly Tasks

```bash
# Full system maintenance
./bin/pai-maintenance --monthly

# Update documentation
# Review customer configurations
# Plan system improvements
```

---

## 📈 Performance Optimization

### Improving Execution Speed

1. **Optimize Case Queries**:
   - Reduce time windows for case discovery
   - Use specific account number filtering
   - Enable SBR Group filtering

2. **System Resources**:
   - Ensure adequate memory (2GB+)
   - Check disk space regularly
   - Monitor network connectivity

3. **Configuration Tuning**:
   - Adjust timeout values
   - Optimize retry logic
   - Enable caching where appropriate

### Monitoring Performance

```bash
# Track execution times
grep "execution_time" /tmp/pai-rfe-monitor-*.log | \
  awk '{print $NF}' | sort -n | tail -10

# Monitor success rates
./bin/pai-metrics --success-rate

# Check resource usage
./bin/pai-metrics --system-resources
```

---

## ✅ Troubleshooting Checklist

Before contacting support, verify:

- [ ] System health check passes: `./bin/pai-rfe-deploy --validate`
- [ ] Authentication is working: `rhcase list [customer] --months 1`
- [ ] Customer configuration is correct: `cat config/my-customers.yaml`
- [ ] Portal access is available: Manual browser test
- [ ] Recent logs reviewed: `tail -50 /tmp/rfe-automation-cron.log`
- [ ] Alert system is functional: `./bin/pai-alerts --test`
- [ ] System resources are adequate: `df -h && free -h`

---

**🔧 Most issues can be resolved with the solutions in this guide. For complex problems, don't hesitate to contact the support team!**

---

*RFE Automation System - Troubleshooting Guide*  
*Version 1.0 - Created for Global TAM Deployment*
