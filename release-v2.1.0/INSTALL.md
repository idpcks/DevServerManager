# DevServer Manager v2.1.0 - Installation Guide

## 🚀 Quick Start

### Requirements
- Python 3.8 or higher
- Windows 10/11 (recommended)

### Installation Steps

1. **Extract Files**
   ```bash
   # Extract the downloaded zip file to your desired location
   # Example: C:\DevServerManager\
   ```

2. **Install Dependencies**
   ```bash
   # Open Command Prompt in the extracted directory
   cd path\to\DevServerManager
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   python main.py
   ```

### Building Executable (Optional)

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_executable.py
```

The executable will be created in the `dist/` directory.

### Features
- ✅ Server management for multiple development frameworks
- ✅ Backup and import configurations  
- ✅ Live update system
- ✅ System tray integration
- ✅ Modern GUI interface

### Documentation
- **User Guide**: docs/USER_GUIDE.md
- **Backup Guide**: docs/BACKUP_IMPORT_GUIDE.md
- **Live Update Guide**: docs/LIVE_UPDATE_README.md
- **Developer Guide**: docs/DEVELOPER.md

### Support
- GitHub Issues: https://github.com/idpcks/DevServerManager/issues
- Email: idpcks.container103@slmail.me

---
**Version**: 2.1.0  
**Date**: 2025-09-11
