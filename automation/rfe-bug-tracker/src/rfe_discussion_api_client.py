#!/usr/bin/env python3

"""
RFE Discussion API Client
Purpose: API client for posting RFE/Bug tracker content to Red Hat Customer Portal Groups
Integrates: JWT authentication + 3-table RFE system + Customer portal management
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from redhat_portal_api_client import RedHatPortalAPIClient
from customer_template_renderer import CustomerTemplateRenderer

class RFEDiscussionAPIClient:
    """Enhanced API client for posting RFE discussions to customer portal groups"""
    
    def __init__(self, environment: str = "qa"):
        """
        Initialize the RFE Discussion API Client
        
        Args:
            environment: 'qa', 'stage', or 'production'
        """
        self.environment = environment
        self.portal_client = RedHatPortalAPIClient(environment)
        self.template_renderer = CustomerTemplateRenderer()
        
        # Customer portal group mappings (auto-discovered)
        self.customer_groups = {
            "wellsfargo": {
                "name": "Wells Fargo",
                "group_id": "4357341",  # Confirmed - Wells Fargo Active Cases
                "portal_url": "https://access.redhat.com/groups/4357341/discussions/7047245",
                "template_key": "wellsfargo"
            },
            "jpmc": {
                "name": "JPMC",
                "group_id": "6956770",  # Confirmed - JP Morgan Chase
                "portal_url": "https://access.redhat.com/groups/6956770",
                "template_key": "jpmc"
            },
            "tdbank": {
                "name": "TD Bank",
                "group_id": "7028358",  # Extracted - Sandbox/Testing
                "portal_url": "https://access.redhat.com/groups/7028358/discussions/7073164",
                "template_key": "tdbank"
            },
            "fanniemae": {
                "name": "Fannie Mae", 
                "group_id": "7095107",  # Confirmed - Fannie Mae
                "portal_url": "https://access.redhat.com/groups/7095107",
                "template_key": "fanniemae"
            }
        }
        
        print(f"🎯 RFE Discussion API Client initialized for {environment.upper()}")
        print(f"   Managing {len(self.customer_groups)} customer groups")
    
    def authenticate(self) -> bool:
        """Authenticate with the CPPG API"""
        print("🔐 Authenticating RFE Discussion API Client...")
        return self.cppg_client.authenticate()
    
    def discover_customer_group_ids(self) -> Dict[str, Optional[int]]:
        """
        Discover real customer group IDs from portal URLs
        This is a placeholder - in production, we'd need to:
        1. Parse portal URLs to extract group IDs
        2. Query the API to validate group access
        3. Store group IDs in configuration
        """
        print("🔍 Discovering customer group IDs...")
        
        discovered_ids = {}
        
        for customer_key, customer_info in self.customer_groups.items():
            portal_url = customer_info["portal_url"]
            
            # Extract group ID from portal URL (simple parsing)
            try:
                # URLs like: https://access.redhat.com/groups/7028358
                if "/groups/" in portal_url:
                    group_id_str = portal_url.split("/groups/")[-1].split("/")[0]
                    if group_id_str.isdigit():
                        group_id = int(group_id_str)
                        discovered_ids[customer_key] = group_id
                        self.customer_groups[customer_key]["group_id"] = group_id
                        print(f"   ✅ {customer_info['name']}: Group ID {group_id}")
                    else:
                        discovered_ids[customer_key] = None
                        print(f"   ❌ {customer_info['name']}: Could not extract group ID from {portal_url}")
                else:
                    discovered_ids[customer_key] = None
                    print(f"   ❌ {customer_info['name']}: Invalid portal URL format")
                    
            except Exception as e:
                discovered_ids[customer_key] = None
                print(f"   ❌ {customer_info['name']}: Error parsing URL - {e}")
        
        return discovered_ids
    
    def validate_group_access(self, customer_key: str) -> bool:
        """Validate that we have access to post to a customer's group"""
        customer_info = self.customer_groups.get(customer_key)
        if not customer_info:
            print(f"❌ Unknown customer: {customer_key}")
            return False
            
        group_id = customer_info.get("group_id")
        if not group_id:
            print(f"❌ No group ID for {customer_info['name']}")
            return False
        
        print(f"🧪 Validating group access for {customer_info['name']} (Group {group_id})...")
        
        # Try to create a test discussion (draft mode)
        test_result = self.cppg_client.create_discussion(
            group_id=group_id,
            title="API Access Test - Please Ignore",
            body="This is an automated test to validate API access. This draft will be deleted.",
            status=False  # Draft mode - not published
        )
        
        if test_result:
            print(f"   ✅ Group access validated for {customer_info['name']}")
            return True
        else:
            print(f"   ❌ Group access validation failed for {customer_info['name']}")
            return False
    
    def generate_rfe_discussion_title(self, customer_name: str, rfe_count: int, bug_count: int) -> str:
        """Generate a descriptive title for the RFE discussion"""
        timestamp = datetime.now().strftime("%B %d, %Y")
        total_cases = rfe_count + bug_count
        return f"RFE/Bug Tracker Update - {customer_name} - {total_cases} Cases ({rfe_count} RFE, {bug_count} Bug) - {timestamp}"
    
    def post_rfe_discussion(self, customer_key: str, cases: List[Dict], update_existing: bool = False) -> Optional[Dict]:
        """
        Post RFE/Bug tracker content as a discussion to customer portal group
        
        Args:
            customer_key: Customer identifier (e.g., 'wellsfargo', 'jpmc')
            cases: List of RFE/Bug cases with enriched data
            update_existing: Whether to update existing discussion or create new one
            
        Returns:
            Dict with posting result or None if failed
        """
        customer_info = self.customer_groups.get(customer_key)
        if not customer_info:
            print(f"❌ Unknown customer: {customer_key}")
            return None
            
        customer_name = customer_info["name"]
        group_id = customer_info.get("group_id")
        template_key = customer_info.get("template_key", customer_key)
        
        if not group_id:
            print(f"❌ No group ID configured for {customer_name}")
            return None
        
        print(f"📝 Posting RFE discussion for {customer_name} (Group {group_id})...")
        
        # Separate cases by type and status for 3-table structure
        active_rfe_cases = [c for c in cases if c.get('rfe_type') == 'RFE' and not self._is_closed_status(c)]
        active_bug_cases = [c for c in cases if c.get('rfe_type') == 'Bug' and not self._is_closed_status(c)]
        closed_cases = [c for c in cases if self._is_closed_status(c)]
        
        print(f"   📊 Content breakdown: {len(active_rfe_cases)} RFE, {len(active_bug_cases)} Bug, {len(closed_cases)} Closed")
        
        # Generate discussion title
        discussion_title = self.generate_rfe_discussion_title(
            customer_name, 
            len(active_rfe_cases), 
            len(active_bug_cases)
        )
        
        # Generate 3-table markdown content using customer template
        discussion_body = self.template_renderer.render_portal_content(
            cases, 
            customer_name, 
            template_key
        )
        
        # Add API posting header
        api_header = self._generate_api_header()
        discussion_body = api_header + "\n\n" + discussion_body
        
        print(f"   📄 Generated {len(discussion_body)} characters of content")
        print(f"   📝 Title: {discussion_title}")
        
        # Post to customer portal group
        try:
            result = self.portal_client.create_group_discussion(
                group_id=group_id,
                title=discussion_title,
                body=discussion_body,
                status="published"
            )
            
            if result and result.get('success'):
                print(f"✅ RFE discussion posted successfully for {customer_name}!")
                print(f"   🔗 Discussion ID: {result.get('discussion_id')}")
                print(f"   📍 URL: {result.get('url')}")
                
                # Store posting record
                posting_record = {
                    "customer": customer_name,
                    "customer_key": customer_key,
                    "group_id": group_id,
                    "discussion_id": result.get('discussion_id'),
                    "discussion_url": result.get('url'),
                    "title": discussion_title,
                    "posted_at": datetime.now().isoformat(),
                    "case_counts": {
                        "active_rfe": len(active_rfe_cases),
                        "active_bug": len(active_bug_cases), 
                        "closed": len(closed_cases),
                        "total": len(cases)
                    },
                    "content_length": len(discussion_body),
                    "success": True
                }
                
                return posting_record
            else:
                error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
                print(f"❌ Failed to post RFE discussion for {customer_name}")
                print(f"   Error: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "customer": customer_name,
                    "group_id": group_id
                }
                
        except Exception as e:
            print(f"❌ Error posting RFE discussion for {customer_name}: {e}")
            return None
    
    def _is_closed_status(self, case: Dict) -> bool:
        """Check if a case status indicates it's closed (same as template renderer)"""
        # Check JIRA status first (most reliable)
        jira_refs = case.get('enriched_jira', case.get('jira_refs', []))
        if jira_refs:
            for jira_ref in jira_refs:
                status = jira_ref.get('status', '').lower()
                if status in ['closed', 'done', 'resolved', 'complete', 'delivered']:
                    return True
        
        # Fallback to case status if no JIRA status available
        case_status = case.get('status', '').lower()
        if case_status in ['closed', 'resolved', 'solved', 'done', 'complete']:
            return True
        
        return False
    
    def _generate_api_header(self) -> str:
        """Generate header indicating content was posted via API"""
        return f"""---
**🤖 Automated Update via Red Hat Customer Portal API**
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}*
*Generated by: RFE Discussion API Client*

---"""
    
    def post_to_all_customers(self, customer_cases: Dict[str, List[Dict]]) -> Dict[str, Optional[Dict]]:
        """
        Post RFE discussions to all customer portal groups
        
        Args:
            customer_cases: Dict mapping customer_key to list of cases
            
        Returns:
            Dict mapping customer_key to posting results
        """
        print("🚀 Posting RFE discussions to all customer portal groups...")
        results = {}
        
        for customer_key, cases in customer_cases.items():
            if not cases:
                print(f"⚠️  No cases for {customer_key} - skipping")
                results[customer_key] = None
                continue
                
            result = self.post_rfe_discussion(customer_key, cases)
            results[customer_key] = result
            
            # Add delay between posts to be respectful to API
            if result:
                print("   ⏱️  Waiting 2 seconds before next post...")
                import time
                time.sleep(2)
        
        # Summary
        successful_posts = sum(1 for r in results.values() if r is not None)
        total_customers = len(results)
        
        print(f"📊 POSTING SUMMARY:")
        print(f"   ✅ Successful: {successful_posts}/{total_customers}")
        print(f"   ❌ Failed: {total_customers - successful_posts}/{total_customers}")
        
        return results
    
    def test_full_workflow(self, customer_key: str = "tdbank") -> bool:
        """
        Test the complete RFE discussion posting workflow
        
        Args:
            customer_key: Customer to test with (default: tdbank for sandbox)
            
        Returns:
            True if workflow test successful, False otherwise
        """
        print(f"🧪 TESTING COMPLETE RFE DISCUSSION WORKFLOW: {customer_key.upper()}")
        print("=" * 60)
        
        try:
            # Step 1: Authenticate
            if not self.authenticate():
                print("❌ Authentication failed")
                return False
            
            # Step 2: Discover group IDs
            group_ids = self.discover_customer_group_ids()
            if not group_ids.get(customer_key):
                print(f"❌ No group ID discovered for {customer_key}")
                return False
            
            # Step 3: Validate group access
            if not self.validate_group_access(customer_key):
                print(f"❌ Group access validation failed for {customer_key}")
                return False
            
            # Step 4: Generate test RFE data (using mock data for testing)
            test_cases = self._generate_test_cases()
            
            # Step 5: Post RFE discussion
            result = self.post_rfe_discussion(customer_key, test_cases)
            
            if result:
                print("✅ COMPLETE WORKFLOW TEST SUCCESSFUL!")
                print(f"   🎯 Posted to: {result['customer']} (Group {result['group_id']})")
                print(f"   📊 Cases: {result['case_counts']['total']} total")
                print(f"   🔗 Discussion ID: {result['discussion_id']}")
                return True
            else:
                print("❌ Discussion posting failed")
                return False
                
        except Exception as e:
            print(f"❌ Workflow test failed: {e}")
            return False
    
    def _generate_test_cases(self) -> List[Dict]:
        """Generate test case data for workflow testing"""
        return [
            {
                'caseNumber': '04244831',
                'summary': '[RFE] Test API Integration',
                'status': 'Waiting on Red Hat',
                'rfe_type': 'RFE',
                'enriched_jira': [{
                    'jira_id': 'AAPRFE-TEST',
                    'status': 'In Progress',
                    'summary': '[RFE] API Integration Test Case'
                }]
            },
            {
                'caseNumber': '04244832',
                'summary': '[BUG] Test Bug Case',
                'status': 'Waiting on Red Hat',
                'rfe_type': 'Bug',
                'enriched_jira': [{
                    'jira_id': 'AAP-TEST',
                    'status': 'New',
                    'summary': '[BUG] API Integration Bug Test'
                }]
            },
            {
                'caseNumber': '04244830',
                'summary': '[RFE] Closed Test Case',
                'status': 'Closed',
                'rfe_type': 'RFE',
                'enriched_jira': [{
                    'jira_id': 'AAPRFE-CLOSED',
                    'status': 'Done',
                    'summary': '[RFE] Completed API Test Case'
                }]
            }
        ]


def main():
    """Test the RFE Discussion API Client"""
    print("🧪 TESTING RFE DISCUSSION API CLIENT")
    print("=" * 50)
    
    # Initialize client
    client = RFEDiscussionAPIClient(environment="qa")
    
    # Test complete workflow
    success = client.test_full_workflow("tdbank")
    
    if success:
        print("\n🎉 RFE Discussion API Client is ready for production!")
    else:
        print("\n❌ RFE Discussion API Client needs debugging")


if __name__ == '__main__':
    main()
