# Building Taminator - Quick Notes

## Network Requirements

**Building packages requires external internet access** to download Electron binaries from GitHub.

### Issue with Red Hat VPN

When connected to Red Hat VPN, external GitHub downloads are blocked:
```
Get "https://release-assets.githubusercontent.com/...electron-v38.3.0-linux-x64.zip":
dial tcp 185.199.110.133:443: connect: network is unreachable
```

### Solutions

**Option 1: Disconnect VPN temporarily**
```bash
# Disconnect VPN
nmcli connection down "Red Hat VPN"

# Build packages
cd /home/jbyrd/pai/automation/rfe-bug-tracker/gui
npm run build

# Reconnect VPN
nmcli connection up "Red Hat VPN"
```

**Option 2: Use cached Electron (if already downloaded)**
```bash
# Check if Electron is cached
ls ~/.cache/electron/

# If present, build should work offline
npm run build
```

**Option 3: Build on external network**
- Connect to non-VPN network
- Run `npm run build`
- Packages built in `gui/dist/`

---

## Build Output

After successful build, you'll have:

```
gui/dist/
├── Taminator-2.0.0-alpha.AppImage          # Universal Linux
├── taminator-2.0.0-alpha.x86_64.rpm        # Fedora/RHEL
├── taminator_2.0.0-alpha_amd64.deb         # Ubuntu/Debian
└── linux-unpacked/                         # Unpacked build
```

---

## Installing on Fedora

### RPM Package (recommended)
```bash
sudo dnf install gui/dist/taminator-2.0.0-alpha.x86_64.rpm
```

**Result:**
- ✅ Installs to `/opt/Taminator/`
- ✅ Desktop entry in Applications
- ✅ Appears in Activities search
- ✅ Icon in launcher

### AppImage (portable)
```bash
chmod +x gui/dist/Taminator-2.0.0-alpha.AppImage
./gui/dist/Taminator-2.0.0-alpha.AppImage
```

**Result:**
- ✅ Runs without installation
- ✅ Auto-registers desktop entry on first run
- ✅ Portable (can copy to USB)

---

## Testing Desktop Integration

After install:

1. **Open Activities** (Super key)
2. **Type "Taminator"**
3. **Should see:**
   - Terminator skull icon
   - "Taminator" app name
   - "The Skynet TAMs actually want" description

4. **Click to launch**
5. **Verify:**
   - GUI opens
   - Auth status shows
   - All features work

---

## Current Status

**✅ Completed:**
- Desktop integration configuration
- Linux packaging setup (AppImage, RPM, DEB)
- macOS DMG configuration
- Windows NSIS installer configuration
- Icon and branding

**⏸️ Pending:**
- Build packages (requires non-VPN network)
- Test installation on clean system
- Verify desktop entry appears correctly

---

**Next Steps:**

1. Disconnect from VPN
2. Run `npm run build` in gui/ directory
3. Install RPM: `sudo dnf install dist/*.rpm`
4. Test: Open Activities, search "Taminator", launch

---

*For full documentation, see BUILDING.md*

