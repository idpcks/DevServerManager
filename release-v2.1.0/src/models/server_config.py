"""Server Configuration Model

This module contains data models for server configuration.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import subprocess


@dataclass
class ServerConfig:
    """Server configuration data model."""
    
    name: str
    path: str
    port: str
    command: str
    process: Optional[subprocess.Popen] = None
    status: str = 'Stopped'
    template_id: str = 'custom'
    category: str = 'custom'
    env_vars: Dict[str, str] = field(default_factory=dict)
    alternative_commands: List[str] = field(default_factory=list)
    description: str = ''
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert server config to dictionary.
        
        Returns:
            Dictionary representation of server config
        """
        return {
            'name': self.name,
            'path': self.path,
            'port': self.port,
            'command': self.command,
            'template_id': self.template_id,
            'category': self.category,
            'env_vars': self.env_vars,
            'alternative_commands': self.alternative_commands,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ServerConfig':
        """Create server config from dictionary.
        
        Args:
            data: Dictionary containing server config data
            
        Returns:
            ServerConfig instance
        """
        return cls(
            name=data.get('name', ''),
            path=data.get('path', ''),
            port=data.get('port', ''),
            command=data.get('command', ''),
            template_id=data.get('template_id', 'custom'),
            category=data.get('category', 'custom'),
            env_vars=data.get('env_vars', {}),
            alternative_commands=data.get('alternative_commands', []),
            description=data.get('description', '')
        )
    
    def is_running(self) -> bool:
        """Check if server process is running.
        
        Returns:
            True if server is running, False otherwise
        """
        return self.process is not None and self.process.poll() is None
    
    def validate(self) -> tuple[bool, str]:
        """Validate server configuration.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.name.strip():
            return False, "Server name is required"
        
        if not self.path.strip():
            return False, "Server path is required"
        
        # Port is now optional
        if self.port.strip():
            try:
                port_num = int(self.port)
                if port_num < 1 or port_num > 65535:
                    return False, "Port must be between 1 and 65535"
            except ValueError:
                return False, "Port must be a valid number"
        
        if not self.command.strip():
            return False, "Start command is required"
        
        return True, ""