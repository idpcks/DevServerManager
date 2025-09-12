"""
Icon Manager - Centralized icon handling for the DevServer Manager application.

This module provides consistent icon loading and management across the application.
"""

import os
import sys
from pathlib import Path
from typing import Optional
try:
    from PIL import Image, ImageDraw, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    # Define dummy classes to avoid unbound variable errors
    class Image:
        @staticmethod
        def new(*args, **kwargs):
            return None
        @staticmethod
        def open(*args, **kwargs):
            return None
        class Resampling:
            LANCZOS = None
    
    class ImageDraw:
        @staticmethod
        def Draw(*args, **kwargs):
            return None
    
    class ImageTk:
        @staticmethod
        def PhotoImage(*args, **kwargs):
            return None

from .logger import app_logger


class IconManager:
    """Centralized icon management for the application."""
    
    def __init__(self):
        """Initialize the icon manager."""
        self.app_dir = Path(__file__).parent.parent
        self.assets_dir = self.app_dir / "assets"
        self._icon_paths = {
            'app_icon': self.assets_dir / "app_icon.ico",
            'app_icon_svg': self.assets_dir / "app_icon.svg", 
            'logo': self.assets_dir / "logo.jpg"
        }
    
    def get_app_icon_path(self) -> Optional[str]:
        """Get the path to the application icon.
        
        Returns:
            Path to the icon file if it exists, None otherwise
        """
        icon_path = self._icon_paths['app_icon']
        if icon_path.exists():
            app_logger.info(f"Application icon found: {icon_path}")
            return str(icon_path)
        
        app_logger.warning(f"Application icon not found at: {icon_path}")
        return None
    
    def set_window_icon(self, window) -> bool:
        """Set the icon for a tkinter window.
        
        Args:
            window: The tkinter window to set the icon for
            
        Returns:
            True if icon was set successfully, False otherwise
        """
        try:
            icon_path = self.get_app_icon_path()
            if icon_path and os.path.exists(icon_path):
                window.iconbitmap(icon_path)
                app_logger.info(f"Window icon set successfully: {icon_path}")
                return True
            else:
                app_logger.warning("No application icon available for window")
                return False
        except Exception as e:
            app_logger.error(f"Error setting window icon: {e}")
            return False
    
    def get_tray_icon_image(self, size: tuple = (64, 64)):
        """Get PIL Image for system tray icon.
        
        Args:
            size: Desired size of the icon (width, height)
            
        Returns:
            PIL Image object or None if not available
        """
        if not PIL_AVAILABLE:
            app_logger.warning("PIL not available for tray icon")
            return None
        
        try:
            # Try to load the main icon file first
            icon_path = self._icon_paths['app_icon']
            if icon_path.exists():
                image = Image.open(icon_path)
                # Resize if needed
                if image.size != size:
                    image = image.resize(size, Image.Resampling.LANCZOS)
                app_logger.info(f"Tray icon loaded from: {icon_path}")
                return image
            
            # Fallback to generated icon
            app_logger.info("Generating fallback tray icon")
            return self._generate_fallback_icon(size)
            
        except Exception as e:
            app_logger.error(f"Error loading tray icon: {e}")
            return self._generate_fallback_icon(size)
    
    def _generate_fallback_icon(self, size: tuple = (64, 64)):
        """Generate a fallback icon when the main icon is not available.
        
        Args:
            size: Size of the icon to generate
            
        Returns:
            PIL Image object
        """
        if not PIL_AVAILABLE:
            return None
        
        try:
            width, height = size
            image = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Create professional server icon
            # Main circle background
            margin = 2
            draw.ellipse([margin, margin, width-margin, height-margin], 
                        fill=(52, 152, 219), outline=(44, 62, 80), width=2)
            
            # Server rack representation
            rack_width = int(width * 0.5)
            rack_height = int(height * 0.45)
            rack_x = (width - rack_width) // 2
            rack_y = (height - rack_height) // 2
            
            # Server rack background
            draw.rectangle([rack_x, rack_y, rack_x + rack_width, rack_y + rack_height], 
                          fill=(236, 240, 241), outline=(52, 73, 94), width=1)
            
            # Server slots
            slot_height = rack_height // 4
            slot_margin = 2
            colors = [(39, 174, 96), (243, 156, 18), (231, 76, 60), (155, 89, 182)]
            
            for i, color in enumerate(colors):
                slot_y = rack_y + (i * slot_height) + slot_margin
                # Slot bar
                draw.rectangle([rack_x + slot_margin, slot_y, 
                              rack_x + rack_width - slot_margin - 6, slot_y + slot_height - slot_margin], 
                              fill=color)
                # Status LED
                led_x = rack_x + rack_width - 5
                led_y = slot_y + (slot_height // 2) - 2
                draw.ellipse([led_x, led_y, led_x + 4, led_y + 4], fill=color)
            
            app_logger.info("Fallback icon generated successfully")
            return image
            
        except Exception as e:
            app_logger.error(f"Error generating fallback icon: {e}")
            return None
    
    def get_logo_for_splash(self, size: tuple = (120, 120)):
        """Get logo image for splash screen.
        
        Args:
            size: Desired size of the logo
            
        Returns:
            PIL ImageTk.PhotoImage object or None if not available
        """
        if not PIL_AVAILABLE:
            return None
        
        try:
            logo_path = self._icon_paths['logo']
            if logo_path.exists():
                image = Image.open(logo_path)
                image = image.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
            else:
                app_logger.warning(f"Logo file not found: {logo_path}")
                return None
                
        except Exception as e:
            app_logger.error(f"Error loading logo for splash: {e}")
            return None


# Global icon manager instance
icon_manager = IconManager()