# Cross-Platform Testing

## Overview

Automated testing suite to validate the RFE Bug Tracker Automation Tool works correctly on **Linux, macOS, and Windows**.

## Test Files

### Platform Abstraction Tests
- **`test_platform_abstraction.py`** - Comprehensive test of `foundation/platform.py`
  - OS detection (Linux/macOS/Windows)
  - Directory path conventions (XDG/Library/AppData)
  - OS-specific helpers (shells, paths, line endings)

- **`test_directory_structure.py`** - Directory creation and management
  - Creates test directories
  - Validates file operations
  - Tests cleanup

### Installation Tests
- **`test-install.sh`** - Linux/macOS installation validation
- **`test_installation_windows.py`** - Windows installation validation

## Running Tests Locally

### Linux/macOS
```bash
# Run all tests
python3 tests/test_platform_abstraction.py
python3 tests/test_directory_structure.py
./tests/test-install.sh
```

### Windows
```powershell
# Run all tests
python tests\test_platform_abstraction.py
python tests\test_directory_structure.py
python tests\test_installation_windows.py
```

## CI/CD Integration

### GitHub Actions
The workflow `.github/workflows/cross-platform-test.yml` automatically tests on:
- **ubuntu-22.04** (Linux)
- **macos-13** (macOS)
- **windows-latest** (Windows)

**Triggers:**
- Push to `main`/`master`
- Pull requests
- Manual workflow dispatch

### GitLab CI
The configuration `.gitlab-ci.yml` tests on available runners:
- **Linux** - UBI9/Python 3.11 container
- **macOS** - Requires macOS runner (optional)
- **Windows** - Requires Windows runner (optional)

## Current Status

| Platform | Status | Coverage |
|----------|--------|----------|
| **Linux** | ✅ **Fully Tested** | RHEL 8/9, Fedora 40-43, Ubuntu 22.04 |
| **macOS** | ⚠️ **Architectural Support** | CI/CD ready, needs runner |
| **Windows** | ⚠️ **Architectural Support** | CI/CD ready, needs runner |

## Path to A+ Grade

**Current Grade: A** (Architecture supports all platforms, validated on Linux)

**To achieve A+:**
1. ✅ Create comprehensive test suite (DONE)
2. ✅ Set up CI/CD workflows (DONE)
3. ⏳ Enable macOS runner in CI/CD
4. ⏳ Enable Windows runner in CI/CD
5. ⏳ Validate production usage on all platforms

### Enabling CI/CD Runners

#### For GitHub Actions
**No action needed** - GitHub provides free Linux/macOS/Windows runners.

Just push to GitHub and workflows run automatically.

#### For GitLab CEE
**Linux:** ✅ Already works with shared runners

**macOS:** Requires GitLab Runner on macOS machine
```bash
# On macOS machine:
brew install gitlab-runner
gitlab-runner register --url https://gitlab.cee.redhat.com \
  --tag-list "macos"
```

**Windows:** Requires GitLab Runner on Windows machine
```powershell
# On Windows machine:
# Download: https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-windows-amd64.exe
gitlab-runner.exe register --url https://gitlab.cee.redhat.com --tag-list "windows"
```

## Test Coverage

### What's Tested
- ✅ OS detection (Linux, macOS, Windows)
- ✅ Directory conventions per platform
- ✅ Directory creation and management
- ✅ File operations
- ✅ Path separators and line endings
- ✅ Executable extensions
- ✅ Shell detection
- ✅ Python executable location

### What's NOT Tested Yet
- ⏳ GUI operations (not applicable for CLI tool)
- ⏳ VPN configuration (requires credentials)
- ⏳ Case API integration (requires Red Hat SSO)
- ⏳ Hydra API integration (requires VPN)

## Adding New Tests

1. Create test file: `tests/test_your_feature.py`
2. Follow existing test structure
3. Add to CI/CD workflows:
   - `.github/workflows/cross-platform-test.yml`
   - `.gitlab-ci.yml`
4. Run locally to verify
5. Commit and push

## Troubleshooting

### Tests fail on macOS
- Check Homebrew is installed
- Verify Python 3.11+ available
- Check `platformdirs` and `keyring` packages installed

### Tests fail on Windows
- Check Python added to PATH
- Verify pip works
- Check AppData directory permissions

### CI/CD not running
- **GitHub:** Check repository settings → Actions enabled
- **GitLab:** Check `.gitlab-ci.yml` syntax with CI Lint tool

## Reference

- **Platform Abstraction:** `foundation/platform.py`
- **PAI Gold Standard:** `docs/PAI-GOLD-STANDARD-INDEX.md`
- **OS-Agnostic Framework:** `docs/OS-AGNOSTIC-FRAMEWORK.md`

---

**Goal:** Achieve **A+ grade** for OS-Agnostic support through comprehensive automated testing on all platforms.

**Current:** A (Architecture complete, Linux validated)  
**Target:** A+ (All platforms tested and production-validated)
