#!/bin/bash
# Automated Installation Testing for RFE Automation
# Tests installation on multiple platforms using containers

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ${NC}  $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }
log_test() { echo -e "${YELLOW}🧪${NC} $1"; }

# Test platforms
PLATFORMS=(
    "almalinux:9:RHEL 9 (AlmaLinux)"
    "almalinux:8:RHEL 8 (AlmaLinux)"
    "fedora:41:Fedora 41"
    "fedora:40:Fedora 40"
)

RESULTS=()
TOTAL=0
PASSED=0
FAILED=0

# Test a single platform
test_platform() {
    local image=$1
    local name=$2
    local test_num=$3
    
    TOTAL=$((TOTAL + 1))
    
    log_test "Test $test_num: $name"
    log_info "Container image: $image"
    
    # Create test directory in home (user has permissions)
    TEST_DIR="$HOME/.cache/rfe-test-$$-$test_num"
    mkdir -p "$TEST_DIR"
    
    # Copy project to test directory (exclude .venv, output, logs)
    rsync -a --exclude='.venv' --exclude='output/' --exclude='logs/' --exclude='__pycache__' --exclude='*.pyc' \
        "$(dirname "$0")/.." "$TEST_DIR/rfe-automation"
    
    # Run test in container
    if podman run --rm \
        -v "$TEST_DIR/rfe-automation:/test:Z" \
        "$image" \
        bash -c "
            set -e
            cd /test
            
            # Install git first (required for submodules)
            dnf install -y git &> /dev/null
            
            # Test installation
            ./install-improved.sh
            
            # Verify rhcase is available
            if command -v rhcase &> /dev/null; then
                echo '✅ rhcase command available'
                rhcase --version
                exit 0
            elif [ -f .venv/bin/rhcase ]; then
                echo '✅ rhcase installed in venv'
                .venv/bin/rhcase --version
                exit 0
            else
                echo '❌ rhcase not found'
                exit 1
            fi
        " &> "$TEST_DIR/test.log"; then
        
        log_success "$name: PASSED"
        RESULTS+=("✅ $name: PASSED")
        PASSED=$((PASSED + 1))
    else
        log_error "$name: FAILED"
        log_info "Log saved to: $TEST_DIR/test.log"
        RESULTS+=("❌ $name: FAILED - Log: $TEST_DIR/test.log")
        FAILED=$((FAILED + 1))
        
        # Show last 20 lines of log for quick diagnosis
        echo ""
        echo "Last 20 lines of log:"
        tail -20 "$TEST_DIR/test.log"
        echo ""
    fi
    
    echo ""
}

# Main test execution
main() {
    echo "🧪 RFE Automation Installation Testing"
    echo "======================================"
    echo ""
    
    # Check if podman is available
    if ! command -v podman &> /dev/null; then
        log_error "Podman is required for testing"
        log_info "Install with: sudo dnf install podman"
        exit 1
    fi
    
    log_success "Podman is available"
    echo ""
    
    # Run tests
    test_num=1
    for platform in "${PLATFORMS[@]}"; do
        IFS=':' read -r image version name <<< "$platform"
        full_image="$image:$version"
        
        test_platform "$full_image" "$name" "$test_num"
        test_num=$((test_num + 1))
    done
    
    # Print summary
    echo "=========================================="
    echo "📊 Test Summary"
    echo "=========================================="
    echo ""
    
    for result in "${RESULTS[@]}"; do
        echo "$result"
    done
    
    echo ""
    echo "Total: $TOTAL | Passed: $PASSED | Failed: $FAILED"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        log_success "All tests passed! 🎉"
        exit 0
    else
        log_error "$FAILED test(s) failed"
        exit 1
    fi
}

# Handle Ctrl+C
trap 'echo ""; log_info "Tests interrupted"; exit 130' INT

# Run tests
main "$@"


