#!/usr/bin/env python3
"""
Charles YouTube Channel Categorization System
Organizes 249+ subscriptions into logical Plex categories
"""

# Channel categorization mapping
CHANNEL_CATEGORIES = {
    # 🎮 MINECRAFT CONTENT
    'Gaming-Minecraft': [
        'Minecraft', 'Knarfy', 'SystemZee', 'Grazzy', 'TrixyBlox', 
        'Element Animation', 'MorePainful', 'Fundy', 'Dream', 'Technoblade',
        'Hermitcraft', 'MumboJumbo', 'Grian', 'GoodTimesWithScar'
    ],
    
    # 🎯 NINTENDO & CONSOLE GAMING  
    'Gaming-Console': [
        'Arlo', 'Nin10doland', 'HMK', 'KnightPohtaytoe', 'Alpharad', 
        'Alpharad LIVE', 'Nintendo', 'PlayStation', 'Xbox', 'GameXplain',
        'Scott The Woz', 'RelaxAlax'
    ],
    
    # 🏢 GAMING COMPANIES & OFFICIAL
    'Gaming-Official': [
        'PlayStation', 'Ubisoft', 'Epic Games', 'Rockstar Games', 
        'Square Enix', 'Nintendo', 'Xbox', 'Blizzard Entertainment',
        'EA', 'Activision', 'Bethesda', 'Steam'
    ],
    
    # 🎬 ANIMATION & STORYTELLING
    'Animation': [
        'TheOdd2sOut', 'Haminations', 'Element Animation', 'Chikn Nuggit',
        'Jaiden Animations', 'SomethingElseYT', 'TimTom', 'Let Me Explain Studios',
        'Domics', 'CircleToonsHD'
    ],
    
    # 😂 COMEDY & ENTERTAINMENT  
    'Comedy': [
        'Steven He Shorts', 'Ice Cream SHORT', 'Ryan HD', 'Laugh Over Life',
        'Memenade', 'Dankpods', 'Drew Gooden', 'Danny Gonzalez',
        'Kurtis Conner', 'CallMeKevin'
    ],
    
    # 🧠 EDUCATIONAL & THEORY
    'Educational': [
        'The Film Theorists', 'Game Theory', 'Food Theory', 'Style Theory',
        'HamaSamaKun', 'instructor_bensei', 'Primitive Technology',
        'Veritasium', 'VSauce', 'Kurzgesagt', 'SciShow'
    ],
    
    # 🎴 POKEMON & TRADING CARDS
    'Pokemon-TCG': [
        'ShortPocketMonster', 'LegendaryPokeman', 'Pokémon TV', 
        'The Official Pokémon YouTube channel', 'PokeRev', 'MaxMoeFoe',
        'UnlistedLeaf', 'TCA Gaming'
    ],
    
    # 🎥 ENTERTAINMENT & MEDIA
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

def create_folder_structure():
    """Create the folder structure for organized downloads"""
    import os
    base_path = "/media/charles/youtube"
    
    categories = list(CHANNEL_CATEGORIES.keys()) + ['Misc']
    
    for category in categories:
        folder_path = os.path.join(base_path, category)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created: {folder_path}")

if __name__ == "__main__":
    print("Charles YouTube Channel Categories:")
    print("=" * 50)
    
    for category, channels in CHANNEL_CATEGORIES.items():
        print(f"\n📁 {category.upper()}: ({len(channels)} channels)")
        for channel in channels[:5]:  # Show first 5
            print(f"   • {channel}")
        if len(channels) > 5:
            print(f"   ... and {len(channels) - 5} more")
    
    print(f"\n📊 TOTAL: {sum(len(channels) for channels in CHANNEL_CATEGORIES.values())} mapped channels")
    print(f"🎯 CATEGORIES: {len(CHANNEL_CATEGORIES)} categories")
