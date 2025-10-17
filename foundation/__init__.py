"""
PAI Foundation - Cross-Platform Abstraction Layer
Part of the Personal AI Infrastructure (PAI) Framework

This package provides OS-agnostic abstractions for:
- Platform detection (Linux/macOS/Windows)
- Directory management (config, data, cache, logs)
- Secret management (OS keychain integration)
- File operations (cross-platform paths)
"""

from .platform import Platform, platform

__all__ = ["Platform", "platform"]
__version__ = "1.0.0"

