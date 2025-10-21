#!/bin/bash

# TAM RFE Automation Tool - Interactive Variable Setup
# Guides users through setting up all required Ansible variables

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANSIBLE_DIR="$SCRIPT_DIR/ansible"
VARS_FILE="$ANSIBLE_DIR/group_vars/all.yml"
BACKUP_FILE="$ANSIBLE_DIR/group_vars/all.yml.backup"

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
    echo "🎯 TAM RFE Automation Tool - Variable Setup"
    echo "=========================================="
    echo -e "${NC}"
    echo "📅 Setup started: $(date)"
    echo "🎯 Purpose: Configure all variables for Ansible deployment"
    echo "💝 Built with passion for helping new TAMs succeed!"
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

# Input validation functions
validate_email() {
    local email="$1"
    if [[ "$email" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
        return 0
    else
        return 1
    fi
}

validate_account_number() {
    local account="$1"
    if [[ "$account" =~ ^[0-9]+$ ]]; then
        return 0
    else
        return 1
    fi
}

validate_group_id() {
    local group_id="$1"
    if [[ "$group_id" =~ ^[0-9]+$ ]]; then
        return 0
    else
        return 1
    fi
}

# Interactive input functions
get_user_input() {
    local prompt="$1"
    local default="$2"
    local validation_func="$3"
    local error_msg="$4"
    
    while true; do
        if [[ -n "$default" ]]; then
            echo -e "${BLUE}$prompt${NC} (default: $default): "
        else
            echo -e "${BLUE}$prompt${NC}: "
        fi
        
        read -r input
        
        # Use default if input is empty
        if [[ -z "$input" && -n "$default" ]]; then
            input="$default"
        fi
        
        # Validate input if validation function is provided
        if [[ -n "$validation_func" ]]; then
            if $validation_func "$input"; then
                echo "$input"
                return 0
            else
                print_error "$error_msg"
                continue
            fi
        else
            echo "$input"
            return 0
        fi
    done
}

get_yes_no() {
    local prompt="$1"
    local default="$2"
    
    while true; do
        if [[ -n "$default" ]]; then
            echo -e "${BLUE}$prompt${NC} (y/n, default: $default): "
        else
            echo -e "${BLUE}$prompt${NC} (y/n): "
        fi
        
        read -r input
        
        # Use default if input is empty
        if [[ -z "$input" && -n "$default" ]]; then
            input="$default"
        fi
        
        case "$input" in
            [Yy]|[Yy][Ee][Ss])
                echo "true"
                return 0
                ;;
            [Nn]|[Nn][Oo])
                echo "false"
                return 0
                ;;
            *)
                print_error "Please enter 'y' for yes or 'n' for no"
                ;;
        esac
    done
}

get_multiple_choice() {
    local prompt="$1"
    local options=("${@:2}")
    
    echo -e "${BLUE}$prompt${NC}"
    for i in "${!options[@]}"; do
        echo "  $((i+1)). ${options[i]}"
    done
    
    while true; do
        echo -e "${BLUE}Enter your choice (1-${#options[@]}):${NC} "
        read -r choice
        
        if [[ "$choice" =~ ^[0-9]+$ ]] && [[ "$choice" -ge 1 ]] && [[ "$choice" -le ${#options[@]} ]]; then
            echo "${options[$((choice-1))]}"
            return 0
        else
            print_error "Please enter a number between 1 and ${#options[@]}"
        fi
    done
}

# Setup functions
setup_user_info() {
    print_step "Setting up your user information..."
    
    local user_name=$(get_user_input "What's your full name?" "" "" "")
    local user_email=$(get_user_input "What's your Red Hat email address?" "" "validate_email" "Please enter a valid email address")
    local user_role=$(get_user_input "What's your role?" "TAM" "" "")
    local user_team=$(get_user_input "What team are you on?" "" "" "")
    
    cat >> "$VARS_FILE" << EOF
# User Information
user_info:
  name: "$user_name"
  email: "$user_email"
  role: "$user_role"
  team: "$user_team"

EOF
    
    print_success "User information configured"
}

setup_customers() {
    print_step "Setting up your customer information..."
    
    local customers=()
    local add_more="true"
    
    while [[ "$add_more" == "true" ]]; do
        echo ""
        print_info "Setting up customer #$(( ${#customers[@]} + 1 ))"
        
        local customer_name=$(get_user_input "What's the customer's company name?" "" "" "")
        local account_number=$(get_user_input "What's their Red Hat account number?" "" "validate_account_number" "Please enter a numeric account number")
        local group_id=$(get_user_input "What's their customer portal group ID?" "" "validate_group_id" "Please enter a numeric group ID")
        
        echo ""
        print_info "Which SBR groups does this customer use?"
        local sbr_groups=()
        local sbr_options=("Ansible" "Ansible Automation Platform" "OpenShift" "OpenShift Container Platform" "RHEL" "Red Hat Enterprise Linux" "Satellite" "Red Hat Satellite" "Custom")
        
        local add_sbr="true"
        while [[ "$add_sbr" == "true" ]]; do
            local sbr_choice=$(get_multiple_choice "Select an SBR group:" "${sbr_options[@]}")
            
            if [[ "$sbr_choice" == "Custom" ]]; then
                local custom_sbr=$(get_user_input "Enter custom SBR group:" "" "" "")
                sbr_groups+=("$custom_sbr")
            else
                sbr_groups+=("$sbr_choice")
            fi
            
            add_sbr=$(get_yes_no "Add another SBR group?" "n")
        done
        
        local primary_contact=$(get_user_input "What's the primary contact email?" "" "validate_email" "Please enter a valid email address")
        
        # Store customer info
        customers+=("$customer_name|$account_number|$group_id|${sbr_groups[*]}|$primary_contact")
        
        add_more=$(get_yes_no "Add another customer?" "n")
    done
    
    # Write customers to file
    cat >> "$VARS_FILE" << EOF
# Customer Information
customers:
EOF
    
    for customer in "${customers[@]}"; do
        IFS='|' read -r name account group_id sbr_groups contact <<< "$customer"
        
        cat >> "$VARS_FILE" << EOF
  - name: "$name"
    account_number: "$account"
    group_id: "$group_id"
    sbr_groups:
EOF
        
        for sbr in $sbr_groups; do
            echo "      - \"$sbr\"" >> "$VARS_FILE"
        done
        
        cat >> "$VARS_FILE" << EOF
    primary_contact: "$contact"
EOF
    done
    
    echo "" >> "$VARS_FILE"
    
    print_success "Customer information configured"
}

setup_system_config() {
    print_step "Setting up system configuration..."
    
    local install_dir=$(get_user_input "Where should we install the tool?" "$HOME/tam-rfe-automation" "" "")
    local python_version=$(get_user_input "What Python version should we use?" "3.7" "" "")
    local create_shortcut=$(get_yes_no "Do you want a desktop shortcut?" "y")
    local create_symlinks=$(get_yes_no "Do you want command shortcuts?" "y")
    
    cat >> "$VARS_FILE" << EOF
# System Configuration
system_config:
  install_directory: "$install_dir"
  python_version: "$python_version"
  create_desktop_shortcut: $create_shortcut
  create_symlinks: $create_symlinks

EOF
    
    print_success "System configuration completed"
}

setup_redhat_config() {
    print_step "Setting up Red Hat configuration..."
    
    local vpn_required=$(get_yes_no "Do you have Red Hat VPN access?" "y")
    local rhcase_required=$(get_yes_no "Do you have the rhcase tool?" "y")
    local portal_access=$(get_yes_no "Do you have customer portal access?" "y")
    local api_credentials=$(get_yes_no "Do you need API credentials?" "y")
    
    cat >> "$VARS_FILE" << EOF
# Red Hat Configuration
redhat_config:
  vpn_required: $vpn_required
  rhcase_required: $rhcase_required
  portal_access: $portal_access
  api_credentials_required: $api_credentials

EOF
    
    print_success "Red Hat configuration completed"
}

setup_notifications() {
    print_step "Setting up notification preferences..."
    
    local email_notifications=$(get_yes_no "Do you want email notifications?" "y")
    local slack_notifications=$(get_yes_no "Do you want Slack notifications?" "n")
    local portal_notifications=$(get_yes_no "Do you want portal notifications?" "y")
    
    local notification_email=""
    if [[ "$email_notifications" == "true" ]]; then
        notification_email=$(get_user_input "What's your email address for notifications?" "" "validate_email" "Please enter a valid email address")
    fi
    
    cat >> "$VARS_FILE" << EOF
# Notification Settings
notifications:
  email: $email_notifications
  slack: $slack_notifications
  portal: $portal_notifications
  email_address: "$notification_email"

EOF
    
    print_success "Notification settings completed"
}

# Validation functions
validate_configuration() {
    print_step "Validating your configuration..."
    
    local errors=0
    
    # Check if required fields are present
    if ! grep -q "user_info:" "$VARS_FILE"; then
        print_error "User information is missing"
        ((errors++))
    fi
    
    if ! grep -q "customers:" "$VARS_FILE"; then
        print_error "Customer information is missing"
        ((errors++))
    fi
    
    if ! grep -q "system_config:" "$VARS_FILE"; then
        print_error "System configuration is missing"
        ((errors++))
    fi
    
    if ! grep -q "redhat_config:" "$VARS_FILE"; then
        print_error "Red Hat configuration is missing"
        ((errors++))
    fi
    
    if ! grep -q "notifications:" "$VARS_FILE"; then
        print_error "Notification settings are missing"
        ((errors++))
    fi
    
    if [[ $errors -eq 0 ]]; then
        print_success "Configuration validation passed"
        return 0
    else
        print_error "Configuration validation failed with $errors errors"
        return 1
    fi
}

# Display configuration summary
display_summary() {
    print_step "Configuration Summary"
    
    echo ""
    echo -e "${CYAN}📋 Your Configuration:${NC}"
    echo "========================"
    
    # Display user info
    if grep -q "user_info:" "$VARS_FILE"; then
        echo -e "${GREEN}✅ User Information:${NC}"
        grep -A 4 "user_info:" "$VARS_FILE" | sed 's/^/   /'
        echo ""
    fi
    
    # Display customers
    if grep -q "customers:" "$VARS_FILE"; then
        echo -e "${GREEN}✅ Customers:${NC}"
        local customer_count=$(grep -c "  - name:" "$VARS_FILE" || echo "0")
        echo "   $customer_count customer(s) configured"
        echo ""
    fi
    
    # Display system config
    if grep -q "system_config:" "$VARS_FILE"; then
        echo -e "${GREEN}✅ System Configuration:${NC}"
        grep -A 4 "system_config:" "$VARS_FILE" | sed 's/^/   /'
        echo ""
    fi
    
    # Display Red Hat config
    if grep -q "redhat_config:" "$VARS_FILE"; then
        echo -e "${GREEN}✅ Red Hat Configuration:${NC}"
        grep -A 4 "redhat_config:" "$VARS_FILE" | sed 's/^/   /'
        echo ""
    fi
    
    # Display notifications
    if grep -q "notifications:" "$VARS_FILE"; then
        echo -e "${GREEN}✅ Notification Settings:${NC}"
        grep -A 4 "notifications:" "$VARS_FILE" | sed 's/^/   /'
        echo ""
    fi
}

# Main setup process
main() {
    print_header
    
    # Create backup of existing file
    if [[ -f "$VARS_FILE" ]]; then
        print_info "Creating backup of existing configuration..."
        cp "$VARS_FILE" "$BACKUP_FILE"
        print_success "Backup created: $BACKUP_FILE"
    fi
    
    # Create variables file
    print_step "Creating variables file..."
    mkdir -p "$(dirname "$VARS_FILE")"
    cat > "$VARS_FILE" << EOF
# TAM RFE Automation Tool - Ansible Variables
# Generated on $(date)
# This file contains all the variables needed for Ansible deployment

EOF
    
    # Run setup steps
    setup_user_info
    setup_customers
    setup_system_config
    setup_redhat_config
    setup_notifications
    
    # Validate configuration
    if validate_configuration; then
        print_success "Configuration setup completed successfully!"
        echo ""
        display_summary
        echo ""
        print_info "Next steps:"
        echo "1. Review your configuration above"
        echo "2. Run the Ansible deployment: ./deploy-with-ansible.sh"
        echo "3. Start using the tool!"
        echo ""
        print_info "Configuration file: $VARS_FILE"
        print_info "Backup file: $BACKUP_FILE"
    else
        print_error "Configuration setup failed. Please check the errors above and try again."
        exit 1
    fi
}

# Run main function
main "$@"
