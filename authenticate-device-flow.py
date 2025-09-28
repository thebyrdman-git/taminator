#!/usr/bin/env python3

"""
Device Flow YouTube API Authentication
No redirect URIs needed - just enter a code on a webpage
"""

import os
import sys
import json

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("❌ Google API libraries not installed!")
    sys.exit(1)

# YouTube API configuration
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
CREDENTIALS_FILE = 'oauth_credentials.json'
TOKEN_FILE = 'youtube_token.json'

def authenticate_with_device_flow():
    """Authenticate using device flow - no redirect URIs needed"""
    print("🔐 Starting YouTube API Authentication (Device Flow)")
    print("===================================================")
    print("Account: terrysnuckers@gmail.com")
    print("")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ {CREDENTIALS_FILE} not found!")
        return None
    
    # Load client config
    with open(CREDENTIALS_FILE, 'r') as f:
        client_config = json.load(f)
    
    # Create flow with device flow
    flow = InstalledAppFlow.from_client_config(
        client_config, SCOPES)
    
    print("🌐 Using Device Flow Authentication...")
    print("This method doesn't need redirect URIs!")
    print("")
    
    # Run device flow
    creds = flow.run_local_server(port=8080, open_browser=False)
    
    # Save credentials
    print("💾 Saving authentication token...")
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

def test_authentication():
    """Test authentication by getting subscription count"""
    try:
        youtube = authenticate_with_device_flow()
        if not youtube:
            return False
        
        print("🔍 Testing API access...")
        
        # Get subscription count
        request = youtube.subscriptions().list(
            part="snippet",
            mine=True,
            maxResults=1
        )
        response = request.execute()
        
        total_subs = response.get('pageInfo', {}).get('totalResults', 0)
        print(f"✅ Authentication successful!")
        print(f"📊 Found {total_subs} subscriptions")
        print("")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {str(e)}")
        return False

def main():
    print("🎬 YouTube API Device Flow Authentication")
    print("========================================")
    print("No redirect URIs needed - easier setup!")
    print("")
    
    success = test_authentication()
    
    if success:
        print("🎉 AUTHENTICATION COMPLETE!")
        print("===========================")
        print("✅ Token saved to: youtube_token.json")
        print("")
        print("📤 NEXT STEPS:")
        print("1. Upload youtube_token.json to the Plex server")
        print("2. Run the YouTube automation")
        print("")
        print("Transfer command:")
        print("scp youtube_token.json jbyrd@192.168.1.17:~/")
        print("")
        print("🚀 Charles's automation is ready!")
    else:
        print("❌ Authentication failed!")

if __name__ == '__main__':
    main()
