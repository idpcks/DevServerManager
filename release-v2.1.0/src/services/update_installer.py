"""Update Installer Service

This module provides functionality to install application updates
with backup and rollback capabilities.
"""

import os
import shutil
import subprocess
import sys
import time
import threading
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import psutil

from utils.logger import app_logger


class UpdateInstaller:
    """Service for installing application updates."""
    
    def __init__(self):
        """Initialize update installer."""
        self.app_dir = Path(sys.executable).parent
        self.backup_dir = self.app_dir / "backup"
        self.temp_dir = self.app_dir / "temp"
        self.is_installing = False
        
        # Create necessary directories
        self.backup_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        
        app_logger.info(f"UpdateInstaller initialized. App dir: {self.app_dir}")
    
    def install_update(self, new_exe_path: str, 
                      progress_callback: Optional[Callable[[str, int], None]] = None,
                      completion_callback: Optional[Callable[[bool, str], None]] = None) -> None:
        """Install update by replacing executable.
        
        Args:
            new_exe_path: Path to new executable file
            progress_callback: Function to call with progress updates (message, percentage)
            completion_callback: Function to call when installation completes (success, message)
        """
        if self.is_installing:
            app_logger.warning("Installation already in progress")
            if completion_callback:
                completion_callback(False, "Installation already in progress")
            return
        
        def install_thread():
            try:
                self.is_installing = True
                
                if progress_callback:
                    progress_callback("Preparing installation...", 0)
                
                # Validate new executable
                if not os.path.exists(new_exe_path):
                    raise FileNotFoundError(f"New executable not found: {new_exe_path}")
                
                # Get current executable path
                current_exe = sys.executable
                current_exe_path = Path(current_exe)
                
                if progress_callback:
                    progress_callback("Creating backup...", 10)
                
                # Create backup of current executable
                backup_path = self.backup_dir / f"backup_{int(time.time())}.exe"
                shutil.copy2(current_exe_path, backup_path)
                app_logger.info(f"Backup created: {backup_path}")
                
                if progress_callback:
                    progress_callback("Stopping application...", 20)
                
                # Schedule application restart
                self._schedule_restart(new_exe_path, current_exe_path, backup_path)
                
                if progress_callback:
                    progress_callback("Installation completed!", 100)
                
                app_logger.info("Update installation completed successfully")
                
                if completion_callback:
                    completion_callback(True, "Update installed successfully. Application will restart.")
                
            except Exception as e:
                app_logger.error(f"Installation failed: {e}")
                if completion_callback:
                    completion_callback(False, f"Installation failed: {str(e)}")
            finally:
                self.is_installing = False
        
        # Start installation in separate thread
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()
    
    def _schedule_restart(self, new_exe_path: str, current_exe_path: Path, backup_path: Path) -> None:
        """Schedule application restart with new executable.
        
        Args:
            new_exe_path: Path to new executable
            current_exe_path: Path to current executable
            backup_path: Path to backup executable
        """
        try:
            # Create restart script
            restart_script = self._create_restart_script(new_exe_path, current_exe_path, backup_path)
            
            # Schedule restart after 3 seconds
            def delayed_restart():
                time.sleep(3)
                try:
                    # Start restart script
                    subprocess.Popen([restart_script], shell=True)
                    # Exit current application
                    sys.exit(0)
                except Exception as e:
                    app_logger.error(f"Error during restart: {e}")
            
            restart_thread = threading.Thread(target=delayed_restart, daemon=True)
            restart_thread.start()
            
        except Exception as e:
            app_logger.error(f"Error scheduling restart: {e}")
    
    def _create_restart_script(self, new_exe_path: str, current_exe_path: Path, backup_path: Path) -> str:
        """Create restart script for Windows.
        
        Args:
            new_exe_path: Path to new executable
            current_exe_path: Path to current executable
            backup_path: Path to backup executable
            
        Returns:
            Path to restart script
        """
        script_path = self.temp_dir / "restart_update.bat"
        
        script_content = f"""@echo off
echo Updating DevServer Manager...

REM Wait for application to close
timeout /t 2 /nobreak >nul

REM Replace executable
copy "{new_exe_path}" "{current_exe_path}" /Y
if errorlevel 1 (
    echo Error: Failed to replace executable
    echo Restoring backup...
    copy "{backup_path}" "{current_exe_path}" /Y
    goto :error
)

REM Start updated application
start "" "{current_exe_path}"

REM Clean up
del "{new_exe_path}"
del "%~f0"

echo Update completed successfully!
goto :end

:error
echo Update failed! Backup restored.
pause

:end
"""
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        return str(script_path)
    
    def create_launcher_script(self) -> str:
        """Create launcher script for easier updates.
        
        Returns:
            Path to launcher script
        """
        launcher_path = self.app_dir / "DevServerManager_Launcher.bat"
        
        launcher_content = f"""@echo off
echo Starting DevServer Manager...

REM Check if main executable exists
if not exist "{sys.executable}" (
    echo Error: Main executable not found!
    pause
    exit /b 1
)

REM Start application
start "" "{sys.executable}"

REM Exit launcher
exit
"""
        
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        return str(launcher_path)
    
    def rollback_update(self, backup_path: str) -> bool:
        """Rollback to previous version.
        
        Args:
            backup_path: Path to backup executable
            
        Returns:
            True if rollback successful, False otherwise
        """
        try:
            if not os.path.exists(backup_path):
                app_logger.error(f"Backup not found: {backup_path}")
                return False
            
            current_exe = sys.executable
            current_exe_path = Path(current_exe)
            
            # Replace current executable with backup
            shutil.copy2(backup_path, current_exe_path)
            
            app_logger.info("Rollback completed successfully")
            return True
            
        except Exception as e:
            app_logger.error(f"Rollback failed: {e}")
            return False
    
    def get_available_backups(self) -> list:
        """Get list of available backups.
        
        Returns:
            List of backup file paths
        """
        try:
            backups = []
            if self.backup_dir.exists():
                for file in self.backup_dir.iterdir():
                    if file.is_file() and file.suffix == '.exe':
                        backups.append(str(file))
            
            # Sort by modification time (newest first)
            backups.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            return backups
            
        except Exception as e:
            app_logger.error(f"Error getting backups: {e}")
            return []
    
    def cleanup_old_backups(self, keep_count: int = 3) -> None:
        """Clean up old backup files.
        
        Args:
            keep_count: Number of recent backups to keep
        """
        try:
            backups = self.get_available_backups()
            
            if len(backups) > keep_count:
                for backup in backups[keep_count:]:
                    os.remove(backup)
                    app_logger.info(f"Cleaned up old backup: {backup}")
                    
        except Exception as e:
            app_logger.error(f"Error cleaning up backups: {e}")
    
    def verify_installation(self, exe_path: str) -> bool:
        """Verify that installation is valid.
        
        Args:
            exe_path: Path to executable to verify
            
        Returns:
            True if installation is valid, False otherwise
        """
        try:
            if not os.path.exists(exe_path):
                return False
            
            # Try to get version info
            try:
                result = subprocess.run([exe_path, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            except:
                # If version check fails, just check if file is executable
                return os.access(exe_path, os.X_OK)
                
        except Exception as e:
            app_logger.error(f"Error verifying installation: {e}")
            return False
    
    def get_installation_info(self) -> Dict[str, Any]:
        """Get current installation information.
        
        Returns:
            Dictionary with installation info
        """
        try:
            current_exe = sys.executable
            current_exe_path = Path(current_exe)
            
            return {
                'executable_path': str(current_exe_path),
                'executable_size': current_exe_path.stat().st_size if current_exe_path.exists() else 0,
                'executable_modified': current_exe_path.stat().st_mtime if current_exe_path.exists() else 0,
                'backup_count': len(self.get_available_backups()),
                'is_valid': self.verify_installation(current_exe)
            }
            
        except Exception as e:
            app_logger.error(f"Error getting installation info: {e}")
            return {
                'executable_path': '',
                'executable_size': 0,
                'executable_modified': 0,
                'backup_count': 0,
                'is_valid': False
            }
