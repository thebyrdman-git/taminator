# Building Taminator for Distribution

**How to create installable packages for Linux, macOS, and Windows**

---

## 🏗️ Build Requirements

### All Platforms
```bash
cd gui
npm install
```

### Platform-Specific Tools

**Linux:**
- `electron-builder` (installed via npm)
- For .deb: `dpkg`, `fakeroot`
- For .rpm: `rpm-build`

**macOS:**
- Xcode Command Line Tools
- Valid Apple Developer ID (for signed builds)

**Windows:**
- NSIS (installed automatically by electron-builder)
- Windows SDK (for code signing)

---

## 📦 Building Packages

### Build for Current Platform

```bash
cd gui
npm run build
```

**Output:** `gui/dist/`

### Build for Specific Platforms

```bash
# Linux only
npm run build -- --linux

# macOS only (must be on macOS)
npm run build -- --mac

# Windows only
npm run build -- --win

# All platforms (from Linux, macOS only)
npm run build -- --linux --win
```

---

## 🐧 Linux Installation

### AppImage (Universal Linux Binary)

**Build:**
```bash
npm run build -- --linux AppImage
```

**Output:** `dist/Taminator-2.0.0-alpha.AppImage`

**Install:**
```bash
# Make executable
chmod +x Taminator-2.0.0-alpha.AppImage

# Run directly
./Taminator-2.0.0-alpha.AppImage

# Or move to applications
mv Taminator-2.0.0-alpha.AppImage ~/Applications/
```

**Desktop Integration (automatic):**
- AppImage auto-registers on first run
- Appears in Applications menu
- Icon shows in launcher

### Linux ARM64 (Fedora aarch64, Apple Silicon Linux VMs)

**If the AppImage does not open on ARM64:** the default Linux build is **x86_64**. You must use the **ARM64** build.

**From GitLab CI:** In Pipelines → open the latest pipeline → download the artifact from the **build:linux:arm64** job (name like `linux-appimage-arm64-main`), not from `build:linux:x64`. Extract the `.AppImage` from the archive.

**Make executable and run from terminal (to see any errors):**
```bash
chmod +x Taminator-*.AppImage
./Taminator-*.AppImage
```

**Build locally on your ARM64 Fedora VM (if no ARM64 artifact is available):**
```bash
cd gui
npm ci
npm run build:linux:arm64:appimage
# Run: ./dist/Taminator-*-arm64.AppImage  (or similar name in dist/)
```

**Fedora:** If you see “error while loading shared libraries: libz.so” (or similar), install the runtime dependency:
```bash
sudo dnf install zlib
```
If other libraries are missing, try: `sudo dnf install zlib libX11 libXcomposite libXdamage libXext libXfixes libXrandr libgbm libnss3 libatk-1.0-0 libatk-bridge-2.0-0 libcups2 libdrm2 libxkbcommon0 libxshmfence1`
For FUSE or “cannot execute binary” errors, install `libfuse2` (or `fuse`) if needed, or run with `--appimage-extract-and-run`.

### Debian Package (.deb)

**Build:**
```bash
npm run build -- --linux deb
```

**Output:** `dist/taminator_2.0.0-alpha_amd64.deb`

**Install:**
```bash
sudo dpkg -i taminator_2.0.0-alpha_amd64.deb

# Fix dependencies if needed
sudo apt-get install -f
```

**Features:**
- ✅ Installs to `/opt/Taminator/`
- ✅ Creates desktop entry
- ✅ Adds to Applications menu
- ✅ Desktop icon
- ✅ Start menu entry

**Uninstall:**
```bash
sudo dpkg -r taminator
```

### RPM Package (Fedora, RHEL)

**Build:**
```bash
npm run build -- --linux rpm
```

**Output:** `dist/taminator-2.0.0-alpha.x86_64.rpm`

**Install:**
```bash
sudo rpm -i taminator-2.0.0-alpha.x86_64.rpm

# Or with dnf
sudo dnf install taminator-2.0.0-alpha.x86_64.rpm
```

**Features:**
- ✅ Installs to `/opt/Taminator/`
- ✅ Desktop entry in Applications
- ✅ Icon in launcher
- ✅ Automatic updates (if configured)

**Uninstall:**
```bash
sudo rpm -e taminator
```

---

## 🍎 macOS Installation

### DMG Installer

**Build (on macOS):**
```bash
npm run build -- --mac
```

**Output:** `dist/Taminator-2.0.0-alpha.dmg`

**Install:**
1. Double-click `Taminator-2.0.0-alpha.dmg`
2. Drag Taminator to Applications folder
3. Eject DMG
4. Launch from Applications or Spotlight

**Features:**
- ✅ Beautiful DMG with background image
- ✅ Drag-and-drop installer
- ✅ Appears in /Applications
- ✅ Launchpad integration
- ✅ Spotlight searchable
- ✅ Dock icon

**Uninstall:**
```bash
rm -rf /Applications/Taminator.app
```

**Code Signing (for distribution):**
```bash
# Requires Apple Developer ID
export CSC_LINK=/path/to/certificate.p12
export CSC_KEY_PASSWORD=your_password

npm run build -- --mac
```

---

## 🪟 Windows Installation

### NSIS Installer

**Build:**
```bash
npm run build -- --win
```

**Output:** `dist/Taminator Setup 2.0.0-alpha.exe`

**Install:**
1. Double-click `Taminator Setup 2.0.0-alpha.exe`
2. Choose installation directory
3. Select "Create Desktop Shortcut"
4. Click Install
5. Launch from Start Menu or Desktop

**Features:**
- ✅ Full installer wizard
- ✅ Start Menu entry
- ✅ Desktop shortcut (optional)
- ✅ Taskbar pinnable
- ✅ Windows 10/11 compatible
- ✅ Uninstaller included

**Uninstall:**
- Start Menu → Taminator → Uninstall
- Or: Control Panel → Programs → Uninstall

**Code Signing (for distribution):**
```bash
# Requires Windows code signing certificate
export CSC_LINK=/path/to/certificate.pfx
export CSC_KEY_PASSWORD=your_password

npm run build -- --win
```

---

## 🎨 Application Integration

### What Gets Installed

**All Platforms:**
- Application executable
- Application icon
- Desktop entry / shortcut
- Application menu entry
- File associations (if configured)

**Linux:**
- `.desktop` file in `~/.local/share/applications/`
- Icon in `/usr/share/icons/` or `~/.local/share/icons/`
- Appears in GNOME Activities, KDE Application Launcher, etc.

**macOS:**
- `.app` bundle in `/Applications/`
- Icon in Launchpad
- Searchable via Spotlight
- Appears in Dock when running

**Windows:**
- `.exe` in `C:\Program Files\Taminator\`
- Start Menu shortcut
- Desktop icon (optional)
- Pinnable to Taskbar

---

## 📋 Build Artifacts

### After Building

```
gui/dist/
├── Taminator-2.0.0-alpha.AppImage          # Linux (universal)
├── taminator_2.0.0-alpha_amd64.deb         # Debian/Ubuntu
├── taminator-2.0.0-alpha.x86_64.rpm        # Fedora/RHEL
├── Taminator-2.0.0-alpha.dmg               # macOS installer
├── Taminator-2.0.0-alpha-mac.zip           # macOS archive
├── Taminator Setup 2.0.0-alpha.exe         # Windows installer
└── linux-unpacked/                         # Unpacked Linux build
```

---

## 🚀 Distribution

### Internal Distribution

**For Red Hat TAMs:**

1. **Build all platforms:**
   ```bash
   cd gui
   npm run build -- --linux --win
   # macOS: npm run build -- --mac (on macOS)
   ```

2. **Upload to internal server:**
   ```bash
   scp dist/* releases@internal-server:/releases/taminator/v2.0.0-alpha/
   ```

3. **Create download page:**
   - List all platform options
   - Include checksums (SHA256)
   - Installation instructions

### Public Distribution (GitHub Releases)

**Automated via GitHub Actions:**

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Build
        run: cd gui && npm install && npm run build
      - name: Upload Release
        uses: actions/upload-artifact@v2
        with:
          name: taminator-${{ matrix.os }}
          path: gui/dist/*
```

---

## 🔐 Code Signing

### Why Code Sign?

**Without signing:**
- macOS: "App from unidentified developer" warning
- Windows: SmartScreen warning
- Users hesitant to install

**With signing:**
- ✅ Trusted installer
- ✅ No security warnings
- ✅ Professional distribution

### macOS Code Signing

**Requirements:**
- Apple Developer Account ($99/year)
- Developer ID Application certificate

**Process:**
```bash
# 1. Get certificate from Apple Developer Portal
# 2. Install certificate in Keychain
# 3. Set environment variables
export CSC_NAME="Developer ID Application: Your Name (TEAM_ID)"

# 4. Build with signing
npm run build -- --mac
```

### Windows Code Signing

**Requirements:**
- Code signing certificate (from Sectigo, DigiCert, etc.)
- Certificate must be EV (Extended Validation) for instant trust

**Process:**
```bash
# 1. Get certificate (.pfx file)
# 2. Set environment variables
export CSC_LINK=/path/to/cert.pfx
export CSC_KEY_PASSWORD=your_password

# 3. Build with signing
npm run build -- --win
```

---

## 🧪 Testing Built Applications

### Before Distribution

**Test on each platform:**

1. **Clean Install:**
   - Uninstall any previous version
   - Install from built package
   - Verify no errors

2. **Launch Test:**
   - Launch from Applications menu
   - Verify icon appears correctly
   - Check window opens properly

3. **Functionality Test:**
   - Test all commands (check, update, config)
   - Verify auth system works
   - Test issue reporting

4. **Uninstall Test:**
   - Uninstall cleanly
   - Verify no leftover files
   - Check Applications menu cleared

---

## 📝 Build Checklist

Before releasing:

- [ ] Update version in `package.json`
- [ ] Build for all platforms
- [ ] Test install on clean systems
- [ ] Verify icons appear correctly
- [ ] Test launch from Applications menu
- [ ] Check code signing (if applicable)
- [ ] Generate SHA256 checksums
- [ ] Create release notes
- [ ] Upload to distribution server
- [ ] Test download links
- [ ] Announce to users

---

## 🐛 Troubleshooting

### Linux: Icon Not Showing

**Fix:**
```bash
# Update icon cache
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/

# Or system-wide
sudo gtk-update-icon-cache -f -t /usr/share/icons/hicolor/
```

### macOS: "App is damaged" Error

**Fix:**
```bash
# Remove quarantine attribute
xattr -cr /Applications/Taminator.app
```

### Windows: SmartScreen Warning

**Fix:**
- Code sign the executable
- Or: Users click "More info" → "Run anyway"

---

*For questions about building/distribution, contact jbyrd@redhat.com*

