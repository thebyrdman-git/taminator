"""
Auth-Box: Complete authentication management for Taminator.

Handles ALL authentication requirements:
- API tokens (automated storage)
- VPN connection (user-interactive)
- Kerberos tickets (user-interactive)
- SSH keys (user-interactive)
- MFA/2FA (just-in-time)

Usage:
    from taminator.core.auth_box import auth_box, auth_required, AuthType
    
    # Check if authenticated
    if auth_box.check(AuthType.JIRA_TOKEN):
        token = auth_box.get_token(AuthType.JIRA_TOKEN)
    
    # Decorator for commands
    @auth_required([AuthType.VPN, AuthType.JIRA_TOKEN])
    def my_command():
        # Only runs if authentication passes
        pass
"""

import os
import subprocess
import time
from typing import List, Optional, Dict
from functools import wraps
from datetime import datetime, timedelta

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .auth_types import (
    AuthType,
    AuthStatus,
    AuthResult,
    TOKEN_REGISTRY,
    TokenMetadata
)

console = Console()


class AuthenticationError(Exception):
    """Raised when authentication requirement is not met."""
    pass


class AuthBox:
    """
    Centralized authentication management for Taminator.
    
    Handles:
    - Token storage and validation
    - VPN connection detection
    - Kerberos ticket checking
    - SSH key verification
    - Pre-flight authentication checks
    """
    
    # Keyring service name
    KEYRING_SERVICE = "taminator"
    
    def __init__(self):
        """Initialize Auth-Box."""
        self.console = Console()
    
    # ===== Token Management =====
    
    def get_token(self, token_type: AuthType, required: bool = True) -> Optional[str]:
        """
        Get authentication token with intelligent fallback.
        
        Args:
            token_type: Type of token to retrieve
            required: If True, raise error with guidance if missing
            
        Returns:
            Token string if found, None if not required and missing
            
        Raises:
            AuthenticationError: If token required but not found
        """
        # Try keyring first (most secure)
        token = self._get_token_from_keyring(token_type)
        
        # Fallback to environment variable
        if not token:
            token = self._get_token_from_env(token_type)
        
        # Fallback to config file
        if not token:
            token = self._get_token_from_config(token_type)
        
        if not token and required:
            self._raise_token_missing_error(token_type)
        
        return token
    
    def set_token(self, token_type: AuthType, token: str) -> bool:
        """
        Store token securely in system keyring.
        
        Args:
            token_type: Type of token
            token: Token value
            
        Returns:
            True if successful
        """
        if not KEYRING_AVAILABLE:
            console.print("⚠️  Keyring not available, token not saved", style="yellow")
            return False
        try:
            keyring.set_password(
                self.KEYRING_SERVICE,
                token_type.value,
                token
            )
            console.print(f"✅ {TOKEN_REGISTRY[token_type].name} saved securely")
            return True
        except Exception as e:
            console.print(f"❌ Failed to save token: {e}", style="red")
            return False
    
    def _get_token_from_keyring(self, token_type: AuthType) -> Optional[str]:
        """Get token from system keyring."""
        if not KEYRING_AVAILABLE:
            return None
        try:
            return keyring.get_password(
                self.KEYRING_SERVICE,
                token_type.value
            )
        except Exception:
            return None
    
    def _get_token_from_env(self, token_type: AuthType) -> Optional[str]:
        """Get token from environment variables."""
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
    
    def _get_token_from_config(self, token_type: AuthType) -> Optional[str]:
        """Get token from config file (future implementation)."""
        # TODO: Implement config file reading
        return None
    
    def _raise_token_missing_error(self, token_type: AuthType):
        """Raise informative error when token is missing."""
        metadata = TOKEN_REGISTRY[token_type]
        
        error_message = f"""
❌ {metadata.name} Required

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
    $ tam-rfe config --add-token {token_type.value}
    
  Option 2 (Environment Variable):
    $ export {token_type.value.upper()}_API_TOKEN="your_token_here"

Once configured, run your command again.

Need Help?
  • Documentation: https://gitlab.cee.redhat.com/jbyrd/taminator
  • Contact: jbyrd@redhat.com
"""
        
        console.print(Panel(error_message, border_style="red"))
        raise AuthenticationError(f"{metadata.name} is required but not configured")
    
    # ===== VPN Detection =====
    
    def check_vpn_connection(self) -> AuthResult:
        """
        Detect if Red Hat VPN is connected.
        
        Methods:
        1. Check active NetworkManager connections
        2. Test connectivity to internal service
        """
        # Method 1: Check NetworkManager
        try:
            result = subprocess.run(
                ['nmcli', 'connection', 'show', '--active'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if 'Red Hat Global VPN' in result.stdout or 'vpn' in result.stdout.lower():
                return AuthResult(
                    auth_type=AuthType.VPN,
                    status=AuthStatus.VALID,
                    passed=True,
                    details="VPN connected via NetworkManager"
                )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Method 2: Test connectivity to internal service
        try:
            response = requests.get(
                'https://issues.redhat.com',
                timeout=5
            )
            if response.status_code in [200, 401, 403]:  # Reachable
                return AuthResult(
                    auth_type=AuthType.VPN,
                    status=AuthStatus.VALID,
                    passed=True,
                    details="VPN connectivity verified"
                )
        except requests.exceptions.ConnectionError:
            pass
        
        # VPN not connected
        return AuthResult(
            auth_type=AuthType.VPN,
            status=AuthStatus.MISSING,
            passed=False,
            error="VPN not connected"
        )
    
    # ===== Kerberos Ticket Check =====
    
    def check_kerberos_ticket(self) -> AuthResult:
        """Check if valid Kerberos ticket exists."""
        try:
            result = subprocess.run(
                ['klist', '-s'],
                capture_output=True,
                timeout=2
            )
            
            if result.returncode == 0:
                # Get ticket details
                ticket_info = subprocess.run(
                    ['klist'],
                    capture_output=True,
                    text=True,
                    timeout=2
                ).stdout
                
                # TODO: Parse expiration time
                
                return AuthResult(
                    auth_type=AuthType.KERBEROS,
                    status=AuthStatus.VALID,
                    passed=True,
                    details="Valid Kerberos ticket"
                )
            else:
                return AuthResult(
                    auth_type=AuthType.KERBEROS,
                    status=AuthStatus.MISSING,
                    passed=False,
                    error="No valid Kerberos ticket"
                )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return AuthResult(
                auth_type=AuthType.KERBEROS,
                status=AuthStatus.MISSING,
                passed=False,
                error="Kerberos not available"
            )
    
    # ===== Pre-Flight Checks =====
    
    def preflight_check(self, required_auth: List[AuthType]) -> Dict[AuthType, AuthResult]:
        """
        Check all authentication requirements before operation.
        
        Args:
            required_auth: List of authentication types required
            
        Returns:
            Dictionary mapping AuthType to AuthResult
        """
        results = {}
        
        console.print("\n🔐 Auth-Box: Pre-flight authentication check...\n")
        
        for auth_type in required_auth:
            if auth_type == AuthType.VPN:
                result = self.check_vpn_connection()
            elif auth_type == AuthType.KERBEROS:
                result = self.check_kerberos_ticket()
            elif auth_type in [AuthType.JIRA_TOKEN, AuthType.PORTAL_TOKEN, 
                              AuthType.HYDRA_TOKEN, AuthType.SUPPORTSHELL_TOKEN]:
                # Token check
                token = self.get_token(auth_type, required=False)
                if token:
                    result = AuthResult(
                        auth_type=auth_type,
                        status=AuthStatus.VALID,
                        passed=True,
                        details="Token configured"
                    )
                else:
                    result = AuthResult(
                        auth_type=auth_type,
                        status=AuthStatus.MISSING,
                        passed=False,
                        error="Token not configured"
                    )
            else:
                # Unknown auth type
                result = AuthResult(
                    auth_type=auth_type,
                    status=AuthStatus.MISSING,
                    passed=False,
                    error="Not implemented"
                )
            
            results[auth_type] = result
            
            # Display result
            if result.passed:
                console.print(f"  ✓ {auth_type.value}: {result.details}", style="green")
            else:
                console.print(f"  ✗ {auth_type.value}: {result.error}", style="red")
        
        console.print()
        
        # Check if all passed
        all_passed = all(r.passed for r in results.values())
        
        if all_passed:
            console.print("✅ All authentication requirements met!\n", style="green bold")
        else:
            console.print("❌ Some authentication requirements not met.\n", style="red bold")
            # Show guidance for failed auth
            for auth_type, result in results.items():
                if not result.passed:
                    if auth_type in [AuthType.JIRA_TOKEN, AuthType.PORTAL_TOKEN,
                                    AuthType.HYDRA_TOKEN, AuthType.SUPPORTSHELL_TOKEN]:
                        self._raise_token_missing_error(auth_type)
                    elif auth_type == AuthType.VPN:
                        self._show_vpn_guidance()
                    elif auth_type == AuthType.KERBEROS:
                        self._show_kerberos_guidance()
        
        return results
    
    def _show_vpn_guidance(self):
        """Show guidance for connecting to VPN."""
        guidance = """
❌ Red Hat VPN Required

How To Connect:
  1. Open Red Hat VPN client (or NetworkManager)
  2. Select: "1 - Red Hat Global VPN"
  3. Enter: PIN + Token from authenticator app
  4. Wait for connection (usually 5-10 seconds)

Check VPN status:
  $ nmcli connection show --active | grep VPN

Need Help?
  • VPN Guide: https://source.redhat.com/kb/vpn-setup
"""
        console.print(Panel(guidance, border_style="red"))
        raise AuthenticationError("VPN connection required")
    
    def _show_kerberos_guidance(self):
        """Show guidance for renewing Kerberos ticket."""
        guidance = """
❌ Kerberos Authentication Required

How To Renew:
  Run this command:
    $ kinit
  
  Enter your Red Hat password when prompted.
  Ticket will be valid for 24 hours.

Check ticket status:
  $ klist
"""
        console.print(Panel(guidance, border_style="red"))
        raise AuthenticationError("Kerberos ticket required")


# Global Auth-Box instance
auth_box = AuthBox()


def auth_required(required_auth: List[AuthType]):
    """
    Decorator to require authentication for a command.
    
    Usage:
        @auth_required([AuthType.VPN, AuthType.JIRA_TOKEN])
        def my_command():
            # Only runs if authentication passed
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Run pre-flight check
            results = auth_box.preflight_check(required_auth)
            
            # Only proceed if all auth passed
            if not all(r.passed for r in results.values()):
                return  # Error already displayed
            
            # All auth passed, run command
            return func(*args, **kwargs)
        return wrapper
    return decorator

