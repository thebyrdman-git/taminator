#!/usr/bin/env python3
"""
YouTube Bulk Subscribe Script
Subscribes terrysnuckers@gmail.com to all channels in Charles's CSV
"""

import json
import csv
import time
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# OAuth 2.0 configuration
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube',  # ⭐ WRITE PERMISSIONS FOR SUBSCRIPTIONS
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

CLIENT_SECRETS_FILE = 'oauth_credentials.json'
TOKEN_FILE = 'youtube_token.json'
CSV_FILE = 'charles-subscriptions-complete.csv'

def show_progress_bar(current, total, channel_name="", status=""):
    """Beautiful animated progress bar"""
    bar_width = 50
    progress = current / total
    filled = int(bar_width * progress)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    percentage = progress * 100
    
    print(f"\r🎬 [{bar}] {percentage:6.2f}% ({current:3d}/{total:3d}) {status} {channel_name[:30]:<30}", end="", flush=True)
    
    if current == total:
        print("\n🎉 BULK SUBSCRIPTION COMPLETE!")

def authenticate_youtube():
    """Authenticate with YouTube API using enhanced scopes"""
    print("🔐 AUTHENTICATING WITH ENHANCED PERMISSIONS...")
    print("   📋 Scopes: YouTube Read + Write + Subscription Management")
    
    creds = None
    
    # Load existing token
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        print("   ✅ Existing credentials found")
    except FileNotFoundError:
        print("   ❌ No existing credentials")
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("   🔄 Refreshing credentials...")
            try:
                creds.refresh(Request())
                print("   ✅ Credentials refreshed successfully")
            except Exception as e:
                print(f"   ❌ Refresh failed: {e}")
                print("   🔄 Getting new credentials...")
                creds = None
        
        if not creds:
            print("   🌐 Starting OAuth flow...")
            flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"\n   📱 Open this URL and authorize the application:")
            print(f"   {auth_url}")
            
            code = input("\n   🔑 Enter authorization code: ").strip()
            flow.fetch_token(code=code)
            creds = flow.credentials
        
        # Save credentials
        with open(TOKEN_FILE, 'w') as token_file:
            token_file.write(creds.to_json())
        print("   💾 Credentials saved")
    
    return build('youtube', 'v3', credentials=creds)

def load_channels_from_csv():
    """Load channel data from CSV"""
    print(f"\n📋 LOADING CHANNELS FROM {CSV_FILE}...")
    
    channels = []
    try:
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                channels.append({
                    'id': row['Channel Id'].strip(),
                    'title': row['Channel Title'].strip(),
                    'url': row['Channel Url'].strip()
                })
        
        print(f"   ✅ Loaded {len(channels)} channels")
        return channels
    
    except FileNotFoundError:
        print(f"   ❌ CSV file not found: {CSV_FILE}")
        return []
    except Exception as e:
        print(f"   ❌ Error loading CSV: {e}")
        return []

def subscribe_to_channel(youtube, channel_id, channel_title):
    """Subscribe to a single channel"""
    try:
        subscription_response = youtube.subscriptions().insert(
            part='snippet',
            body={
                'snippet': {
                    'resourceId': {
                        'kind': 'youtube#channel',
                        'channelId': channel_id
                    }
                }
            }
        ).execute()
        
        return True, "✅ Subscribed"
        
    except HttpError as e:
        error_details = json.loads(e.content)
        error_reason = error_details.get('error', {}).get('errors', [{}])[0].get('reason', 'unknown')
        
        if error_reason == 'subscriptionDuplicate':
            return True, "👍 Already subscribed"
        else:
            return False, f"❌ Error: {error_reason}"
    
    except Exception as e:
        return False, f"❌ Exception: {str(e)[:20]}"

def bulk_subscribe():
    """Main bulk subscription process"""
    print("🚀 STARTING BULK SUBSCRIPTION PROCESS")
    print("=" * 50)
    
    # Authenticate
    youtube = authenticate_youtube()
    if not youtube:
        print("❌ Authentication failed!")
        return False
    
    # Load channels
    channels = load_channels_from_csv()
    if not channels:
        print("❌ No channels to process!")
        return False
    
    print(f"\n🎯 SUBSCRIBING TO {len(channels)} CHANNELS...")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for i, channel in enumerate(channels, 1):
        success, status = subscribe_to_channel(youtube, channel['id'], channel['title'])
        
        if success:
            successful += 1
        else:
            failed += 1
        
        show_progress_bar(i, len(channels), channel['title'], status)
        
        # Rate limiting - be nice to YouTube's API
        time.sleep(0.5)
    
    print(f"\n\n📊 SUBSCRIPTION SUMMARY:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📊 Total: {len(channels)}")
    
    return successful > 0

if __name__ == "__main__":
    print("🎬 CHARLES'S YOUTUBE BULK SUBSCRIBER")
    print("   terrysnuckers@gmail.com → 249 channels")
    print("=" * 50)
    
    success = bulk_subscribe()
    
    if success:
        print("\n🎉 BULK SUBSCRIPTION PROCESS COMPLETED!")
        print("   Charles's YouTube automation is ready! 🚀")
    else:
        print("\n❌ BULK SUBSCRIPTION PROCESS FAILED!")
        sys.exit(1)