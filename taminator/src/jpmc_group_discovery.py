#!/usr/bin/env python3

"""
JPMC Group ID Discovery Tool
Purpose: Find JPMC group ID using account number 334224
Method: Targeted search with account number analysis
"""

import json
import requests
import time
from typing import Dict, List
from datetime import datetime

class JPMCGroupDiscovery:
    """Discover JPMC group ID using account number 334224"""
    
    def __init__(self):
        self.customer = {
            'name': 'JP Morgan Chase',
            'account_number': '334224',
            'alternative_names': ['JPMC', 'JP Morgan', 'JPMorgan Chase']
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
        
        print("🏦 JPMC Group ID Discovery")
        print(f"   Account Number: {self.customer['account_number']}")
        print("   Target: Find JPMC customer portal group ID")
    
    def generate_jpmc_candidates(self) -> List[str]:
        """Generate potential group IDs for JPMC account 334224"""
        candidates = []
        account_num = self.customer['account_number']
        account_int = int(account_num)
        
        print(f"\n📋 Generating JPMC group ID candidates...")
        
        # Strategy 1: Direct account number variations
        direct_variations = [
            account_num,  # 334224
            f"{account_num}1",  # 3342241
            f"{account_num}0",  # 3342240
            f"1{account_num}",  # 1334224
            f"0{account_num}",  # 0334224
            f"{account_num}00",  # 33422400
            f"00{account_num}",  # 00334224
        ]
        candidates.extend(direct_variations)
        
        # Strategy 2: Account number with systematic offsets
        for offset in [1, 10, 100, 1000, 10000, 100000]:
            candidates.extend([
                str(account_int + offset),
                str(account_int - offset)
            ])
        
        # Strategy 3: Account number in known group ID ranges
        # Wells Fargo: 838043 -> 4357341 (4M range)
        # TD Bank: 1912101 -> 7028358 (7M range)
        # JPMC: 334224 -> likely in 3M, 4M, or 5M range
        
        group_id_ranges = [
            (3000000, 3500000),  # Close to account number range
            (4000000, 4500000),  # Wells Fargo range
            (5000000, 5500000),  # Between Wells Fargo and TD Bank
            (7000000, 7500000),  # TD Bank range
            (2000000, 3000000),  # Lower range
            (6000000, 7000000),  # Between ranges
        ]
        
        for start, end in group_id_ranges:
            # Generate systematic IDs from each range
            step = (end - start) // 100  # 100 candidates per range
            for i in range(100):
                candidate_id = start + (i * step)
                candidates.append(str(candidate_id))
        
        # Strategy 4: Account number with common prefixes/suffixes
        for prefix in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            candidates.append(f"{prefix}{account_num}")
        
        for suffix in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            candidates.append(f"{account_num}{suffix}")
        
        # Strategy 5: Account number with double digits
        for prefix in ['11', '22', '33', '44', '55', '66', '77', '88', '99']:
            candidates.append(f"{prefix}{account_num}")
        
        for suffix in ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99']:
            candidates.append(f"{account_num}{suffix}")
        
        # Remove duplicates and sort
        unique_candidates = sorted(list(set(candidates)))
        
        print(f"   ✅ Generated {len(unique_candidates)} unique candidates")
        print(f"   🎯 Sample candidates: {unique_candidates[:10]}")
        
        return unique_candidates
    
    def test_group_id(self, group_id: str) -> Dict:
        """Test if a group ID is accessible"""
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
    
    def discover_jpmc_group_id(self) -> Dict:
        """Discover JPMC group ID"""
        print(f"\n🔍 DISCOVERING JPMC GROUP ID")
        print("=" * 30)
        print(f"Customer: {self.customer['name']}")
        print(f"Account: {self.customer['account_number']}")
        
        # Generate candidates
        candidates = self.generate_jpmc_candidates()
        
        # Test candidates (limit to avoid too many requests)
        test_limit = 200
        print(f"\n🧪 Testing top {test_limit} candidates...")
        
        results = []
        for i, candidate in enumerate(candidates[:test_limit]):
            if i % 20 == 0:
                print(f"   Testing candidate {i+1}/{test_limit}: {candidate}")
            
            result = self.test_group_id(candidate)
            results.append(result)
            
            # Small delay to be respectful
            time.sleep(0.1)
        
        # Sort results by confidence
        results.sort(key=lambda x: {
            'high': 3, 'medium': 2, 'low': 1, 'none': 0
        }.get(x.get('confidence', 'none'), 0), reverse=True)
        
        # Show results
        print(f"\n📊 JPMC DISCOVERY RESULTS:")
        print("-" * 30)
        
        high_confidence = [r for r in results if r.get('confidence') == 'high']
        medium_confidence = [r for r in results if r.get('confidence') == 'medium']
        
        if high_confidence:
            print("🎯 HIGH CONFIDENCE CANDIDATES:")
            for i, result in enumerate(high_confidence[:10]):
                print(f"   {i+1}. Group ID: {result['group_id']}")
                print(f"      URL: {result['url']}")
                print(f"      Status: {result['http_status']}")
                print()
        
        if medium_confidence:
            print("🔍 MEDIUM CONFIDENCE CANDIDATES:")
            for i, result in enumerate(medium_confidence[:10]):
                print(f"   {i+1}. Group ID: {result['group_id']}")
                print(f"      URL: {result['url']}")
                print(f"      Status: {result['http_status']}")
                print()
        
        if not high_confidence and not medium_confidence:
            print("❌ No high or medium confidence candidates found")
            print("💡 Consider manual portal search or contact Red Hat support")
        
        # Save results
        report = {
            'customer': self.customer['name'],
            'account_number': self.customer['account_number'],
            'discovery_timestamp': datetime.now().isoformat(),
            'total_candidates_tested': len(results),
            'high_confidence_candidates': high_confidence,
            'medium_confidence_candidates': medium_confidence,
            'all_results': results[:50]  # Top 50 results
        }
        
        report_file = f"/tmp/jpmc_group_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📁 Results saved to: {report_file}")
        
        return report

def main():
    """Run JPMC group ID discovery"""
    discovery = JPMCGroupDiscovery()
    report = discovery.discover_jpmc_group_id()
    
    print("\n🎯 NEXT STEPS FOR JPMC:")
    print("1. Review high-confidence candidates in the report")
    print("2. Manually test the top candidates in Red Hat portal")
    print("3. Look for JPMC-specific content or discussions")
    print("4. Update RFE automation configuration with confirmed group ID")
    
    if report['high_confidence_candidates']:
        print(f"\n🎉 FOUND {len(report['high_confidence_candidates'])} HIGH CONFIDENCE CANDIDATES!")
        print("   Test these manually in Red Hat portal:")
        for candidate in report['high_confidence_candidates'][:3]:
            print(f"   - {candidate['group_id']}: {candidate['url']}")

if __name__ == '__main__':
    main()

