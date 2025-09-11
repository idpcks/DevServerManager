# Release & Distribution Guide

## Overview

Panduan lengkap untuk membuat dan mendistribusikan release DevServer Manager.

## 🚀 Quick Start

### Automated Release (Recommended)
1. **Update Version**: Edit `setup.py` dan ubah version number
2. **Create Release**: Jalankan release script:
   ```bash
   python scripts/create_release.py 1.0.0
   ```
3. **Push Changes**: Push ke GitHub:
   ```bash
   git push origin main
   git push origin --tags
   ```
4. **GitHub Actions**: Workflow akan otomatis membuat release

### Manual Release
1. **Build Executable**:
   ```bash
   python build_executable.py
   ```
2. **Create Release Package**:
   ```bash
   python scripts/create_release.py 1.0.0 --skip-tag
   ```
3. **Upload to GitHub**: Upload ZIP file ke GitHub Releases

## 📋 Release Process

### 1. Pre-Release Checklist
- [ ] Update version di `setup.py`
- [ ] Update `CHANGELOG.md` dengan fitur/fixes baru
- [ ] Test aplikasi secara menyeluruh
- [ ] Pastikan semua tests pass
- [ ] Update dokumentasi jika diperlukan
- [ ] Buat release notes

### 2. Version Numbering
Gunakan [Semantic Versioning](https://semver.org/):
- **MAJOR** (X.0.0): Incompatible API changes
- **MINOR** (X.Y.0): New functionality, backwards compatible
- **PATCH** (X.Y.Z): Bug fixes, backwards compatible

### 3. Release Package Contents
```
DevServerManager-vX.Y.Z-Windows.zip
├── DevServerManager.exe              # Main executable
├── README.md                         # Documentation
├── PANDUAN_PENGGUNAAN.txt           # User guide (Indonesian)
├── requirements.txt                  # Dependencies info
├── server_templates.json            # Server templates
├── server_config_example.json       # Example configuration
└── CHANGELOG.md                     # Version history
```

## 🔧 Build Configuration

### PyInstaller Options
```python
# Key options used:
--onefile          # Single executable
--windowed         # No console window
--icon             # Custom application icon
--add-data         # Include data files
--hidden-import    # Ensure all dependencies
```

### Included Dependencies
- tkinter (GUI framework)
- PIL/Pillow (Image processing)
- pystray (System tray)
- psutil (Process management)
- All custom modules

## 📦 Distribution Methods

### 1. GitHub Releases (Recommended)
- **Professional**: Metode distribusi paling profesional
- **User Friendly**: User tidak perlu install Python
- **Secure**: File di-scan oleh VirusTotal
- **Easy**: Download dan run langsung

### 2. System Requirements untuk User
- **OS**: Windows 10/11 (64-bit)
- **RAM**: Minimum 4GB
- **Storage**: 100MB free space
- **Network**: Internet connection (untuk server management)

### 3. User Installation
1. **Download**: Download dari GitHub Releases
2. **Extract**: Extract ZIP file
3. **Run**: Double-click `DevServerManager.exe`

## 🚨 Troubleshooting

### Common Issues
**Build Fails:**
- Check Python version (3.8+ required)
- Ensure all dependencies are installed
- Verify PyInstaller is working: `pyinstaller --version`

**Release Script Fails:**
- Ensure git is configured properly
- Check that all files are committed
- Verify version format is correct

**Executable Issues:**
- Test on clean Windows machine
- Check Windows Defender settings
- Verify all dependencies are included

### Debug Mode
```bash
# Run build with verbose output
python build_executable.py --verbose

# Check PyInstaller logs
pyinstaller --log-level DEBUG main.py
```

## 🔄 Rollback Process

Jika release memiliki masalah kritis:
1. **Mark as Pre-release**: Edit release di GitHub
2. **Create Hotfix**: Buat patch version baru
3. **Communicate**: Update users tentang masalah
4. **Fix and Release**: Deploy fixed version dengan cepat

## 📊 Release Metrics

Track release success:
- **Download Count**: Monitor di GitHub Releases
- **Issue Reports**: Track issues baru setelah release
- **User Feedback**: Monitor discussions dan comments
- **Build Success**: Check GitHub Actions status

## 🔗 Additional Resources

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)

## 📞 Support

Untuk masalah release:
- **GitHub Issues**: [Create an issue](https://github.com/idpcks/DevServerManager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/idpcks/DevServerManager/discussions)
- **Email**: idpcks.container103@slmail.me

---

**Last Updated**: 11 September 2025 
**Version**: 1.0.0