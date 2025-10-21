#!/usr/bin/env python3

"""
Weekly Discussion Poster - Automated troubleshooting case reports via Red Hat CPPG API
Purpose: Create new discussion posts weekly with current troubleshooting cases
Schedule: Wednesdays at 9am EST
Features: Date-stamped titles, no email notifications, zero browser automation
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from active_case_report_system import ActiveCaseReportSystem
from redhat_cppg_api_client import RedHatCPPGAPIClient

class WeeklyDiscussionPoster:
    """Automated weekly troubleshooting case discussion poster"""
    
    def __init__(self):
        """Initialize the weekly discussion poster"""
        self.case_system = ActiveCaseReportSystem()
        
        # Customer group configuration (auto-discovered)
        self.customer_groups = {
            "wellsfargo": {
                "name": "Wells Fargo",
                "group_id": "4357341",  # Confirmed - Wells Fargo Active Cases
                "account_name": "wellsfargo"
            },
            "tdbank": {
                "name": "TD Bank", 
                "group_id": "7028358",  # Extracted - Sandbox/Testing
                "account_name": "tdbank"
            },
            "jpmc": {
                "name": "JPMC",
                "group_id": None,  # Manual discovery needed - account #334224
                "account_name": "jpmc"
            },
            "fanniemae": {
                "name": "Fannie Mae",
                "group_id": None,  # Manual discovery needed - account #1460290  
                "account_name": "fanniemae"
            }
        }
        
        # API configuration
        self.api_servers = {
            "qa": "https://access.qa.redhat.com",
            "stage": "https://access.stage.redhat.com", 
            "production": "https://access.redhat.com"
        }
        
        print("📅 Weekly Discussion Poster Initialized")
        print("   🕘 Schedule: Wednesdays at 9am EST")
        print("   🎯 Target: Wells Fargo troubleshooting cases")
        print("   🔕 Email notifications: Disabled")
        print("   🌐 Method: Red Hat CPPG API")
    
    def generate_discussion_title(self, customer_name: str, case_count: int) -> str:
        """Generate date-stamped discussion title"""
        today = datetime.now()
        formatted_date = today.strftime("%B %d, %Y")  # "October 2, 2025"
        
        title = f"Weekly Troubleshooting Case Report - {formatted_date}"
        
        # Add case count for quick reference
        if case_count > 0:
            title += f" ({case_count} Active Cases)"
        else:
            title += " (No Active Cases)"
        
        print(f"   📝 Generated title: {title}")
        return title
    
    def enhance_content_for_discussion(self, content: str, customer_name: str, case_count: int) -> str:
        """Enhance the troubleshooting case content for discussion post format"""
        today = datetime.now()
        formatted_date = today.strftime("%B %d, %Y")
        week_of_year = today.strftime("Week %U of %Y")
        
        # Create enhanced header
        enhanced_content = f"""# Weekly Troubleshooting Case Report
**Customer**: {customer_name}  
**Report Date**: {formatted_date}  
**Period**: {week_of_year}  
**Active Troubleshooting Cases**: {case_count}

---

## Executive Summary
This weekly report focuses on active troubleshooting cases that require technical assistance but haven't been escalated to formal RFE or Bug submissions. These cases represent customers needing help resolving technical issues.

**Key Metrics This Week:**
- 🔍 **Active Cases**: {case_count} troubleshooting cases requiring attention
- ❌ **Excluded**: RFE and Bug cases (tracked in separate dedicated systems)
- 🎯 **Focus**: Customer issues needing support team intervention

---

{content}

---

## Weekly Summary
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}
- **Next Report**: {(today + timedelta(days=7)).strftime('%B %d, %Y')} (Next Wednesday)
- **Automation**: pai-troubleshooting-report system
- **Questions**: Contact jbyrd@redhat.com

*This report is automatically generated weekly and posted to keep all stakeholders informed of active troubleshooting needs.*
"""
        return enhanced_content
    
    def create_weekly_discussion(self, customer_key: str = "wellsfargo", months: int = 6) -> Dict[str, Any]:
        """Create a new weekly discussion post with troubleshooting cases"""
        print(f"📅 CREATING WEEKLY DISCUSSION POST: {customer_key.upper()}")
        print("=" * 60)
        
        try:
            # Step 1: Generate troubleshooting case report
            print("📋 Step 1: Generating troubleshooting case report...")
            report_result = self.case_system.generate_report_for_customer(customer_key, months)
            
            if not report_result.get("success"):
                return {
                    "success": False,
                    "error": f"Report generation failed: {report_result.get('error')}",
                    "step": "report_generation"
                }
            
            case_count = report_result["troubleshooting_cases"]
            customer_name = report_result["customer"]
            base_content = report_result["content"]
            
            print(f"   ✅ Report generated: {case_count} troubleshooting cases")
            
            # Step 2: Generate discussion title with date
            print("📝 Step 2: Generating discussion title...")
            title = self.generate_discussion_title(customer_name, case_count)
            
            # Step 3: Enhance content for discussion format
            print("🎨 Step 3: Enhancing content for discussion post...")
            enhanced_content = self.enhance_content_for_discussion(base_content, customer_name, case_count)
            
            # Step 4: Initialize CPPG API client
            print("🔐 Step 4: Initializing Red Hat CPPG API client...")
            
            # Try QA first (production requires VPN), fallback to production if available
            api_client = None
            for env in ["qa", "production"]:
                try:
                    api_client = RedHatCPPGAPIClient(environment=env)
                    
                    print(f"   🌐 Trying {env.upper()} environment: {api_client.base_url}")
                    
                    # Test authentication
                    if api_client.authenticate():
                        print(f"   ✅ Successfully connected to {env.upper()} environment")
                        break
                    else:
                        print(f"   ❌ Authentication failed for {env.upper()}")
                        api_client = None
                except Exception as e:
                    print(f"   ❌ {env.upper()} connection failed: {e}")
                    api_client = None
            
            if not api_client:
                return {
                    "success": False,
                    "error": "Could not connect to any CPPG API environment",
                    "step": "api_connection"
                }
            
            # Step 5: Create discussion post
            print("🚀 Step 5: Creating discussion post via API...")
            customer_config = self.customer_groups[customer_key]
            group_id = customer_config["group_id"]
            
            print(f"   🎯 Target group: {group_id} ({customer_name})")
            print(f"   📝 Title: {title}")
            print(f"   📄 Content length: {len(enhanced_content)} characters")
            
            # Create the discussion
            discussion_result = api_client.create_discussion(
                group_id=group_id,
                title=title,
                body=enhanced_content
            )
            
            if discussion_result.get("success"):
                print("🎉 WEEKLY DISCUSSION POST CREATED SUCCESSFULLY!")
                return {
                    "success": True,
                    "customer": customer_name,
                    "troubleshooting_cases": case_count,
                    "discussion_title": title,
                    "discussion_id": discussion_result.get("discussion_id"),
                    "group_id": group_id,
                    "content_length": len(enhanced_content),
                    "api_environment": api_client.server_url,
                    "created_at": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Discussion creation failed: {discussion_result.get('error')}",
                    "step": "discussion_creation"
                }
                
        except Exception as e:
            print(f"❌ Weekly discussion creation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "step": "general_error"
            }
    
    def test_weekly_creation(self, customer_key: str = "wellsfargo") -> Dict[str, Any]:
        """Test the weekly discussion creation process"""
        print("🧪 TESTING WEEKLY DISCUSSION CREATION")
        print("=" * 50)
        
        result = self.create_weekly_discussion(customer_key)
        
        if result.get("success"):
            print(f"✅ SUCCESS: Weekly discussion created!")
            print(f"   🏢 Customer: {result['customer']}")
            print(f"   🔍 Cases: {result['troubleshooting_cases']}")
            print(f"   📝 Title: {result['discussion_title']}")
            print(f"   🆔 Discussion ID: {result.get('discussion_id', 'N/A')}")
            print(f"   🌐 Environment: {result.get('api_environment', 'Unknown')}")
            return result
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            print(f"   🔍 Failed at step: {result.get('step', 'unknown')}")
            return result


def main():
    """Demo the weekly discussion poster"""
    print("🧪 TESTING WEEKLY DISCUSSION POSTER")
    print("=" * 50)
    
    # Ensure environment variables are set
    if not os.getenv('REDHAT_USERNAME') or not os.getenv('REDHAT_PASSWORD'):
        print("❌ ERROR: REDHAT_USERNAME and REDHAT_PASSWORD environment variables required")
        sys.exit(1)
    
    poster = WeeklyDiscussionPoster()
    
    # Test the weekly creation process
    result = poster.test_weekly_creation("wellsfargo")
    
    if result.get("success"):
        print(f"\n🎉 WEEKLY AUTOMATION READY!")
        print(f"   📅 Schedule this to run Wednesdays at 9am EST")
        print(f"   💼 Command: python3 weekly_discussion_poster.py")
        print(f"   🔄 Cron: 0 9 * * 3 /path/to/weekly_discussion_poster.py")
    else:
        print(f"\n❌ Weekly automation not ready - fix issues above")
        sys.exit(1)


if __name__ == '__main__':
    main()
