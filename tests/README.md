# RFE Automation Installation Testing

**Automated testing infrastructure for validating zero-dependency-hell installation**

---

## 🚀 Quick Start

```bash
cd /home/jbyrd/pai/rfe-automation-clean/tests
./run-tests.sh
```

**What it does**:
- Tests installation on RHEL 9, RHEL 8, Fedora 41, Fedora 40
- Uses Ansible + Podman for automation
- Only installs minimal prerequisites (git, python3)
- Validates installer handles everything else
- Takes ~10-15 minutes

---

## 📋 Prerequisites

The test requires:
- `ansible-core` - Install: `sudo dnf install ansible-core`
- `podman` - Install: `sudo dnf install podman`
- `rsync` - Install: `sudo dnf install rsync`
- Red Hat VPN (for cloning rhcase from GitLab)

---

## 🧪 What Gets Tested

### Minimal Prerequisites Only
Each test container gets ONLY:
- `git` - For cloning rhcase
- `python3` - Runtime

### Installer Must Handle
- All Python packages (requests, pyyaml, jinja2, cryptography, etc.)
- Build dependencies (if needed)
- rhcase cloning from GitLab
- rhcase installation
- PATH configuration

### Validation
Tests verify `rhcase` command works via:
1. Global install (`rhcase --version`)
2. User install (`~/.local/bin/rhcase --version`)
3. Venv install (`.venv/bin/rhcase --version`)

---

## 📁 Files

```
tests/
├── run-tests.sh              # Main test runner
├── test-installation.yml     # Ansible playbook (orchestration)
├── test-platform.yml         # Per-platform test logic
├── test-installation.sh      # Original bash test (deprecated)
├── Vagrantfile              # VM-based testing (alternative)
└── README.md                # This file
```

---

## 🎯 Success Criteria

**Installation must**:
- ✅ Work with ONLY git + python3 pre-installed
- ✅ Clone rhcase from GitLab automatically
- ✅ Handle all dependencies (3 fallback methods)
- ✅ Complete in < 5 minutes per platform
- ✅ Leave rhcase command functional

---

## 📊 Test Output

```
🧪 RFE Automation Installation Testing (Ansible)
==================================================

✅ All test prerequisites available

PLAY [Test RFE Automation Installation] ****************

TASK [Test installation on each platform] **************

✅ PASSED: RHEL 9 (AlmaLinux)
✅ PASSED: RHEL 8 (AlmaLinux)
✅ PASSED: Fedora 41
✅ PASSED: Fedora 40

==================================================
Test results saved in: ~/.cache/rfe-tests/
==================================================
```

---

## 🔍 Troubleshooting

### Test fails with "Failed to clone rhcase"
**Cause**: Not connected to Red Hat VPN  
**Fix**: Connect to Red Hat VPN and retry

### Test fails with "ansible-playbook: command not found"
**Cause**: Ansible not installed  
**Fix**: `sudo dnf install ansible-core`

### Test fails with permission denied
**Cause**: SELinux or container permissions  
**Fix**: Tests use `:Z` flag for SELinux, should work automatically

### Want to see detailed output
**Fix**: Run with verbose flag: `ansible-playbook test-installation.yml -vv`

---

## 🧹 Cleanup

Failed tests leave directories for debugging:
```bash
# View failed test logs
ls -la ~/.cache/rfe-tests/

# Clean up all test directories
rm -rf ~/.cache/rfe-tests/
```

---

## 🎯 Why This Approach

### Ansible Benefits
- ✅ Declarative, readable test definitions
- ✅ Easy to add more platforms
- ✅ Structured error handling
- ✅ Reusable for CI/CD
- ✅ Industry standard for automation

### Container Benefits
- ✅ Clean slate every time
- ✅ Fast (no VM overhead)
- ✅ Parallel testing possible
- ✅ Consistent environment

### GitLab Integration
- ✅ Always tests latest rhcase
- ✅ No submodule complexity
- ✅ Simpler for TAMs (they clone fresh too)
- ✅ Matches real-world usage

---

## 📝 Adding New Platforms

Edit `test-installation.yml`:

```yaml
test_platforms:
  - name: "Rocky Linux 9"
    image: "rockylinux:9"
    base_packages:
      - git
      - python3
```

That's it. The test will automatically include the new platform.

---

*Ready to test! Run: `./run-tests.sh`*

