"""
HashiCorp Vault Client for Taminator.

Provides enterprise-grade secrets management as an upgrade to Auth Box.

Features:
- Centralized credential storage
- Audit logging
- Token rotation
- Policy-based access
- Team collaboration ready

Usage:
    from taminator.core.vault_client import vault_client
    
    # Store a token
    vault_client.set_token('jira', 'my-token')
    
    # Retrieve a token
    token = vault_client.get_token('jira')
    
    # Check Vault status
    if vault_client.is_available():
        print("Vault is ready!")
"""

import os
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

try:
    from rich.console import Console
    console = Console()
except ImportError:
    console = None


@dataclass
class VaultConfig:
    """Vault connection configuration."""
    addr: str = "http://192.168.1.34:8201"
    token: Optional[str] = None
    namespace: str = "pai/taminator"
    
    @classmethod
    def from_env(cls) -> 'VaultConfig':
        """Load config from environment variables."""
        return cls(
            addr=os.environ.get('VAULT_ADDR', cls.addr),
            token=os.environ.get('VAULT_TOKEN'),
            namespace=os.environ.get('VAULT_NAMESPACE', cls.namespace)
        )


class VaultClient:
    """
    HashiCorp Vault client for Taminator credentials.
    
    This is an enterprise upgrade to Auth Box, providing:
    - Centralized secrets (one source of truth)
    - Audit logging (who accessed what, when)
    - Team sharing (multiple TAMs can share tokens)
    - Rotation support (update tokens without breaking tools)
    - Policy enforcement (read-only vs full access)
    """
    
    def __init__(self, config: Optional[VaultConfig] = None):
        """Initialize Vault client."""
        self.config = config or VaultConfig.from_env()
        self._session = requests.Session()
        self._session.verify = False  # MiracleMax uses self-signed certs
        
        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def is_available(self) -> bool:
        """Check if Vault is accessible and unsealed."""
        try:
            response = self._session.get(
                f"{self.config.addr}/v1/sys/health",
                timeout=2
            )
            health = response.json()
            return health.get('initialized') and not health.get('sealed')
        except Exception:
            return False
    
    def get_token(self, service: str) -> Optional[str]:
        """
        Retrieve authentication token from Vault.
        
        Args:
            service: Service name (jira, portal, github, etc.)
            
        Returns:
            Token string if found, None otherwise
        """
        if not self.config.token:
            return None
        
        try:
            secret_path = f"{self.config.namespace}/{service}"
            response = self._session.get(
                f"{self.config.addr}/v1/{secret_path}",
                headers={'X-Vault-Token': self.config.token},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['data']['data'].get('token')
            
            return None
            
        except Exception as e:
            if console:
                console.print(f"[yellow]⚠️  Vault read failed: {e}[/yellow]")
            return None
    
    def set_token(self, service: str, token: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store authentication token in Vault.
        
        Args:
            service: Service name (jira, portal, github, etc.)
            token: The authentication token
            metadata: Optional metadata (description, expiry, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.config.token:
            if console:
                console.print("[red]❌ VAULT_TOKEN not set[/red]")
            return False
        
        try:
            secret_path = f"{self.config.namespace}/{service}"
            
            payload = {
                'token': token,
                'stored_at': datetime.now().isoformat(),
                'stored_by': os.environ.get('USER', 'unknown')
            }
            
            if metadata:
                payload.update(metadata)
            
            response = self._session.post(
                f"{self.config.addr}/v1/{secret_path}",
                headers={'X-Vault-Token': self.config.token},
                json={'data': payload},
                timeout=5
            )
            
            return response.status_code in [200, 204]
            
        except Exception as e:
            if console:
                console.print(f"[red]❌ Vault write failed: {e}[/red]")
            return False
    
    def delete_token(self, service: str) -> bool:
        """Delete token from Vault."""
        if not self.config.token:
            return False
        
        try:
            secret_path = f"{self.config.namespace}/{service}"
            response = self._session.delete(
                f"{self.config.addr}/v1/{secret_path}",
                headers={'X-Vault-Token': self.config.token},
                timeout=5
            )
            return response.status_code in [200, 204]
        except Exception:
            return False
    
    def list_tokens(self) -> list:
        """List all tokens stored in Vault."""
        if not self.config.token:
            return []
        
        try:
            response = self._session.get(
                f"{self.config.addr}/v1/{self.config.namespace}?list=true",
                headers={'X-Vault-Token': self.config.token},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('keys', [])
            
            return []
            
        except Exception:
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get Vault connection status."""
        try:
            response = self._session.get(
                f"{self.config.addr}/v1/sys/health",
                timeout=2
            )
            health = response.json()
            
            return {
                'available': True,
                'initialized': health.get('initialized', False),
                'sealed': health.get('sealed', True),
                'version': health.get('version', 'unknown'),
                'addr': self.config.addr
            }
        except Exception as e:
            return {
                'available': False,
                'error': str(e),
                'addr': self.config.addr
            }


# Global Vault client instance
vault_client = VaultClient()


def migrate_from_authbox():
    """
    Migrate Auth Box tokens to Vault.
    
    This function reads tokens from Auth Box storage and migrates them to Vault.
    Run this once to upgrade from Auth Box to Vault.
    """
    if console:
        console.print("\n[cyan]🔄 Migrating Auth Box tokens to Vault...[/cyan]\n")
    
    try:
        from taminator.core.auth_box import auth_box
        from taminator.core.auth_types import AuthType
        
        migrated = 0
        failed = 0
        
        # Token types to migrate
        token_types = [
            (AuthType.JIRA_TOKEN, 'jira'),
            (AuthType.PORTAL_TOKEN, 'portal'),
            (AuthType.GITHUB_TOKEN, 'github'),
            (AuthType.SUPPORTSHELL_TOKEN, 'supportshell'),
            (AuthType.HYDRA_TOKEN, 'hydra'),
        ]
        
        for auth_type, service_name in token_types:
            token = auth_box.get_token(auth_type, required=False)
            if token:
                if vault_client.set_token(service_name, token, {'migrated_from': 'authbox'}):
                    if console:
                        console.print(f"  ✅ Migrated {service_name} token")
                    migrated += 1
                else:
                    if console:
                        console.print(f"  ❌ Failed to migrate {service_name}")
                    failed += 1
        
        if console:
            console.print(f"\n[green]✅ Migration complete: {migrated} tokens migrated[/green]")
            if failed > 0:
                console.print(f"[yellow]⚠️  {failed} tokens failed to migrate[/yellow]")
        
        return migrated, failed
        
    except Exception as e:
        if console:
            console.print(f"[red]❌ Migration failed: {e}[/red]")
        return 0, 0

