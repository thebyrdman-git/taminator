#!/usr/bin/env python3
"""
Improved categorization system for Jimmy's YouTube channels
Based on actual subscription analysis
"""

import csv
import os

# Improved categorization for Jimmy's interests
JIMMY_CHANNEL_CATEGORIES = {
    'Gaming': [
        'Nintendo of America', 'MorePegasus', 'Nintendo', 'PlayStation', 
        'Xbox', 'GameXplain', 'IGN', 'Gamespot'
    ],
    
    'Legal-Educational': [
        'Law By Mike', 'Legal Eagle', 'Steve Lehto', 'Attorney Tom'
    ],
    
    'Tech-Reviews': [
        'DazzReviews', 'Unbox Therapy', 'MKBHD', 'Linus Tech Tips',
        'Dave2D', 'Austin Evans'
    ],
    
    'Comedy-Entertainment': [
        'RoyalPear', 'SNL', 'Comedy Central', 'The Tonight Show',
        'Late Night', 'Conan O\'Brien'
    ],
    
    'News-Politics': [
        'CNN', 'BBC', 'NPR', 'The Daily Show', 'Last Week Tonight'
    ],
    
    'Lifestyle-Personal': [
        'Casey Neistat', 'Peter McKinnon', 'Matt D\'Avella'
    ]
}

def get_category_for_channel(channel_name):
    """Return category for a given channel name"""
    for category, channels in JIMMY_CHANNEL_CATEGORIES.items():
        if channel_name in channels:
            return category
    
    # Fallback pattern matching
    name_lower = channel_name.lower()
    
    if any(term in name_lower for term in ['game', 'gaming', 'nintendo', 'playstation']):
        return 'Gaming'
    elif any(term in name_lower for term in ['law', 'legal', 'attorney', 'lawyer']):
        return 'Legal-Educational'
    elif any(term in name_lower for term in ['review', 'tech', 'unbox']):
        return 'Tech-Reviews'
    elif any(term in name_lower for term in ['comedy', 'funny', 'entertainment']):
        return 'Comedy-Entertainment'
    elif any(term in name_lower for term in ['news', 'politics', 'daily']):
        return 'News-Politics'
    
    return 'Personal-Interest'  # Better default than "General"

def recategorize_subscriptions():
    """Re-categorize Jimmy's subscriptions with improved logic"""
    categories = {}
    
    with open('jimmy-subscriptions.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            channel_name = row['Channel Title']
            category = get_category_for_channel(channel_name)
            
            if category not in categories:
                categories[category] = []
            
            categories[category].append({
                'name': channel_name,
                'id': row['Channel Id'],
                'url': row['Channel Url'],
                'description': row.get('Description', '')
            })
    
    return categories

def create_directory_structure(base_path="/mnt/nfs_share/jimmy/youtube"):
    """Create directory structure for categorized downloads"""
    categories = recategorize_subscriptions()
    
    print(f"🏗️ CREATING DIRECTORY STRUCTURE:")
    print(f"Base path: {base_path}")
    print("=" * 50)
    
    # Note: We're creating the plan here, actual directory creation happens on miraclemax
    for category, channels in categories.items():
        category_path = f"{base_path}/{category}"
        print(f"📁 {category_path}/ ({len(channels)} channels)")
        
        # Show first few channels in each category
        for i, channel in enumerate(channels[:3]):
            print(f"   • {channel['name']}")
        if len(channels) > 3:
            print(f"   ... and {len(channels) - 3} more")
        print()
    
    return categories

if __name__ == "__main__":
    print("🎯 Jimmy's Improved YouTube Categorization")
    print("=" * 50)
    
    categories = create_directory_structure()
    
    print(f"📊 FINAL BREAKDOWN:")
    print("=" * 30)
    total_channels = sum(len(channels) for channels in categories.values())
    for category, channels in sorted(categories.items()):
        percentage = (len(channels) / total_channels) * 100
        print(f"{category}: {len(channels)} channels ({percentage:.1f}%)")
    
    print(f"\n✅ Ready to create directories and set up automation!")
    print(f"Total: {total_channels} channels categorized")

