"""Download Manager Service

This module provides functionality to download update files
with progress tracking and integrity verification.
"""

import requests
import os
import hashlib
import threading
import time
import zipfile
import shutil
from pathlib import Path
from typing import Callable, Optional, Dict, Any
from urllib.parse import urlparse

from utils.logger import app_logger


class DownloadProgress:
    """Class to hold download progress information."""
    
    def __init__(self, downloaded: int = 0, total: int = 0, percentage: float = 0.0, 
                 speed: float = 0.0, eta: int = 0):
        self.downloaded = downloaded
        self.total = total
        self.percentage = percentage
        self.speed = speed  # bytes per second
        self.eta = eta  # estimated time remaining in seconds


class DownloadManager:
    """Service for downloading update files with progress tracking."""
    
    def __init__(self):
        """Initialize download manager."""
        self.download_dir = Path(__file__).parent.parent.parent / "downloads"
        self.download_dir.mkdir(exist_ok=True)
        self.is_downloading = False
        self.cancel_download = False
        
        app_logger.info(f"DownloadManager initialized. Download dir: {self.download_dir}")
    
    def download_file(self, url: str, filename: str = None, 
                     progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
                     completion_callback: Optional[Callable[[str, bool], None]] = None) -> None:
        """Download file with progress tracking.
        
        Args:
            url: URL to download from
            filename: Local filename (auto-generated if None)
            progress_callback: Function to call with progress updates
            completion_callback: Function to call when download completes (filepath, success)
        """
        if self.is_downloading:
            app_logger.warning("Download already in progress")
            if completion_callback:
                completion_callback("", False)
            return
        
        def download_thread():
            nonlocal filename  # Allow access to filename in nested function
            try:
                self.is_downloading = True
                self.cancel_download = False
                
                # Generate filename if not provided
                if not filename:
                    parsed_url = urlparse(url)
                    filename = os.path.basename(parsed_url.path)
                    if not filename:
                        filename = f"update_{int(time.time())}.exe"
                
                filepath = self.download_dir / filename
                
                app_logger.info(f"Starting download: {url} -> {filepath}")
                
                # Start download with streaming
                response = requests.get(url, stream=True, timeout=30)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                start_time = time.time()
                last_update = start_time
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if self.cancel_download:
                            app_logger.info("Download cancelled by user")
                            f.close()
                            if filepath.exists():
                                filepath.unlink()
                            if completion_callback:
                                completion_callback("", False)
                            return
                        
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Update progress every 0.5 seconds
                            current_time = time.time()
                            if current_time - last_update >= 0.5:
                                elapsed = current_time - start_time
                                speed = downloaded / elapsed if elapsed > 0 else 0
                                percentage = (downloaded / total_size * 100) if total_size > 0 else 0
                                eta = int((total_size - downloaded) / speed) if speed > 0 else 0
                                
                                progress = DownloadProgress(
                                    downloaded=downloaded,
                                    total=total_size,
                                    percentage=percentage,
                                    speed=speed,
                                    eta=eta
                                )
                                
                                if progress_callback:
                                    progress_callback(progress)
                                
                                last_update = current_time
                
                # Final progress update
                if progress_callback:
                    final_progress = DownloadProgress(
                        downloaded=downloaded,
                        total=total_size,
                        percentage=100.0,
                        speed=0,
                        eta=0
                    )
                    progress_callback(final_progress)
                
                app_logger.info(f"Download completed: {filepath}")
                
                # If it's a ZIP file, extract the executable
                final_filepath = str(filepath)
                if str(filepath).endswith('.zip'):
                    exe_path = self._extract_executable_from_zip(str(filepath))
                    if exe_path:
                        final_filepath = exe_path
                        app_logger.info(f"Extracted executable: {exe_path}")
                    else:
                        app_logger.error("Failed to extract executable from ZIP")
                        if completion_callback:
                            completion_callback("", False)
                        return
                
                if completion_callback:
                    completion_callback(final_filepath, True)
                    
            except Exception as e:
                app_logger.error(f"Download failed: {e}")
                if completion_callback:
                    completion_callback("", False)
            finally:
                self.is_downloading = False
        
        # Start download in separate thread
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def verify_file_integrity(self, filepath: str, expected_checksum: str = None) -> bool:
        """Verify file integrity using checksum.
        
        Args:
            filepath: Path to file to verify
            expected_checksum: Expected SHA256 checksum (optional)
            
        Returns:
            True if file is valid, False otherwise
        """
        try:
            if not os.path.exists(filepath):
                return False
            
            # Calculate SHA256 checksum
            sha256_hash = hashlib.sha256()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            
            actual_checksum = sha256_hash.hexdigest()
            
            if expected_checksum:
                is_valid = actual_checksum.lower() == expected_checksum.lower()
                app_logger.info(f"File integrity check: {'PASSED' if is_valid else 'FAILED'}")
                return is_valid
            else:
                app_logger.info(f"File checksum: {actual_checksum}")
                return True
                
        except Exception as e:
            app_logger.error(f"Error verifying file integrity: {e}")
            return False
    
    def get_file_size(self, url: str) -> int:
        """Get file size from URL without downloading.
        
        Args:
            url: URL to check
            
        Returns:
            File size in bytes, 0 if unknown
        """
        try:
            response = requests.head(url, timeout=10)
            response.raise_for_status()
            return int(response.headers.get('content-length', 0))
        except Exception as e:
            app_logger.error(f"Error getting file size: {e}")
            return 0
    
    def _extract_executable_from_zip(self, zip_filepath: str) -> Optional[str]:
        """Extract executable from ZIP file.
        
        Args:
            zip_filepath: Path to ZIP file
            
        Returns:
            Path to extracted executable or None if failed
        """
        try:
            extract_dir = Path(zip_filepath).parent / "extracted"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                # List all files in ZIP
                file_list = zip_ref.namelist()
                app_logger.info(f"ZIP contains files: {file_list}")
                
                # Find executable file
                exe_file = None
                for file_name in file_list:
                    if file_name.endswith('.exe') and not file_name.startswith('__MACOSX'):
                        exe_file = file_name
                        break
                
                if not exe_file:
                    app_logger.error("No executable file found in ZIP")
                    return None
                
                # Extract the executable
                zip_ref.extract(exe_file, extract_dir)
                extracted_path = extract_dir / exe_file
                
                # Move to downloads directory with simpler name
                final_path = self.download_dir / "DevServerManager.exe"
                if final_path.exists():
                    final_path.unlink()  # Remove old file
                
                extracted_path.rename(final_path)
                
                # Clean up
                if extract_dir.exists():
                    shutil.rmtree(extract_dir)
                
                app_logger.info(f"Executable extracted to: {final_path}")
                return str(final_path)
                
        except Exception as e:
            app_logger.error(f"Error extracting executable from ZIP: {e}")
            return None

    def cancel_download(self) -> None:
        """Cancel current download."""
        if self.is_downloading:
            self.cancel_download = True
            app_logger.info("Download cancellation requested")
    
    def cleanup_downloads(self) -> None:
        """Clean up old download files."""
        try:
            if self.download_dir.exists():
                for file in self.download_dir.iterdir():
                    if file.is_file():
                        # Delete files older than 7 days
                        if time.time() - file.stat().st_mtime > 7 * 24 * 3600:
                            file.unlink()
                            app_logger.info(f"Cleaned up old download: {file}")
        except Exception as e:
            app_logger.error(f"Error cleaning up downloads: {e}")
    
    def get_download_info(self, url: str) -> Dict[str, Any]:
        """Get download information without downloading.
        
        Args:
            url: URL to check
            
        Returns:
            Dictionary with download info
        """
        try:
            response = requests.head(url, timeout=10)
            response.raise_for_status()
            
            return {
                'size': int(response.headers.get('content-length', 0)),
                'content_type': response.headers.get('content-type', ''),
                'last_modified': response.headers.get('last-modified', ''),
                'etag': response.headers.get('etag', ''),
                'available': True
            }
        except Exception as e:
            app_logger.error(f"Error getting download info: {e}")
            return {
                'size': 0,
                'content_type': '',
                'last_modified': '',
                'etag': '',
                'available': False
            }
