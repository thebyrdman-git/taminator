#!/usr/bin/env python3
"""
Set up Jimmy's Personal YouTube-Plex System
Creates directories, categories, and Plex libraries with "Jimmy Youtube" naming
"""

import requests
import csv
import os

PLEX_SERVER = "http://192.168.1.17:32400"
PLEX_TOKEN = "***REMOVED***"

# Jimmy's categorized channels
JIMMY_CATEGORIES = {
    'Gaming': ['Nintendo of America', 'MorePegasus'],
    'Legal-Educational': ['Law By Mike'],
    'Tech-Reviews': ['DazzReviews'],
    'Animation': ['TheOdd1sOut', 'Danno Cal Drawings'],
    'Comedy-Entertainment': ['RoyalPear', 'Theatre of the Unaligned'],
    'Personal-Interest': []  # Will catch remaining channels
}

def get_category_for_channel(channel_name):
    """Return category for Jimmy's channel"""
    for category, channels in JIMMY_CATEGORIES.items():
        if channel_name in channels:
            return category
    
    # Pattern matching for uncategorized channels
    name_lower = channel_name.lower()
    
    if any(term in name_lower for term in ['game', 'gaming', 'nintendo', 'pegasus']):
        return 'Gaming'
    elif any(term in name_lower for term in ['law', 'legal', 'mike']):
        return 'Legal-Educational'
    elif any(term in name_lower for term in ['review', 'tech', 'dazz']):
        return 'Tech-Reviews'
    elif any(term in name_lower for term in ['draw', 'art', 'odd', 'animation']):
        return 'Animation'
    elif any(term in name_lower for term in ['comedy', 'funny', 'pear', 'theatre']):
        return 'Comedy-Entertainment'
    
    return 'Personal-Interest'

def create_jimmy_plex_libraries():
    """Create Jimmy Youtube Plex libraries"""
    # First, categorize the subscriptions
    categories_with_content = {}
    
    with open('jimmy-subscriptions.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            channel_name = row['Channel Title']
            category = get_category_for_channel(channel_name)
            
            if category not in categories_with_content:
                categories_with_content[category] = 0
            categories_with_content[category] += 1
    
    print("🎬 CREATING JIMMY YOUTUBE PLEX LIBRARIES")
    print("=" * 50)
    print()
    
    success_count = 0
    
    for category, count in categories_with_content.items():
        if count == 0:  # Skip empty categories
            continue
            
        library_name = f"Jimmy Youtube {category}"
        library_path = f"/mnt/nfs_share/jimmy/youtube/{category}"
        
        print(f"📚 Creating: {library_name} ({count} channels)")
        
        if create_plex_library(library_name, library_path):
            success_count += 1
    
    print(f"\n✅ Created {success_count} Jimmy Youtube libraries!")
    return success_count

def create_plex_library(name, path):
    """Create a new Plex library"""
    url = f"{PLEX_SERVER}/library/sections"
    
    params = {
        'name': name,
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
            print(f"   ✅ Created: {name}")
            return True
        else:
            print(f"   ❌ Failed: {name} - {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error creating {name}: {e}")
        return False

def create_directory_structure():
    """Show the directory structure that will be created on miraclemax"""
    print("📁 DIRECTORY STRUCTURE TO CREATE ON MIRACLEMAX:")
    print("=" * 55)
    print()
    
    base_path = "/mnt/nfs_share/jimmy/youtube"
    categories_with_content = {}
    
    with open('jimmy-subscriptions.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            channel_name = row['Channel Title']
            category = get_category_for_channel(channel_name)
            
            if category not in categories_with_content:
                categories_with_content[category] = []
            categories_with_content[category].append(channel_name)
    
    for category, channels in categories_with_content.items():
        if not channels:
            continue
        print(f"📂 {base_path}/{category}/")
        print(f"   Channels: {len(channels)}")
        for channel in channels[:3]:  # Show first 3
            print(f"   • {channel}")
        if len(channels) > 3:
            print(f"   ... and {len(channels) - 3} more")
        print()
    
    return categories_with_content

def show_plex_library_plan():
    """Show what Jimmy Youtube libraries will be created"""
    print("📚 JIMMY YOUTUBE PLEX LIBRARIES PLAN:")
    print("=" * 45)
    print()
    
    categories_with_content = {}
    with open('jimmy-subscriptions.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            channel_name = row['Channel Title']
            category = get_category_for_channel(channel_name)
            
            if category not in categories_with_content:
                categories_with_content[category] = 0
            categories_with_content[category] += 1
    
    for category, count in sorted(categories_with_content.items()):
        if count > 0:
            library_name = f"Jimmy Youtube {category}"
            print(f"📺 {library_name}")
            print(f"   Path: /mnt/nfs_share/jimmy/youtube/{category}/")
            print(f"   Channels: {count}")
            print()

if __name__ == "__main__":
    print("🎯 Jimmy's Personal YouTube-Plex Setup")
    print("=" * 50)
    print()
    
    # Show the plan
    show_plex_library_plan()
    create_directory_structure()
    
    print("\n🚀 READY TO EXECUTE:")
    print("1. Create directories on miraclemax")
    print("2. Create Jimmy Youtube Plex libraries") 
    print("3. Set up download automation")
    print()
    print("Would you like me to proceed? (This will create the Plex libraries)")

