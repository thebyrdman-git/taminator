#!/bin/bash
# Enhanced TAM Portfolio Setup Tool
# Handles real-world complexity: multi-TAM accounts, product specialization,
# coverage models, backup relationships, and account weights

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

CONFIG_DIR="$HOME/.config/rfe-automation"
CONFIG_FILE="$CONFIG_DIR/enhanced-tam-portfolio.yml"

echo -e "${PURPLE}🎯 Enhanced TAM Portfolio Setup Tool${NC}"
echo -e "${PURPLE}====================================${NC}"
echo -e "${CYAN}Handles real-world TAM complexity:${NC}"
echo -e "  • Multi-TAM accounts (up to 5 TAMs per account)"
echo -e "  • Product specialization (Platform, OpenShift, Ansible, etc.)"
echo -e "  • Coverage models (Dedicated vs Shared)"
echo -e "  • Backup TAM relationships"
echo -e "  • Account weights (1-4 priority scale)"
echo -e "  • Multi-account customers"
echo ""

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Check if config already exists
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠️  Enhanced TAM portfolio config already exists at:${NC}"
    echo -e "${BLUE}$CONFIG_FILE${NC}"
    echo ""
    read -p "Do you want to update it? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}✅ Keeping existing configuration.${NC}"
        exit 0
    fi
fi

echo -e "${BLUE}📋 Let's set up your enhanced TAM portfolio configuration...${NC}"
echo ""

# Get TAM information
read -p "Enter your name: " TAM_NAME
read -p "Enter your email: " TAM_EMAIL
read -p "Enter your TAM type (e.g., Ansible Specialist, Platform TAM): " TAM_TYPE
read -p "Enter your region (e.g., NA, EMEA, APAC): " REGION
read -p "Enter your primary vertical (e.g., FSI, Healthcare, Government): " VERTICAL
read -p "Enter your backup TAM: " BACKUP_TAM

echo ""
echo -e "${CYAN}🔍 Analyzing your case data to suggest accounts...${NC}"

# Get case data and suggest accounts with enhanced analysis
TEMP_FILE=$(mktemp)
rhcase list --all --format json 2>/dev/null | jq -r '
  group_by(.accountNumber) | 
  map({
    account_number: .[0].accountNumber,
    customer_name: .[0].account.name,
    account_name: .[0].accountName,
    total_cases: length,
    active_cases: map(select(.isClosed == false)) | length,
    sbr_groups: [.[].sbrGroup] | unique,
    vertical: .[0].account.vertical,
    case_owner: .[0].caseOwner.name
  }) | 
  sort_by(-.active_cases) | 
  .[] | 
  select(.active_cases >= 1) |
  "\(.account_number)|\(.customer_name)|\(.account_name)|\(.active_cases)|\(.total_cases)|\(.sbr_groups | join(","))|\(.vertical // "Unknown")|\(.case_owner)"
' > "$TEMP_FILE" || {
    echo -e "${RED}❌ Failed to analyze case data. Please check rhcase configuration.${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}📊 Found the following accounts with case activity:${NC}"
echo ""

# Display suggested accounts with enhanced information
ACCOUNTS=()
while IFS='|' read -r account_number customer_name account_name active_cases total_cases sbr_groups vertical case_owner; do
    echo -e "${CYAN}Account: $account_number${NC}"
    echo -e "  Customer: $customer_name"
    echo -e "  Account Name: $account_name"
    echo -e "  Active Cases: $active_cases"
    echo -e "  Total Cases: $total_cases"
    echo -e "  SBR Groups: $sbr_groups"
    echo -e "  Vertical: $vertical"
    echo -e "  Case Owner: $case_owner"
    echo ""
    
    read -p "Include this account in your portfolio? (Y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        # Get enhanced account information
        echo "Account Details:"
        read -p "TAM Role (Primary/Secondary): " tam_role
        tam_role=${tam_role:-Primary}
        
        read -p "Products (comma-separated): " products
        products=${products:-$sbr_groups}
        
        echo "Account Weight (1=Low, 2=Medium, 3=High, 4=Critical):"
        read -p "Account Weight (default: 2): " account_weight
        account_weight=${account_weight:-2}
        
        echo "Coverage Model (Dedicated/Shared):"
        read -p "Coverage Model (default: Shared): " coverage_model
        coverage_model=${coverage_model:-Shared}
        
        read -p "Backup TAM: " account_backup_tam
        account_backup_tam=${account_backup_tam:-$BACKUP_TAM}
        
        read -p "Account Exec: " account_exec
        
        read -p "Description: " description
        
        ACCOUNTS+=("$account_number|$customer_name|$account_name|$products|$vertical|$tam_role|$account_weight|$coverage_model|$account_backup_tam|$account_exec|$description")
    fi
done < "$TEMP_FILE"

rm "$TEMP_FILE"

# Generate enhanced config file
echo -e "${BLUE}📝 Generating enhanced TAM portfolio configuration...${NC}"

cat > "$CONFIG_FILE" << EOF
---
# Enhanced TAM Portfolio Configuration
# Handles real-world complexity: multi-TAM accounts, product specialization,
# coverage models, backup relationships, and account weights

# TAM Information
tam_name: "$TAM_NAME"
tam_email: "$TAM_EMAIL"
tam_type: "$TAM_TYPE"
region: "$REGION"
vertical: "$VERTICAL"
backup_tam: "$BACKUP_TAM"

# Portfolio Definition with Real-World Complexity
accounts:
EOF

for account_info in "${ACCOUNTS[@]}"; do
    IFS='|' read -r account_number customer_name account_name products vertical tam_role account_weight coverage_model account_backup_tam account_exec description <<< "$account_info"
    
    cat >> "$CONFIG_FILE" << EOF
  - customer_name: "$customer_name"
    account_numbers: ["$account_number"]
    tam_role: "$tam_role"
    products: [$(echo "$products" | sed 's/,/", "/g' | sed 's/^/"/' | sed 's/$/"/')]
    account_weight: $account_weight
    coverage_model: "$coverage_model"
    backup_tam: "$account_backup_tam"
    account_exec: "$account_exec"
    start_date: "$(date +%Y-%m-%d)"
    end_date: "$(date -d "+1 year" +%Y-%m-%d)"
    renewal_status: "Active"
    notes: "$description"
EOF
done

cat >> "$CONFIG_FILE" << EOF

# Multi-TAM Coordination (to be configured manually)
coordination:
  shared_accounts: []
  # Example:
  # - customer_name: "Bank of America"
  #   other_tams:
  #     - name: "Stephen Hobbs"
  #       products: ["Platform"]
  #       role: "Primary"
  #   coordination_notes: "Weekly sync calls"

# Backup Coverage
backup_coverage:
  primary_backup: "$BACKUP_TAM"
  coverage_schedule: []

# Account Prioritization
prioritization:
  high_priority: []
  medium_priority: []
  low_priority: []

# Reporting Preferences
reporting:
  frequency: "weekly"
  report_types: ["rfe_bug_tracker", "active_cases"]
  include_backup_coverage: true
  include_coordination_notes: true
  notification_preferences:
    email: true
    slack: false
    teams: false

# Validation Settings
validation_mode: "active_cases"
auto_suggestions: true
min_cases_for_suggestion: 3
include_closed: false
min_cases: 1
EOF

echo ""
echo -e "${GREEN}✅ Enhanced TAM portfolio configuration created!${NC}"
echo -e "${BLUE}📁 Location: $CONFIG_FILE${NC}"
echo ""
echo -e "${CYAN}📋 Your enhanced portfolio includes ${#ACCOUNTS[@]} accounts:${NC}"
for account_info in "${ACCOUNTS[@]}"; do
    IFS='|' read -r account_number customer_name account_name products tam_role account_weight coverage_model account_backup_tam account_exec description <<< "$account_info"
    echo -e "  • $customer_name ($account_number) - $products - $coverage_model (Weight: $account_weight)"
done

echo ""
echo -e "${PURPLE}🚀 Next Steps:${NC}"
echo -e "1. Review your configuration: ${BLUE}cat $CONFIG_FILE${NC}"
echo -e "2. Add multi-TAM coordination details manually"
echo -e "3. Configure backup coverage schedules"
echo -e "4. Test your portfolio: ${BLUE}make discover-enhanced-portfolio${NC}"
echo -e "5. Generate reports: ${BLUE}make generate-enhanced-tam-reports${NC}"
echo -e "6. Edit your portfolio anytime: ${BLUE}$CONFIG_FILE${NC}"

echo ""
echo -e "${GREEN}🎯 Enhanced TAM Portfolio Setup Complete!${NC}"
echo -e "${CYAN}This configuration handles real-world TAM complexity including:${NC}"
echo -e "  ✅ Multi-TAM account coordination"
echo -e "  ✅ Product specialization"
echo -e "  ✅ Coverage models (Dedicated/Shared)"
echo -e "  ✅ Backup TAM relationships"
echo -e "  ✅ Account weight prioritization"
echo -e "  ✅ Multi-account customers"
