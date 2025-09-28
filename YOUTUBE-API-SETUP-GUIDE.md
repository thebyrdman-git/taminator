# YouTube API Setup for Charles's Account (cebyrdlegomaster@gmail.com)

## 🎯 Goal: Full Automation with Real-Time Subscription Monitoring

This will enable our beautiful automation system to:
- ✅ **Auto-detect** when Charles subscribes to new channels
- ✅ **Real-time** access to his subscription list
- ✅ **Latest videos** from all his subscribed channels
- ✅ **Channel metadata** for proper organization

## 📋 Step-by-Step Setup Process

### **Phase 1: Google Cloud Console Setup**

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with **your Google account** (not Charles's - you'll be the admin)

2. **Create New Project**
   - Click "Select a project" → "New Project"
   - Project name: `Charles YouTube Automation`
   - Click "Create"

3. **Enable YouTube Data API v3**
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click on it → Click "Enable"

### **Phase 2: API Credentials Setup**

4. **Create API Key**
   - Go to "APIs & Services" → "Credentials"
   - Click "+ Create Credentials" → "API Key"
   - **Copy the API key** - we'll need this!
   - Click "Restrict Key" for security

5. **Restrict API Key**
   - Application restrictions: "IP addresses"
   - Add: `192.168.1.17` (Plex server IP)
   - API restrictions: "YouTube Data API v3"
   - Click "Save"

### **Phase 3: OAuth Setup for Charles's Account**

6. **Configure OAuth Consent Screen**
   - Go to "APIs & Services" → "OAuth consent screen"
   - User Type: "External" → Click "Create"
   - App name: `Charles YouTube Automation`
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue"

7. **Add Scopes**
   - Click "Add or Remove Scopes"
   - Add: `https://www.googleapis.com/auth/youtube.readonly`
   - Click "Update" → "Save and Continue"

8. **Add Charles as Test User**
   - In "Test users" section
   - Click "+ Add Users"
   - Add: `cebyrdlegomaster@gmail.com`
   - Click "Save and Continue"

9. **Create OAuth Client**
   - Go to "Credentials" → "+ Create Credentials" → "OAuth client ID"
   - Application type: "Desktop application"
   - Name: `Charles YouTube Client`
   - Click "Create"
   - **Download the JSON file** - we'll need this!

### **Phase 4: Authentication with Charles's Account**

10. **Authenticate Charles's Account**
    ```bash
    # We'll run this on the Plex server
    ssh jbyrd@192.168.1.17
    pip3 install --user google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    
    # Upload the OAuth JSON file and authenticate
    # This will open a browser for Charles to log in and authorize
    ```

### **Phase 5: Update Automation Scripts**

11. **Configure API Access**
    - Upload API key and OAuth credentials to Plex server
    - Update `pai-youtube-subscription-sync` to use real API
    - Test with Charles's actual subscription list

## 🔐 Security Configuration

### **API Key Restrictions**
```
IP Restrictions: 192.168.1.17 (Plex server only)
API Restrictions: YouTube Data API v3 only
Quota: 10,000 requests/day (more than enough)
```

### **OAuth Permissions** 
```
Scope: youtube.readonly (read-only access)
Account: cebyrdlegomaster@gmail.com only
Environment: Test (for family use)
```

## 📊 Expected Quotas & Limits

- **Daily Quota**: 10,000 units (generous for personal use)
- **Subscription List**: ~1 unit per request (once per hour)
- **Video Search**: ~100 units per channel (every few hours)
- **Total Usage**: ~500-1000 units/day (well within limits)

## 🎬 What This Enables

### **Real-Time Automation**
```
✅ Detect new subscriptions automatically
✅ Get latest videos from all channels  
✅ Full channel metadata (thumbnails, descriptions)
✅ Upload schedules and channel statistics
✅ Playlist and series detection
```

### **Beautiful Progress Tracking**
```
🔄 Checking 127 subscribed channels...
📥 Found 23 new videos from last 24 hours
✨ Downloading: "Latest Ninjago Episode" from TommyAndrea
████████████████████████████████ 100% Complete
✅ All channels processed - 23 videos added to Plex
```

## 🚀 Next Steps After API Setup

1. **Test API Access**: Verify we can read Charles's subscriptions
2. **Update Scripts**: Replace mock data with real API calls  
3. **Deploy to Plex**: Full automation with beautiful progress bars
4. **Schedule Automation**: Hourly checks for new content
5. **Monitor & Enjoy**: Charles gets latest videos automatically

## 📞 Support Notes

- **Family-Safe**: Read-only access, no posting/commenting abilities
- **Privacy**: Only accesses public subscription data
- **Control**: You maintain full admin control over the project
- **Monitoring**: Full logging of all API requests and downloads

---

*Ready to set up? Let's start with Phase 1: Google Cloud Console!*

