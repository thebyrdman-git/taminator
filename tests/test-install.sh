#!/bin/bash
#
# Test installation on Linux/macOS
#

set -e

echo "=================================="
echo "Installation Test (Linux/macOS)"
echo "=================================="
echo ""

OS_TYPE=$(uname -s)
echo "Operating System: $OS_TYPE"
echo ""

# Test 1: Python available
echo "Test 1: Python availability"
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python not found"
    exit 1
fi
echo ""

# Test 2: Foundation module imports
echo "Test 2: Foundation module imports"
if python3 -c "from foundation.platform import platform; print('Platform:', platform.system())" 2>/dev/null; then
    echo "✅ Foundation module imports successfully"
else
    echo "❌ Foundation module import failed"
    exit 1
fi
echo ""

# Test 3: Directory structure
echo "Test 3: Directory structure validation"
REQUIRED_DIRS=(
    "foundation"
    "bin"
    "config"
    "docs"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ Directory exists: $dir"
    else
        echo "⚠️  Directory missing: $dir (may be optional)"
    fi
done
echo ""

# Test 4: Executable scripts
echo "Test 4: Executable script validation"
if [ -d "bin" ]; then
    SCRIPT_COUNT=$(find bin -type f -name "tam-rfe-*" 2>/dev/null | wc -l)
    echo "✅ Found $SCRIPT_COUNT RFE tool scripts in bin/"
fi
echo ""

# Test 5: Platform-specific paths
echo "Test 5: Platform-specific paths"
python3 << 'PYEOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from foundation.platform import platform

print(f"Config dir: {platform.config_dir('rfe-tool')}")
print(f"Data dir: {platform.data_dir('rfe-tool')}")
print(f"Cache dir: {platform.cache_dir('rfe-tool')}")

# Verify OS conventions
import os
detected_os = platform.system()
config = platform.config_dir('rfe-tool')

if detected_os == 'linux':
    assert '.config' in str(config) or 'XDG_CONFIG_HOME' in os.environ
    print("✅ Linux: XDG conventions followed")
elif detected_os == 'macos':
    assert 'Library' in str(config)
    print("✅ macOS: Library conventions followed")
PYEOF
echo ""

echo "=================================="
echo "✅ All installation tests PASSED"
echo "=================================="

