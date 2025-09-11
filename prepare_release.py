#!/usr/bin/env python3
"""
Simplified release preparation script
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def get_version():
    """Get version from setup.py"""
    try:
        with open('setup.py', 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'version=' in line:
                    version = line.split('version=')[1].split(',')[0].strip().strip('"\'')
                    return version
    except Exception:
        pass
    return "2.1.0"

def create_source_release_package():
    """Create source code release package"""
    version = get_version()
    print(f"Creating source release package for version {version}...")
    
    # Create release directory
    release_dir = f"release-v{version}"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    os.makedirs(release_dir)
    
    # Files and directories to include in source release
    items_to_copy = [
        # Essential files
        "main.py",
        "setup.py",
        "pyproject.toml", 
        "requirements.txt",
        "README.md",
        "CHANGELOG.md",
        "RELEASE_NOTES_v2.1.0.md",
        "LICENSE",
        "build_executable.py",
        "backup_config.py",
        
        # Directories
        "src",
        "utils", 
        "config",
        "assets",
        "docs",
        "scripts"
    ]
    
    copied_items = []
    for item in items_to_copy:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, os.path.join(release_dir, item))
                print(f"Copied directory {item}")
            else:
                shutil.copy2(item, release_dir)
                print(f"Copied file {item}")
            copied_items.append(item)
        else:
            print(f"Warning: {item} not found, skipping...")
    
    # Create installation guide
    install_guide = f"""# DevServer Manager v{version} - Installation Guide

## 🚀 Quick Start

### Requirements
- Python 3.8 or higher
- Windows 10/11 (recommended)

### Installation Steps

1. **Extract Files**
   ```bash
   # Extract the downloaded zip file to your desired location
   # Example: C:\\DevServerManager\\
   ```

2. **Install Dependencies**
   ```bash
   # Open Command Prompt in the extracted directory
   cd path\\to\\DevServerManager
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
**Version**: {version}  
**Date**: {datetime.now().strftime('%Y-%m-%d')}
"""
    
    with open(os.path.join(release_dir, "INSTALL.md"), 'w', encoding='utf-8') as f:
        f.write(install_guide)
    
    # Create ZIP package
    zip_filename = f"DevServerManager-v{version}-source.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arc_name)
                
    print(f"\\nSource release package created: {zip_filename}")
    print(f"Release directory: {release_dir}/")
    
    # Print summary
    print(f"\\n{'='*50}")
    print(f"RELEASE SUMMARY")
    print(f"{'='*50}")
    print(f"Version: {version}")
    print(f"Package: {zip_filename}")
    print(f"Items included: {len(copied_items)}")
    print(f"Size: {os.path.getsize(zip_filename) / 1024 / 1024:.2f} MB")
    print(f"\\nNext steps:")
    print(f"1. Upload {zip_filename} to GitHub Releases")
    print(f"2. Use RELEASE_NOTES_v{version}.md as release description")
    print(f"3. Tag the release: git tag v{version}")
    print(f"4. Push tags: git push origin v{version}")
    
    return zip_filename

if __name__ == "__main__":
    create_source_release_package()