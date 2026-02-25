#!/usr/bin/env python3

"""
TAM Call Notes Poster - Automated discussion posts for TAM call notes
Purpose: Post formatted TAM call notes as new discussion posts
Features: Flexible formatting, automatic case/JIRA linking, no email notifications
"""

import os
import sys
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from redhat_cppg_api_client import RedHatCPPGAPIClient

class TAMCallNotesPoster:
    """Automated TAM call notes discussion poster"""
    
    def __init__(self):
        """Initialize the TAM call notes poster"""
        
        # Customer group configuration (auto-discovered)
        self.customer_groups = {
            "wellsfargo": {
                "name": "Wells Fargo",
                "group_id": "4357341",  # Confirmed - Wells Fargo Active Cases
                "account_name": "wellsfargo"
            },
            "jpmc": {
                "name": "JP Morgan Chase",
                "group_id": None,  # Manual discovery needed - account #334224
                "account_name": "jpmc"
            },
            "tdbank": {
                "name": "TD Bank",
                "group_id": "7028358",  # Extracted - Sandbox/Testing
                "account_name": "tdbank"
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
        
        print("📞 TAM Call Notes Poster Initialized")
        print("   🎯 Post-call discussion automation")
        print("   📝 Flexible note formatting")
        print("   🔕 No email notifications")
        print("   🌐 Red Hat CPPG API integration")
    
    def generate_call_title(self, customer_name: str, call_type: str = "Weekly TAM Call") -> str:
        """Generate date/time stamped call title"""
        today = datetime.now()
        formatted_date = today.strftime("%B %d, %Y")  # "October 2, 2025"
        
        title = f"{call_type} Notes - {customer_name} - {formatted_date}"
        
        print(f"   📝 Generated title: {title}")
        return title
    
    def auto_link_cases_and_jira(self, content: str) -> str:
        """Automatically convert case numbers and JIRA IDs to clickable links"""
        print("🔗 Adding automatic links to cases and JIRA tickets...")
        
        # Link Red Hat support cases (format: 04123456)
        case_pattern = r'\b(04\d{6})\b'
        content = re.sub(
            case_pattern,
            r'[\1](https://access.redhat.com/support/cases/#/case/\1)',
            content
        )
        
        # Link JIRA tickets (AAP-, AAPRFE-, ANSTRAT-)
        jira_pattern = r'\b((?:AAP|AAPRFE|ANSTRAT)-\d+)\b'
        content = re.sub(
            jira_pattern, 
            r'[\1](https://issues.redhat.com/browse/\1)',
            content
        )
        
        print("   ✅ Auto-linking completed")
        return content
    
    def format_structured_notes(self, raw_notes: str, call_metadata: Dict = None) -> str:
        """Format raw notes into structured discussion post format"""
        print("🎨 Formatting notes into structured discussion format...")
        
        if call_metadata is None:
            call_metadata = {}
        
        today = datetime.now()
        formatted_date = today.strftime("%B %d, %Y at %I:%M %p EST")
        
        # Extract metadata
        customer_name = call_metadata.get('customer', 'Customer')
        attendees = call_metadata.get('attendees', [])
        duration = call_metadata.get('duration', 'N/A')
        call_type = call_metadata.get('type', 'Weekly TAM Call')
        
        # Start building formatted content
        formatted_content = f"""# {call_type} Notes
**Customer**: {customer_name}  
**Date**: {formatted_date}  
**Duration**: {duration}  
"""
        
        # Add attendees if provided
        if attendees:
            formatted_content += f"**Attendees**: {', '.join(attendees)}\n"
        
        formatted_content += "\n---\n\n"
        
        # Process the raw notes
        enhanced_notes = self.auto_link_cases_and_jira(raw_notes)
        
        # Add the notes content
        formatted_content += enhanced_notes
        
        # Add standard footer
        formatted_content += f"""

---

## Call Summary
- **Call Type**: {call_type}
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}
- **TAM**: Jimmy Byrd (jbyrd@redhat.com)
- **Next Call**: TBD

## Quick References
- 📋 [Active Troubleshooting Cases](https://access.redhat.com/groups/4357341/discussions/7047245)
- 🔧 [RFE/Bug Tracker](https://access.redhat.com/groups/7028358/discussions/)
- 📞 [Schedule TAM Call](mailto:jbyrd@redhat.com)

*These notes are automatically posted for stakeholder visibility and follow-up tracking.*
"""
        
        return formatted_content
    
    def create_call_discussion(self, customer_key: str, notes_content: str, 
                             call_metadata: Dict = None) -> Dict[str, Any]:
        """Create a new discussion post with TAM call notes"""
        print(f"📞 CREATING TAM CALL DISCUSSION POST: {customer_key.upper()}")
        print("=" * 60)
        
        try:
            if customer_key not in self.customer_groups:
                return {
                    "success": False,
                    "error": f"Unknown customer key: {customer_key}",
                    "step": "customer_validation"
                }
            
            customer_config = self.customer_groups[customer_key]
            customer_name = customer_config["name"]
            
            # Step 1: Generate discussion title
            print("📝 Step 1: Generating discussion title...")
            call_type = call_metadata.get('type', 'Weekly TAM Call') if call_metadata else 'Weekly TAM Call'
            title = self.generate_call_title(customer_name, call_type)
            
            # Step 2: Format the notes content
            print("🎨 Step 2: Formatting call notes...")
            formatted_content = self.format_structured_notes(notes_content, call_metadata)
            
            # Step 3: Initialize CPPG API client
            print("🔐 Step 3: Initializing Red Hat CPPG API client...")
            
            api_client = None
            for env in ["qa", "production"]:
                try:
                    api_client = RedHatCPPGAPIClient(environment=env)
                    
                    print(f"   🌐 Trying {env.upper()} environment: {api_client.base_url}")
                    
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
            
            # Step 4: Create discussion post
            print("🚀 Step 4: Creating call notes discussion post...")
            group_id = customer_config["group_id"]
            
            print(f"   🎯 Target group: {group_id} ({customer_name})")
            print(f"   📝 Title: {title}")
            print(f"   📄 Content length: {len(formatted_content)} characters")
            
            # Create the discussion
            discussion_result = api_client.create_discussion(
                group_id=group_id,
                title=title,
                body=formatted_content
            )
            
            if discussion_result.get("success"):
                print("🎉 TAM CALL NOTES POSTED SUCCESSFULLY!")
                return {
                    "success": True,
                    "customer": customer_name,
                    "discussion_title": title,
                    "discussion_id": discussion_result.get("discussion_id"),
                    "group_id": group_id,
                    "content_length": len(formatted_content),
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
            print(f"❌ TAM call notes posting failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "step": "general_error"
            }
    
    def post_notes_from_file(self, customer_key: str, notes_file: str, 
                           call_metadata: Dict = None) -> Dict[str, Any]:
        """Post TAM call notes from a file"""
        print(f"📁 Reading call notes from file: {notes_file}")
        
        try:
            with open(notes_file, 'r') as f:
                notes_content = f.read()
            
            print(f"   ✅ Read {len(notes_content)} characters from {notes_file}")
            
            return self.create_call_discussion(customer_key, notes_content, call_metadata)
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"Notes file not found: {notes_file}",
                "step": "file_reading"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading notes file: {e}",
                "step": "file_reading"
            }
    
    def create_example_notes_template(self, customer_key: str) -> str:
        """Create an example notes template for the specified customer"""
        customer_name = self.customer_groups.get(customer_key, {}).get('name', 'Customer')
        
        template = f"""## {customer_name} TAM Call Notes - [Date]

### Call Details
- **Duration**: 60 minutes
- **Attendees**: Jimmy Byrd (Red Hat TAM), [Customer attendees]

### Agenda Items
1. Review current support cases
2. Discuss recent issues and resolutions
3. Upcoming projects and planning
4. Q&A and open discussion

### Discussion Points

#### Active Cases Review
- Case 04123456: Brief description and status
- Case 04234567: Brief description and status

#### Recent Issues & Resolutions
- Issue 1: Description and resolution
- Issue 2: Description and resolution

#### Upcoming Projects
- Project A: Timeline and requirements
- Project B: Planning and resources needed

### Action Items
- [ ] Action item 1 - Owner: [Name] - Due: [Date]
- [ ] Action item 2 - Owner: [Name] - Due: [Date]
- [ ] Follow up on case 04123456 - Owner: Jimmy Byrd - Due: Next week

### Questions & Answers
- Q: Customer question here?
- A: TAM response and guidance

### Next Steps
1. Schedule follow-up for [specific topic]
2. Review progress on action items
3. Continue monitoring active cases

### Next Call
- **Scheduled**: [Date and time]
- **Focus**: [Primary topics for next call]

---

*Template for {customer_name} TAM call notes*
*Customize sections as needed for your specific call format*
"""
        return template


def main():
    """Demo the TAM call notes poster with formatting options"""
    print("🧪 TAM CALL NOTES POSTER - FORMATTING DEMO")
    print("=" * 50)
    
    poster = TAMCallNotesPoster()
    
    # Show formatting options
    print("📝 AVAILABLE FORMATTING OPTIONS:")
    print("   1. Structured notes with sections (agenda, action items, etc.)")
    print("   2. Automatic case number linking (04123456 → clickable)")
    print("   3. Automatic JIRA ticket linking (AAP-12345 → clickable)")
    print("   4. Call metadata (attendees, duration, type)")
    print("   5. Professional headers and footers")
    print("   6. Quick reference links")
    print("")
    
    # Generate example template
    print("📋 EXAMPLE NOTES TEMPLATE:")
    print("=" * 30)
    template = poster.create_example_notes_template("wellsfargo")
    print(template[:500] + "...")
    print("=" * 30)
    
    print("\n💡 USAGE OPTIONS:")
    print("   Option 1: pai-tam-call-notes [customer] [notes-file.md]")
    print("   Option 2: pai-tam-call-notes [customer] --template > notes.md")
    print("   Option 3: pai-tam-call-notes [customer] --interactive")
    print("")
    print("🎯 READY TO DISCUSS SPECIFIC FORMATTING PREFERENCES!")


if __name__ == '__main__':
    main()
