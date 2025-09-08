"""Logging Utility

This module provides logging functionality for the application.
"""

import logging
import os
from datetime import datetime
from typing import Optional


class AppLogger:
    """Application logger with file and console output."""
    
    def __init__(self, name: str = "ServerManager", log_dir: str = "logs"):
        """Initialize application logger.
        
        Args:
            name: Logger name
            log_dir: Directory for log files
        """
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up logger
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Set up logger with file and console handlers."""
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Set logger level
        self.logger.setLevel(logging.DEBUG)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # File handler
        log_file = os.path.join(self.log_dir, f"{self.name.lower()}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str) -> None:
        """Log debug message.
        
        Args:
            message: Debug message
        """
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log info message.
        
        Args:
            message: Info message
        """
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message.
        
        Args:
            message: Warning message
        """
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False) -> None:
        """Log error message.
        
        Args:
            message: Error message
            exc_info: Include exception info
        """
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False) -> None:
        """Log critical message.
        
        Args:
            message: Critical message
            exc_info: Include exception info
        """
        self.logger.critical(message, exc_info=exc_info)
    
    def log_server_action(self, server_name: str, action: str, status: str, 
                         details: Optional[str] = None) -> None:
        """Log server-related actions.
        
        Args:
            server_name: Name of the server
            action: Action performed (start, stop, add, remove, etc.)
            status: Status of the action (success, error, warning)
            details: Additional details
        """
        message = f"Server '{server_name}' - {action.upper()}: {status.upper()}"
        if details:
            message += f" - {details}"
        
        if status.lower() == 'error':
            self.error(message)
        elif status.lower() == 'warning':
            self.warning(message)
        else:
            self.info(message)
    
    def log_config_action(self, config_type: str, action: str, status: str,
                         details: Optional[str] = None) -> None:
        """Log configuration-related actions.
        
        Args:
            config_type: Type of configuration (server, theme)
            action: Action performed (load, save, backup, restore)
            status: Status of the action (success, error, warning)
            details: Additional details
        """
        message = f"Config '{config_type}' - {action.upper()}: {status.upper()}"
        if details:
            message += f" - {details}"
        
        if status.lower() == 'error':
            self.error(message)
        elif status.lower() == 'warning':
            self.warning(message)
        else:
            self.info(message)
    
    def log_app_event(self, event: str, details: Optional[str] = None) -> None:
        """Log application events.
        
        Args:
            event: Event description
            details: Additional details
        """
        message = f"App Event: {event}"
        if details:
            message += f" - {details}"
        
        self.info(message)
    
    def get_log_file_path(self) -> str:
        """Get path to current log file.
        
        Returns:
            Path to log file
        """
        return os.path.join(self.log_dir, f"{self.name.lower()}.log")
    
    def clear_logs(self) -> bool:
        """Clear log file contents.
        
        Returns:
            True if cleared successfully, False otherwise
        """
        try:
            log_file = self.get_log_file_path()
            if os.path.exists(log_file):
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write(f"Log cleared at {datetime.now()}\n")
            return True
        except Exception as e:
            self.error(f"Failed to clear logs: {e}")
            return False
    
    def rotate_logs(self, max_files: int = 5) -> bool:
        """Rotate log files to prevent them from getting too large.
        
        Args:
            max_files: Maximum number of log files to keep
            
        Returns:
            True if rotation was successful, False otherwise
        """
        try:
            log_file = self.get_log_file_path()
            
            if not os.path.exists(log_file):
                return True
            
            # Check file size (rotate if > 10MB)
            if os.path.getsize(log_file) > 10 * 1024 * 1024:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                rotated_file = f"{log_file}.{timestamp}"
                
                # Rename current log file
                os.rename(log_file, rotated_file)
                
                # Clean up old rotated files
                log_files = []
                for file in os.listdir(self.log_dir):
                    if file.startswith(f"{self.name.lower()}.log."):
                        log_files.append(os.path.join(self.log_dir, file))
                
                # Sort by modification time and remove oldest files
                log_files.sort(key=os.path.getmtime, reverse=True)
                for old_file in log_files[max_files-1:]:
                    os.remove(old_file)
                
                # Recreate logger to use new file
                self._setup_logger()
                self.info("Log file rotated")
            
            return True
            
        except Exception as e:
            self.error(f"Failed to rotate logs: {e}")
            return False


# Global logger instance
app_logger = AppLogger()