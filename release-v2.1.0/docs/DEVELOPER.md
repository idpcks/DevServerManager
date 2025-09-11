# 👨‍💻 Developer Guide - DevServer Manager

## 📋 Daftar Isi

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup Development](#setup-development)
- [Architecture](#architecture)
- [Core Components](#core-components)
- [Adding Features](#adding-features)
- [Testing](#testing)
- [Building](#building)
- [Contributing](#contributing)

---

## 🔍 Overview

DevServer Manager adalah aplikasi GUI modern yang dibangun dengan Python dan Tkinter. Aplikasi ini dirancang untuk mengelola multiple development servers dengan interface yang user-friendly.

### Tech Stack

- **Language**: Python 3.8+
- **GUI Framework**: Tkinter
- **System Tray**: pystray
- **Image Processing**: Pillow
- **Process Management**: psutil
- **File Monitoring**: watchdog
- **Configuration**: JSON
- **Build Tool**: PyInstaller

---

## 📁 Project Structure

```
runserver/
├── src/                          # Source code utama
│   ├── __init__.py              # Package initialization
│   ├── gui/                     # GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py       # Main window class
│   │   ├── dialogs.py           # Dialog windows
│   │   ├── widgets.py           # Custom widgets
│   │   ├── splashscreen.py      # Splash screen
│   │   └── base.py              # Base GUI classes
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   └── server_config.py     # Server configuration model
│   └── services/                # Business logic
│       ├── __init__.py
│       ├── server_manager.py    # Server management service
│       ├── config_manager.py    # Configuration management
│       ├── template_manager.py  # Template management
│       └── update_checker.py    # Update checking service
├── utils/                       # Utility functions
│   ├── __init__.py
│   ├── logger.py                # Logging utilities
│   ├── theme_manager.py         # Theme management
│   └── file_utils.py            # File utilities
├── config/                      # Configuration files
│   ├── server_config.json       # Server configurations
│   ├── server_templates.json    # Server templates
│   ├── theme_config.json        # Theme configurations
│   └── update_cache.json        # Update cache
├── assets/                      # Static assets
│   ├── app_icon.ico             # Application icon
│   ├── app_icon.svg             # SVG icon
│   └── logo.jpg                 # Logo image
├── docs/                        # Documentation
│   ├── USER_GUIDE.md            # User guide
│   ├── CONFIGURATION.md         # Configuration guide
│   ├── TROUBLESHOOTING.md       # Troubleshooting guide
│   └── DEVELOPER.md             # This file
├── tests/                       # Test files
├── logs/                        # Log files
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
├── setup.py                    # Setup script
└── build_executable.py         # Build script
```

---

## 🚀 Setup Development

### Prerequisites

- Python 3.8 atau lebih tinggi
- Git
- Code editor (VS Code, PyCharm, dll)

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/idpcks/DevServerManager.git
   cd DevServerManager/runserver
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python main.py
   ```

### Development Dependencies

```bash
# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Install build dependencies
pip install pyinstaller cx-Freeze
```

---

## 🏗️ Architecture

### MVC Pattern

Aplikasi menggunakan pattern Model-View-Controller:

- **Model**: `src/models/` - Data structures dan business logic
- **View**: `src/gui/` - User interface components
- **Controller**: `src/services/` - Business logic dan data management

### Component Architecture

```
MainWindow (GUI)
    ├── ServerManagerService (Business Logic)
    ├── ConfigManager (Configuration)
    ├── UpdateCheckerService (Updates)
    └── ThemeManager (UI Theming)
```

### Data Flow

1. **User Input** → GUI Components
2. **GUI Events** → Service Layer
3. **Service Layer** → Model Layer
4. **Model Changes** → GUI Updates
5. **Configuration** → File System

---

## 🔧 Core Components

### MainWindow (`src/gui/main_window.py`)

Main window class yang mengatur seluruh UI aplikasi.

**Key Methods**:
- `__init__()`: Initialize window dan components
- `_setup_ui()`: Setup user interface
- `_load_servers()`: Load server configurations
- `refresh_server_list()`: Refresh server display
- `start_server()`: Start specific server
- `stop_server()`: Stop specific server

**Key Features**:
- Responsive layout
- Theme support
- System tray integration
- Real-time logging

### ServerManagerService (`src/services/server_manager.py`)

Service untuk mengelola server processes.

**Key Methods**:
- `add_server()`: Add new server
- `remove_server()`: Remove server
- `start_server()`: Start server process
- `stop_server()`: Stop server process
- `get_all_servers()`: Get all servers

**Key Features**:
- Process management
- Port conflict detection
- Server status monitoring
- Error handling

### ConfigManager (`src/services/config_manager.py`)

Service untuk mengelola konfigurasi aplikasi.

**Key Methods**:
- `load_server_config()`: Load server configurations
- `save_server_config()`: Save server configurations
- `load_templates()`: Load server templates
- `save_templates()`: Save server templates

**Key Features**:
- JSON configuration management
- Template system
- Configuration validation
- Backup/restore

### ThemeManager (`utils/theme_manager.py`)

Utility untuk mengelola tema UI.

**Key Methods**:
- `set_theme()`: Set active theme
- `get_current_colors()`: Get current theme colors
- `apply_theme()`: Apply theme to widgets
- `load_theme()`: Load theme from config

**Key Features**:
- Multiple theme support
- Real-time theme switching
- Custom color schemes
- Persistent theme storage

---

## ➕ Adding Features

### Adding New Server Template

1. **Edit Template File**
   ```json
   // config/server_templates.json
   {
     "templates": {
       "new_template": {
         "name": "New Template",
         "description": "Description of new template",
         "command": "command with {port} placeholder",
         "default_port": 8000,
         "category": "Technology",
         "env_vars": {},
         "requirements": ["file1", "file2"]
       }
     }
   }
   ```

2. **Update Template Manager**
   ```python
   # src/services/template_manager.py
   def load_templates(self):
       # Add validation for new template
       pass
   ```

### Adding New GUI Component

1. **Create Widget Class**
   ```python
   # src/gui/widgets.py
   class NewWidget(tk.Frame):
       def __init__(self, parent, **kwargs):
           super().__init__(parent, **kwargs)
           self._setup_ui()
       
       def _setup_ui(self):
           # Setup widget UI
           pass
   ```

2. **Integrate with MainWindow**
   ```python
   # src/gui/main_window.py
   def _setup_ui(self):
       # Add new widget to UI
       self.new_widget = NewWidget(self.root)
       self.new_widget.pack()
   ```

### Adding New Service

1. **Create Service Class**
   ```python
   # src/services/new_service.py
   class NewService:
       def __init__(self):
           self.initialized = False
       
       def initialize(self):
           # Initialize service
           self.initialized = True
       
       def cleanup(self):
           # Cleanup resources
           self.initialized = False
   ```

2. **Integrate with MainWindow**
   ```python
   # src/gui/main_window.py
   def __init__(self, root):
       # Add new service
       self.new_service = NewService()
       self.new_service.initialize()
   ```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_server_manager.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── __init__.py
├── test_server_manager.py      # Server manager tests
├── test_config_manager.py      # Config manager tests
├── test_theme_manager.py       # Theme manager tests
└── test_gui_components.py      # GUI component tests
```

### Writing Tests

```python
# tests/test_server_manager.py
import pytest
from src.services.server_manager import ServerManagerService
from src.models.server_config import ServerConfig

class TestServerManager:
    def setup_method(self):
        self.service = ServerManagerService()
    
    def test_add_server(self):
        config = ServerConfig(
            name="test_server",
            path="/test/path",
            port="8000",
            command="python -m http.server"
        )
        
        result = self.service.add_server(config)
        assert result == True
        assert "test_server" in self.service.get_all_servers()
    
    def test_start_server(self):
        # Test server start functionality
        pass
    
    def test_stop_server(self):
        # Test server stop functionality
        pass
```

---

## 🔨 Building

### Building Executable

1. **Install Build Dependencies**
   ```bash
   pip install pyinstaller
   ```

2. **Run Build Script**
   ```bash
   python build_executable.py
   ```

3. **Output Files**
   ```
   dist/
   ├── DevServerManager.exe      # Main executable
   └── release/                  # Release package
       ├── DevServerManager.exe
       ├── README.md
       ├── requirements.txt
       └── config/
   ```

### Build Configuration

```python
# build_executable.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=DevServerManager',
    '--icon=assets/app_icon.ico',
    '--add-data=config;config',
    '--add-data=assets;assets',
    '--hidden-import=pystray',
    '--hidden-import=PIL',
])
```

### Release Process

1. **Update Version**
   ```python
   # src/__init__.py
   __version__ = "1.0.2"
   ```

2. **Update Changelog**
   ```markdown
   # CHANGELOG.md
   ## [1.0.2] - 2025-01-11
   - Added new feature
   - Fixed bug
   ```

3. **Build Release**
   ```bash
   python build_executable.py
   ```

4. **Create GitHub Release**
   - Upload files from `release/` folder
   - Add release notes
   - Tag version

---

## 🤝 Contributing

### Development Workflow

1. **Fork Repository**
   ```bash
   # Fork di GitHub, lalu clone
   git clone https://github.com/yourusername/DevServerManager.git
   cd DevServerManager/runserver
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

4. **Test Changes**
   ```bash
   pytest
   python main.py  # Manual testing
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/amazing-feature
   # Create Pull Request di GitHub
   ```

### Code Style

#### Python Style Guide
- Follow PEP 8
- Use type hints
- Write docstrings
- Use meaningful variable names

#### Example Code Style
```python
def start_server(self, server_name: str) -> bool:
    """Start a specific server.
    
    Args:
        server_name: Name of the server to start
        
    Returns:
        True if server started successfully, False otherwise
        
    Raises:
        ServerNotFoundError: If server doesn't exist
        PortInUseError: If port is already in use
    """
    try:
        # Implementation here
        return True
    except Exception as e:
        self.logger.error(f"Failed to start server {server_name}: {e}")
        return False
```

### Pull Request Guidelines

1. **Title**: Clear, descriptive title
2. **Description**: Explain what and why
3. **Tests**: Include tests for new features
4. **Documentation**: Update relevant docs
5. **Screenshots**: Include UI changes

### Issue Guidelines

1. **Bug Reports**:
   - Clear reproduction steps
   - Expected vs actual behavior
   - System information
   - Log files

2. **Feature Requests**:
   - Clear description
   - Use case
   - Proposed solution
   - Alternatives considered

---

## 📚 Additional Resources

### Documentation
- [Python Documentation](https://docs.python.org/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)

### Tools
- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [GitHub Desktop](https://desktop.github.com/)

### Community
- [GitHub Discussions](https://github.com/idpcks/DevServerManager/discussions)
- [Python Discord](https://discord.gg/python)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python)

---

**Last Updated**: 11 September 2025  
**Version**: 1.0.1  
**Developer**: idpcks
