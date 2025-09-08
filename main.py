#!/usr/bin/env python3
"""Main Entry Point for DevServer Manager Application

This is the main entry point for the DevServer Manager GUI application.
It initializes all services and starts the GUI.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.gui.main_window import MainWindow
from src.services.config_manager import ConfigManager
from src.services.server_manager import ServerManagerService
from utils.logger import app_logger
from utils.file_utils import FileUtils
from src.gui.splashscreen import show_splash


class DevServerManagerApp:
    """Main application class that coordinates all components."""
    
    def __init__(self):
        """Initialize the application."""
        self.root = None
        self.main_window = None
        self.config_manager = None
        self.server_manager = None
        
        # Application directories
        self.app_dir = Path(__file__).parent
        self.config_dir = self.app_dir / "config"
        self.logs_dir = self.app_dir / "logs"
        self.assets_dir = self.app_dir / "assets"
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [self.config_dir, self.logs_dir, self.assets_dir]
        
        for directory in directories:
            FileUtils.ensure_directory(directory)
            app_logger.info(f"Ensured directory exists: {directory}")
    
    def initialize_services(self) -> bool:
        """Initialize all application services.
        
        Returns:
            True if all services initialized successfully
        """
        try:
            app_logger.info("Initializing application services...")
            
            # Initialize configuration manager
            self.config_manager = ConfigManager(self.config_dir)
            if not self.config_manager.initialize():
                app_logger.error("Failed to initialize configuration manager")
                return False
            
            # Initialize server manager
            self.server_manager = ServerManagerService()
            if not self.server_manager.initialize():
                app_logger.error("Failed to initialize server manager")
                return False
            
            app_logger.info("All services initialized successfully")
            return True
            
        except Exception as e:
            app_logger.error(f"Error initializing services: {e}")
            return False
    
    def create_gui(self) -> bool:
        """Create and setup the GUI.
        
        Returns:
            True if GUI was created successfully
        """
        try:
            app_logger.info("Creating GUI...")
            
            # Create root window
            self.root = tk.Tk()
            self.root.title("DevServer Manager")
            
            # Create main window
            self.main_window = MainWindow(self.root)
            
            # Apply saved theme
            theme_config = self.config_manager.get_theme_config()
            if theme_config:
                self.main_window.apply_theme(theme_config)
            
            # Setup window close handler
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            
            app_logger.info("GUI created successfully")
            return True
            
        except Exception as e:
            app_logger.error(f"Error creating GUI: {e}")
            return False
    
    def run(self) -> None:
        """Run the application with splash screen."""
        try:
            app_logger.info("Starting DevServer Manager Application")
            
            # Define main app initialization function for splash screen callback
            def init_main_app():
                try:
                    # Initialize services
                    if not self.initialize_services():
                        self._show_error("Failed to initialize application services")
                        return
                    
                    # Create GUI
                    if not self.create_gui():
                        self._show_error("Failed to create application GUI")
                        return
                    
                    # Start GUI main loop
                    app_logger.info("Starting GUI main loop")
                    self.root.mainloop()
                    
                except Exception as e:
                    app_logger.error(f"Error in main app initialization: {e}")
                    self._show_error(f"Error starting application: {e}")
                finally:
                    self._cleanup()
            
            # Show splash screen with callback to main app
            show_splash(init_main_app)
            
        except KeyboardInterrupt:
            app_logger.info("Application interrupted by user")
        except Exception as e:
            app_logger.error(f"Unexpected error in main application: {e}")
            self._show_error(f"Unexpected error: {e}")
    
    def _on_closing(self) -> None:
        """Handle application closing."""
        try:
            app_logger.info("Application closing...")
            
            # Stop all running servers
            if self.server_manager:
                running_servers = self.server_manager.get_running_servers()
                if running_servers:
                    result = messagebox.askyesnocancel(
                        "Confirm Exit",
                        f"There are {len(running_servers)} running servers. "
                        "Do you want to stop them before exiting?",
                        parent=self.root
                    )
                    
                    if result is None:  # Cancel
                        return
                    elif result:  # Yes, stop servers
                        for server_name in running_servers:
                            self.server_manager.stop_server(server_name)
                        app_logger.info("All servers stopped")
            
            # Save configuration
            if self.config_manager:
                self.config_manager.save_all_configs()
                app_logger.info("Configuration saved")
            
            # Close application
            self.root.quit()
            
        except Exception as e:
            app_logger.error(f"Error during application closing: {e}")
            self.root.quit()
    
    def _cleanup(self) -> None:
        """Cleanup application resources."""
        try:
            app_logger.info("Cleaning up application resources...")
            
            # Cleanup services
            if self.server_manager:
                self.server_manager.cleanup()
            
            if self.config_manager:
                self.config_manager.cleanup()
            
            app_logger.info("Application cleanup completed")
            
        except Exception as e:
            app_logger.error(f"Error during cleanup: {e}")
    
    def _show_error(self, message: str) -> None:
        """Show error message to user.
        
        Args:
            message: Error message to display
        """
        try:
            if self.root:
                messagebox.showerror("Error", message, parent=self.root)
            else:
                # Fallback for errors before GUI is created
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                messagebox.showerror("Error", message)
                root.destroy()
        except Exception:
            # Last resort - print to console
            print(f"ERROR: {message}")


def main() -> int:
    """Main function.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Setup logging
        app_logger.info("=" * 50)
        app_logger.info("DevServer Manager Application Starting")
        app_logger.info("=" * 50)
        
        # Create and run application
        app = DevServerManagerApp()
        app.run()
        
        app_logger.info("Application exited normally")
        return 0
        
    except Exception as e:
        app_logger.error(f"Fatal error in main: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())