# RFE Automation Tool - Installation Requirements

**User-Space Installation Only - No sudo/dnf Required**

---

## 🎯 Design Philosophy

**TAMs should never need sudo access to install the RFE automation tool.**

The installer is designed to work in user-space with only basic prerequisites that are already present on Red Hat laptops.

---

## ✅ Prerequisites (Already on TAM Laptops)

### Required (Pre-installed on RHEL/Fedora)
- `git` - For cloning repositories
- `python3` (3.8+) - Runtime environment
- Red Hat VPN - For accessing internal GitLab

### Optional (Improves Experience)
- `python3-pip` - Usually pre-installed
- `python3-venv` - Usually pre-installed

**That's it.** No build tools, no compiler, no system packages.

---

## 🚀 Installation Methods (User-Space Only)

### Method 1: UV Package Manager (Recommended)
```bash
# Installs to ~/.cargo/bin/uv (no sudo)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installs rhcase to ~/.local/bin (no sudo)
uv tool install ./rhcase
```

**Why UV?**
- ✅ 10-100x faster than pip
- ✅ Automatic virtual environment isolation
- ✅ Pre-built wheels (no gcc/build tools needed)
- ✅ Works on all platforms
- ✅ User-space only (~/.cargo, ~/.local)

### Method 2: Pip + Virtual Environment (Fallback)
```bash
# Creates .venv in project directory
python3 -m venv .venv
source .venv/bin/activate

# Installs to .venv/bin (no sudo)
pip install ./rhcase
```

**Why Pip+Venv?**
- ✅ Always available (part of Python)
- ✅ No external dependencies
- ✅ Isolated from system Python
- ✅ User-space only

---

## ❌ What We Don't Do

### No System Package Installation
```bash
# ❌ NEVER do this
sudo dnf install python3-requests python3-cryptography

# ❌ NEVER require sudo
# ❌ NEVER touch /usr/lib or /usr/bin
# ❌ NEVER require build tools (gcc, python3-devel)
```

**Why?**
- TAMs may not have sudo access
- Corporate laptops are locked down
- System package installation can break other tools
- Creates support burden ("why did it install system packages?")

---

## 🔧 How It Works

### Automatic Method Selection
The installer tries methods in order:

1. **UV** (if available or can install)
   - Fast, isolated, pre-built wheels
   - No build dependencies needed
   
2. **Pip + Venv** (always works)
   - Slower but reliable
   - May need to compile some packages (cryptography)
   - Falls back to pure-Python alternatives if compilation fails

### Smart Dependency Handling
- Uses pre-built wheels when available (avoid compilation)
- Falls back to older versions if needed (RHEL 8 compatibility)
- Provides clear error messages with solutions
- Never fails silently

---

## 📊 Tested Platforms

| Platform | Python | UV | Pip+Venv | Notes |
|----------|--------|----|---------|-|
| **RHEL 9** | 3.9 | ✅ | ✅ | Primary target |
| **RHEL 8** | 3.6/3.8 | ✅ | ✅ | May need python39 package |
| **Fedora 40** | 3.12 | ✅ | ✅ | Latest packages |
| **Fedora 41** | 3.13 | ✅ | ✅ | Latest packages |

---

## 🎯 TAM Experience

### Before (With sudo requirements)
```
TAM: ./install.sh
Error: sudo: command not found
TAM: "I don't have sudo access"
TAM: Gives up
```

### After (User-space only)
```
TAM: ./install.sh
Script: ℹ  Method 1: Trying UV package manager...
Script: ✅ UV installed successfully
Script: ✅ rhcase installed successfully
Script: 🎉 Installation Complete!
TAM: ./bin/tam-rfe-chat
TAM: Works perfectly
```

---

## 🔍 Troubleshooting

### "Python 3.8+ required but found 3.6"
**Platform**: RHEL 8  
**Solution**: Install python39 (one-time, may need IT)
```bash
sudo dnf install python39
python3.9 -m venv .venv
source .venv/bin/activate
pip install ./rhcase
```

### "gcc: command not found" (during pip install)
**Cause**: Trying to compile cryptography  
**Solution**: Installer auto-handles this by:
1. Trying UV first (pre-built wheels)
2. Falling back to older versions
3. Using pure-Python alternatives

**No action needed** - installer handles it.

### "Failed to clone rhcase from GitLab"
**Cause**: Not on Red Hat VPN  
**Solution**: Connect to Red Hat VPN

---

## 📝 For Developers

### Adding New Dependencies
When adding dependencies to rhcase:

1. **Check if wheels available**: https://pypi.org/project/PACKAGE/#files
2. **Prefer pure-Python packages**: Avoid C extensions
3. **Document minimum versions**: For RHEL 8 compatibility
4. **Test on oldest platform**: RHEL 8 with Python 3.6

### Testing Installation
```bash
# Test with only git + python3 available
podman run --rm -it -v $(pwd):/test:Z fedora:41 bash -c "
    dnf install -y git python3
    cd /test
    ./install-improved.sh
"
```

---

## ✅ Success Criteria

Installation is successful when:
- ✅ Works with ONLY git + python3 pre-installed
- ✅ No sudo/dnf commands required
- ✅ No build tools (gcc, python3-devel) required
- ✅ Completes in < 5 minutes
- ✅ rhcase command functional
- ✅ All files in user-space (~/.local, ~/.cargo, .venv)

---

*Installation designed for TAMs by TAMs - no sudo required, ever.*

