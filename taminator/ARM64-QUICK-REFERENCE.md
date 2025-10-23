# ARM64 Quick Reference Card

**For: Fedora on Apple Silicon MacBooks (M1/M2/M3/M4)**

---

## User Quick Start

```bash
# 1. Check architecture
uname -m  # Should show: aarch64

# 2. Download
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator/releases/v1.9.2/

# 3. Run
chmod +x Taminator-*-arm64.AppImage
./Taminator-*-arm64.AppImage

# 4. If "fuse" error
sudo dnf install fuse fuse-libs
```

**Full Guide:** [docs/ARM64-FEDORA-MACBOOK.md](docs/ARM64-FEDORA-MACBOOK.md)

---

## Developer Quick Start

```bash
# Trigger release (includes ARM64)
git tag v1.9.3 && git push origin v1.9.3

# Monitor build (~25-40 min)
https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

# Download artifacts
https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
```

**Full Guide:** [GITLAB-CI-QUICKSTART.md](GITLAB-CI-QUICKSTART.md)

---

## Build Times

| Job | Duration |
|-----|----------|
| Linux x64 | 5-8 min |
| Linux ARM64 | 15-25 min (QEMU) |
| Windows | 8-12 min |
| macOS | 10-15 min |
| **Total** | ~25-40 min (parallel) |

---

## Files Produced

```
✅ Taminator-1.9.3-x86_64.AppImage     # Linux Intel/AMD
⭐ Taminator-1.9.3-arm64.AppImage      # Fedora on MacBook Pro
✅ Taminator-Setup-1.9.3.exe           # Windows
✅ Taminator-1.9.3-x64.dmg             # macOS Intel
✅ Taminator-1.9.3-arm64.dmg           # macOS Apple Silicon
```

---

## Troubleshooting

### Wrong Architecture Error
```bash
# Verify you downloaded ARM64, not x86_64
file Taminator-*.AppImage
# Should show: ARM aarch64 (not x86-64)
```

### FUSE Error
```bash
sudo dnf install fuse fuse-libs
sudo modprobe fuse
```

### SELinux Block (Fedora)
```bash
sudo setsebool -P allow_execheap 1
# Or extract: ./Taminator-*.AppImage --appimage-extract
```

---

## Why ARM64 for Fedora MacBook?

| Option | Works? | Reason |
|--------|--------|--------|
| macOS DMG | ❌ | macOS-only (you're running Linux) |
| x86_64 AppImage | ❌ | Wrong architecture (you have ARM64) |
| **ARM64 AppImage** | ✅ | **Linux + ARM64 = Perfect match** |

---

## Documentation

- 📖 **User Guide:** [docs/ARM64-FEDORA-MACBOOK.md](docs/ARM64-FEDORA-MACBOOK.md)
- 🔧 **CI/CD Guide:** [GITLAB-CI-QUICKSTART.md](GITLAB-CI-QUICKSTART.md)
- 📋 **Implementation:** [CI-CD-ARM64-IMPLEMENTATION.md](CI-CD-ARM64-IMPLEMENTATION.md)
- 🏗️ **Original ARM64:** [ARM64-INTEGRATION-COMPLETE.md](ARM64-INTEGRATION-COMPLETE.md)

---

**Status:** ✅ Production Ready  
**CI/CD:** ✅ Automated via GitLab  
**Platform:** Fedora 39+ on M1/M2/M3/M4 MacBooks

