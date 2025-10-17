"""
Cross-Platform Abstraction Layer
Business logic NEVER imports os, sys, platform directly
Always use this module instead

Part of PAI Framework - OS-Agnostic Design Philosophy
"""

import platform as _platform
import sys
from pathlib import Path
from typing import Optional
import os

# Optional dependencies (graceful degradation)
try:
    import platformdirs
    HAS_PLATFORMDIRS = True
except ImportError:
    HAS_PLATFORMDIRS = False

try:
    import keyring
    HAS_KEYRING = True
except ImportError:
    HAS_KEYRING = False


class Platform:
    """
    Single interface for all platform-specific operations
    Write once, run everywhere (Linux, macOS, Windows)
    """
    
    # ==================== OS Detection ====================
    
    @staticmethod
    def system() -> str:
        """
        Get OS name in normalized form
        Returns: 'linux', 'macos', or 'windows'
        """
        system = _platform.system().lower()
        if system == 'darwin':
            return 'macos'
        return system
    
    @staticmethod
    def is_linux() -> bool:
        return Platform.system() == 'linux'
    
    @staticmethod
    def is_macos() -> bool:
        return Platform.system() == 'macos'
    
    @staticmethod
    def is_windows() -> bool:
        return Platform.system() == 'windows'
    
    @staticmethod
    def version() -> str:
        """Get OS version string"""
        return _platform.release()
    
    @staticmethod
    def architecture() -> str:
        """Get system architecture (x86_64, arm64, etc.)"""
        return _platform.machine()
    
    # ==================== Directory Management ====================
    
    @staticmethod
    def home_dir() -> Path:
        """User's home directory (cross-platform)"""
        return Path.home()
    
    @staticmethod
    def config_dir(app_name: str = "rfe-tool") -> Path:
        """
        Application config directory (OS-appropriate)
        - Linux: ~/.config/rfe-tool/
        - macOS: ~/Library/Application Support/rfe-tool/
        - Windows: %APPDATA%/rfe-tool/
        """
        if HAS_PLATFORMDIRS:
            return Path(platformdirs.user_config_dir(app_name, "redhat"))
        else:
            # Fallback for systems without platformdirs
            if Platform.is_windows():
                base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
            elif Platform.is_macos():
                base = Path.home() / 'Library' / 'Application Support'
            else:  # Linux
                base = Path.home() / '.config'
            return base / app_name
    
    @staticmethod
    def data_dir(app_name: str = "rfe-tool") -> Path:
        """
        Application data directory (OS-appropriate)
        - Linux: ~/.local/share/rfe-tool/
        - macOS: ~/Library/Application Support/rfe-tool/
        - Windows: %LOCALAPPDATA%/rfe-tool/
        """
        if HAS_PLATFORMDIRS:
            return Path(platformdirs.user_data_dir(app_name, "redhat"))
        else:
            if Platform.is_windows():
                base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
            elif Platform.is_macos():
                base = Path.home() / 'Library' / 'Application Support'
            else:  # Linux
                base = Path.home() / '.local' / 'share'
            return base / app_name
    
    @staticmethod
    def cache_dir(app_name: str = "rfe-tool") -> Path:
        """
        Application cache directory (OS-appropriate)
        - Linux: ~/.cache/rfe-tool/
        - macOS: ~/Library/Caches/rfe-tool/
        - Windows: %LOCALAPPDATA%/rfe-tool/Cache/
        """
        if HAS_PLATFORMDIRS:
            return Path(platformdirs.user_cache_dir(app_name, "redhat"))
        else:
            if Platform.is_windows():
                base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
                return base / app_name / 'Cache'
            elif Platform.is_macos():
                return Path.home() / 'Library' / 'Caches' / app_name
            else:  # Linux
                return Path.home() / '.cache' / app_name
    
    @staticmethod
    def log_dir(app_name: str = "rfe-tool") -> Path:
        """
        Application log directory (OS-appropriate)
        - Linux: ~/.local/state/rfe-tool/log/
        - macOS: ~/Library/Logs/rfe-tool/
        - Windows: %LOCALAPPDATA%/rfe-tool/Logs/
        """
        if HAS_PLATFORMDIRS:
            return Path(platformdirs.user_log_dir(app_name, "redhat"))
        else:
            if Platform.is_windows():
                base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
                return base / app_name / 'Logs'
            elif Platform.is_macos():
                return Path.home() / 'Library' / 'Logs' / app_name
            else:  # Linux
                return Path.home() / '.local' / 'state' / app_name / 'log'
    
    @staticmethod
    def temp_dir() -> Path:
        """Temporary directory (cross-platform)"""
        import tempfile
        return Path(tempfile.gettempdir())
    
    @staticmethod
    def ensure_dirs(app_name: str = "rfe-tool") -> None:
        """Create all required directories"""
        for dir_func in [Platform.config_dir, Platform.data_dir, 
                         Platform.cache_dir, Platform.log_dir]:
            dir_path = dir_func(app_name)
            dir_path.mkdir(parents=True, exist_ok=True)
    
    # ==================== Secret Management ====================
    
    @staticmethod
    def get_secret(service: str, key: str) -> Optional[str]:
        """
        Get secret from OS keychain (cross-platform)
        - Linux: Secret Service (GNOME Keyring, KWallet)
        - macOS: Keychain
        - Windows: Credential Manager
        """
        if not HAS_KEYRING:
            return None
        try:
            return keyring.get_password(service, key)
        except Exception:
            return None
    
    @staticmethod
    def set_secret(service: str, key: str, value: str) -> bool:
        """
        Store secret in OS keychain (cross-platform)
        Returns True on success, False on failure
        """
        if not HAS_KEYRING:
            return False
        try:
            keyring.set_password(service, key, value)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete_secret(service: str, key: str) -> bool:
        """Delete secret from OS keychain (cross-platform)"""
        if not HAS_KEYRING:
            return False
        try:
            keyring.delete_password(service, key)
            return True
        except Exception:
            return False
    
    # ==================== Shell & Execution ====================
    
    @staticmethod
    def shell_available() -> list[str]:
        """
        Get available shells (cross-platform)
        Returns list of shell names
        """
        if Platform.is_windows():
            return ['powershell', 'cmd']
        else:
            return ['bash', 'zsh', 'fish']
    
    @staticmethod
    def default_shell() -> str:
        """Get default shell for this platform"""
        if Platform.is_windows():
            return 'powershell'
        else:
            shell = os.environ.get('SHELL', '/bin/bash')
            return os.path.basename(shell)
    
    @staticmethod
    def executable_extension() -> str:
        """Get executable file extension for this platform"""
        return '.exe' if Platform.is_windows() else ''
    
    @staticmethod
    def path_separator() -> str:
        """Get PATH separator for this platform"""
        return ';' if Platform.is_windows() else ':'
    
    @staticmethod
    def line_ending() -> str:
        """Get line ending for this platform"""
        return '\r\n' if Platform.is_windows() else '\n'
    
    # ==================== File Operations ====================
    
    @staticmethod
    def open_file(path: Path) -> bool:
        """Open file with default application (cross-platform)"""
        import subprocess
        try:
            if Platform.is_macos():
                subprocess.run(['open', str(path)], check=True)
            elif Platform.is_linux():
                subprocess.run(['xdg-open', str(path)], check=True)
            elif Platform.is_windows():
                os.startfile(str(path))
            return True
        except Exception:
            return False
    
    @staticmethod
    def open_url(url: str) -> bool:
        """Open URL in default browser (cross-platform)"""
        import webbrowser
        return webbrowser.open(url)
    
    # ==================== Python Environment ====================
    
    @staticmethod
    def python_version() -> str:
        """Get Python version string"""
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    @staticmethod
    def python_executable() -> Path:
        """Get path to Python executable"""
        return Path(sys.executable)


# Global instance for convenience
platform = Platform()


# Convenience function for legacy code migration
def migrate_path(old_path: str, app_name: str = "rfe-tool") -> Path:
    """
    Migrate hardcoded paths to platform-agnostic paths
    
    Example:
        migrate_path("/home/jbyrd/.config/tamscripts") → Platform.config_dir("rfe-tool")
        migrate_path("~/Documents/rh") → Platform.data_dir("rfe-tool")
    """
    old_path = os.path.expanduser(old_path)
    
    # Detect what kind of directory this is
    if '.config' in old_path or 'AppData/Roaming' in old_path:
        return Platform.config_dir(app_name)
    elif '.local/share' in old_path or 'Application Support' in old_path:
        return Platform.data_dir(app_name)
    elif '.cache' in old_path or 'Caches' in old_path:
        return Platform.cache_dir(app_name)
    elif 'Documents' in old_path:
        return Platform.data_dir(app_name)
    else:
        # Default to data directory
        return Platform.data_dir(app_name)

