# RFE Automation Tool - Installation Testing Plan

**Goal**: Zero-dependency-hell installation that works out-of-the-box on Red Hat TAM laptops

**Date**: October 15, 2025  
**Status**: 🚧 Planning Phase

---

## 🎯 Target Platforms (Priority Order)

### 1. **RHEL 9.x** (Primary - Most TAM laptops)
- Clean RHEL 9.5 installation
- Standard Corporate Standard Build (CSB) configuration
- Only base system packages installed

### 2. **Fedora 40/41** (Secondary - Developer laptops)
- Clean Fedora Workstation installation
- Standard developer environment

### 3. **RHEL 8.x** (Legacy - Some TAM laptops)
- Clean RHEL 8.10 installation
- Older TAM laptops

---

## 📦 Dependency Analysis

### **Currently Required**:
```
git                 # For cloning repo
python3             # Runtime
python3-devel       # For building Python packages
gcc                 # For building Python packages (cryptography)
openssl-devel       # For building Python packages (cryptography)
libffi-devel        # For building Python packages (cryptography)
```

### **Python Packages** (from rhcase):
```
requests>=2.25.0
PyYAML>=6.0
rich>=13.0.0
aiohttp>=3.8.0
requests-oauthlib>=1.3.1
cryptography>=45.0.6
jinja2>=3.0.0
markdownify>=1.2.0
html2text>=2024.2.26
packaging>=21.0
psutil>=5.9.0
jira>=3.8.0
```

---

## 🚨 Current Installation Problems

### Problem 1: Missing System Dependencies
```bash
# Current install-dependencies doesn't install build tools
# Installing cryptography WILL FAIL without gcc, openssl-devel, etc.
```

### Problem 2: No Python Package Installation
```bash
# Current script only CHECKS for packages, doesn't install them
# TAMs will hit "ModuleNotFoundError" immediately
```

### Problem 3: Submodule Complexity
```bash
# Requires git submodule knowledge
# Can fail if GitLab auth not configured
```

### Problem 4: No Isolation
```bash
# pip3 install pollutes user's Python environment
# Conflicts with other tools possible
```

---

## ✅ Proposed Solution: Three Installation Methods

### **Method 1: System Package Installation (Easiest - RHEL/Fedora Only)**

**Pros**:
- Uses system package manager (dnf)
- No build dependencies needed
- System packages are tested and stable
- No virtual environment needed

**Cons**:
- Only works on RHEL/Fedora
- Package names differ between versions
- Slower package updates

**Implementation**:
```bash
#!/bin/bash
# install-system-packages.sh

# Install ALL system packages needed
sudo dnf install -y \
    git \
    python3 \
    python3-requests \
    python3-pyyaml \
    python3-rich \
    python3-aiohttp \
    python3-jinja2 \
    python3-cryptography \
    python3-packaging \
    python3-psutil

# rhcase from source (no system package available)
```

---

### **Method 2: UV Package Manager (Recommended - Cross-platform)**

**Pros**:
- 10-100x faster than pip
- Automatic virtual environment isolation
- No dependency conflicts
- Works on all platforms
- Single binary installation

**Cons**:
- Requires downloading uv binary first
- Less familiar to TAMs

**Implementation**:
```bash
#!/bin/bash
# install-with-uv.sh

# Install uv (one command, no dependencies)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install rhcase and all dependencies
uv tool install ./rhcase

# Creates isolated environment automatically
```

---

### **Method 3: Pipx Installation (Middle Ground)**

**Pros**:
- Automatic isolation
- Familiar to Python users
- Handles dependencies well
- Available as system package

**Cons**:
- Still needs build dependencies
- Slower than uv

**Implementation**:
```bash
#!/bin/bash
# install-with-pipx.sh

# Install pipx via system package
sudo dnf install -y pipx
pipx ensurepath

# Install build dependencies
sudo dnf install -y gcc python3-devel openssl-devel libffi-devel

# Install rhcase
pipx install ./rhcase
```

---

## 🧪 Testing Matrix

### Test Environments

| Platform | Version | VM Provider | Setup Time |
|----------|---------|-------------|------------|
| RHEL | 9.5 | Vagrant/libvirt | 10 min |
| RHEL | 8.10 | Vagrant/libvirt | 10 min |
| Fedora | 41 | Vagrant/libvirt | 5 min |
| Fedora | 40 | Vagrant/libvirt | 5 min |

### Test Scenarios

#### **Scenario 1: Fresh RHEL 9.5 (CSB Equivalent)**
```bash
# Start with minimal RHEL installation
# NO developer tools installed
# Only standard CSB packages

# Test: Run install script
# Expected: Complete installation in < 5 minutes
# Expected: No errors, no manual intervention needed
```

#### **Scenario 2: Fresh Fedora 41 (Developer Laptop)**
```bash
# Start with Fedora Workstation
# Standard developer tools (git, python3, gcc)

# Test: Run install script
# Expected: Complete installation in < 3 minutes
# Expected: Detects existing tools, skips unnecessary steps
```

#### **Scenario 3: RHEL 8.10 (Legacy TAM Laptop)**
```bash
# Start with RHEL 8.10
# Python 3.6 or 3.8

# Test: Run install script
# Expected: Warns about Python version if needed
# Expected: Installs compatible versions or upgrades Python
```

---

## 📝 Automated Testing Script

```bash
#!/bin/bash
# test-installation.sh

# Create test matrix
PLATFORMS=(
    "almalinux/9:rhel-9"
    "almalinux/8:rhel-8"
    "fedora:41"
    "fedora:40"
)

for platform in "${PLATFORMS[@]}"; do
    image="${platform%:*}"
    name="${platform#*:}"
    
    echo "Testing on $name..."
    
    # Create container
    podman run --rm -it \
        --name "rfe-test-$name" \
        "$image" \
        bash -c "
            # Simulate fresh system
            cd /tmp
            
            # Clone repo
            dnf install -y git
            git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
            cd rfe-and-bug-tracker-automation
            
            # Test installation
            time ./install.sh
            
            # Verify
            ./bin/tam-rfe-chat --version
        "
    
    if [ $? -eq 0 ]; then
        echo "✅ $name: PASSED"
    else
        echo "❌ $name: FAILED"
    fi
done
```

---

## 🎯 Recommended Approach

### **Primary Installation Method: UV (Universal)**

**Why UV?**:
1. **No Build Dependencies**: Pre-built wheels, no gcc needed
2. **Fast**: 10-100x faster than pip
3. **Isolated**: Automatic virtual environments
4. **Simple**: One command installation
5. **Cross-Platform**: Works on RHEL, Fedora, macOS

**Fallback Method: System Packages (RHEL/Fedora Only)**

### **Improved install.sh Structure**:
```bash
#!/bin/bash
# Detect platform
PLATFORM=$(detect_platform)

if [[ "$PLATFORM" == "rhel" ]] || [[ "$PLATFORM" == "fedora" ]]; then
    # Method 1: Try system packages first (fastest, no build needed)
    if try_system_packages; then
        echo "✅ Installed via system packages"
        exit 0
    fi
fi

# Method 2: Try UV (works everywhere)
if command -v uv &> /dev/null || install_uv; then
    uv tool install ./rhcase
    echo "✅ Installed via UV"
    exit 0
fi

# Method 3: Fallback to pipx
if install_pipx; then
    install_build_dependencies
    pipx install ./rhcase
    echo "✅ Installed via pipx"
    exit 0
fi

# Method 4: Last resort - pip with venv
python3 -m venv .venv
source .venv/bin/activate
pip install ./rhcase
echo "✅ Installed via pip+venv"
```

---

## 🚀 Action Items

### Immediate (This Week)
- [ ] Create Vagrant test environments for RHEL 9, RHEL 8, Fedora 41
- [ ] Build new install.sh with UV-first approach
- [ ] Test on vanilla RHEL 9.5
- [ ] Document system package mapping for RHEL/Fedora

### Short-term (Next Week)
- [ ] Build automated testing script
- [ ] Test on all target platforms
- [ ] Create TAM-friendly documentation
- [ ] Record installation demo video

### Long-term (Next Month)
- [ ] Build RPM package for RHEL/Fedora
- [ ] Submit to Red Hat internal repositories
- [ ] Create one-liner installation URL

---

## 💡 TAM-Friendly Installation Goal

### **The Dream**:
```bash
# Single command that works on ANY Red Hat laptop
curl -sSL https://rfe.automation.redhat.com/install | bash

# Or even better, RPM package
sudo dnf install rh-tam-rfe-automation
```

### **The Reality (Phase 1)**:
```bash
# Three commands that work reliably
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation
./install.sh  # Handles everything automatically
```

---

## 📊 Success Metrics

### Installation Success
- ✅ Works on vanilla RHEL 9.5 (no errors)
- ✅ Works on vanilla Fedora 41 (no errors)
- ✅ Works on RHEL 8.10 (with warnings OK)
- ✅ No manual dependency installation needed
- ✅ No "ModuleNotFoundError" or "command not found"

### User Experience
- ✅ Total installation time < 5 minutes
- ✅ Zero manual intervention required
- ✅ Clear progress indicators
- ✅ Helpful error messages with solutions

### Compatibility
- ✅ Doesn't break existing Python tools
- ✅ Doesn't require sudo (except for system packages)
- ✅ Works with Red Hat VPN on/off (for installation)
- ✅ Survives system updates

---

*Next Step: Create vagrant test environments and build improved installer*


