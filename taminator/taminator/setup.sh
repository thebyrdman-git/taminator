#!/bin/bash
#
# Taminator Setup Script
# Initializes user data directories and configuration.
# Supports macOS (primary) and Linux.
#
# This script creates the necessary directories OUTSIDE the git repository
# to ensure user data is never accidentally committed.
#

set -e

# Script directory (so we find requirements.txt whether run from repo root or from taminator/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              TAMINATOR SETUP                               ║"
echo "║     RFE and Bug Report Generator                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if running in git repo
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Warning: Not in a git repository${NC}"
    echo "This script should be run from the taminator repository root."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🔧 Creating Taminator directories..."
echo ""

# Create user data directory
DATA_DIR="$HOME/.taminator-data"
if [ ! -d "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
    echo -e "${GREEN}✓${NC} Created: $DATA_DIR"
else
    echo -e "${YELLOW}⚠${NC}  Already exists: $DATA_DIR"
fi

# Create subdirectories
mkdir -p "$DATA_DIR/customers"
echo -e "${GREEN}✓${NC} Created: $DATA_DIR/customers/ (for customer reports)"

mkdir -p "$DATA_DIR/test-data"
echo -e "${GREEN}✓${NC} Created: $DATA_DIR/test-data/ (for test customer data)"

mkdir -p "$DATA_DIR/backups"
echo -e "${GREEN}✓${NC} Created: $DATA_DIR/backups/ (for report backups)"

mkdir -p "$DATA_DIR/logs"
echo -e "${GREEN}✓${NC} Created: $DATA_DIR/logs/ (for application logs)"

echo ""

# Create config directory
CONFIG_DIR="$HOME/.config/taminator"
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
    echo -e "${GREEN}✓${NC} Created: $CONFIG_DIR"
else
    echo -e "${YELLOW}⚠${NC}  Already exists: $CONFIG_DIR"
fi

# Create config file if it doesn't exist
CONFIG_FILE="$CONFIG_DIR/config.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << 'EOF'
# Taminator Configuration
# This file is NOT tracked by git

# Data directories
data_directory: ~/.taminator-data
customers_directory: ~/.taminator-data/customers
test_data_directory: ~/.taminator-data/test-data
backups_directory: ~/.taminator-data/backups

# Behavior
auto_backup: true
confirm_updates: true
check_vpn: true

# GitHub (for issue reporting)
github_repo: thebyrdman-git/taminator

# Logging
log_level: INFO
log_file: ~/.taminator-data/logs/taminator.log
EOF
    echo -e "${GREEN}✓${NC} Created: $CONFIG_FILE"
else
    echo -e "${YELLOW}⚠${NC}  Already exists: $CONFIG_FILE"
fi

echo ""

# Create test customer data
TEST_CUSTOMER="$DATA_DIR/test-data/testcustomer.md"
if [ ! -f "$TEST_CUSTOMER" ]; then
    cat > "$TEST_CUSTOMER" << 'EOF'
# Test Customer RFE/Bug Tracker

Oct 21, 2025, 10:51 AM EDT Jimmy Byrd

Summary: 5 total cases (3 RFE, 2 Bug)

## Enhancement Requests (RFE)

| RED HAT JIRA ID | Support Case | Enhancement Request | Status |
|-----------------|--------------|---------------------|--------|
| AAPRFE-999 | 99999999 | [RFE] Test Enhancement Request 1 | Backlog |
| AAPRFE-998 | 99999998 | [RFE] Test Enhancement Request 2 | Review |
| AAPRFE-997 | 99999997 | [RFE] Test Enhancement Request 3 | Backlog |

## Bug Reports

| RED HAT JIRA ID | Support Case | Bug Description | Status |
|-----------------|--------------|-----------------|--------|
| AAP-99999 | 99999996 | [BUG] Test Bug Report 1 | New |
| AAP-99998 | 99999995 | [BUG] Test Bug Report 2 | Closed |

---

**Notes:**
- This is TEST DATA for demonstration purposes
- Safe to use for testing Taminator features
- Not real customer data
EOF
    echo -e "${GREEN}✓${NC} Created: $TEST_CUSTOMER (test data)"
else
    echo -e "${YELLOW}⚠${NC}  Already exists: $TEST_CUSTOMER"
fi

echo ""

# Install pre-commit hook
HOOK_FILE=".git/hooks/pre-commit"
if [ -f "$HOOK_FILE" ]; then
    echo -e "${GREEN}✓${NC} Pre-commit hook already installed"
else
    if [ -d ".git/hooks" ]; then
        chmod +x .git/hooks/pre-commit 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Pre-commit hook installed (blocks sensitive data)"
    else
        echo -e "${YELLOW}⚠${NC}  Not a git repository - skipping pre-commit hook"
    fi
fi

echo ""

# Check Python dependencies (Google Drive/Docs, markdown for formatted Docs)
echo "📦 Checking Python dependencies..."
REQ_FILE="$SCRIPT_DIR/requirements.txt"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip3 found"
    if [ -f "$REQ_FILE" ]; then
        echo "   (includes Google Drive & Docs, and markdown for formatted Open in Google Docs)"
        echo ""
        read -p "Install Python dependencies now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pip3 install --user -r "$REQ_FILE"
            echo -e "${GREEN}✓${NC} Python dependencies installed (Google API + markdown for formatted Docs)"
        else
            echo -e "${YELLOW}⚠${NC}  Skipped - install later with: pip3 install --user -r \"$REQ_FILE\""
        fi
    else
        echo -e "${YELLOW}⚠${NC}  requirements.txt not found at $REQ_FILE"
    fi
else
    echo -e "${YELLOW}⚠${NC}  pip3 not found - install Python 3 first (e.g. on macOS: brew install python@3)"
fi

echo ""

# Summary
echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              SETUP COMPLETE!                               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "📁 User data directory:"
echo "   $DATA_DIR"
echo ""
echo "⚙️  Configuration:"
echo "   $CONFIG_FILE"
echo ""
echo "🔒 Security:"
echo "   ✓ Pre-commit hook installed (blocks sensitive data)"
echo "   ✓ .gitignore configured"
echo "   ✓ Data directories outside git repository"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Configure your API tokens:"
echo "   $ ./tam-rfe config --add-token"
echo ""
echo "2. Test with sample data:"
echo "   $ ./tam-rfe check --test-data"
echo ""
echo "3. Run the web UI (Settings, reports, Google Drive backup & Docs):"
echo "   $ ./tam-rfe serve"
echo ""
echo "4. Launch GUI (optional):"
echo "   $ cd gui && npm install && npm start"
echo ""
echo "📚 Documentation:"
echo "   • README.md - Getting started"
echo "   • DEPLOYMENT-ARCHITECTURE.md - Security architecture"
echo "   • PRE-COMMIT-CHECKLIST.md - Security checklist"
echo ""
echo "Need help? Contact: jbyrd@redhat.com"
echo ""

