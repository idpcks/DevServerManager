"""Server Management Service

This module contains the business logic for managing servers.
"""

import subprocess
import os
import signal
from typing import Dict, List, Optional, Callable
from models.server_config import ServerConfig
from .template_manager import TemplateManager
from .env_manager import env_manager


class ServerManagerService:
    """Service class for managing server processes."""
    
    def __init__(self, log_callback: Optional[Callable[[str, str], None]] = None):
        """Initialize server manager service.
        
        Args:
            log_callback: Optional callback function for logging messages
        """
        # Load environment variables
        env_manager.load_env()
        
        self.servers: Dict[str, ServerConfig] = {}
        self.log_callback = log_callback
        self._initialized = False
        self.template_manager = TemplateManager()
    
    def initialize(self) -> bool:
        """Initialize the server manager service.
        
        Returns:
            True if initialization was successful
        """
        try:
            self._initialized = True
            self._log("Server manager service initialized successfully", "INFO")
            return True
        except Exception as e:
            self._log(f"Error initializing server manager service: {e}", "ERROR")
            return False
    
    def cleanup(self) -> None:
        """Cleanup server manager resources."""
        try:
            # Stop all running servers
            self.stop_all_servers()
            self._log("Server manager service cleanup completed", "INFO")
        except Exception as e:
            self._log(f"Error during server manager cleanup: {e}", "ERROR")
    
    def add_server(self, server_config: ServerConfig) -> bool:
        """Add a new server configuration.
        
        Args:
            server_config: Server configuration to add
            
        Returns:
            True if server was added successfully, False otherwise
        """
        try:
            # Validate configuration
            is_valid, error_msg = server_config.validate()
            if not is_valid:
                self._log(f"Invalid server configuration: {error_msg}", "ERROR")
                return False
            
            # Check if server name already exists
            if server_config.name in self.servers:
                self._log(f"Server '{server_config.name}' already exists", "ERROR")
                return False
            
            # Add server
            self.servers[server_config.name] = server_config
            self._log(f"Server '{server_config.name}' added successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self._log(f"Error adding server: {str(e)}", "ERROR")
            return False
    
    def update_server(self, old_name: str, server_config: ServerConfig) -> bool:
        """Update an existing server configuration.
        
        Args:
            old_name: Current name of the server
            server_config: New server configuration
            
        Returns:
            True if server was updated successfully, False otherwise
        """
        try:
            # Validate configuration
            is_valid, error_msg = server_config.validate()
            if not is_valid:
                self._log(f"Invalid server configuration: {error_msg}", "ERROR")
                return False
            
            # Check if old server exists
            if old_name not in self.servers:
                self._log(f"Server '{old_name}' not found", "ERROR")
                return False
            
            # Stop server if running
            if self.servers[old_name].is_running():
                self.stop_server(old_name)
            
            # Remove old server and add new one
            del self.servers[old_name]
            self.servers[server_config.name] = server_config
            
            self._log(f"Server '{old_name}' updated to '{server_config.name}'", "SUCCESS")
            return True
            
        except Exception as e:
            self._log(f"Error updating server: {str(e)}", "ERROR")
            return False
    
    def remove_server(self, server_name: str) -> bool:
        """Remove a server configuration.
        
        Args:
            server_name: Name of the server to remove
            
        Returns:
            True if server was removed successfully, False otherwise
        """
        try:
            if server_name not in self.servers:
                self._log(f"Server '{server_name}' not found", "ERROR")
                return False
            
            # Stop server if running
            if self.servers[server_name].is_running():
                self.stop_server(server_name)
            
            # Remove server
            del self.servers[server_name]
            self._log(f"Server '{server_name}' removed successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self._log(f"Error removing server: {str(e)}", "ERROR")
            return False
    
    def start_server(self, server_name: str) -> bool:
        """Start a server.
        
        Args:
            server_name: Name of the server to start
            
        Returns:
            True if server was started successfully, False otherwise
        """
        try:
            if server_name not in self.servers:
                self._log(f"Server '{server_name}' not found", "ERROR")
                return False
            
            server = self.servers[server_name]
            
            # Check if already running
            if server.is_running():
                self._log(f"Server '{server_name}' is already running", "WARNING")
                return False
            
            # Check if path exists
            if not os.path.exists(server.path):
                self._log(f"Server path does not exist: {server.path}", "ERROR")
                return False
            
            # Prepare command using template system
            port_num = None
            if server.port.strip():
                try:
                    port_num = int(server.port)
                except ValueError:
                    self._log(f"Invalid port number: {server.port}", "WARNING")
            
            # Build command using template manager
            command_to_run = self.template_manager.build_command(
                server.template_id,
                server.command,
                port=port_num
            )
            
            # Get environment variables from template
            env_vars = os.environ.copy()
            template_env = self.template_manager.get_environment_vars(
                server.template_id,
                port=port_num
            )
            env_vars.update(template_env)
            env_vars.update(server.env_vars)  # User-defined env vars override template ones
            
            if port_num:
                self._log(f"Starting server '{server_name}' on port {port_num}...", "INFO")
            else:
                self._log(f"Starting server '{server_name}' without specific port...", "INFO")
            
            self._log(f"Command: {command_to_run}", "DEBUG")
            if template_env or server.env_vars:
                env_info = {**template_env, **server.env_vars}
                self._log(f"Environment variables: {env_info}", "DEBUG")
            
            process = subprocess.Popen(
                command_to_run,
                shell=True,
                cwd=server.path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                env=env_vars
            )
            
            server.process = process
            server.status = 'Running'
            self._log(f"Server '{server_name}' started successfully (PID: {process.pid})", "SUCCESS")
            return True
            
        except Exception as e:
            self._log(f"Error starting server '{server_name}': {str(e)}", "ERROR")
            return False
    
    def stop_server(self, server_name: str) -> bool:
        """Stop a server.
        
        Args:
            server_name: Name of the server to stop
            
        Returns:
            True if server was stopped successfully, False otherwise
        """
        try:
            if server_name not in self.servers:
                self._log(f"Server '{server_name}' not found", "ERROR")
                return False
            
            server = self.servers[server_name]
            
            if not server.is_running():
                self._log(f"Server '{server_name}' is not running", "WARNING")
                return False
            
            # Stop server process
            self._log(f"Stopping server '{server_name}'...", "INFO")
            
            try:
                # Try graceful shutdown first
                server.process.terminate()
                server.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if graceful shutdown fails
                server.process.kill()
                server.process.wait()
            
            server.process = None
            server.status = 'Stopped'
            self._log(f"Server '{server_name}' stopped successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self._log(f"Error stopping server '{server_name}': {str(e)}", "ERROR")
            return False
    
    def stop_all_servers(self) -> None:
        """Stop all running servers."""
        self._log("Stopping all servers...", "INFO")
        
        for server_name, server in self.servers.items():
            if server.is_running():
                self.stop_server(server_name)
    
    def get_running_servers(self) -> List[str]:
        """Get list of running server names.
        
        Returns:
            List of running server names
        """
        return [name for name, server in self.servers.items() if server.is_running()]
    
    def get_server_status(self, server_name: str) -> Optional[str]:
        """Get server status.
        
        Args:
            server_name: Name of the server
            
        Returns:
            Server status string or None if server not found
        """
        if server_name not in self.servers:
            return None
        
        server = self.servers[server_name]
        return "Running" if server.is_running() else "Stopped"
    
    def get_all_servers(self) -> Dict[str, ServerConfig]:
        """Get all server configurations.
        
        Returns:
            Dictionary of all server configurations
        """
        return self.servers.copy()
    
    def get_server(self, server_name: str) -> Optional[ServerConfig]:
        """Get a specific server configuration.
        
        Args:
            server_name: Name of the server
            
        Returns:
            Server configuration if found, None otherwise
        """
        return self.servers.get(server_name)
    
    def detect_project_type(self, project_path: str) -> List[tuple]:
        """Auto-detect project type for a given path.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            List of tuples: (template_id, template_config, confidence_score)
        """
        return self.template_manager.detect_project_type(project_path)
    
    def get_suggested_config(self, project_path: str, template_id: Optional[str] = None) -> Dict:
        """Get suggested server configuration for a project.
        
        Args:
            project_path: Path to the project directory
            template_id: Specific template to use, or None for auto-detection
            
        Returns:
            Dictionary with suggested configuration
        """
        return self.template_manager.get_suggested_config(project_path, template_id)
    
    def get_available_templates(self) -> Dict:
        """Get all available server templates.
        
        Returns:
            Dictionary of available templates
        """
        return self.template_manager.get_all_templates()
    
    def get_template_categories(self) -> Dict:
        """Get all template categories.
        
        Returns:
            Dictionary of template categories
        """
        return self.template_manager.get_categories()
    
    def validate_project_path(self, project_path: str, template_id: str) -> tuple:
        """Validate if project path is suitable for the given template.
        
        Args:
            project_path: Path to the project directory
            template_id: Template identifier
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        return self.template_manager.validate_project_path(project_path, template_id)
    
    def _log(self, message: str, level: str = "INFO") -> None:
        """Log a message using the callback function.
        
        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR, SUCCESS)
        """
        if self.log_callback:
            self.log_callback(message, level)