"""Main Window Component

This module contains the main window class for the DevServer Manager GUI.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
from datetime import datetime
from typing import Dict, Any, Optional, Callable
import os

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    app_logger.warning("pystray or PIL not available. System tray functionality disabled.")

from ..services.server_manager import ServerManagerService
from ..services.config_manager import ConfigManager
from .dialogs import ServerConfigDialog, TemplateWizardDialog
from utils.theme_manager import theme_manager
from utils.logger import app_logger


class MainWindow:
    """Main window for the DevServer Manager application."""
    
    def __init__(self, root: tk.Tk):
        """Initialize main window.
        
        Args:
            root: Root tkinter window
        """
        self.root = root
        self.server_manager = ServerManagerService()
        self.config_manager = ConfigManager()
        
        # Queue for thread communication
        self.log_queue = queue.Queue()
        self.log_processor_running = True
        
        # UI components
        self.server_frames = {}
        self.log_text = None
        self.command_entry = None
        self.theme_var = None
        self.theme_combo = None
        self.scrollable_frame = None
        
        # System tray components
        self.tray_icon = None
        self.is_minimized_to_tray = False
        
        # Initialize window
        self._setup_window()
        self._setup_styles()
        self._setup_ui()
        self._init_theme_manager()
        
        # Initialize system tray
        if TRAY_AVAILABLE:
            self._setup_system_tray()
        
        self._start_log_processor()
    
    def apply_theme(self, theme_name: str = None):
        """Apply theme to the main window.
        
        Args:
            theme_name: Name of theme to apply (optional)
        """
        try:
            if theme_name:
                theme_manager.set_theme(theme_name)
            
            # Apply theme to all widgets
            colors = theme_manager.get_current_colors()
            
            # Apply to root window
            self.root.configure(bg=colors["bg"])
            
            # Apply to other widgets as needed
            if hasattr(self, 'log_text') and self.log_text:
                theme_manager.apply_theme_to_widget(self.log_text, "text")
            
            print(f"Theme applied successfully")
        except Exception as e:
            print(f"Error applying theme: {e}")
        
        # Load configuration
        self._load_servers()
        
        # Bind events
        self.root.bind('<Configure>', self._on_window_resize)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Bind iconify event for minimize to tray
        if TRAY_AVAILABLE:
            self.root.bind('<Map>', self._on_window_map)
            self.root.bind('<Unmap>', self._on_window_unmap)
    
    def _setup_window(self) -> None:
        """Setup main window properties."""
        self.root.title("DevServer Manager")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.configure(bg='#2c3e50')
        
        # Set application icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'app_icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                app_logger.info(f"Application icon set: {icon_path}")
            else:
                app_logger.warning(f"Icon file not found: {icon_path}")
        except Exception as e:
            app_logger.error(f"Error setting application icon: {e}")
        
        # Center window on screen
        self._center_window()
        
        # Configure window resizing behavior
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def _center_window(self) -> None:
        """Center the window on the screen."""
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")
        except Exception as e:
            app_logger.error(f"Error centering window: {e}")
    
    def _setup_styles(self) -> None:
        """Setup custom styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Server.TLabel', 
                       background='#34495e', 
                       foreground='#ecf0f1', 
                       font=('Arial', 10))
        
        style.configure('Success.TButton', 
                       background='#27ae60', 
                       foreground='white')
        
        style.configure('Danger.TButton', 
                       background='#e74c3c', 
                       foreground='white')
        
        style.configure('Info.TButton', 
                       background='#3498db', 
                       foreground='white')
    
    def _setup_ui(self) -> None:
        """Setup the main user interface with responsive grid layout."""
        try:
            # Configure root grid
            self.root.grid_rowconfigure(1, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            
            # Main title
            self._setup_title_bar()
            
            # Main container with grid
            main_frame = tk.Frame(self.root, bg='#2c3e50')
            main_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
            
            # Configure main_frame grid
            main_frame.grid_rowconfigure(0, weight=1)
            main_frame.grid_columnconfigure(0, weight=0, minsize=350)  # Left panel fixed width
            main_frame.grid_columnconfigure(1, weight=1)  # Right panel expandable
            
            # Left panel - Server controls
            self._setup_left_panel(main_frame)
            
            # Right panel - Log and commands
            self._setup_right_panel(main_frame)
            
        except Exception as e:
            app_logger.error(f"Error setting up UI: {e}")
    
    def _setup_title_bar(self) -> None:
        """Setup title bar with theme switcher."""
        colors = theme_manager.get_current_colors()
        
        self.title_frame = tk.Frame(self.root, bg=colors['frame_bg'])
        self.title_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        
        # Title and theme switcher container
        self.title_container = tk.Frame(self.title_frame, bg=colors['frame_bg'])
        self.title_container.pack(fill='x', padx=10)
        
        self.title_label = ttk.Label(self.title_container, 
                              text="🚀 DevServer Manager", 
                              style='Title.TLabel')
        self.title_label.pack(side='left')
        
        # Theme switcher
        self.theme_frame = tk.Frame(self.title_container, bg=colors['frame_bg'])
        self.theme_frame.pack(side='right')
        
        self.theme_label = tk.Label(self.theme_frame, text="Theme:", 
                             bg=colors['frame_bg'], fg=colors['fg'], font=('Arial', 10))
        self.theme_label.pack(side='left', padx=(0, 5))
        
        self.theme_var = tk.StringVar(value=theme_manager.get_theme())
        self.theme_combo = ttk.Combobox(self.theme_frame, textvariable=self.theme_var,
                                      values=["system", "dark", "light"],
                                      state="readonly", width=10)
        self.theme_combo.pack(side='left')
        self.theme_combo.bind('<<ComboboxSelected>>', self._on_theme_change)
    
    def _setup_left_panel(self, parent: tk.Widget) -> None:
        """Setup left panel with server controls."""
        colors = theme_manager.get_current_colors()
        
        self.left_frame = tk.Frame(parent, bg=colors['frame_bg'], relief='raised', bd=2)
        self.left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        # Server controls with scrollable canvas
        self._setup_scrollable_server_controls(self.left_frame)
    
    def _setup_right_panel(self, parent: tk.Widget) -> None:
        """Setup right panel with logs and commands."""
        colors = theme_manager.get_current_colors()
        
        self.right_frame = tk.Frame(parent, bg=colors['frame_bg'], relief='raised', bd=2)
        self.right_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        # Configure right_frame grid
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=0)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        # Log area
        self._setup_log_area(self.right_frame)
        
        # Command area
        self._setup_command_area(self.right_frame)
    
    def _setup_scrollable_server_controls(self, parent: tk.Widget) -> None:
        """Setup scrollable server control panel."""
        try:
            colors = theme_manager.get_current_colors()
            
            # Configure parent grid
            parent.grid_rowconfigure(0, weight=1)
            parent.grid_columnconfigure(0, weight=1)
            
            # Create canvas and scrollbar for scrollable content
            self.canvas = tk.Canvas(parent, bg=colors['frame_bg'], highlightthickness=0)
            self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
            self.scrollable_frame = tk.Frame(self.canvas, bg=colors['frame_bg'])
            
            # Configure scrolling
            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            )
            
            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            
            # Grid layout for canvas and scrollbar
            self.canvas.grid(row=0, column=0, sticky='nsew')
            self.scrollbar.grid(row=0, column=1, sticky='ns')
            
            # Bind mousewheel to canvas
            def _on_mousewheel(event):
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            # Setup server controls in the scrollable frame
            self._setup_server_controls(self.scrollable_frame)
            
            # Initialize scrollbar visibility (will be updated when servers are loaded)
            self._update_scrollbar_visibility(0)
            
        except Exception as e:
            app_logger.error(f"Error setting up scrollable server controls: {e}")
    
    def _update_scrollbar_visibility(self, server_count: int) -> None:
        """Update scrollbar visibility based on server count.
        
        Args:
            server_count: Number of servers in the list
        """
        try:
            if server_count == 0:
                # Hide scrollbar when no servers
                self.scrollbar.grid_remove()
                # Reconfigure canvas to take full width
                self.canvas.grid_configure(columnspan=2)
            else:
                # Show scrollbar when servers exist
                self.scrollbar.grid(row=0, column=1, sticky='ns')
                # Reconfigure canvas to normal width
                self.canvas.grid_configure(columnspan=1)
        except Exception as e:
            app_logger.error(f"Error updating scrollbar visibility: {e}")
    
    def _setup_server_controls(self, parent: tk.Widget) -> None:
        """Setup server control panel."""
        try:
            control_label = ttk.Label(parent, 
                                    text="Server Controls", 
                                    style='Title.TLabel')
            control_label.pack(pady=10)
            
            # Server status and controls will be populated by refresh_server_list
            self._setup_global_controls(parent)
            self._setup_crud_controls(parent)
            
        except Exception as e:
            app_logger.error(f"Error setting up server controls: {e}")
    
    def _setup_global_controls(self, parent: tk.Widget) -> None:
        """Setup global control buttons."""
        global_frame = tk.Frame(parent, bg='#34495e', relief='groove', bd=2)
        global_frame.pack(fill='x', padx=10, pady=10)
        
        global_label = ttk.Label(global_frame, 
                               text="Global Controls", 
                               style='Server.TLabel')
        global_label.pack(pady=5)
        
        start_all_btn = ttk.Button(global_frame, 
                                 text="🚀 Start All Servers", 
                                 style='Success.TButton',
                                 command=self.start_all_servers)
        start_all_btn.pack(fill='x', padx=5, pady=2)
        
        stop_all_btn = ttk.Button(global_frame, 
                                text="🛑 Stop All Servers", 
                                style='Danger.TButton',
                                command=self.stop_all_servers)
        stop_all_btn.pack(fill='x', padx=5, pady=2)
        
        clear_log_btn = ttk.Button(global_frame, 
                                 text="🗑️ Clear Log", 
                                 style='Info.TButton',
                                 command=self.clear_log)
        clear_log_btn.pack(fill='x', padx=5, pady=2)
    
    def _setup_crud_controls(self, parent: tk.Widget) -> None:
        """Setup CRUD control buttons."""
        crud_frame = tk.Frame(parent, bg='#34495e', relief='groove', bd=2)
        crud_frame.pack(fill='x', padx=10, pady=10)
        
        crud_label = ttk.Label(crud_frame, 
                             text="Server Management", 
                             style='Server.TLabel')
        crud_label.pack(pady=5)
        
        add_server_btn = ttk.Button(crud_frame, 
                                  text="➕ Add Server", 
                                  style='Success.TButton',
                                  command=self.add_server)
        add_server_btn.pack(fill='x', padx=5, pady=2)
        
        refresh_btn = ttk.Button(crud_frame, 
                               text="🔄 Refresh UI", 
                               style='Info.TButton',
                               command=self.refresh_server_list)
        refresh_btn.pack(fill='x', padx=5, pady=2)
    
    def _setup_log_area(self, parent: tk.Widget) -> None:
        """Setup log display area with responsive grid layout."""
        try:
            log_label = ttk.Label(parent, 
                                text="📋 Server Logs", 
                                style='Title.TLabel')
            log_label.grid(row=0, column=0, pady=(5, 2), sticky='ew')
            
            # Log text area with scrollbar
            self.log_text = scrolledtext.ScrolledText(
                parent, 
                height=20, 
                bg='#1e1e1e', 
                fg='#00ff00', 
                font=('Consolas', 9),
                wrap=tk.WORD
            )
            self.log_text.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 5))
            
            # Configure text tags for different log levels
            self.log_text.tag_configure('INFO', foreground='#00ff00')
            self.log_text.tag_configure('ERROR', foreground='#ff4444')
            self.log_text.tag_configure('WARNING', foreground='#ffaa00')
            self.log_text.tag_configure('SUCCESS', foreground='#44ff44')
            
            self.log_message("DevServer Manager initialized successfully!", "SUCCESS")
            
        except Exception as e:
            app_logger.error(f"Error setting up log area: {e}")
    
    def _setup_command_area(self, parent: tk.Widget) -> None:
        """Setup custom command execution area."""
        try:
            cmd_frame = tk.Frame(parent, bg='#34495e')
            cmd_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=5)
            
            # Configure cmd_frame grid
            cmd_frame.grid_columnconfigure(0, weight=1)
            
            cmd_label = ttk.Label(cmd_frame, 
                                text="💻 Custom Command", 
                                style='Server.TLabel')
            cmd_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
            
            # Command input
            input_frame = tk.Frame(cmd_frame, bg='#34495e')
            input_frame.grid(row=1, column=0, sticky='ew', pady=5)
            
            # Configure input_frame grid
            input_frame.grid_columnconfigure(0, weight=1)
            
            self.command_entry = tk.Entry(
                input_frame, 
                bg='#2c3e50', 
                fg='#ecf0f1', 
                font=('Consolas', 10),
                insertbackground='#ecf0f1'
            )
            self.command_entry.grid(row=0, column=0, sticky='ew', padx=(0, 5))
            self.command_entry.bind('<Return>', lambda e: self.execute_custom_command())
            
            execute_btn = ttk.Button(
                input_frame, 
                text="Execute", 
                style='Info.TButton',
                command=self.execute_custom_command
            )
            execute_btn.grid(row=0, column=1, sticky='e')
            
        except Exception as e:
            app_logger.error(f"Error setting up command area: {e}")
    
    def _init_theme_manager(self) -> None:
        """Initialize theme manager."""
        try:
            # Register callback for theme changes
            theme_manager.register_callback(self._apply_theme_callback)
            
            # Load and apply initial theme
            theme_manager.load_theme()
            self._apply_theme()
        except Exception as e:
            app_logger.error(f"Error initializing theme manager: {e}")
    
    def _apply_theme(self) -> None:
        """Apply current theme to the interface."""
        try:
            colors = theme_manager.get_current_colors()
            
            # Apply to root window
            self.root.configure(bg=colors["bg"])
            
            # Apply theme recursively to all widgets
            self._apply_theme_recursive(self.root, colors)
            
        except Exception as e:
            app_logger.error(f"Error applying theme: {e}")
    
    def _apply_theme_callback(self, colors: Dict[str, str]) -> None:
        """Callback function for theme changes."""
        try:
            # Apply to root window
            self.root.configure(bg=colors["bg"])
            
            # Apply theme recursively to all widgets
            self._apply_theme_recursive(self.root, colors)
            
        except Exception as e:
            app_logger.error(f"Error in theme callback: {e}")
    
    def _apply_theme_recursive(self, widget, colors: Dict[str, str]) -> None:
        """Recursively apply theme to all child widgets."""
        try:
            widget_class = widget.winfo_class()
            
            # Apply theme based on widget type
            if widget_class == "Frame":
                widget.configure(bg=colors["frame_bg"])
            elif widget_class == "Label":
                widget.configure(bg=colors["bg"], fg=colors["fg"])
            elif widget_class == "Button":
                widget.configure(
                    bg=colors["button_bg"],
                    fg=colors["button_fg"],
                    activebackground=colors["button_active_bg"],
                    activeforeground=colors["button_fg"]
                )
            elif widget_class == "Entry":
                widget.configure(
                    bg=colors["entry_bg"],
                    fg=colors["entry_fg"],
                    insertbackground=colors["entry_fg"]
                )
            elif widget_class == "Text":
                widget.configure(
                    bg=colors["text_bg"],
                    fg=colors["text_fg"],
                    insertbackground=colors["text_fg"],
                    selectbackground=colors["select_bg"],
                    selectforeground=colors["select_fg"]
                )
            elif widget_class == "Listbox":
                widget.configure(
                    bg=colors["text_bg"],
                    fg=colors["text_fg"],
                    selectbackground=colors["select_bg"],
                    selectforeground=colors["select_fg"]
                )
            elif widget_class == "Scrollbar":
                widget.configure(
                    bg=colors["scrollbar_bg"],
                    troughcolor=colors["scrollbar_bg"],
                    activebackground=colors["scrollbar_fg"]
                )
            
            # Recursively apply to all children
            for child in widget.winfo_children():
                self._apply_theme_recursive(child, colors)
                
        except Exception as e:
            # Silently ignore theme application errors for individual widgets
            pass
    
    def _start_log_processor(self) -> None:
        """Start the log processor thread."""
        def process_logs():
            while self.log_processor_running:
                try:
                    message, level = self.log_queue.get(timeout=0.1)
                    if self.log_processor_running:  # Check again before GUI operation
                        self.root.after(0, self._add_log_to_text, message, level)
                except queue.Empty:
                    continue
                except Exception as e:
                    if self.log_processor_running:  # Only log if still running
                        app_logger.error(f"Error processing logs: {e}")
                    break
        
        log_thread = threading.Thread(target=process_logs, daemon=True)
        log_thread.start()
    
    def _add_log_to_text(self, message: str, level: str) -> None:
        """Add log message to text widget (called from main thread)."""
        try:
            if self.log_text and self.log_processor_running:
                self.log_text.insert(tk.END, message, level)
                self.log_text.see(tk.END)
        except Exception as e:
            if self.log_processor_running:  # Only log if still running
                app_logger.error(f"Error adding log to text: {e}")
    
    def _load_servers(self) -> None:
        """Load server configurations."""
        try:
            servers = self.config_manager.load_server_config()
            for name, config in servers.items():
                # Convert to ServerConfig if it's a dict
                if isinstance(config, dict):
                    from ..models.server_config import ServerConfig
                    server_config = ServerConfig(
                        name=name,
                        path=config.get('path', ''),
                        port=str(config.get('port', 8000)),
                        command=config.get('command', 'python -m http.server')
                    )
                else:
                    server_config = config
                
                self.server_manager.add_server(server_config)
            self.refresh_server_list()
        except Exception as e:
            app_logger.error(f"Error loading servers: {e}")
    
    def _on_window_resize(self, event) -> None:
        """Handle window resize events."""
        try:
            # Only handle resize events for the main window
            if event.widget == self.root:
                # Adjust layout based on window size
                width = self.root.winfo_width()
                
                # Responsive layout adjustments
                if width < 900:
                    self._adjust_compact_layout()
                else:
                    self._adjust_normal_layout()
        except Exception:
            pass  # Ignore resize errors to prevent spam
    
    def _adjust_compact_layout(self) -> None:
        """Adjust layout for compact/smaller windows."""
        # Implementation for compact layout adjustments
        pass
    
    def _adjust_normal_layout(self) -> None:
        """Adjust layout for normal/larger windows."""
        # Implementation for normal layout adjustments
        pass
    
    def _on_theme_change(self, event=None) -> None:
        """Handle theme change event."""
        try:
            new_theme = self.theme_var.get()
            theme_manager.set_theme(new_theme)
            self._apply_theme()
            self.log_message(f"Theme changed to: {new_theme}", "INFO")
        except Exception as e:
            app_logger.error(f"Error changing theme: {e}")
    
    def _setup_system_tray(self) -> None:
        """Setup system tray icon and menu."""
        try:
            if not TRAY_AVAILABLE:
                return
            
            # Try to load custom icon, fallback to generated icon
            try:
                icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'app_icon.ico')
                if os.path.exists(icon_path):
                    image = Image.open(icon_path)
                    # Resize to 64x64 if needed
                    if image.size != (64, 64):
                        image = image.resize((64, 64), Image.Resampling.LANCZOS)
                else:
                    raise FileNotFoundError("Icon file not found")
            except Exception:
                # Fallback to generated icon
                image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
                draw = ImageDraw.Draw(image)
                # Create professional server icon
                draw.ellipse([2, 2, 62, 62], fill=(52, 152, 219), outline=(44, 62, 80), width=2)
                draw.rectangle([16, 18, 48, 46], fill=(236, 240, 241), outline=(52, 73, 94), width=1)
                draw.rectangle([18, 21, 46, 25], fill=(39, 174, 96))
                draw.rectangle([18, 27, 46, 31], fill=(243, 156, 18))
                draw.rectangle([18, 33, 46, 37], fill=(231, 76, 60))
                draw.rectangle([18, 39, 46, 43], fill=(155, 89, 182))
                # Power indicators
                draw.ellipse([40, 21, 44, 25], fill=(39, 174, 96))
                draw.ellipse([40, 27, 44, 31], fill=(243, 156, 18))
                draw.ellipse([40, 33, 44, 37], fill=(231, 76, 60))
                draw.ellipse([40, 39, 44, 43], fill=(155, 89, 182))
            
            # Create tray menu
            menu = pystray.Menu(
                pystray.MenuItem("Show", self._show_window),
                pystray.MenuItem("Hide", self._hide_to_tray),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Start All Servers", self.start_all_servers),
                pystray.MenuItem("Stop All Servers", self.stop_all_servers),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit", self._quit_application)
            )
            
            # Create tray icon with double-click action
            self.tray_icon = pystray.Icon(
                "DevServer Manager",
                image,
                "DevServer Manager",
                menu,
                default_action=self._show_window  # Double-click action
            )
            
            # Start tray icon in separate thread
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
            app_logger.info("System tray initialized")
            
        except Exception as e:
            app_logger.error(f"Error setting up system tray: {e}")
    
    def _show_window(self, icon=None, item=None) -> None:
        """Show the main window from system tray."""
        try:
            self.root.after(0, self._restore_window)
        except Exception as e:
            app_logger.error(f"Error showing window: {e}")
    
    def _restore_window(self) -> None:
        """Restore window from minimized state."""
        try:
            # Restore window from withdrawn state
            self.root.deiconify()
            
            # Make sure window is visible and on top
            self.root.state('normal')
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.root.attributes('-topmost', False)
            
            # Force focus and bring to front
            self.root.focus_force()
            self.root.grab_set_global()
            self.root.grab_release()
            
            # Update state
            self.is_minimized_to_tray = False
            self.log_message("Window restored from system tray", "INFO")
            
        except Exception as e:
            app_logger.error(f"Error restoring window: {e}")
    
    def _hide_to_tray(self, icon=None, item=None) -> None:
        """Hide window to system tray."""
        try:
            if TRAY_AVAILABLE:
                self.root.withdraw()
                self.is_minimized_to_tray = True
                self.log_message("Application minimized to system tray", "INFO")
            else:
                self.root.iconify()
        except Exception as e:
            app_logger.error(f"Error hiding to tray: {e}")
    
    def _on_window_map(self, event) -> None:
        """Handle window map (show) event."""
        try:
            if event.widget == self.root:
                self.is_minimized_to_tray = False
        except Exception as e:
            app_logger.error(f"Error handling window map: {e}")
    
    def _on_window_unmap(self, event) -> None:
        """Handle window unmap (hide/minimize) event."""
        try:
            if event.widget == self.root and TRAY_AVAILABLE:
                # Small delay to check if window is actually minimized
                self.root.after(100, self._check_minimize_state)
        except Exception as e:
            app_logger.error(f"Error handling window unmap: {e}")
    
    def _check_minimize_state(self) -> None:
        """Check if window should be minimized to tray."""
        try:
            if self.root.state() == 'iconic' and not self.is_minimized_to_tray:
                self._hide_to_tray()
        except Exception as e:
            app_logger.error(f"Error checking minimize state: {e}")
    
    def _quit_application(self, icon=None, item=None) -> None:
        """Quit the application completely."""
        try:
            # Stop tray icon
            if self.tray_icon:
                self.tray_icon.stop()
            
            # Close main window
            self.root.after(0, self._on_closing)
            
        except Exception as e:
            app_logger.error(f"Error quitting application: {e}")
    
    def _on_closing(self) -> None:
        """Handle window closing event."""
        try:
            app_logger.info("_on_closing method called")
            # Check if there are running servers
            running_servers = []
            servers = self.server_manager.get_all_servers()
            for server_name, server_config in servers.items():
                if self.server_manager.is_server_running(server_name):
                    running_servers.append(server_name)
            
            app_logger.info(f"Found {len(running_servers)} running servers: {running_servers}")
            
            # Show confirmation dialog
            from tkinter import messagebox
            if running_servers:
                message = f"Ada {len(running_servers)} server yang sedang berjalan:\n\n"
                message += "\n".join([f"• {name}" for name in running_servers])
                message += "\n\nApakah Anda yakin ingin menutup aplikasi?\nServer yang berjalan akan dihentikan terlebih dahulu."
            else:
                message = "Apakah Anda yakin ingin menutup aplikasi?"
            
            app_logger.info(f"Showing confirmation dialog with message: {message}")
            
            result = messagebox.askyesno(
                "Konfirmasi Tutup Aplikasi",
                message
            )
            
            app_logger.info(f"Dialog result: {result}")
            
            if not result:  # User clicked "No"
                app_logger.info("User clicked No, canceling close")
                return
            
            # User clicked "Yes" - proceed with shutdown
            # Stop log processor first
            self.log_processor_running = False
            
            if running_servers:
                self.log_message("Menghentikan semua server yang sedang berjalan...", "INFO")
                # Stop all servers before closing
                self.stop_all_servers()
                self.log_message("Semua server telah dihentikan.", "SUCCESS")
            
            # Stop tray icon
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.stop()
            
            # Save configuration
            self.config_manager.save_server_configs(servers)
            
            app_logger.info("Application closing")
            self.root.destroy()
            
        except Exception as e:
            app_logger.error(f"Error during application shutdown: {e}")
            self.root.destroy()
    
    # Public methods for server management
    def log_message(self, message: str, level: str = "INFO") -> None:
        """Add message to log with timestamp and level."""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] [{level}] {message}\n"
            
            # Add to queue for thread-safe logging
            self.log_queue.put((formatted_message, level))
            
            # Also log to file
            app_logger.log_app_event(message)
            
        except Exception as e:
            app_logger.error(f"Error logging message: {e}")
    
    def refresh_server_list(self) -> None:
        """Refresh the server list display."""
        try:
            # Clear existing individual server frames only
            for widget in self.scrollable_frame.winfo_children():
                if hasattr(widget, 'server_name'):
                    widget.destroy()
            
            # Add individual server controls (don't recreate global controls)
            servers = self.server_manager.get_all_servers()
            for server_name, config in servers.items():
                self._create_server_control(server_name, config)
            
            # Update scrollbar visibility based on server count
            self._update_scrollbar_visibility(len(servers))
            
        except Exception as e:
            app_logger.error(f"Error refreshing server list: {e}")
    
    def _create_server_control(self, server_name: str, config: Dict[str, Any]) -> None:
        """Create control panel for a single server."""
        try:
            from .widgets import ServerControlWidget
            from ..models.server_config import ServerConfig
            
            # Convert dict to ServerConfig if needed
            if isinstance(config, dict):
                server_config = ServerConfig(
                    name=server_name,
                    path=config.get('path', ''),
                    port=config.get('port', 8000),
                    command=config.get('command', 'python -m http.server')
                )
            else:
                server_config = config
            
            # Create server control widget
            widget = ServerControlWidget(
                parent=self.scrollable_frame,
                server_name=server_name,
                config=server_config,
                on_start=lambda name: self.start_server(name),
                on_stop=lambda name: self.stop_server(name),
                on_edit=lambda name: self.edit_server(name),
                on_delete=lambda name: self.delete_server(name),
                on_browse=lambda name: self.browse_server_folder(name)
            )
            
            # Store reference for later updates
            self.server_frames[server_name] = widget
            
        except Exception as e:
            app_logger.error(f"Error creating server control for {server_name}: {e}")
    
    def start_server(self, server_name: str) -> None:
        """Start a specific server."""
        try:
            success = self.server_manager.start_server(server_name)
            if success:
                self.log_message(f"Started {server_name}", "SUCCESS")
                # Update widget status
                if server_name in self.server_frames:
                    server_config = self.server_manager.get_server(server_name)
                    if server_config:
                        self.server_frames[server_name].update_config(server_config)
            else:
                self.log_message(f"Failed to start {server_name}", "ERROR")
        except Exception as e:
            app_logger.error(f"Error starting server {server_name}: {e}")
    
    def stop_server(self, server_name: str) -> None:
        """Stop a specific server."""
        try:
            success = self.server_manager.stop_server(server_name)
            if success:
                self.log_message(f"Stopped {server_name}", "SUCCESS")
                # Update widget status
                if server_name in self.server_frames:
                    server_config = self.server_manager.get_server(server_name)
                    if server_config:
                        self.server_frames[server_name].update_config(server_config)
            else:
                self.log_message(f"Failed to stop {server_name}", "ERROR")
        except Exception as e:
            app_logger.error(f"Error stopping server {server_name}: {e}")
    
    def start_all_servers(self) -> None:
        """Start all servers."""
        try:
            servers = self.server_manager.get_all_servers()
            for server_name in servers.keys():
                self.start_server(server_name)
        except Exception as e:
            app_logger.error(f"Error starting all servers: {e}")
    
    def stop_all_servers(self) -> None:
        """Stop all servers."""
        try:
            servers = self.server_manager.get_all_servers()
            for server_name in servers.keys():
                self.stop_server(server_name)
        except Exception as e:
            app_logger.error(f"Error stopping all servers: {e}")
    
    def add_server(self) -> None:
        """Add a new server configuration using template wizard."""
        try:
            wizard = TemplateWizardDialog(self.root)
            if wizard.result:
                wizard_data = wizard.result
                
                # Create ServerConfig object with extended fields
                from ..models.server_config import ServerConfig
                server_config = ServerConfig(
                    name=wizard_data['name'],
                    path=wizard_data['project_path'],
                    port=wizard_data['port'],
                    command=wizard_data['command'],
                    template_id=wizard_data['template_id'],
                    category=wizard_data.get('category', ''),
                    env_vars=wizard_data.get('env_vars', {}),
                    description=wizard_data.get('description', '')
                )
                
                # Add server to manager
                if self.server_manager.add_server(server_config):
                    self.refresh_server_list()
                    self.log_message(f"Added server: {wizard_data['name']} (Template: {wizard_data['template_id']})", "SUCCESS")
                    
                    # Save configuration
                    servers = self.server_manager.get_all_servers()
                    self.config_manager.save_server_config(servers)
                else:
                    self.log_message(f"Failed to add server: {wizard_data['name']}", "ERROR")
        except Exception as e:
            app_logger.error(f"Error adding server: {e}")
            self.log_message(f"Error adding server: {str(e)}", "ERROR")
    
    def edit_server(self, server_name: str) -> None:
        """Edit an existing server configuration."""
        try:
            from tkinter import messagebox
            
            # Check if server exists
            servers = self.server_manager.get_all_servers()
            if server_name not in servers:
                messagebox.showerror("Error", f"Server '{server_name}' not found!")
                return
            
            # Check if server is running
            server = servers[server_name]
            if hasattr(server, 'is_running') and server.is_running():
                messagebox.showwarning("Warning", 
                                     f"Please stop '{server_name}' before editing.")
                return
            
            # Get current config
            current_config = {
                'name': server_name,
                'path': server.path if hasattr(server, 'path') else '',
                'port': server.port if hasattr(server, 'port') else 8000,
                'command': server.command if hasattr(server, 'command') else 'python -m http.server'
            }
            
            # Show edit dialog
            dialog = ServerConfigDialog(
                self.root, 
                "Edit Server", 
                current_config['name'],
                current_config['path'],
                str(current_config['port']),
                current_config['command']
            )
            if dialog.result:
                name, path, port, command = dialog.result
                
                # Create new ServerConfig object
                from ..models.server_config import ServerConfig
                new_server_config = ServerConfig(
                    name=name,
                    path=path,
                    port=str(port),
                    command=command
                )
                
                # Update server configuration using update_server method
                if self.server_manager.update_server(server_name, new_server_config):
                    self.refresh_server_list()
                    self.log_message(f"Server '{server_name}' updated to '{name}'", "SUCCESS")
                    
                    # Save configuration
                    servers = self.server_manager.get_all_servers()
                    self.config_manager.save_server_config(servers)
                else:
                    self.log_message(f"Failed to update server: {server_name}", "ERROR")
                
                self.refresh_server_list()
                
        except Exception as e:
            app_logger.error(f"Error editing server {server_name}: {e}")
    
    def delete_server(self, server_name: str) -> None:
        """Delete a server configuration."""
        try:
            from tkinter import messagebox
            
            # Check if server exists
            servers = self.server_manager.get_all_servers()
            if server_name not in servers:
                messagebox.showerror("Error", f"Server '{server_name}' not found!")
                return
            
            # Check if server is running
            server = servers[server_name]
            if hasattr(server, 'is_running') and server.is_running():
                messagebox.showwarning("Warning", 
                                     f"Please stop '{server_name}' before deleting.")
                return
            
            # Confirm deletion
            result = messagebox.askyesno(
                "Confirm Delete", 
                f"Are you sure you want to delete server '{server_name}'?\n\n"
                f"This action cannot be undone.",
                icon='warning'
            )
            
            if result:
                success = self.server_manager.remove_server(server_name)
                if success:
                    self.log_message(f"Server '{server_name}' deleted successfully", "SUCCESS")
                    self.refresh_server_list()
                    
                    # Save configuration
                    servers = self.server_manager.get_all_servers()
                    self.config_manager.save_server_config(servers)
                else:
                    self.log_message(f"Failed to delete server '{server_name}'", "ERROR")
                    
        except Exception as e:
            app_logger.error(f"Error deleting server {server_name}: {e}")
    
    def browse_server_folder(self, server_name: str) -> None:
        """Browse server folder in file explorer."""
        try:
            import os
            import platform
            import subprocess
            
            servers = self.server_manager.get_all_servers()
            if server_name in servers:
                server = servers[server_name]
                path = server.path if hasattr(server, 'path') else ''
                
                if path:
                    # Normalize path for current OS
                    normalized_path = os.path.normpath(os.path.abspath(path))
                    
                    if os.path.exists(normalized_path):
                        try:
                            # Use os.startfile for Windows (more reliable)
                            if platform.system() == 'Windows':
                                os.startfile(normalized_path)
                            elif platform.system() == 'Darwin':  # macOS
                                subprocess.run(['open', normalized_path], check=True)
                            else:  # Linux
                                subprocess.run(['xdg-open', normalized_path], check=True)
                            
                            self.log_message(f"Opened folder for '{server_name}': {normalized_path}", "SUCCESS")
                        except Exception as open_error:
                            # Fallback to explorer command for Windows
                            if platform.system() == 'Windows':
                                subprocess.run(['explorer', '/select,', normalized_path], check=False)
                                self.log_message(f"Opened folder for '{server_name}': {normalized_path}", "SUCCESS")
                            else:
                                raise open_error
                    else:
                        self.log_message(f"Path not found for '{server_name}': {normalized_path}", "ERROR")
                        # Try to create the directory if it doesn't exist
                        try:
                            os.makedirs(normalized_path, exist_ok=True)
                            self.log_message(f"Created directory: {normalized_path}", "INFO")
                            if platform.system() == 'Windows':
                                os.startfile(normalized_path)
                            self.log_message(f"Opened newly created folder for '{server_name}'", "SUCCESS")
                        except Exception as create_error:
                            self.log_message(f"Failed to create directory: {str(create_error)}", "ERROR")
                else:
                    self.log_message(f"No path configured for '{server_name}'", "ERROR")
            else:
                self.log_message(f"Server '{server_name}' not found", "ERROR")
                
        except Exception as e:
            app_logger.error(f"Error browsing server folder {server_name}: {e}")
            self.log_message(f"Error opening folder for '{server_name}': {str(e)}", "ERROR")
    
    def clear_log(self) -> None:
        """Clear the log display."""
        try:
            if self.log_text:
                self.log_text.delete(1.0, tk.END)
                self.log_message("Log cleared", "INFO")
        except Exception as e:
            app_logger.error(f"Error clearing log: {e}")
    
    def execute_custom_command(self) -> None:
        """Execute custom command from entry field."""
        import subprocess
        import threading
        
        try:
            command = self.command_entry.get().strip()
            if not command:
                return
            
            self.log_message(f"Executing: {command}", "INFO")
            self.command_entry.delete(0, tk.END)
            
            def run_command():
                try:
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.stdout:
                        self.log_message(f"Output: {result.stdout.strip()}", "INFO")
                    
                    if result.stderr:
                        self.log_message(f"Error: {result.stderr.strip()}", "ERROR")
                    
                    if result.returncode == 0:
                        self.log_message("Command executed successfully", "SUCCESS")
                    else:
                        self.log_message(f"Command failed with code {result.returncode}", "ERROR")
                        
                except subprocess.TimeoutExpired:
                    self.log_message("Command timed out (30s limit)", "ERROR")
                except Exception as e:
                    self.log_message(f"Command execution error: {str(e)}", "ERROR")
            
            cmd_thread = threading.Thread(target=run_command, daemon=True)
            cmd_thread.start()
            
        except Exception as e:
            app_logger.error(f"Error executing custom command: {e}")