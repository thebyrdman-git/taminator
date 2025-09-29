#!/usr/bin/env python3
"""
Create separate Plex libraries for Charles's YouTube categories
"""

import requests
import json

PLEX_SERVER = "http://192.168.1.17:32400"
PLEX_TOKEN = "***REMOVED***"

# Categories that have videos
ACTIVE_CATEGORIES = {
    'Gaming-Minecraft': 8,
    'Gaming-Console': 6, 
    'Comedy': 4,
    'Misc': 4,
    'Educational': 3,
    'Animation': 2,
    'Gaming-Official': 2,
    'Entertainment': 1,
    'Pokemon-TCG': 1
}

def create_library(name, path):
    """Create a new Plex library"""
    url = f"{PLEX_SERVER}/library/sections"
    
    params = {
        'name': f"Charles {name}",
        'type': 'movie',  # Use movie type for flat video files
        'agent': 'com.plexapp.agents.none',  # No metadata agent
        'scanner': 'Plex Video Files Scanner',  # Video files scanner
        'location': path,
        'language': 'xn',  # Match existing library format
        'X-Plex-Token': PLEX_TOKEN
    }
    
    try:
        response = requests.post(url, params=params)
        if response.status_code in [200, 201]:
            print(f"✅ CREATED: Charles {name} library")
            return True
        else:
            print(f"❌ FAILED: Charles {name} - {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ ERROR creating {name}: {e}")
        return False

def refresh_library_by_name(name):
    """Refresh a library by name"""
    try:
        # Get library sections
        response = requests.get(f"{PLEX_SERVER}/library/sections?X-Plex-Token={PLEX_TOKEN}")
        if response.status_code != 200:
            return False
            
        # Find our library
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.text)
        
        for directory in root.findall('.//Directory'):
            if directory.get('title') == f"Charles {name}":
                section_id = directory.get('key')
                refresh_url = f"{PLEX_SERVER}/library/sections/{section_id}/refresh?X-Plex-Token={PLEX_TOKEN}"
                refresh_response = requests.get(refresh_url)
                print(f"📚 REFRESHED: Charles {name} (section {section_id})")
                return True
        
        print(f"❓ NOT FOUND: Charles {name}")
        return False
        
    except Exception as e:
        print(f"❌ REFRESH ERROR for {name}: {e}")
        return False

if __name__ == "__main__":
    print("🎬 Creating Separate Plex Libraries for Charles")
    print("=" * 60)
    
    success_count = 0
    
    for category, video_count in ACTIVE_CATEGORIES.items():
        library_path = f"/mnt/nfs_share/charles/youtube/{category}"
        
        if create_library(category, library_path):
            success_count += 1
            
        # Small delay between creations
        import time
        time.sleep(1)
    
    print(f"\n📊 RESULTS:")
    print(f"   Libraries Created: {success_count}/{len(ACTIVE_CATEGORIES)}")
    
    if success_count > 0:
        print(f"\n🔄 Refreshing new libraries...")
        for category in ACTIVE_CATEGORIES:
            refresh_library_by_name(category)
            time.sleep(2)
    
    print(f"\n✅ Charles now has {success_count} dedicated YouTube libraries!")
