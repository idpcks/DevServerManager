"""Base Classes and Interfaces

This module contains base classes and interfaces for GUI components.
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, List
from enum import Enum

from utils.logger import app_logger


class ComponentState(Enum):
    """Enumeration for component states."""
    IDLE = "idle"
    LOADING = "loading"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


class IThemeable(ABC):
    """Interface for themeable components."""
    
    @abstractmethod
    def apply_theme(self, theme_config: Dict[str, Any]) -> None:
        """Apply theme configuration to the component.
        
        Args:
            theme_config: Theme configuration dictionary
        """
        pass
    
    @abstractmethod
    def get_theme_properties(self) -> List[str]:
        """Get list of themeable properties.
        
        Returns:
            List of property names that can be themed
        """
        pass


class IConfigurable(ABC):
    """Interface for configurable components."""
    
    @abstractmethod
    def load_config(self, config: Dict[str, Any]) -> bool:
        """Load configuration for the component.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if configuration was loaded successfully
        """
        pass
    
    @abstractmethod
    def save_config(self) -> Dict[str, Any]:
        """Save current configuration.
        
        Returns:
            Configuration dictionary
        """
        pass
    
    @abstractmethod
    def reset_config(self) -> None:
        """Reset configuration to defaults."""
        pass


class IValidatable(ABC):
    """Interface for validatable components."""
    
    @abstractmethod
    def validate(self) -> tuple[bool, str]:
        """Validate component state.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    def get_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules for the component.
        
        Returns:
            Dictionary of validation rules
        """
        pass


class IObservable(ABC):
    """Interface for observable components that can notify observers."""
    
    def __init__(self):
        self._observers: List[Callable] = []
    
    def add_observer(self, observer: Callable) -> None:
        """Add an observer.
        
        Args:
            observer: Observer callback function
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer: Callable) -> None:
        """Remove an observer.
        
        Args:
            observer: Observer callback function
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self, event_type: str, data: Any = None) -> None:
        """Notify all observers of an event.
        
        Args:
            event_type: Type of event
            data: Event data
        """
        for observer in self._observers:
            try:
                observer(event_type, data)
            except Exception as e:
                app_logger.error(f"Error notifying observer: {e}")


class BaseWidget(tk.Frame, IThemeable, IConfigurable, IObservable):
    """Base class for all custom widgets."""
    
    def __init__(self, parent: tk.Widget, **kwargs):
        """Initialize base widget.
        
        Args:
            parent: Parent widget
            **kwargs: Additional keyword arguments
        """
        tk.Frame.__init__(self, parent, **kwargs)
        IObservable.__init__(self)
        
        self._state = ComponentState.IDLE
        self._config = {}
        self._theme_config = {}
        self._validation_errors = []
        
        # Default styling
        self.configure(bg='#34495e')
    
    @property
    def state(self) -> ComponentState:
        """Get current component state."""
        return self._state
    
    @state.setter
    def state(self, value: ComponentState) -> None:
        """Set component state.
        
        Args:
            value: New state
        """
        old_state = self._state
        self._state = value
        self._on_state_changed(old_state, value)
        self.notify_observers('state_changed', {'old': old_state, 'new': value})
    
    def _on_state_changed(self, old_state: ComponentState, new_state: ComponentState) -> None:
        """Handle state change.
        
        Args:
            old_state: Previous state
            new_state: New state
        """
        # Override in subclasses to handle state changes
        pass
    
    def set_loading(self, loading: bool = True) -> None:
        """Set loading state.
        
        Args:
            loading: Whether component is loading
        """
        self.state = ComponentState.LOADING if loading else ComponentState.IDLE
    
    def set_error(self, error_message: str = "") -> None:
        """Set error state.
        
        Args:
            error_message: Error message
        """
        self.state = ComponentState.ERROR
        if error_message:
            self._validation_errors.append(error_message)
    
    def clear_errors(self) -> None:
        """Clear all errors."""
        self._validation_errors.clear()
        if self.state == ComponentState.ERROR:
            self.state = ComponentState.IDLE
    
    def get_errors(self) -> List[str]:
        """Get current validation errors.
        
        Returns:
            List of error messages
        """
        return self._validation_errors.copy()
    
    # IThemeable implementation
    def apply_theme(self, theme_config: Dict[str, Any]) -> None:
        """Apply theme configuration.
        
        Args:
            theme_config: Theme configuration
        """
        self._theme_config = theme_config.copy()
        
        # Apply basic theme properties
        if 'bg_color' in theme_config:
            self.configure(bg=theme_config['bg_color'])
        
        if 'fg_color' in theme_config:
            # Apply to child widgets that support foreground color
            for child in self.winfo_children():
                if hasattr(child, 'configure'):
                    try:
                        child.configure(fg=theme_config['fg_color'])
                    except tk.TclError:
                        pass  # Widget doesn't support fg color
    
    def get_theme_properties(self) -> List[str]:
        """Get themeable properties.
        
        Returns:
            List of themeable property names
        """
        return ['bg_color', 'fg_color', 'font_family', 'font_size']
    
    # IConfigurable implementation
    def load_config(self, config: Dict[str, Any]) -> bool:
        """Load configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if loaded successfully
        """
        try:
            self._config = config.copy()
            self._apply_config()
            return True
        except Exception as e:
            app_logger.error(f"Error loading config: {e}")
            return False
    
    def save_config(self) -> Dict[str, Any]:
        """Save current configuration.
        
        Returns:
            Configuration dictionary
        """
        return self._config.copy()
    
    def reset_config(self) -> None:
        """Reset configuration to defaults."""
        self._config.clear()
        self._apply_config()
    
    def _apply_config(self) -> None:
        """Apply current configuration."""
        # Override in subclasses to apply specific configuration
        pass


class BaseDialog(tk.Toplevel, IThemeable, IConfigurable, IValidatable):
    """Base class for dialog windows."""
    
    def __init__(self, parent: tk.Widget, title: str = "Dialog", 
                 modal: bool = True, **kwargs):
        """Initialize base dialog.
        
        Args:
            parent: Parent widget
            title: Dialog title
            modal: Whether dialog is modal
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.result = None
        self._config = {}
        self._theme_config = {}
        
        # Setup dialog
        self.title(title)
        self.transient(parent)
        
        if modal:
            self.grab_set()
        
        # Center dialog
        self._center_dialog()
        
        # Setup UI
        self._setup_ui()
        
        # Bind events
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.bind('<Escape>', lambda e: self._on_cancel())
    
    def _center_dialog(self) -> None:
        """Center dialog on parent window."""
        try:
            self.update_idletasks()
            
            # Get dialog size
            width = self.winfo_width()
            height = self.winfo_height()
            
            # Get parent position and size
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            # Calculate center position
            x = parent_x + (parent_width // 2) - (width // 2)
            y = parent_y + (parent_height // 2) - (height // 2)
            
            self.geometry(f"{width}x{height}+{x}+{y}")
            
        except Exception as e:
            app_logger.error(f"Error centering dialog: {e}")
    
    @abstractmethod
    def _setup_ui(self) -> None:
        """Setup dialog UI. Must be implemented by subclasses."""
        pass
    
    def _on_ok(self) -> None:
        """Handle OK button click."""
        is_valid, error_msg = self.validate()
        if is_valid:
            self.result = self._get_result()
            self.destroy()
        else:
            self._show_validation_error(error_msg)
    
    def _on_cancel(self) -> None:
        """Handle Cancel button click."""
        self.result = None
        self.destroy()
    
    @abstractmethod
    def _get_result(self) -> Any:
        """Get dialog result. Must be implemented by subclasses."""
        pass
    
    def _show_validation_error(self, message: str) -> None:
        """Show validation error message.
        
        Args:
            message: Error message
        """
        from tkinter import messagebox
        messagebox.showerror("Validation Error", message, parent=self)
    
    # IThemeable implementation
    def apply_theme(self, theme_config: Dict[str, Any]) -> None:
        """Apply theme configuration.
        
        Args:
            theme_config: Theme configuration
        """
        self._theme_config = theme_config.copy()
        
        if 'bg_color' in theme_config:
            self.configure(bg=theme_config['bg_color'])
    
    def get_theme_properties(self) -> List[str]:
        """Get themeable properties.
        
        Returns:
            List of themeable property names
        """
        return ['bg_color', 'fg_color']
    
    # IConfigurable implementation
    def load_config(self, config: Dict[str, Any]) -> bool:
        """Load configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if loaded successfully
        """
        try:
            self._config = config.copy()
            return True
        except Exception as e:
            app_logger.error(f"Error loading dialog config: {e}")
            return False
    
    def save_config(self) -> Dict[str, Any]:
        """Save current configuration.
        
        Returns:
            Configuration dictionary
        """
        return self._config.copy()
    
    def reset_config(self) -> None:
        """Reset configuration to defaults."""
        self._config.clear()


class BaseService(ABC, IObservable):
    """Base class for service layer components."""
    
    def __init__(self):
        """Initialize base service."""
        IObservable.__init__(self)
        self._initialized = False
        self._config = {}
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the service.
        
        Returns:
            True if initialization was successful
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup service resources."""
        pass
    
    @property
    def is_initialized(self) -> bool:
        """Check if service is initialized.
        
        Returns:
            True if service is initialized
        """
        return self._initialized
    
    def _set_initialized(self, value: bool) -> None:
        """Set initialization status.
        
        Args:
            value: Initialization status
        """
        self._initialized = value
        self.notify_observers('initialized_changed', value)


class EventManager:
    """Centralized event management system."""
    
    def __init__(self):
        """Initialize event manager."""
        self._handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            handler: Event handler function
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            handler: Event handler function
        """
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
    
    def emit(self, event_type: str, data: Any = None) -> None:
        """Emit an event to all subscribers.
        
        Args:
            event_type: Type of event to emit
            data: Event data
        """
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    app_logger.error(f"Error in event handler for {event_type}: {e}")
    
    def clear_handlers(self, event_type: Optional[str] = None) -> None:
        """Clear event handlers.
        
        Args:
            event_type: Specific event type to clear, or None to clear all
        """
        if event_type:
            if event_type in self._handlers:
                self._handlers[event_type].clear()
        else:
            self._handlers.clear()


# Global event manager instance
event_manager = EventManager()