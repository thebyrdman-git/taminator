# README.md Updates for Automated Installer

## Changes Made

Updated README.md to reflect the new automated installation process:

### 1. Quick Start Section
**Before**: Referenced GETTING-STARTED.md only  
**After**: Shows complete 3-command installation

```bash
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation
./install-improved.sh
```

### 2. What You Need Section
**Before**: Listed many requirements including "Python 3 with required packages"  
**After**: Minimal requirements - just git + python3

Removed:
- ❌ "Access to customer portal" (not needed for installation)
- ❌ "Python 3 with required packages" (installer handles this)
- ❌ "Git installed and configured" (simplified)

Added:
- ✅ "No sudo, no build tools, no system packages required"
- ✅ Clear minimal requirements

### 3. Installation Section
**Before**: `./bin/install-dependencies` (old script)  
**After**: `./install-improved.sh` with feature highlights

Features now highlighted:
- ✅ Fully automated
- ✅ No sudo needed
- ✅ User-space only
- ✅ Smart fallback
- ✅ Auto-clones rhcase
- ✅ Clear errors

### 4. Get the Tool Section
**Before**: Only ZIP download instructions  
**After**: Git clone first, ZIP as alternative

More modern approach for developers.

---

## What Still Needs Review

1. **GETTING-STARTED.md** - May need updates to reference new installer
2. **Build scripts** - Any references to old `install-dependencies`
3. **Documentation links** - Ensure all docs reference correct installer

---

These changes align README.md with the new automated installer while keeping all other useful information intact.

