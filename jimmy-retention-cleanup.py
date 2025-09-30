#!/usr/bin/env python3
"""
Jimmy's 90-Day YouTube Retention Policy
Automatically removes videos older than 90 days from Jimmy's YouTube system
"""

import os
import sqlite3
import time
from datetime import datetime, timedelta
import subprocess
import logging
import glob

# Configuration for Jimmy's system
JIMMY_YOUTUBE_DIR = "/mnt/nfs_share/jimmy/youtube"
JIMMY_DATABASE_PATH = "/home/jbyrd/hatter-pai/jimmy_youtube_automation.db"
RETENTION_DAYS = 90
LOG_FILE = "/home/jbyrd/hatter-pai/jimmy-retention.log"

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

def get_storage_info():
    """Get storage information for Jimmy's YouTube directory"""
    if not os.path.exists(JIMMY_YOUTUBE_DIR):
        return "Directory not found"
    
    try:
        result = subprocess.run(['df', '-h', JIMMY_YOUTUBE_DIR], 
                              capture_output=True, text=True)
        return result.stdout.strip().split('\n')[-1]
    except Exception as e:
        return f"Error getting storage info: {e}"

def find_old_videos(retention_days=RETENTION_DAYS):
    """Find video files older than retention_days"""
    if not os.path.exists(JIMMY_YOUTUBE_DIR):
        logger.warning(f"YouTube directory does not exist: {JIMMY_YOUTUBE_DIR}")
        return []
    
    cutoff_time = time.time() - (retention_days * 24 * 60 * 60)
    old_videos = []
    
    # Find all video files in Jimmy's YouTube directory
    for root, dirs, files in os.walk(JIMMY_YOUTUBE_DIR):
        for file in files:
            if file.lower().endswith(('.mp4', '.mkv', '.webm', '.avi')):
                file_path = os.path.join(root, file)
                try:
                    # Check modification time
                    if os.path.getmtime(file_path) < cutoff_time:
                        old_videos.append(file_path)
                except OSError:
                    continue
    
    return old_videos

def is_video_protected(video_path):
    """Check if a video should be protected from deletion"""
    # Check if recently accessed (within 7 days)
    try:
        access_time = os.path.getatime(video_path)
        seven_days_ago = time.time() - (7 * 24 * 60 * 60)
        
        if access_time > seven_days_ago:
            return True, "Recently accessed"
    except OSError:
        pass
    
    # Check database for any special status
    try:
        conn = sqlite3.connect(JIMMY_DATABASE_PATH)
        cursor = conn.cursor()
        
        filename = os.path.basename(video_path)
        cursor.execute('''
            SELECT status FROM jimmy_downloads 
            WHERE file_path LIKE ? OR video_title LIKE ?
        ''', (f'%{filename}%', f'%{filename}%'))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == 'favorite':
            return True, "Marked as favorite"
            
    except Exception as e:
        logger.debug(f"Database check failed: {e}")
    
    return False, "Not protected"

def analyze_cleanup(retention_days=RETENTION_DAYS):
    """Analyze what would be cleaned up without deleting"""
    logger.info(f"🔍 Analyzing Jimmy's {retention_days}-day retention policy...")
    
    old_videos = find_old_videos(retention_days)
    
    if not old_videos:
        logger.info(f"✅ No videos found older than {retention_days} days")
        return {"total_videos": 0, "deletable_videos": 0, "protected_videos": 0, "space_recoverable": 0}
    
    total_size = 0
    protected_count = 0
    deletable_count = 0
    protected_size = 0
    deletable_size = 0
    
    category_stats = {}
    
    print(f"\n📊 JIMMY'S {retention_days}-DAY RETENTION ANALYSIS")
    print("=" * 50)
    print(f"Retention period: {retention_days} days")
    print(f"Videos found: {len(old_videos)}")
    print()
    
    for video in old_videos:
        try:
            size = os.path.getsize(video)
            total_size += size
            
            # Get category from path
            category = os.path.basename(os.path.dirname(video))
            if category not in category_stats:
                category_stats[category] = {"count": 0, "size": 0}
            
            protected, reason = is_video_protected(video)
            
            if protected:
                protected_count += 1
                protected_size += size
                print(f"  🔒 PROTECTED: {os.path.basename(video)} ({reason})")
            else:
                deletable_count += 1
                deletable_size += size
                category_stats[category]["count"] += 1
                category_stats[category]["size"] += size
                
        except OSError:
            continue
    
    print()
    print("📈 Summary:")
    print(f"  Total videos: {len(old_videos)}")
    print(f"  Protected: {protected_count} ({format_bytes(protected_size)})")
    print(f"  Can delete: {deletable_count} ({format_bytes(deletable_size)})")
    print(f"  Space recoverable: {format_bytes(deletable_size)}")
    
    if category_stats:
        print()
        print("📁 Deletable videos by category:")
        for category, stats in category_stats.items():
            print(f"  🎬 Jimmy Youtube {category}: {stats['count']} videos ({format_bytes(stats['size'])})")
    
    return {
        "total_videos": len(old_videos),
        "deletable_videos": deletable_count,
        "protected_videos": protected_count,
        "space_recoverable": deletable_size
    }

def perform_cleanup(retention_days=RETENTION_DAYS, dry_run=False, force=False):
    """Perform the actual cleanup"""
    logger.info(f"🧹 Starting Jimmy's {retention_days}-day cleanup (dry_run={dry_run})")
    
    old_videos = find_old_videos(retention_days)
    
    if not old_videos:
        logger.info(f"✅ No videos found older than {retention_days} days")
        return {"deleted_count": 0, "space_freed": 0}
    
    # Build list of deletable videos
    deletable_videos = []
    total_size = 0
    
    for video in old_videos:
        protected, reason = is_video_protected(video)
        if not protected:
            try:
                size = os.path.getsize(video)
                deletable_videos.append((video, size))
                total_size += size
            except OSError:
                continue
    
    if not deletable_videos:
        logger.info("✅ No deletable videos found (all are protected)")
        return {"deleted_count": 0, "space_freed": 0}
    
    logger.info(f"Found {len(deletable_videos)} videos to delete ({format_bytes(total_size)})")
    
    # Confirmation prompt
    if not force and not dry_run:
        response = input(f"\n⚠️  Delete {len(deletable_videos)} videos ({format_bytes(total_size)})? (y/N): ")
        if response.lower() != 'y':
            logger.info("Cleanup cancelled by user")
            return {"deleted_count": 0, "space_freed": 0}
    
    # Delete videos
    deleted_count = 0
    space_freed = 0
    
    for i, (video, size) in enumerate(deletable_videos, 1):
        video_name = os.path.basename(video)
        category = os.path.basename(os.path.dirname(video))
        
        print(f"🔄 [{i}/{len(deletable_videos)}] Processing {category}: {video_name}")
        
        if dry_run:
            logger.info(f"DRY RUN: Would delete {video}")
            continue
        
        try:
            # Delete associated files (thumbnails, etc.)
            base_path = os.path.splitext(video)[0]
            for pattern in [f"{base_path}.*", f"{video}.*"]:
                for assoc_file in glob.glob(pattern):
                    if assoc_file != video and os.path.isfile(assoc_file):
                        os.remove(assoc_file)
                        logger.debug(f"Removed associated file: {assoc_file}")
            
            # Delete main video file
            os.remove(video)
            deleted_count += 1
            space_freed += size
            
            logger.info(f"✅ Deleted: {video_name} ({format_bytes(size)})")
            
        except OSError as e:
            logger.error(f"❌ Failed to delete {video}: {e}")
    
    # Clean up empty directories
    if not dry_run:
        try:
            for root, dirs, files in os.walk(JIMMY_YOUTUBE_DIR, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        if not os.listdir(dir_path):  # Empty directory
                            os.rmdir(dir_path)
                            logger.debug(f"Removed empty directory: {dir_path}")
                    except OSError:
                        pass
        except Exception as e:
            logger.debug(f"Error cleaning empty directories: {e}")
    
    # Update database
    if not dry_run:
        try:
            conn = sqlite3.connect(JIMMY_DATABASE_PATH)
            cursor = conn.cursor()
            
            # Log cleanup event
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jimmy_cleanup_log (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    retention_days INTEGER,
                    deleted_count INTEGER,
                    space_freed INTEGER,
                    type TEXT
                )
            ''')
            
            cursor.execute('''
                INSERT INTO jimmy_cleanup_log (retention_days, deleted_count, space_freed, type)
                VALUES (?, ?, ?, ?)
            ''', (retention_days, deleted_count, space_freed, "manual" if force else "automated"))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to update database: {e}")
    
    logger.info(f"🎊 Cleanup completed: {deleted_count} videos deleted, {format_bytes(space_freed)} recovered")
    
    return {"deleted_count": deleted_count, "space_freed": space_freed}

def show_status():
    """Show current retention status"""
    print("🧹 JIMMY'S 90-DAY RETENTION STATUS")
    print("=" * 40)
    print()
    
    print("💾 Storage Information:")
    storage_info = get_storage_info()
    print(f"  {storage_info}")
    
    # Get retention analysis
    analysis = analyze_cleanup(RETENTION_DAYS)
    print()
    print(f"📊 {RETENTION_DAYS}-Day Retention Status:")
    print(f"  Videos older than {RETENTION_DAYS} days: {analysis['total_videos']}")
    print(f"  Space recoverable: {format_bytes(analysis['space_recoverable'])}")
    
    # Show last cleanup
    try:
        conn = sqlite3.connect(JIMMY_DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, deleted_count, space_freed FROM jimmy_cleanup_log 
            ORDER BY timestamp DESC LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"  Last cleanup: {result[0]} ({result[1]} videos, {format_bytes(result[2])})")
        else:
            print("  Last cleanup: Never")
            
    except Exception:
        print("  Last cleanup: Unknown")

def format_bytes(bytes):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} PB"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Jimmy's 90-Day YouTube Retention Manager")
    parser.add_argument('command', choices=['analyze', 'cleanup', 'status'], 
                      help='Command to execute')
    parser.add_argument('--retention-days', type=int, default=RETENTION_DAYS,
                      help=f'Days to retain videos (default: {RETENTION_DAYS})')
    parser.add_argument('--dry-run', action='store_true',
                      help='Show what would be deleted without deleting')
    parser.add_argument('--force', action='store_true',
                      help='Skip confirmation prompts')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyze_cleanup(args.retention_days)
    elif args.command == 'cleanup':
        perform_cleanup(args.retention_days, args.dry_run, args.force)
    elif args.command == 'status':
        show_status()

if __name__ == "__main__":
    main()
