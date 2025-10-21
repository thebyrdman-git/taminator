# Auth-Box: Real-World Authentication Examples

**Date:** October 21, 2025  
**Component:** auth-box module  
**Purpose:** Show how auth-box handles ALL authentication types

---

## Example 1: Missing VPN Connection (User-Interactive)

### Scenario
TAM tries to check TD Bank RFE report, but Red Hat VPN is not connected.

### Without Auth-Box (Current)
```bash
$ tam-rfe check tdbank

⏳ Checking 9 JIRA issues...
❌ Error: Connection timeout to issues.redhat.com
Traceback (most recent call last):
  File "/home/jbyrd/.local/bin/tam-rfe-check", line 42
    ...
requests.exceptions.ConnectionError: Failed to establish connection
```

**User Experience:** ❌ Confusing error, no guidance

### With Auth-Box (Proposed)
```bash
$ tam-rfe check tdbank

🔐 Auth-Box: Pre-flight authentication check...

Checking authentication requirements:
  ✓ JIRA API Token: Valid
  ✗ Red Hat VPN: Not connected
  
❌ Red Hat VPN Required

Why This Is Needed:
  Access to internal Red Hat services (JIRA, Hydra API, etc.)
  requires an active VPN connection.
  
What This Provides Access To:
  • issues.redhat.com (JIRA)
  • Hydra API (customer intelligence)
  • Internal GitLab repositories

How To Connect:

  1. Open Red Hat VPN client (or NetworkManager)
  2. Select: "1 - Red Hat Global VPN"
  3. Enter: PIN + Token from authenticator app
  4. Wait for connection (usually 5-10 seconds)

Command to check VPN status:
  $ nmcli connection show --active | grep VPN

Once connected, run your command again:
  $ tam-rfe check tdbank

Need Help?
  • VPN Guide: https://source.redhat.com/kb/vpn-setup
  • IT Support: help.redhat.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Cannot proceed without VPN connection.
```

**User Experience:** ✅ Clear guidance, knows exactly what to do

---

## Example 2: Expired Kerberos Ticket (User-Interactive)

### Scenario
TAM tries to access Hydra API, but Kerberos ticket has expired.

### With Auth-Box
```bash
$ tam-rfe onboard newcustomer

🔐 Auth-Box: Pre-flight authentication check...

Checking authentication requirements:
  ✓ Red Hat VPN: Connected
  ✓ JIRA API Token: Valid
  ✗ Kerberos Ticket: Expired (last renewed 26 hours ago)
  
❌ Kerberos Authentication Required

Why This Is Needed:
  Access to internal Red Hat services (Hydra API, internal databases)
  requires a valid Kerberos ticket.

How To Renew:
  
  Run this command:
    $ kinit
  
  Enter your Red Hat password when prompted.
  Ticket will be valid for 24 hours.

Check ticket status:
  $ klist

Once renewed, run your command again:
  $ tam-rfe onboard newcustomer

Need Help?
  • Kerberos Guide: https://source.redhat.com/kb/kerberos
  • Contact: IT Help Desk
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Attempting to continue anyway (may fail)...
```

---

## Example 3: Missing JIRA Token (API Token)

### Scenario
TAM has never configured JIRA API token.

### With Auth-Box
```bash
$ tam-rfe check tdbank

🔐 Auth-Box: Pre-flight authentication check...

Checking authentication requirements:
  ✓ Red Hat VPN: Connected
  ✗ JIRA API Token: Not configured

❌ JIRA API Token Required

Why This Is Needed:
  Query Red Hat JIRA (issues.redhat.com) for RFE/Bug statuses.
  Without this, you cannot check if customer reports are current.

Required For:
  • tam-rfe check - Verify report statuses
  • tam-rfe update - Update reports with current statuses

How To Get This Token:
  1. Go to: https://issues.redhat.com/secure/ViewProfile.jspa
  2. Click "Personal Access Tokens" tab
  3. Click "Create token"
  4. Name: "TAM RFE Tool"
  5. Permissions: Read-only
  6. Copy the generated token

How To Configure:
  
  Option 1 (Recommended - will prompt now):
    Continue with onboarding to configure all tokens
  
  Option 2 (Quick - configure just this token):
    $ tam-rfe config --add-token jira
  
  Option 3 (Environment variable):
    $ export JIRA_API_TOKEN="your_token_here"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Cannot proceed without JIRA token.

Options:
  [o] Run onboarding wizard (configure all authentication)
  [j] Configure just JIRA token
  [q] Quit

Choice [o]: _
```

---

## Example 4: All Authentication Valid (Success Path)

### Scenario
TAM has everything configured correctly.

### With Auth-Box
```bash
$ tam-rfe check tdbank

🔐 Auth-Box: Pre-flight authentication check...

Checking authentication requirements:
  ✓ Red Hat VPN: Connected (plv-vpn-01.redhat.com)
  ✓ JIRA API Token: Valid (expires in 87 days)
  ✓ Customer Portal Token: Valid (expires in 28 days)
  ✓ Kerberos Ticket: Valid (expires in 18 hours)

✅ All authentication requirements met!

╭─────────────────────────────────────────────────────╮
│  TD Bank RFE/Bug Status Check                      │
╰─────────────────────────────────────────────────────╯

📄 Report: tdbank-rfe-tracker.md
🔍 Checking 9 JIRA issues...

[continues with report check...]
```

---

## Example 5: Token Expiring Soon (Proactive Warning)

### Scenario
Customer Portal token expires in 2 days.

### With Auth-Box
```bash
$ tam-rfe check tdbank

🔐 Auth-Box: Pre-flight authentication check...

Checking authentication requirements:
  ✓ Red Hat VPN: Connected
  ✓ JIRA API Token: Valid (expires in 87 days)
  ⚠️  Customer Portal Token: Valid but expires soon (2 days remaining)
  ✓ Kerberos Ticket: Valid

⚠️  Customer Portal Token Expiring Soon

Your Customer Portal API token expires in 2 days.

Impact:
  You won't be able to post RFE/Bug reports to customer portal.

How To Renew:
  1. Go to: https://access.redhat.com/management/api
  2. Click "Generate Token"
  3. Scopes: case:read, case:write
  4. Copy new token
  5. Run: tam-rfe config --update-token portal

Reminder: We'll notify you 3 days before expiration.

⏸️  [Press any key to continue or 'r' to renew now]
```

---

## Example 6: SSH Key Access (GitLab)

### Scenario
Tool needs to clone internal GitLab repository.

### With Auth-Box
```bash
$ tam-rfe deploy --to-production

🔐 Auth-Box: Pre-flight authentication check...

Checking authentication requirements:
  ✓ Red Hat VPN: Connected
  ✓ GitLab SSH Key: Checking access...
  ✗ GitLab SSH Key: No SSH access to gitlab.cee.redhat.com

❌ GitLab SSH Access Required

Why This Is Needed:
  Deploy tool to production requires cloning internal GitLab repository.

What Went Wrong:
  SSH key authentication to gitlab.cee.redhat.com failed.

Common Causes:
  • SSH key not added to GitLab profile
  • SSH key not loaded in ssh-agent
  • Wrong SSH key configured

How To Fix:

  1. Generate SSH key (if you don't have one):
     $ ssh-keygen -t ed25519 -C "your@redhat.com"
  
  2. Add key to ssh-agent:
     $ eval "$(ssh-agent -s)"
     $ ssh-add ~/.ssh/id_ed25519
  
  3. Add public key to GitLab:
     • Go to: https://gitlab.cee.redhat.com/-/profile/keys
     • Click "Add new key"
     • Paste contents of: ~/.ssh/id_ed25519.pub
  
  4. Test SSH access:
     $ ssh -T git@gitlab.cee.redhat.com

Once configured, run your command again:
  $ tam-rfe deploy --to-production

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Cannot proceed without GitLab SSH access.
```

---

## Example 7: MFA/2FA Required (Just-In-Time)

### Scenario
Accessing Customer Portal API requires MFA code.

### With Auth-Box
```bash
$ tam-rfe post tdbank

🔐 Auth-Box: Pre-flight authentication check...

Checking authentication requirements:
  ✓ Red Hat VPN: Connected
  ✓ Customer Portal Token: Valid
  ⚠️  Customer Portal: MFA verification required

🔐 Multi-Factor Authentication Required

Your Customer Portal access requires MFA verification.

Please enter your 6-digit MFA code from your authenticator app:

MFA Code: ______

[Code will not be stored]
```

---

## Auth-Box Architecture

### Pre-Flight Check Flow

```python
def preflight_check(required_auth: List[AuthType]) -> AuthStatus:
    """
    Check all authentication requirements before operation.
    
    Returns:
        AuthStatus with pass/fail and guidance for failures
    """
    results = []
    
    for auth_type in required_auth:
        if auth_type == AuthType.JIRA_TOKEN:
            results.append(check_jira_token())
        
        elif auth_type == AuthType.VPN:
            results.append(check_vpn_connection())
        
        elif auth_type == AuthType.KERBEROS:
            results.append(check_kerberos_ticket())
        
        elif auth_type == AuthType.SSH_KEY:
            results.append(check_ssh_access())
    
    if all(r.passed for r in results):
        return AuthStatus.SUCCESS
    
    # Show failure guidance
    for result in results:
        if not result.passed:
            show_auth_guidance(result.auth_type, result.error)
    
    return AuthStatus.FAILED
```

### Authentication Type Registry

```python
class AuthType(Enum):
    # API Tokens (automated storage)
    JIRA_TOKEN = "jira_token"
    PORTAL_TOKEN = "portal_token"
    HYDRA_TOKEN = "hydra_token"
    
    # User-Interactive (detection + guidance)
    VPN = "vpn_connection"
    KERBEROS = "kerberos_ticket"
    SSH_KEY = "ssh_key_access"
    
    # Just-In-Time (prompt when needed)
    MFA = "mfa_code"
    BROWSER_OAUTH = "browser_oauth"

AUTH_REQUIREMENTS = {
    "tam-rfe-check": [
        AuthType.VPN,
        AuthType.JIRA_TOKEN,
    ],
    "tam-rfe-post": [
        AuthType.VPN,
        AuthType.PORTAL_TOKEN,
        AuthType.MFA,  # May be required
    ],
    "tam-rfe-onboard": [
        AuthType.VPN,
        AuthType.KERBEROS,
        AuthType.HYDRA_TOKEN,
    ],
    "tam-rfe-deploy": [
        AuthType.VPN,
        AuthType.SSH_KEY,
    ],
}
```

### VPN Detection Implementation

```python
def check_vpn_connection() -> AuthResult:
    """
    Detect if Red Hat VPN is connected.
    
    Methods:
    1. Check active NetworkManager connections
    2. Check routing table for VPN routes
    3. Test connectivity to internal service
    """
    # Method 1: NetworkManager (Linux)
    result = subprocess.run(
        ['nmcli', 'connection', 'show', '--active'],
        capture_output=True,
        text=True
    )
    
    if 'Red Hat Global VPN' in result.stdout or 'vpn' in result.stdout.lower():
        return AuthResult(
            passed=True,
            auth_type=AuthType.VPN,
            details="VPN connected via NetworkManager"
        )
    
    # Method 2: Test connectivity
    try:
        response = requests.get(
            'https://issues.redhat.com',
            timeout=5
        )
        if response.status_code == 200:
            return AuthResult(
                passed=True,
                auth_type=AuthType.VPN,
                details="VPN connectivity verified"
            )
    except requests.exceptions.ConnectionError:
        pass
    
    # VPN not connected
    return AuthResult(
        passed=False,
        auth_type=AuthType.VPN,
        error="VPN not connected",
        guidance=VPN_CONNECTION_GUIDANCE
    )
```

### Kerberos Ticket Check

```python
def check_kerberos_ticket() -> AuthResult:
    """Check if valid Kerberos ticket exists."""
    result = subprocess.run(
        ['klist', '-s'],
        capture_output=True
    )
    
    if result.returncode == 0:
        # Get ticket details
        ticket_info = subprocess.run(
            ['klist'],
            capture_output=True,
            text=True
        ).stdout
        
        # Parse expiration
        # ... check if expired soon ...
        
        return AuthResult(
            passed=True,
            auth_type=AuthType.KERBEROS,
            details="Valid Kerberos ticket"
        )
    else:
        return AuthResult(
            passed=False,
            auth_type=AuthType.KERBEROS,
            error="No valid Kerberos ticket",
            guidance=KERBEROS_RENEWAL_GUIDANCE
        )
```

---

## Integration with Commands

### Every Command Uses Auth-Box

```python
@auth_required([AuthType.VPN, AuthType.JIRA_TOKEN])
def tam_rfe_check(customer: str):
    """
    Decorator automatically runs pre-flight check.
    Command only executes if auth passes.
    """
    # This code only runs if authentication passed
    jira_token = auth_box.get_token(AuthType.JIRA_TOKEN)
    # ... rest of command ...
```

---

## Success Criteria

### Auth-Box Must:
- ✅ Detect ALL authentication requirements
- ✅ Handle both automated (tokens) and user-interactive (VPN) auth
- ✅ Provide clear guidance for every authentication failure
- ✅ Block operations until auth requirements are met
- ✅ Warn proactively about expiring credentials
- ✅ Beautiful, consistent error messages
- ✅ Support just-in-time authentication (MFA)

**Bottom Line:** Auth-Box is aware of ALL authentication, not just tokens. It guides users through any manual steps required.

