#!/bin/bash
# VPN Connection Verification Script
# Tests Red Hat VPN connectivity and internal service access

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0;33m' # No Color

ERRORS=0
WARNINGS=0

echo -e "${BLUE}🔍 Red Hat VPN Verification${NC}"
echo "================================"
echo ""

# Check VPN connection
echo -n "VPN Connection: "
if nmcli connection show --active | grep -iq "vpn\|tun\|redhat"; then
    echo -e "${GREEN}✅ Connected${NC}"
    VPN_NAME=$(nmcli connection show --active | grep -i "vpn\|tun\|redhat" | awk '{print $1}')
    echo "   Connection: $VPN_NAME"
else
    echo -e "${RED}❌ Not connected${NC}"
    echo "   Run: sudo nmcli connection up <vpn-name>"
    ERRORS=$((ERRORS + 1))
fi

# Check DNS resolution
echo ""
echo -n "Internal DNS: "
if nslookup gitlab.cee.redhat.com &>/dev/null; then
    IP=$(nslookup gitlab.cee.redhat.com 2>/dev/null | grep -A1 "Name:" | tail -1 | awk '{print $2}')
    echo -e "${GREEN}✅ Working${NC}"
    echo "   gitlab.cee.redhat.com → $IP"
else
    echo -e "${RED}❌ Failed${NC}"
    echo "   Cannot resolve internal hostnames"
    ERRORS=$((ERRORS + 1))
fi

# Test GitLab CEE access
echo ""
echo -n "GitLab CEE: "
if curl -I https://gitlab.cee.redhat.com 2>/dev/null | head -1 | grep -q "200\|302\|301"; then
    echo -e "${GREEN}✅ Accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Not accessible${NC}"
    echo "   May need Kerberos ticket for authentication"
    WARNINGS=$((WARNINGS + 1))
fi

# Check Kerberos ticket
echo ""
echo -n "Kerberos Ticket: "
if klist &>/dev/null; then
    PRINCIPAL=$(klist 2>/dev/null | grep "Default principal:" | cut -d: -f2 | xargs)
    EXPIRES=$(klist 2>/dev/null | grep "renew until" | awk '{print $3, $4}')
    echo -e "${GREEN}✅ Valid${NC}"
    echo "   Principal: $PRINCIPAL"
    echo "   Expires: $EXPIRES"
else
    echo -e "${YELLOW}ℹ️  No ticket${NC}"
    echo "   Run: kinit jbyrd@REDHAT.COM"
    WARNINGS=$((WARNINGS + 1))
fi

# Test SSH to GitLab
echo ""
echo -n "GitLab SSH: "
if timeout 5 ssh -T git@gitlab.cee.redhat.com 2>&1 | grep -q "Welcome to GitLab"; then
    echo -e "${GREEN}✅ Working${NC}"
elif timeout 5 ssh -T git@gitlab.cee.redhat.com 2>&1 | grep -q "Permission denied"; then
    echo -e "${YELLOW}⚠️  SSH key not configured${NC}"
    echo "   Add SSH key: https://gitlab.cee.redhat.com/-/profile/keys"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${YELLOW}⚠️  Cannot connect${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check CA certificates
echo ""
echo -n "Red Hat CA Certs: "
if ls /etc/pki/ca-trust/source/anchors/*RH*.* &>/dev/null || \
   ls /etc/pki/ca-trust/source/anchors/*redhat*.* &>/dev/null; then
    echo -e "${GREEN}✅ Installed${NC}"
    ls /etc/pki/ca-trust/source/anchors/ | grep -i "rh\|redhat" | sed 's/^/   /'
else
    echo -e "${YELLOW}⚠️  Not found${NC}"
    echo "   May cause SSL errors for internal services"
    WARNINGS=$((WARNINGS + 1))
fi

# Check routing (internal networks)
echo ""
echo -n "Internal Routing: "
if ip route | grep -q "10\."; then
    echo -e "${GREEN}✅ Configured${NC}"
    ip route | grep "10\." | head -3 | sed 's/^/   /'
else
    echo -e "${YELLOW}⚠️  No 10.x routes${NC}"
    echo "   VPN may not be pushing routes"
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "================================"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ VPN fully configured and working${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  VPN working with $WARNINGS warnings${NC}"
    exit 0
else
    echo -e "${RED}❌ VPN has $ERRORS errors and $WARNINGS warnings${NC}"
    exit 1
fi
