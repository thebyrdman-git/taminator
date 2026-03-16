# Feature Request: Auth-Box Module

**Date:** October 21, 2025  
**Priority:** CRITICAL (blocker for tool functionality)  
**Component:** Core Infrastructure  
**Name:** auth-box (centralized authentication management)

**Issue:** Without complete authentication, the tool doesn't function

**Scope:** Manage ALL authentication requirements, including those requiring user intervention

---

## Problem Statement

### Current Situation
Taminator tools require multiple authentication mechanisms:

**API Tokens (Automated):**
- **JIRA API Token** - Query JIRA status (issues.redhat.com)
- **Red Hat Customer Portal API Token** - Post RFE/Bug reports
- **Hydra API Token** - Customer intelligence data
- **SupportShell API Token** - Case data access

**User-Interactive Authentication:**
- **Red Hat VPN** - Required for internal API access (user must connect manually)
- **Kerberos/SSO** - May require kinit or browser login
- **GitLab SSH Keys** - For internal repository access
- **MFA/2FA** - User interaction required for some services

**Current Problems:**
1. ❌ No centralized authentication management
2. ❌ No awareness of user-interactive auth requirements
3. ❌ Tools fail when VPN is disconnected (no guidance)
4. ❌ No clear explanation WHY each auth is needed
5. ❌ No guidance on HOW to authenticate
6. ❌ No pre-flight checks before operations
7. ❌ Tools fail silently or with confusing errors

### Real-World Example: JIRA Token Missing
```bash
$ tam-rfe-verify-template --file tdbank.md

Traceback (most recent call last):
  File "/home/jbyrd/.local/bin/tam-rfe-verify-template", line 42, in main
    status = fetch_jira_status(jira_id)
  File "/home/jbyrd/.local/lib/taminator/jira.py", line 15, in fetch_jira_status
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
UnboundLocalError: local variable 'token' referenced before assignment
```

**User Experience:**
- ❌ Confusing error message
- ❌ No explanation of what's needed
- ❌ No guidance on how to fix
- ❌ Tool doesn't function

---

## Proposed Solution: Auth-Box Module

### Design Philosophy: Elegant & User-Friendly
**Elegant** = Clean interface, beautiful output, professional appearance  
**User-Friendly** = Simple commands, clear guidance, minimal friction

### Module Purpose: Complete Authentication Management
Auth-Box handles ALL authentication requirements with:
1. ✅ API token storage and validation
2. ✅ VPN connection detection and guidance
3. ✅ Kerberos/SSO authentication checks
4. ✅ SSH key verification
5. ✅ Pre-flight authentication checks before operations
6. ✅ User intervention guidance (when manual steps required)
7. ✅ Clear error messages with context
8. ✅ Step-by-step authentication walkthroughs
9. ✅ Multiple storage backends (env vars, keyring, config file)
10. ✅ Beautiful terminal UI (using Rich)
11. ✅ Simple, intuitive commands

---

## Auth-Box: Complete Authentication Awareness

### Authentication Types Managed

**Type 1: API Tokens (Automated Storage)**
- Store in system keyring
- Validate automatically
- Refresh when expired

**Type 2: User-Interactive (Detection + Guidance)**
- Detect if VPN is connected
- Check Kerberos ticket validity
- Verify SSH key access
- Guide user through manual steps

**Type 3: Just-In-Time (Prompt When Needed)**
- MFA/2FA codes
- Browser-based OAuth flows
- Manual password entry (when keyring unavailable)

---

## User Experience: Elegant & User-Friendly Design

### Design Principles

**Elegant:**
- Clean, uncluttered output
- Professional color scheme (blue for info, green for success, red for errors)
- Consistent formatting using Rich tables and panels
- Beautiful progress indicators
- Minimal but meaningful output

**User-Friendly:**
- Single command does the right thing
- Clear, actionable guidance
- No jargon or technical complexity
- Copy-paste ready commands
- Interactive prompts with smart defaults

---

## User Experience Examples

### Scenario 1: Missing JIRA Token (Elegant Error)
```bash
$ tam-rfe-verify-template --file tdbank.md

❌ JIRA API Token Required
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Why This Token Is Needed:
  The JIRA API token allows Taminator to query Red Hat JIRA
  (issues.redhat.com) for current RFE and Bug statuses.
  
  Without this token, Taminator cannot:
  • Verify if customer templates are up-to-date
  • Fetch current status of AAPRFE-* and AAP-* issues
  • Generate accurate RFE/Bug tracker reports

What This Token Provides Access To:
  • Read-only access to Red Hat JIRA issues
  • Your assigned issues and customer-facing issues
  • JIRA status, assignee, and metadata

How To Obtain This Token:
  1. Go to: https://issues.redhat.com/secure/ViewProfile.jspa
  2. Click "Personal Access Tokens" tab
  3. Click "Create token"
  4. Name: "Taminator JIRA Access"
  5. Permissions: Read-only
  6. Copy the generated token

How To Provide This Token:
  Option 1 (Secure - Recommended):
    $ tam-token-manager add jira
    Enter JIRA token: [paste token]
    ✓ Token saved securely in system keyring
  
  Option 2 (Environment Variable):
    $ export JIRA_API_TOKEN="your_token_here"
  
  Option 3 (Configuration File):
    $ echo "jira_token: your_token_here" >> ~/.config/taminator/tokens.yaml
    $ chmod 600 ~/.config/taminator/tokens.yaml

Once configured, run this command again.

Need Help?
  • Documentation: https://gitlab.cee.redhat.com/jbyrd/taminator/-/docs/tokens
  • Contact: jbyrd@redhat.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Scenario 2: All Tokens Configured (Success)
```bash
$ tam-rfe-verify-template --file tdbank.md

✓ Validating API tokens...
  ✓ JIRA API Token: Valid (expires in 89 days)
  ✓ Customer Portal API Token: Valid
  
✓ Verifying TD Bank template...
  Checking 9 JIRA issues...
  
Summary: 9/9 statuses match (100%)
Status: ✅ Template is UP-TO-DATE
```

---

## Implementation: Token Manager Module

### Module Structure
```
taminator/
  core/
    token_manager.py       # Core token management
    token_storage.py       # Storage backends
    token_validator.py     # Token validation
    token_cli.py          # CLI commands
```

### Core Token Manager (`token_manager.py`)

```python
"""
Taminator Token Manager - Centralized API token management
"""

from enum import Enum
from typing import Optional, Dict
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel

console = Console()

class TokenType(Enum):
    """Supported API token types."""
    JIRA = "jira"
    CUSTOMER_PORTAL = "customer_portal"
    HYDRA = "hydra"
    SUPPORTSHELL = "supportshell"

@dataclass
class TokenMetadata:
    """Metadata about each token type."""
    name: str
    purpose: str
    provides_access_to: list[str]
    required_for_features: list[str]
    obtain_url: str
    obtain_steps: list[str]
    permissions_required: str

TOKEN_REGISTRY: Dict[TokenType, TokenMetadata] = {
    TokenType.JIRA: TokenMetadata(
        name="JIRA API Token",
        purpose="Query Red Hat JIRA for RFE and Bug statuses",
        provides_access_to=[
            "Read-only access to Red Hat JIRA issues",
            "Your assigned issues and customer-facing issues",
            "JIRA status, assignee, and metadata"
        ],
        required_for_features=[
            "tam-rfe-verify-template - Verify customer templates",
            "tam-monitor - Track RFE/Bug status changes",
            "tam-rfe-report - Generate customer reports"
        ],
        obtain_url="https://issues.redhat.com/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens",
        obtain_steps=[
            "Go to: https://issues.redhat.com/secure/ViewProfile.jspa",
            "Click 'Personal Access Tokens' tab",
            "Click 'Create token'",
            "Name: 'Taminator JIRA Access'",
            "Permissions: Read-only",
            "Copy the generated token"
        ],
        permissions_required="Read-only access to JIRA issues"
    ),
    
    TokenType.CUSTOMER_PORTAL: TokenMetadata(
        name="Red Hat Customer Portal API Token",
        purpose="Post RFE/Bug tracker updates to customer portal groups",
        provides_access_to=[
            "Customer group pages (read/write)",
            "Case comments and attachments",
            "Customer account information"
        ],
        required_for_features=[
            "tam-rfe-post - Post RFE reports to customer portal",
            "tam-rfe-monitor - Auto-update customer pages",
            "tam-case-comment - Add case comments"
        ],
        obtain_url="https://access.redhat.com/management/api",
        obtain_steps=[
            "Go to: https://access.redhat.com/management/api",
            "Click 'Generate Token'",
            "Select scopes: 'case:read', 'case:write'",
            "Copy the generated token",
            "Token expires after 30 days (refresh required)"
        ],
        permissions_required="Case read/write, Customer group access"
    ),
    
    TokenType.HYDRA: TokenMetadata(
        name="Hydra API Token",
        purpose="Access customer intelligence and account data",
        provides_access_to=[
            "Customer account details",
            "Contact information",
            "Subscription data",
            "Historical case data"
        ],
        required_for_features=[
            "tam-discover-customers - Auto-discover customer accounts",
            "tam-onboard - Onboard new customers",
            "tam-contact-intelligence - Get contact info"
        ],
        obtain_url="https://hydra.corp.redhat.com/api",
        obtain_steps=[
            "Contact TAM Tools team for Hydra API access",
            "Request: hydra-api-access@redhat.com",
            "Include: Your Red Hat username and manager approval",
            "Token will be provided via secure channel"
        ],
        permissions_required="TAM role required, manager approval"
    ),
    
    TokenType.SUPPORTSHELL: TokenMetadata(
        name="SupportShell API Token",
        purpose="Query Red Hat support cases and SBR data",
        provides_access_to=[
            "Support case details",
            "SBR Group assignments",
            "Case status and priority",
            "Case comments and updates"
        ],
        required_for_features=[
            "tam-active-cases - Generate call agendas",
            "tam-case-processor - Process case data",
            "tam-my-plate - Dashboard for assigned cases"
        ],
        obtain_url="https://supportshell.redhat.com/api/tokens",
        obtain_steps=[
            "Go to: https://supportshell.redhat.com",
            "Click your profile → 'API Tokens'",
            "Click 'Generate New Token'",
            "Name: 'Taminator Access'",
            "Copy the generated token"
        ],
        permissions_required="SupportShell access (TAM role)"
    )
}


class TokenManager:
    """
    Centralized token management for Taminator tools.
    
    Handles:
    - Token storage (keyring, env vars, config file)
    - Token validation
    - Clear error messages with context
    - Token lifecycle management
    """
    
    def __init__(self, storage_backend='auto'):
        self.storage = self._init_storage(storage_backend)
        
    def get_token(self, token_type: TokenType, required: bool = True) -> Optional[str]:
        """
        Get token with intelligent fallback and error handling.
        
        Args:
            token_type: Type of token to retrieve
            required: If True, raise error with guidance if missing
            
        Returns:
            Token string if found, None if not required and missing
            
        Raises:
            TokenMissingError: If token required but not found (includes guidance)
        """
        token = self.storage.get(token_type)
        
        if token is None and required:
            self._raise_missing_token_error(token_type)
        
        return token
    
    def _raise_missing_token_error(self, token_type: TokenType):
        """
        Raise informative error when token is missing.
        
        Includes:
        - Why this token is needed
        - What it provides access to
        - Which features require it
        - How to obtain it
        - How to configure it
        """
        metadata = TOKEN_REGISTRY[token_type]
        
        error_message = f"""
❌ {metadata.name} Required
{'━' * 60}

Why This Token Is Needed:
  {metadata.purpose}

What This Token Provides Access To:
{chr(10).join(f'  • {item}' for item in metadata.provides_access_to)}

Required For These Features:
{chr(10).join(f'  • {feature}' for feature in metadata.required_for_features)}

How To Obtain This Token:
{chr(10).join(f'  {i+1}. {step}' for i, step in enumerate(metadata.obtain_steps))}

Permissions Required:
  {metadata.permissions_required}

How To Provide This Token:
  Option 1 (Secure - Recommended):
    $ tam-token-manager add {token_type.value}
    Enter {metadata.name}: [paste token]
    ✓ Token saved securely in system keyring
  
  Option 2 (Environment Variable):
    $ export {token_type.value.upper()}_API_TOKEN="your_token_here"
  
  Option 3 (Configuration File):
    $ echo "{token_type.value}_token: your_token_here" >> ~/.config/taminator/tokens.yaml
    $ chmod 600 ~/.config/taminator/tokens.yaml

Once configured, run your command again.

Need Help?
  • Documentation: https://gitlab.cee.redhat.com/jbyrd/taminator/-/docs/tokens
  • Contact: jbyrd@redhat.com
{'━' * 60}
"""
        console.print(Panel(error_message, border_style="red"))
        raise TokenMissingError(f"{metadata.name} is required but not configured")


class TokenMissingError(Exception):
    """Raised when a required token is missing."""
    pass
```

---

## Token Storage Backends

### Priority Order
1. **System Keyring** (most secure - recommended)
2. **Environment Variables** (good for development/CI)
3. **Configuration File** (least secure - encrypted at rest)

### Storage Backend Implementation

```python
"""Token storage backends with automatic fallback."""

import os
import keyring
import yaml
from pathlib import Path
from cryptography.fernet import Fernet

class TokenStorage:
    """Manages token storage with multiple backends."""
    
    def __init__(self, backend='auto'):
        self.backends = self._init_backends(backend)
    
    def get(self, token_type: TokenType) -> Optional[str]:
        """Get token with fallback through backends."""
        for backend in self.backends:
            token = backend.get(token_type)
            if token:
                return token
        return None
    
    def set(self, token_type: TokenType, token: str):
        """Set token in primary backend."""
        self.backends[0].set(token_type, token)


class KeyringBackend:
    """Secure token storage using system keyring."""
    
    SERVICE_NAME = "taminator"
    
    def get(self, token_type: TokenType) -> Optional[str]:
        try:
            return keyring.get_password(self.SERVICE_NAME, token_type.value)
        except Exception:
            return None
    
    def set(self, token_type: TokenType, token: str):
        keyring.set_password(self.SERVICE_NAME, token_type.value, token)


class EnvironmentBackend:
    """Token storage via environment variables."""
    
    def get(self, token_type: TokenType) -> Optional[str]:
        # Try multiple naming conventions
        env_names = [
            f"{token_type.value.upper()}_API_TOKEN",
            f"{token_type.value.upper()}_TOKEN",
            f"TAMINATOR_{token_type.value.upper()}_TOKEN"
        ]
        for env_name in env_names:
            token = os.getenv(env_name)
            if token:
                return token
        return None


class ConfigFileBackend:
    """Token storage in encrypted config file."""
    
    CONFIG_PATH = Path.home() / ".config" / "taminator" / "tokens.yaml"
    
    def get(self, token_type: TokenType) -> Optional[str]:
        if not self.CONFIG_PATH.exists():
            return None
        
        with open(self.CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)
        
        return config.get(f"{token_type.value}_token")
```

---

## CLI Commands

### `tam-token-manager` - Token Management CLI

```bash
# List configured tokens
$ tam-token-manager list
✓ JIRA API Token: Configured (keyring)
✗ Customer Portal Token: Not configured
✗ Hydra API Token: Not configured
✓ SupportShell Token: Configured (environment)

# Add token interactively
$ tam-token-manager add jira
Enter JIRA API Token: [paste token - hidden]
✓ Token saved securely in system keyring

# Test token validity
$ tam-token-manager test jira
Testing JIRA API Token...
✓ Token is valid
✓ Expires in 89 days
✓ Permissions: read:jira-work

# Remove token
$ tam-token-manager remove jira
⚠  This will remove JIRA API Token from keyring
Confirm? (y/n): y
✓ Token removed

# Export tokens (for backup/migration)
$ tam-token-manager export --secure
Enter encryption passphrase: 
✓ Tokens exported to: ~/.config/taminator/tokens-backup-20251021.gpg

# Import tokens
$ tam-token-manager import ~/.config/taminator/tokens-backup-20251021.gpg
Enter decryption passphrase:
✓ Imported 2 tokens
```

---

## Integration Example

### Before (Tool Failure)
```python
# In tam-rfe-verify-template
def main():
    jira_token = os.getenv('JIRA_API_TOKEN')  # None
    status = fetch_jira_status(jira_token)    # ❌ Crashes
```

### After (Token Manager)
```python
# In tam-rfe-verify-template
from taminator.core.token_manager import TokenManager, TokenType

def main():
    tm = TokenManager()
    
    # If token missing, user gets clear guidance
    jira_token = tm.get_token(TokenType.JIRA, required=True)
    
    status = fetch_jira_status(jira_token)  # ✅ Works
```

---

## Token Validation

```python
"""Token validation and health checks."""

class TokenValidator:
    """Validates tokens and checks expiration."""
    
    def validate_jira_token(self, token: str) -> dict:
        """Validate JIRA token and return metadata."""
        response = requests.get(
            'https://issues.redhat.com/rest/api/2/myself',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'valid': True,
                'username': data['name'],
                'email': data['emailAddress']
            }
        else:
            return {'valid': False, 'error': response.text}
    
    def check_expiration(self, token: str) -> Optional[int]:
        """Check token expiration (days remaining)."""
        # Implementation varies by token type
        pass
```

---

## Benefits

### 1. Tool Reliability
- No more cryptic errors
- Tools fail fast with clear guidance
- Users know exactly what to do

### 2. Security
- Tokens stored in system keyring (encrypted)
- Not visible in process list or logs
- Easy rotation and revocation

### 3. User Experience
- Clear error messages
- Step-by-step guidance
- Multiple configuration options

### 4. Maintainability
- Centralized token logic
- Easy to add new token types
- Consistent error handling

---

## Implementation Plan

### Phase 1: Core Token Manager (Week 1)
- [ ] Create TokenManager class
- [ ] Implement TokenType enum and metadata registry
- [ ] Build clear error messages
- [ ] Add keyring storage backend

### Phase 2: CLI Commands (Week 2)
- [ ] `tam-token-manager list`
- [ ] `tam-token-manager add <type>`
- [ ] `tam-token-manager remove <type>`
- [ ] `tam-token-manager test <type>`

### Phase 3: Integration (Week 3)
- [ ] Integrate into tam-rfe-verify-template
- [ ] Integrate into tam-active-cases
- [ ] Integrate into tam-monitor
- [ ] Update all tools to use TokenManager

### Phase 4: Advanced Features (Week 4)
- [ ] Token expiration warnings
- [ ] Auto-refresh for short-lived tokens
- [ ] Token export/import for backup
- [ ] CI/CD integration documentation

---

## Success Metrics

- **Error Clarity:** 100% of token errors provide clear guidance
- **Tool Reliability:** Zero crashes due to missing tokens
- **User Satisfaction:** < 5 minutes to configure all tokens
- **Security:** 90%+ of users use keyring storage

---

**Bottom Line:** Without valid tokens, tools don't function. Token Manager ensures users always know what's needed, why it's needed, and how to configure it.

