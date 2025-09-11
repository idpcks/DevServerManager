"""File System Utilities

This module provides file system utility functions.
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class FileUtils:
    """File system utility functions."""
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists, create if it doesn't.
        
        Args:
            path: Directory path
            
        Returns:
            True if directory exists or was created successfully
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def safe_read_json(file_path: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Safely read JSON file with fallback to default.
        
        Args:
            file_path: Path to JSON file
            default: Default value if file doesn't exist or is invalid
            
        Returns:
            JSON data or default value
        """
        if default is None:
            default = {}
            
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        
        return default
    
    @staticmethod
    def safe_write_json(file_path: str, data: Dict[str, Any], 
                       create_backup: bool = True) -> bool:
        """Safely write JSON file with optional backup.
        
        Args:
            file_path: Path to JSON file
            data: Data to write
            create_backup: Whether to create backup before writing
            
        Returns:
            True if write was successful
        """
        try:
            # Create directory if it doesn't exist
            FileUtils.ensure_directory(os.path.dirname(file_path))
            
            # Create backup if requested and file exists
            if create_backup and os.path.exists(file_path):
                FileUtils.create_backup(file_path)
            
            # Write JSON file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def create_backup(file_path: str, backup_dir: Optional[str] = None) -> Optional[str]:
        """Create backup of a file.
        
        Args:
            file_path: Path to file to backup
            backup_dir: Directory to store backup (default: same directory)
            
        Returns:
            Path to backup file if successful, None otherwise
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            # Determine backup directory
            if backup_dir is None:
                backup_dir = os.path.dirname(file_path)
            else:
                FileUtils.ensure_directory(backup_dir)
            
            # Create backup filename with timestamp
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{name}_backup_{timestamp}{ext}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Copy file to backup location
            shutil.copy2(file_path, backup_path)
            
            return backup_path
            
        except Exception:
            return None
    
    @staticmethod
    def cleanup_backups(directory: str, pattern: str = "*_backup_*", 
                       max_backups: int = 10) -> int:
        """Clean up old backup files.
        
        Args:
            directory: Directory to clean up
            pattern: File pattern to match
            max_backups: Maximum number of backups to keep
            
        Returns:
            Number of files deleted
        """
        try:
            if not os.path.exists(directory):
                return 0
            
            # Find backup files
            backup_files = []
            for file in os.listdir(directory):
                if "_backup_" in file:
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        backup_files.append(file_path)
            
            # Sort by modification time (newest first)
            backup_files.sort(key=os.path.getmtime, reverse=True)
            
            # Delete old backups
            deleted_count = 0
            for old_backup in backup_files[max_backups:]:
                try:
                    os.remove(old_backup)
                    deleted_count += 1
                except Exception:
                    pass
            
            return deleted_count
            
        except Exception:
            return 0
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes.
        
        Args:
            file_path: Path to file
            
        Returns:
            File size in bytes, -1 if file doesn't exist
        """
        try:
            if os.path.exists(file_path):
                return os.path.getsize(file_path)
        except Exception:
            pass
        return -1
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        if size_bytes < 0:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} PB"
    
    @staticmethod
    def is_valid_directory(path: str) -> bool:
        """Check if path is a valid directory.
        
        Args:
            path: Directory path to check
            
        Returns:
            True if path is a valid directory
        """
        try:
            return os.path.isdir(path) and os.access(path, os.R_OK)
        except Exception:
            return False
    
    @staticmethod
    def is_valid_file(path: str) -> bool:
        """Check if path is a valid file.
        
        Args:
            path: File path to check
            
        Returns:
            True if path is a valid file
        """
        try:
            return os.path.isfile(path) and os.access(path, os.R_OK)
        except Exception:
            return False
    
    @staticmethod
    def get_directory_size(directory: str) -> int:
        """Get total size of directory and all its contents.
        
        Args:
            directory: Directory path
            
        Returns:
            Total size in bytes
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(file_path)
                    except Exception:
                        pass
        except Exception:
            pass
        
        return total_size
    
    @staticmethod
    def find_files(directory: str, pattern: str = "*", 
                  recursive: bool = True) -> List[str]:
        """Find files matching pattern in directory.
        
        Args:
            directory: Directory to search
            pattern: File pattern to match
            recursive: Whether to search recursively
            
        Returns:
            List of matching file paths
        """
        try:
            path = Path(directory)
            if recursive:
                return [str(p) for p in path.rglob(pattern) if p.is_file()]
            else:
                return [str(p) for p in path.glob(pattern) if p.is_file()]
        except Exception:
            return []
    
    @staticmethod
    def copy_file(src: str, dst: str, create_dirs: bool = True) -> bool:
        """Copy file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            create_dirs: Whether to create destination directories
            
        Returns:
            True if copy was successful
        """
        try:
            if create_dirs:
                FileUtils.ensure_directory(os.path.dirname(dst))
            
            shutil.copy2(src, dst)
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def move_file(src: str, dst: str, create_dirs: bool = True) -> bool:
        """Move file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            create_dirs: Whether to create destination directories
            
        Returns:
            True if move was successful
        """
        try:
            if create_dirs:
                FileUtils.ensure_directory(os.path.dirname(dst))
            
            shutil.move(src, dst)
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Safely delete a file.
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            True if deletion was successful
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_temp_file(prefix: str = "temp", suffix: str = ".tmp", 
                     directory: Optional[str] = None) -> str:
        """Get path to temporary file.
        
        Args:
            prefix: File prefix
            suffix: File suffix
            directory: Directory for temp file (default: system temp)
            
        Returns:
            Path to temporary file
        """
        import tempfile
        
        if directory is None:
            directory = tempfile.gettempdir()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{prefix}_{timestamp}{suffix}"
        
        return os.path.join(directory, filename)