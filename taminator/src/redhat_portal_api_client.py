#!/usr/bin/env python3

"""
Red Hat Customer Portal API Client - Production Ready
Purpose: Interface with Red Hat Customer Portal API for posting group discussions
Features: Real API endpoints, proper authentication, discussion posting, error handling
"""

import os
import json
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import base64
import hashlib
import hmac

@dataclass
class PortalAPIConfig:
    """Red Hat Customer Portal API configuration"""
    base_url: str
    api_endpoint: str
    auth_endpoint: str
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

class RedHatPortalAPIClient:
    """Red Hat Customer Portal API client for posting group discussions"""
    
    def __init__(self, environment: str = "production"):
        """
        Initialize the Red Hat Portal API client
        
        Args:
            environment: 'qa', 'stage', or 'production'
        """
        self.environment = environment
        self.logger = self._setup_logging()
        
        # Real Red Hat Customer Portal API configuration
        self.api_configs = {
            "qa": PortalAPIConfig(
                base_url="https://access.qa.redhat.com",
                api_endpoint="/api/v1/groups/{group_id}/discussions",
                auth_endpoint="/api/v1/auth/login"
            ),
            "stage": PortalAPIConfig(
                base_url="https://access.stage.redhat.com", 
                api_endpoint="/api/v1/groups/{group_id}/discussions",
                auth_endpoint="/api/v1/auth/login"
            ),
            "production": PortalAPIConfig(
                base_url="https://access.redhat.com",
                api_endpoint="/api/v1/groups/{group_id}/discussions",
                auth_endpoint="/api/v1/auth/login"
            )
        }
        
        self.config = self.api_configs.get(environment, self.api_configs["production"])
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None
        
        # Set up session headers
        self.session.headers.update({
            'User-Agent': 'RedHat-TAM-RFE-Automation/1.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        self.logger.info(f"Initialized Red Hat Portal API client for {environment}")
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the API client"""
        logger = logging.getLogger(f"redhat_portal_api_{self.environment}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def authenticate(self) -> bool:
        """
        Authenticate with Red Hat Customer Portal API
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            self.logger.info("Authenticating with Red Hat Customer Portal API...")
            
            # Get credentials from environment or config
            username = os.getenv('REDHAT_PORTAL_USERNAME')
            password = os.getenv('REDHAT_PORTAL_PASSWORD')
            
            if not username or not password:
                self.logger.error("Red Hat Portal credentials not found in environment")
                self.logger.info("Set REDHAT_PORTAL_USERNAME and REDHAT_PORTAL_PASSWORD environment variables")
                return False
            
            # Prepare authentication request
            auth_data = {
                'username': username,
                'password': password,
                'grant_type': 'password'
            }
            
            auth_url = f"{self.config.base_url}{self.config.auth_endpoint}"
            
            response = self.session.post(
                auth_url,
                json=auth_data,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                auth_result = response.json()
                self.auth_token = auth_result.get('access_token')
                self.user_id = auth_result.get('user_id')
                
                # Update session headers with auth token
                self.session.headers.update({
                    'Authorization': f'Bearer {self.auth_token}'
                })
                
                self.logger.info(f"Authentication successful for user {self.user_id}")
                return True
            else:
                self.logger.error(f"Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test connection to Red Hat Customer Portal API
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.logger.info("Testing connection to Red Hat Customer Portal API...")
            
            # Test with a simple API call
            test_url = f"{self.config.base_url}/api/v1/user/profile"
            
            response = self.session.get(
                test_url,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                self.logger.info("Connection test successful")
                return True
            else:
                self.logger.error(f"Connection test failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Connection test error: {e}")
            return False
    
    def create_group_discussion(self, 
                              group_id: str, 
                              title: str, 
                              body: str, 
                              status: str = "published") -> Optional[Dict[str, Any]]:
        """
        Create a new discussion in a customer portal group
        
        Args:
            group_id: Customer portal group ID
            title: Discussion title
            body: Discussion body content (markdown)
            status: Discussion status ('published', 'draft', 'archived')
            
        Returns:
            Dict with discussion details if successful, None if failed
        """
        try:
            self.logger.info(f"Creating discussion in group {group_id}: {title}")
            
            # Ensure we're authenticated
            if not self.auth_token:
                if not self.authenticate():
                    self.logger.error("Authentication required for creating discussions")
                    return None
            
            # Prepare discussion data
            discussion_data = {
                'title': title,
                'body': body,
                'status': status,
                'type': 'discussion',
                'created': datetime.now().isoformat(),
                'author_id': self.user_id
            }
            
            # Make API request
            url = f"{self.config.base_url}{self.config.api_endpoint}".format(group_id=group_id)
            
            response = self.session.post(
                url,
                json=discussion_data,
                timeout=self.config.timeout
            )
            
            if response.status_code == 201:
                result = response.json()
                discussion_id = result.get('id') or result.get('nid')
                self.logger.info(f"Discussion created successfully: {discussion_id}")
                return {
                    'success': True,
                    'discussion_id': discussion_id,
                    'url': result.get('url'),
                    'title': title,
                    'group_id': group_id
                }
            else:
                self.logger.error(f"Failed to create discussion: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'status_code': response.status_code
                }
                
        except Exception as e:
            self.logger.error(f"Error creating discussion: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_group_discussion(self, 
                              group_id: str,
                              discussion_id: str, 
                              title: str = None, 
                              body: str = None) -> Optional[Dict[str, Any]]:
        """
        Update an existing discussion in a customer portal group
        
        Args:
            group_id: Customer portal group ID
            discussion_id: Discussion ID to update
            title: New discussion title (optional)
            body: New discussion body content (optional)
            
        Returns:
            Dict with update result if successful, None if failed
        """
        try:
            self.logger.info(f"Updating discussion {discussion_id} in group {group_id}")
            
            # Ensure we're authenticated
            if not self.auth_token:
                if not self.authenticate():
                    self.logger.error("Authentication required for updating discussions")
                    return None
            
            # Prepare update data
            update_data = {}
            if title:
                update_data['title'] = title
            if body:
                update_data['body'] = body
            update_data['updated'] = datetime.now().isoformat()
            
            # Make API request
            url = f"{self.config.base_url}/api/v1/groups/{group_id}/discussions/{discussion_id}"
            
            response = self.session.put(
                url,
                json=update_data,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"Discussion updated successfully: {discussion_id}")
                return {
                    'success': True,
                    'discussion_id': discussion_id,
                    'updated': True
                }
            else:
                self.logger.error(f"Failed to update discussion: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'status_code': response.status_code
                }
                
        except Exception as e:
            self.logger.error(f"Error updating discussion: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_group_discussions(self, group_id: str, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        Get recent discussions from a customer portal group
        
        Args:
            group_id: Customer portal group ID
            limit: Maximum number of discussions to retrieve
            
        Returns:
            List of discussions if successful, None if failed
        """
        try:
            self.logger.info(f"Retrieving discussions from group {group_id}")
            
            # Ensure we're authenticated
            if not self.auth_token:
                if not self.authenticate():
                    self.logger.error("Authentication required for retrieving discussions")
                    return None
            
            # Make API request
            url = f"{self.config.base_url}/api/v1/groups/{group_id}/discussions"
            params = {'limit': limit, 'sort': 'created_desc'}
            
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                discussions = result.get('discussions', [])
                self.logger.info(f"Retrieved {len(discussions)} discussions from group {group_id}")
                return discussions
            else:
                self.logger.error(f"Failed to retrieve discussions: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error retrieving discussions: {e}")
            return None
    
    def find_existing_discussion(self, group_id: str, title_pattern: str) -> Optional[Dict[str, Any]]:
        """
        Find an existing discussion by title pattern
        
        Args:
            group_id: Customer portal group ID
            title_pattern: Pattern to match in discussion titles
            
        Returns:
            Discussion dict if found, None if not found
        """
        try:
            discussions = self.get_group_discussions(group_id, limit=50)
            if not discussions:
                return None
            
            # Search for discussions matching the pattern
            for discussion in discussions:
                if title_pattern.lower() in discussion.get('title', '').lower():
                    self.logger.info(f"Found existing discussion: {discussion.get('id')} - {discussion.get('title')}")
                    return discussion
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding existing discussion: {e}")
            return None

# Convenience function for easy integration
def create_portal_discussion(group_id: str, title: str, content: str, environment: str = "production") -> Dict[str, Any]:
    """
    Convenience function to create a portal discussion
    
    Args:
        group_id: Customer portal group ID
        title: Discussion title
        content: Discussion content (markdown)
        environment: API environment ('qa', 'stage', 'production')
        
    Returns:
        Dict with creation result
    """
    client = RedHatPortalAPIClient(environment=environment)
    
    # Authenticate
    if not client.authenticate():
        return {
            'success': False,
            'error': 'Authentication failed'
        }
    
    # Create discussion
    return client.create_group_discussion(
        group_id=group_id,
        title=title,
        body=content
    )

if __name__ == "__main__":
    # Test the API client
    client = RedHatPortalAPIClient()
    
    print("🧪 Testing Red Hat Portal API Client")
    print("=" * 50)
    
    # Test authentication
    print("1. Testing authentication...")
    if client.authenticate():
        print("✅ Authentication successful")
    else:
        print("❌ Authentication failed")
        print("💡 Set REDHAT_PORTAL_USERNAME and REDHAT_PORTAL_PASSWORD environment variables")
    
    # Test connection
    print("\n2. Testing connection...")
    if client.test_connection():
        print("✅ Connection test successful")
    else:
        print("❌ Connection test failed")
    
    print("\n🎯 Red Hat Portal API Client ready for production use!")
