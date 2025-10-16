#!/bin/bash
# RFE Automation Tool - Fully Automated Installation Script
# Zero-dependency-hell installation for Red Hat TAM laptops
# FULLY AUTOMATED - No user interaction required

set -euo pipefail

# Non-interactive mode
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a
export ANSIBLE_FORCE_COLOR=0

echo "🚀 RFE Automation Tool - Smart Installation"
echo "=============================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}ℹ${NC}  $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC}  $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

# Platform detection
detect_platform() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
            rhel|centos|rocky|almalinux)
                echo "rhel"
                ;;
            fedora)
                echo "fedora"
                ;;
            *)
                echo "unknown"
                ;;
        esac
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Install UV package manager
install_uv() {
    log_info "Installing UV package manager (fast Python package manager)..."
    
    # Non-interactive UV installation
    if curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --yes &> /tmp/uv-install.log; then
        # Add to current session
        export PATH="$HOME/.cargo/bin:$PATH"
        
        # Add to shell config
        if [ -f "$HOME/.bashrc" ]; then
            if ! grep -q 'cargo/bin' "$HOME/.bashrc"; then
                echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> "$HOME/.bashrc"
            fi
        fi
        
        log_success "UV installed successfully"
        return 0
    else
        log_warning "UV installation failed, will try alternative methods"
        return 1
    fi
}

# Note: System package installation removed - users should not need sudo/dnf

# Install via pip with virtual environment
install_via_pip() {
    log_info "Installing via pip with virtual environment..."
    
    # Check if python3 is available
    if ! command_exists python3; then
        log_error "Python 3 is not installed. Please install Python 3 first."
        return 1
    fi
    
    # Check Python version
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    log_info "Detected Python version: $python_version"
    
    if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'; then
        log_warning "Python 3.8+ recommended, but found $python_version"
        log_info "Installation will continue but may have issues"
    fi
    
    # Create virtual environment
    log_info "Creating virtual environment..."
    if ! python3 -m venv .venv; then
        log_error "Failed to create virtual environment"
        log_info "Try installing: sudo dnf install python3-venv"
        return 1
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Upgrade pip (quietly, non-interactive)
    log_info "Upgrading pip..."
    python3 -m pip install --upgrade pip --quiet --no-input &> /dev/null || true
    
    # Install rhcase and dependencies (non-interactive)
    log_info "Installing rhcase and dependencies..."
    if python3 -m pip install ./rhcase --quiet --no-input &> /tmp/rfe-pip-install.log; then
        log_success "Installation complete via pip+venv"
        
        # Create activation helper
        cat > ./activate-rfe << 'EOF'
#!/bin/bash
# Activate RFE Automation environment
source "$(dirname "$0")/.venv/bin/activate"
echo "✅ RFE Automation environment activated"
echo "Run: ./bin/tam-rfe-chat"
EOF
        chmod +x ./activate-rfe
        
        log_info "To use the tool, first run: source .venv/bin/activate"
        log_info "Or use: ./activate-rfe"
        return 0
    else
        log_error "pip installation failed"
        cat /tmp/rfe-pip-install.log
        return 1
    fi
}

# Main installation logic
main() {
    echo ""
    log_info "Detecting platform..."
    PLATFORM=$(detect_platform)
    log_info "Platform detected: $PLATFORM"
    echo ""
    
    # Check for git
    if ! command_exists git; then
        log_error "Git is required but not installed"
        case "$PLATFORM" in
            rhel|fedora)
                log_info "Install with: sudo dnf install git"
                ;;
            macos)
                log_info "Install with: brew install git"
                ;;
            *)
                log_info "Please install git for your platform"
                ;;
        esac
        exit 1
    fi
    log_success "Git is installed"
    
    # Clone/update rhcase from GitLab
RHCASE_DIR="./rhcase"
RHCASE_REPO="https://gitlab.cee.redhat.com/gvaughn/rhcase.git"

log_info "Getting latest rhcase from GitLab..."

# Robust git repository detection (handles submodules, regular repos, and non-repos)
if [ -d "$RHCASE_DIR" ] && git -C "$RHCASE_DIR" rev-parse --git-dir &> /dev/null; then
    log_info "Updating existing rhcase..."
    
    # Handle detached HEAD state (common in submodules)
    if (cd "$RHCASE_DIR" && git symbolic-ref -q HEAD &> /dev/null); then
        # Normal branch state - safe to pull
        if git -C "$RHCASE_DIR" pull origin main &> /tmp/rhcase-update.log; then
            log_success "rhcase updated to latest version"
        else
            log_warning "rhcase update failed, using existing version"
        fi
    else
        # Detached HEAD (submodule) - fetch and reset to latest
        log_info "Detached HEAD detected (submodule), fetching latest..."
        if (cd "$RHCASE_DIR" && git fetch origin main &> /tmp/rhcase-fetch.log && git reset --hard origin/main &> /tmp/rhcase-reset.log); then
            log_success "rhcase updated to latest version"
        else
            log_warning "rhcase update failed, using existing version"
        fi
    fi
elif [ -d "$RHCASE_DIR" ]; then
    # Directory exists but isn't a git repo - remove and clone fresh
    log_warning "rhcase directory exists but isn't a valid git repository"
    log_info "Removing and cloning fresh..."
    rm -rf "$RHCASE_DIR"
    if git clone "$RHCASE_REPO" "$RHCASE_DIR" &> /tmp/rhcase-clone.log; then
        log_success "rhcase cloned successfully"
    else
        log_error "Failed to clone rhcase from GitLab"
        log_info "This requires Red Hat VPN access"
        log_info "Check: https://gitlab.cee.redhat.com/gvaughn/rhcase"
        cat /tmp/rhcase-clone.log
        exit 1
    fi
else
    # Directory doesn't exist - clone fresh
    log_info "Cloning rhcase from GitLab..."
    if git clone "$RHCASE_REPO" "$RHCASE_DIR" &> /tmp/rhcase-clone.log; then
        log_success "rhcase cloned successfully"
    else
        log_error "Failed to clone rhcase from GitLab"
        log_info "This requires Red Hat VPN access"
        log_info "Check: https://gitlab.cee.redhat.com/gvaughn/rhcase"
        log_info ""
        log_info "Clone output:"
        cat /tmp/rhcase-clone.log
        exit 1
    fi
fi
    
    # Try installation methods in order of preference
    echo ""
    log_info "Attempting installation (user-space only, no sudo required)..."
    echo ""
    
    # Method 1: UV (fast, isolated, works everywhere)
    log_info "Method 1: Trying UV package manager..."
    if command_exists uv || install_uv; then
        log_info "Installing rhcase via UV..."
        if uv tool install ./rhcase &> /tmp/rfe-uv-install.log; then
            log_success "UV installation successful"
            
            echo ""
            log_success "🎉 Installation Complete!"
            log_info "Run: rhcase --version"
            log_info "Run: ./bin/tam-rfe-chat"
            exit 0
        else
            log_warning "UV installation failed"
        fi
    fi
    log_warning "UV method failed, trying pip..."
    echo ""
    
    # Method 2: pip with venv (fallback, always works)
    log_info "Method 2: Using pip with virtual environment..."
    if install_via_pip; then
        echo ""
        log_success "🎉 Installation Complete!"
        log_info "Activate environment: source .venv/bin/activate"
        log_info "Then run: ./bin/tam-rfe-chat"
        exit 0
    fi
    
    # If we get here, all methods failed
    echo ""
    log_error "All installation methods failed"
    log_error "Please check the logs in /tmp/rfe-*.log"
    log_info "Manual installation steps:"
    log_info "  1. Install Python 3.8+: sudo dnf install python3 python3-pip"
    log_info "  2. Install dependencies: sudo dnf install python3-requests python3-pyyaml"
    log_info "  3. Install rhcase: python3 -m pip install --user ./rhcase"
    exit 1
}

# Run main installation
main "$@"


