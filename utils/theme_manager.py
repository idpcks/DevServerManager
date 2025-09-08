import tkinter as tk
import json
import os
import winreg
from typing import Dict, Any, Callable

class ThemeManager:
    """Manages application themes (dark, light, system)"""
    
    def __init__(self):
        self.current_theme = "system"
        self.theme_callbacks = []
        self.config_file = "theme_config.json"
        
        # Define color schemes
        self.themes = {
            "dark": {
                "bg": "#2c3e50",
                "fg": "#ecf0f1",
                "select_bg": "#34495e",
                "select_fg": "#ffffff",
                "button_bg": "#3498db",
                "button_fg": "#ffffff",
                "button_active_bg": "#2980b9",
                "entry_bg": "#34495e",
                "entry_fg": "#ecf0f1",
                "frame_bg": "#2c3e50",
                "text_bg": "#34495e",
                "text_fg": "#ecf0f1",
                "scrollbar_bg": "#34495e",
                "scrollbar_fg": "#7f8c8d",
                "menu_bg": "#34495e",
                "menu_fg": "#ecf0f1",
                "border": "#7f8c8d",
                "success": "#27ae60",
                "warning": "#f39c12",
                "error": "#e74c3c",
                "info": "#3498db"
            },
            "light": {
                "bg": "#ffffff",
                "fg": "#2c3e50",
                "select_bg": "#e8f4fd",
                "select_fg": "#2c3e50",
                "button_bg": "#3498db",
                "button_fg": "#ffffff",
                "button_active_bg": "#2980b9",
                "entry_bg": "#ffffff",
                "entry_fg": "#2c3e50",
                "frame_bg": "#f8f9fa",
                "text_bg": "#ffffff",
                "text_fg": "#2c3e50",
                "scrollbar_bg": "#e9ecef",
                "scrollbar_fg": "#6c757d",
                "menu_bg": "#ffffff",
                "menu_fg": "#2c3e50",
                "border": "#dee2e6",
                "success": "#28a745",
                "warning": "#ffc107",
                "error": "#dc3545",
                "info": "#17a2b8"
            }
        }
        
        # Load saved theme preference
        self.load_theme_config()
    
    def detect_system_theme(self) -> str:
        """Detect Windows system theme"""
        try:
            # Check Windows registry for system theme
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            
            # AppsUseLightTheme: 0 = dark, 1 = light
            apps_use_light_theme, _ = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
            winreg.CloseKey(registry_key)
            
            return "light" if apps_use_light_theme else "dark"
            
        except Exception:
            # Default to light theme if detection fails
            return "light"
    
    def get_current_colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        if self.current_theme == "system":
            system_theme = self.detect_system_theme()
            return self.themes[system_theme]
        else:
            return self.themes[self.current_theme]
    
    def set_theme(self, theme: str):
        """Set application theme"""
        if theme in ["dark", "light", "system"]:
            self.current_theme = theme
            self.save_theme_config()
            self.notify_theme_change()
    
    def get_theme(self) -> str:
        """Get current theme name"""
        return self.current_theme
    
    def register_callback(self, callback: Callable):
        """Register callback for theme changes"""
        self.theme_callbacks.append(callback)
    
    def notify_theme_change(self):
        """Notify all registered callbacks about theme change"""
        colors = self.get_current_colors()
        for callback in self.theme_callbacks:
            try:
                callback(colors)
            except Exception as e:
                print(f"Error in theme callback: {e}")
    
    def apply_theme_to_widget(self, widget, widget_type="default"):
        """Apply current theme to a specific widget"""
        colors = self.get_current_colors()
        
        try:
            if widget_type == "button":
                widget.configure(
                    bg=colors["button_bg"],
                    fg=colors["button_fg"],
                    activebackground=colors["button_active_bg"],
                    activeforeground=colors["button_fg"]
                )
            elif widget_type == "entry":
                widget.configure(
                    bg=colors["entry_bg"],
                    fg=colors["entry_fg"],
                    insertbackground=colors["entry_fg"]
                )
            elif widget_type == "text":
                widget.configure(
                    bg=colors["text_bg"],
                    fg=colors["text_fg"],
                    insertbackground=colors["text_fg"],
                    selectbackground=colors["select_bg"],
                    selectforeground=colors["select_fg"]
                )
            elif widget_type == "frame":
                widget.configure(bg=colors["frame_bg"])
            elif widget_type == "label":
                widget.configure(
                    bg=colors["bg"],
                    fg=colors["fg"]
                )
            elif widget_type == "listbox":
                widget.configure(
                    bg=colors["text_bg"],
                    fg=colors["text_fg"],
                    selectbackground=colors["select_bg"],
                    selectforeground=colors["select_fg"]
                )
            elif widget_type == "scrollbar":
                widget.configure(
                    bg=colors["scrollbar_bg"],
                    troughcolor=colors["scrollbar_bg"],
                    activebackground=colors["scrollbar_fg"]
                )
            else:  # default
                widget.configure(
                    bg=colors["bg"],
                    fg=colors["fg"]
                )
        except Exception as e:
            print(f"Error applying theme to widget: {e}")
    
    def save_theme_config(self):
        """Save theme configuration to file"""
        try:
            config = {
                "theme": self.current_theme
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving theme config: {e}")
    
    def load_theme_config(self):
        """Load theme configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.current_theme = config.get("theme", "system")
        except Exception as e:
            print(f"Error loading theme config: {e}")
            self.current_theme = "system"
    
    def load_theme(self):
        """Load and apply theme configuration"""
        self.load_theme_config()
        self.notify_theme_change()

# Global theme manager instance
theme_manager = ThemeManager()