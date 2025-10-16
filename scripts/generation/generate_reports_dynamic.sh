#!/bin/bash
# Dynamic RFE Automation Tool - Auto-Discovery of Customers
# Usage: ./generate_reports_dynamic.sh [report_type] [sbr_groups] [min_cases]

set -e

# Default values
REPORT_TYPE="${1:-all}"
SBR_GROUPS="${2:-Ansible}"
MIN_CASES="${3:-1}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🔍 Dynamic RFE Automation Tool${NC}"
echo -e "${PURPLE}==============================${NC}"
echo -e "Report Type: ${GREEN}${REPORT_TYPE}${NC}"
echo -e "SBR Groups: ${GREEN}${SBR_GROUPS}${NC}"
echo -e "Min Cases: ${GREEN}${MIN_CASES}${NC}"
echo -e "Mode: ${BLUE}Dynamic Customer Discovery${NC}"
echo ""

# Set report types based on input
case "${REPORT_TYPE}" in
    "rfe"|"rfe_bug")
        REPORT_TYPES='["rfe_bug_tracker"]'
        ;;
    "active"|"active_cases")
        REPORT_TYPES='["active_cases"]'
        ;;
    "all")
        REPORT_TYPES='["rfe_bug_tracker", "active_cases"]'
        ;;
    *)
        echo -e "${RED}❌ Error: Invalid report type '${REPORT_TYPE}'${NC}"
        echo -e "${YELLOW}Valid options: rfe, active, all${NC}"
        exit 1
        ;;
esac

# Convert SBR groups to array format
SBR_ARRAY="["
IFS=',' read -ra GROUPS <<< "$SBR_GROUPS"
for i in "${!GROUPS[@]}"; do
    if [ $i -gt 0 ]; then
        SBR_ARRAY+=", "
    fi
    SBR_ARRAY+="\"${GROUPS[i]}\""
done
SBR_ARRAY+="]"

echo -e "${BLUE}🔍 Discovering customers dynamically...${NC}"

# First, let's see what customers we can discover
echo -e "${CYAN}📊 Running customer discovery...${NC}"
ansible-inventory -i inventory/rfe_customers.yml --list | jq -r '.all_customers.hosts[]?' 2>/dev/null | head -10 || echo "No customers discovered or jq not available"

echo ""
echo -e "${BLUE}📋 Generating reports for all discovered customers...${NC}"

# Run the dynamic playbook
ansible-playbook generate_reports_dynamic.yml \
    -i inventory/rfe_customers.yml \
    -e "report_types=${REPORT_TYPES}" \
    -e "sbr_groups=${SBR_ARRAY}" \
    -e "min_cases=${MIN_CASES}" \
    -v

echo ""
echo -e "${GREEN}✅ Dynamic reports generated successfully!${NC}"
echo -e "${BLUE}📁 Check the output directory for customer-specific reports.${NC}"
echo -e "${PURPLE}🚀 Powered by dynamic customer discovery and smart custom modules.${NC}"

# Show summary
if [ -f "output/discovery_summary.md" ]; then
    echo ""
    echo -e "${CYAN}📊 Discovery Summary:${NC}"
    echo -e "${CYAN}====================${NC}"
    head -20 output/discovery_summary.md
    echo -e "${CYAN}... (see output/discovery_summary.md for full details)${NC}"
fi
