#!/usr/bin/env python3

"""
YouTube API Helper for Charles's Automation
Uses terrysnuckers@gmail.com account for authenticated access
"""

import json
import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# YouTube API configuration
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CREDENTIALS_FILE = 'oauth_credentials.json'
TOKEN_FILE = 'youtube_token.json'

def authenticate_youtube():
    """Authenticate and return YouTube service object"""
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERROR: {CREDENTIALS_FILE} not found!")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def get_my_subscriptions():
    """Get all subscriptions from the authenticated account"""
    try:
        youtube = authenticate_youtube()
        
        subscriptions = []
        next_page_token = None
        
        while True:
            request = youtube.subscriptions().list(
                part="snippet",
                mine=True,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response['items']:
                channel_id = item['snippet']['resourceId']['channelId']
                channel_title = item['snippet']['title']
                channel_url = f"https://www.youtube.com/channel/{channel_id}"
                
                subscriptions.append({
                    'id': channel_id,
                    'name': channel_title,
                    'url': channel_url
                })
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return subscriptions
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return []

def get_latest_videos(channel_id, max_results=5):
    """Get latest videos from a specific channel"""
    try:
        youtube = authenticate_youtube()
        
        # Search for latest videos from this channel
        search_request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=max_results,
            order="date",
            type="video"
        )
        search_response = search_request.execute()
        
        videos = []
        for item in search_response['items']:
            video_info = {
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'published': item['snippet']['publishedAt']
            }
            videos.append(video_info)
        
        return videos
    
    except Exception as e:
        print(f"ERROR getting videos for {channel_id}: {str(e)}")
        return []

def main():
    """Main function - handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 youtube-api-helper.py subscriptions")
        print("  python3 youtube-api-helper.py videos <channel_id>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "subscriptions":
        print("🔄 Getting subscriptions from terrysnuckers@gmail.com...")
        subscriptions = get_my_subscriptions()
        
        if subscriptions:
            print(f"✅ Found {len(subscriptions)} subscriptions")
            # Output JSON for bash script to parse
            print(json.dumps({"subscriptions": subscriptions}, indent=2))
        else:
            print("❌ No subscriptions found or API error")
            sys.exit(1)
    
    elif command == "videos" and len(sys.argv) > 2:
        channel_id = sys.argv[2]
        max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        
        print(f"🔄 Getting latest videos from channel {channel_id}...")
        videos = get_latest_videos(channel_id, max_results)
        
        if videos:
            print(f"✅ Found {len(videos)} videos")
            print(json.dumps({"videos": videos}, indent=2))
        else:
            print(f"❌ No videos found for channel {channel_id}")
    
    else:
        print("Invalid command. Use 'subscriptions' or 'videos <channel_id>'")
        sys.exit(1)

if __name__ == '__main__':
    main()

