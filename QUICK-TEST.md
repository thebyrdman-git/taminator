# Quick Installation Test

**Fully automated, rapid validation in ~3 minutes**

---

## 🚀 Run It

```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests
./test-single-platform.sh
```

**That's it.** No interaction needed.

---

## 🎯 What It Does

1. **Creates test workspace** in `~/.cache/rfe-quick-test-*`
2. **Copies project** (excludes .venv, output, logs)
3. **Launches Fedora 41 container** (default, fastest)
4. **Installs prerequisites**: `git` + `python3` only
5. **Runs installer**: `./install-improved.sh`
6. **Verifies rhcase works**
7. **Reports PASS/FAIL**
8. **Cleans up** (on success)

**Total time**: ~2-3 minutes

---

## 🎨 Test Different Platforms

```bash
# RHEL 9
./test-single-platform.sh almalinux:9

# RHEL 8
./test-single-platform.sh almalinux:8

# Fedora 40
./test-single-platform.sh fedora:40

# Fedora 41 (default)
./test-single-platform.sh
```

---

## ✅ Expected Output

```
🧪 Quick Installation Test
==========================
Platform: fedora:41

ℹ  Creating test workspace...
ℹ  Copying project files...
✅ Test workspace ready

ℹ  Starting container test...

=== Installing prerequisites (git + python3) ===
Complete!

=== Running install-improved.sh ===
🚀 RFE Automation Tool - Fully Automated Installation
ℹ  Detecting platform...
ℹ  Platform detected: fedora
✅ Git is installed
ℹ  Getting latest rhcase from GitLab...
ℹ  Cloning rhcase from GitLab...
✅ rhcase cloned successfully
ℹ  Method 1: Trying UV package manager...
ℹ  Installing UV package manager...
✅ UV installed successfully
ℹ  Installing rhcase via UV...
✅ UV installation successful
🎉 Installation Complete!

=== Verifying installation ===
✅ rhcase found in PATH
rhcase 1.2.3

==========================================
✅ TEST PASSED: fedora:41
==========================================
```

---

## 🔧 Troubleshooting

### Test fails with "Failed to clone rhcase"
**Cause**: Not on Red Hat VPN  
**Fix**: Connect VPN and retry

### Test fails with podman errors
**Cause**: Podman not installed or not running  
**Fix**: `sudo dnf install podman`

### Want to see full log
```bash
# Run with debug output
./test-single-platform.sh 2>&1 | tee test-debug.log
```

### Test fails, want to investigate
```bash
# Check the saved log
cat ~/.cache/rfe-quick-test-*/test.log

# Or enter the container manually
podman run --rm -it -v $(pwd)/../:/test:Z fedora:41 bash
cd /test
./install-improved.sh
```

---

## 📊 Full Test Suite

For complete testing across all platforms:

```bash
# Ansible-based test (all 4 platforms)
./run-tests.sh

# Takes ~10-15 minutes
# Tests: RHEL 9, RHEL 8, Fedora 41, Fedora 40
```

---

## 🎯 Why Two Test Options?

### Quick Test (`test-single-platform.sh`)
- ✅ **Fast**: 2-3 minutes
- ✅ **Simple**: Bash script
- ✅ **Focused**: One platform at a time
- ✅ **Great for**: Rapid iteration during development

### Full Test (`run-tests.sh`)
- ✅ **Comprehensive**: All 4 platforms
- ✅ **Structured**: Ansible playbook
- ✅ **Detailed**: Per-platform logs
- ✅ **Great for**: Final validation before release

---

## ✨ Fully Automated

**Both tests are fully automated**:
- ❌ No user prompts
- ❌ No manual steps
- ❌ No configuration files
- ✅ Just run and get results

**Perfect for**:
- CI/CD pipelines
- Quick validation
- Pre-commit checks
- TAM testing

---

*Test your changes in 3 minutes: `./test-single-platform.sh`*

