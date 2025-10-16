#!/bin/bash
# Create Offline Installation Package for RFE Bug Tracker Automation
# For colleagues without access to gitlab.cee.redhat.com

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PACKAGE_NAME="rfe-bug-tracker-automation-offline"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_DIR="/tmp/${PACKAGE_NAME}_${TIMESTAMP}"
TARBALL="${PACKAGE_NAME}_${TIMESTAMP}.tar.gz"

echo "🎁 Creating Offline Installation Package"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ${NC}  $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC}  $1"; }

# Create temporary package directory
log_info "Creating package directory..."
mkdir -p "$PACKAGE_DIR"

# Copy repository excluding large/unnecessary files
log_info "Copying repository files (excluding .git, output, logs, etc.)..."
cd "$PROJECT_ROOT"

rsync -av \
  --exclude='.git' \
  --exclude='.vagrant' \
  --exclude='rhcase/.venv' \
  --exclude='rhcase/.git' \
  --exclude='output/' \
  --exclude='logs/' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.pyo' \
  --exclude='.pytest_cache' \
  --exclude='*.log' \
  --exclude='.DS_Store' \
  --exclude='*.swp' \
  --exclude='*~' \
  . "$PACKAGE_DIR/"

log_success "Repository copied"

# Create installation instructions
log_info "Creating installation instructions..."
cat > "$PACKAGE_DIR/OFFLINE-INSTALL.md" << 'EOF'
# RFE Bug Tracker Automation - Offline Installation

## Package Contents

This offline package contains everything needed to install the RFE Bug Tracker Automation tool without access to gitlab.cee.redhat.com.

**Included:**
- Complete RFE automation tool codebase
- rhcase submodule (without .venv - will be built locally)
- All scripts, templates, and configurations
- Offline installer script
- Documentation

**Excluded (will be built locally):**
- Python virtual environments
- Git history
- Generated output files
- Log files

## Prerequisites

**Required:**
- Red Hat VPN access (for case data access)
- Python 3.8 or higher
- Git (for rhcase submodule initialization)

**System Requirements:**
- RHEL 8/9, Rocky 8/9, AlmaLinux 8/9, or Fedora
- 2GB RAM minimum
- 500MB disk space

## Installation Steps

### 1. Extract Package

```bash
tar -xzf rfe-bug-tracker-automation-offline_*.tar.gz
cd rfe-bug-tracker-automation-offline_*/
```

### 2. Run Offline Installer

```bash
# Fully automated installation
./scripts/installation/install-offline.sh
```

The installer will:
- Detect your platform (RHEL/Rocky/Alma/Fedora)
- Install required system packages
- Initialize rhcase submodule
- Set up Python virtual environment for rhcase
- Install Python dependencies
- Set up tamscripts configuration
- Make all scripts executable

### 3. Verify Installation

```bash
# Test rhcase installation
./rhcase/.venv/bin/rhcase --version

# List available tools
ls -1 bin/tam-rfe-*
```

### 4. Configure Your Environment

```bash
# Configure tamscripts for your user
mkdir -p ~/.config/tamscripts
cp rhcase/examples/tamscripts.config.example ~/.config/tamscripts/tamscripts.config

# Edit with your accounts
nano ~/.config/tamscripts/tamscripts.config
```

### 5. Onboard Your First Customer

```bash
# Interactive intelligent onboarding
./bin/tam-rfe-onboard-intelligent

# Or discover customers first
./bin/tam-rfe-discover-customers-hydra geo NAMER
./bin/tam-rfe-hydra-api org Commercial
```

## Quick Start

After installation, try these commands:

```bash
# Discover customers by region
./bin/tam-rfe-discover-customers-hydra geo APAC

# Search for a customer
./bin/tam-rfe-hydra-api search "Customer Name"

# Intelligent customer onboarding
./bin/tam-rfe-onboard-intelligent

# Natural language case interface
./bin/tam-rfe-chat

# Validate configuration
./bin/tam-rfe-validate-intelligence westpac
```

## Documentation

**In this package:**
- `README.md` - Main documentation
- `GETTING-STARTED.md` - Quick start guide
- `INSTALLATION-GUIDE.md` - Detailed installation
- `HYDRA-PHASES-OVERVIEW.md` - Customer discovery overview
- `DIRECTORY-STRUCTURE.md` - Repository structure

**Online (when on VPN):**
- GitLab: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation

## Troubleshooting

### Python Version Issues
If you have Python version issues:
```bash
# Check Python version
python3 --version

# Fedora: Install Python 3.11+
sudo dnf install python3.11

# RHEL 9: Python 3.9 is default (supported)
```

### rhcase Installation Fails
If rhcase installation fails:
```bash
# Manual rhcase setup
cd rhcase
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Permission Issues
If you get permission errors:
```bash
# Make scripts executable
chmod +x bin/*
chmod +x scripts/**/*.sh
```

### Network/VPN Required
Some features require Red Hat VPN:
- Case data access (rhcase)
- Hydra API queries
- Customer discovery

## Support

**Internal Red Hat:**
- GitLab Issues: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/issues
- Slack: #tam-automation (if it exists)
- Email: jbyrd@redhat.com

## What's Included in This Release

### Hydra API Customer Discovery
- **Phase 1:** Geographic discovery (APAC, EMEA, NAMER, LATAM, India)
- **Phase 2:** Organizational discovery (NAPS, Commercial)
- **Phase 3:** Blocked (awaiting Hydra org API endpoints)

### TAM Tools (70+ scripts)
- `tam-rfe-chat` - Natural language case interface
- `tam-rfe-onboard-intelligent` - Smart customer onboarding
- `tam-rfe-discover-customers-hydra` - Geographic discovery
- `tam-rfe-hydra-api` - Organizational discovery
- `tam-rfe-validate-intelligence` - Config validation
- And 65+ more...

### Intelligence Features
- Dynamic customer onboarding
- Automated configuration updates
- Real-time case searching
- Intelligent monitoring
- Portfolio analytics

## Version Information

**Package Date:** $(date +"%B %d, %Y")
**Created By:** Hatter (Red Hat Digital Assistant)
**Project:** RFE Bug Tracker Automation
**Repository:** rfe-bug-tracker-automation

---

**Happy Automating!** 🚀
EOF

log_success "Installation instructions created"

# Create a README in the package root
cat > "$PACKAGE_DIR/README-FIRST.txt" << 'EOF'
RFE Bug Tracker Automation - Offline Installation Package
===========================================================

QUICK START:

1. Read OFFLINE-INSTALL.md for complete instructions

2. Run the installer:
   ./scripts/installation/install-offline.sh

3. Start using:
   ./bin/tam-rfe-discover-customers-hydra geo APAC

REQUIREMENTS:
- Red Hat VPN access
- Python 3.8+
- RHEL/Rocky/Alma/Fedora

DOCUMENTATION:
- OFFLINE-INSTALL.md    (installation guide)
- README.md             (project overview)
- GETTING-STARTED.md    (quick start)
- HYDRA-PHASES-OVERVIEW.md (customer discovery)

SUPPORT:
- GitLab: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
- Email: jbyrd@redhat.com
EOF

log_success "Quick start guide created"

# Create checksums
log_info "Creating checksums..."
cd "$PACKAGE_DIR"
find . -type f -exec sha256sum {} \; > CHECKSUMS.txt
log_success "Checksums created"

# Create tarball
log_info "Creating compressed tarball..."
cd /tmp
tar -czf "$TARBALL" "${PACKAGE_NAME}_${TIMESTAMP}/"
TARBALL_SIZE=$(du -h "$TARBALL" | cut -f1)
log_success "Tarball created: $TARBALL ($TARBALL_SIZE)"

# Calculate final checksum
TARBALL_SHA=$(sha256sum "$TARBALL" | cut -d' ' -f1)

# Create transfer instructions
cat > "/tmp/${PACKAGE_NAME}_${TIMESTAMP}_TRANSFER.txt" << EOF
RFE Bug Tracker Automation - Offline Package Transfer Instructions
====================================================================

PACKAGE INFORMATION:
  File: $TARBALL
  Size: $TARBALL_SIZE
  SHA256: $TARBALL_SHA
  Created: $(date)

TRANSFER OPTIONS:

1. USB Drive (Recommended for large files)
   - Copy $TARBALL to USB drive
   - Verify checksum on target system:
     sha256sum $TARBALL

2. SCP (if limited network access)
   scp $TARBALL user@target-host:/tmp/

3. Shared Network Drive
   - Copy to shared location
   - Verify checksum after transfer

INSTALLATION ON TARGET SYSTEM:

1. Verify checksum:
   echo "$TARBALL_SHA  $TARBALL" | sha256sum -c

2. Extract:
   tar -xzf $TARBALL
   cd ${PACKAGE_NAME}_${TIMESTAMP}/

3. Read instructions:
   cat README-FIRST.txt
   cat OFFLINE-INSTALL.md

4. Run installer:
   ./scripts/installation/install-offline.sh

NOTES:
- This package does NOT require gitlab.cee access
- Red Hat VPN IS required for case data access
- Package includes all code, scripts, and documentation
- Python virtual environments will be built locally

SUPPORT:
  GitLab: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
  Email: jbyrd@redhat.com
EOF

log_success "Transfer instructions created"

# Summary
echo ""
echo "================================================"
echo "📦 Offline Package Created Successfully"
echo "================================================"
echo ""
echo "Package Details:"
echo "  📁 Directory: ${PACKAGE_NAME}_${TIMESTAMP}/"
echo "  📦 Tarball: $TARBALL"
echo "  📊 Size: $TARBALL_SIZE"
echo "  🔐 SHA256: $TARBALL_SHA"
echo ""
echo "Files Created:"
echo "  ✅ /tmp/$TARBALL"
echo "  ✅ /tmp/${PACKAGE_NAME}_${TIMESTAMP}_TRANSFER.txt"
echo ""
echo "Next Steps:"
echo "  1. Read transfer instructions:"
echo "     cat /tmp/${PACKAGE_NAME}_${TIMESTAMP}_TRANSFER.txt"
echo ""
echo "  2. Transfer to colleague via USB/SCP/Network"
echo ""
echo "  3. Colleague extracts and runs:"
echo "     tar -xzf $TARBALL"
echo "     cd ${PACKAGE_NAME}_${TIMESTAMP}/"
echo "     ./scripts/installation/install-offline.sh"
echo ""
echo "Package Location: /tmp/$TARBALL"
echo ""

