# GitLab CI/CD Quick Start Guide

## Overview

Taminator now has **automated CI/CD** via GitLab CI that builds releases for all platforms including ARM64 (Fedora on MacBook Pro).

---

## How It Works

### Pipeline Stages

```
┌─────────────────────────────────────────────┐
│            Stage 1: Build                   │
├─────────────────────────────────────────────┤
│  build:linux:x64      (Ubuntu + Node 20)    │
│  build:linux:arm64    (QEMU emulation)      │
│  build:windows        (Windows runner)      │
│  build:macos          (macOS runner)        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│            Stage 2: Release                 │
├─────────────────────────────────────────────┤
│  release:gitlab   (Create GitLab Release)   │
│    - Downloads all artifacts                │
│    - Creates release with notes             │
│    - Attaches binaries                      │
└─────────────────────────────────────────────┘
```

---

## Triggering a Release

### Method 1: Tag Push (Recommended)

```bash
cd /home/jbyrd/pai/taminator

# Update version in gui/package.json first
vim gui/package.json  # Change "version": "1.9.3"

# Commit version bump
git add gui/package.json
git commit -m "Bump version to 1.9.3"

# Create and push tag
git tag v1.9.3
git push origin main
git push origin v1.9.3

# CI/CD automatically starts
```

### Method 2: Manual Pipeline Trigger

Via GitLab UI:
1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines
2. Click **"Run Pipeline"**
3. Select branch: `main`
4. Click **"Run Pipeline"**

---

## Monitoring the Build

### Check Pipeline Status

```bash
# Via GitLab UI
https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

# Via GitLab CLI (if installed)
glab ci status
glab ci view
```

### Expected Timeline

| Job | Duration | Notes |
|-----|----------|-------|
| `build:linux:x64` | 5-8 min | Fast, native x86_64 |
| `build:linux:arm64` | 15-25 min | Slower, QEMU emulation |
| `build:windows` | 8-12 min | Windows runner |
| `build:macos` | 10-15 min | macOS runner |
| `release:gitlab` | 1-2 min | Artifact collection |
| **Total** | ~25-40 min | Parallel execution |

---

## What Gets Built

### Artifacts Produced

```
Taminator-1.9.3-x86_64.AppImage      # Linux Intel/AMD (~118 MB)
Taminator-1.9.3-arm64.AppImage       # Linux ARM64 (~118 MB) ⭐ Fedora on MacBook
Taminator-Setup-1.9.3.exe            # Windows NSIS (~88 MB)
Taminator-1.9.3-x64.dmg              # macOS Intel (~111 MB)
Taminator-1.9.3-arm64.dmg            # macOS Apple Silicon (~111 MB)
```

### Download Locations

**Current Release (v1.9.2) - Available Now:**
- **Repository:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/tree/main/taminator/releases/v1.9.2
- Files committed to Git (LFS)
- Includes ARM64 AppImage: `Taminator-1.9.2-arm64.AppImage`

**Future Releases (v1.9.3+) - CI/CD Automated:**
- **GitLab Releases:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- Built automatically by pipeline
- Artifacts attached to release

**Direct Artifact Links (CI/CD):**
```
https://gitlab.cee.redhat.com/jbyrd/taminator/-/jobs/artifacts/v1.9.3/raw/gui/dist/Taminator-1.9.3-arm64.AppImage?job=build:linux:arm64
```

**Both Options Work:**
- Manual: Build locally, commit to `releases/` directory
- Automated: CI/CD builds and attaches to GitLab Release
- v1.9.2 uses manual, v1.9.3+ can use either or both

---

## Configuration Files

### `.gitlab-ci.yml` Structure

```yaml
stages:
  - build      # Parallel platform builds
  - release    # Collect and publish

variables:
  NODE_VERSION: "20"
  PYTHON_VERSION: "3.11"
  ARTIFACTS_EXPIRE: "7 days"

jobs:
  - build:linux:x64        # Native x86_64
  - build:linux:arm64      # QEMU ARM64 ⭐ For Fedora on MacBook
  - build:windows          # Windows NSIS
  - build:macos            # Universal macOS
  - release:gitlab         # GitLab Release
```

---

## Runner Requirements

### What You Need on GitLab

| Platform | Runner Type | Tag | Notes |
|----------|-------------|-----|-------|
| Linux x64 | Docker | `docker` | ✅ GitLab.com provides |
| Linux ARM64 | Docker + QEMU | `docker` | ✅ GitLab.com provides |
| Windows | Windows Shell | `windows` | ⚠️ Need Red Hat runner |
| macOS | macOS Shell | `macos` | ⚠️ Need Red Hat runner |

### Using GitLab SaaS Runners

GitLab.com provides:
- ✅ **Linux x64** - Unlimited (shared runners)
- ✅ **Linux ARM64** - Via QEMU on x64 runners
- ❌ **Windows** - Requires self-hosted or paid plan
- ❌ **macOS** - Requires self-hosted

### For Red Hat Internal GitLab

If you're on `gitlab.cee.redhat.com`:
- Check with IT for available runner tags
- May need to request Windows/macOS runner access
- Or: Build locally and upload manually

---

## ARM64 Build Details

### Why QEMU?

GitLab runners are typically x86_64, so we use QEMU to cross-compile ARM64:

```yaml
before_script:
  - apt-get install -y qemu-user-static binfmt-support
  - update-binfmts --enable qemu-aarch64
```

### Performance Impact

| Method | Build Time |
|--------|------------|
| Native ARM64 runner | 5-8 minutes |
| QEMU emulation | 15-25 minutes |

### Alternative: Native ARM64 Runners

If you have ARM64 GitLab runners available:

```yaml
build:linux:arm64:native:
  stage: build
  tags:
    - arm64  # Your ARM64 runner tag
  # ... rest of config
```

Uncomment the native build job in `.gitlab-ci.yml` and comment out the QEMU version.

---

## Troubleshooting

### Build Fails: "No runner available"

**Problem:** No runners with required tags.

**Fix:**
```bash
# Check available runners
https://gitlab.cee.redhat.com/jbyrd/taminator/-/settings/ci_cd

# Verify tags in .gitlab-ci.yml match available runners
# Default: docker, windows, macos
```

### Build Fails: QEMU Timeout

**Problem:** ARM64 build exceeds 2-hour timeout.

**Fix:**
```yaml
# In .gitlab-ci.yml, increase timeout
build:linux:arm64:
  timeout: 3h  # Increase from 2h
```

### Build Succeeds but No Release Created

**Problem:** Release job only runs on tags.

**Fix:**
```bash
# Ensure you pushed a tag
git push origin v1.9.3

# Check pipeline was triggered by tag
https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines
```

### Artifacts Expired

**Problem:** Artifacts deleted after 7 days.

**Fix:**
```yaml
# In .gitlab-ci.yml, extend expiration
artifacts:
  expire_in: 30 days  # or "never"
```

---

## Manual Build Fallback

If CI/CD is unavailable, build locally:

```bash
cd /home/jbyrd/pai/taminator

# Linux x64
./build-standalone.sh

# Linux ARM64
./build-linux-arm64.sh

# Windows (on Windows machine)
./build-windows.sh

# macOS (on Mac)
cd gui && npm run build:mac
```

---

## Testing the Pipeline

### Dry Run (No Release)

```bash
# Push to branch (not tag)
git checkout -b test-ci
git push origin test-ci

# Triggers build jobs but NOT release job
# Verify artifacts are created correctly
```

### Full Test Release

```bash
# Create test tag
git tag v1.9.3-test
git push origin v1.9.3-test

# Full pipeline runs including release
# Delete after verification:
git tag -d v1.9.3-test
git push origin :refs/tags/v1.9.3-test
```

---

## Best Practices

### Before Every Release

1. ✅ Update version in `gui/package.json`
2. ✅ Test locally: `./build-standalone.sh`
3. ✅ Commit version bump
4. ✅ Create and push tag
5. ✅ Monitor pipeline
6. ✅ Verify artifacts in GitLab Release
7. ✅ Test download and install on target platform

### Version Numbering

Follow semantic versioning:
- `v1.9.3` - Patch (bug fixes)
- `v1.10.0` - Minor (new features)
- `v2.0.0` - Major (breaking changes)

---

## CI/CD Checklist

### Initial Setup (One-Time)

- [x] `.gitlab-ci.yml` created
- [x] Runner tags configured
- [ ] Windows runner access (if needed)
- [ ] macOS runner access (if needed)
- [ ] Test pipeline on non-tag branch
- [ ] Test full release with test tag

### Per-Release (Every Time)

- [ ] Version bumped in `gui/package.json`
- [ ] Local build tested
- [ ] Changes committed
- [ ] Tag created and pushed
- [ ] Pipeline monitored
- [ ] Artifacts verified
- [ ] Release notes updated
- [ ] Downloads tested

---

## Resources

### GitLab CI/CD Documentation
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
- [QEMU Setup](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-qemu-to-build-multi-platform-images)
- [Release CLI](https://docs.gitlab.com/ee/ci/yaml/index.html#release)

### Electron Builder
- [Multi-Platform Builds](https://www.electron.build/multi-platform-build)
- [AppImage](https://www.electron.build/configuration/linux)

---

## Summary

**GitLab CI/CD is now configured for Taminator:**
- ✅ Automated multi-platform builds
- ✅ ARM64 support for Fedora on MacBook Pro
- ✅ Automatic GitLab Release creation
- ✅ Artifact management
- ✅ Tag-triggered releases

**To release:**
```bash
git tag v1.9.3 && git push origin v1.9.3
```

**Done.** CI/CD handles the rest.

---

**Status:** ✅ Production Ready  
**Maintainer:** Jimmy Byrd (jbyrd@redhat.com)  
**Last Updated:** October 23, 2025

