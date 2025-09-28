#!/usr/bin/env python3

"""
Local YouTube API Authentication
Run this on your local machine to authenticate terrysnuckers@gmail.com
Then transfer the token to the Plex server
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
    print("Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# YouTube API configuration
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
CREDENTIALS_FILE = 'oauth_credentials.json'
TOKEN_FILE = 'youtube_token.json'

def authenticate_youtube():
    """Authenticate and return YouTube service object"""
    print("🔐 Starting YouTube API Authentication")
    print("=====================================")
    print("Account: terrysnuckers@gmail.com")
    print("")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ {CREDENTIALS_FILE} not found!")
        print("Make sure oauth_credentials.json is in this directory")
        return None
    
    creds = None
    
    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        print("📋 Found existing token file")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🌐 Opening browser for OAuth authentication...")
            print("Please sign in as: terrysnuckers@gmail.com")
            print("")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Save credentials for next run
        print("💾 Saving authentication token...")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

def test_authentication():
    """Test authentication by getting subscription count"""
    try:
        youtube = authenticate_youtube()
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
    print("🎬 YouTube API Local Authentication")
    print("==================================")
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
    else:
        print("❌ Authentication failed!")
        print("Please check your credentials and try again.")

if __name__ == '__main__':
    main()
