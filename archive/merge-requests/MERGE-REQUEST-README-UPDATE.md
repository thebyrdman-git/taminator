# Merge Request: Update README for Automated Installer

## Overview

Update README.md to accurately reflect the new automated installation process and remove outdated references to the old `install-dependencies` script.

## Branch Information

- **Source Branch**: `feature/update-readme-automated-installer`
- **Target Branch**: `main`
- **Merge Request Title**: "docs: Update README to reflect automated installer"

## Changes Made

### 1. Quick Start Section
**Cleaned up** to show straightforward 3-command installation:
```bash
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation
./install-improved.sh
```

### 2. What You Need Section
**Simplified** requirements to minimal essentials:
- `git` (pre-installed on RHEL/Fedora)
- `python3` 3.8+ (pre-installed on RHEL/Fedora)
- Red Hat VPN for GitLab access

**Removed** obsolete requirements:
- "Python 3 with required packages" (installer handles this)
- "Access to customer portal" (not needed for installation)

**Added** clarity:
- "No sudo, no build tools, no system packages required"

### 3. Installation Section
**Replaced** old `./bin/install-dependencies` with `./install-improved.sh`

**Highlighted** new features:
- ✅ Fully automated (no user interaction)
- ✅ No sudo needed (locked-down laptops)
- ✅ User-space only (no system packages)
- ✅ Smart fallback (UV → pip+venv)
- ✅ Auto-clones rhcase from GitLab
- ✅ Clear error messages

### 4. Get the Tool Section
**Modernized** with git clone as primary method:
- Git clone shown first (developer-friendly)
- ZIP download as alternative (less technical users)

### 5. Repository Visibility Note
**Simplified** GitLab access information:
- Removed lengthy GitLab CEE license instructions (not required for Internal repos)
- Added simple note about Internal visibility
- Repository is accessible to all Red Hat employees with GitLab access

## Files Changed

- `README.md` - Updated installation instructions, requirements, and quick start

## Testing

- ✅ Verified all links still work
- ✅ Confirmed installation commands are accurate
- ✅ Checked markdown formatting renders correctly

## Related Changes

This merge request complements the automated installer merge request:
- Previous MR: "feat: Add fully automated installation system"
- This MR: Documentation updates to match new installer

## Merge Request Description (Copy/Paste to GitLab)

```markdown
## Summary

Updates README.md to reflect the new automated installer (`install-improved.sh`) and removes references to the deprecated `install-dependencies` script.

## Changes

### Quick Start
- Added 3-command installation example at top
- Shows: clone → install → run

### Requirements Section
- Simplified to minimal essentials (git + python3)
- Removed outdated package requirements
- Emphasized "no sudo needed"

### Installation Instructions
- Updated to use `./install-improved.sh`
- Highlighted automation features (no interaction, smart fallback, auto-clones rhcase)
- Added estimated installation time (2-5 minutes)

### Get the Tool
- Git clone now primary method
- ZIP download as alternative

## Why This Matters

1. **Old installer reference**: README referenced `./bin/install-dependencies` which no longer exists
2. **Simplified access info**: Removed confusing GitLab CEE license instructions that weren't necessary (repo is Internal visibility)
3. **User feedback**: Simplified based on issue reported by Dave Carmichael (dcarmich) - actual issue was repository visibility, not licensing

This update ensures documentation matches the actual installation process with clear, simple instructions.

## Testing

- [x] Verified all commands are correct
- [x] Confirmed all links work
- [x] Checked markdown rendering

## Related Work

Companion to automated installer MR. Should be merged after installer MR is approved.

## Checklist

- [x] Documentation is accurate
- [x] No broken links
- [x] Commands tested
- [x] Formatting correct
```

## Labels

- `documentation`
- `enhancement`

## Assignee

- jbyrd

## Reviewer Suggestions

- Anyone who has tested the automated installer
- TAMs who will use this tool

---

*Generated: 2025-10-15*
*Author: jbyrd*

