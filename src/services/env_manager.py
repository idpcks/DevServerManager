"""Environment Variables Management Service

This module handles loading and managing environment variables using python-dotenv.
"""

import os
from typing import Any, Optional, Dict
from dotenv import load_dotenv
from pathlib import Path


class EnvManager:
    """Service class for managing environment variables."""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize environment manager.
        
        Args:
            env_file: Path to the .env file
        """
        self.env_file = env_file
        self.env_path = Path(env_file)
        self._loaded = False
        
    def load_env(self) -> bool:
        """Load environment variables from .env file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if self.env_path.exists():
                load_dotenv(self.env_path)
                self._loaded = True
                return True
            else:
                # Create default .env file if it doesn't exist
                self._create_default_env()
                load_dotenv(self.env_path)
                self._loaded = True
                return True
        except Exception as e:
            print(f"Error loading environment variables: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get environment variable value.
        
        Args:
            key: Environment variable key
            default: Default value if key not found
            
        Returns:
            Environment variable value or default
        """
        if not self._loaded:
            self.load_env()
        
        return os.getenv(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get environment variable as integer.
        
        Args:
            key: Environment variable key
            default: Default value if key not found or invalid
            
        Returns:
            Environment variable value as integer or default
        """
        try:
            value = self.get(key, str(default))
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get environment variable as boolean.
        
        Args:
            key: Environment variable key
            default: Default value if key not found
            
        Returns:
            Environment variable value as boolean or default
        """
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_list(self, key: str, separator: str = ',', default: Optional[list] = None) -> list:
        """Get environment variable as list.
        
        Args:
            key: Environment variable key
            separator: Separator character for splitting
            default: Default value if key not found
            
        Returns:
            Environment variable value as list or default
        """
        if default is None:
            default = []
        
        value = self.get(key, '')
        if not value:
            return default
        
        return [item.strip() for item in value.split(separator) if item.strip()]
    
    def set(self, key: str, value: Any) -> None:
        """Set environment variable.
        
        Args:
            key: Environment variable key
            value: Value to set
        """
        os.environ[key] = str(value)
    
    def get_all_env_vars(self) -> Dict[str, str]:
        """Get all environment variables as dictionary.
        
        Returns:
            Dictionary of all environment variables
        """
        return dict(os.environ)
    
    def _create_default_env(self) -> None:
        """Create default .env file with basic configuration."""
        default_content = """# DevServer Manager Environment Configuration
# This file contains environment variables for the application

# Application Settings
APP_NAME=DevServer Manager
APP_VERSION=2.1.3
APP_DEBUG=false

# Default Server Configuration
DEFAULT_SERVER_PORT=8000
DEFAULT_SERVER_HOST=127.0.0.1
DEFAULT_SERVER_COMMAND=python -m http.server

# Paths Configuration
CONFIG_DIR=config
LOGS_DIR=logs
ASSETS_DIR=assets

# Theme Configuration
DEFAULT_THEME=system
THEME_DARK_BG=#2c3e50
THEME_DARK_FG=#ecf0f1
THEME_LIGHT_BG=#ffffff
THEME_LIGHT_FG=#2c3e50

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# Update Configuration
AUTO_UPDATE_CHECK=true
UPDATE_CHECK_INTERVAL_HOURS=24
UPDATE_CACHE_DURATION_HOURS=1
GITHUB_OWNER=idpcks
GITHUB_REPO=DevServerManager
GITHUB_REPO_URL=https://github.com/idpcks/DevServerManager

# Security Configuration
ENABLE_IP_BANNING=false
MAX_LOGIN_ATTEMPTS=5
SESSION_TIMEOUT=3600

# Performance Configuration
MAX_CONCURRENT_SERVERS=10
SERVER_STARTUP_TIMEOUT=30
AUTO_CLEANUP_INTERVAL=300

# Build Configuration
BUILD_EXCLUDE_MODULES=tkinter.test,unittest,test,doctest,pdb,pydoc
BUILD_INCLUDE_MODULES=tkinter,tkinter.ttk,tkinter.messagebox,tkinter.filedialog,PIL.Image,PIL.ImageTk,requests,json,threading,subprocess,sys,os

# Application Window Configuration
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
WINDOW_MIN_WIDTH=800
WINDOW_MIN_HEIGHT=600
WINDOW_TITLE=DevServer Manager
"""
        
        try:
            with open(self.env_path, 'w', encoding='utf-8') as f:
                f.write(default_content)
        except Exception as e:
            print(f"Error creating default .env file: {e}")


# Global instance
env_manager = EnvManager()
