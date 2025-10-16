#!/usr/bin/env python3

"""
Test script to demonstrate external tracker detection using Customer Portal API
"""

import sys
import os
sys.path.append('/home/jbyrd/pai/rfe-automation-clean/rhcase/tamscripts')

try:
    import rhcase
    print("✅ Successfully imported rhcase module")
except ImportError as e:
    print(f"❌ Failed to import rhcase: {e}")
    sys.exit(1)

def test_external_trackers():
    """Test external tracker detection for JPMC cases"""
    
    # Test cases from JPMC
    test_cases = [
        "03208295",  # Case that should have external tracker
        "03662419",  # Bug case
        "03845427",  # RFE case
    ]
    
    print("🔍 Testing External Tracker Detection using Customer Portal API")
    print("=" * 60)
    
    for case_number in test_cases:
        print(f"\n📋 Testing Case: {case_number}")
        print("-" * 40)
        
        try:
            # Get external references using Customer Portal API
            external_references = rhcase.get_external_references(case_number, verbose=True)
            
            if external_references:
                print(f"✅ Found {len(external_references)} external tracker(s)")
                
                # Show the structure of external references
                print("📊 External Tracker Data Structure:")
                print(f"Type: {type(external_references)}")
                print(f"Content: {external_references}")
                
                # If it's a dict, show the keys
                if isinstance(external_references, dict):
                    print(f"Keys: {list(external_references.keys())}")
                    
                    # Check for external_tracker_updates
                    if 'external_tracker_updates' in external_references:
                        trackers = external_references['external_tracker_updates']
                        print(f"External Tracker Updates: {len(trackers)} found")
                        for i, tracker in enumerate(trackers):
                            print(f"  Tracker {i+1}: {tracker}")
                
            else:
                print("❌ No external trackers found")
                
        except Exception as e:
            print(f"❌ Error getting external references: {e}")
            print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_external_trackers()
