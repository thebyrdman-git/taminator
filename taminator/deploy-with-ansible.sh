#!/bin/bash

# TAM RFE Automation Tool - Ansible Deployment Script
# Automates the complete setup and configuration using Ansible

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANSIBLE_DIR="$SCRIPT_DIR/ansible"
INVENTORY_FILE="$ANSIBLE_DIR/inventory.yml"
PLAYBOOK_FILE="$ANSIBLE_DIR/playbook.yml"
LOG_FILE="$HOME/.config/tam-rfe-automation/ansible-deployment.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${CYAN}"
    echo "🚀 TAM RFE Automation Tool - Ansible Deployment"
    echo "=============================================="
    echo -e "${NC}"
    echo "📅 Deployment started: $(date)"
    echo "🎯 Target: $(hostname)"
    echo "👤 User: $(whoami)"
    echo "📁 Script directory: $SCRIPT_DIR"
    echo "📋 Ansible directory: $ANSIBLE_DIR"
    echo ""
}

print_step() {
    echo -e "${YELLOW}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking deployment prerequisites..."
    
    # Check if Ansible is installed
    if ! command -v ansible-playbook >/dev/null 2>&1; then
        print_error "Ansible is not installed"
        print_info "Installing Ansible..."
        
        # Install Ansible based on platform
        if command -v python3 >/dev/null 2>&1; then
            pip3 install ansible
        elif command -v python >/dev/null 2>&1; then
            pip install ansible
        else
            print_error "Python is required to install Ansible"
            exit 1
        fi
        
        print_success "Ansible installed"
    else
        print_success "Ansible is available"
    fi
    
    # Check if inventory file exists
    if [[ ! -f "$INVENTORY_FILE" ]]; then
        print_error "Inventory file not found: $INVENTORY_FILE"
        exit 1
    fi
    
    # Check if playbook file exists
    if [[ ! -f "$PLAYBOOK_FILE" ]]; then
        print_error "Playbook file not found: $PLAYBOOK_FILE"
        exit 1
    fi
    
    # Check if we're on a supported platform
    local platform=$(uname -s)
    case $platform in
        "Linux"|"Darwin"|"MINGW"*|"CYGWIN"*|"MSYS"*)
            print_success "Supported platform: $platform"
            ;;
        *)
            print_warning "Platform $platform may not be fully supported"
            ;;
    esac
    
    print_success "Prerequisites checked"
}

# Create log directory
create_log_directory() {
    print_step "Creating log directory..."
    
    local log_dir=$(dirname "$LOG_FILE")
    mkdir -p "$log_dir"
    
    print_success "Log directory created: $log_dir"
}

# Validate inventory
validate_inventory() {
    print_step "Validating Ansible inventory..."
    
    if ansible-inventory -i "$INVENTORY_FILE" --list >/dev/null 2>&1; then
        print_success "Inventory file is valid"
    else
        print_error "Inventory file is invalid"
        exit 1
 fi
}

# Run Ansible playbook
run_ansible_playbook() {
    print_step "Running Ansible playbook..."
    
    local ansible_args=(
        "-i" "$INVENTORY_FILE"
        "$PLAYBOOK_FILE"
        "--verbose"
        "--diff"
        "--check"  # Remove this for actual deployment
    )
    
    print_info "Ansible command: ansible-playbook ${ansible_args[*]}"
    print_info "Log file: $LOG_FILE"
    
    # Run the playbook
    if ansible-playbook "${ansible_args[@]}" 2>&1 | tee "$LOG_FILE"; then
        print_success "Ansible playbook completed successfully"
    else
        print_error "Ansible playbook failed"
        print_info "Check the log file for details: $LOG_FILE"
        exit 1
    fi
}

# Post-deployment verification
post_deployment_verification() {
    print_step "Running post-deployment verification..."
    
    local install_dir="$HOME/tam-rfe-automation"
    
    # Check if installation directory exists
    if [[ -d "$install_dir" ]]; then
        print_success "Installation directory exists: $install_dir"
    else
        print_error "Installation directory not found: $install_dir"
        return 1
    fi
    
    # Check if main executable exists
    if [[ -f "$install_dir/tam-rfe-standalone.py" ]]; then
        print_success "Main executable exists"
    else
        print_error "Main executable not found"
        return 1
    fi
    
    # Check if bin directory exists
    if [[ -d "$install_dir/bin" ]]; then
        print_success "Bin directory exists"
    else
        print_error "Bin directory not found"
        return 1
    fi
    
    # Check if chat interface exists
    if [[ -f "$install_dir/bin/tam-rfe-chat" ]]; then
        print_success "Chat interface exists"
    else
        print_error "Chat interface not found"
        return 1
    fi
    
    # Test Python script execution
    if python3 "$install_dir/tam-rfe-standalone.py" --version >/dev/null 2>&1; then
        print_success "Python script execution test passed"
    else
        print_warning "Python script execution test failed"
    fi
    
    print_success "Post-deployment verification completed"
}

# Display completion message
display_completion_message() {
    echo ""
    echo -e "${GREEN}🎉 TAM RFE Automation Tool Deployment Complete!${NC}"
    echo ""
    echo -e "${CYAN}🚀 Quick Start:${NC}"
    echo "1. Open terminal and run: $HOME/tam-rfe-automation/bin/tam-rfe-chat"
    echo "2. Or use the desktop shortcut (if created)"
    echo "3. Follow the guided onboarding process"
    echo "4. Generate your first report in minutes!"
    echo ""
    echo -e "${CYAN}📚 Documentation:${NC}"
    echo "- User Guide: $HOME/tam-rfe-automation/docs/BRAND-NEW-TAM-GUIDE.md"
    echo "- Getting Started: $HOME/tam-rfe-automation/GETTING-STARTED.md"
    echo "- Prerequisites: $HOME/tam-rfe-automation/docs/PREREQUISITES-GUIDE.md"
    echo ""
    echo -e "${CYAN}🆘 Need Help?${NC}"
    echo "- Run the tool and ask for assistance"
    echo "- Check the documentation in $HOME/tam-rfe-automation/docs/"
    echo "- Contact your TAM manager for support"
    echo ""
    echo -e "${PURPLE}💝 Built with passion for helping new TAMs succeed!${NC}"
    echo ""
}

# Show help
show_help() {
    cat << EOF
TAM RFE Automation Tool - Ansible Deployment Script

Usage: $0 [OPTIONS]

Options:
  -h, --help          Show this help message
  -v, --verbose       Enable verbose output
  -c, --check         Run in check mode (dry run)
  -i, --inventory     Specify custom inventory file
  -p, --playbook      Specify custom playbook file
  --skip-verification Skip post-deployment verification
  --log-file          Specify custom log file

Examples:
  $0                          # Deploy with default settings
  $0 --check                  # Run in check mode (dry run)
  $0 --verbose                # Enable verbose output
  $0 --skip-verification      # Skip post-deployment verification

Environment Variables:
  ANSIBLE_CONFIG              # Ansible configuration file
  ANSIBLE_INVENTORY           # Default inventory file
  ANSIBLE_PLAYBOOK            # Default playbook file

For more information, see the documentation in the docs/ directory.
EOF
}

# Parse command line arguments
parse_arguments() {
    local ansible_args=()
    local skip_verification=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                ansible_args+=("--verbose")
                shift
                ;;
            -c|--check)
                ansible_args+=("--check")
                shift
                ;;
            -i|--inventory)
                INVENTORY_FILE="$2"
                shift 2
                ;;
            -p|--playbook)
                PLAYBOOK_FILE="$2"
                shift 2
                ;;
            --skip-verification)
                skip_verification=true
                shift
                ;;
            --log-file)
                LOG_FILE="$2"
                shift 2
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Store ansible args for later use
    ANSIBLE_ARGS=("${ansible_args[@]}")
    SKIP_VERIFICATION=$skip_verification
}

# Main deployment process
main() {
    print_header
    
    # Parse command line arguments
    parse_arguments "$@"
    
    # Run deployment steps
    check_prerequisites
    create_log_directory
    validate_inventory
    run_ansible_playbook
    
    # Post-deployment verification (unless skipped)
    if [[ "$SKIP_VERIFICATION" != "true" ]]; then
        post_deployment_verification
    else
        print_info "Skipping post-deployment verification"
    fi
    
    # Display completion message
    display_completion_message
}

# Run main function with all arguments
main "$@"
