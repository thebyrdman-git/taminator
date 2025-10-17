#!/usr/bin/env python3
"""
Test that directories can be created and managed on all platforms
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from foundation.platform import platform


def test_directory_creation():
    """Test creating nested directory structures"""
    test_app = "rfe-tool-ci-test"
    
    # Get directories
    config_dir = platform.config_dir(test_app)
    data_dir = platform.data_dir(test_app)
    cache_dir = platform.cache_dir(test_app)
    log_dir = platform.log_dir(test_app)
    
    print(f"Testing on: {platform.system()}")
    print(f"Config: {config_dir}")
    print(f"Data: {data_dir}")
    print(f"Cache: {cache_dir}")
    print(f"Log: {log_dir}")
    
    # Create all directories
    platform.ensure_dirs(test_app)
    
    # Verify they exist
    assert config_dir.exists(), f"Config dir not created: {config_dir}"
    assert data_dir.exists(), f"Data dir not created: {data_dir}"
    assert cache_dir.exists(), f"Cache dir not created: {cache_dir}"
    assert log_dir.exists(), f"Log dir not created: {log_dir}"
    
    # Test file creation
    test_file = config_dir / "test.conf"
    test_file.write_text("test content")
    assert test_file.exists()
    assert test_file.read_text() == "test content"
    
    print("✅ All directory operations successful")
    
    # Cleanup
    import shutil
    for dir_path in [config_dir, data_dir, cache_dir, log_dir]:
        if dir_path.exists():
            shutil.rmtree(dir_path, ignore_errors=True)
    
    print("✅ Cleanup complete")


if __name__ == '__main__':
    try:
        test_directory_creation()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

