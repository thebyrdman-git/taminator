"""
Hybrid Authentication System for Taminator.

Tries Vault first, falls back to Auth Box.
This allows gradual migration from Auth Box to Vault.

Usage:
    from taminator.core.hybrid_auth import hybrid_auth
    
    # Get token (tries Vault, then Auth Box)
    token = hybrid_auth.get_token('jira')
    
    # Set token (stores in both Vault and Auth Box)
    hybrid_auth.set_token('jira', 'my-token')
"""

from typing import Optional
from .vault_client import vault_client
from .auth_box import auth_box
from .auth_types import AuthType

try:
    from rich.console import Console
    console = Console()
except ImportError:
    console = None


# Mapping between service names and AuthType enum
SERVICE_TO_AUTHTYPE = {
    'jira': AuthType.JIRA_TOKEN,
    'portal': AuthType.PORTAL_TOKEN,
    'github': AuthType.GITHUB_TOKEN,
    'supportshell': AuthType.SUPPORTSHELL_TOKEN,
    'hydra': AuthType.HYDRA_TOKEN,
}


class HybridAuth:
    """
    Hybrid authentication system.
    
    Strategy:
    1. Try Vault first (if available)
    2. Fall back to Auth Box
    3. When storing, write to both (sync)
    
    This allows:
    - Gradual migration to Vault
    - Zero downtime during transition
    - Vault as single source of truth (eventually)
    """
    
    def __init__(self):
        """Initialize hybrid auth."""
        self._vault_available = None
    
    def is_vault_available(self) -> bool:
        """Check if Vault is available (cached)."""
        if self._vault_available is None:
            self._vault_available = vault_client.is_available()
        return self._vault_available
    
    def get_token(self, service: str, required: bool = True) -> Optional[str]:
        """
        Get token with Vault-first strategy.
        
        Args:
            service: Service name (jira, portal, github, etc.)
            required: If True, raise error if not found
            
        Returns:
            Token string if found, None otherwise
        """
        # Try Vault first
        if self.is_vault_available():
            token = vault_client.get_token(service)
            if token:
                if console and os.environ.get('TAMINATOR_DEBUG'):
                    console.print(f"[dim]🔐 Retrieved {service} token from Vault[/dim]")
                return token
        
        # Fall back to Auth Box
        auth_type = SERVICE_TO_AUTHTYPE.get(service)
        if auth_type:
            token = auth_box.get_token(auth_type, required=required)
            if token and console and os.environ.get('TAMINATOR_DEBUG'):
                console.print(f"[dim]📦 Retrieved {service} token from Auth Box[/dim]")
            return token
        
        if required:
            raise ValueError(f"Unknown service: {service}")
        
        return None
    
    def set_token(self, service: str, token: str, metadata: Optional[dict] = None) -> bool:
        """
        Store token in both Vault and Auth Box.
        
        Args:
            service: Service name
            token: Authentication token
            metadata: Optional metadata
            
        Returns:
            True if stored in at least one location
        """
        vault_success = False
        authbox_success = False
        
        # Store in Vault if available
        if self.is_vault_available():
            vault_success = vault_client.set_token(service, token, metadata)
            if vault_success and console:
                console.print(f"[green]✅ Stored {service} token in Vault[/green]")
        
        # Store in Auth Box as backup
        auth_type = SERVICE_TO_AUTHTYPE.get(service)
        if auth_type:
            authbox_success = auth_box.set_token(auth_type, token)
            if authbox_success and console:
                console.print(f"[green]✅ Stored {service} token in Auth Box[/green]")
        
        return vault_success or authbox_success
    
    def get_status(self) -> dict:
        """Get authentication system status."""
        vault_status = vault_client.get_status() if self.is_vault_available() else {'available': False}
        
        return {
            'vault': vault_status,
            'auth_box': {
                'available': True,  # Auth Box is always available locally
                'keyring': auth_box.KEYRING_AVAILABLE if hasattr(auth_box, 'KEYRING_AVAILABLE') else False
            },
            'strategy': 'vault-first' if vault_status['available'] else 'auth-box-only'
        }
    
    def migrate_to_vault(self) -> tuple:
        """Migrate all Auth Box tokens to Vault."""
        from .vault_client import migrate_from_authbox
        return migrate_from_authbox()


# Global hybrid auth instance
hybrid_auth = HybridAuth()


# Import guard
import os

