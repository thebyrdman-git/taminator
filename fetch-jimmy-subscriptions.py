#!/usr/bin/env python3
"""
Fetch Jimmy's YouTube subscriptions and categorize them
Based on the Charles system but adapted for adult professional interests
"""

import os
import json
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def load_youtube_credentials():
    """Load YouTube API credentials from token file"""
    creds = None
    token_file = "youtube_token.json"
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save refreshed credentials
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
    
    return creds

def fetch_subscriptions():
    """Fetch all YouTube subscriptions"""
    creds = load_youtube_credentials()
    youtube = build('youtube', 'v3', credentials=creds)
    
    subscriptions = []
    next_page_token = None
    
    print("🔄 Fetching YouTube subscriptions...")
    
    while True:
        request = youtube.subscriptions().list(
            part='snippet',
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        )
        
        response = request.execute()
        
        for item in response['items']:
            snippet = item['snippet']
            subscription = {
                'Channel Id': snippet['resourceId']['channelId'],
                'Channel Title': snippet['title'],
                'Channel Url': f"https://www.youtube.com/channel/{snippet['resourceId']['channelId']}",
                'Description': snippet.get('description', '')[:100]  # First 100 chars
            }
            subscriptions.append(subscription)
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
        
        print(f"   Fetched {len(subscriptions)} subscriptions so far...")
    
    print(f"✅ Total subscriptions found: {len(subscriptions)}")
    return subscriptions

def save_subscriptions_csv(subscriptions, filename):
    """Save subscriptions to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Channel Id', 'Channel Url', 'Channel Title', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(subscriptions)
    
    print(f"✅ Saved subscriptions to: {filename}")

def categorize_channel(channel_name, description):
    """Categorize a channel based on name and description"""
    name_lower = channel_name.lower()
    desc_lower = description.lower()
    
    # Tech/Professional categories
    if any(term in name_lower for term in ['tech', 'linux', 'coding', 'programming', 'developer', 'software', 'devops', 'cloud', 'aws', 'kubernetes', 'docker', 'ansible', 'redhat', 'rhel', 'fedora', 'openshift']):
        return 'Tech-Professional'
    
    # Gaming categories
    if any(term in name_lower for term in ['gaming', 'gamer', 'game', 'nintendo', 'playstation', 'xbox', 'steam', 'twitch']):
        return 'Gaming'
    
    # Educational/Learning
    if any(term in name_lower for term in ['tutorial', 'learn', 'course', 'education', 'university', 'academy', 'training', 'how to']):
        return 'Educational'
    
    # News/Current Events  
    if any(term in name_lower for term in ['news', 'cnn', 'bbc', 'npr', 'current', 'politics', 'breaking']):
        return 'News-Current'
    
    # Entertainment
    if any(term in name_lower for term in ['comedy', 'funny', 'entertainment', 'podcast', 'talk show', 'late night']):
        return 'Entertainment'
    
    # DIY/Hobbies
    if any(term in name_lower for term in ['diy', 'maker', 'build', 'craft', 'woodwork', 'electronics', 'repair', 'review']):
        return 'Hobbies-DIY'
    
    # Default category
    return 'General'

def analyze_subscriptions(subscriptions):
    """Analyze and categorize subscriptions"""
    categories = {}
    
    for sub in subscriptions:
        category = categorize_channel(sub['Channel Title'], sub['Description'])
        if category not in categories:
            categories[category] = []
        categories[category].append(sub)
    
    print(f"\n📊 SUBSCRIPTION BREAKDOWN:")
    print("=" * 40)
    for category, channels in sorted(categories.items()):
        print(f"📁 {category}: {len(channels)} channels")
        # Show first 3 examples
        for i, channel in enumerate(channels[:3]):
            print(f"   • {channel['Channel Title']}")
        if len(channels) > 3:
            print(f"   ... and {len(channels) - 3} more")
        print()
    
    return categories

if __name__ == "__main__":
    print("🎬 Jimmy's YouTube Subscription Fetcher")
    print("=" * 50)
    
    try:
        # Fetch subscriptions
        subs = fetch_subscriptions()
        
        # Save to CSV
        csv_filename = "jimmy-subscriptions.csv"
        save_subscriptions_csv(subs, csv_filename)
        
        # Analyze and categorize
        categories = analyze_subscriptions(subs)
        
        print(f"✅ Ready to set up categorized directories and automation!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure youtube_token.json is valid")
        print("2. Check YouTube API quota limits") 
        print("3. Verify Google OAuth credentials")

