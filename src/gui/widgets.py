"""Reusable Widget Components

This module contains reusable widget components for the Server Manager GUI.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Callable
from datetime import datetime

from ..models.server_config import ServerConfig
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.logger import app_logger


class ServerControlWidget(tk.Frame):
    """Widget for controlling individual servers."""
    
    def __init__(self, parent: tk.Widget, server_name: str, config: ServerConfig,
                 on_start: Optional[Callable] = None,
                 on_stop: Optional[Callable] = None,
                 on_edit: Optional[Callable] = None,
                 on_delete: Optional[Callable] = None,
                 on_browse: Optional[Callable] = None):
        """Initialize server control widget.
        
        Args:
            parent: Parent widget
            server_name: Name of the server
            config: Server configuration
            on_start: Callback for start button
            on_stop: Callback for stop button
            on_edit: Callback for edit button
            on_delete: Callback for delete button
            on_browse: Callback for browse button
        """
        super().__init__(parent, bg='#34495e', relief='groove', bd=1)
        
        self.server_name = server_name
        self.config = config
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_browse = on_browse
        
        # UI components
        self.status_label = None
        self.start_btn = None
        self.stop_btn = None
        
        self._setup_ui()
        self._update_status()
    
    def _setup_ui(self) -> None:
        """Setup the widget UI."""
        self.pack(fill='x', padx=10, pady=5)
        
        # Server name and status
        name_frame = tk.Frame(self, bg='#34495e')
        name_frame.pack(fill='x', pady=2)
        
        name_label = ttk.Label(name_frame, 
                             text=self.server_name, 
                             style='Server.TLabel')
        name_label.pack(side='left')
        
        self.status_label = ttk.Label(name_frame, 
                                    text=self.config.status if hasattr(self.config, 'status') else 'Stopped', 
                                    style='Server.TLabel')
        self.status_label.pack(side='right')
        
        # Path and port info
        path_display = self.config.path[:30] + "..." if len(self.config.path) > 30 else self.config.path
        info_label = ttk.Label(self, 
                             text=f"Port: {self.config.port} | Path: {path_display}", 
                             style='Server.TLabel')
        info_label.pack(fill='x', pady=2)
        
        # Control buttons
        button_frame = tk.Frame(self, bg='#34495e')
        button_frame.pack(fill='x', pady=5)
        
        self.start_btn = ttk.Button(button_frame, 
                                  text="▶️", 
                                  style='Success.TButton',
                                  width=3,
                                  command=self._on_start_clicked)
        self.start_btn.pack(side='left', padx=2)
        
        self.stop_btn = ttk.Button(button_frame, 
                                 text="⏹️", 
                                 style='Danger.TButton',
                                 width=3,
                                 command=self._on_stop_clicked)
        self.stop_btn.pack(side='left', padx=2)
        
        folder_btn = ttk.Button(button_frame, 
                              text="📁", 
                              style='Info.TButton',
                              width=3,
                              command=self._on_browse_clicked)
        folder_btn.pack(side='right', padx=2)
        
        edit_btn = ttk.Button(button_frame, 
                            text="✏️", 
                            style='Info.TButton',
                            width=3,
                            command=self._on_edit_clicked)
        edit_btn.pack(side='right', padx=2)
        
        delete_btn = ttk.Button(button_frame, 
                              text="🗑️", 
                              style='Danger.TButton',
                              width=3,
                              command=self._on_delete_clicked)
        delete_btn.pack(side='right', padx=2)
    
    def _on_start_clicked(self) -> None:
        """Handle start button click."""
        if self.on_start:
            self.on_start(self.server_name)
    
    def _on_stop_clicked(self) -> None:
        """Handle stop button click."""
        if self.on_stop:
            self.on_stop(self.server_name)
    
    def _on_edit_clicked(self) -> None:
        """Handle edit button click."""
        if self.on_edit:
            self.on_edit(self.server_name)
    
    def _on_delete_clicked(self) -> None:
        """Handle delete button click."""
        if self.on_delete:
            self.on_delete(self.server_name)
    
    def _on_browse_clicked(self) -> None:
        """Handle browse button click."""
        if self.on_browse:
            self.on_browse(self.server_name)
    
    def _update_status(self) -> None:
        """Update status display."""
        if self.status_label:
            status = getattr(self.config, 'status', 'Stopped')
            self.status_label.config(text=status)
            
            # Update button states
            if hasattr(self.config, 'is_running') and self.config.is_running():
                self.start_btn.config(state='disabled')
                self.stop_btn.config(state='normal')
            else:
                self.start_btn.config(state='normal')
                self.stop_btn.config(state='disabled')
    
    def update_config(self, config: ServerConfig) -> None:
        """Update server configuration.
        
        Args:
            config: New server configuration
        """
        self.config = config
        self._update_status()
    
    def set_status(self, status: str) -> None:
        """Set server status.
        
        Args:
            status: New status
        """
        if hasattr(self.config, 'status'):
            self.config.status = status
        self._update_status()


class LogWidget(tk.Frame):
    """Enhanced log display widget."""
    
    def __init__(self, parent: tk.Widget, height: int = 20):
        """Initialize log widget.
        
        Args:
            parent: Parent widget
            height: Height of the log area
        """
        super().__init__(parent, bg='#34495e')
        
        self.height = height
        self.log_text = None
        self.auto_scroll = True
        self.max_lines = 1000
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the log widget UI."""
        # Title bar with controls
        title_frame = tk.Frame(self, bg='#34495e')
        title_frame.pack(fill='x', pady=(5, 2))
        
        title_label = ttk.Label(title_frame, 
                              text="📋 Server Logs", 
                              style='Title.TLabel')
        title_label.pack(side='left')
        
        # Log controls
        controls_frame = tk.Frame(title_frame, bg='#34495e')
        controls_frame.pack(side='right')
        
        self.auto_scroll_var = tk.BooleanVar(value=True)
        auto_scroll_cb = ttk.Checkbutton(controls_frame,
                                       text="Auto Scroll",
                                       variable=self.auto_scroll_var,
                                       command=self._toggle_auto_scroll)
        auto_scroll_cb.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(controls_frame,
                             text="Clear",
                             style='Info.TButton',
                             command=self.clear)
        clear_btn.pack(side='left', padx=2)
        
        save_btn = ttk.Button(controls_frame,
                            text="Save",
                            style='Info.TButton',
                            command=self.save_to_file)
        save_btn.pack(side='left', padx=2)
        
        # Log text area
        from tkinter import scrolledtext
        self.log_text = scrolledtext.ScrolledText(
            self, 
            height=self.height, 
            bg='#1e1e1e', 
            fg='#00ff00', 
            font=('Consolas', 9),
            wrap=tk.WORD,
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True, padx=10, pady=(0, 5))
        
        # Configure text tags for different log levels
        self.log_text.tag_configure('INFO', foreground='#00ff00')
        self.log_text.tag_configure('ERROR', foreground='#ff4444')
        self.log_text.tag_configure('WARNING', foreground='#ffaa00')
        self.log_text.tag_configure('SUCCESS', foreground='#44ff44')
        self.log_text.tag_configure('DEBUG', foreground='#888888')
    
    def _toggle_auto_scroll(self) -> None:
        """Toggle auto scroll feature."""
        self.auto_scroll = self.auto_scroll_var.get()
    
    def add_message(self, message: str, level: str = "INFO") -> None:
        """Add message to log.
        
        Args:
            message: Log message
            level: Log level (INFO, ERROR, WARNING, SUCCESS, DEBUG)
        """
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] [{level}] {message}\n"
            
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, formatted_message, level)
            
            # Limit number of lines
            lines = int(self.log_text.index('end-1c').split('.')[0])
            if lines > self.max_lines:
                self.log_text.delete('1.0', f'{lines - self.max_lines}.0')
            
            if self.auto_scroll:
                self.log_text.see(tk.END)
            
            self.log_text.config(state='disabled')
            
        except Exception as e:
            app_logger.error(f"Error adding log message: {e}")
    
    def clear(self) -> None:
        """Clear log contents."""
        try:
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state='disabled')
            self.add_message("Log cleared", "INFO")
        except Exception as e:
            app_logger.error(f"Error clearing log: {e}")
    
    def save_to_file(self) -> None:
        """Save log contents to file."""
        try:
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                content = self.log_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.add_message(f"Log saved to: {filename}", "SUCCESS")
                
        except Exception as e:
            app_logger.error(f"Error saving log to file: {e}")
            self.add_message(f"Error saving log: {e}", "ERROR")
    
    def get_content(self) -> str:
        """Get current log content.
        
        Returns:
            Current log content as string
        """
        try:
            return self.log_text.get(1.0, tk.END)
        except Exception:
            return ""


class CommandWidget(tk.Frame):
    """Enhanced command input widget."""
    
    def __init__(self, parent: tk.Widget, on_execute: Optional[Callable] = None):
        """Initialize command widget.
        
        Args:
            parent: Parent widget
            on_execute: Callback for command execution
        """
        super().__init__(parent, bg='#34495e')
        
        self.on_execute = on_execute
        self.command_history = []
        self.history_index = -1
        self.command_entry = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the command widget UI."""
        # Title
        cmd_label = ttk.Label(self, 
                            text="💻 Custom Command", 
                            style='Server.TLabel')
        cmd_label.pack(anchor='w', pady=(0, 5))
        
        # Command input frame
        input_frame = tk.Frame(self, bg='#34495e')
        input_frame.pack(fill='x', pady=5)
        
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
        
        # Bind events
        self.command_entry.bind('<Return>', self._on_execute)
        self.command_entry.bind('<Up>', self._on_history_up)
        self.command_entry.bind('<Down>', self._on_history_down)
        
        execute_btn = ttk.Button(
            input_frame, 
            text="Execute", 
            style='Info.TButton',
            command=self._on_execute
        )
        execute_btn.grid(row=0, column=1, sticky='e')
        
        # Command history frame
        history_frame = tk.Frame(self, bg='#34495e')
        history_frame.pack(fill='x', pady=(5, 0))
        
        history_label = ttk.Label(history_frame,
                                text="Recent Commands:",
                                style='Server.TLabel')
        history_label.pack(anchor='w')
        
        # History listbox
        self.history_listbox = tk.Listbox(
            history_frame,
            height=3,
            bg='#2c3e50',
            fg='#ecf0f1',
            font=('Consolas', 9),
            selectbackground='#3498db'
        )
        self.history_listbox.pack(fill='x', pady=(2, 0))
        self.history_listbox.bind('<Double-Button-1>', self._on_history_select)
    
    def _on_execute(self, event=None) -> None:
        """Handle command execution."""
        command = self.command_entry.get().strip()
        if command:
            # Add to history
            if command not in self.command_history:
                self.command_history.append(command)
                self.history_listbox.insert(tk.END, command)
                
                # Limit history size
                if len(self.command_history) > 20:
                    self.command_history.pop(0)
                    self.history_listbox.delete(0)
            
            self.history_index = len(self.command_history)
            
            # Execute command
            if self.on_execute:
                self.on_execute(command)
            
            # Clear entry
            self.command_entry.delete(0, tk.END)
    
    def _on_history_up(self, event) -> None:
        """Handle up arrow key for command history."""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
    
    def _on_history_down(self, event) -> None:
        """Handle down arrow key for command history."""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        elif self.history_index >= len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.command_entry.delete(0, tk.END)
    
    def _on_history_select(self, event) -> None:
        """Handle history selection from listbox."""
        selection = self.history_listbox.curselection()
        if selection:
            command = self.history_listbox.get(selection[0])
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, command)
    
    def set_command(self, command: str) -> None:
        """Set command in entry field.
        
        Args:
            command: Command to set
        """
        self.command_entry.delete(0, tk.END)
        self.command_entry.insert(0, command)
    
    def get_command(self) -> str:
        """Get current command from entry field.
        
        Returns:
            Current command text
        """
        return self.command_entry.get().strip()
    
    def clear_history(self) -> None:
        """Clear command history."""
        self.command_history.clear()
        self.history_listbox.delete(0, tk.END)
        self.history_index = -1


class StatusBarWidget(tk.Frame):
    """Status bar widget for displaying application status."""
    
    def __init__(self, parent: tk.Widget):
        """Initialize status bar widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent, bg='#2c3e50', height=25)
        
        self.status_label = None
        self.server_count_label = None
        self.running_count_label = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup status bar UI."""
        self.pack(fill='x', side='bottom')
        self.pack_propagate(False)
        
        # Status message
        self.status_label = tk.Label(
            self,
            text="Ready",
            bg='#2c3e50',
            fg='#ecf0f1',
            font=('Arial', 9),
            anchor='w'
        )
        self.status_label.pack(side='left', padx=10)
        
        # Server counts
        self.server_count_label = tk.Label(
            self,
            text="Servers: 0",
            bg='#2c3e50',
            fg='#ecf0f1',
            font=('Arial', 9)
        )
        self.server_count_label.pack(side='right', padx=10)
        
        self.running_count_label = tk.Label(
            self,
            text="Running: 0",
            bg='#2c3e50',
            fg='#27ae60',
            font=('Arial', 9)
        )
        self.running_count_label.pack(side='right', padx=10)
    
    def set_status(self, message: str) -> None:
        """Set status message.
        
        Args:
            message: Status message
        """
        if self.status_label:
            self.status_label.config(text=message)
    
    def update_server_counts(self, total: int, running: int) -> None:
        """Update server count displays.
        
        Args:
            total: Total number of servers
            running: Number of running servers
        """
        if self.server_count_label:
            self.server_count_label.config(text=f"Servers: {total}")
        
        if self.running_count_label:
            self.running_count_label.config(
                text=f"Running: {running}",
                fg='#27ae60' if running > 0 else '#95a5a6'
            )