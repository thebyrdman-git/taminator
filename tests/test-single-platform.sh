#!/bin/bash
# Quick single-platform test for rapid validation
# Fully automated, no user interaction

set -euo pipefail

# Configuration
PLATFORM="${1:-fedora:41}"
TEST_DIR="$HOME/.cache/rfe-quick-test-$$"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ${NC}  $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

echo "🧪 Quick Installation Test"
echo "=========================="
echo "Platform: $PLATFORM"
echo ""

# Create test directory
log_info "Creating test workspace..."
mkdir -p "$TEST_DIR"

# Copy project (excluding build artifacts)
log_info "Copying project files..."
rsync -a --quiet \
    --exclude='.venv' \
    --exclude='output/' \
    --exclude='logs/' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='rhcase' \
    "$PROJECT_DIR/" "$TEST_DIR/rfe-automation/"

log_success "Test workspace ready"
echo ""

# Run test
log_info "Starting container test..."
echo ""

if podman run --rm \
    -v "$TEST_DIR/rfe-automation:/test:Z" \
    "$PLATFORM" \
    bash -c '
        set -e
        
        # Non-interactive mode
        export DEBIAN_FRONTEND=noninteractive
        
        echo "=== Installing prerequisites (git + python3) ==="
        dnf install -y git python3 2>&1 | grep -v "^Importing GPG key" || true
        
        echo ""
        echo "=== Running install-improved.sh ==="
        cd /test
        bash -x ./install-improved.sh 2>&1 | tail -50
        
        echo ""
        echo "=== Verifying installation ==="
        
        # Check for rhcase in various locations
        if command -v rhcase &> /dev/null; then
            echo "✅ rhcase found in PATH"
            rhcase --version
            exit 0
        elif [ -f ~/.local/bin/rhcase ]; then
            echo "✅ rhcase found in ~/.local/bin"
            ~/.local/bin/rhcase --version
            exit 0
        elif [ -f .venv/bin/rhcase ]; then
            echo "✅ rhcase found in .venv"
            .venv/bin/rhcase --version
            exit 0
        else
            echo "❌ rhcase not found"
            echo "Checking directories:"
            ls -la ~/.local/bin/ 2>/dev/null || echo "~/.local/bin/ does not exist"
            ls -la .venv/bin/ 2>/dev/null || echo ".venv/bin/ does not exist"
            exit 1
        fi
    ' 2>&1 | tee "$TEST_DIR/test.log"
then
    echo ""
    echo "=========================================="
    log_success "TEST PASSED: $PLATFORM"
    echo "=========================================="
    
    # Clean up on success
    rm -rf "$TEST_DIR"
    exit 0
else
    echo ""
    echo "=========================================="
    log_error "TEST FAILED: $PLATFORM"
    echo "=========================================="
    log_info "Log saved: $TEST_DIR/test.log"
    log_info "View with: cat $TEST_DIR/test.log"
    exit 1
fi

