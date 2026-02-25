#!/usr/bin/env python3

"""
Enhanced Group ID Discovery Tool
Purpose: Advanced discovery of customer group IDs for JPMC and Fannie Mae
Methods: Account number analysis, pattern matching, and systematic search
"""

import os
import re
import requests
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time

class EnhancedGroupIDDiscovery:
    """Advanced customer group ID discovery with multiple strategies"""
    
    def __init__(self):
        self.customers = {
            'jpmc': {
                'name': 'JP Morgan Chase',
                'account_number': '334224',
                'alternative_names': ['JPMC', 'JP Morgan', 'JPMorgan Chase'],
                'known_patterns': [],
                'discovered_candidates': []
            },
            'fanniemae': {
                'name': 'Fannie Mae',
                'account_number': '1460290',
                'alternative_names': ['FannieMae', 'FNMA', 'Federal National Mortgage Association'],
                'known_patterns': [],
                'discovered_candidates': []
            }
        }
        
        # Reference data from confirmed customers
        self.reference_data = {
            'wellsfargo': {
                'account_number': '838043',
                'group_id': '4357341',
                'name_pattern': 'Wells Fargo'
            },
            'tdbank': {
                'account_number': '1912101', 
                'group_id': '7028358',
                'name_pattern': 'TD Bank'
            }
        }
        
        print("🔍 Enhanced Group ID Discovery Tool Initialized")
        print("   🎯 Target: JPMC and Fannie Mae group IDs")
        print("   📊 Reference: Wells Fargo (4357341), TD Bank (7028358)")
        print("   🔬 Methods: Account analysis, pattern matching, systematic search")
    
    def analyze_account_number_patterns(self) -> Dict[str, List[str]]:
        """Analyze account numbers to find potential group ID patterns"""
        print("\n📊 ACCOUNT NUMBER PATTERN ANALYSIS")
        print("=" * 40)
        
        patterns = {}
        
        for customer_key, customer_info in self.customers.items():
            account_num = customer_info['account_number']
            print(f"\n🏢 {customer_info['name']} (Account: {account_num})")
            
            # Strategy 1: Direct account number variations
            account_variations = [
                account_num,  # Direct match
                f"{account_num}1",  # Account + 1
                f"{account_num}0",  # Account + 0
                f"1{account_num}",  # 1 + Account
                f"0{account_num}",  # 0 + Account
            ]
            
            # Strategy 2: Account number with common prefixes/suffixes
            account_int = int(account_num)
            for offset in [0, 1, 10, 100, 1000, 10000]:
                account_variations.extend([
                    str(account_int + offset),
                    str(account_int - offset)
                ])
            
            # Strategy 3: Account number in different ranges
            # Wells Fargo: 838043 -> 4357341 (different range)
            # TD Bank: 1912101 -> 7028358 (different range)
            # Hypothesis: Group IDs might be in different ranges than account numbers
            
            # Generate IDs in known group ID ranges
            group_id_ranges = [
                (4000000, 4500000),  # Wells Fargo range
                (7000000, 7500000),  # TD Bank range
                (1000000, 2000000),  # Lower range
                (3000000, 4000000),  # Mid range
                (5000000, 6000000),  # Higher range
            ]
            
            for start, end in group_id_ranges:
                # Generate some IDs from each range
                step = (end - start) // 20
                for i in range(10):
                    candidate_id = start + (i * step)
                    account_variations.append(str(candidate_id))
            
            # Remove duplicates and sort
            unique_variations = sorted(list(set(account_variations)))
            patterns[customer_key] = unique_variations[:50]  # Top 50 candidates
            
            print(f"   📋 Generated {len(unique_variations)} potential group IDs")
            print(f"   🎯 Top 5 candidates:")
            for i, candidate in enumerate(unique_variations[:5]):
                print(f"      {i+1}. {candidate}")
        
        return patterns
    
    def search_redhat_portal_patterns(self) -> Dict[str, List[str]]:
        """Search for patterns that might indicate customer group IDs"""
        print("\n🌐 RED HAT PORTAL PATTERN SEARCH")
        print("=" * 35)
        
        # Common Red Hat portal URL patterns
        portal_patterns = [
            "https://access.redhat.com/groups/{group_id}",
            "https://access.redhat.com/groups/{group_id}/discussions",
            "https://access.redhat.com/groups/node/{node_id}/edit"
        ]
        
        # Search strategies based on known patterns
        search_candidates = {}
        
        for customer_key, customer_info in self.customers.items():
            print(f"\n🏢 Searching for {customer_info['name']}...")
            
            candidates = []
            
            # Strategy 1: Account number based searches
            account_num = customer_info['account_number']
            
            # Try account number in different positions
            for position in ['start', 'end', 'middle']:
                if position == 'start':
                    candidates.extend([f"{account_num}000", f"{account_num}001", f"{account_num}100"])
                elif position == 'end':
                    candidates.extend([f"000{account_num}", f"001{account_num}", f"100{account_num}"])
                else:  # middle
                    candidates.extend([f"1{account_num}0", f"0{account_num}1", f"2{account_num}2"])
            
            # Strategy 2: Name-based searches (if we had name hashing)
            # This would require more sophisticated analysis
            
            # Strategy 3: Sequential searches around known IDs
            for ref_key, ref_data in self.reference_data.items():
                ref_group_id = int(ref_data['group_id'])
                
                # Search in ranges around known IDs
                for offset in [-10000, -5000, -1000, -500, -100, 100, 500, 1000, 5000, 10000]:
                    candidate = str(ref_group_id + offset)
                    candidates.append(candidate)
            
            # Remove duplicates
            unique_candidates = list(set(candidates))
            search_candidates[customer_key] = unique_candidates[:30]  # Top 30
            
            print(f"   📋 Generated {len(unique_candidates)} search candidates")
            print(f"   🎯 Sample candidates: {unique_candidates[:5]}")
        
        return search_candidates
    
    def validate_group_id_candidates(self, candidates: Dict[str, List[str]]) -> Dict[str, List[Dict]]:
        """Validate group ID candidates using various methods"""
        print("\n✅ GROUP ID CANDIDATE VALIDATION")
        print("=" * 35)
        
        validated_candidates = {}
        
        for customer_key, candidate_list in candidates.items():
            customer_info = self.customers[customer_key]
            print(f"\n🏢 Validating {customer_info['name']} candidates...")
            
            validated = []
            
            for i, candidate_id in enumerate(candidate_list[:20]):  # Validate top 20
                print(f"   🔍 Testing candidate {i+1}/20: {candidate_id}")
                
                # Validation method 1: URL accessibility test
                test_url = f"https://access.redhat.com/groups/{candidate_id}"
                
                try:
                    # Note: This is a basic test - in production we'd need proper authentication
                    response = requests.head(test_url, timeout=5, allow_redirects=True)
                    
                    validation_result = {
                        'group_id': candidate_id,
                        'url': test_url,
                        'http_status': response.status_code,
                        'accessible': response.status_code in [200, 301, 302, 403],  # 403 might indicate group exists but access denied
                        'response_time': response.elapsed.total_seconds(),
                        'confidence': 'low'
                    }
                    
                    # Adjust confidence based on response
                    if response.status_code == 200:
                        validation_result['confidence'] = 'high'
                    elif response.status_code == 403:
                        validation_result['confidence'] = 'medium'  # Group exists but access denied
                    elif response.status_code in [301, 302]:
                        validation_result['confidence'] = 'medium'  # Redirect might indicate group
                    
                    validated.append(validation_result)
                    
                    if response.status_code == 200:
                        print(f"      ✅ Accessible (Status: {response.status_code})")
                    elif response.status_code == 403:
                        print(f"      🔒 Access denied (Status: {response.status_code}) - Group likely exists")
                    else:
                        print(f"      ❓ Status: {response.status_code}")
                    
                except requests.RequestException as e:
                    print(f"      ❌ Error testing {candidate_id}: {e}")
                    validated.append({
                        'group_id': candidate_id,
                        'url': test_url,
                        'error': str(e),
                        'confidence': 'none'
                    })
                
                # Small delay to be respectful
                time.sleep(0.5)
            
            # Sort by confidence and accessibility
            validated.sort(key=lambda x: (
                {'high': 3, 'medium': 2, 'low': 1, 'none': 0}.get(x.get('confidence', 'none'), 0),
                x.get('accessible', False)
            ), reverse=True)
            
            validated_candidates[customer_key] = validated
            
            # Show top results
            print(f"\n   📊 Top validation results:")
            for i, result in enumerate(validated[:5]):
                confidence = result.get('confidence', 'none')
                accessible = result.get('accessible', False)
                status = "✅" if accessible else "❓"
                print(f"      {i+1}. {status} {result['group_id']} (Confidence: {confidence})")
        
        return validated_candidates
    
    def generate_discovery_report(self, validated_candidates: Dict[str, List[Dict]]) -> Dict:
        """Generate comprehensive discovery report"""
        print("\n📋 GENERATING DISCOVERY REPORT")
        print("=" * 30)
        
        report = {
            'discovery_timestamp': datetime.now().isoformat(),
            'customers': {},
            'summary': {
                'total_candidates_tested': 0,
                'high_confidence_finds': 0,
                'medium_confidence_finds': 0,
                'accessible_groups': 0
            }
        }
        
        for customer_key, candidates in validated_candidates.items():
            customer_info = self.customers[customer_key]
            
            # Count confidence levels
            high_conf = [c for c in candidates if c.get('confidence') == 'high']
            medium_conf = [c for c in candidates if c.get('confidence') == 'medium']
            accessible = [c for c in candidates if c.get('accessible', False)]
            
            report['customers'][customer_key] = {
                'name': customer_info['name'],
                'account_number': customer_info['account_number'],
                'total_candidates_tested': len(candidates),
                'high_confidence_candidates': len(high_conf),
                'medium_confidence_candidates': len(medium_conf),
                'accessible_candidates': len(accessible),
                'top_candidates': candidates[:10],  # Top 10 for each customer
                'recommendations': self._generate_recommendations(customer_key, candidates)
            }
            
            # Update summary
            report['summary']['total_candidates_tested'] += len(candidates)
            report['summary']['high_confidence_finds'] += len(high_conf)
            report['summary']['medium_confidence_finds'] += len(medium_conf)
            report['summary']['accessible_groups'] += len(accessible)
        
        return report
    
    def _generate_recommendations(self, customer_key: str, candidates: List[Dict]) -> List[str]:
        """Generate recommendations for manual verification"""
        recommendations = []
        
        high_conf = [c for c in candidates if c.get('confidence') == 'high']
        medium_conf = [c for c in candidates if c.get('confidence') == 'medium']
        
        if high_conf:
            recommendations.append(f"🎯 HIGH PRIORITY: Test group ID {high_conf[0]['group_id']} manually in Red Hat portal")
            recommendations.append(f"   URL: {high_conf[0]['url']}")
        
        if medium_conf:
            recommendations.append(f"🔍 MEDIUM PRIORITY: Verify {len(medium_conf)} medium-confidence candidates")
            for candidate in medium_conf[:3]:
                recommendations.append(f"   - {candidate['group_id']} (Status: {candidate.get('http_status', 'unknown')})")
        
        if not high_conf and not medium_conf:
            recommendations.append("❌ No high-confidence candidates found")
            recommendations.append("💡 Consider manual portal search using account number")
            recommendations.append("💡 Check with Red Hat support for group ID lookup")
        
        return recommendations
    
    def run_complete_discovery(self) -> Dict:
        """Run the complete discovery process"""
        print("🚀 ENHANCED GROUP ID DISCOVERY")
        print("=" * 35)
        print("Target: JPMC and Fannie Mae group IDs")
        print("Method: Multi-strategy discovery with validation")
        print()
        
        # Step 1: Analyze account number patterns
        account_patterns = self.analyze_account_number_patterns()
        
        # Step 2: Search portal patterns
        portal_patterns = self.search_redhat_portal_patterns()
        
        # Step 3: Combine and validate candidates
        all_candidates = {}
        for customer_key in self.customers.keys():
            # Combine patterns from both methods
            combined = account_patterns.get(customer_key, []) + portal_patterns.get(customer_key, [])
            # Remove duplicates and limit
            all_candidates[customer_key] = list(set(combined))[:30]
        
        # Step 4: Validate candidates
        validated_candidates = self.validate_group_id_candidates(all_candidates)
        
        # Step 5: Generate report
        report = self.generate_discovery_report(validated_candidates)
        
        # Step 6: Save report
        report_file = f"/tmp/group_id_discovery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📁 Discovery report saved to: {report_file}")
        
        # Step 7: Summary
        print(f"\n📊 DISCOVERY SUMMARY")
        print("=" * 20)
        print(f"Total candidates tested: {report['summary']['total_candidates_tested']}")
        print(f"High confidence finds: {report['summary']['high_confidence_finds']}")
        print(f"Medium confidence finds: {report['summary']['medium_confidence_finds']}")
        print(f"Accessible groups found: {report['summary']['accessible_groups']}")
        
        return report

def main():
    """Run enhanced group ID discovery"""
    discovery = EnhancedGroupIDDiscovery()
    report = discovery.run_complete_discovery()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Review the discovery report for high-confidence candidates")
    print("2. Manually test the top candidates in Red Hat portal")
    print("3. Update customer configuration with confirmed group IDs")
    print("4. Re-run RFE automation with new group IDs")

if __name__ == '__main__':
    main()

