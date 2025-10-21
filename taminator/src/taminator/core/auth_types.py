"""
Authentication type definitions for Auth-Box.

This module defines all authentication types that Taminator supports,
including API tokens, user-interactive auth, and just-in-time auth.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


class AuthType(Enum):
    """
    All authentication types supported by Auth-Box.
    
    Categories:
    - API Tokens: Automated storage and validation
    - User-Interactive: Detection and guidance
    - Just-In-Time: Prompt when needed
    """
    
    # API Tokens (automated storage)
    JIRA_TOKEN = "jira_token"
    PORTAL_TOKEN = "portal_token"
    HYDRA_TOKEN = "hydra_token"
    SUPPORTSHELL_TOKEN = "supportshell_token"
    GITHUB_TOKEN = "github_token"
    
    # User-Interactive (detection + guidance)
    VPN = "vpn_connection"
    KERBEROS = "kerberos_ticket"
    SSH_KEY = "ssh_key_access"
    
    # Just-In-Time (prompt when needed)
    MFA = "mfa_code"
    BROWSER_OAUTH = "browser_oauth"


class AuthStatus(Enum):
    """Authentication check status."""
    VALID = "valid"
    INVALID = "invalid"
    MISSING = "missing"
    EXPIRING_SOON = "expiring_soon"
    EXPIRED = "expired"
    WARNING = "warning"


@dataclass
class TokenMetadata:
    """Metadata about each authentication token type."""
    name: str
    purpose: str
    provides_access_to: List[str]
    required_for_features: List[str]
    obtain_url: str
    obtain_steps: List[str]
    permissions_required: str
    expiration_warning_days: int = 7


@dataclass
class AuthResult:
    """Result of an authentication check."""
    auth_type: AuthType
    status: AuthStatus
    passed: bool
    details: Optional[str] = None
    error: Optional[str] = None
    warning: Optional[str] = None
    expires: Optional[datetime] = None
    days_remaining: Optional[int] = None
    last_used: Optional[datetime] = None
    test_passed: Optional[bool] = None


# Token Registry: Metadata for each token type
TOKEN_REGISTRY = {
    AuthType.JIRA_TOKEN: TokenMetadata(
        name="JIRA API Token",
        purpose="Query Red Hat JIRA for RFE and Bug statuses",
        provides_access_to=[
            "Read-only access to Red Hat JIRA issues",
            "Your assigned issues and customer-facing issues",
            "JIRA status, assignee, and metadata"
        ],
        required_for_features=[
            "tam-rfe check - Verify customer templates",
            "tam-rfe update - Update reports with current statuses",
            "tam-rfe watch - Monitor status changes"
        ],
        obtain_url="https://issues.redhat.com/secure/ViewProfile.jspa",
        obtain_steps=[
            "Go to: https://issues.redhat.com/secure/ViewProfile.jspa",
            "Click 'Personal Access Tokens' tab",
            "Click 'Create token'",
            "Name: 'Taminator JIRA Access'",
            "Permissions: Read-only",
            "Copy the generated token"
        ],
        permissions_required="Read-only access to JIRA issues",
        expiration_warning_days=7
    ),
    
    AuthType.PORTAL_TOKEN: TokenMetadata(
        name="Red Hat Customer Portal API Token",
        purpose="Post RFE/Bug tracker updates to customer portal groups",
        provides_access_to=[
            "Customer group pages (read/write)",
            "Case comments and attachments",
            "Customer account information"
        ],
        required_for_features=[
            "tam-rfe post - Post RFE reports to customer portal",
            "tam-rfe update - Auto-update customer pages"
        ],
        obtain_url="https://access.redhat.com/management/api",
        obtain_steps=[
            "Go to: https://access.redhat.com/management/api",
            "Click 'Generate Token'",
            "Select scopes: 'case:read', 'case:write'",
            "Copy the generated token",
            "Token expires after 30 days (refresh required)"
        ],
        permissions_required="Case read/write, Customer group access",
        expiration_warning_days=3
    ),
    
    AuthType.HYDRA_TOKEN: TokenMetadata(
        name="Hydra API Token",
        purpose="Access customer intelligence and account data",
        provides_access_to=[
            "Customer account details",
            "Contact information",
            "Subscription data",
            "Historical case data"
        ],
        required_for_features=[
            "tam-rfe discover - Auto-discover customer accounts",
            "tam-rfe onboard - Onboard new customers"
        ],
        obtain_url="https://hydra.corp.redhat.com/api",
        obtain_steps=[
            "Contact TAM Tools team for Hydra API access",
            "Request: hydra-api-access@redhat.com",
            "Include: Your Red Hat username and manager approval",
            "Token will be provided via secure channel"
        ],
        permissions_required="TAM role required, manager approval",
        expiration_warning_days=7
    ),
    
    AuthType.SUPPORTSHELL_TOKEN: TokenMetadata(
        name="SupportShell API Token",
        purpose="Query Red Hat support cases and SBR data",
        provides_access_to=[
            "Support case details",
            "SBR Group assignments",
            "Case status and priority",
            "Case comments and updates"
        ],
        required_for_features=[
            "tam-rfe active-cases - Generate call agendas"
        ],
        obtain_url="https://supportshell.redhat.com/api/tokens",
        obtain_steps=[
            "Go to: https://supportshell.redhat.com",
            "Click your profile → 'API Tokens'",
            "Click 'Generate New Token'",
            "Name: 'Taminator Access'",
            "Copy the generated token"
        ],
        permissions_required="SupportShell access (TAM role)",
        expiration_warning_days=7
    ),
    
    AuthType.GITHUB_TOKEN: TokenMetadata(
        name="GitHub Personal Access Token",
        purpose="Submit bug reports and feature requests to Taminator GitHub repository",
        provides_access_to=[
            "Create issues in Taminator repository",
            "Attach logs and screenshots",
            "Track your reported issues",
            "Comment on existing issues"
        ],
        required_for_features=[
            "tam-rfe report-issue - Submit bugs/features from GUI",
            "GUI Issue Submission - Report directly from app"
        ],
        obtain_url="https://github.com/settings/tokens",
        obtain_steps=[
            "Go to: https://github.com/settings/tokens",
            "Click 'Generate new token' → 'Generate new token (classic)'",
            "Name: 'Taminator Issue Reporter'",
            "Select scope: 'public_repo' (for public repositories)",
            "Set expiration: 90 days or No expiration",
            "Click 'Generate token'",
            "Copy the generated token (starts with 'ghp_')"
        ],
        permissions_required="GitHub account, public_repo scope",
        expiration_warning_days=7
    ),
}


# Command authentication requirements
AUTH_REQUIREMENTS = {
    "tam-rfe-check": [
        AuthType.VPN,
        AuthType.JIRA_TOKEN,
    ],
    "tam-rfe-update": [
        AuthType.VPN,
        AuthType.JIRA_TOKEN,
    ],
    "tam-rfe-post": [
        AuthType.VPN,
        AuthType.PORTAL_TOKEN,
        # AuthType.MFA,  # May be required
    ],
    "tam-rfe-onboard": [
        AuthType.VPN,
        AuthType.KERBEROS,
        AuthType.HYDRA_TOKEN,
    ],
}

