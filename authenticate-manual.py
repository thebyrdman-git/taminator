#!/usr/bin/env python3

"""
Manual YouTube API Authentication
No redirect URIs, no localhost - completely manual process
"""

import os
import sys
import json
import urllib.parse

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

def manual_authentication():
    """Manual authentication - no redirect URIs needed"""
    print("🔐 Manual YouTube API Authentication")
    print("====================================")
    print("Account: terrysnuckers@gmail.com")
    print("")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ {CREDENTIALS_FILE} not found!")
        return None
    
    # Load client config
    with open(CREDENTIALS_FILE, 'r') as f:
        client_config = json.load(f)
    
    client_id = client_config['installed']['client_id']
    client_secret = client_config['installed']['client_secret']
    
    # Build authorization URL manually
    auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode({
        'client_id': client_id,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',  # Special redirect URI for manual flow
        'scope': ' '.join(SCOPES),
        'response_type': 'code',
        'access_type': 'offline'
    })
    
    print("🌐 MANUAL AUTHENTICATION PROCESS")
    print("================================")
    print("")
    print("1️⃣ Copy this URL and open it in Chrome (terrysnuckers profile):")
    print("")
    print(auth_url)
    print("")
    print("2️⃣ Sign in as terrysnuckers@gmail.com")
    print("3️⃣ Authorize the application")
    print("4️⃣ Copy the authorization code from the page")
    print("5️⃣ Paste it below")
    print("")
    
    # Get authorization code from user
    auth_code = input("🔑 Enter the authorization code: ").strip()
    
    if not auth_code:
        print("❌ No authorization code provided!")
        return None
    
    print("")
    print("🔄 Exchanging code for access token...")
    
    # Create flow and exchange code for credentials
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    try:
        creds = flow.fetch_token(code=auth_code)
        
        # Convert to Credentials object
        creds = Credentials(
            token=creds['access_token'],
            refresh_token=creds.get('refresh_token'),
            token_uri=client_config['installed']['token_uri'],
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        
        # Save credentials
        print("💾 Saving authentication token...")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        return build('youtube', 'v3', credentials=creds)
        
    except Exception as e:
        print(f"❌ Token exchange failed: {str(e)}")
        return None

def test_authentication():
    """Test authentication by getting subscription count"""
    try:
        youtube = manual_authentication()
        if not youtube:
            return False
        
        print("")
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
    print("🎬 YouTube API Manual Authentication")
    print("===================================")
    print("No redirect URIs needed - 100% manual!")
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
        print("🚀 Charles's YouTube automation is ready!")
    else:
        print("❌ Authentication failed!")

if __name__ == '__main__':
    main()
