# Manual YouTube Automation Deployment Steps

## 🚀 Charles YouTube Plex Automation - Manual Setup

**Issue**: SSH interactive sessions get stuck on password prompts
**Solution**: Manual deployment steps for Plex server (192.168.1.17)

## ✅ Already Completed
- ✅ All YouTube automation scripts deployed to 192.168.1.17
- ✅ Files copied to `/home/jbyrd/.local/bin/` and contexts
- ✅ Scripts are executable and PATH-ready
- ✅ 37GB+ of YouTube content already in Plex

## 🔧 Remaining Manual Steps

### Step 1: SSH to Plex Server
```bash
ssh jbyrd@192.168.1.17
```

### Step 2: Install Dependencies
```bash
sudo apt update
sudo apt install -y sqlite3 jq curl python3-pip
pip3 install --user yt-dlp
```

### Step 3: Initialize Database
```bash
export PATH=$PATH:$HOME/.local/bin
pai-youtube-subscription-sync setup
```

### Step 4: Test System
```bash
pai-youtube-subscription-sync status
pai-youtube-retention-cleanup status
```

### Step 5: Setup Automation
```bash
pai-youtube-setup-automation --setup-cron --start-now
```

## 🎯 What This Automation Provides

### ✨ Beautiful Visual Features
- **Stunning Progress Bars**: Unicode animations with rainbow colors
- **Elegant Headers**: Box-drawing characters with emojis
- **Real-time Status**: Live updates for all operations
- **Color-Coded Results**: Green/red/yellow status indicators

### 🔄 Automated Workflows
- **Subscription Monitoring**: Check every 3 hours for new videos
- **Auto-Downloads**: Download latest videos from cebyrdlegomaster@gmail.com subscriptions
- **30-Day Retention**: Automatically remove old videos to save space
- **New Channel Detection**: Auto-configure when Charles subscribes to new channels
- **Plex Integration**: Automatic library refreshes after changes

### 📊 Storage Management
- **Storage Location**: `/mnt/nfs_share/charles/youtube/`
- **Quality**: 720p MP4 (optimized for Plex)
- **Organization**: By channel: `/YouTube/[Channel Name]/YYYY-MM-DD - Title.mp4`
- **Space Monitoring**: Automated cleanup when storage is full

## 🎬 Current Content Status
- ✅ **37GB+ YouTube videos** already in Plex
- ✅ **Recent content** from October-December 2024
- ✅ **Popular channels**: Ninjago, Nintendo, Tech, Gaming, MLP, etc.
- ✅ **Well organized** in subdirectories by channel

## 💡 Alternative: Use Current Setup

**Option**: Keep using the existing YouTube content without automation
- Current videos are already working perfectly in Plex
- Manual downloads can continue as-is
- Automation can be added later when convenient

## 🚨 If Issues Occur

### Database Issues
```bash
# Reset database if needed
rm ~/.config/pai/youtube/subscriptions.db
pai-youtube-subscription-sync setup
```

### Permission Issues
```bash
# Fix permissions
chmod +x ~/.local/bin/pai-youtube-*
sudo chown -R jbyrd:jbyrd /mnt/nfs_share/charles/youtube/
```

### Cron Issues
```bash
# Check cron jobs
crontab -l | grep pai-youtube

# Remove if needed
crontab -e  # Delete pai-youtube lines
```

## 📞 Support Commands

```bash
# System status
pai-youtube-subscription-sync status

# Storage analysis  
pai-youtube-retention-cleanup analyze

# Manual sync
pai-youtube-subscription-sync sync --dry-run

# Test progress bars
pai-youtube-progress-bar
```

---

*Manual Deployment Guide - Charles YouTube Plex Automation*  
*Priority #1: Visually Stunning Automation with 30-day Retention*

