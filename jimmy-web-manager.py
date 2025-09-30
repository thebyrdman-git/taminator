#!/usr/bin/env python3
"""
Jimmy's YouTube Download Manager Web Interface
Personal management dashboard for jimmykbyrd@gmail.com YouTube automation
"""

from flask import Flask, render_template_string, jsonify, request
import sqlite3
import subprocess
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jimmy-youtube-system-2025'

# Jimmy's configuration
JIMMY_YOUTUBE_DIR = "/mnt/nfs_share/jimmy/youtube"
JIMMY_DATABASE_PATH = "/home/jbyrd/hatter-pai/jimmy_youtube_automation.db"

# Global status for downloads
jimmy_download_status = {
    'active': False,
    'current_channel': None,
    'progress': 0,
    'total_channels': 0,
    'completed_channels': 0,
    'downloaded_videos': 0,
    'errors': []
}

def get_jimmy_stats():
    """Get Jimmy's YouTube system statistics"""
    try:
        conn = sqlite3.connect(JIMMY_DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get channel counts by category
        categories = cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM jimmy_channels 
            GROUP BY category 
            ORDER BY count DESC
        ''').fetchall()
        
        # Get recent downloads
        recent = cursor.execute('''
            SELECT channel_name, video_title, category, downloaded_at
            FROM jimmy_downloads 
            ORDER BY downloaded_at DESC 
            LIMIT 10
        ''').fetchall()
        
        # Get total counts
        total_channels = cursor.execute('SELECT COUNT(*) FROM jimmy_channels').fetchone()[0]
        total_downloads = cursor.execute('SELECT COUNT(*) FROM jimmy_downloads').fetchone()[0]
        
        conn.close()
        
        return {
            'categories': categories,
            'recent_downloads': recent,
            'total_channels': total_channels,
            'total_downloads': total_downloads
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def jimmy_dashboard():
    """Jimmy's YouTube automation dashboard"""
    stats = get_jimmy_stats()
    
    dashboard_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jimmy's YouTube Download Manager</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
            .stat-number { font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }
            .stat-label { font-size: 1.1em; opacity: 0.9; }
            .categories { background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; backdrop-filter: blur(10px); margin-bottom: 20px; }
            .category-item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
            .category-item:last-child { border-bottom: none; }
            .controls { display: flex; gap: 15px; justify-content: center; margin: 20px 0; }
            .btn { padding: 12px 25px; border: none; border-radius: 25px; font-size: 1em; cursor: pointer; transition: transform 0.2s; }
            .btn-primary { background: #4CAF50; color: white; }
            .btn-secondary { background: #2196F3; color: white; }
            .btn:hover { transform: translateY(-2px); }
            .status { text-align: center; margin: 20px 0; padding: 15px; border-radius: 10px; }
            .status.downloading { background: rgba(255, 193, 7, 0.2); }
            .status.idle { background: rgba(76, 175, 80, 0.2); }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎬 Jimmy's YouTube Manager</h1>
                <p>Personal Download Dashboard for jimmykbyrd@gmail.com</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ stats.total_channels or 0 }}</div>
                    <div class="stat-label">📺 Subscribed Channels</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">6</div>
                    <div class="stat-label">📚 Plex Libraries</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.total_downloads or 0 }}</div>
                    <div class="stat-label">⬇️ Downloaded Videos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="systemStatus">{{ 'Active' if status.active else 'Ready' }}</div>
                    <div class="stat-label">🎯 System Status</div>
                </div>
            </div>

            <div class="categories">
                <h3>📊 Jimmy's YouTube Categories</h3>
                {% if stats.categories %}
                    {% for category, count in stats.categories %}
                    <div class="category-item">
                        <span>🎬 Jimmy Youtube {{ category }}</span>
                        <span><strong>{{ count }}</strong> channels</span>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="category-item">
                        <span>Loading categories...</span>
                    </div>
                {% endif %}
            </div>

            <div class="controls">
                <button class="btn btn-primary" onclick="startDownloads()">🚀 Start Downloads</button>
                <button class="btn btn-secondary" onclick="refreshPlex()">📚 Refresh Plex</button>
                <button class="btn btn-secondary" onclick="viewStatus()">📊 View Status</button>
            </div>

            <div id="statusDisplay" class="status idle">
                <strong>💡 Ready to download from your 29 YouTube subscriptions!</strong><br>
                Videos will be organized into 6 categorized Plex libraries.
            </div>
        </div>

        <script>
            function startDownloads() {
                document.getElementById('statusDisplay').className = 'status downloading';
                document.getElementById('statusDisplay').innerHTML = '<strong>🔄 Starting downloads from Jimmy\\'s 29 subscriptions...</strong><br>This may take a few minutes.';
                
                fetch('/api/start_downloads', {method: 'POST'})
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            updateStatus();
                        } else {
                            alert('Error starting downloads: ' + data.error);
                        }
                    });
            }

            function refreshPlex() {
                fetch('/api/refresh_plex', {method: 'POST'})
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                    });
            }

            function viewStatus() {
                fetch('/api/status')
                    .then(response => response.json())
                    .then(data => {
                        let status = `Status: ${data.active ? 'Downloading' : 'Idle'}\\n`;
                        status += `Progress: ${data.completed_channels}/${data.total_channels}\\n`;
                        status += `Videos Downloaded: ${data.downloaded_videos}`;
                        alert(status);
                    });
            }

            function updateStatus() {
                fetch('/api/status')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('systemStatus').textContent = data.active ? 'Downloading' : 'Ready';
                        
                        if (data.active) {
                            document.getElementById('statusDisplay').className = 'status downloading';
                            document.getElementById('statusDisplay').innerHTML = 
                                `<strong>🔄 Downloading: ${data.current_channel || 'Processing...'}</strong><br>` +
                                `Progress: ${data.completed_channels}/${data.total_channels} channels`;
                            setTimeout(updateStatus, 2000);
                        } else {
                            document.getElementById('statusDisplay').className = 'status idle';
                            document.getElementById('statusDisplay').innerHTML = 
                                '<strong>✅ Downloads complete!</strong><br>Check your Jimmy Youtube libraries in Plex.';
                        }
                    });
            }
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(dashboard_html, stats=stats, status=jimmy_download_status)

@app.route('/api/start_downloads', methods=['POST'])
def api_start_downloads():
    """Start Jimmy's YouTube downloads"""
    try:
        # Start download in background thread
        thread = threading.Thread(target=run_jimmy_downloads)
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Downloads started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/refresh_plex', methods=['POST'])
def api_refresh_plex():
    """Refresh Jimmy's Plex libraries"""
    try:
        # Import and run the refresh function
        import requests
        
        PLEX_SERVER = "http://192.168.1.17:32400"
        PLEX_TOKEN = "***REMOVED***"
        
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
                    requests.get(refresh_url)
                    refreshed += 1
            
            return jsonify({'success': True, 'message': f'Refreshed {refreshed} Jimmy Youtube libraries'})
        
        return jsonify({'success': False, 'error': 'Could not connect to Plex'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/status')
def api_status():
    """Get current download status"""
    return jsonify(jimmy_download_status)

def run_jimmy_downloads():
    """Background download process"""
    global jimmy_download_status
    
    try:
        jimmy_download_status['active'] = True
        jimmy_download_status['errors'] = []
        
        # Run the download script
        result = subprocess.run([
            'python3', '/home/jbyrd/hatter-pai/jimmy-youtube-app.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            jimmy_download_status['downloaded_videos'] += 1
        else:
            jimmy_download_status['errors'].append(result.stderr)
        
    except Exception as e:
        jimmy_download_status['errors'].append(str(e))
    finally:
        jimmy_download_status['active'] = False

if __name__ == '__main__':
    print("🎬 Starting Jimmy's YouTube Download Manager")
    print("=" * 50)
    print("📊 Dashboard: http://192.168.1.34:5001")
    print("🎯 Managing 29 YouTube subscriptions")
    print("📚 6 Plex libraries: Jimmy Youtube [Category]")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
