# TAM RFE Tool - Onboarding Flow

**Date:** October 21, 2025  
**Purpose:** Mandatory onboarding process with token validation  
**Philosophy:** Block progress until all requirements are met

---

## Onboarding Philosophy: Validate Everything

### Core Principle
**"You cannot proceed until everything is configured and validated."**

**Why:**
- Tools fail silently without proper configuration
- Missing tokens cause cryptic errors later
- Better to fail fast during setup than during customer work
- Ensure TAM success from day one

### Validation Strategy
1. **Collect information** (tokens, customer data)
2. **Test immediately** with real API calls
3. **Block progress** if any validation fails
4. **Provide clear guidance** on fixing issues
5. **Only proceed** when everything works

---

## Onboarding Command: `tam-rfe onboard`

### Entry Point
```bash
# Start onboarding (interactive wizard)
$ tam-rfe onboard

# Or with customer name (still interactive for tokens)
$ tam-rfe onboard mycustomer
```

### Onboarding Flow

```
╭─────────────────────────────────────────────────────╮
│  TAM RFE Tool - Onboarding Wizard                  │
│  Let's get you set up (takes ~5 minutes)           │
╰─────────────────────────────────────────────────────╯

Step 1 of 5: JIRA API Token
Step 2 of 5: Customer Portal Token  
Step 3 of 5: Customer Information
Step 4 of 5: Validation Testing
Step 5 of 5: Final Configuration

Each step must pass before proceeding.
```

---

## Step 1: JIRA API Token (Mandatory)

### What User Sees
```
╭─────────────────────────────────────────────────────╮
│  Step 1 of 5: JIRA API Token                       │
╰─────────────────────────────────────────────────────╯

Why This Is Needed:
  Query Red Hat JIRA (issues.redhat.com) for RFE/Bug statuses.
  Without this, you cannot check if customer reports are current.

Required For:
  • tam-rfe check - Verify report statuses
  • tam-rfe update - Update reports with current statuses
  • tam-rfe watch - Monitor status changes

How To Get This Token:
  1. Go to: https://issues.redhat.com/secure/ViewProfile.jspa
  2. Click "Personal Access Tokens" tab
  3. Click "Create token"
  4. Name: "TAM RFE Tool"
  5. Permissions: Read-only
  6. Copy the token

Enter JIRA API Token (or 'skip' to configure later): _
```

### After Token Entered
```
⏳ Validating JIRA token...

Testing API access:
  ✓ Token format valid
  ✓ Connection to issues.redhat.com successful
  ✓ Authentication successful
  ✓ Permissions verified (read access confirmed)
  ✓ User: jbyrd@redhat.com (Jimmy Byrd)

Testing with sample query:
  ✓ Fetched AAPRFE-762 successfully
  ✓ Status: Backlog
  ✓ API response time: 1.2s

✅ JIRA token validated and saved securely!

Storage: System keyring (encrypted)
Location: ~/.config/taminator/ (secure)
```

### If Validation Fails
```
❌ JIRA Token Validation Failed

Problem: Invalid token or insufficient permissions

What We Tried:
  ✓ Token format valid
  ✗ API authentication failed (401 Unauthorized)

Common Issues:
  • Token has expired (check expiration date)
  • Incorrect token copied (check for extra spaces)
  • Token revoked (create new token)
  • Network issues (check Red Hat VPN connection)

Next Steps:
  1. Create a new token at: https://issues.redhat.com/...
  2. Ensure you copy the ENTIRE token
  3. Try again

❌ Cannot proceed without valid JIRA token.

Enter JIRA API Token (or 'quit' to exit): _
```

---

## Step 2: Customer Portal Token (Mandatory)

### What User Sees
```
╭─────────────────────────────────────────────────────╮
│  Step 2 of 5: Customer Portal Token                │
╰─────────────────────────────────────────────────────╯

Why This Is Needed:
  Post RFE/Bug tracker updates to customer portal groups.
  Without this, you must manually copy/paste reports.

Required For:
  • tam-rfe post - Auto-post reports to customer portal

How To Get This Token:
  1. Go to: https://access.redhat.com/management/api
  2. Click "Generate Token"
  3. Scopes: case:read, case:write
  4. Copy the token
  
Note: This token expires every 30 days (we'll remind you)

Enter Customer Portal Token (or 'skip' to configure later): _
```

### After Token Entered
```
⏳ Validating Customer Portal token...

Testing API access:
  ✓ Token format valid
  ✓ Connection to access.redhat.com successful
  ✓ Authentication successful
  ✓ Permissions verified (case read/write access)
  ✓ User: jbyrd@redhat.com

Testing portal access:
  ✓ Can access customer portal API
  ✓ Token expiration: 29 days remaining

✅ Customer Portal token validated and saved securely!

⚠️  Reminder: This token expires in 29 days
    We'll notify you 3 days before expiration.
```

---

## Step 3: Customer Information (Flexible)

### What User Sees
```
╭─────────────────────────────────────────────────────╮
│  Step 3 of 5: Customer Information                 │
╰─────────────────────────────────────────────────────╯

Let's set up your first customer (you can add more later).

You can configure a real customer now, or use test data to
explore the tool first.

What would you like to do?
  1) Configure real customer (recommended)
  2) Use test data to explore tool
  
Choice [1]: _
```

### Option 1: Real Customer
```
Customer Setup

Customer Name: _
(Examples: tdbank, wellsfargo, jpmc)

Account Number: _
(Red Hat account number, e.g., 540251)

Report File Location: _
(Leave empty for auto-detection)

SBR Groups (comma-separated): _
(Examples: Ansible, OpenShift, RHEL)
```

### Option 2: Test Data
```
✓ Creating test customer with sample data...

Test Customer Created:
  Name: testcustomer
  Account: 999999 (fake account)
  RFEs: 5 sample RFEs (fake JIRA IDs)
  Bugs: 2 sample bugs (fake JIRA IDs)
  Report: ~/testcustomer-rfe-tracker.md

This test customer lets you:
  • Run tam-rfe check testcustomer
  • Run tam-rfe update testcustomer  
  • See how the tool works without real data

You can configure real customers later with:
  tam-rfe onboard <customer>
```

---

## Step 4: Validation Testing (Critical)

### What User Sees
```
╭─────────────────────────────────────────────────────╮
│  Step 4 of 5: Validation Testing                   │
╰─────────────────────────────────────────────────────╯

Testing your configuration with real API calls...

Testing JIRA Access:
  ⏳ Fetching sample RFE status...
  ✓ AAPRFE-762: Backlog (response: 1.1s)
  ✓ AAPRFE-430: Backlog (response: 0.9s)

Testing Customer Portal Access:
  ⏳ Checking portal API...
  ✓ Portal API accessible
  ✓ Can read case data

Testing Report Generation:
  ⏳ Creating sample report...
  ✓ Report generated successfully
  ✓ File: /tmp/test-report.md

Testing tam-rfe check:
  ⏳ Running status comparison...
  ✓ Command works correctly
  ✓ Output formatting correct

All Tests Passed! ✅
```

### If Any Test Fails
```
❌ Validation Testing Failed

JIRA Access:
  ✓ AAPRFE-762: Success
  ✗ AAPRFE-430: Failed (404 Not Found)

Problem: JIRA access is intermittent

Possible Causes:
  • Red Hat VPN not connected
  • Network connectivity issues
  • JIRA service degradation

Next Steps:
  1. Connect to Red Hat VPN
  2. Test manually: rhcase jira fetch AAPRFE-430
  3. Try onboarding again

❌ Cannot proceed with unreliable JIRA access.

Options:
  [r] Retry validation tests
  [s] Skip validation (not recommended)
  [q] Quit and fix issues

Choice [r]: _
```

---

## Step 5: Final Configuration

### What User Sees
```
╭─────────────────────────────────────────────────────╮
│  Step 5 of 5: Final Configuration                  │
╰─────────────────────────────────────────────────────╯

Almost done! Let's finalize your setup.

Notification Preferences:
  Email alerts when RFEs change? [Y/n]: y
  Email address: jbyrd@redhat.com
  
  Slack notifications? [y/N]: n

Update Schedule:
  Auto-check reports daily? [Y/n]: y
  Preferred time: 08:00 AM

Configuration Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokens:
  ✓ JIRA API Token configured
  ✓ Customer Portal Token configured

Customers:
  ✓ testcustomer (test data for exploration)

Notifications:
  ✓ Email alerts enabled
  ✗ Slack disabled

Automation:
  ✓ Daily report checks at 08:00 AM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Save configuration? [Y/n]: y

✅ Configuration saved!

🎉 Onboarding Complete!
```

---

## Post-Onboarding: Quick Start Guide

```
╭─────────────────────────────────────────────────────╮
│  You're All Set! Quick Start Commands              │
╰─────────────────────────────────────────────────────╯

Try These Commands:

1. Check test customer report:
   $ tam-rfe check testcustomer

2. Update test customer report:
   $ tam-rfe update testcustomer

3. Add a real customer:
   $ tam-rfe onboard mycustomer

4. Check all customers:
   $ tam-rfe check --all

5. View configuration:
   $ tam-rfe config --show

Need help?
  • Documentation: https://gitlab.cee.redhat.com/jbyrd/taminator
  • Contact: jbyrd@redhat.com
  • TAM Slack: #tam-rfe-tool

Happy automating! 🚀
```

---

## Validation Requirements Matrix

### What Must Be Validated

| Item | Validation Test | Block If Fails? | Why |
|------|----------------|-----------------|-----|
| JIRA Token | Fetch sample JIRA issue | ✅ YES | Core functionality broken |
| Portal Token | Access portal API | ⚠️ WARN | Can still check reports |
| VPN Connection | Ping Red Hat internal | ⚠️ WARN | May be working offline |
| Network | HTTP connectivity | ✅ YES | Tool requires network |
| Customer Account | Valid account number | ⚠️ WARN | Can use test data |
| Report File | File exists or can create | ℹ️ INFO | Can create new |
| JIRA IDs | At least one valid JIRA | ⚠️ WARN | May be new customer |

**Legend:**
- ✅ BLOCK - Cannot proceed, must fix
- ⚠️ WARN - Can proceed but with limitations
- ℹ️ INFO - Informational, doesn't block

---

## Error Recovery Flow

### When Validation Fails

```python
def validate_and_recover():
    """Validation with smart recovery options."""
    
    results = run_validation_tests()
    
    if results.all_passed():
        return SUCCESS
    
    if results.has_blocking_failures():
        console.print("[red]❌ Critical validation failures[/red]")
        
        # Show what failed
        for failure in results.blocking_failures:
            console.print(f"  ✗ {failure.name}: {failure.error}")
        
        # Provide options
        console.print("\n[yellow]Options:[/yellow]")
        console.print("  [r] Retry validation")
        console.print("  [f] Fix configuration")
        console.print("  [h] Get help")
        console.print("  [q] Quit")
        
        choice = Prompt.ask("Choice", choices=["r", "f", "h", "q"])
        
        if choice == "r":
            return validate_and_recover()  # Retry
        elif choice == "f":
            return fix_configuration_wizard()
        elif choice == "h":
            return show_troubleshooting_guide()
        else:
            raise OnboardingAborted("User quit during validation")
    
    # Has warnings but not blocking
    if results.has_warnings():
        console.print("[yellow]⚠️  Some validation warnings[/yellow]")
        
        for warning in results.warnings:
            console.print(f"  ⚠️  {warning.name}: {warning.message}")
        
        proceed = Confirm.ask(
            "Proceed with warnings?",
            default=False
        )
        
        if not proceed:
            return fix_configuration_wizard()
    
    return SUCCESS
```

---

## Implementation Checklist

### Mandatory Onboarding Features

- [ ] Interactive wizard with 5 steps
- [ ] Token collection (JIRA + Portal)
- [ ] Real-time token validation with API tests
- [ ] Test customer data option
- [ ] Validation testing phase (block if fails)
- [ ] Clear error messages with recovery options
- [ ] Final configuration summary
- [ ] Post-onboarding quick start guide

### Token Validation Tests

- [ ] JIRA token: Fetch sample issue (AAPRFE-762)
- [ ] Portal token: Access portal API endpoint
- [ ] Token expiration check
- [ ] Permission verification
- [ ] Network connectivity test
- [ ] VPN status check (warn if not connected)

### Error Handling

- [ ] Invalid token format
- [ ] Authentication failures (401)
- [ ] Permission errors (403)
- [ ] Network timeouts
- [ ] VPN not connected
- [ ] Expired tokens

### User Experience

- [ ] Beautiful Rich UI (panels, progress bars)
- [ ] Clear step-by-step progress
- [ ] Cannot skip critical steps
- [ ] Option to use test data
- [ ] Recovery wizard for failures
- [ ] Help at every step

---

## Testing Strategy

### Test Scenarios

1. **Happy Path**
   - Valid JIRA token
   - Valid portal token
   - All validation passes
   - Result: Success

2. **Invalid JIRA Token**
   - Expired or wrong token
   - Validation fails
   - User gets clear error
   - Can retry with new token
   - Result: Blocked until fixed

3. **No VPN Connection**
   - JIRA API unreachable
   - Validation warns
   - Suggest connecting VPN
   - Result: Warn but allow proceed (for offline testing)

4. **Test Data Path**
   - Skip real customer setup
   - Create test customer
   - Generate sample report
   - Result: Can explore tool without real data

5. **Partial Configuration**
   - JIRA token works
   - Portal token fails
   - Result: Can check reports but not post them

---

## Success Criteria

### After Successful Onboarding:

- ✅ TAM has all required tokens configured
- ✅ All tokens validated with real API calls
- ✅ At least one customer configured (real or test)
- ✅ TAM can run `tam-rfe check` successfully
- ✅ TAM understands next steps
- ✅ Configuration saved securely

### Failure Is Not An Option:

- ❌ Cannot proceed without valid JIRA token
- ❌ Cannot proceed without passing validation tests
- ❌ Cannot proceed with invalid configuration
- ❌ Cannot save configuration until validated

**Bottom Line:** Onboarding must be bulletproof. Better to block during setup than fail during customer calls.

