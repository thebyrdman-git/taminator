#!/usr/bin/env python3
"""
Organize existing Charles YouTube videos into category folders
"""

import os
import shutil
import glob

# Channel categorization mapping from our earlier work
CHANNEL_CATEGORIES = {
    'Gaming-Minecraft': [
        'Minecraft', 'Knarfy', 'SystemZee', 'Grazzy', 'TrixyBlox', 
        'Element Animation', 'MorePainful', 'Fundy', 'Dream', 'Technoblade',
        'Hermitcraft', 'MumboJumbo', 'Grian', 'GoodTimesWithScar'
    ],
    'Gaming-Console': [
        'Arlo', 'Nin10doland', 'HMK', 'KnightPohtaytoe', 'Alpharad', 
        'Alpharad LIVE', 'Nintendo', 'PlayStation', 'Xbox', 'GameXplain',
        'Scott The Woz', 'RelaxAlax'
    ],
    'Gaming-Official': [
        'PlayStation', 'Ubisoft', 'Epic Games', 'Rockstar Games', 
        'Square Enix', 'Nintendo', 'Xbox', 'Blizzard Entertainment',
        'EA', 'Activision', 'Bethesda', 'Steam'
    ],
    'Animation': [
        'TheOdd2sOut', 'Haminations', 'Element Animation', 'Chikn Nuggit',
        'Jaiden Animations', 'SomethingElseYT', 'TimTom', 'Let Me Explain Studios',
        'Domics', 'CircleToonsHD'
    ],
    'Comedy': [
        'Steven He Shorts', 'Ice Cream SHORT', 'Ryan HD', 'Laugh Over Life',
        'Memenade', 'Dankpods', 'Drew Gooden', 'Danny Gonzalez',
        'Kurtis Conner', 'CallMeKevin'
    ],
    'Educational': [
        'The Film Theorists', 'Game Theory', 'Food Theory', 'Style Theory',
        'HamaSamaKun', 'instructor_bensei', 'Primitive Technology',
        'Veritasium', 'VSauce', 'Kurzgesagt', 'SciShow'
    ],
    'Pokemon-TCG': [
        'ShortPocketMonster', 'LegendaryPokeman', 'Pokémon TV', 
        'The Official Pokémon YouTube channel', 'PokeRev', 'MaxMoeFoe',
        'UnlistedLeaf', 'TCA Gaming'
    ],
    'Entertainment': [
        'Star Wars Theory', 'DuckBricks', 'Vivilly', 'Austin Sweatt',
        'Captain Kidd', 'Ashnflash', 'Danno Cal Drawings'
    ]
}

def get_category_for_channel(channel_name):
    """Return category for a given channel name"""
    for category, channels in CHANNEL_CATEGORIES.items():
        if channel_name in channels:
            return category
    return 'Misc'  # Default category for unmapped channels

def extract_channel_from_filename(filename):
    """Extract channel name from video filename format: YYYYMMDD - Channel - Title.mp4"""
    base = os.path.basename(filename)
    if ' - ' in base:
        parts = base.split(' - ')
        if len(parts) >= 3:
            return parts[1].strip()  # Channel is the second part
    return None

def organize_videos(source_dir="/media/charles/youtube"):
    """Organize videos into category folders"""
    video_files = glob.glob(os.path.join(source_dir, "*.mp4"))
    
    moves = []
    for video_file in video_files:
        filename = os.path.basename(video_file)
        
        # Skip test files
        if any(test in filename for test in ['TEST', 'SINGLE-VIDEO', 'PRODUCTION']):
            print(f"⏭️  SKIPPING: {filename}")
            continue
            
        channel = extract_channel_from_filename(video_file)
        if channel:
            category = get_category_for_channel(channel)
            category_dir = os.path.join(source_dir, category)
            
            # Ensure category directory exists
            os.makedirs(category_dir, exist_ok=True)
            
            target_path = os.path.join(category_dir, filename)
            moves.append((video_file, target_path, channel, category))
        else:
            print(f"❓ UNKNOWN FORMAT: {filename}")
    
    return moves

if __name__ == "__main__":
    print("🎬 Charles YouTube Video Organization")
    print("=" * 50)
    
    moves = organize_videos()
    
    print(f"\n📋 ORGANIZATION PLAN:")
    for src, dst, channel, category in moves:
        print(f"📁 {category}: {channel} - {os.path.basename(src)}")
    
    print(f"\n📊 SUMMARY:")
    categories = {}
    for _, _, channel, category in moves:
        categories[category] = categories.get(category, 0) + 1
    
    for category, count in sorted(categories.items()):
        print(f"   {category}: {count} videos")
    
    print(f"\nTotal videos to organize: {len(moves)}")
