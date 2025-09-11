"""
DevServer Manager - A modern GUI application for managing multiple development servers.

This package provides a comprehensive solution for managing multiple development
servers with an intuitive graphical user interface, system tray integration,
and advanced features like server templates and auto-update checking.
"""

__version__ = "2.1.1"
__author__ = "idpcks"
__email__ = "idpcks.container103@slmail.me"

# Import main components for easy access
from .gui.main_window import MainWindow
from .services.server_manager import ServerManagerService
from .services.config_manager import ConfigManager
from .services.update_checker import UpdateCheckerService

__all__ = [
    "MainWindow",
    "ServerManagerService", 
    "ConfigManager",
    "UpdateCheckerService",
]