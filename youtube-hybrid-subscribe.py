#!/usr/bin/env python3
"""
YouTube Hybrid Subscription System
Creates streamlined manual subscription process for terrysnuckers@gmail.com
"""

import json
import csv
import webbrowser
import time
from urllib.parse import quote

CSV_FILE = 'charles-subscriptions-complete.csv'
OUTPUT_FILE = 'terrysnuckers-bulk-subscribe.html'

def show_progress_bar(current, total, channel_name="", status=""):
    """Beautiful animated progress bar"""
    bar_width = 50
    progress = current / total
    filled = int(bar_width * progress)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    percentage = progress * 100
    
    print(f"\r🔗 [{bar}] {percentage:6.2f}% ({current:3d}/{total:3d}) {status} {channel_name[:25]:<25}", end="", flush=True)
    
    if current == total:
        print(f"\n✨ Generated {total} subscription links!")

def load_channels_from_csv():
    """Load channel data from CSV"""
    print(f"📋 LOADING CHANNELS FROM {CSV_FILE}...")
    
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

def create_subscription_html(channels):
    """Create beautiful HTML page for streamlined subscriptions"""
    print(f"\n🎨 CREATING STREAMLINED SUBSCRIPTION PAGE...")
    
    # Group channels by category for better organization
    gaming_keywords = ['minecraft', 'nintendo', 'xbox', 'playstation', 'game', 'gaming']
    animation_keywords = ['animation', 'cartoon', 'animated']
    educational_keywords = ['theory', 'science', 'educational', 'learning']
    
    gaming_channels = []
    animation_channels = []
    educational_channels = []
    entertainment_channels = []
    
    for channel in channels:
        title_lower = channel['title'].lower()
        if any(keyword in title_lower for keyword in gaming_keywords):
            gaming_channels.append(channel)
        elif any(keyword in title_lower for keyword in animation_keywords):
            animation_channels.append(channel)
        elif any(keyword in title_lower for keyword in educational_keywords):
            educational_channels.append(channel)
        else:
            entertainment_channels.append(channel)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Charles's YouTube Subscriptions - Bulk Subscribe</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .stats {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 20px auto;
            max-width: 800px;
            color: white;
        }}
        
        .category {{
            background: white;
            border-radius: 15px;
            margin: 20px auto;
            max-width: 1200px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .category-header {{
            padding: 20px;
            font-size: 1.5em;
            font-weight: bold;
            text-align: center;
            color: white;
        }}
        
        .gaming {{ background: linear-gradient(135deg, #ff6b6b, #ffa500); }}
        .animation {{ background: linear-gradient(135deg, #4ecdc4, #44a08d); }}
        .educational {{ background: linear-gradient(135deg, #a8edea, #fed6e3); color: #333 !important; }}
        .entertainment {{ background: linear-gradient(135deg, #667eea, #764ba2); }}
        
        .channels-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            padding: 20px;
        }}
        
        .channel-card {{
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            transition: all 0.3s ease;
        }}
        
        .channel-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-color: #007bff;
        }}
        
        .channel-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }}
        
        .subscribe-btn {{
            background: linear-gradient(135deg, #ff0000, #cc0000);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            width: 100%;
            text-align: center;
        }}
        
        .subscribe-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255,0,0,0.3);
        }}
        
        .progress-container {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 20px auto;
            max-width: 800px;
            color: white;
            position: sticky;
            top: 20px;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            width: 0%;
            transition: width 0.3s ease;
        }}
        
        .bulk-actions {{
            text-align: center;
            margin: 20px 0;
        }}
        
        .bulk-btn {{
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            margin: 0 10px;
            transition: all 0.3s ease;
        }}
        
        .bulk-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎬 Charles's YouTube Universe</h1>
        <p>Subscribe terrysnuckers@gmail.com to 249 amazing channels!</p>
    </div>
    
    <div class="stats">
        <h2>📊 Channel Statistics</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 15px;">
            <div style="text-align: center;">
                <div style="font-size: 2em;">🎮</div>
                <div style="font-size: 1.5em; font-weight: bold;">{len(gaming_channels)}</div>
                <div>Gaming</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2em;">🎨</div>
                <div style="font-size: 1.5em; font-weight: bold;">{len(animation_channels)}</div>
                <div>Animation</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2em;">🧠</div>
                <div style="font-size: 1.5em; font-weight: bold;">{len(educational_channels)}</div>
                <div>Educational</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2em;">🎭</div>
                <div style="font-size: 1.5em; font-weight: bold;">{len(entertainment_channels)}</div>
                <div>Entertainment</div>
            </div>
        </div>
    </div>
    
    <div class="progress-container" id="progressContainer">
        <h3>🚀 Subscription Progress</h3>
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>
        <div id="progressText">0 / {len(channels)} channels subscribed</div>
        <div class="bulk-actions">
            <button class="bulk-btn" onclick="subscribeToCategory('gaming')">🎮 Subscribe All Gaming ({len(gaming_channels)})</button>
            <button class="bulk-btn" onclick="subscribeToCategory('animation')">🎨 Subscribe All Animation ({len(animation_channels)})</button>
            <button class="bulk-btn" onclick="subscribeToCategory('educational')">🧠 Subscribe All Educational ({len(educational_channels)})</button>
            <button class="bulk-btn" onclick="subscribeToCategory('entertainment')">🎭 Subscribe All Entertainment ({len(entertainment_channels)})</button>
        </div>
    </div>
"""
    
    # Add each category
    categories = [
        ("🎮 Gaming Channels", gaming_channels, "gaming"),
        ("🎨 Animation Channels", animation_channels, "animation"),
        ("🧠 Educational Channels", educational_channels, "educational"),
        ("🎭 Entertainment Channels", entertainment_channels, "entertainment")
    ]
    
    for category_name, category_channels, category_class in categories:
        if category_channels:
            html_content += f"""
    <div class="category">
        <div class="category-header {category_class}">
            {category_name} ({len(category_channels)})
        </div>
        <div class="channels-grid">
"""
            for channel in category_channels:
                subscribe_url = f"https://www.youtube.com/channel/{channel['id']}?sub_confirmation=1"
                html_content += f"""
            <div class="channel-card" data-category="{category_class}">
                <div class="channel-title">{channel['title']}</div>
                <a href="{subscribe_url}" target="_blank" class="subscribe-btn" onclick="markSubscribed(this)">
                    📺 Subscribe to {channel['title'][:20]}{'...' if len(channel['title']) > 20 else ''}
                </a>
            </div>
"""
            html_content += """
        </div>
    </div>
"""
    
    # Add JavaScript for progress tracking
    html_content += """
    <script>
        let subscribedCount = 0;
        const totalChannels = """ + str(len(channels)) + """;
        
        function markSubscribed(button) {
            if (!button.classList.contains('subscribed')) {
                button.classList.add('subscribed');
                button.style.background = 'linear-gradient(135deg, #4CAF50, #45a049)';
                button.innerHTML = '✅ Subscribed!';
                subscribedCount++;
                updateProgress();
            }
        }
        
        function updateProgress() {
            const percentage = (subscribedCount / totalChannels) * 100;
            document.getElementById('progressFill').style.width = percentage + '%';
            document.getElementById('progressText').innerHTML = 
                subscribedCount + ' / ' + totalChannels + ' channels subscribed (' + percentage.toFixed(1) + '%)';
                
            if (subscribedCount === totalChannels) {
                document.getElementById('progressText').innerHTML += ' 🎉 ALL COMPLETE!';
            }
        }
        
        function subscribeToCategory(category) {
            const cards = document.querySelectorAll(`[data-category="${category}"] .subscribe-btn`);
            let delay = 0;
            
            cards.forEach(button => {
                setTimeout(() => {
                    if (!button.classList.contains('subscribed')) {
                        window.open(button.href, '_blank');
                        markSubscribed(button);
                    }
                }, delay);
                delay += 500; // 500ms delay between opens to avoid browser popup blocking
            });
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case '1': subscribeToCategory('gaming'); break;
                    case '2': subscribeToCategory('animation'); break;
                    case '3': subscribeToCategory('educational'); break;
                    case '4': subscribeToCategory('entertainment'); break;
                }
            }
        });
    </script>
</body>
</html>
"""
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"   ❌ Error creating HTML: {e}")
        return False

def create_hybrid_system():
    """Main hybrid system creation"""
    print("🚀 CREATING HYBRID SUBSCRIPTION SYSTEM")
    print("=" * 50)
    
    # Load channels
    channels = load_channels_from_csv()
    if not channels:
        print("❌ No channels to process!")
        return False
    
    print(f"\n🎨 GENERATING STREAMLINED INTERFACE...")
    for i, channel in enumerate(channels, 1):
        show_progress_bar(i, len(channels), channel['title'], "Processing")
        time.sleep(0.01)  # Small delay for visual effect
    
    # Create HTML interface
    print(f"\n🌐 CREATING BEAUTIFUL SUBSCRIPTION INTERFACE...")
    success = create_subscription_html(channels)
    
    if success:
        print(f"✅ Created: {OUTPUT_FILE}")
        print(f"🎯 Features:")
        print(f"   • Beautiful categorized interface")
        print(f"   • Progress tracking")
        print(f"   • Bulk category subscriptions")
        print(f"   • Keyboard shortcuts (Ctrl+1-4)")
        print(f"   • Auto-opening tabs")
        
        return True
    else:
        return False

if __name__ == "__main__":
    print("🎬 CHARLES'S YOUTUBE HYBRID SUBSCRIPTION SYSTEM")
    print("   Creating streamlined manual process...")
    print("=" * 50)
    
    success = create_hybrid_system()
    
    if success:
        print(f"\n🎉 HYBRID SYSTEM READY!")
        print(f"📁 Open: {OUTPUT_FILE}")
        print(f"🔗 Sign in to terrysnuckers@gmail.com and use the interface!")
        
        # Optionally open in browser
        try:
            webbrowser.open(OUTPUT_FILE)
            print(f"🌐 Opened in default browser!")
        except:
            print(f"💡 Manually open {OUTPUT_FILE} in your browser")
    else:
        print(f"\n❌ HYBRID SYSTEM CREATION FAILED!")

