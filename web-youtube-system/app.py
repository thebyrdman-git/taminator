#!/usr/bin/env python3
"""
🎬 Charles's YouTube Automation Web System
Complete web-based YouTube download and management system
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import json
import subprocess
import sqlite3
import threading
import time
import csv
from datetime import datetime
import yt_dlp
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'charles-youtube-system-2024'

# Configuration
YOUTUBE_DIR = "/mnt/nfs_share/charles/youtube"
DATABASE_PATH = "/home/jbyrd/hatter-pai/youtube_automation.db"
SUBSCRIPTIONS_CSV = "/home/jbyrd/hatter-pai/charles-subscriptions-complete.csv"
LOG_FILE = "/home/jbyrd/hatter-pai/web-youtube.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global state
download_status = {
    'active': False,
    'current_channel': None,
    'progress': 0,
    'total_channels': 0,
    'completed_channels': 0,
    'downloaded_videos': 0,
    'errors': []
}

class YouTubeAutomation:
    def __init__(self):
        self.setup_database()
        self.load_subscriptions()
    
    def setup_database(self):
        """Initialize SQLite database for tracking downloads"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                channel_id TEXT,
                url TEXT,
                status TEXT DEFAULT 'pending',
                last_download TIMESTAMP,
                video_count INTEGER DEFAULT 0,
                total_size INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY,
                channel_id INTEGER,
                video_id TEXT,
                title TEXT,
                download_date TIMESTAMP,
                file_path TEXT,
                file_size INTEGER,
                FOREIGN KEY (channel_id) REFERENCES channels (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def load_subscriptions(self):
        """Load subscriptions from CSV file"""
        if not os.path.exists(SUBSCRIPTIONS_CSV):
            logger.error(f"Subscriptions CSV not found: {SUBSCRIPTIONS_CSV}")
            return
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        with open(SUBSCRIPTIONS_CSV, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute('''
                    INSERT OR IGNORE INTO channels (name, channel_id, url)
                    VALUES (?, ?, ?)
                ''', (row['Channel Name'], row['Channel ID'], row['Channel URL']))
        
        conn.commit()
        conn.close()
        
        # Update global status
        download_status['total_channels'] = self.get_total_channels()
        logger.info(f"Loaded {download_status['total_channels']} channels from CSV")
    
    def get_total_channels(self):
        """Get total number of channels"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM channels")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_channel_status(self):
        """Get current status of all channels"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, status, video_count, total_size, last_download
            FROM channels ORDER BY name
        ''')
        channels = cursor.fetchall()
        conn.close()
        
        return [
            {
                'name': channel[0],
                'status': channel[1],
                'video_count': channel[2],
                'total_size': channel[3],
                'last_download': channel[4]
            }
            for channel in channels
        ]
    
    def download_channel_videos(self, channel_name, channel_url, max_videos=5):
        """Download videos from a specific channel"""
        try:
            # Update channel status to downloading
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE channels SET status = 'downloading', last_download = ?
                WHERE name = ?
            ''', (datetime.now().isoformat(), channel_name))
            conn.commit()
            conn.close()
            
            # Create channel directory
            channel_dir = os.path.join(YOUTUBE_DIR, channel_name.replace('/', '_'))
            os.makedirs(channel_dir, exist_ok=True)
            
            # yt-dlp options
            ydl_opts = {
                'outtmpl': f'{channel_dir}/%(upload_date)s - %(title)s.%(ext)s',
                'format': 'best[height<=720]/best',
                'writeinfojson': True,
                'writethumbnail': True,
                'writesubtitles': False,
                'playlistend': max_videos,
                'ignoreerrors': True,
            }
            
            downloaded_count = 0
            total_size = 0
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    # Get channel info
                    info = ydl.extract_info(channel_url, download=False)
                    if info and 'entries' in info:
                        for entry in list(info['entries'])[:max_videos]:
                            try:
                                # Download individual video
                                ydl.download([entry['webpage_url']])
                                downloaded_count += 1
                                
                                # Estimate file size (rough calculation)
                                estimated_size = entry.get('filesize', entry.get('filesize_approx', 50 * 1024 * 1024))  # Default 50MB
                                total_size += estimated_size
                                
                                logger.info(f"Downloaded: {entry.get('title', 'Unknown')} from {channel_name}")
                                
                            except Exception as e:
                                logger.error(f"Error downloading video from {channel_name}: {str(e)}")
                                continue
                    
                except Exception as e:
                    logger.error(f"Error processing channel {channel_name}: {str(e)}")
                    raise e
            
            # Update channel status to completed
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE channels SET status = 'completed', video_count = ?, total_size = ?
                WHERE name = ?
            ''', (downloaded_count, total_size, channel_name))
            conn.commit()
            conn.close()
            
            logger.info(f"Completed {channel_name}: {downloaded_count} videos, {total_size/1024/1024:.1f} MB")
            return True
            
        except Exception as e:
            # Update channel status to error
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE channels SET status = 'error'
                WHERE name = ?
            ''', (channel_name,))
            conn.commit()
            conn.close()
            
            logger.error(f"Failed to download from {channel_name}: {str(e)}")
            download_status['errors'].append(f"{channel_name}: {str(e)}")
            return False

youtube_automation = YouTubeAutomation()

def download_all_channels():
    """Download videos from all channels (runs in background thread)"""
    global download_status
    
    download_status['active'] = True
    download_status['progress'] = 0
    download_status['completed_channels'] = 0
    download_status['downloaded_videos'] = 0
    download_status['errors'] = []
    
    logger.info("Starting bulk download of all channels")
    
    try:
        # Get all pending channels
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, url FROM channels WHERE status != 'completed'")
        channels = cursor.fetchall()
        conn.close()
        
        total_channels = len(channels)
        download_status['total_channels'] = total_channels
        
        for i, (channel_name, channel_url) in enumerate(channels):
            if not download_status['active']:  # Check if download was stopped
                break
                
            download_status['current_channel'] = channel_name
            download_status['progress'] = int((i / total_channels) * 100)
            
            logger.info(f"Processing channel {i+1}/{total_channels}: {channel_name}")
            
            success = youtube_automation.download_channel_videos(channel_name, channel_url)
            if success:
                download_status['completed_channels'] += 1
                
                # Update downloaded videos count
                conn = sqlite3.connect(DATABASE_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT SUM(video_count) FROM channels WHERE status = 'completed'")
                total_videos = cursor.fetchone()[0] or 0
                conn.close()
                download_status['downloaded_videos'] = total_videos
            
            # Small delay to prevent overwhelming the system
            time.sleep(2)
        
        download_status['progress'] = 100
        logger.info(f"Bulk download completed: {download_status['completed_channels']} channels processed")
        
    except Exception as e:
        logger.error(f"Error in bulk download: {str(e)}")
        download_status['errors'].append(f"Bulk download error: {str(e)}")
    
    finally:
        download_status['active'] = False
        download_status['current_channel'] = None

# Web Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/subscriptions')
def subscriptions():
    """Subscriptions management page"""
    return render_template('subscriptions.html')

@app.route('/downloads')
def downloads():
    """Downloads control page"""
    return render_template('downloads.html')

@app.route('/settings')
def settings():
    """Settings and configuration page"""
    return render_template('settings.html')

# API Routes
@app.route('/api/status')
def api_status():
    """Get current download status"""
    return jsonify(download_status)

@app.route('/api/channels')
def api_channels():
    """Get all channels and their status"""
    channels = youtube_automation.get_channel_status()
    return jsonify(channels)

@app.route('/api/start_downloads', methods=['POST'])
def api_start_downloads():
    """Start downloading from all channels"""
    if not download_status['active']:
        # Start download in background thread
        thread = threading.Thread(target=download_all_channels)
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Download started'})
    else:
        return jsonify({'success': False, 'message': 'Download already in progress'})

@app.route('/api/stop_downloads', methods=['POST'])
def api_stop_downloads():
    """Stop current downloads"""
    download_status['active'] = False
    return jsonify({'success': True, 'message': 'Download stopped'})

@app.route('/api/refresh_plex', methods=['POST'])
def api_refresh_plex():
    """Trigger Plex library refresh"""
    try:
        import requests
        
        # Use the working Plex token and server
        PLEX_SERVER = "http://192.168.1.17:32400"
        PLEX_TOKEN = "***REMOVED***"
        
        headers = {"X-Plex-Token": PLEX_TOKEN}
        
        # Get library sections first
        response = requests.get(f"{PLEX_SERVER}/library/sections", headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Trigger deep refresh for all sections
            refresh_response = requests.get(
                f"{PLEX_SERVER}/library/sections/all/refresh",
                headers=headers,
                params={'force': '1', 'deep': '1'},
                timeout=10
            )
            
            if refresh_response.status_code == 200:
                logger.info("Plex deep refresh triggered successfully")
                return jsonify({'success': True, 'message': 'Plex deep refresh triggered! Check library in 5-10 minutes.'})
            else:
                return jsonify({'success': False, 'message': f'Plex refresh failed with status: {refresh_response.status_code}'})
        else:
            return jsonify({'success': False, 'message': f'Cannot connect to Plex server: {response.status_code}'})
            
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'message': 'Plex server timeout - server may be busy'})
    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'message': 'Cannot connect to Plex server at 192.168.1.17:32400'})
    except Exception as e:
        logger.error(f"Plex refresh error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/cleanup', methods=['POST'])
def api_cleanup():
    """Trigger 30-day retention cleanup"""
    try:
        # Run cleanup script
        result = subprocess.run([
            '/home/jbyrd/hatter-pai/bin/pai-youtube-retention-cleanup'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Cleanup completed'})
        else:
            return jsonify({'success': False, 'message': f'Cleanup failed: {result.stderr}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(YOUTUBE_DIR, exist_ok=True)
    os.makedirs('/home/jbyrd/hatter-pai/templates', exist_ok=True)
    os.makedirs('/home/jbyrd/hatter-pai/static', exist_ok=True)
    
    logger.info("🎬 Starting Charles's YouTube Web System")
    logger.info(f"📁 YouTube Directory: {YOUTUBE_DIR}")
    logger.info(f"📊 Database: {DATABASE_PATH}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
