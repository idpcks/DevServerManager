"""
Build-time Configuration Manager

This module embeds environment variables at build time for secure distribution.
Only developers can modify these values during the build process.
"""

import os
from typing import Dict, Any, TypeVar, Union, overload
from dotenv import load_dotenv

T = TypeVar('T')


class BuildConfig:
    """Build-time configuration that gets embedded into the executable."""
    
    def __init__(self):
        """Initialize build configuration by loading .env at build time."""
        # Load .env only during build process
        load_dotenv()
        
        # Embed critical configurations at build time
        self._build_config = {
            # Application Settings (embedded at build time)
            'APP_NAME': os.getenv('APP_NAME', 'DevServer Manager'),
            'APP_VERSION': os.getenv('APP_VERSION', '2.1.3'),
            'APP_DEBUG': os.getenv('APP_DEBUG', 'false').lower() == 'true',
            
            # Window Configuration (embedded)
            'WINDOW_TITLE': os.getenv('WINDOW_TITLE', 'DevServer Manager'),
            'WINDOW_WIDTH': int(os.getenv('WINDOW_WIDTH', '1200')),
            'WINDOW_HEIGHT': int(os.getenv('WINDOW_HEIGHT', '800')),
            'WINDOW_MIN_WIDTH': int(os.getenv('WINDOW_MIN_WIDTH', '800')),
            'WINDOW_MIN_HEIGHT': int(os.getenv('WINDOW_MIN_HEIGHT', '600')),
            
            # GitHub Configuration (embedded for security)
            'GITHUB_OWNER': os.getenv('GITHUB_OWNER', 'idpcks'),
            'GITHUB_REPO': os.getenv('GITHUB_REPO', 'DevServerManager'),
            'GITHUB_REPO_URL': os.getenv('GITHUB_REPO_URL', 'https://github.com/idpcks/DevServerManager'),
            
            # Update Configuration (embedded)
            'UPDATE_CHECK_INTERVAL_HOURS': int(os.getenv('UPDATE_CHECK_INTERVAL_HOURS', '24')),
            'UPDATE_CACHE_DURATION_HOURS': int(os.getenv('UPDATE_CACHE_DURATION_HOURS', '1')),
            'AUTO_UPDATE_CHECK': os.getenv('AUTO_UPDATE_CHECK', 'true').lower() == 'true',
            
            # Theme Configuration (embedded)
            'DEFAULT_THEME': os.getenv('DEFAULT_THEME', 'system'),
            'THEME_DARK_BG': os.getenv('THEME_DARK_BG', '#2c3e50'),
            'THEME_DARK_FG': os.getenv('THEME_DARK_FG', '#ecf0f1'),
            'THEME_LIGHT_BG': os.getenv('THEME_LIGHT_BG', '#ffffff'),
            'THEME_LIGHT_FG': os.getenv('THEME_LIGHT_FG', '#2c3e50'),
            
            # Build Configuration (embedded)
            'BUILD_EXCLUDE_MODULES': os.getenv('BUILD_EXCLUDE_MODULES', 
                'tkinter.test,unittest,test,doctest,pdb,pydoc').split(','),
            'BUILD_INCLUDE_MODULES': os.getenv('BUILD_INCLUDE_MODULES',
                'tkinter,tkinter.ttk,tkinter.messagebox,tkinter.filedialog,PIL.Image,PIL.ImageTk,requests,json,threading,subprocess,sys,os').split(','),
        }
        
        # User-configurable settings (can be modified at runtime)
        self._user_config = {
            # Paths Configuration (user can modify)
            'CONFIG_DIR': 'config',
            'LOGS_DIR': 'logs',
            'ASSETS_DIR': 'assets',
            
            # Server Defaults (user can modify)
            'DEFAULT_SERVER_PORT': 8000,
            'DEFAULT_SERVER_HOST': '127.0.0.1',
            'DEFAULT_SERVER_COMMAND': 'python -m http.server',
            
            # Performance Settings (user can modify)
            'MAX_CONCURRENT_SERVERS': 10,
            'SERVER_STARTUP_TIMEOUT': 30,
            'AUTO_CLEANUP_INTERVAL': 300,
            
            # Logging Configuration (user can modify)
            'LOG_LEVEL': 'INFO',
            'LOG_MAX_SIZE': 10485760,
            'LOG_BACKUP_COUNT': 5,
        }
    
    @overload
    def get_build_config(self, key: str) -> Any: ...
    
    @overload
    def get_build_config(self, key: str, default: T) -> Union[Any, T]: ...
    
    def get_build_config(self, key: str, default: Any = None) -> Any:
        """Get build-time embedded configuration (immutable).
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value (embedded at build time)
        """
        return self._build_config.get(key, default)
    
    @overload
    def get_user_config(self, key: str) -> Any: ...
    
    @overload
    def get_user_config(self, key: str, default: T) -> Union[Any, T]: ...
    
    def get_user_config(self, key: str, default: Any = None) -> Any:
        """Get user-configurable setting.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value (can be modified by user)
        """
        return self._user_config.get(key, default)
    
    def set_user_config(self, key: str, value: Any) -> bool:
        """Set user-configurable setting.
        
        Args:
            key: Configuration key
            value: Value to set
            
        Returns:
            True if successfully set (only user-configurable settings can be modified)
        """
        if key in self._user_config:
            self._user_config[key] = value
            return True
        return False  # Build config cannot be modified
    
    def get_all_build_config(self) -> Dict[str, Any]:
        """Get all build-time configuration (read-only)."""
        return self._build_config.copy()
    
    def get_all_user_config(self) -> Dict[str, Any]:
        """Get all user-configurable settings."""
        return self._user_config.copy()


# Global build configuration instance
build_config = BuildConfig()