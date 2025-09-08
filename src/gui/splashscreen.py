import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import sys
import os
from pathlib import Path

from utils.theme_manager import theme_manager

class SplashScreen:
    def __init__(self, main_app_callback):
        self.main_app_callback = main_app_callback
        self.splash = tk.Tk()
        self.splash.title("Server Manager")
        
        # Get current theme colors
        self.colors = theme_manager.get_current_colors()
        
        # Make splash responsive based on screen size
        self.setup_responsive_size()
        self.splash.configure(bg=self.colors['bg'])
        
        # Center the splash screen
        self.center_window()
        
        # Remove window decorations for a cleaner look
        self.splash.overrideredirect(True)
        
        # Create border frame for modern look
        self.border_frame = tk.Frame(self.splash, bg=self.colors['frame_bg'], relief='raised', bd=2)
        self.border_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create main frame with gradient-like effect
        self.main_frame = tk.Frame(self.border_frame, bg=self.colors['bg'])
        self.main_frame.pack(expand=True, fill='both', padx=15, pady=15)
        
        # Setup UI elements
        self.setup_logo()
        self.setup_loading_elements()
        
        # Start loading animation
        self.start_loading()
        
    def setup_responsive_size(self):
        """Setup responsive window size based on screen resolution"""
        # Get screen dimensions
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        # Calculate responsive dimensions (percentage of screen size)
        # Minimum size: 400x300, Maximum size: 600x450
        base_width = max(400, min(600, int(screen_width * 0.25)))
        base_height = max(300, min(450, int(screen_height * 0.3)))
        
        # Set geometry and make it non-resizable for clean look
        self.splash.geometry(f"{base_width}x{base_height}")
        self.splash.resizable(False, False)
        
        # Store dimensions for responsive elements
        self.splash_width = base_width
        self.splash_height = base_height
        
    def center_window(self):
        """Center the splash screen on the screen"""
        self.splash.update_idletasks()
        width = self.splash.winfo_width()
        height = self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() // 2) - (width // 2)
        y = (self.splash.winfo_screenheight() // 2) - (height // 2)
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_logo(self):
        """Setup logo display"""
        try:
            # Load and resize logo responsively
            logo_image = Image.open("logo.jpg")
            # Scale logo size based on window size (15-25% of window width)
            logo_size = max(80, min(150, int(self.splash_width * 0.2)))
            logo_image = logo_image.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Create logo label
            self.logo_label = tk.Label(
                self.main_frame,
                image=self.logo_photo,
                bg=self.colors['bg']
            )
            self.logo_label.pack(pady=(30, 20))
            
        except Exception as e:
            # Fallback if logo.jpg not found
            self.logo_label = tk.Label(
                self.main_frame,
                text="SERVER\nMANAGER",
                font=('Arial', 20, 'bold'),
                fg=self.colors['fg'],
                bg=self.colors['bg']
            )
            self.logo_label.pack(pady=(30, 20))
            
    def setup_loading_elements(self):
        """Setup loading progress bar and text"""
        # App title
        self.title_label = tk.Label(
            self.main_frame,
            text="Server Manager",
            font=('Arial', 16, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.title_label.pack(pady=(0, 20))
        
        # Progress bar (responsive width)
        self.progress_var = tk.DoubleVar()
        # Scale progress bar length based on window width (60-80% of window width)
        progress_length = max(250, min(500, int(self.splash_width * 0.7)))
        self.progress_bar = ttk.Progressbar(
            self.main_frame,
            variable=self.progress_var,
            maximum=100,
            length=progress_length,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(0, 15))
        
        # Loading text
        self.loading_label = tk.Label(
            self.main_frame,
            text="Loading...",
            font=('Arial', 10),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.loading_label.pack()
        
        # Version info
        self.version_label = tk.Label(
            self.main_frame,
            text="v1.0.0",
            font=('Arial', 8),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.version_label.pack(side='bottom', pady=(20, 0))
        
    def start_loading(self):
        """Start the loading animation in a separate thread"""
        loading_thread = threading.Thread(target=self.loading_animation, daemon=True)
        loading_thread.start()
        
    def loading_animation(self):
        """Animate the loading process"""
        self.loading_steps = [
            ("Initializing...", 20),
            ("Loading components...", 40),
            ("Setting up interface...", 60),
            ("Preparing server manager...", 80),
            ("Almost ready...", 95),
            ("Ready!", 100)
        ]
        
        self.current_step = 0
        self.animate_step()
        
    def animate_step(self):
        """Animate individual loading step"""
        if self.current_step < len(self.loading_steps):
            text, target_progress = self.loading_steps[self.current_step]
            
            # Update loading text with smooth transition
            self.loading_label.config(text=text)
            
            # Animate progress bar smoothly
            current_progress = self.progress_var.get()
            self.animate_progress(current_progress, target_progress)
            
        else:
            # All steps completed, wait and close
            self.splash.after(800, self.close_splash)
            
    def animate_progress(self, start_progress, target_progress, step=0):
        """Smoothly animate progress bar"""
        steps = 25
        if step <= steps:
            # Easing function for smooth animation
            progress = start_progress + (target_progress - start_progress) * (step / steps)
            self.progress_var.set(progress)
            
            if step < steps:
                self.splash.after(30, lambda: self.animate_progress(start_progress, target_progress, step + 1))
            else:
                # Move to next step after delay
                self.current_step += 1
                self.splash.after(400, self.animate_step)
        
    def close_splash(self):
        """Close splash screen with fade effect and start main app"""
        self.fade_out(100)
        
    def fade_out(self, alpha):
        """Fade out animation using after() method"""
        if alpha > 0:
            self.splash.attributes('-alpha', alpha / 100.0)
            self.splash.after(20, lambda: self.fade_out(alpha - 5))
        else:
            self.splash.destroy()
            # Start main application
            if self.main_app_callback:
                self.main_app_callback()
            
    def show(self):
        """Show the splash screen"""
        # Start with transparent window
        self.splash.attributes('-alpha', 0.0)
        self.splash.deiconify()
        
        # Start fade in animation
        self.fade_in(0)
        
        self.splash.mainloop()
        
    def fade_in(self, alpha):
        """Fade in animation using after() method"""
        if alpha <= 100:
            self.splash.attributes('-alpha', alpha / 100.0)
            if alpha < 100:
                self.splash.after(20, lambda: self.fade_in(alpha + 5))

def show_splash(main_app_callback):
    """Convenience function to show splash screen"""
    try:
        splash = SplashScreen(main_app_callback)
        splash.show()
    except Exception as e:
        print(f"Error showing splash screen: {e}")
        # Fallback - call main app directly if splash fails
        if main_app_callback:
            main_app_callback()