#!/usr/bin/env python3
"""
Test script for dynamic inventory functionality
"""

import json
import subprocess
import sys

def test_rhcase_data():
    """Test rhcase data retrieval"""
    print("🔍 Testing rhcase data retrieval...")
    
    try:
        cmd = [
            "rhcase",
            "list",
            "--all",
            "--format", "json",
            "--includefilter", "sbrGroup,Ansible"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            check=False
        )
        
        if result.returncode != 0:
            print(f"❌ rhcase command failed: {result.stderr}")
            return None
        
        # Parse JSON output
        try:
            cases = json.loads(result.stdout)
            if not isinstance(cases, list):
                print("❌ rhcase output is not a list")
                return None
            
            print(f"✅ Found {len(cases)} cases from rhcase")
            
            # Group by account
            accounts = {}
            for case in cases:
                account_number = case.get('accountNumber')
                if account_number:
                    if account_number not in accounts:
                        accounts[account_number] = {
                            'name': case.get('account', {}).get('name', 'Unknown'),
                            'cases': 0
                        }
                    accounts[account_number]['cases'] += 1
            
            print(f"✅ Found {len(accounts)} unique accounts:")
            for account_number, info in accounts.items():
                print(f"  - {account_number}: {info['name']} ({info['cases']} cases)")
            
            return accounts
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ rhcase command timed out")
        return None
    except FileNotFoundError:
        print("❌ rhcase executable not found")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    """Main test function"""
    print("🚀 Dynamic Inventory Test")
    print("=" * 30)
    
    accounts = test_rhcase_data()
    
    if accounts:
        print(f"\n✅ Test successful! Found {len(accounts)} customers")
        print("\n📊 Sample customer data:")
        for i, (account_number, info) in enumerate(list(accounts.items())[:3]):
            print(f"  {i+1}. Account: {account_number}")
            print(f"     Name: {info['name']}")
            print(f"     Cases: {info['cases']}")
    else:
        print("\n❌ Test failed - no customer data found")
        sys.exit(1)

if __name__ == "__main__":
    main()
