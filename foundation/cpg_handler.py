"""
Customer Portal Private Groups (CPG) Integration

Enables posting content to customer private groups on Red Hat Customer Portal:
- TAM call agendas
- T3 blog articles
- Coverage announcements
- Other TAM communications

Authentication: Red Hat SSO (Kerberos or OAuth)
API: Red Hat Customer Portal API

⚠️ IMPORTANT: API ENDPOINTS NEED VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The API endpoints in this file are PLACEHOLDERS and need to be verified
against actual Red Hat Customer Portal API documentation.

See docs/CPG-API-VERIFICATION.md for:
  • How to obtain API documentation
  • How to verify endpoints
  • How to test with curl
  • How to update this file
  • Who to contact for help

Current Status: Framework complete, endpoints need verification
Estimated time to fix: 1 day (with API docs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime


class CPGConfig:
    """CPG configuration manager"""
    
    def __init__(self):
        self.api_base_url = os.getenv('CPG_API_URL', 'https://api.access.redhat.com/rs')
        self.sso_url = os.getenv('CPG_SSO_URL', 'https://sso.redhat.com')
        self.username = os.getenv('CPG_USERNAME', '')
        self.password = os.getenv('CPG_PASSWORD', '')
        self.use_kerberos = os.getenv('CPG_USE_KERBEROS', 'true').lower() == 'true'
        
        # Load from config file if available
        self._load_from_config()
    
    def _load_from_config(self):
        """Load configuration from file"""
        config_locations = [
            Path.home() / ".config" / "rfe-automation" / "cpg.conf",
            Path.home() / ".config" / "pai" / "cpg.conf",
        ]
        
        for config_file in config_locations:
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        self.api_base_url = config.get('api_base_url', self.api_base_url)
                        self.sso_url = config.get('sso_url', self.sso_url)
                        self.username = config.get('username', self.username)
                        self.password = config.get('password', self.password)
                        self.use_kerberos = config.get('use_kerberos', self.use_kerberos)
                        break
                except Exception:
                    continue
    
    def is_configured(self) -> bool:
        """Check if CPG is properly configured"""
        if self.use_kerberos:
            # Check for valid Kerberos ticket
            import subprocess
            try:
                result = subprocess.run(['klist', '-s'], capture_output=True)
                return result.returncode == 0
            except FileNotFoundError:
                return False
        else:
            return bool(self.username and self.password)


class CPGHandler:
    """Handler for Customer Portal Private Groups API"""
    
    def __init__(self):
        self.config = CPGConfig()
        self.session = None
        self._customer_group_cache = {}
    
    def _get_session(self) -> requests.Session:
        """Get or create authenticated session"""
        if self.session is None:
            self.session = requests.Session()
            
            if self.config.use_kerberos:
                # Use Kerberos authentication
                try:
                    from requests_kerberos import HTTPKerberosAuth, OPTIONAL
                    self.session.auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
                except ImportError:
                    print("⚠️  Kerberos support not available. Install: pip install requests-kerberos")
                    return None
            else:
                # Use basic auth
                self.session.auth = (self.config.username, self.config.password)
            
            # Set common headers
            self.session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': 'Taminator/1.0'
            })
        
        return self.session
    
    def get_customer_groups(self, customer_name: str) -> List[Dict]:
        """
        Get private groups for a customer
        
        Args:
            customer_name: Customer name or account number
        
        Returns:
            List of group dictionaries with id, name, description
        """
        if not self.config.is_configured():
            print("❌ CPG not configured")
            return []
        
        # Check cache first
        if customer_name in self._customer_group_cache:
            return self._customer_group_cache[customer_name]
        
        session = self._get_session()
        if not session:
            return []
        
        try:
            # TODO: VERIFY ENDPOINT - See docs/CPG-API-VERIFICATION.md
            # Current endpoint is a placeholder and needs verification against
            # actual Red Hat Customer Portal API documentation.
            # Possible alternatives:
            #   - /rs/customers/{accountNumber}/groups
            #   - /rs/privategroups?account={accountNumber}
            #   - /rs/groups?customer={accountNumber}
            url = f"{self.config.api_base_url}/customers/{customer_name}/groups"
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            groups = response.json()
            self._customer_group_cache[customer_name] = groups
            return groups
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get customer groups: {e}")
            return []
    
    def post_content(
        self,
        customer_name: str,
        title: str,
        content: str,
        content_type: str = "markdown",
        group_id: Optional[str] = None
    ) -> bool:
        """
        Post content to customer private group
        
        Args:
            customer_name: Customer name or account number
            title: Post title
            content: Post content (markdown or HTML)
            content_type: Content format ("markdown" or "html")
            group_id: Specific group ID (optional, uses default if not provided)
        
        Returns:
            True if posted successfully, False otherwise
        """
        if not self.config.is_configured():
            print("❌ CPG not configured")
            print("   Set CPG_* environment variables or create cpg.conf")
            return False
        
        session = self._get_session()
        if not session:
            return False
        
        try:
            # Get group ID if not provided
            if not group_id:
                groups = self.get_customer_groups(customer_name)
                if not groups:
                    print(f"❌ No private groups found for {customer_name}")
                    return False
                
                # Use first group as default
                group_id = groups[0].get('id')
            
            # TODO: VERIFY REQUEST FORMAT - See docs/CPG-API-VERIFICATION.md
            # Current post_data format may need adjustment based on actual API requirements
            post_data = {
                'title': title,
                'content': content,
                'content_type': content_type,
                'timestamp': datetime.now().isoformat(),
                'author': self.config.username or 'TAM',
                'source': 'Taminator'
            }
            
            # TODO: VERIFY ENDPOINT - See docs/CPG-API-VERIFICATION.md
            # Current endpoint is a placeholder and needs verification against
            # actual Red Hat Customer Portal API documentation.
            # Possible alternatives:
            #   - /rs/groups/{groupId}/posts
            #   - /rs/privategroups/{groupId}/content
            #   - /rs/groups/{groupId}/discussions
            url = f"{self.config.api_base_url}/groups/{group_id}/posts"
            response = session.post(url, json=post_data, timeout=30)
            response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to post to CPG: {e}")
            return False
    
    def post_agenda(self, customer_name: str, agenda_file: Path) -> bool:
        """Post TAM call agenda to customer private group"""
        
        if not agenda_file.exists():
            print(f"❌ Agenda file not found: {agenda_file}")
            return False
        
        with open(agenda_file, 'r') as f:
            content = f.read()
        
        # Extract title from first line of markdown
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip() if lines else "TAM Call Agenda"
        
        return self.post_content(
            customer_name=customer_name,
            title=title,
            content=content,
            content_type="markdown"
        )
    
    def post_t3_article(self, customer_name: str, article: Dict) -> bool:
        """Post T3 blog article to customer private group"""
        
        title = f"T3 Article: {article.get('title', 'Recommended Reading')}"
        
        content = f"""# {article.get('title', 'T3 Article')}

**Published:** {article.get('published_date', 'Unknown')}  
**Category:** {article.get('category', 'General')}

## Summary

{article.get('summary', 'No summary available')}

## Read More

{article.get('url', '#')}

---

*Shared by your Red Hat TAM via Taminator*
"""
        
        return self.post_content(
            customer_name=customer_name,
            title=title,
            content=content,
            content_type="markdown"
        )
    
    def post_coverage_announcement(self, customer_name: str, announcement_file: Path) -> bool:
        """Post coverage announcement to customer private group"""
        
        if not announcement_file.exists():
            print(f"❌ Announcement file not found: {announcement_file}")
            return False
        
        with open(announcement_file, 'r') as f:
            content = f.read()
        
        title = "TAM Out of Office Notification"
        
        return self.post_content(
            customer_name=customer_name,
            title=title,
            content=content,
            content_type="markdown"
        )


# Convenience function for direct imports
_handler = None

def get_cpg_handler() -> CPGHandler:
    """Get CPG handler instance"""
    global _handler
    if _handler is None:
        _handler = CPGHandler()
    return _handler


def post_to_cpg(customer_name: str, title: str, content: str) -> bool:
    """Post content to CPG (convenience function)"""
    handler = get_cpg_handler()
    return handler.post_content(customer_name, title, content)

