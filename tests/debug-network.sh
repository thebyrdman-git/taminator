#!/bin/bash
# Debug libvirt networking issues

echo "🔍 Libvirt Network Debugging"
echo "=============================="
echo ""

# 1. Check libvirt networks
echo "1️⃣  Libvirt Networks:"
sudo virsh net-list --all
echo ""

# 2. Check default network details
echo "2️⃣  Default Network Info:"
sudo virsh net-info default 2>&1 || echo "❌ Default network not found"
echo ""

# 3. Check bridge interface
echo "3️⃣  Bridge Interface (virbr0):"
ip addr show virbr0 2>&1 || echo "❌ virbr0 not found"
echo ""

# 4. Check dnsmasq processes
echo "4️⃣  DHCP Server (dnsmasq):"
ps aux | grep dnsmasq | grep -v grep | grep -E "default|virbr0"
if [ $? -ne 0 ]; then
    echo "❌ No dnsmasq running for default network"
fi
echo ""

# 5. Check routing
echo "5️⃣  Routing Table:"
ip route | grep -E "192.168.122|virbr"
echo ""

# 6. Check NAT rules
echo "6️⃣  NAT/Firewall Rules:"
sudo iptables -t nat -L -n -v | grep -A 5 "Chain LIBVIRT"
echo ""

# 7. Check if VPN is interfering
echo "7️⃣  Active VPN Connections:"
ip link show | grep -E "tun|tap|wg|ppp" || echo "✅ No VPN interfaces detected"
echo ""

# 8. Check for conflicting subnets
echo "8️⃣  All IP Subnets:"
ip -4 addr show | grep inet | grep -v "127.0.0.1"
echo ""

# 9. Test DNS resolution through dnsmasq
echo "9️⃣  DNS Test (from host):"
dig @192.168.122.1 google.com +short 2>&1 || echo "❌ DNS not responding"
echo ""

# 10. Check libvirtd service
echo "🔟 Libvirtd Service:"
systemctl status libvirtd --no-pager | head -5
echo ""

# Summary
echo "📋 Quick Fixes:"
echo "==============="
echo ""
echo "If dnsmasq is not running:"
echo "  sudo virsh net-destroy default && sudo virsh net-start default"
echo ""
echo "If bridge is down:"
echo "  sudo ip link set virbr0 up"
echo ""
echo "If network doesn't exist:"
echo "  cd ~/pai/rfe-automation-clean/tests"
echo "  sudo virsh net-define /dev/stdin < network-default.xml"
echo "  sudo virsh net-start default"
echo "  sudo virsh net-autostart default"
echo ""
echo "If VPN is interfering:"
echo "  Disconnect from VPN and run: sudo virsh net-destroy default && sudo virsh net-start default"
echo ""

