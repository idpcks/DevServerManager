"""Update Checker Service

This module provides functionality to check for application updates
from GitHub releases and notify users about available updates.
"""

import requests
import json
import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable
from pathlib import Path
import sys

from utils.logger import app_logger
from .env_manager import env_manager


class UpdateInfo:
    """Class to hold update information."""
    
    def __init__(self, version: str, download_url: str, release_notes: str, 
                 published_at: str, is_prerelease: bool = False):
        self.version = version
        self.download_url = download_url
        self.release_notes = release_notes
        self.published_at = published_at
        self.is_prerelease = is_prerelease
    
    def __str__(self):
        return f"UpdateInfo(version={self.version}, prerelease={self.is_prerelease})"


class UpdateCheckerService:
    """Service for checking application updates from GitHub."""
    
    def __init__(self):
        """Initialize the update checker service."""
        # Load environment variables
        env_manager.load_env()
        
        # GitHub repository information from environment
        self.GITHUB_OWNER = env_manager.get("GITHUB_OWNER", "idpcks")
        self.GITHUB_REPO = env_manager.get("GITHUB_REPO", "DevServerManager")
        self.GITHUB_API_URL = f"https://api.github.com/repos/{self.GITHUB_OWNER}/{self.GITHUB_REPO}/releases"
        
        # Update check settings from environment
        self.CHECK_INTERVAL_HOURS = env_manager.get_int("UPDATE_CHECK_INTERVAL_HOURS", 24)
        self.CACHE_DURATION_HOURS = env_manager.get_int("UPDATE_CACHE_DURATION_HOURS", 1)
        self.current_version = self._get_current_version()
        self.last_check_time = None
        self.cached_update_info = None
        self.update_callback = None
        self.auto_check_enabled = True
        self.check_thread = None
        self.running = False
        
        # Cache file for storing last check time
        cache_dir = env_manager.get("CONFIG_DIR", "config")
        self.cache_file = Path(__file__).parent.parent.parent / cache_dir / "update_cache.json"
        self._load_cache()
        
        app_logger.info(f"UpdateChecker initialized for version {self.current_version}")
    
    def _get_current_version(self) -> str:
        """Get current application version.
        
        Returns:
            Current version string
        """
        try:
            # Try to get version from setup.py or version file
            setup_file = Path(__file__).parent.parent.parent / "setup.py"
            if setup_file.exists():
                with open(setup_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Look for version in setup.py
                    for line in content.split('\n'):
                        if 'version' in line and '=' in line:
                            version = line.split('=')[1].strip().strip('"\'')
                            # Remove trailing comma and quotes
                            version = version.rstrip(',').strip().strip('"\'')
                            # Remove 'v' prefix if present
                            version = version.lstrip('v')
                            if version and version != 'None':
                                return version
            
            # Fallback to a default version
            return "1.0.1"
            
        except Exception as e:
            app_logger.warning(f"Could not determine current version: {e}")
            return "1.0.1"
    
    def _load_cache(self) -> None:
        """Load cached update information."""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    self.last_check_time = datetime.fromisoformat(cache_data.get('last_check', ''))
                    if cache_data.get('update_info'):
                        update_data = cache_data['update_info']
                        self.cached_update_info = UpdateInfo(
                            version=update_data['version'],
                            download_url=update_data['download_url'],
                            release_notes=update_data['release_notes'],
                            published_at=update_data['published_at'],
                            is_prerelease=update_data.get('is_prerelease', False)
                        )
        except Exception as e:
            app_logger.warning(f"Could not load update cache: {e}")
            self.last_check_time = None
            self.cached_update_info = None
    
    def _save_cache(self) -> None:
        """Save update information to cache."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_data = {
                'last_check': self.last_check_time.isoformat() if self.last_check_time else '',
                'update_info': {
                    'version': self.cached_update_info.version,
                    'download_url': self.cached_update_info.download_url,
                    'release_notes': self.cached_update_info.release_notes,
                    'published_at': self.cached_update_info.published_at,
                    'is_prerelease': self.cached_update_info.is_prerelease
                } if self.cached_update_info else None
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            app_logger.warning(f"Could not save update cache: {e}")
    
    def _is_cache_valid(self) -> bool:
        """Check if cached update information is still valid.
        
        Returns:
            True if cache is valid and not expired
        """
        if not self.last_check_time or not self.cached_update_info:
            return False
        
        cache_age = datetime.now() - self.last_check_time
        return cache_age < timedelta(hours=self.CACHE_DURATION_HOURS)
    
    def _should_check_for_updates(self) -> bool:
        """Check if it's time to check for updates.
        
        Returns:
            True if should check for updates
        """
        if not self.last_check_time:
            return True
        
        time_since_check = datetime.now() - self.last_check_time
        return time_since_check >= timedelta(hours=self.CHECK_INTERVAL_HOURS)
    
    def _parse_version(self, version_str: str) -> tuple:
        """Parse version string to tuple for comparison.
        
        Args:
            version_str: Version string (e.g., "1.2.3")
            
        Returns:
            Tuple of version numbers
        """
        try:
            # Remove 'v' prefix if present and clean string
            version_str = version_str.lstrip('v').strip().strip('"\'')
            parts = version_str.split('.')
            return tuple(int(part) for part in parts)
        except ValueError:
            return (0, 0, 0)
    
    def _is_newer_version(self, remote_version: str) -> bool:
        """Check if remote version is newer than current version.
        
        Args:
            remote_version: Remote version string
            
        Returns:
            True if remote version is newer
        """
        try:
            current_parts = self._parse_version(self.current_version)
            remote_parts = self._parse_version(remote_version)
            
            # Compare version tuples
            return remote_parts > current_parts
            
        except Exception as e:
            app_logger.warning(f"Error comparing versions: {e}")
            return False
    
    def check_for_updates(self, force: bool = False) -> Optional[UpdateInfo]:
        """Check for available updates.
        
        Args:
            force: Force check even if cache is valid
            
        Returns:
            UpdateInfo if update is available, None otherwise
        """
        try:
            app_logger.info("Checking for updates...")
            
            # Use cache if valid and not forcing
            if not force and self._is_cache_valid():
                app_logger.info("Using cached update information")
                return self.cached_update_info if self._is_newer_version(self.cached_update_info.version) else None
            
            # Make API request to GitHub
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': f'DevServerManager/{self.current_version}'
            }
            
            response = requests.get(self.GITHUB_API_URL, headers=headers, timeout=10)
            response.raise_for_status()
            
            releases = response.json()
            
            if not releases:
                app_logger.info("No releases found")
                return None
            
            # Get the latest release (first in the list)
            latest_release = releases[0]
            
            # Skip pre-releases unless current version is also pre-release
            if latest_release.get('prerelease', False) and not self.current_version.endswith('-beta'):
                # Look for the latest stable release
                for release in releases:
                    if not release.get('prerelease', False):
                        latest_release = release
                        break
            
            version = latest_release['tag_name']
            download_url = None
            release_notes = latest_release.get('body', '')
            published_at = latest_release['published_at']
            is_prerelease = latest_release.get('prerelease', False)
            
            # Find download URL - prioritize ZIP files with Windows in name
            for asset in latest_release.get('assets', []):
                if asset['name'].endswith('.zip') and 'Windows' in asset['name']:
                    download_url = asset['browser_download_url']
                    break
            
            if not download_url:
                # Fallback to any ZIP file
                for asset in latest_release.get('assets', []):
                    if asset['name'].endswith('.zip'):
                        download_url = asset['browser_download_url']
                        break
            
            if not download_url:
                # Final fallback to exe files
                for asset in latest_release.get('assets', []):
                    if asset['name'].endswith('.exe'):
                        download_url = asset['browser_download_url']
                        break
            
            # Create update info
            update_info = UpdateInfo(
                version=version,
                download_url=download_url or latest_release['html_url'],
                release_notes=release_notes,
                published_at=published_at,
                is_prerelease=is_prerelease
            )
            
            # Update cache
            self.last_check_time = datetime.now()
            self.cached_update_info = update_info
            self._save_cache()
            
            # Check if this is a newer version
            if self._is_newer_version(version):
                app_logger.info(f"Update available: {version}")
                return update_info
            else:
                app_logger.info(f"No update needed. Current: {self.current_version}, Latest: {version}")
                return None
                
        except requests.exceptions.RequestException as e:
            app_logger.error(f"Network error checking for updates: {e}")
            return None
        except Exception as e:
            app_logger.error(f"Error checking for updates: {e}")
            return None
    
    def check_for_updates_async(self, callback: Optional[Callable[[Optional[UpdateInfo]], None]] = None) -> None:
        """Check for updates asynchronously.
        
        Args:
            callback: Function to call with update result
        """
        if callback:
            self.update_callback = callback
        
        def check_thread():
            try:
                update_info = self.check_for_updates()
                if self.update_callback:
                    self.update_callback(update_info)
            except Exception as e:
                app_logger.error(f"Error in async update check: {e}")
                if self.update_callback:
                    self.update_callback(None)
        
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
    
    def start_auto_check(self) -> None:
        """Start automatic update checking in background."""
        if self.running:
            return
        
        self.running = True
        self.auto_check_enabled = True
        
        def auto_check_loop():
            while self.running and self.auto_check_enabled:
                try:
                    if self._should_check_for_updates():
                        app_logger.info("Auto-checking for updates...")
                        update_info = self.check_for_updates()
                        
                        if update_info and self.update_callback:
                            self.update_callback(update_info)
                    
                    # Sleep for 1 hour before next check
                    for _ in range(3600):  # 3600 seconds = 1 hour
                        if not self.running:
                            break
                        time.sleep(1)
                        
                except Exception as e:
                    app_logger.error(f"Error in auto-update check: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying
        
        self.check_thread = threading.Thread(target=auto_check_loop, daemon=True)
        self.check_thread.start()
        app_logger.info("Auto-update check started")
    
    def stop_auto_check(self) -> None:
        """Stop automatic update checking."""
        self.running = False
        self.auto_check_enabled = False
        app_logger.info("Auto-update check stopped")
    
    def set_update_callback(self, callback: Callable[[Optional[UpdateInfo]], None]) -> None:
        """Set callback function for update notifications.
        
        Args:
            callback: Function to call when update is found
        """
        self.update_callback = callback
    
    def get_current_version(self) -> str:
        """Get current application version.
        
        Returns:
            Current version string
        """
        return self.current_version
    
    def get_last_check_time(self) -> Optional[datetime]:
        """Get last update check time.
        
        Returns:
            Last check time or None
        """
        return self.last_check_time
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.stop_auto_check()
        app_logger.info("UpdateChecker cleanup completed")
