"""Dialog components for DevServer Manager Application

This module contains dialog classes for various user interactions.
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk, scrolledtext
import os
import webbrowser
from typing import Optional, Tuple, Dict, List
from ..services.template_manager import TemplateManager
from ..services.update_checker import UpdateInfo
from ..services.download_manager import DownloadManager, DownloadProgress
from ..services.update_installer import UpdateInstaller


class ServerConfigDialog:
    """Dialog for server configuration (Add/Edit)"""
    
    def __init__(self, parent: tk.Widget, title: str, name: str = "", 
                 path: str = "", port: str = "", command: str = ""):
        """Initialize server configuration dialog.
        
        Args:
            parent: Parent widget
            title: Dialog title
            name: Initial server name
            path: Initial server path
            port: Initial server port
            command: Initial server command
        """
        self.result: Optional[Tuple[str, str, str, str]] = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.configure(bg='#2c3e50')
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_dialog_ui(name, path, port, command)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_dialog_ui(self, name: str, path: str, port: str, command: str) -> None:
        """Setup dialog UI elements.
        
        Args:
            name: Initial server name
            path: Initial server path
            port: Initial server port
            command: Initial server command
        """
        try:
            # Main frame
            main_frame = tk.Frame(self.dialog, bg='#2c3e50')
            main_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(
                main_frame,
                text="Server Configuration",
                bg='#2c3e50',
                fg='#ecf0f1',
                font=('Arial', 14, 'bold')
            )
            title_label.pack(pady=(0, 20))
            
            # Server Name
            name_frame = tk.Frame(main_frame, bg='#2c3e50')
            name_frame.pack(fill='x', pady=5)
            
            tk.Label(
                name_frame,
                text="Server Name:",
                bg='#2c3e50',
                fg='#ecf0f1',
                font=('Arial', 10, 'bold')
            ).pack(anchor='w')
            
            self.name_entry = tk.Entry(
                name_frame,
                bg='#34495e',
                fg='#ecf0f1',
                font=('Arial', 10),
                insertbackground='#ecf0f1'
            )
            self.name_entry.pack(fill='x', pady=(5, 0))
            self.name_entry.insert(0, name)
            
            # Server Path
            path_frame = tk.Frame(main_frame, bg='#2c3e50')
            path_frame.pack(fill='x', pady=5)
            
            tk.Label(
                path_frame,
                text="Server Path:",
                bg='#2c3e50',
                fg='#ecf0f1',
                font=('Arial', 10, 'bold')
            ).pack(anchor='w')
            
            path_input_frame = tk.Frame(path_frame, bg='#2c3e50')
            path_input_frame.pack(fill='x', pady=(5, 0))
            
            self.path_entry = tk.Entry(
                path_input_frame,
                bg='#34495e',
                fg='#ecf0f1',
                font=('Arial', 10),
                insertbackground='#ecf0f1'
            )
            self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
            self.path_entry.insert(0, path)
            
            browse_btn = tk.Button(
                path_input_frame,
                text="📁 Browse",
                bg='#3498db',
                fg='white',
                font=('Arial', 9),
                command=self.browse_path
            )
            browse_btn.pack(side='right')
            
            # Server Port
            port_frame = tk.Frame(main_frame, bg='#2c3e50')
            port_frame.pack(fill='x', pady=5)
            
            tk.Label(
                port_frame,
                text="Server Port (Optional):",
                bg='#2c3e50',
                fg='#ecf0f1',
                font=('Arial', 10, 'bold')
            ).pack(anchor='w')
            
            # Add description label
            tk.Label(
                port_frame,
                text="Leave empty to run without specific port, or enter port number to append --port=<number> to command",
                bg='#2c3e50',
                fg='#95a5a6',
                font=('Arial', 8),
                wraplength=400
            ).pack(anchor='w', pady=(0, 5))
            
            self.port_entry = tk.Entry(
                port_frame,
                bg='#34495e',
                fg='#ecf0f1',
                font=('Arial', 10),
                insertbackground='#ecf0f1'
            )
            self.port_entry.pack(fill='x', pady=(5, 0))
            self.port_entry.insert(0, port)
            
            # Server Command
            command_frame = tk.Frame(main_frame, bg='#2c3e50')
            command_frame.pack(fill='x', pady=5)
            
            tk.Label(
                command_frame,
                text="Start Command:",
                bg='#2c3e50',
                fg='#ecf0f1',
                font=('Arial', 10, 'bold')
            ).pack(anchor='w')
            
            self.command_entry = tk.Text(
                command_frame,
                bg='#34495e',
                fg='#ecf0f1',
                font=('Consolas', 9),
                insertbackground='#ecf0f1',
                height=3,
                wrap=tk.WORD
            )
            self.command_entry.pack(fill='x', pady=(5, 0))
            self.command_entry.insert('1.0', command)
            
            # Buttons
            button_frame = tk.Frame(main_frame, bg='#2c3e50')
            button_frame.pack(fill='x', pady=(20, 0))
            
            save_btn = tk.Button(
                button_frame,
                text="💾 Save",
                bg='#27ae60',
                fg='white',
                font=('Arial', 10, 'bold'),
                command=self.save_config
            )
            save_btn.pack(side='left', padx=(0, 10))
            
            cancel_btn = tk.Button(
                button_frame,
                text="❌ Cancel",
                bg='#e74c3c',
                fg='white',
                font=('Arial', 10, 'bold'),
                command=self.cancel
            )
            cancel_btn.pack(side='left')
            
            # Bind Enter key to save
            self.dialog.bind('<Return>', lambda e: self.save_config())
            self.dialog.bind('<Escape>', lambda e: self.cancel())
            
            # Focus on name entry
            self.name_entry.focus_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error setting up dialog: {str(e)}")
    
    def browse_path(self) -> None:
        """Browse for server path."""
        try:
            current_path = self.path_entry.get()
            new_path = filedialog.askdirectory(
                title="Select Server Directory",
                initialdir=current_path if current_path else os.getcwd()
            )
            
            if new_path:
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, new_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error browsing path: {str(e)}")
    
    def save_config(self) -> None:
        """Save server configuration."""
        try:
            name = self.name_entry.get().strip()
            path = self.path_entry.get().strip()
            port = self.port_entry.get().strip()
            command = self.command_entry.get('1.0', tk.END).strip()
            
            # Validation
            if not name:
                messagebox.showerror("Error", "Server name is required!")
                self.name_entry.focus_set()
                return
            
            if not path:
                messagebox.showerror("Error", "Server path is required!")
                self.path_entry.focus_set()
                return
            
            if not os.path.exists(path):
                messagebox.showerror("Error", f"Path does not exist: {path}")
                self.path_entry.focus_set()
                return
            
            # Port is now optional - only validate if provided
            if port:
                try:
                    port_num = int(port)
                    if port_num < 1 or port_num > 65535:
                        raise ValueError("Port out of range")
                except ValueError:
                    messagebox.showerror("Error", "Port must be a number between 1 and 65535!")
                    self.port_entry.focus_set()
                    return
            
            if not command:
                messagebox.showerror("Error", "Start command is required!")
                self.command_entry.focus_set()
                return
            
            # Set result and close dialog
            self.result = (name, path, port, command)
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving configuration: {str(e)}")
    
    def cancel(self) -> None:
        """Cancel dialog."""
        self.result = None
        self.dialog.destroy()


class TemplateWizardDialog:
    """Wizard dialog for creating server with template selection"""
    
    def __init__(self, parent: tk.Widget):
        """Initialize template wizard dialog.
        
        Args:
            parent: Parent widget
        """
        self.result: Optional[Dict] = None
        self.template_manager = TemplateManager()
        self.current_step = 0
        self.total_steps = 3
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Server Wizard")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg='#2c3e50')
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        # Initialize data
        self.wizard_data = {
            'project_path': '',
            'template_id': 'custom',
            'name': '',
            'port': '',
            'command': '',
            'env_vars': {},
            'description': ''
        }
        
        self.setup_wizard_ui()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_wizard_ui(self) -> None:
        """Setup wizard UI components."""
        # Main container
        main_frame = tk.Frame(self.dialog, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = tk.Label(
            header_frame,
            text="Step 1: Select Project Directory",
            font=('Arial', 16, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.title_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(
            header_frame,
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=(10, 0))
        self.update_progress()
        
        # Content frame
        self.content_frame = tk.Frame(main_frame, bg='#2c3e50')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.back_button = tk.Button(
            button_frame,
            text="← Back",
            command=self.previous_step,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10),
            padx=20,
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.next_button = tk.Button(
            button_frame,
            text="Next →",
            command=self.next_step,
            bg='#3498db',
            fg='white',
            font=('Arial', 10),
            padx=20
        )
        self.next_button.pack(side=tk.RIGHT)
        
        self.cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            padx=20
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Show first step
        self.show_step_1()
    
    def update_progress(self) -> None:
        """Update progress bar."""
        progress_value = (self.current_step / self.total_steps) * 100
        self.progress['value'] = progress_value
    
    def show_step_1(self) -> None:
        """Show step 1: Project directory selection."""
        self.clear_content()
        self.title_label.config(text="Step 1: Select Project Directory")
        
        # Project path selection
        path_frame = tk.Frame(self.content_frame, bg='#2c3e50')
        path_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            path_frame,
            text="Project Directory:",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        path_input_frame = tk.Frame(path_frame, bg='#2c3e50')
        path_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.path_entry = tk.Entry(
            path_input_frame,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.path_entry.insert(0, self.wizard_data['project_path'])
        
        browse_button = tk.Button(
            path_input_frame,
            text="Browse",
            command=self.browse_directory,
            bg='#3498db',
            fg='white',
            font=('Arial', 9)
        )
        browse_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Auto-detect button
        detect_button = tk.Button(
            path_frame,
            text="🔍 Auto-Detect Project Type",
            command=self.auto_detect,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10)
        )
        detect_button.pack(pady=(10, 0))
        
        # Detection results
        self.detection_frame = tk.Frame(self.content_frame, bg='#2c3e50')
        self.detection_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
    
    def show_step_2(self) -> None:
        """Show step 2: Template selection."""
        self.clear_content()
        self.title_label.config(text="Step 2: Choose Server Template")
        
        # Template categories
        categories = self.template_manager.get_categories()
        templates = self.template_manager.get_all_templates()
        
        # Create notebook for categories
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        self.template_var = tk.StringVar(value=self.wizard_data['template_id'])
        
        for category_id, category_info in categories.items():
            # Create tab for each category
            tab_frame = tk.Frame(notebook, bg='#2c3e50')
            notebook.add(tab_frame, text=f"{category_info['icon']} {category_info['name']}")
            
            # Scrollable frame for templates
            canvas = tk.Canvas(tab_frame, bg='#2c3e50')
            scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#2c3e50')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add templates for this category
            category_templates = {k: v for k, v in templates.items() if v.get('category') == category_id}
            
            for template_id, template_config in category_templates.items():
                template_frame = tk.Frame(scrollable_frame, bg='#34495e', relief=tk.RAISED, bd=1)
                template_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Radio button
                radio = tk.Radiobutton(
                    template_frame,
                    text=template_config['name'],
                    variable=self.template_var,
                    value=template_id,
                    font=('Arial', 11, 'bold'),
                    fg='#ecf0f1',
                    bg='#34495e',
                    selectcolor='#3498db',
                    command=self.on_template_select
                )
                radio.pack(anchor=tk.W, padx=10, pady=(10, 5))
                
                # Description
                desc_label = tk.Label(
                    template_frame,
                    text=template_config.get('description', ''),
                    font=('Arial', 9),
                    fg='#ecf0f1',
                    bg='#34495e',
                    wraplength=700,
                    justify=tk.LEFT
                )
                desc_label.pack(anchor=tk.W, padx=30, pady=(0, 10))
    
    def show_step_3(self) -> None:
        """Show step 3: Configuration details."""
        self.clear_content()
        self.title_label.config(text="Step 3: Configure Server Details")
        
        # Get selected template
        template = self.template_manager.get_template(self.wizard_data['template_id'])
        
        # Server name
        name_frame = tk.Frame(self.content_frame, bg='#2c3e50')
        name_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            name_frame,
            text="Server Name:",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        self.name_entry = tk.Entry(
            name_frame,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.name_entry.pack(fill=tk.X, pady=(5, 0))
        self.name_entry.insert(0, self.wizard_data['name'])
        
        # Port (optional)
        port_frame = tk.Frame(self.content_frame, bg='#2c3e50')
        port_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            port_frame,
            text="Port (Optional):",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        port_info = f"Default: {template.get('default_port', 'None')}" if template else "Default: None"
        tk.Label(
            port_frame,
            text=port_info,
            font=('Arial', 9),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        self.port_entry = tk.Entry(
            port_frame,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.port_entry.pack(fill=tk.X, pady=(5, 0))
        self.port_entry.insert(0, self.wizard_data['port'])
        
        # Command
        command_frame = tk.Frame(self.content_frame, bg='#2c3e50')
        command_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            command_frame,
            text="Start Command:",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        command_info = f"Default: {template.get('default_command', '')}" if template else "Default: None"
        tk.Label(
            command_frame,
            text=command_info,
            font=('Arial', 9),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        self.command_entry = tk.Entry(
            command_frame,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.command_entry.pack(fill=tk.X, pady=(5, 0))
        self.command_entry.insert(0, self.wizard_data['command'])
        
        # Description
        desc_frame = tk.Frame(self.content_frame, bg='#2c3e50')
        desc_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            desc_frame,
            text="Description (Optional):",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        self.desc_entry = tk.Entry(
            desc_frame,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.desc_entry.pack(fill=tk.X, pady=(5, 0))
        self.desc_entry.insert(0, self.wizard_data['description'])
        
        # Update next button to finish
        self.next_button.config(text="Create Server", bg='#27ae60')
    
    def clear_content(self) -> None:
        """Clear content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def browse_directory(self) -> None:
        """Browse for project directory."""
        directory = filedialog.askdirectory(
            title="Select Project Directory",
            initialdir=self.wizard_data['project_path'] or os.getcwd()
        )
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)
            self.wizard_data['project_path'] = directory
    
    def auto_detect(self) -> None:
        """Auto-detect project type."""
        project_path = self.path_entry.get().strip()
        if not project_path:
            messagebox.showwarning("Warning", "Please select a project directory first.")
            return
        
        if not os.path.exists(project_path):
            messagebox.showerror("Error", "Selected directory does not exist.")
            return
        
        # Clear previous results
        for widget in self.detection_frame.winfo_children():
            widget.destroy()
        
        # Detect project types
        detected = self.template_manager.detect_project_type(project_path)
        
        if not detected:
            tk.Label(
                self.detection_frame,
                text="❌ No specific project type detected. You can use Custom template.",
                font=('Arial', 10),
                fg='#e67e22',
                bg='#2c3e50'
            ).pack(pady=10)
            return
        
        # Show detection results
        tk.Label(
            self.detection_frame,
            text="🎯 Detected Project Types:",
            font=('Arial', 12, 'bold'),
            fg='#27ae60',
            bg='#2c3e50'
        ).pack(anchor=tk.W, pady=(10, 5))
        
        for i, (template_id, template_config, confidence) in enumerate(detected[:3]):
            confidence_percent = int(confidence * 100)
            result_text = f"• {template_config['name']} ({confidence_percent}% match)"
            
            color = '#27ae60' if i == 0 else '#f39c12' if i == 1 else '#95a5a6'
            
            tk.Label(
                self.detection_frame,
                text=result_text,
                font=('Arial', 10),
                fg=color,
                bg='#2c3e50'
            ).pack(anchor=tk.W, padx=20)
        
        # Auto-select best match
        if detected:
            best_match = detected[0]
            self.wizard_data['template_id'] = best_match[0]
            
            # Auto-fill suggested config
            suggested = self.template_manager.get_suggested_config(project_path, best_match[0])
            self.wizard_data.update(suggested)
    
    def on_template_select(self) -> None:
        """Handle template selection."""
        template_id = self.template_var.get()
        self.wizard_data['template_id'] = template_id
        
        # Update suggested config
        if self.wizard_data['project_path']:
            suggested = self.template_manager.get_suggested_config(
                self.wizard_data['project_path'], 
                template_id
            )
            # Only update if not already set by user
            if not self.wizard_data['command']:
                self.wizard_data['command'] = suggested.get('command', '')
            if not self.wizard_data['port']:
                self.wizard_data['port'] = str(suggested.get('port', '')) if suggested.get('port') else ''
    
    def next_step(self) -> None:
        """Go to next step."""
        if self.current_step == 0:
            # Validate step 1
            project_path = self.path_entry.get().strip()
            if not project_path:
                messagebox.showerror("Error", "Please select a project directory.")
                return
            if not os.path.exists(project_path):
                messagebox.showerror("Error", "Selected directory does not exist.")
                return
            
            self.wizard_data['project_path'] = project_path
            self.current_step = 1
            self.show_step_2()
            self.back_button.config(state=tk.NORMAL)
            
        elif self.current_step == 1:
            # Validate step 2
            template_id = self.template_var.get()
            if not template_id:
                messagebox.showerror("Error", "Please select a server template.")
                return
            
            self.wizard_data['template_id'] = template_id
            self.current_step = 2
            self.show_step_3()
            
        elif self.current_step == 2:
            # Validate step 3 and finish
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a server name.")
                return
            
            port = self.port_entry.get().strip()
            if port:
                try:
                    port_num = int(port)
                    if port_num < 1 or port_num > 65535:
                        raise ValueError("Port out of range")
                except ValueError:
                    messagebox.showerror("Error", "Port must be a number between 1 and 65535!")
                    return
            
            command = self.command_entry.get().strip()
            if not command:
                messagebox.showerror("Error", "Please enter a start command.")
                return
            
            # Validate project path with template
            is_valid, error_msg = self.template_manager.validate_project_path(
                self.wizard_data['project_path'], 
                self.wizard_data['template_id']
            )
            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return
            
            # Save final data
            self.wizard_data.update({
                'name': name,
                'port': port,
                'command': command,
                'description': self.desc_entry.get().strip()
            })
            
            self.result = self.wizard_data
            self.dialog.destroy()
            return
        
        self.update_progress()
    
    def previous_step(self) -> None:
        """Go to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            
            if self.current_step == 0:
                self.show_step_1()
                self.back_button.config(state=tk.DISABLED)
            elif self.current_step == 1:
                self.show_step_2()
                self.next_button.config(text="Next →", bg='#3498db')
            
            self.update_progress()
    
    def cancel(self) -> None:
        """Cancel wizard."""
        self.result = None
        self.dialog.destroy()


class UpdateDialog:
    """Dialog for displaying update information."""
    
    def __init__(self, parent: tk.Widget, update_info: UpdateInfo, current_version: str):
        """Initialize update dialog.
        
        Args:
            parent: Parent widget
            update_info: Update information
            current_version: Current application version
        """
        self.update_info = update_info
        self.current_version = current_version
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Update Available")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg='#2c3e50')
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_dialog_ui()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_dialog_ui(self) -> None:
        """Setup dialog UI components."""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Update icon (using text for now)
        update_icon = tk.Label(
            title_frame,
            text="🔄",
            font=("Arial", 24),
            bg='#2c3e50',
            fg='#3498db'
        )
        update_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title text
        title_text = tk.Label(
            title_frame,
            text="Update Available!",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_text.pack(side=tk.LEFT)
        
        # Version info frame
        version_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        version_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Current version
        current_label = tk.Label(
            version_frame,
            text=f"Current Version: {self.current_version}",
            font=("Arial", 10),
            bg='#34495e',
            fg='#ecf0f1'
        )
        current_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # New version
        new_label = tk.Label(
            version_frame,
            text=f"New Version: {self.update_info.version}",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#2ecc71'
        )
        new_label.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Release notes frame
        notes_frame = tk.Frame(main_frame, bg='#2c3e50')
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Release notes label
        notes_label = tk.Label(
            notes_frame,
            text="Release Notes:",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        notes_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Release notes text
        notes_text = scrolledtext.ScrolledText(
            notes_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=("Consolas", 9),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1',
            selectbackground='#3498db',
            state=tk.DISABLED
        )
        notes_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert release notes
        notes_text.config(state=tk.NORMAL)
        notes_text.insert(tk.END, self.update_info.release_notes or "No release notes available.")
        notes_text.config(state=tk.DISABLED)
        
        # Published date
        if self.update_info.published_at:
            try:
                from datetime import datetime
                published_date = datetime.fromisoformat(
                    self.update_info.published_at.replace('Z', '+00:00')
                ).strftime('%B %d, %Y')
                
                date_label = tk.Label(
                    notes_frame,
                    text=f"Published: {published_date}",
                    font=("Arial", 9),
                    bg='#2c3e50',
                    fg='#95a5a6'
                )
                date_label.pack(anchor=tk.W, pady=(10, 0))
            except:
                pass
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Download button
        download_button = tk.Button(
            buttons_frame,
            text="Download Update",
            font=("Arial", 10, "bold"),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.download_update,
            cursor='hand2'
        )
        download_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # View on GitHub button
        github_button = tk.Button(
            buttons_frame,
            text="View on GitHub",
            font=("Arial", 10),
            bg='#34495e',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.view_on_github,
            cursor='hand2'
        )
        github_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Later button
        later_button = tk.Button(
            buttons_frame,
            text="Later",
            font=("Arial", 10),
            bg='#7f8c8d',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.dialog.destroy,
            cursor='hand2'
        )
        later_button.pack(side=tk.LEFT)
    
    def download_update(self) -> None:
        """Open download URL in browser."""
        try:
            webbrowser.open(self.update_info.download_url)
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open download URL: {e}")
    
    def view_on_github(self) -> None:
        """Open GitHub repository in browser."""
        try:
            github_url = f"https://github.com/idpcks/DevServerManager/releases/tag/{self.update_info.version}"
            webbrowser.open(github_url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open GitHub: {e}")


class NoUpdateDialog:
    """Dialog for when no update is available."""
    
    def __init__(self, parent: tk.Widget, current_version: str):
        """Initialize no update dialog.
        
        Args:
            parent: Parent widget
            current_version: Current application version
        """
        self.current_version = current_version
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Check for Updates")
        self.dialog.geometry("450x250")
        self.dialog.configure(bg='#2c3e50')
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 100,
            parent.winfo_rooty() + 100
        ))
        
        self.setup_dialog_ui()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_dialog_ui(self) -> None:
        """Setup dialog UI components."""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#2c3e50', padx=40, pady=40)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon frame
        icon_frame = tk.Frame(main_frame, bg='#2c3e50')
        icon_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Icon
        icon_label = tk.Label(
            icon_frame,
            text="✅",
            font=("Arial", 36),
            bg='#2c3e50',
            fg='#2ecc71'
        )
        icon_label.pack()
        
        # Title frame
        title_frame = tk.Frame(main_frame, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        title_label = tk.Label(
            title_frame,
            text="You're up to date!",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack()
        
        # Version frame
        version_frame = tk.Frame(main_frame, bg='#2c3e50')
        version_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Version info
        version_label = tk.Label(
            version_frame,
            text=f"Current version: {self.current_version}",
            font=("Arial", 13),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        version_label.pack()
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill=tk.X)
        
        # OK button
        ok_button = tk.Button(
            button_frame,
            text="OK",
            font=("Arial", 11, "bold"),
            bg='#3498db',
            fg='white',
            relief=tk.FLAT,
            padx=40,
            pady=12,
            command=self.dialog.destroy,
            cursor='hand2'
        )
        ok_button.pack()


class ProgressDialog:
    """Dialog for showing download and installation progress."""
    
    def __init__(self, parent: tk.Widget, title: str = "Progress"):
        """Initialize progress dialog.
        
        Args:
            parent: Parent widget
            title: Dialog title
        """
        self.parent = parent
        self.dialog = None
        self.progress_var = None
        self.status_var = None
        self.speed_var = None
        self.eta_var = None
        self.cancel_callback = None
        
        self._create_dialog(title)
    
    def _create_dialog(self, title: str) -> None:
        """Create progress dialog."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(title)
        self.dialog.geometry("500x200")
        self.dialog.configure(bg='#2c3e50')
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 100,
            self.parent.winfo_rooty() + 100
        ))
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup progress dialog UI."""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#2c3e50', padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_var = tk.StringVar(value="Preparing...")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        status_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0.0)
        progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100.0,
            length=400,
            mode='determinate'
        )
        progress_bar.pack(pady=(0, 10))
        
        # Progress info frame
        info_frame = tk.Frame(main_frame, bg='#2c3e50')
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Speed info
        self.speed_var = tk.StringVar(value="")
        speed_label = tk.Label(
            info_frame,
            textvariable=self.speed_var,
            font=("Arial", 9),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        speed_label.pack(side=tk.LEFT)
        
        # ETA info
        self.eta_var = tk.StringVar(value="")
        eta_label = tk.Label(
            info_frame,
            textvariable=self.eta_var,
            font=("Arial", 9),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        eta_label.pack(side=tk.RIGHT)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        buttons_frame.pack(fill=tk.X)
        
        # Cancel button
        cancel_button = tk.Button(
            buttons_frame,
            text="Cancel",
            font=("Arial", 10),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self._on_cancel,
            cursor='hand2'
        )
        cancel_button.pack(side=tk.RIGHT)
    
    def update_progress(self, progress: DownloadProgress) -> None:
        """Update progress display.
        
        Args:
            progress: DownloadProgress object with progress info
        """
        if self.dialog and self.dialog.winfo_exists():
            self.progress_var.set(progress.percentage)
            
            # Update speed display
            if progress.speed > 0:
                speed_mb = progress.speed / (1024 * 1024)
                self.speed_var.set(f"Speed: {speed_mb:.1f} MB/s")
            else:
                self.speed_var.set("")
            
            # Update ETA display
            if progress.eta > 0:
                eta_minutes = progress.eta // 60
                eta_seconds = progress.eta % 60
                self.eta_var.set(f"ETA: {eta_minutes:02d}:{eta_seconds:02d}")
            else:
                self.eta_var.set("")
            
            self.dialog.update_idletasks()
    
    def update_status(self, status: str) -> None:
        """Update status message.
        
        Args:
            status: Status message
        """
        if self.dialog and self.dialog.winfo_exists():
            self.status_var.set(status)
            self.dialog.update_idletasks()
    
    def set_cancel_callback(self, callback: callable) -> None:
        """Set callback for cancel button.
        
        Args:
            callback: Function to call when cancel is clicked
        """
        self.cancel_callback = callback
    
    def _on_cancel(self) -> None:
        """Handle cancel button click."""
        if self.cancel_callback:
            self.cancel_callback()
        self.close()
    
    def close(self) -> None:
        """Close progress dialog."""
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.destroy()


class LiveUpdateDialog:
    """Dialog for live update with download and install."""
    
    def __init__(self, parent: tk.Widget, update_info: UpdateInfo, current_version: str):
        """Initialize live update dialog.
        
        Args:
            parent: Parent widget
            update_info: Update information
            current_version: Current application version
        """
        self.update_info = update_info
        self.current_version = current_version
        self.download_manager = DownloadManager()
        self.update_installer = UpdateInstaller()
        self.progress_dialog = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Live Update Available")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg='#2c3e50')
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_dialog_ui()
    
    def setup_dialog_ui(self) -> None:
        """Setup live update dialog UI."""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Update icon
        update_icon = tk.Label(
            title_frame,
            text="🔄",
            font=("Arial", 24),
            bg='#2c3e50',
            fg='#3498db'
        )
        update_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title text
        title_text = tk.Label(
            title_frame,
            text="Live Update Available!",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_text.pack(side=tk.LEFT)
        
        # Version info frame
        version_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        version_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Current version
        current_label = tk.Label(
            version_frame,
            text=f"Current Version: {self.current_version}",
            font=("Arial", 10),
            bg='#34495e',
            fg='#ecf0f1'
        )
        current_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # New version
        new_label = tk.Label(
            version_frame,
            text=f"New Version: {self.update_info.version}",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#2ecc71'
        )
        new_label.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Features frame
        features_frame = tk.Frame(main_frame, bg='#2c3e50')
        features_frame.pack(fill=tk.X, pady=(0, 20))
        
        features_label = tk.Label(
            features_frame,
            text="✨ Live Update Features:",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#f39c12'
        )
        features_label.pack(anchor=tk.W, pady=(0, 10))
        
        features_list = [
            "• Automatic download with progress tracking",
            "• Background installation process",
            "• Automatic application restart",
            "• Backup and rollback capability",
            "• File integrity verification"
        ]
        
        for feature in features_list:
            feature_label = tk.Label(
                features_frame,
                text=feature,
                font=("Arial", 10),
                bg='#2c3e50',
                fg='#ecf0f1'
            )
            feature_label.pack(anchor=tk.W, pady=2)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Live Update button
        live_update_button = tk.Button(
            buttons_frame,
            text="🚀 Live Update Now",
            font=("Arial", 11, "bold"),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            padx=25,
            pady=12,
            command=self.start_live_update,
            cursor='hand2'
        )
        live_update_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Manual Download button
        manual_button = tk.Button(
            buttons_frame,
            text="Manual Download",
            font=("Arial", 10),
            bg='#34495e',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.manual_download,
            cursor='hand2'
        )
        manual_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Later button
        later_button = tk.Button(
            buttons_frame,
            text="Later",
            font=("Arial", 10),
            bg='#7f8c8d',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.dialog.destroy,
            cursor='hand2'
        )
        later_button.pack(side=tk.LEFT)
    
    def start_live_update(self) -> None:
        """Start live update process."""
        try:
            # Create progress dialog
            self.progress_dialog = ProgressDialog(self.dialog, "Live Update Progress")
            self.progress_dialog.set_cancel_callback(self.cancel_update)
            
            # Start download
            self.download_manager.download_file(
                url=self.update_info.download_url,
                progress_callback=self.on_download_progress,
                completion_callback=self.on_download_complete
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start live update: {e}")
    
    def on_download_progress(self, progress: DownloadProgress) -> None:
        """Handle download progress updates."""
        if self.progress_dialog:
            self.progress_dialog.update_progress(progress)
            self.progress_dialog.update_status(f"Downloading update... {progress.percentage:.1f}%")
    
    def on_download_complete(self, filepath: str, success: bool) -> None:
        """Handle download completion."""
        if not success:
            if self.progress_dialog:
                self.progress_dialog.close()
            messagebox.showerror("Error", "Download failed!")
            return
        
        # Start installation
        if self.progress_dialog:
            self.progress_dialog.update_status("Installing update...")
            self.progress_dialog.update_progress(DownloadProgress(percentage=50.0))
        
        self.update_installer.install_update(
            new_exe_path=filepath,
            progress_callback=self.on_install_progress,
            completion_callback=self.on_install_complete
        )
    
    def on_install_progress(self, message: str, percentage: int) -> None:
        """Handle installation progress updates."""
        if self.progress_dialog:
            self.progress_dialog.update_status(message)
            self.progress_dialog.update_progress(DownloadProgress(percentage=float(percentage)))
    
    def on_install_complete(self, success: bool, message: str) -> None:
        """Handle installation completion."""
        if self.progress_dialog:
            self.progress_dialog.close()
        
        if success:
            messagebox.showinfo("Success", message)
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", message)
    
    def cancel_update(self) -> None:
        """Cancel update process."""
        self.download_manager.cancel_download()
        if self.progress_dialog:
            self.progress_dialog.close()
        messagebox.showinfo("Cancelled", "Update cancelled by user")
    
    def manual_download(self) -> None:
        """Open manual download in browser."""
        try:
            webbrowser.open(self.update_info.download_url)
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open download URL: {e}")