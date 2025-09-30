#!/usr/bin/env python3
"""
Jimmy's Personal YouTube Download Automation
Based on Charles's system but adapted for jimmykbyrd@gmail.com
"""

import os
import csv
import sqlite3
import subprocess
from datetime import datetime
import yt_dlp
import logging

# Configuration for Jimmy's system
JIMMY_YOUTUBE_DIR = "/mnt/nfs_share/jimmy/youtube"
JIMMY_DATABASE_PATH = "/home/jbyrd/hatter-pai/jimmy_youtube_automation.db"
JIMMY_SUBSCRIPTIONS_CSV = "/home/jbyrd/hatter-pai-youtube/jimmy-subscriptions.csv"

# Jimmy's channel categories (from our analysis)
JIMMY_CATEGORIES = {
    'Gaming': ['Nintendo of America', 'MorePegasus'],
    'Animation': ['TheOdd1sOut', 'Danno Cal Drawings', 'Cartoon Universe'],
    'Comedy-Entertainment': ['RoyalPear', 'Theatre of the Unaligned'],
    'Legal-Educational': ['Law By Mike'],
    'Tech-Reviews': ['DazzReviews'],
    'Personal-Interest': []  # Default for uncategorized
}

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_category_for_channel(channel_name):
    """Get category for Jimmy's channels"""
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
    elif any(term in name_lower for term in ['draw', 'art', 'odd', 'animation', 'cartoon']):
        return 'Animation'
    elif any(term in name_lower for term in ['comedy', 'funny', 'pear', 'theatre']):
        return 'Comedy-Entertainment'
    
    return 'Personal-Interest'

def setup_jimmy_database():
    """Initialize Jimmy's YouTube automation database"""
    conn = sqlite3.connect(JIMMY_DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jimmy_channels (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            channel_id TEXT UNIQUE NOT NULL,
            url TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            last_download TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jimmy_downloads (
            id INTEGER PRIMARY KEY,
            channel_name TEXT NOT NULL,
            video_title TEXT NOT NULL,
            video_id TEXT NOT NULL,
            file_path TEXT NOT NULL,
            category TEXT NOT NULL,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Jimmy's database initialized successfully")

def load_jimmy_subscriptions():
    """Load Jimmy's subscriptions into database"""
    setup_jimmy_database()
    conn = sqlite3.connect(JIMMY_DATABASE_PATH)
    cursor = conn.cursor()
    
    with open(JIMMY_SUBSCRIPTIONS_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            channel_name = row['Channel Title']
            category = get_category_for_channel(channel_name)
            
            cursor.execute('''
                INSERT OR REPLACE INTO jimmy_channels (name, channel_id, url, category)
                VALUES (?, ?, ?, ?)
            ''', (channel_name, row['Channel Id'], row['Channel Url'], category))
    
    conn.commit()
    count = cursor.execute('SELECT COUNT(*) FROM jimmy_channels').fetchone()[0]
    conn.close()
    
    logger.info(f"Loaded {count} channels into Jimmy's database")
    return count

def download_jimmy_channel_videos(channel_name, channel_url, max_videos=1):
    """Download latest video from Jimmy's subscribed channel"""
    try:
        # Get category for this channel
        category = get_category_for_channel(channel_name)
        category_path = os.path.join(JIMMY_YOUTUBE_DIR, category)
        
        # Ensure category directory exists
        os.makedirs(category_path, exist_ok=True)
        
        logger.info(f"Downloading from {channel_name} to {category} category")
        
        # yt-dlp options optimized for single video downloads
        ydl_opts = {
            'format': 'best[height<=720]/best',
            'outtmpl': f'{category_path}/%(upload_date)s - {channel_name} - %(title)s.%(ext)s',
            'writeinfojson': False,
            'writethumbnail': False,
            'no_warnings': True,
            'extract_flat': False,
            'playlistend': max_videos,
            'cookiesfrom browser': ('firefox', None, None, None),  # Use browser cookies
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download from channel
            ydl.download([channel_url])
        
        # Update database
        conn = sqlite3.connect(JIMMY_DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE jimmy_channels SET last_download = ?, status = 'downloaded'
            WHERE name = ?
        ''', (datetime.now().isoformat(), channel_name))
        conn.commit()
        conn.close()
        
        logger.info(f"Successfully downloaded from {channel_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error downloading from {channel_name}: {e}")
        return False

def download_all_jimmy_channels():
    """Download latest videos from all of Jimmy's subscribed channels"""
    conn = sqlite3.connect(JIMMY_DATABASE_PATH)
    cursor = conn.cursor()
    
    channels = cursor.execute('''
        SELECT name, url FROM jimmy_channels 
        WHERE status = 'active' OR status IS NULL
        ORDER BY name
    ''').fetchall()
    
    conn.close()
    
    logger.info(f"Starting download for {len(channels)} Jimmy's channels")
    
    successful = 0
    failed = 0
    
    for channel_name, channel_url in channels:
        if download_jimmy_channel_videos(channel_name, channel_url):
            successful += 1
        else:
            failed += 1
        
        # Small delay between downloads
        import time
        time.sleep(2)
    
    logger.info(f"Jimmy's download complete: {successful} successful, {failed} failed")
    return successful, failed

def refresh_jimmy_plex_libraries():
    """Refresh all Jimmy Youtube Plex libraries"""
    import requests
    
    PLEX_SERVER = "http://192.168.1.17:32400"
    PLEX_TOKEN = "***REMOVED***"
    
    # Get all Jimmy Youtube libraries
    response = requests.get(f"{PLEX_SERVER}/library/sections?X-Plex-Token={PLEX_TOKEN}")
    
    if response.status_code == 200:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.text)
        
        refreshed = 0
        for directory in root.findall('.//Directory'):
            title = directory.get('title', '')
            if title.startswith('Jimmy Youtube'):
                section_id = directory.get('key')
                refresh_url = f"{PLEX_SERVER}/library/sections/{section_id}/refresh?X-Plex-Token={PLEX_TOKEN}&force=1&deep=1"
                refresh_response = requests.get(refresh_url)
                if refresh_response.status_code == 200:
                    logger.info(f"Refreshed: {title}")
                    refreshed += 1
        
        logger.info(f"Refreshed {refreshed} Jimmy Youtube libraries")
        return refreshed
    
    return 0

if __name__ == "__main__":
    print("🎬 Jimmy's YouTube Automation System")
    print("=" * 50)
    
    # Load subscriptions
    count = load_jimmy_subscriptions()
    print(f"✅ Loaded {count} Jimmy's subscriptions")
    
    # Download videos
    print("\n🔄 Starting downloads...")
    successful, failed = download_all_jimmy_channels()
    print(f"✅ Downloads complete: {successful} successful, {failed} failed")
    
    # Refresh Plex
    print("\n📚 Refreshing Plex libraries...")
    refreshed = refresh_jimmy_plex_libraries()
    print(f"✅ Refreshed {refreshed} Jimmy Youtube libraries")
    
    print(f"\n🎊 Jimmy's YouTube automation complete!")
