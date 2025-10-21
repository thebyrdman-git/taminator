# Auth-Box: Comprehensive Authentication Audit

**Date:** October 21, 2025  
**Component:** auth-box audit submodule  
**Purpose:** Comprehensive audit of ALL authentication requirements

---

## Overview

The **auth-box audit** submodule provides a complete assessment of authentication health across all requirements.

### Purpose
- Identify missing or invalid authentication
- Check expiration dates and warn proactively
- Verify connectivity to all required services
- Provide actionable remediation steps
- Generate audit reports for compliance

---

## Command: `tam-rfe auth-audit`

### Basic Usage
```bash
# Run comprehensive authentication audit
$ tam-rfe auth-audit

# Quick check (faster, less detailed)
$ tam-rfe auth-audit --quick

# Generate report file
$ tam-rfe auth-audit --report audit-report.md

# JSON output for automation
$ tam-rfe auth-audit --format json

# Check specific authentication types
$ tam-rfe auth-audit --check vpn,jira,portal
```

---

## Example Output: Full Audit

```bash
$ tam-rfe auth-audit

╭─────────────────────────────────────────────────────╮
│  Auth-Box: Comprehensive Authentication Audit      │
│  Started: 2025-10-21 09:15:32                      │
╰─────────────────────────────────────────────────────╯

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 API Tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JIRA API Token
  Status:     ✅ Valid
  Storage:    System keyring (encrypted)
  User:       jbyrd@redhat.com
  Permissions: Read-only access to JIRA issues
  Expires:    2026-01-15 (87 days remaining)
  Last Used:  2025-10-21 08:45:12
  Test Query: ✅ Successfully fetched AAPRFE-762

Customer Portal Token
  Status:     ⚠️  Valid but expiring soon
  Storage:    System keyring (encrypted)
  User:       jbyrd@redhat.com
  Permissions: case:read, case:write
  Expires:    2025-10-23 (2 days remaining) ⚠️
  Last Used:  2025-10-19 14:23:01
  Test Query: ✅ Successfully accessed portal API
  
  ⚠️  ACTION REQUIRED:
      Renew token before 2025-10-23
      Command: tam-rfe config --renew-token portal

Hydra API Token
  Status:     ✅ Valid
  Storage:    System keyring (encrypted)
  User:       jbyrd@redhat.com
  Permissions: Read-only customer data
  Expires:    Never (permanent token)
  Last Used:  2025-10-20 16:12:45
  Test Query: ✅ Successfully accessed Hydra API

SupportShell Token
  Status:     ❌ Not configured
  Storage:    Not found
  
  ❌ MISSING TOKEN:
      Required for: tam-active-cases, tam-case-processor
      How to obtain:
        1. Go to: https://supportshell.redhat.com
        2. Profile → API Tokens
        3. Generate new token
        4. Run: tam-rfe config --add-token supportshell

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Network & Connectivity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Red Hat VPN
  Status:       ✅ Connected
  Connection:   1 - Red Hat Global VPN
  Server:       plv-vpn-01.redhat.com
  Connected:    2025-10-21 07:30:15 (1h 45m ago)
  IP Address:   10.11.12.13
  DNS Servers:  10.2.70.215, 10.11.5.19
  
  Connectivity Tests:
    ✅ issues.redhat.com (JIRA) - 24ms
    ✅ hydra.corp.redhat.com - 18ms
    ✅ gitlab.cee.redhat.com - 31ms
    ✅ access.redhat.com (Portal) - 42ms

Internet Connectivity
  Status:       ✅ Connected
  Public IP:    [hidden for security]
  DNS:          ✅ Resolving external domains
  Latency:      12ms (to 8.8.8.8)

Internal Network Access
  Status:       ✅ Can reach Red Hat internal services
  Corp Network: ✅ Reachable
  VPN Required: ✅ Currently connected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎫 Kerberos & SSO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Kerberos Ticket
  Status:       ✅ Valid
  Principal:    jbyrd@IPA.REDHAT.COM
  Issued:       2025-10-20 18:30:00
  Expires:      2025-10-21 18:30:00 (9h 15m remaining)
  Renew Until:  2025-10-28 18:30:00
  Ticket Cache: FILE:/tmp/krb5cc_1000
  
  ⚠️  REMINDER:
      Ticket expires in 9 hours
      Renew with: kinit

SSO Session
  Status:       ✅ Active
  Provider:     Red Hat SSO
  Session ID:   [hidden]
  Expires:      2025-10-21 17:30:00 (8h 15m remaining)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 SSH Keys & Git Access
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GitLab SSH Access
  Status:       ✅ Working
  Host:         gitlab.cee.redhat.com
  Key Type:     ED25519
  Key Location: ~/.ssh/id_ed25519
  Key Added:    ✅ Loaded in ssh-agent
  Test:         ✅ Successfully authenticated as jbyrd
  Last Used:    2025-10-20 14:12:03

GitHub SSH Access
  Status:       ⚠️  Not configured (optional)
  Note:         Only needed for public repository work

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ Security & Compliance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Token Storage Security
  Keyring:      ✅ Using system keyring (Secret Service)
  Encryption:   ✅ Tokens encrypted at rest
  Permissions:  ✅ Config files have correct permissions (600)
  Backup:       ✅ Encrypted backup available

Password Policy Compliance
  Token Rotation: ⚠️  Customer Portal token should be rotated (28 days old)
  Strong Auth:    ✅ MFA enabled on all services
  Least Privilege: ✅ All tokens have minimal required permissions

Audit Logging
  Status:       ✅ Enabled
  Log Location: ~/.config/taminator/audit.log
  Retention:    90 days
  Last Entry:   2025-10-21 09:10:15

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Status: ⚠️  MOSTLY HEALTHY (2 warnings, 1 error)

Authentication Status:
  ✅ Working:    5 (JIRA, Portal, Hydra, VPN, GitLab)
  ⚠️  Warnings:   2 (Portal token expiring, Kerberos expiring soon)
  ❌ Errors:     1 (SupportShell token missing)

Immediate Actions Required:
  1. ⚠️  Renew Customer Portal token (expires in 2 days)
  2. ❌ Configure SupportShell token (required for case commands)

Recommended Actions:
  3. ℹ️  Renew Kerberos ticket (expires in 9 hours)
  4. ℹ️  Rotate Customer Portal token (best practice: every 30 days)

Next Audit:
  Recommended: Daily (automatic)
  Last Audit:  2025-10-20 09:00:00 (24 hours ago)
  
Run specific fixes:
  $ tam-rfe config --renew-token portal
  $ tam-rfe config --add-token supportshell
  $ kinit  # Renew Kerberos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Audit completed in 3.2 seconds
Report saved to: ~/.config/taminator/audit-reports/audit-20251021-091532.md
```

---

## Quick Audit Output

```bash
$ tam-rfe auth-audit --quick

╭─────────────────────────────────────────────────────╮
│  Auth-Box: Quick Audit                             │
╰─────────────────────────────────────────────────────╯

✅ JIRA Token:          Valid (87 days)
⚠️  Portal Token:        Valid (2 days) - EXPIRING SOON
✅ Hydra Token:         Valid
❌ SupportShell Token:  NOT CONFIGURED
✅ VPN:                 Connected
✅ Kerberos:            Valid (9 hours)
✅ GitLab SSH:          Working

Status: ⚠️  2 warnings, 1 error

Actions needed:
  1. Renew Portal token: tam-rfe config --renew-token portal
  2. Add SupportShell token: tam-rfe config --add-token supportshell
```

---

## JSON Output (for Automation)

```bash
$ tam-rfe auth-audit --format json
```

```json
{
  "audit_id": "audit-20251021-091532",
  "timestamp": "2025-10-21T09:15:32Z",
  "status": "warnings",
  "summary": {
    "working": 5,
    "warnings": 2,
    "errors": 1
  },
  "tokens": {
    "jira": {
      "status": "valid",
      "expires": "2026-01-15T00:00:00Z",
      "days_remaining": 87,
      "last_used": "2025-10-21T08:45:12Z",
      "test_passed": true
    },
    "portal": {
      "status": "expiring_soon",
      "expires": "2025-10-23T00:00:00Z",
      "days_remaining": 2,
      "warning": "Token expires in 2 days",
      "action": "renew",
      "test_passed": true
    },
    "supportshell": {
      "status": "missing",
      "error": "Token not configured",
      "action": "configure"
    }
  },
  "network": {
    "vpn": {
      "status": "connected",
      "server": "plv-vpn-01.redhat.com",
      "uptime_hours": 1.75
    },
    "connectivity": {
      "jira": {"reachable": true, "latency_ms": 24},
      "hydra": {"reachable": true, "latency_ms": 18},
      "gitlab": {"reachable": true, "latency_ms": 31}
    }
  },
  "kerberos": {
    "status": "valid",
    "expires": "2025-10-21T18:30:00Z",
    "hours_remaining": 9.25,
    "principal": "jbyrd@IPA.REDHAT.COM"
  },
  "ssh": {
    "gitlab": {
      "status": "working",
      "key_type": "ED25519",
      "test_passed": true
    }
  },
  "actions_required": [
    {
      "priority": "high",
      "type": "renew_token",
      "target": "portal",
      "command": "tam-rfe config --renew-token portal",
      "reason": "Token expires in 2 days"
    },
    {
      "priority": "high",
      "type": "configure_token",
      "target": "supportshell",
      "command": "tam-rfe config --add-token supportshell",
      "reason": "Required for case commands"
    }
  ]
}
```

---

## Audit Scheduling

### Automatic Daily Audits

```bash
# Enable daily automatic audits
$ tam-rfe config --enable-daily-audit

Daily audit configured:
  Schedule: Every day at 08:00 AM
  Action: Run audit, send report if warnings/errors
  Report: Email to jbyrd@redhat.com
```

### Cron Integration

```bash
# Daily audit at 8 AM
0 8 * * * /home/jbyrd/.local/bin/tam-rfe auth-audit --format json > /tmp/auth-audit.json && /home/jbyrd/.local/bin/tam-rfe-audit-reporter /tmp/auth-audit.json
```

---

## Audit Report Generation

### Markdown Report

```bash
$ tam-rfe auth-audit --report audit-report.md

✅ Report generated: audit-report.md

Report includes:
  • Complete authentication status
  • Expiration warnings
  • Action items with commands
  • Historical trends
  • Compliance checklist
```

### Email Report

```bash
# Email report to TAM
$ tam-rfe auth-audit --email jbyrd@redhat.com

📧 Email sent to: jbyrd@redhat.com
Subject: Auth-Box Audit Report - 2 warnings, 1 error
```

---

## Audit Categories

### 1. Token Health Check
**What's Checked:**
- Token existence
- Token validity (API test)
- Expiration dates
- Storage security
- Last used timestamp

**Tests Performed:**
```python
def audit_token(token_type: AuthType) -> TokenAuditResult:
    """Comprehensive token health check."""
    token = get_token(token_type)
    
    if not token:
        return TokenAuditResult(
            status=Status.MISSING,
            error="Token not configured"
        )
    
    # Test token with real API call
    api_test = test_token_api_access(token_type, token)
    
    if not api_test.success:
        return TokenAuditResult(
            status=Status.INVALID,
            error=f"API test failed: {api_test.error}"
        )
    
    # Check expiration
    expiration = get_token_expiration(token_type, token)
    days_remaining = (expiration - datetime.now()).days
    
    if days_remaining < 3:
        return TokenAuditResult(
            status=Status.EXPIRING_SOON,
            warning=f"Expires in {days_remaining} days"
        )
    
    return TokenAuditResult(
        status=Status.VALID,
        days_remaining=days_remaining,
        last_used=get_last_used(token_type)
    )
```

### 2. Network Connectivity Audit
**What's Checked:**
- VPN connection status
- Connectivity to internal services
- DNS resolution
- Network latency
- Route availability

**Tests Performed:**
```python
def audit_network() -> NetworkAuditResult:
    """Check network connectivity to all required services."""
    results = {}
    
    # VPN status
    vpn_status = check_vpn_connection()
    results['vpn'] = vpn_status
    
    # Test each service
    services = [
        ('jira', 'https://issues.redhat.com'),
        ('hydra', 'https://hydra.corp.redhat.com'),
        ('gitlab', 'https://gitlab.cee.redhat.com'),
        ('portal', 'https://access.redhat.com'),
    ]
    
    for name, url in services:
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = (time.time() - start) * 1000
            results[name] = ServiceStatus(
                reachable=True,
                latency_ms=latency,
                status_code=response.status_code
            )
        except Exception as e:
            results[name] = ServiceStatus(
                reachable=False,
                error=str(e)
            )
    
    return NetworkAuditResult(services=results)
```

### 3. Kerberos & SSO Audit
**What's Checked:**
- Kerberos ticket validity
- Ticket expiration
- SSO session status
- Renewal capability

### 4. SSH Key Audit
**What's Checked:**
- SSH key existence
- Key loaded in ssh-agent
- Access to GitLab
- Key type and strength

### 5. Security & Compliance Audit
**What's Checked:**
- Token storage security
- File permissions
- Encryption status
- Backup availability
- Rotation compliance
- Audit logging

---

## Audit History & Trends

### Historical Tracking

```bash
$ tam-rfe auth-audit --history

╭─────────────────────────────────────────────────────╮
│  Audit History (Last 7 Days)                       │
╰─────────────────────────────────────────────────────╯

Date         Status   Warnings  Errors  Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2025-10-21   ⚠️       2         1       Portal expiring, SS missing
2025-10-20   ✅       0         0       All healthy
2025-10-19   ⚠️       1         0       Kerberos expired
2025-10-18   ✅       0         0       All healthy
2025-10-17   ⚠️       1         1       VPN down, SS missing
2025-10-16   ✅       0         0       All healthy
2025-10-15   ✅       0         0       All healthy

Trends:
  • SupportShell token never configured (action needed)
  • Customer Portal token rotation needed (every 28 days)
  • VPN connection stable (99% uptime)
```

---

## Integration with Commands

### Pre-Command Mini-Audit

Every `tam-rfe` command runs a quick auth check:

```bash
$ tam-rfe check tdbank

🔐 Auth-Box: Quick check (run 'tam-rfe auth-audit' for full audit)
  ✅ JIRA Token: Valid
  ⚠️  Portal Token: Expires in 2 days
  ✅ VPN: Connected

⚠️  Run full audit to see all warnings: tam-rfe auth-audit

[continues with main command...]
```

---

## Audit Configuration

### Configuration File: `~/.config/taminator/audit-config.yaml`

```yaml
audit:
  # Automatic audit schedule
  automatic:
    enabled: true
    schedule: "0 8 * * *"  # Daily at 8 AM
    notify_on_warnings: true
    notify_on_errors: true
  
  # Notification settings
  notifications:
    email:
      enabled: true
      recipients:
        - jbyrd@redhat.com
      include_full_report: true
    
    slack:
      enabled: false
      channel: "#tam-alerts"
      webhook_url: "..."
  
  # Warning thresholds
  thresholds:
    token_expiration_warning_days: 7
    kerberos_expiration_warning_hours: 12
    token_rotation_recommended_days: 30
  
  # Report retention
  reports:
    retention_days: 90
    location: "~/.config/taminator/audit-reports/"
  
  # Tests to run
  tests:
    api_token_validation: true
    network_connectivity: true
    kerberos_check: true
    ssh_key_check: true
    security_compliance: true
```

---

## Success Criteria

### Audit Must:
- ✅ Check ALL authentication types (tokens, VPN, Kerberos, SSH)
- ✅ Test with real API calls (not just config checks)
- ✅ Provide actionable remediation steps
- ✅ Support multiple output formats (human, JSON, markdown)
- ✅ Track history and trends
- ✅ Run automatically on schedule
- ✅ Generate compliance reports
- ✅ Complete in < 5 seconds (quick mode)
- ✅ Complete in < 30 seconds (full audit)

---

## Command Reference

```bash
# Full audit with all checks
tam-rfe auth-audit

# Quick audit (faster)
tam-rfe auth-audit --quick

# Specific checks only
tam-rfe auth-audit --check vpn,jira,kerberos

# Generate report file
tam-rfe auth-audit --report audit.md

# JSON output for automation
tam-rfe auth-audit --format json

# Show audit history
tam-rfe auth-audit --history

# Enable automatic daily audits
tam-rfe config --enable-daily-audit

# Email report
tam-rfe auth-audit --email jbyrd@redhat.com
```

---

**Bottom Line:** Auth-Box audit provides complete visibility into authentication health with actionable remediation steps. Run daily automatically to catch issues before they impact customer work.

