"""Configuration Management Service

This module handles loading and saving application configurations.
"""

import json
import os
from typing import Dict, Any, Optional, List
from ..models.server_config import ServerConfig


class ConfigManager:
    """Service class for managing application configuration."""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        self.server_config_file = os.path.join(config_dir, "server_config.json")
        self.theme_config_file = os.path.join(config_dir, "theme_config.json")
        
        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)
        
        self._initialized = False
    
    def initialize(self) -> bool:
        """Initialize the configuration manager.
        
        Returns:
            True if initialization was successful
        """
        try:
            self._initialized = True
            print("Configuration manager initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing configuration manager: {e}")
            return False
    
    def cleanup(self) -> None:
        """Cleanup configuration manager resources."""
        try:
            print("Configuration manager cleanup completed")
        except Exception as e:
            print(f"Error during configuration manager cleanup: {e}")
    
    def save_all_configs(self) -> None:
        """Save all configurations."""
        try:
            # Save server configurations
            self.save_server_configs(self.load_server_configs())
            print("All configurations saved")
        except Exception as e:
            print(f"Error saving configurations: {e}")
    
    def get_theme_config(self) -> Optional[Dict[str, Any]]:
        """Get theme configuration.
        
        Returns:
            Theme configuration dictionary or None
        """
        try:
            return self.load_theme_config()
        except Exception:
            return None
    
    def load_server_config(self) -> Dict[str, Any]:
        """Load server configuration.
        
        Returns:
            Server configuration dictionary
        """
        try:
            return self.load_server_configs()
        except Exception as e:
            print(f"Error loading server config: {e}")
            return {}
    
    def save_server_config(self, servers: Dict[str, Any]) -> bool:
        """Save server configuration (compatibility method).
        
        Args:
            servers: Dictionary of server configurations to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Convert to ServerConfig objects if needed
            server_configs = {}
            for name, config in servers.items():
                if hasattr(config, 'to_dict'):
                    # Already a ServerConfig object
                    server_configs[name] = config
                else:
                    # Convert dict to ServerConfig
                    from ..models.server_config import ServerConfig
                    server_configs[name] = ServerConfig(
                        name=config.get('name', name),
                        path=config.get('path', ''),
                        port=str(config.get('port', 8000)),
                        command=config.get('command', 'python -m http.server')
                    )
            
            return self.save_server_configs(server_configs)
        except Exception as e:
            print(f"Error saving server config: {e}")
            return False
    
    def load_server_configs(self) -> Dict[str, ServerConfig]:
        """Load server configurations from file.
        
        Returns:
            Dictionary of server configurations
        """
        try:
            if not os.path.exists(self.server_config_file):
                default_servers = self._create_default_server_config()
                # Save default servers to file
                self.save_server_configs(default_servers)
                return default_servers
            
            with open(self.server_config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            servers = {}
            server_data_dict = data.get('servers', {})
            
            # If servers dict is empty, create and save default servers
            if not server_data_dict:
                default_servers = self._create_default_server_config()
                self.save_server_configs(default_servers)
                return default_servers
            
            for server_name, server_data in server_data_dict.items():
                servers[server_name] = ServerConfig.from_dict(server_data)
            
            return servers
            
        except Exception as e:
            print(f"Error loading server config: {e}")
            default_servers = self._create_default_server_config()
            # Save default servers to file
            self.save_server_configs(default_servers)
            return default_servers
    
    def save_server_configs(self, servers: Dict[str, ServerConfig]) -> bool:
        """Save server configurations to file.
        
        Args:
            servers: Dictionary of server configurations to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Convert servers to dictionary format
            servers_data = {}
            for server_name, server_config in servers.items():
                servers_data[server_name] = server_config.to_dict()
            
            config_data = {
                'servers': servers_data,
                'version': '1.0.0'
            }
            
            # Save to file
            with open(self.server_config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving server config: {e}")
            return False
    
    def load_theme_config(self) -> Dict[str, Any]:
        """Load theme configuration from file.
        
        Returns:
            Dictionary containing theme configuration
        """
        try:
            if not os.path.exists(self.theme_config_file):
                return self._create_default_theme_config()
            
            with open(self.theme_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
            
        except Exception as e:
            print(f"Error loading theme config: {e}")
            return self._create_default_theme_config()
    
    def save_theme_config(self, theme_config: Dict[str, Any]) -> bool:
        """Save theme configuration to file.
        
        Args:
            theme_config: Theme configuration to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self.theme_config_file, 'w', encoding='utf-8') as f:
                json.dump(theme_config, f, indent=4, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving theme config: {e}")
            return False
    
    def get_config_file_path(self, config_type: str) -> str:
        """Get path to configuration file.
        
        Args:
            config_type: Type of config ('server' or 'theme')
            
        Returns:
            Path to configuration file
        """
        if config_type == 'server':
            return self.server_config_file
        elif config_type == 'theme':
            return self.theme_config_file
        else:
            raise ValueError(f"Unknown config type: {config_type}")
    
    def backup_config(self, config_type: str) -> Optional[str]:
        """Create backup of configuration file.
        
        Args:
            config_type: Type of config to backup ('server' or 'theme')
            
        Returns:
            Path to backup file or None if failed
        """
        try:
            config_file = self.get_config_file_path(config_type)
            
            if not os.path.exists(config_file):
                return None
            
            backup_file = f"{config_file}.backup"
            
            with open(config_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            return backup_file
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
    
    def restore_config(self, config_type: str) -> bool:
        """Restore configuration from backup.
        
        Args:
            config_type: Type of config to restore ('server' or 'theme')
            
        Returns:
            True if restored successfully, False otherwise
        """
        try:
            config_file = self.get_config_file_path(config_type)
            backup_file = f"{config_file}.backup"
            
            if not os.path.exists(backup_file):
                return False
            
            with open(backup_file, 'r', encoding='utf-8') as src:
                with open(config_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            return True
            
        except Exception as e:
            print(f"Error restoring config: {e}")
            return False
    
    def _create_default_server_config(self) -> Dict[str, ServerConfig]:
        """Create default server configuration.
        
        Returns:
            Dictionary with empty server configurations (no example servers)
        """
        # Return empty server configuration - no example servers
        default_servers = {}
        
        # Save empty configuration
        self.save_server_configs(default_servers)
        
        return default_servers
    
    def _create_default_theme_config(self) -> Dict[str, Any]:
        """Create default theme configuration.
        
        Returns:
            Dictionary with default theme configuration
        """
        default_theme = {
            "current_theme": "system",
            "themes": {
                "dark": {
                    "bg": "#2c3e50",
                    "fg": "#ecf0f1",
                    "select_bg": "#34495e",
                    "select_fg": "#ecf0f1",
                    "button_bg": "#3498db",
                    "button_fg": "white",
                    "entry_bg": "#34495e",
                    "entry_fg": "#ecf0f1"
                },
                "light": {
                    "bg": "#ffffff",
                    "fg": "#2c3e50",
                    "select_bg": "#ecf0f1",
                    "select_fg": "#2c3e50",
                    "button_bg": "#3498db",
                    "button_fg": "white",
                    "entry_bg": "#ffffff",
                    "entry_fg": "#2c3e50"
                }
            }
        }
        
        # Save default configuration
        self.save_theme_config(default_theme)
        
        return default_theme