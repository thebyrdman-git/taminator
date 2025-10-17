"""
Salesforce Integration Handler

Enables writing case updates, comments, and status changes to Salesforce.
Provides framework for automating case management workflows.
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


class SalesforceConfig:
    """Salesforce configuration manager"""
    
    def __init__(self):
        self.instance_url = os.getenv('SALESFORCE_INSTANCE_URL', '')
        self.client_id = os.getenv('SALESFORCE_CLIENT_ID', '')
        self.client_secret = os.getenv('SALESFORCE_CLIENT_SECRET', '')
        self.username = os.getenv('SALESFORCE_USERNAME', '')
        self.password = os.getenv('SALESFORCE_PASSWORD', '')
        self.security_token = os.getenv('SALESFORCE_SECURITY_TOKEN', '')
        self.access_token = None
        
        # Load from config file if available
        self._load_from_config()
    
    def _load_from_config(self):
        """Load configuration from file"""
        config_locations = [
            Path.home() / ".config" / "rfe-automation" / "salesforce.conf",
            Path.home() / ".config" / "pai" / "salesforce.conf",
        ]
        
        for config_file in config_locations:
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        self.instance_url = config.get('instance_url', self.instance_url)
                        self.client_id = config.get('client_id', self.client_id)
                        self.client_secret = config.get('client_secret', self.client_secret)
                        self.username = config.get('username', self.username)
                        self.password = config.get('password', self.password)
                        self.security_token = config.get('security_token', self.security_token)
                        self.access_token = config.get('access_token')
                        break
                except Exception:
                    continue
    
    def is_configured(self) -> bool:
        """Check if Salesforce is properly configured"""
        # Need either access token or credentials
        if self.access_token:
            return bool(self.instance_url)
        
        return bool(
            self.instance_url and
            self.client_id and
            self.client_secret and
            self.username and
            self.password
        )


class SalesforceHandler:
    """Handler for Salesforce API write operations"""
    
    def __init__(self):
        self.config = SalesforceConfig()
        self.session = None
    
    def _authenticate(self) -> bool:
        """
        Authenticate with Salesforce using OAuth2 password flow
        
        Returns:
            True if authentication successful
        """
        if self.config.access_token:
            # Already have access token
            return True
        
        if not self.config.is_configured():
            return False
        
        try:
            # OAuth2 password flow
            auth_url = f"{self.config.instance_url}/services/oauth2/token"
            
            data = {
                'grant_type': 'password',
                'client_id': self.config.client_id,
                'client_secret': self.config.client_secret,
                'username': self.config.username,
                'password': self.config.password + self.config.security_token
            }
            
            response = requests.post(auth_url, data=data, timeout=30)
            response.raise_for_status()
            
            auth_data = response.json()
            self.config.access_token = auth_data.get('access_token')
            self.config.instance_url = auth_data.get('instance_url', self.config.instance_url)
            
            return bool(self.config.access_token)
            
        except Exception as e:
            print(f"❌ Salesforce authentication failed: {e}")
            return False
    
    def _get_session(self) -> Optional[requests.Session]:
        """Get or create authenticated session"""
        if not self._authenticate():
            return None
        
        if self.session is None:
            self.session = requests.Session()
            self.session.headers.update({
                'Authorization': f'Bearer {self.config.access_token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
        
        return self.session
    
    def add_case_comment(
        self,
        case_number: str,
        comment: str,
        is_public: bool = True
    ) -> bool:
        """
        Add a comment to a Salesforce case
        
        Args:
            case_number: Case number (e.g., "04280915")
            comment: Comment text
            is_public: Whether comment is visible to customer
        
        Returns:
            True if comment added successfully
        """
        session = self._get_session()
        if not session:
            print("❌ Salesforce not configured")
            return False
        
        try:
            # Find case ID from case number
            case_id = self._get_case_id(case_number)
            if not case_id:
                print(f"❌ Case {case_number} not found in Salesforce")
                return False
            
            # Create case comment
            url = f"{self.config.instance_url}/services/data/v59.0/sobjects/CaseComment"
            
            data = {
                'ParentId': case_id,
                'CommentBody': comment,
                'IsPublished': is_public
            }
            
            response = session.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to add comment: {e}")
            return False
    
    def update_case_status(
        self,
        case_number: str,
        status: str,
        comment: Optional[str] = None
    ) -> bool:
        """
        Update case status in Salesforce
        
        Args:
            case_number: Case number
            status: New status (e.g., "Waiting on Customer", "In Progress", "Closed")
            comment: Optional comment to add with status change
        
        Returns:
            True if status updated successfully
        """
        session = self._get_session()
        if not session:
            print("❌ Salesforce not configured")
            return False
        
        try:
            # Find case ID
            case_id = self._get_case_id(case_number)
            if not case_id:
                print(f"❌ Case {case_number} not found in Salesforce")
                return False
            
            # Update case status
            url = f"{self.config.instance_url}/services/data/v59.0/sobjects/Case/{case_id}"
            
            data = {'Status': status}
            
            response = session.patch(url, json=data, timeout=30)
            response.raise_for_status()
            
            # Add comment if provided
            if comment:
                self.add_case_comment(case_number, comment, is_public=True)
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to update status: {e}")
            return False
    
    def close_case(
        self,
        case_number: str,
        resolution: str,
        close_code: str = "Solved"
    ) -> bool:
        """
        Close a Salesforce case
        
        Args:
            case_number: Case number
            resolution: Resolution description
            close_code: Close code (e.g., "Solved", "Not a Bug", "Duplicate")
        
        Returns:
            True if case closed successfully
        """
        session = self._get_session()
        if not session:
            print("❌ Salesforce not configured")
            return False
        
        try:
            # Find case ID
            case_id = self._get_case_id(case_number)
            if not case_id:
                print(f"❌ Case {case_number} not found in Salesforce")
                return False
            
            # Close case
            url = f"{self.config.instance_url}/services/data/v59.0/sobjects/Case/{case_id}"
            
            data = {
                'Status': 'Closed',
                'Resolution__c': resolution,
                'Close_Code__c': close_code
            }
            
            response = session.patch(url, json=data, timeout=30)
            response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to close case: {e}")
            return False
    
    def update_case_fields(
        self,
        case_number: str,
        fields: Dict[str, Any]
    ) -> bool:
        """
        Update arbitrary case fields in Salesforce
        
        Args:
            case_number: Case number
            fields: Dictionary of field names and values
        
        Returns:
            True if fields updated successfully
        """
        session = self._get_session()
        if not session:
            print("❌ Salesforce not configured")
            return False
        
        try:
            # Find case ID
            case_id = self._get_case_id(case_number)
            if not case_id:
                print(f"❌ Case {case_number} not found in Salesforce")
                return False
            
            # Update fields
            url = f"{self.config.instance_url}/services/data/v59.0/sobjects/Case/{case_id}"
            
            response = session.patch(url, json=fields, timeout=30)
            response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to update case: {e}")
            return False
    
    def _get_case_id(self, case_number: str) -> Optional[str]:
        """
        Get Salesforce case ID from case number
        
        Args:
            case_number: Case number (e.g., "04280915")
        
        Returns:
            Salesforce case ID or None
        """
        session = self._get_session()
        if not session:
            return None
        
        try:
            # Query for case ID
            query = f"SELECT Id FROM Case WHERE CaseNumber = '{case_number}'"
            url = f"{self.config.instance_url}/services/data/v59.0/query"
            
            response = session.get(url, params={'q': query}, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            records = data.get('records', [])
            
            if records:
                return records[0].get('Id')
            
            return None
            
        except Exception:
            return None
    
    def bulk_add_comments(
        self,
        cases: List[Dict[str, str]],
        is_public: bool = True
    ) -> Dict[str, bool]:
        """
        Add comments to multiple cases
        
        Args:
            cases: List of dicts with 'case_number' and 'comment'
            is_public: Whether comments are visible to customer
        
        Returns:
            Dict mapping case numbers to success status
        """
        results = {}
        
        for case in cases:
            case_number = case.get('case_number')
            comment = case.get('comment')
            
            if case_number and comment:
                success = self.add_case_comment(case_number, comment, is_public)
                results[case_number] = success
        
        return results
    
    def post_agenda_update(
        self,
        customer: str,
        cases: List[Dict],
        agenda_summary: str
    ) -> int:
        """
        Post TAM call agenda updates to related cases
        
        Args:
            customer: Customer name
            cases: List of case dicts from agenda
            agenda_summary: Summary of agenda/call
        
        Returns:
            Number of cases updated
        """
        updated_count = 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        for case in cases:
            case_number = case.get('number')
            if not case_number:
                continue
            
            comment = f"""TAM Call Update ({timestamp})

{agenda_summary}

Next Steps: As discussed in TAM call

---
Posted automatically by Taminator
"""
            
            if self.add_case_comment(case_number, comment, is_public=True):
                updated_count += 1
        
        return updated_count


# Convenience functions
_handler = None

def get_salesforce_handler() -> SalesforceHandler:
    """Get Salesforce handler instance"""
    global _handler
    if _handler is None:
        _handler = SalesforceHandler()
    return _handler


def add_case_comment(case_number: str, comment: str, is_public: bool = True) -> bool:
    """Add case comment (convenience function)"""
    handler = get_salesforce_handler()
    return handler.add_case_comment(case_number, comment, is_public)


def update_case_status(case_number: str, status: str, comment: Optional[str] = None) -> bool:
    """Update case status (convenience function)"""
    handler = get_salesforce_handler()
    return handler.update_case_status(case_number, status, comment)


def close_case(case_number: str, resolution: str, close_code: str = "Solved") -> bool:
    """Close case (convenience function)"""
    handler = get_salesforce_handler()
    return handler.close_case(case_number, resolution, close_code)

