#!/bin/bash
# Reliable Distribution Detection Script
# Cannot trust /etc/os-release alone!

echo "=== COMPREHENSIVE DISTRIBUTION DETECTION ==="
echo

echo "1. /etc/os-release (MAY BE DECEPTIVE):"
if [ -f /etc/os-release ]; then
    echo "   NAME: $(grep '^NAME=' /etc/os-release | cut -d'=' -f2 | tr -d '"')"
    echo "   ID: $(grep '^ID=' /etc/os-release | cut -d'=' -f2 | tr -d '"')"
    echo "   Comments/Hidden Info:"
    grep '^#.*SUSE\|^#.*Liberty\|^#.*compatibility' /etc/os-release || echo "   (No hidden distribution info found)"
else
    echo "   /etc/os-release NOT FOUND"
fi
echo

echo "2. Legacy Release Files (MORE RELIABLE):"
for file in /etc/redhat-release /etc/centos-release /etc/suse-release /etc/debian_version /etc/oracle-release; do
    if [ -f "$file" ]; then
        echo "   $file: $(cat $file)"
    fi
done
echo

echo "3. Package Manager Detection (MOST RELIABLE):"
echo -n "   Package Managers: "
which yum >/dev/null 2>&1 && echo -n "yum "
which dnf >/dev/null 2>&1 && echo -n "dnf "
which zypper >/dev/null 2>&1 && echo -n "zypper "
which apt >/dev/null 2>&1 && echo -n "apt "
which pacman >/dev/null 2>&1 && echo -n "pacman "
echo
echo

echo "4. Kernel and System Info:"
echo "   Kernel: $(uname -r)"
echo "   Architecture: $(uname -m)"
echo "   Hostname: $(hostname)"
echo

echo "5. Process Manager:"
if pidof systemd >/dev/null 2>&1; then
    echo "   systemd detected"
    if which hostnamectl >/dev/null 2>&1; then
        echo "   hostnamectl info: $(hostnamectl | grep 'Operating System' | cut -d':' -f2 | xargs)"
    fi
elif pidof init >/dev/null 2>&1; then
    echo "   SysV init detected"
fi
echo

echo "6. File System Paths (Distribution Specific):"
[ -d /etc/yum.repos.d ] && echo "   RHEL-style: /etc/yum.repos.d/ exists"
[ -d /etc/zypp ] && echo "   SUSE-style: /etc/zypp/ exists"
[ -d /etc/apt ] && echo "   Debian-style: /etc/apt/ exists"
echo

echo "7. Library Versions (Can Reveal True Base):"
if which rpm >/dev/null 2>&1; then
    echo "   RPM database present"
    rpm -qa | grep -E "(suse|sle|liberty)" | head -3
fi
echo

echo "=== RECOMMENDATION ==="
echo "Cross-reference ALL methods above to determine true distribution!"
echo "Never trust /etc/os-release alone in enterprise environments."

