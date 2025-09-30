#!/usr/bin/env python3
"""
Update Jimmy's subscriptions with complete Google Takeout data
Better categorization based on his actual interests
"""

import sqlite3
import csv
import os

# Configuration
JIMMY_DATABASE_PATH = "/home/jbyrd/hatter-pai/jimmy_youtube_automation.db"
TAKEOUT_CSV = "/home/jbyrd/hatter-pai/jimmy-takeout-subscriptions.csv"

def categorize_jimmy_channel(channel_name):
    """Categorize Jimmy's channels based on his actual interests from Takeout"""
    name_lower = channel_name.lower()
    
    # Music & Entertainment
    if any(term in name_lower for term in [
        'plini', 'vulf', 'charles', 'colby', 'drums', 'bass', 'groove', 'music'
    ]):
        return 'Music'
    
    # Faith & Christian Content  
    elif any(term in name_lower for term in [
        'chosen', 'theocast', 'reformed', 'bless', 'god', 'christian'
    ]):
        return 'Faith'
    
    # Sports & Fitness
    elif any(term in name_lower for term in [
        'braves', 'mlb', 'crossfit', 'games', 'atlanta', 'sport'
    ]):
        return 'Sports'
    
    # Technology & Professional
    elif any(term in name_lower for term in [
        'ansible', 'luca', 'berton', 'tech', 'devops', 'linux', 'automation'
    ]):
        return 'Tech-Professional'
    
    # Science & Space
    elif any(term in name_lower for term in [
        'spacex', 'nasa', 'space', 'science', 'elon'
    ]):
        return 'Science-Space'
    
    # Education & Learning
    elif any(term in name_lower for term in [
        'language', 'learn', 'education', 'school', 'student', 'tutorial'
    ]):
        return 'Education'
    
    # Personal & Family
    elif any(term in name_lower for term in [
        'byrd', 'family', 'personal'
    ]):
        return 'Personal-Family'
    
    # Default category for everything else
    else:
        return 'General-Interest'

def update_jimmy_database():
    """Update Jimmy's database with complete Takeout subscriptions"""
    
    # Add Description column to jimmy-takeout-subscriptions.csv
    print("🔧 Processing Takeout subscriptions...")
    
    # Read takeout CSV and add descriptions  
    updated_subscriptions = []
    with open(TAKEOUT_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Add empty description for Takeout format
            subscription = {
                'Channel Id': row['Channel Id'],
                'Channel Title': row['Channel Title'], 
                'Channel Url': row['Channel Url'],
                'Description': ''  # Takeout doesn't include descriptions
            }
            updated_subscriptions.append(subscription)
    
    # Save updated CSV
    updated_csv_path = "/home/jbyrd/hatter-pai/jimmy-subscriptions-complete.csv"
    with open(updated_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Channel Id', 'Channel Url', 'Channel Title', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_subscriptions)
    
    print(f"✅ Created complete subscription file: {updated_csv_path}")
    
    # Update database
    conn = sqlite3.connect(JIMMY_DATABASE_PATH)
    cursor = conn.cursor()
    
    # Clear existing channels
    cursor.execute('DELETE FROM jimmy_channels')
    print("🗑️  Cleared old subscription data")
    
    # Load complete subscriptions
    with open(updated_csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            channel_name = row['Channel Title']
            category = categorize_jimmy_channel(channel_name)
            
            cursor.execute('''
                INSERT INTO jimmy_channels (name, channel_id, url, category)
                VALUES (?, ?, ?, ?)
            ''', (channel_name, row['Channel Id'], row['Channel Url'], category))
    
    conn.commit()
    
    # Show updated stats
    print("\n🎬 Jimmy's Complete YouTube Subscriptions (Google Takeout)")
    print("=" * 60)
    
    categories = cursor.execute('''
        SELECT category, COUNT(*) as count 
        FROM jimmy_channels 
        GROUP BY category 
        ORDER BY count DESC
    ''').fetchall()
    
    total_channels = cursor.execute('SELECT COUNT(*) FROM jimmy_channels').fetchone()[0]
    
    print(f"📺 Total Channels: {total_channels}")
    print("\n📊 Categories:")
    for category, count in categories:
        print(f"   • {category}: {count} channels")
    
    print(f"\n📂 Jimmy Youtube Plex Libraries:")
    for category, count in categories:
        print(f"   🎬 Jimmy Youtube {category}")
    
    conn.close()
    
    print(f"\n✅ Database updated with {total_channels} complete subscriptions!")
    return total_channels

if __name__ == "__main__":
    if not os.path.exists(TAKEOUT_CSV):
        print(f"❌ Takeout CSV not found: {TAKEOUT_CSV}")
        exit(1)
    
    total = update_jimmy_database()
    print(f"\n🎊 Jimmy's YouTube system now has his complete {total} subscriptions!")
