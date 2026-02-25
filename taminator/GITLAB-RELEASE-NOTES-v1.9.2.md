## Taminator v1.9.2 - Cross-Platform Release

### 🎉 What's New
- ✅ **macOS builds now available** (Intel + Apple Silicon Universal DMG)
- ✅ **Windows builds now available** (NSIS Installer)
- ✅ **Linux AppImage x86_64** (Intel/AMD)
- ✅ **Linux AppImage ARM64** ⭐ (Fedora on MacBook Pro M1/M2/M3/M4)
- ✅ Setup wizard for first-time users
- ✅ Empty states with helpful guidance
- ✅ All core features fully functional

### 📥 Downloads

**From GitLab Repository (requires Red Hat VPN):**
- 🐧 [Linux AppImage x86_64](https://gitlab.cee.redhat.com/jbyrd/taminator/-/tree/main/taminator/releases/v1.9.2) (116 MB - Intel/AMD)
- 🐧 [Linux AppImage ARM64](https://gitlab.cee.redhat.com/jbyrd/taminator/-/tree/main/taminator/releases/v1.9.2) (118 MB - Fedora on MacBook) ⭐
- 🍎 [macOS Universal DMG](https://gitlab.cee.redhat.com/jbyrd/taminator/-/tree/main/taminator/releases/v1.9.2) (111 MB - Intel + Apple Silicon)
- 🪟 [Windows Installer](https://gitlab.cee.redhat.com/jbyrd/taminator/-/tree/main/taminator/releases/v1.9.2) (88 MB)

**All files in:** `taminator/releases/v1.9.2/`

### 🔧 Installation

**Linux (x86_64 - Intel/AMD):**
```bash
chmod +x Taminator-1.9.2.AppImage
./Taminator-1.9.2.AppImage
```

**Linux (ARM64 - Fedora on MacBook Pro):**
```bash
# Verify architecture
uname -m  # Should show: aarch64

# Install and run
chmod +x Taminator-1.9.2-arm64.AppImage
./Taminator-1.9.2-arm64.AppImage

# If FUSE error (Fedora)
sudo dnf install fuse fuse-libs
```
**📖 ARM64 Guide:** [docs/ARM64-FEDORA-MACBOOK.md](https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/taminator/docs/ARM64-FEDORA-MACBOOK.md)

**macOS:**
- Open DMG, drag to Applications
- First launch: Right-click → Open (to bypass Gatekeeper)
- Works on both Intel and Apple Silicon Macs

**Windows:**
- Run `Taminator-Setup-1.9.2.exe`
- Follow installation wizard
- Launch from Start Menu

### 🐛 Bug Fixes
- Fixed settings save functionality
- Fixed bug report submission
- Fixed T3/KAB tab visibility
- Removed hardcoded test data
- Added missing IPC handlers

### 🔒 Requirements
- Red Hat VPN for KB/T3 features
- Portal token (rh_jwt cookie) for authentication
- JIRA token for RFE tracking

### 📚 Documentation
- [README](https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/README.md)
- [Getting Started Guide](https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/GETTING-STARTED.md)

---

**"Come with me if you want to save time."** - Taminator T-800

