#!/usr/bin/env python3
"""
Setup automated 90-day retention cleanup for Jimmy's YouTube system
Creates cron job to run daily cleanup
"""

import subprocess
import os

def setup_cron_job():
    """Setup cron job for Jimmy's 90-day retention policy"""
    
    # Cron job to run daily at 3:00 AM
    cron_entry = "0 3 * * * /usr/bin/python3 /home/jbyrd/hatter-pai/jimmy-retention-cleanup.py cleanup --force >> /home/jbyrd/hatter-pai/jimmy-retention-cron.log 2>&1"
    
    print("🕒 Setting up Jimmy's 90-day retention cron job...")
    
    try:
        # Get current crontab
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_cron = result.stdout if result.returncode == 0 else ""
        
        # Check if our cron job already exists
        if "jimmy-retention-cleanup.py" in current_cron:
            print("✅ Jimmy's retention cron job already exists")
            return True
        
        # Add our cron job
        new_cron = current_cron.strip() + "\n" + cron_entry + "\n"
        
        # Install new crontab
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_cron)
        
        if process.returncode == 0:
            print("✅ Successfully added Jimmy's 90-day retention cron job")
            print("📅 Schedule: Daily at 3:00 AM")
            print("📋 Command: 90-day cleanup with automatic deletion")
            print("📝 Logs: /home/jbyrd/hatter-pai/jimmy-retention-cron.log")
            return True
        else:
            print("❌ Failed to install cron job")
            return False
            
    except Exception as e:
        print(f"❌ Error setting up cron job: {e}")
        return False

def test_retention_system():
    """Test that the retention system is working"""
    print("\n🧪 Testing Jimmy's retention system...")
    
    try:
        # Test the analyze command
        result = subprocess.run([
            'python3', '/home/jbyrd/hatter-pai/jimmy-retention-cleanup.py', 'status'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Retention system is working correctly")
            print(result.stdout)
            return True
        else:
            print(f"❌ Retention system test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing retention system: {e}")
        return False

def main():
    print("🎬 Jimmy's 90-Day YouTube Retention Setup")
    print("=" * 45)
    
    # Test the retention system first
    if not test_retention_system():
        print("❌ Retention system test failed - not setting up cron")
        return False
    
    # Setup cron job
    if not setup_cron_job():
        print("❌ Failed to setup automated cleanup")
        return False
    
    print("\n🎊 Jimmy's 90-day retention policy is now active!")
    print("🧹 Automatic cleanup: Daily at 3:00 AM")
    print("📊 Videos older than 90 days will be automatically removed")
    print("🔒 Protected: Recently watched & favorited videos")
    print("📝 Logs: jimmy-retention-cron.log & jimmy-retention.log")
    
    return True

if __name__ == "__main__":
    main()
