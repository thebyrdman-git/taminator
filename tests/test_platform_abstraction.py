#!/usr/bin/env python3
"""
Test platform abstraction layer works on all platforms
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from foundation.platform import Platform, platform


def test_os_detection():
    """Test OS detection works correctly"""
    detected_os = platform.system()
    
    assert detected_os in ['linux', 'macos', 'windows'], \
        f"Unexpected OS: {detected_os}"
    
    print(f"[OK] OS Detection: {detected_os}")
    
    # Test helper methods
    if detected_os == 'linux':
        assert platform.is_linux()
        assert not platform.is_macos()
        assert not platform.is_windows()
    elif detected_os == 'macos':
        assert not platform.is_linux()
        assert platform.is_macos()
        assert not platform.is_windows()
    elif detected_os == 'windows':
        assert not platform.is_linux()
        assert not platform.is_macos()
        assert platform.is_windows()
    
    print(f"[OK] OS Helper Methods: Correct")


def test_directory_methods():
    """Test directory methods return valid paths"""
    
    # Home directory
    home = platform.home_dir()
    assert home.exists(), "Home directory must exist"
    print(f"[OK] Home Dir: {home}")
    
    # Config directory
    config = platform.config_dir("rfe-tool-test")
    assert isinstance(config, Path), "Config dir must be Path object"
    print(f"[OK] Config Dir: {config}")
    
    # Data directory
    data = platform.data_dir("rfe-tool-test")
    assert isinstance(data, Path), "Data dir must be Path object"
    print(f"[OK] Data Dir: {data}")
    
    # Cache directory
    cache = platform.cache_dir("rfe-tool-test")
    assert isinstance(cache, Path), "Cache dir must be Path object"
    print(f"[OK] Cache Dir: {cache}")
    
    # Log directory
    log = platform.log_dir("rfe-tool-test")
    assert isinstance(log, Path), "Log dir must be Path object"
    print(f"[OK] Log Dir: {log}")
    
    # Temp directory
    temp = platform.temp_dir()
    assert temp.exists(), "Temp directory must exist"
    print(f"[OK] Temp Dir: {temp}")


def test_directory_conventions():
    """Test OS-specific directory conventions are followed"""
    detected_os = platform.system()
    config = platform.config_dir("rfe-tool-test")
    
    if detected_os == 'linux':
        # Linux: Should use XDG Base Directory spec
        assert '.config' in str(config) or 'XDG_CONFIG_HOME' in os.environ
        print("[OK] Linux: XDG Base Directory conventions")
    
    elif detected_os == 'macos':
        # macOS: Should use ~/Library/Application Support
        assert 'Library' in str(config)
        print("[OK] macOS: Library conventions")
    
    elif detected_os == 'windows':
        # Windows: Should use AppData
        assert 'AppData' in str(config) or 'APPDATA' in os.environ
        print("[OK] Windows: AppData conventions")


def test_ensure_dirs():
    """Test directory creation works"""
    try:
        platform.ensure_dirs("rfe-tool-test")
        
        # Verify directories were created
        config = platform.config_dir("rfe-tool-test")
        data = platform.data_dir("rfe-tool-test")
        cache = platform.cache_dir("rfe-tool-test")
        log = platform.log_dir("rfe-tool-test")
        
        assert config.exists(), f"Config dir not created: {config}"
        assert data.exists(), f"Data dir not created: {data}"
        assert cache.exists(), f"Cache dir not created: {cache}"
        assert log.exists(), f"Log dir not created: {log}"
        
        print("[OK] Directory Creation: All directories created")
        
        # Cleanup
        import shutil
        for dir_path in [config, data, cache, log]:
            if dir_path.exists():
                shutil.rmtree(dir_path, ignore_errors=True)
        
        print("[OK] Cleanup: Test directories removed")
        
    except Exception as e:
        print(f"[FAIL] Directory creation failed: {e}")
        raise


def test_shell_detection():
    """Test shell detection returns valid values"""
    shells = platform.shell_available()
    assert isinstance(shells, list), "shell_available() must return list"
    assert len(shells) > 0, "Must have at least one shell available"
    print(f"[OK] Available Shells: {', '.join(shells)}")
    
    default = platform.default_shell()
    assert default in shells, f"Default shell {default} not in available shells"
    print(f"[OK] Default Shell: {default}")


def test_path_helpers():
    """Test path-related helper methods"""
    
    # Executable extension
    ext = platform.executable_extension()
    detected_os = platform.system()
    if detected_os == 'windows':
        assert ext == '.exe', "Windows should return .exe"
    else:
        assert ext == '', "Unix-like should return empty string"
    print(f"[OK] Executable Extension: '{ext}'")
    
    # Path separator
    sep = platform.path_separator()
    if detected_os == 'windows':
        assert sep == ';', "Windows should use semicolon"
    else:
        assert sep == ':', "Unix-like should use colon"
    print(f"[OK] Path Separator: '{sep}'")
    
    # Line ending
    ending = platform.line_ending()
    if detected_os == 'windows':
        assert ending == '\r\n', "Windows should use CRLF"
    else:
        assert ending == '\n', "Unix-like should use LF"
    print(f"[OK] Line Ending: {repr(ending)}")


def test_python_executable():
    """Test Python executable detection"""
    python_exe = platform.python_executable()
    assert python_exe.exists(), f"Python executable not found: {python_exe}"
    print(f"[OK] Python Executable: {python_exe}")


def main():
    """Run all tests"""
    # Use ASCII characters for Windows compatibility
    separator = "=" * 60
    line = "-" * 60
    
    print(separator)
    print("Platform Abstraction Layer Tests")
    print(separator)
    print()
    
    tests = [
        ("OS Detection", test_os_detection),
        ("Directory Methods", test_directory_methods),
        ("Directory Conventions", test_directory_conventions),
        ("Directory Creation", test_ensure_dirs),
        ("Shell Detection", test_shell_detection),
        ("Path Helpers", test_path_helpers),
        ("Python Executable", test_python_executable),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{line}")
        print(f"Test: {test_name}")
        print(line)
        try:
            test_func()
            passed += 1
            print(f"[OK] {test_name}: PASSED")
        except Exception as e:
            failed += 1
            print(f"[FAIL] {test_name}: FAILED - {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print(separator)
    print(f"Results: {passed} passed, {failed} failed")
    print(separator)
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n[OK] All platform abstraction tests PASSED!")
        sys.exit(0)


if __name__ == '__main__':
    main()

