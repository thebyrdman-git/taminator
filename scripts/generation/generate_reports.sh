#!/bin/bash
# RFE Automation Tool - Simple Wrapper Script
# Usage: ./generate_reports.sh [customer] [report_type]

set -e

# Default values
CUSTOMER="${1:-jpmc}"
REPORT_TYPE="${2:-all}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 RFE Automation Tool${NC}"
echo -e "${BLUE}=====================${NC}"
echo -e "Customer: ${GREEN}${CUSTOMER}${NC}"
echo -e "Report Type: ${GREEN}${REPORT_TYPE}${NC}"
echo ""

# Validate customer exists in vars file
if ! grep -q "^  ${CUSTOMER}:" vars/accounts.yml; then
    echo -e "${RED}❌ Error: Customer '${CUSTOMER}' not found in vars/accounts.yml${NC}"
    echo -e "${YELLOW}Available customers:${NC}"
    grep -E "^  [a-zA-Z_]+:" vars/accounts.yml | sed 's/^  /  - /' | sed 's/:$//'
    exit 1
fi

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

echo -e "${BLUE}📋 Generating reports...${NC}"

# Run the playbook
ansible-playbook generate_reports_with_vars.yml \
    -e "customer=${CUSTOMER}" \
    -e "report_types=${REPORT_TYPES}" \
    -v

echo ""
echo -e "${GREEN}✅ Reports generated successfully!${NC}"
echo -e "${BLUE}📁 Check the output directory for your reports.${NC}"
