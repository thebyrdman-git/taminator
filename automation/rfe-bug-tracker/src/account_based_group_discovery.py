#!/usr/bin/env python3

"""
Account-Based Group ID Discovery
Purpose: Find customer group IDs using known account numbers
Method: Account number analysis and systematic group ID generation
"""

import json
import requests
import time
from typing import Dict, List, Optional
from datetime import datetime

class AccountBasedGroupDiscovery:
    """Discover group IDs using account numbers and systematic search"""
    
    def __init__(self):
        # Customer data with account numbers
        self.customers = {
            'jpmc': {
                'name': 'JP Morgan Chase',
                'account_number': '334224',  # You know this
                'alternative_names': ['JPMC', 'JP Morgan', 'JPMorgan Chase']
            },
            'fanniemae': {
                'name': 'Fannie Mae', 
                'account_number': '1460290',  # You know this
                'alternative_names': ['FannieMae', 'FNMA', 'Federal National Mortgage Association']
            }
        }
        
        # Reference data for pattern analysis
        self.reference_customers = {
            'wellsfargo': {
                'account_number': '838043',
                'group_id': '4357341'
            },
            'tdbank': {
                'account_number': '1912101',
                'group_id': '7028358'
            }
        }
        
        print("🎯 Account-Based Group ID Discovery")
        print("   📊 Using known account numbers for targeted search")
        print("   🔍 JPMC: Account 334224")
        print("   🔍 Fannie Mae: Account 1460290")
    
    def generate_group_id_candidates(self, account_number: str) -> List[str]:
        """Generate potential group IDs based on account number"""
        candidates = []
        account_int = int(account_number)
        
        print(f"\n📋 Generating candidates for account {account_number}...")
        
        # Strategy 1: Direct account number variations
        direct_variations = [
            account_number,  # Direct match
            f"{account_number}1",  # Account + 1
            f"{account_number}0",  # Account + 0
            f"1{account_number}",  # 1 + Account
            f"0{account_number}",  # 0 + Account
            f"{account_number}00",  # Account + 00
            f"00{account_number}",  # 00 + Account
        ]
        candidates.extend(direct_variations)
        
        # Strategy 2: Account number with offsets
        for offset in [1, 10, 100, 1000, 10000, 100000]:
            candidates.extend([
                str(account_int + offset),
                str(account_int - offset)
            ])
        
        # Strategy 3: Account number in different ranges
        # Based on Wells Fargo (838043 -> 4357341) and TD Bank (1912101 -> 7028358)
        # Group IDs seem to be in different ranges than account numbers
        
        # Generate IDs in known group ID ranges
        group_id_ranges = [
            (4000000, 4500000),  # Wells Fargo range
            (7000000, 7500000),  # TD Bank range  
            (1000000, 2000000),  # Lower range
            (3000000, 4000000),  # Mid range
            (5000000, 6000000),  # Higher range
            (6000000, 7000000),  # Between TD Bank and Wells Fargo
        ]
        
        for start, end in group_id_ranges:
            # Generate systematic IDs from each range
            step = (end - start) // 50  # 50 candidates per range
            for i in range(50):
                candidate_id = start + (i * step)
                candidates.append(str(candidate_id))
        
        # Strategy 4: Account number with common prefixes/suffixes
        common_prefixes = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        common_suffixes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        for prefix in common_prefixes:
            candidates.append(f"{prefix}{account_number}")
        
        for suffix in common_suffixes:
            candidates.append(f"{account_number}{suffix}")
        
        # Remove duplicates and sort
        unique_candidates = sorted(list(set(candidates)))
        
        print(f"   ✅ Generated {len(unique_candidates)} unique candidates")
        print(f"   🎯 Sample candidates: {unique_candidates[:10]}")
        
        return unique_candidates
    
    def test_group_id_accessibility(self, group_id: str) -> Dict:
        """Test if a group ID is accessible/valid"""
        test_url = f"https://access.redhat.com/groups/{group_id}"
        
        try:
            response = requests.head(test_url, timeout=10, allow_redirects=True)
            
            result = {
                'group_id': group_id,
                'url': test_url,
                'http_status': response.status_code,
                'accessible': response.status_code in [200, 301, 302, 403],
                'response_time': response.elapsed.total_seconds(),
                'confidence': 'none'
            }
            
            # Determine confidence level
            if response.status_code == 200:
                result['confidence'] = 'high'  # Group exists and is accessible
            elif response.status_code == 403:
                result['confidence'] = 'medium'  # Group exists but access denied
            elif response.status_code in [301, 302]:
                result['confidence'] = 'medium'  # Redirect might indicate group
            elif response.status_code == 404:
                result['confidence'] = 'none'  # Group doesn't exist
            
            return result
            
        except requests.RequestException as e:
            return {
                'group_id': group_id,
                'url': test_url,
                'error': str(e),
                'confidence': 'none'
            }
    
    def discover_customer_group_id(self, customer_key: str) -> Dict:
        """Discover group ID for a specific customer"""
        customer_info = self.customers[customer_key]
        account_number = customer_info['account_number']
        
        print(f"\n🔍 DISCOVERING GROUP ID FOR {customer_info['name'].upper()}")
        print("=" * 50)
        print(f"Account Number: {account_number}")
        
        # Generate candidates
        candidates = self.generate_group_id_candidates(account_number)
        
        # Test top candidates (limit to avoid too many requests)
        test_limit = 100
        print(f"\n🧪 Testing top {test_limit} candidates...")
        
        results = []
        for i, candidate in enumerate(candidates[:test_limit]):
            if i % 10 == 0:
                print(f"   Testing candidate {i+1}/{test_limit}: {candidate}")
            
            result = self.test_group_id_accessibility(candidate)
            results.append(result)
            
            # Small delay to be respectful
            time.sleep(0.2)
        
        # Sort results by confidence
        results.sort(key=lambda x: {
            'high': 3, 'medium': 2, 'low': 1, 'none': 0
        }.get(x.get('confidence', 'none'), 0), reverse=True)
        
        # Show top results
        print(f"\n📊 TOP RESULTS FOR {customer_info['name']}:")
        print("-" * 40)
        
        high_confidence = [r for r in results if r.get('confidence') == 'high']
        medium_confidence = [r for r in results if r.get('confidence') == 'medium']
        
        if high_confidence:
            print("🎯 HIGH CONFIDENCE CANDIDATES:")
            for i, result in enumerate(high_confidence[:5]):
                print(f"   {i+1}. Group ID: {result['group_id']}")
                print(f"      URL: {result['url']}")
                print(f"      Status: {result['http_status']}")
                print()
        
        if medium_confidence:
            print("🔍 MEDIUM CONFIDENCE CANDIDATES:")
            for i, result in enumerate(medium_confidence[:5]):
                print(f"   {i+1}. Group ID: {result['group_id']}")
                print(f"      URL: {result['url']}")
                print(f"      Status: {result['http_status']}")
                print()
        
        if not high_confidence and not medium_confidence:
            print("❌ No high or medium confidence candidates found")
            print("💡 Consider manual portal search or contact Red Hat support")
        
        return {
            'customer': customer_info['name'],
            'account_number': account_number,
            'total_candidates_tested': len(results),
            'high_confidence_candidates': high_confidence,
            'medium_confidence_candidates': medium_confidence,
            'all_results': results
        }
    
    def run_discovery_for_all_customers(self) -> Dict:
        """Run discovery for all customers"""
        print("🚀 ACCOUNT-BASED GROUP ID DISCOVERY")
        print("=" * 40)
        
        all_results = {}
        
        for customer_key in self.customers.keys():
            result = self.discover_customer_group_id(customer_key)
            all_results[customer_key] = result
        
        # Generate summary report
        report = {
            'discovery_timestamp': datetime.now().isoformat(),
            'customers': all_results,
            'summary': {
                'total_customers': len(all_results),
                'customers_with_high_confidence': 0,
                'customers_with_medium_confidence': 0,
                'total_candidates_tested': 0
            }
        }
        
        # Calculate summary statistics
        for customer_key, result in all_results.items():
            report['summary']['total_candidates_tested'] += result['total_candidates_tested']
            
            if result['high_confidence_candidates']:
                report['summary']['customers_with_high_confidence'] += 1
            elif result['medium_confidence_candidates']:
                report['summary']['customers_with_medium_confidence'] += 1
        
        # Save report
        report_file = f"/tmp/account_based_discovery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📁 Discovery report saved to: {report_file}")
        
        # Print final summary
        print(f"\n📊 FINAL SUMMARY")
        print("=" * 15)
        print(f"Total customers tested: {report['summary']['total_customers']}")
        print(f"High confidence finds: {report['summary']['customers_with_high_confidence']}")
        print(f"Medium confidence finds: {report['summary']['customers_with_medium_confidence']}")
        print(f"Total candidates tested: {report['summary']['total_candidates_tested']}")
        
        return report

def main():
    """Run account-based group ID discovery"""
    discovery = AccountBasedGroupDiscovery()
    report = discovery.run_discovery_for_all_customers()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Review high-confidence candidates in the report")
    print("2. Manually test the top candidates in Red Hat portal")
    print("3. Update customer configuration with confirmed group IDs")
    print("4. Re-run RFE automation with new group IDs")

if __name__ == '__main__':
    main()

