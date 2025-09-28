# 🎬 Charles's YouTube Web Automation System

A complete web-based YouTube download and management system with real-time progress monitoring, subscription management, and Plex integration.

## ✨ Features

### 📊 Real-time Dashboard
- Live progress monitoring with animated progress bars
- Channel status tracking (completed, downloading, pending, error)
- Download statistics and system health metrics
- Beautiful glass-morphism design with gradient backgrounds

### 📺 Subscription Management
- Manage 249 YouTube channels from CSV import
- Advanced filtering and sorting capabilities  
- Paginated view with search functionality
- Export capabilities for data backup

### ⬇️ Download Controller
- Start/stop/pause download operations
- Configurable video quality and concurrent downloads
- Real-time download queue management
- Automatic retry for failed downloads

### ⚙️ Settings & Configuration
- System-wide configuration management
- Automated scheduling for downloads and cleanup
- Storage path and Plex server configuration
- Advanced debugging and telemetry options

### 🎬 Plex Integration
- Automatic library refresh after downloads
- Proper file organization and naming
- 30-day retention policy management
- Storage monitoring and cleanup

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Configuration**:
   - Place `charles-subscriptions-complete.csv` in the project root
   - Ensure storage directory `/mnt/nfs_share/charles/youtube/` exists
   - Configure Plex server settings in Settings page

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access Web Interface**:
   - Open browser to `http://localhost:5000`
   - Navigate through Dashboard, Subscriptions, Downloads, and Settings

## 📁 Project Structure

```
web-youtube-system/
├── app.py                 # Flask application server
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    ├── base.html         # Base template with navigation
    ├── dashboard.html    # Main dashboard with real-time stats
    ├── subscriptions.html # Channel management interface
    ├── downloads.html    # Download control center
    └── settings.html     # System configuration
```

## 🔧 Technical Details

### Backend (Flask + SQLite)
- **Flask**: Web framework for API endpoints and page serving
- **SQLite**: Database for tracking channels, downloads, and metadata  
- **yt-dlp**: YouTube video downloading engine
- **Threading**: Background processing for downloads

### Frontend (Tailwind + Vanilla JS)
- **Tailwind CSS**: Utility-first CSS framework
- **Glass-morphism**: Modern UI design with backdrop blur effects
- **Real-time Updates**: Auto-refreshing progress and status
- **Responsive Design**: Mobile-first approach with grid layouts

### API Endpoints
- `GET /api/status` - Current download status
- `GET /api/channels` - All channels with metadata
- `POST /api/start_downloads` - Start bulk downloads
- `POST /api/stop_downloads` - Stop active downloads
- `POST /api/refresh_plex` - Trigger Plex library refresh
- `POST /api/cleanup` - Run 30-day retention cleanup

## 🎯 Visual Design Features

### Progress Bars
- Animated shimmer effects
- Color-coded status indicators
- Real-time width transitions
- Custom gradient backgrounds

### Card Components
- Hover animations with transform effects
- Glass-morphism backgrounds
- Color-coded borders for status
- Shadow depth for visual hierarchy

### Navigation
- Sticky header with blur backdrop
- Active state highlighting
- Mobile-responsive hamburger menu
- Smooth transition animations

## 🔮 Future Enhancements

- [ ] Channel-specific download controls
- [ ] Video preview and selection
- [ ] Advanced filtering by upload date/views
- [ ] Integration with YouTube Data API
- [ ] Multi-user support with authentication
- [ ] Webhook notifications for completed downloads
- [ ] Advanced analytics and reporting
- [ ] Mobile app companion

## 🏗️ Deployment

### Local Development
```bash
python app.py  # Runs on http://localhost:5000
```

### Production (Miraclemax Server)
```bash
# Deploy to miraclemax HP server (192.168.1.34)
# Run as container or VM for isolation
# Ensure NFS mount access to /mnt/nfs_share/charles/youtube/
```

---

**Part of the Red Hat PAI (Personal AI Infrastructure) System**
*Hatter - Digital Assistant for Charles's YouTube Content Management*
