#!/usr/bin/env python3
"""
Execute the Charles YouTube video organization
"""

import os
import shutil
import glob

# Same categorization as before
CHANNEL_CATEGORIES = {
    'Gaming-Minecraft': [
        'Minecraft', 'Knarfy', 'SystemZee', 'Grazzy', 'TrixyBlox', 
        'Element Animation', 'MorePainful', 'Fundy', 'Dream', 'Technoblade'
    ],
    'Gaming-Console': [
        'Arlo', 'Nin10doland', 'HMK', 'KnightPohtaytoe', 'Alpharad', 
        'Alpharad LIVE', 'Nintendo', 'PlayStation', 'Xbox'
    ],
    'Gaming-Official': [
        'PlayStation', 'Ubisoft', 'Epic Games', 'Rockstar Games', 
        'Square Enix', 'Nintendo', 'Xbox'
    ],
    'Animation': [
        'TheOdd2sOut', 'Haminations', 'Element Animation', 'Chikn Nuggit',
        'Jaiden Animations', 'SomethingElseYT'
    ],
    'Comedy': [
        'Steven He Shorts', 'Ice Cream SHORT', 'Ryan HD', 'Laugh Over Life',
        'Memenade', 'Dankpods'
    ],
    'Educational': [
        'The Film Theorists', 'Game Theory', 'Food Theory', 'Style Theory',
        'HamaSamaKun', 'instructor_bensei', 'Primitive Technology'
    ],
    'Pokemon-TCG': [
        'ShortPocketMonster', 'LegendaryPokeman', 'Pokémon TV', 
        'PokeRev', 'MaxMoeFoe'
    ],
    'Entertainment': [
        'Star Wars Theory', 'DuckBricks', 'Vivilly', 'Austin Sweatt',
        'Captain Kidd', 'Ashnflash'
    ]
}

def get_category_for_channel(channel_name):
    for category, channels in CHANNEL_CATEGORIES.items():
        if channel_name in channels:
            return category
    return 'Misc'

def extract_channel_from_filename(filename):
    base = os.path.basename(filename)
    if ' - ' in base:
        parts = base.split(' - ')
        if len(parts) >= 3:
            return parts[1].strip()
    return None

def execute_organization(source_dir="/media/charles/youtube", dry_run=True):
    video_files = glob.glob(os.path.join(source_dir, "*.mp4"))
    
    success_count = 0
    for video_file in video_files:
        filename = os.path.basename(video_file)
        
        # Skip test files
        if any(test in filename for test in ['TEST', 'SINGLE-VIDEO', 'PRODUCTION']):
            continue
            
        channel = extract_channel_from_filename(video_file)
        if channel:
            category = get_category_for_channel(channel)
            category_dir = os.path.join(source_dir, category)
            
            # Ensure category directory exists
            os.makedirs(category_dir, exist_ok=True)
            
            target_path = os.path.join(category_dir, filename)
            
            if dry_run:
                print(f"WOULD MOVE: {filename} → {category}/")
            else:
                try:
                    shutil.move(video_file, target_path)
                    print(f"✅ MOVED: {filename} → {category}/")
                    success_count += 1
                except Exception as e:
                    print(f"❌ ERROR moving {filename}: {e}")
    
    return success_count

if __name__ == "__main__":
    import sys
    dry_run = "--execute" not in sys.argv
    
    if dry_run:
        print("🎬 DRY RUN - Video Organization Preview")
        print("=" * 50)
        execute_organization(dry_run=True)
        print("\nAdd --execute to actually move the files")
    else:
        print("🎬 EXECUTING Video Organization")
        print("=" * 50)
        count = execute_organization(dry_run=False)
        print(f"\n✅ Successfully organized {count} videos!")
