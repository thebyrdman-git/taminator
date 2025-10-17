# 🧪 Phase 3 Integration Testing Guide

## 🎯 Overview

This guide provides comprehensive end-to-end testing procedures for all Phase 3 integrations:
- ✅ Email delivery (SMTP)
- ✅ Customer Portal Private Groups (CPG)
- ✅ Real rhcase data integration
- ✅ Salesforce write operations

**Test Coverage:**
- Individual integration tests
- Cross-integration tests
- Full workflow tests
- Error handling and fallback tests

---

## 📋 Pre-Test Checklist

Before running tests, ensure:

- [ ] Test environment configured
- [ ] Test customer data available
- [ ] Non-production Salesforce instance (if testing writes)
- [ ] SMTP credentials configured (test account)
- [ ] rhcase authenticated
- [ ] Test email inbox accessible

---

## 🧪 Test Suite 1: Email Integration

### Test 1.1: Email Configuration

```bash
# Verify email configuration
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.email_handler import EmailHandler

handler = EmailHandler()
print(f"SMTP Server: {handler.smtp_server}")
print(f"SMTP Port: {handler.smtp_port}")
print(f"SMTP User: {handler.smtp_username}")
print(f"From Email: {handler.from_email}")
print(f"Configured: {handler.is_configured()}")
EOF
```

**Expected Output:**
```
SMTP Server: smtp.gmail.com
SMTP Port: 587
SMTP User: your-email@gmail.com
From Email: your-email@gmail.com
Configured: True
```

### Test 1.2: Send Test Email

```bash
# Send simple test email
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.email_handler import get_email_handler

handler = get_email_handler()
success = handler._send_email(
    to_email="your-test-email@example.com",
    subject="Taminator Test Email",
    body="This is a test email from Taminator Phase 3 integration testing.",
    html_body="<h1>Test Email</h1><p>This is a test.</p>"
)

if success:
    print("✅ Test email sent successfully")
else:
    print("❌ Test email failed")
EOF
```

**Expected Output:**
```
✅ Test email sent successfully
```

**Verification:** Check inbox for test email

### Test 1.3: Generate Agenda with Email

```bash
# Generate agenda and email it
tam-generate-agenda --customer test --email your-test-email@example.com

# Expected output:
# 📧 Emailing agenda to your-test-email@example.com...
# ✅ Email sent successfully!
```

**Verification:** Check inbox for agenda email with HTML formatting

### Test 1.4: Backlog Report with Email

```bash
# Generate backlog report and email it
tam-backlog-cleanup --customer test --email your-test-email@example.com

# Expected output:
# 📧 Emailing report to your-test-email@example.com...
# ✅ Email sent successfully!
```

**Verification:** Check inbox for backlog report email

---

## 🧪 Test Suite 2: CPG Integration

### Test 2.1: CPG Configuration

```bash
# Verify CPG configuration
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.cpg_handler import CPGConfig

config = CPGConfig()
print(f"API Base URL: {config.api_base_url}")
print(f"Use Kerberos: {config.use_kerberos}")
print(f"Configured: {config.is_configured()}")
EOF
```

**Expected Output:**
```
API Base URL: https://api.access.redhat.com/rs
Use Kerberos: True
Configured: True
```

### Test 2.2: CPG Authentication

```bash
# Test Kerberos ticket
klist

# Expected output:
# Ticket cache: KEYRING:persistent:1000:krb_ccache_...
# Default principal: jbyrd@REDHAT.COM
```

### Test 2.3: Post T3 Article to CPG

```bash
# Post T3 recommendations to CPG
tam-t3-reader --customer test --recommend --post-cpg

# Expected output:
# 📤 Posting 4 articles to CPG...
# ✅ Posted 4 article(s) to test's private group
```

**Verification:** Check Customer Portal Private Group for posted articles

### Test 2.4: Post Coverage Announcement to CPG

```bash
# Post coverage announcement
tam-coverage --tam "Test TAM" --tam-email test@redhat.com \
  --backup "Backup TAM" --backup-email backup@redhat.com \
  --start 2025-11-04 --end 2025-11-15 --customer test \
  --post-cpg

# Expected output:
# 📤 Posting announcement to CPG...
# ✅ Posted to test's private group
```

**Verification:** Check Customer Portal for coverage announcement

---

## 🧪 Test Suite 3: rhcase Integration

### Test 3.1: rhcase Configuration

```bash
# Verify rhcase is available
tam-verify --test rhcase

# Expected output:
# ✅ rhcase available and functional
# ✅ rhcase connectivity test PASSED
```

### Test 3.2: Fetch Real Case Data

```bash
# Test rhcase data fetching
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.rhcase_handler import get_rhcase_handler

handler = get_rhcase_handler()

# Fetch open cases
cases = handler.get_open_cases("test-customer")
print(f"✅ Found {len(cases)} open cases")

if cases:
    case = cases[0]
    print(f"\nSample case:")
    print(f"  Number: {case.get('number')}")
    print(f"  Summary: {case.get('summary')}")
    print(f"  Severity: {case.get('severity')}")
    print(f"  Status: {case.get('status')}")
EOF
```

**Expected Output:**
```
✅ Found 15 open cases

Sample case:
  Number: 04280915
  Summary: AAP networking issue
  Severity: 2
  Status: open
```

### Test 3.3: Generate Agenda with Real Data

```bash
# Generate agenda using real rhcase data
tam-generate-agenda --customer jpmc --print

# Expected output:
# 🔍 Fetching open cases...
# ✅ Found 15 open case(s)
# ✅ Fetching recently closed cases...
# ✅ Found 5 recently closed case(s)
```

**Verification:** Agenda shows actual case numbers, summaries, severities

### Test 3.4: Backlog Cleanup with Real Data

```bash
# Run backlog cleanup with real data
tam-backlog-cleanup --customer jpmc --print

# Expected output:
# 🔍 Fetching open cases...
# ✅ Found 12 open case(s)
# 🔍 Analyzing 12 cases...
```

**Verification:** Report shows actual case analysis

---

## 🧪 Test Suite 4: Salesforce Integration

### Test 4.1: Salesforce Configuration

```bash
# Verify Salesforce configuration
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import SalesforceConfig

config = SalesforceConfig()
print(f"Instance URL: {config.instance_url}")
print(f"Client ID: {config.client_id[:10]}..." if config.client_id else "Client ID: (not set)")
print(f"Username: {config.username}")
print(f"Configured: {config.is_configured()}")
EOF
```

**Expected Output:**
```
Instance URL: https://redhat.my.salesforce.com
Client ID: 3MVG9A2kN3...
Username: jbyrd@redhat.com
Configured: True
```

### Test 4.2: Salesforce Authentication

```bash
# Test authentication
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import get_salesforce_handler

handler = get_salesforce_handler()

if handler._authenticate():
    print("✅ Authentication successful")
    print(f"   Access token: {handler.config.access_token[:20]}...")
else:
    print("❌ Authentication failed")
EOF
```

**Expected Output:**
```
✅ Authentication successful
   Access token: 00D8c0000004Z7o!AQ...
```

### Test 4.3: Add Test Comment (Non-Production)

**⚠️ WARNING: Only run on TEST/SANDBOX Salesforce instance!**

```bash
# Add test comment to a case
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import add_case_comment

# Replace with actual TEST case number
success = add_case_comment(
    case_number="TEST12345",
    comment="Test comment from Taminator Phase 3 integration testing",
    is_public=False  # Internal only for testing
)

if success:
    print("✅ Test comment added successfully")
else:
    print("❌ Failed to add comment")
EOF
```

**Verification:** Check Salesforce case for new comment

### Test 4.4: Update Case Status (Non-Production)

**⚠️ WARNING: Only run on TEST/SANDBOX Salesforce instance!**

```bash
# Update case status
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import update_case_status

# Replace with actual TEST case number
success = update_case_status(
    case_number="TEST12345",
    status="In Progress",
    comment="Status updated by Taminator integration test"
)

if success:
    print("✅ Status updated successfully")
else:
    print("❌ Failed to update status")
EOF
```

**Verification:** Check Salesforce case status changed

---

## 🧪 Test Suite 5: Cross-Integration Tests

### Test 5.1: Email + rhcase Integration

**Test:** Generate agenda with real cases and email it

```bash
# Full workflow: rhcase → agenda → email
tam-generate-agenda --customer jpmc --email your-test-email@example.com

# Expected output:
# 🔍 Fetching open cases...
# ✅ Found 15 open case(s)
# ✅ Fetching recently closed cases...
# ✅ Found 5 recently closed case(s)
# 📧 Emailing agenda to your-test-email@example.com...
# ✅ Email sent successfully!
```

**Verification:**
- Email received with HTML-formatted agenda
- Agenda contains actual case numbers from rhcase
- Case summaries are accurate

### Test 5.2: Email + CPG Integration

**Test:** Generate T3 recommendations, post to CPG, and email

```bash
# Full workflow: T3 → CPG + Email
tam-t3-reader --customer jpmc --recommend --post-cpg --email your-test-email@example.com

# Expected output:
# 📤 Posting 4 articles to CPG...
# ✅ Posted 4 article(s) to jpmc's private group
# 📧 Emailing T3 report to your-test-email@example.com...
# ✅ Email sent successfully!
```

**Verification:**
- Articles posted to CPG
- Email received with T3 recommendations
- Both outputs contain same recommendations

### Test 5.3: rhcase + Salesforce Integration (Framework Test)

**Test:** Fetch cases from rhcase and simulate Salesforce update

```bash
# Fetch cases and test Salesforce framework
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.rhcase_handler import get_rhcase_handler
from foundation.salesforce_handler import get_salesforce_handler

# Get cases from rhcase
rhcase = get_rhcase_handler()
cases = rhcase.get_open_cases("jpmc")

print(f"✅ rhcase: Found {len(cases)} cases")

# Test Salesforce handler (no actual writes)
sf = get_salesforce_handler()
if sf.config.is_configured():
    print("✅ Salesforce: Configured and ready")
else:
    print("ℹ️  Salesforce: Not configured (framework ready)")

# Simulate workflow
print(f"\n📋 Workflow simulation:")
print(f"   1. Fetch {len(cases)} cases from rhcase")
print(f"   2. Generate agenda")
print(f"   3. Post updates to {len(cases)} cases in Salesforce")
print(f"   ✅ Framework ready for automation")
EOF
```

**Expected Output:**
```
✅ rhcase: Found 15 cases
✅ Salesforce: Configured and ready

📋 Workflow simulation:
   1. Fetch 15 cases from rhcase
   2. Generate agenda
   3. Post updates to 15 cases in Salesforce
   ✅ Framework ready for automation
```

---

## 🧪 Test Suite 6: Error Handling & Fallbacks

### Test 6.1: rhcase Unavailable Fallback

```bash
# Temporarily make rhcase unavailable
export RHCASE_PATH="/nonexistent/rhcase"

# Generate agenda (should fall back to sample data)
tam-generate-agenda --customer test --print

# Expected output:
# 🔍 Fetching open cases...
# ⚠️  Error fetching cases: ...
# ℹ️  Using sample data for demonstration

# Restore
unset RHCASE_PATH
```

**Verification:** Tool works with sample data, doesn't crash

### Test 6.2: Email Not Configured

```bash
# Temporarily unset email config
export SMTP_SERVER=""

# Try to email agenda
tam-generate-agenda --customer test --email test@example.com

# Expected output:
# 📧 Emailing agenda to test@example.com...
# ⚠️  Email failed. Agenda saved to: ~/tam-agendas/...
# ℹ️  Configure email: Set SMTP_* environment variables

# Restore email config
```

**Verification:** Tool saves file, provides helpful error message

### Test 6.3: CPG Not Configured

```bash
# Post without CPG configured
tam-t3-reader --customer test --post-cpg

# Expected output:
# 📤 Posting 4 articles to CPG...
# ⚠️  CPG posting failed. Articles saved to file
# ℹ️  Configure CPG: Set CPG_* environment variables or create cpg.conf
```

**Verification:** Tool gracefully handles missing CPG config

### Test 6.4: Salesforce Not Configured

```bash
# Test Salesforce without config
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import add_case_comment

# Try to add comment without config
success = add_case_comment("TEST12345", "Test comment")

# Expected: Returns False with error message
if not success:
    print("✅ Graceful failure: Salesforce not configured")
EOF
```

**Verification:** No crashes, helpful error messages

---

## 📊 Test Results Summary

### Test Report Template

```markdown
# Phase 3 Integration Test Results

**Date:** YYYY-MM-DD
**Tester:** [Your Name]
**Environment:** [Production/Test/Local]

## Email Integration
- [ ] Configuration: PASS/FAIL
- [ ] Send test email: PASS/FAIL
- [ ] Generate agenda with email: PASS/FAIL
- [ ] Backlog report with email: PASS/FAIL

## CPG Integration
- [ ] Configuration: PASS/FAIL
- [ ] Authentication: PASS/FAIL
- [ ] Post T3 articles: PASS/FAIL
- [ ] Post coverage announcement: PASS/FAIL

## rhcase Integration
- [ ] Configuration: PASS/FAIL
- [ ] Fetch real case data: PASS/FAIL
- [ ] Generate agenda with real data: PASS/FAIL
- [ ] Backlog cleanup with real data: PASS/FAIL

## Salesforce Integration
- [ ] Configuration: PASS/FAIL
- [ ] Authentication: PASS/FAIL
- [ ] Add test comment: PASS/FAIL
- [ ] Update case status: PASS/FAIL

## Cross-Integration Tests
- [ ] Email + rhcase: PASS/FAIL
- [ ] Email + CPG: PASS/FAIL
- [ ] rhcase + Salesforce framework: PASS/FAIL

## Error Handling
- [ ] rhcase unavailable fallback: PASS/FAIL
- [ ] Email not configured: PASS/FAIL
- [ ] CPG not configured: PASS/FAIL
- [ ] Salesforce not configured: PASS/FAIL

## Overall Status
- [ ] All tests passed
- [ ] Some tests failed (see notes)
- [ ] Production ready
- [ ] Needs fixes

## Notes
[Add any additional notes, issues found, or recommendations]
```

---

## ✅ Production Readiness Checklist

Before deploying to production:

### Configuration
- [ ] All configuration files secured (`chmod 600`)
- [ ] No secrets in git repository
- [ ] Environment variables documented
- [ ] Test environment verified

### Integration Tests
- [ ] All individual integration tests passed
- [ ] All cross-integration tests passed
- [ ] Error handling verified
- [ ] Fallback mechanisms work

### Documentation
- [ ] All configuration guides reviewed
- [ ] Troubleshooting guides complete
- [ ] Security best practices documented
- [ ] User training materials available

### Security
- [ ] API credentials secured
- [ ] Access controls configured
- [ ] Audit logging enabled
- [ ] Compliance requirements met

### Monitoring
- [ ] Error logging configured
- [ ] API usage monitoring set up
- [ ] Alert thresholds defined
- [ ] Backup procedures documented

---

## 📞 Support

### Issues During Testing

1. **Check logs:** Tool output shows warnings/errors
2. **Review configuration:** Verify all credentials set
3. **Test individually:** Isolate failing integration
4. **Check documentation:** Review relevant configuration guide
5. **Ask for help:** Slack #tam-automation

### Reporting Test Failures

When reporting failures, include:
- Test suite and test number
- Complete error output
- Configuration status (is_configured() output)
- Environment details (VPN status, network, etc.)

---

**"I'll be back"** — with fully tested integrations! 🧪✅

*Taminator Phase 3 Integration Testing Guide*  
*Terminate untested code, embrace quality assurance*


