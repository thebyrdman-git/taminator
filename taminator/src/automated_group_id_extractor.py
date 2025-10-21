#!/usr/bin/env python3

"""
Automated Customer Group ID Extractor
Purpose: Automatically extract and validate customer group IDs from known sources
Method: URL analysis, pattern matching, and automated validation
"""

import os
import re
import requests
from typing import Dict, List, Optional
import json

class AutomatedGroupIDExtractor:
    """Automatically extract customer group IDs from available data sources"""
    
    def __init__(self):
        self.customers = {
            'wellsfargo': {
                'name': 'Wells Fargo',
                'account_number': '838043',
                'known_urls': [
                    'https://access.redhat.com/groups/4357341/discussions/7047245',
                    'https://access.redhat.com/groups/node/7047245/edit'
                ],
                'confirmed_group_id': '4357341'
            },
            'jpmc': {
                'name': 'JP Morgan Chase', 
                'account_number': '334224',
                'known_urls': [],
                'confirmed_group_id': None
            },
            'tdbank': {
                'name': 'TD Bank',
                'account_number': '1912101',
                'known_urls': [
                    'https://access.redhat.com/groups/7028358/discussions/7073164',  # Sandbox
                    'https://access.redhat.com/groups/node/7073164/edit'
                ],
                'confirmed_group_id': None,  # 7028358 is sandbox, need production
                'sandbox_group_id': '7028358'
            },
            'fanniemae': {
                'name': 'Fannie Mae',
                'account_number': '1460290',
                'known_urls': [],
                'confirmed_group_id': None
            }
        }
        
        self.extracted_group_ids = {}
        
    def extract_group_ids_from_urls(self):
        """Extract group IDs from known URLs using regex patterns"""
        print("🔍 EXTRACTING GROUP IDs FROM KNOWN URLs")
        print("=" * 45)
        
        # Pattern to match Red Hat group URLs
        group_url_pattern = r'https://access\.redhat\.com/groups/(\d+)/'
        node_url_pattern = r'https://access\.redhat\.com/groups/node/(\d+)/'
        
        for customer_key, customer_info in self.customers.items():
            print(f"\\n🏢 {customer_info['name']}:")
            
            if customer_info['confirmed_group_id']:
                print(f"   ✅ Confirmed group ID: {customer_info['confirmed_group_id']}")
                self.extracted_group_ids[customer_key] = customer_info['confirmed_group_id']
                continue
            
            group_ids_found = set()
            
            for url in customer_info['known_urls']:
                print(f"   🔗 Analyzing: {url}")
                
                # Try direct group URL pattern
                group_match = re.search(group_url_pattern, url)
                if group_match:
                    group_id = group_match.group(1)
                    group_ids_found.add(group_id)
                    print(f"      📋 Found group ID: {group_id}")
                
                # Try node URL pattern  
                node_match = re.search(node_url_pattern, url)
                if node_match:
                    node_id = node_match.group(1)
                    print(f"      📋 Found node ID: {node_id} (potential group content)")
            
            if group_ids_found:
                # Use the most common group ID if multiple found
                group_id = list(group_ids_found)[0]
                self.extracted_group_ids[customer_key] = group_id
                print(f"   ✅ Extracted group ID: {group_id}")
            else:
                print(f"   ❌ No group IDs found in URLs")
    
    def use_systematic_group_id_discovery(self):
        """Use systematic approach to discover likely group IDs"""
        print("\\n🎯 SYSTEMATIC GROUP ID DISCOVERY")
        print("=" * 35)
        
        # Wells Fargo confirmed: 4357341
        # TD Bank sandbox: 7028358 (7073164 is content ID)
        # Need to find: JPMC, TD Bank production, Fannie Mae
        
        # Hypothesis: Customer group IDs might follow patterns
        # Let's analyze the Wells Fargo ID: 4357341
        wells_fargo_id = 4357341
        
        print(f"📊 Analysis based on Wells Fargo ID: {wells_fargo_id}")
        
        # Generate potential group IDs for other customers
        potential_ids = {
            'jpmc': self._generate_potential_ids_for_customer('jpmc', wells_fargo_id),
            'tdbank': self._generate_potential_ids_for_customer('tdbank', wells_fargo_id), 
            'fanniemae': self._generate_potential_ids_for_customer('fanniemae', wells_fargo_id)
        }
        
        for customer_key, ids in potential_ids.items():
            customer_name = self.customers[customer_key]['name']
            print(f"\\n🏢 {customer_name} potential group IDs:")
            for i, group_id in enumerate(ids[:5]):  # Show top 5
                print(f"   {i+1}. {group_id}")
        
        return potential_ids
    
    def _generate_potential_ids_for_customer(self, customer_key: str, base_id: int) -> List[str]:
        """Generate potential group IDs based on patterns"""
        potential_ids = []
        
        # Pattern 1: Sequential IDs around base ID
        for offset in [-1000, -500, -100, -50, -10, 10, 50, 100, 500, 1000]:
            potential_ids.append(str(base_id + offset))
        
        # Pattern 2: Account number based IDs (if there's a correlation)
        account_num = self.customers[customer_key]['account_number']
        if account_num:
            # Try account number directly
            potential_ids.append(account_num)
            # Try account number + common offsets
            account_int = int(account_num)
            for offset in [0, 1, 10, 100, 1000]:
                potential_ids.append(str(account_int + offset))
        
        # Pattern 3: Common group ID ranges (observed from Red Hat portal)
        common_ranges = [
            (4000000, 4500000),  # Range around Wells Fargo
            (7000000, 7500000),  # Range around TD Bank sandbox
            (1000000, 2000000),  # Lower range
            (3000000, 4000000),  # Mid range
        ]
        
        # Add some IDs from each range
        for start, end in common_ranges:
            step = (end - start) // 10
            for i in range(5):
                potential_ids.append(str(start + i * step))
        
        return list(set(potential_ids))  # Remove duplicates
    
    def create_group_id_configuration(self):
        """Create configuration file with discovered group IDs"""
        print("\\n💾 CREATING GROUP ID CONFIGURATION")
        print("=" * 35)
        
        config = {
            'customer_group_ids': {},
            'discovery_method': 'automated_extraction',
            'confidence_levels': {}
        }
        
        for customer_key, customer_info in self.customers.items():
            if customer_key in self.extracted_group_ids:
                group_id = self.extracted_group_ids[customer_key]
                confidence = 'confirmed' if customer_info.get('confirmed_group_id') else 'extracted'
                
                config['customer_group_ids'][customer_key] = {
                    'name': customer_info['name'],
                    'group_id': group_id,
                    'account_number': customer_info['account_number'],
                    'confidence': confidence
                }
                
                print(f"   ✅ {customer_info['name']}: {group_id} ({confidence})")
            else:
                print(f"   ❌ {customer_info['name']}: No group ID found")
        
        # Save configuration
        config_file = '/tmp/customer_group_ids_config.json'
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\\n📁 Configuration saved to: {config_file}")
        return config
    
    def update_automation_systems(self, config: Dict):
        """Generate updated configuration for automation systems"""
        print("\\n🔧 UPDATING AUTOMATION SYSTEM CONFIGURATIONS")  
        print("=" * 45)
        
        # Generate Python configuration for API clients
        python_config = '''# Customer Group IDs for API-based Portal Posting
# Auto-generated from Automated Group ID Extraction

CUSTOMER_GROUP_IDS = {
'''
        
        for customer_key, customer_data in config['customer_group_ids'].items():
            python_config += f'    "{customer_key}": "{customer_data["group_id"]}",  # {customer_data["name"]} ({customer_data["confidence"]})\\n'
        
        python_config += '''}

# Confidence levels for validation
CUSTOMER_CONFIDENCE = {
'''
        
        for customer_key, customer_data in config['customer_group_ids'].items():
            python_config += f'    "{customer_key}": "{customer_data["confidence"]}",\\n'
        
        python_config += '''}

def get_group_id(customer_key: str) -> str:
    """Get group ID for customer with validation"""
    if customer_key not in CUSTOMER_GROUP_IDS:
        raise ValueError(f"Unknown customer: {customer_key}")
    
    group_id = CUSTOMER_GROUP_IDS[customer_key]
    confidence = CUSTOMER_CONFIDENCE[customer_key]
    
    if confidence != "confirmed":
        print(f"⚠️  Warning: Group ID {group_id} for {customer_key} is {confidence}, not confirmed")
    
    return group_id
'''
        
        # Save Python config
        python_file = '/tmp/customer_group_ids.py'
        with open(python_file, 'w') as f:
            f.write(python_config)
        
        print(f"📁 Python configuration: {python_file}")
        
        # Generate YAML configuration for weekly troubleshooting system
        yaml_config = '''# Customer Group IDs for Weekly Troubleshooting Reports
# Auto-generated from Automated Group ID Extraction

customers:
'''
        
        for customer_key, customer_data in config['customer_group_ids'].items():
            yaml_config += f'''  {customer_key}:
    name: "{customer_data["name"]}"
    group_id: "{customer_data["group_id"]}"
    account_number: "{customer_data["account_number"]}"
    confidence: "{customer_data["confidence"]}"
    
'''
        
        yaml_file = '/tmp/customer_group_ids.yaml'
        with open(yaml_file, 'w') as f:
            f.write(yaml_config)
        
        print(f"📁 YAML configuration: {yaml_file}")
        
        return {
            'python_config': python_file,
            'yaml_config': yaml_file
        }

    def run_automated_discovery(self):
        """Run the complete automated discovery process"""
        print("🚀 AUTOMATED CUSTOMER GROUP ID DISCOVERY")
        print("=" * 45)
        print("Purpose: Find real customer group IDs for API-based posting")
        print("Method: URL analysis and systematic pattern discovery")
        print()
        
        # Step 1: Extract from known URLs
        self.extract_group_ids_from_urls()
        
        # Step 2: Systematic discovery for missing IDs
        potential_ids = self.use_systematic_group_id_discovery()
        
        # Step 3: Create configuration
        config = self.create_group_id_configuration()
        
        # Step 4: Update automation systems
        files = self.update_automation_systems(config)
        
        # Step 5: Summary report
        print("\\n📊 DISCOVERY SUMMARY")
        print("=" * 20)
        
        confirmed_count = sum(1 for data in config['customer_group_ids'].values() if data['confidence'] == 'confirmed')
        extracted_count = sum(1 for data in config['customer_group_ids'].values() if data['confidence'] == 'extracted')
        missing_count = len(self.customers) - len(config['customer_group_ids'])
        
        print(f"✅ Confirmed group IDs: {confirmed_count}")
        print(f"🔍 Extracted group IDs: {extracted_count}")
        print(f"❌ Missing group IDs: {missing_count}")
        
        if missing_count > 0:
            print("\\n💡 NEXT STEPS FOR MISSING GROUP IDs:")
            for customer_key, customer_info in self.customers.items():
                if customer_key not in self.extracted_group_ids:
                    print(f"   🏢 {customer_info['name']}: Manual discovery needed")
                    print(f"      - Search Red Hat portal for customer-specific groups")
                    print(f"      - Look for URLs containing account #{customer_info['account_number']}")
        
        return config

def main():
    """Run automated group ID discovery"""
    extractor = AutomatedGroupIDExtractor()
    config = extractor.run_automated_discovery()
    
    print("\\n🎯 Ready to integrate discovered group IDs into automation systems!")

if __name__ == '__main__':
    main()
