"""Service Layer for Server Manager Application

This package contains business logic and service classes:
- Server management service
- Configuration service
- Process management service
"""

# Import and expose the build_config module specifically
# Other modules are imported only when needed to avoid circular dependencies
from .build_config import build_config, BuildConfig

__all__ = [
    'build_config',
    'BuildConfig',
]