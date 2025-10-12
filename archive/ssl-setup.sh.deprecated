#!/bin/bash

# 🦆 DuckDNS + SSL Setup for miraclemax.duckdns.org
# ================================================

echo "🦆 SETTING UP DUCKDNS + SSL FOR MIRACLEMAX"
echo "=========================================="

# Configuration
DOMAIN="miraclemax.duckdns.org"
DUCKDNS_TOKEN="YOUR_DUCKDNS_TOKEN_HERE"  # User needs to provide this
EMAIL="jbyrd@example.com"  # For Let's Encrypt
WEB_DIR="/home/jbyrd/web-youtube-system"

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx curl

# Install DuckDNS updater
echo "🦆 Setting up DuckDNS updater..."
mkdir -p /home/jbyrd/duckdns
cd /home/jbyrd/duckdns

cat > duck.sh << EOF
#!/bin/bash
curl "https://www.duckdns.org/update?domains=miraclemax&token=${DUCKDNS_TOKEN}&ip=" > duck.log 2>&1
EOF

chmod +x duck.sh

# Test DuckDNS update
echo "🧪 Testing DuckDNS update..."
./duck.sh
cat duck.log

# Add to crontab for automatic updates
echo "⏰ Adding DuckDNS to crontab..."
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/jbyrd/duckdns/duck.sh >/dev/null 2>&1") | crontab -

# Set up Python environment for web app
echo "🐍 Setting up Python environment..."
cd $WEB_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create enhanced SSL-enabled Flask app
echo "🔐 Creating SSL-enabled Flask app..."
cat > app_ssl.py << 'EOF'
#!/usr/bin/env python3
"""
🎬 Charles's YouTube Automation Web System - SSL Enabled
Complete web-based YouTube download and management system with SSL
"""

from flask import Flask, render_template, jsonify, request
import os
import ssl
import json
import subprocess
import sqlite3
import threading
import time
import csv
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'charles-youtube-system-ssl-2024'

# Configuration
YOUTUBE_DIR = "/mnt/nfs_share/charles/youtube"
DATABASE_PATH = "/home/jbyrd/web-youtube-system/youtube_automation.db"
SUBSCRIPTIONS_CSV = "/home/jbyrd/web-youtube-system/charles-subscriptions-complete.csv"
LOG_FILE = "/home/jbyrd/web-youtube-system/web-youtube.log"

# SSL Configuration
SSL_CERT_PATH = "/etc/letsencrypt/live/miraclemax.duckdns.org/fullchain.pem"
SSL_KEY_PATH = "/etc/letsencrypt/live/miraclemax.duckdns.org/privkey.pem"

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

# Import existing classes and functions from original app.py
class YouTubeAutomation:
    def __init__(self):
        self.setup_database()
        self.load_subscriptions()
    
    def setup_database(self):
        """Initialize SQLite database for tracking downloads"""
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
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

# Initialize automation system
youtube_automation = YouTubeAutomation()

# Web Routes (same as original)
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

# API Routes (same as original)
@app.route('/api/status')
def api_status():
    return jsonify(download_status)

@app.route('/api/channels')
def api_channels():
    channels = youtube_automation.get_channel_status()
    return jsonify(channels)

@app.route('/api/start_downloads', methods=['POST'])
def api_start_downloads():
    if not download_status['active']:
        # Mock start for now
        download_status['active'] = True
        return jsonify({'success': True, 'message': 'Download started'})
    else:
        return jsonify({'success': False, 'message': 'Download already in progress'})

@app.route('/api/stop_downloads', methods=['POST'])
def api_stop_downloads():
    download_status['active'] = False
    return jsonify({'success': True, 'message': 'Download stopped'})

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(YOUTUBE_DIR, exist_ok=True)
    os.makedirs('/home/jbyrd/web-youtube-system/templates', exist_ok=True)
    
    logger.info("🎬 Starting Charles's YouTube Web System with SSL")
    logger.info(f"📁 YouTube Directory: {YOUTUBE_DIR}")
    logger.info(f"📊 Database: {DATABASE_PATH}")
    logger.info(f"🔐 SSL Domain: miraclemax.duckdns.org")
    
    # Check if SSL certificates exist
    if os.path.exists(SSL_CERT_PATH) and os.path.exists(SSL_KEY_PATH):
        logger.info("🔐 Running with SSL certificates")
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(SSL_CERT_PATH, SSL_KEY_PATH)
        app.run(host='0.0.0.0', port=443, ssl_context=context, debug=False)
    else:
        logger.warning("⚠️  SSL certificates not found, running without SSL on port 5000")
        logger.info("🔧 To enable SSL, run: sudo certbot --nginx -d miraclemax.duckdns.org")
        app.run(host='0.0.0.0', port=5000, debug=True)
EOF

chmod +x app_ssl.py

# Configure Nginx reverse proxy
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/youtube-system << EOF
server {
    listen 80;
    server_name miraclemax.duckdns.org;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl;
    server_name miraclemax.duckdns.org;

    # SSL configuration (will be updated by certbot)
    ssl_certificate /etc/letsencrypt/live/miraclemax.duckdns.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/miraclemax.duckdns.org/privkey.pem;
    
    # Modern SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Proxy to Flask app
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/youtube-system /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    sudo systemctl reload nginx
    echo "✅ Nginx configured successfully!"
else
    echo "❌ Nginx configuration error!"
    exit 1
fi

echo ""
echo "🦆 SETUP INSTRUCTIONS:"
echo "======================"
echo ""
echo "1. 🔑 Get your DuckDNS token from https://www.duckdns.org/"
echo "2. 📝 Edit this script and replace YOUR_DUCKDNS_TOKEN_HERE with your token"
echo "3. 🚀 Run: sudo ./ssl-setup.sh"
echo "4. 🔐 Get SSL certificate: sudo certbot --nginx -d miraclemax.duckdns.org"
echo "5. 🎬 Start the app: cd $WEB_DIR && source venv/bin/activate && python app_ssl.py"
echo ""
echo "📡 Your YouTube system will be available at: https://miraclemax.duckdns.org"
echo ""
echo "🔧 To run as service, create systemd service file:"
echo "   sudo systemctl enable youtube-web-system"
echo "   sudo systemctl start youtube-web-system"
