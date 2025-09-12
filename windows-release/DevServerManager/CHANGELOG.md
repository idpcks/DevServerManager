<<<<<<< HEAD
## [v2.1.0] - 2025-09-11
=======
## [v2.1.1] - 2025-09-11 - **Current Latest Release**

> **DevServer Manager Version 2.x Series** - Complete application rewrite with modern architecture and enhanced features. This version series represents a major evolution from previous versions.
>>>>>>> main

### Added
- New features and improvements

### Changed
- Updated dependencies and configurations

### Fixed
- Bug fixes and stability improvements

### Security
- Security updates and patches

---

# Changelog

<<<<<<< HEAD
All notable changes to this project will be documented in this file.
=======
All notable changes to DevServer Manager will be documented in this file.

> **Current Major Version: 2.x** - This represents a complete rewrite of the application with modern architecture, enhanced features, and improved user experience. Users should download version 2.x releases for the latest functionality.
>>>>>>> main

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<<<<<<< HEAD
=======
---

>>>>>>> main
## [Unreleased]

### Planning
- Future enhancements and features

<<<<<<< HEAD
## [2.1.1] - 2025-09-11 - **Security & Build Update**

### Added
- 🛡️ **Antivirus False Positive Solutions**: Comprehensive guide for handling antivirus detection issues
- 📋 **Security Documentation**: Clear explanation of false positive causes and solutions
- 🔧 **Enhanced Build Process**: Optimized PyInstaller settings to reduce false positives
  - Added `--noupx` flag to disable compression that triggers detection
  - Added `--clean` and `--strip` flags for cleaner builds
  - Excluded unnecessary modules that increase suspicion
  - Enhanced hidden imports for better compatibility

### Changed
- 📖 **README Security Section**: Added antivirus notice and safe installation instructions
- 🏗️ **Build Configuration**: Updated build script with antivirus-optimized settings
- 🛡️ **User Communication**: Clear guidance on false positive handling

### Fixed
- 🚨 **Antivirus Detection**: Implemented multiple strategies to reduce false positive rates
- 📦 **Build Optimization**: Reduced executable size and suspicious patterns
- 🔒 **Security Transparency**: Enhanced documentation about application safety

### Security
- ✅ **False Positive Mitigation**: Multiple strategies to reduce antivirus false positives
- 📝 **Transparency**: Clear documentation about why detection occurs
- 🛡️ **Safe Installation**: Provided source code installation as primary safe method

=======
>>>>>>> main
## [2.1.0] - 2025-09-11 - **Current Release**

### Added
- ✨ **Comprehensive Backup & Import System**: User-friendly backup/import functionality with JSON format
  - BackupExportDialog for creating configuration backups
  - ImportRestoreDialog for importing settings with validation
  - Preview functionality for backup contents
  - UI integration with File menu and toolbar buttons
- 🚀 **Live Update System**: Automatic application updates with progress tracking
  - DownloadManager for background downloads with progress
  - UpdateInstaller for automatic installation with backup
  - Progress dialogs with real-time speed and ETA information
  - Automatic rollback on update failure
- 📚 **Enhanced Documentation**: Comprehensive guides and user documentation
  - Live Update user guide (Indonesian) and technical documentation (English)
  - Backup & Import guide with team collaboration workflows
  - Improved documentation organization in /docs folder
  - Elimination of documentation redundancy
- 🛠️ **Configuration Management**: Enhanced configuration handling and migration
  - Automatic configuration migration for backward compatibility
  - Cross-platform JSON backup format
  - Theme settings backup and restore
  - Server configuration validation and preview
- 🎯 **Core Features**: Complete development server management
  - Modern GUI interface with Tkinter
  - Server template system for various technologies (Laravel, Node.js, Python, Go, .NET)
  - Auto-detection of project types based on file markers
  - Real-time server status monitoring
  - Process management with graceful shutdown
  - System tray integration
  - Custom command execution
  - Advanced logging system with color coding
  - Theme customization system
  - Environment variables support
  - Multi-threading for non-blocking UI

### Changed
- 📖 **Documentation Structure**: Reorganized documentation files in dedicated /docs folder
  - Moved LIVE_UPDATE_README.md and BACKUP_IMPORT_GUIDE.md to docs/
  - Updated INDEX.md with clear documentation hierarchy
  - Improved cross-references between documentation files
- 🎨 **User Experience**: Enhanced UI/UX for backup and update operations
  - Professional dialog designs with consistent styling
  - Real-time progress feedback for all operations
  - User-friendly error messages and recovery options
- 🏗️ **System Architecture**: Improved modularity and maintainability
  - Enhanced ConfigManager integration
  - Better separation of concerns in backup/import functionality
  - Improved error handling and validation
  - Startup performance improvements
  - Enhanced memory management

### Fixed
- 🐛 **Unicode Encoding Issues**: Fixed Windows-specific Unicode errors
  - Resolved emoji character encoding in Windows Command Prompt
  - Added UTF-8 encoding support for cross-platform compatibility
  - Enhanced subprocess calls with proper encoding parameters
- 🔧 **Layout Manager Conflicts**: Fixed Tkinter widget layout issues
  - Resolved pack/grid layout manager conflicts in StatusBarWidget
  - Improved widget placement and parent-child relationships
- 📋 **Configuration Import**: Enhanced validation and error handling
  - Better backup file format validation
  - Improved server configuration restoration
  - Enhanced theme settings import/export
- 🔍 **Server Management**: Fixed core functionality issues
  - Fixed server status not updating correctly
  - Resolved memory leak in long-running sessions
  - Corrected port conflict detection
  - Enhanced process monitoring

### Security
- 🔒 **File Integrity**: Enhanced backup and update security
  - SHA256 checksum validation for downloads
  - Secure backup file creation and validation
  - Safe installation process with automatic rollback
- 🛡️ **Input Validation**: Improved security for user inputs
  - Enhanced JSON schema validation
  - Secure file path handling
  - Better error boundary handling
  - Improved input sanitization

---

## Release History Summary

This application represents the culmination of development efforts to create a comprehensive development server management solution. Version 2.1.0 includes all core features, advanced functionality, and modern enhancements in a single, stable release.

### Development Evolution
- **Foundation**: Basic server management and GUI interface
- **Enhancement**: Template system, auto-detection, and system tray integration
- **Advanced Features**: Backup/import system and live update functionality
- **Documentation**: Comprehensive guides and technical documentation
- **Current State**: v2.1.0 - Complete feature set with modern UI and robust functionality

---

## Release Process

1. Update version in `setup.py`, `pyproject.toml`, and `src/__init__.py`
2. Update this changelog with new features and fixes
3. Run `python prepare_release.py` to create release package
4. Create Git tag: `git tag v[version]`
5. Push changes and tags to GitHub
6. Create GitHub Release with generated package and release notes

---

**Latest Release**: v2.1.0 - Complete development server management solution with backup, live updates, and comprehensive documentation.