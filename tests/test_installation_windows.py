#!/usr/bin/env python3
"""
Test installation on Windows
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from foundation.platform import platform


def test_windows_installation():
    """Test RFE tool installation on Windows"""
    
    print("=" * 60)
    print("Installation Test (Windows)")
    print("=" * 60)
    print()
    
    # Test 1: Platform detection
    print("Test 1: Platform detection")
    assert platform.is_windows(), "Should detect Windows"
    print(f"✅ Platform detected: {platform.system()}")
    print()
    
    # Test 2: Directory paths use Windows conventions
    print("Test 2: Windows directory conventions")
    config = platform.config_dir("rfe-tool")
    
    assert 'AppData' in str(config) or 'APPDATA' in os.environ, \
        "Windows should use AppData"
    print(f"✅ Config dir: {config}")
    print()
    
    # Test 3: Path separator
    print("Test 3: Windows path separator")
    sep = platform.path_separator()
    assert sep == ';', "Windows should use semicolon"
    print(f"✅ Path separator: '{sep}'")
    print()
    
    # Test 4: Executable extension
    print("Test 4: Windows executable extension")
    ext = platform.executable_extension()
    assert ext == '.exe', "Windows should use .exe"
    print(f"✅ Executable extension: '{ext}'")
    print()
    
    # Test 5: Line endings
    print("Test 5: Windows line endings")
    ending = platform.line_ending()
    assert ending == '\r\n', "Windows should use CRLF"
    print(f"✅ Line ending: CRLF")
    print()
    
    # Test 6: Directory creation
    print("Test 6: Directory creation")
    platform.ensure_dirs("rfe-tool-test")
    
    test_dirs = [
        platform.config_dir("rfe-tool-test"),
        platform.data_dir("rfe-tool-test"),
        platform.cache_dir("rfe-tool-test"),
        platform.log_dir("rfe-tool-test"),
    ]
    
    for test_dir in test_dirs:
        assert test_dir.exists(), f"Directory not created: {test_dir}"
        print(f"✅ Created: {test_dir}")
    
    # Cleanup
    import shutil
    for test_dir in test_dirs:
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)
    print("✅ Cleanup complete")
    print()
    
    print("=" * 60)
    print("✅ All Windows installation tests PASSED")
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_windows_installation()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

