# DevServer Manager

🚀 **Modern GUI Application for Managing Development Servers**

A comprehensive solution for managing multiple development servers with an intuitive interface, featuring backup/import functionality, live updates, and support for various frameworks.

## ✨ Features

- **🎯 Multi-Framework Support**: Laravel, Node.js, Python, Go, .NET, and more
- **📦 Backup & Import**: Export/import configurations with preview
- **🚀 Live Updates**: Automatic application updates with progress tracking
- **🎨 Modern UI**: Professional interface with system tray integration
- **⚡ Auto-Detection**: Automatically detects project types
- **🔧 Template System**: Pre-configured server templates
- **📊 Real-time Monitoring**: Server status and process management

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/idpcks/DevServerManager.git
cd DevServerManager/runserver

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Requirements

- Python 3.8+
- Windows 10/11 (recommended)
- 256MB RAM minimum
- 100MB storage space

## 📋 Basic Usage

1. **Launch**: Run `python main.py`
2. **Add Server**: Use templates or custom configuration
3. **Start/Stop**: Manage servers with one click
4. **Backup**: Export configurations for backup
5. **Update**: Use live update feature for latest version

## 🔒 Security & Antivirus Notice

### ⚠️ False Positive Detection
Some antivirus software may flag the executable as suspicious. This is a **known false positive** common with PyInstaller applications.

**Why this happens:**
- Unsigned executable (no code signing certificate yet)
- Packed binary format triggers heuristic detection
- New application without established reputation

**✅ Recommended Safe Installation:**
```bash
# Install from source (100% safe)
git clone https://github.com/idpcks/DevServerManager.git
cd DevServerManager/runserver
pip install -r requirements.txt
python main.py
```

**🛡️ Verification:**
- **Open Source**: All code is publicly auditable
- **No Network Data**: Application doesn't send data to external servers
- **Local Only**: All operations are performed locally

## 🔧 Configuration

Server configurations are stored in `config/server_config.json`. The application supports:

- **Templates**: Pre-configured for popular frameworks
- **Custom Commands**: Define your own server commands
- **Environment Variables**: Framework-specific configurations
- **Port Management**: Automatic port conflict detection

## 📦 Core Files Structure

```
DevServerManager/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── setup.py            # Package configuration
├── pyproject.toml      # Project metadata
├── src/                # Core source code
│   ├── gui/           # User interface components
│   ├── services/      # Business logic services
│   └── models/        # Data models
├── utils/              # Utility functions
├── config/             # Configuration files
├── assets/             # Application assets
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/idpcks/DevServerManager
- **Issues**: https://github.com/idpcks/DevServerManager/issues
- **Releases**: https://github.com/idpcks/DevServerManager/releases

## 📧 Support

- **Email**: idpcks.container103@slmail.me
- **GitHub Issues**: For bug reports and feature requests

---

**Made with ❤️ for developers by developers**