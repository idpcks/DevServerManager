# Live Update Feature

## Overview

DevServer Manager now includes a comprehensive **Live Update** system that allows users to automatically download and install application updates without manual intervention. This feature provides a seamless update experience with progress tracking, backup capabilities, and rollback options.

## Features

### ✨ **Core Live Update Features**

- **🚀 Automatic Download**: Downloads updates in the background with progress tracking
- **📊 Progress Monitoring**: Real-time progress bar with speed and ETA information
- **🔧 Automatic Installation**: Installs updates automatically with backup creation
- **🔄 Automatic Restart**: Restarts application with new version seamlessly
- **💾 Backup & Rollback**: Creates backups and allows rollback to previous versions
- **✅ Integrity Verification**: Verifies file integrity using checksums
- **❌ Cancellation Support**: Allows users to cancel update process

### 🎯 **User Experience**

- **Modern UI**: Beautiful progress dialogs with real-time updates
- **Non-blocking**: Updates run in background without blocking the application
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Manual Fallback**: Option to download manually if automatic update fails

## How It Works

### 1. **Update Detection**
```
Application checks GitHub API → Compares versions → Shows Live Update dialog
```

### 2. **Download Process**
```
User clicks "Live Update Now" → Progress dialog appears → File downloads with progress tracking
```

### 3. **Installation Process**
```
Download completes → Backup created → Executable replaced → Application restarts
```

### 4. **Rollback Process**
```
If update fails → Backup restored → Application continues with previous version
```

## Usage

### **Automatic Detection**
- Live update is automatically detected when updates are available
- Users see a "Live Update Available!" dialog with update information

### **Manual Check**
- Go to **Help** → **🚀 Live Update** to manually check for updates
- This forces a check and shows live update dialog if available

### **Update Process**
1. Click **"🚀 Live Update Now"** button
2. Progress dialog shows download progress with:
   - Download percentage
   - Download speed (MB/s)
   - Estimated time remaining (ETA)
   - Current status message
3. Installation happens automatically
4. Application restarts with new version

### **Cancellation**
- Click **"Cancel"** button during download to stop the process
- No changes are made if cancelled

## Technical Implementation

### **Download Manager** (`download_manager.py`)
- Handles file downloads with progress tracking
- Supports cancellation and integrity verification
- Manages download cache and cleanup

### **Update Installer** (`update_installer.py`)
- Manages installation process
- Creates backups before updating
- Handles application restart
- Provides rollback functionality

### **Progress Dialog** (`dialogs.py`)
- Shows real-time progress information
- Displays download speed and ETA
- Provides cancellation option
- Modern, responsive UI

### **Live Update Dialog** (`dialogs.py`)
- Main interface for live updates
- Shows update information and features
- Provides both automatic and manual options

## Configuration

### **Update Settings**
- **Check Interval**: Every 24 hours (configurable)
- **Cache Duration**: 1 hour (configurable)
- **Backup Retention**: 3 recent backups kept
- **Download Directory**: `runserver/downloads/`
- **Backup Directory**: `runserver/backup/`

### **GitHub Integration**
- **Repository**: `idpcks/DevServerManager`
- **API Endpoint**: GitHub Releases API
- **Asset Detection**: Automatically finds Windows .exe files
- **Fallback**: Uses .zip files if .exe not available

## File Structure

```
runserver/
├── src/
│   ├── services/
│   │   ├── download_manager.py      # Download management
│   │   └── update_installer.py      # Installation management
│   └── gui/
│       └── dialogs.py               # UI components
├── downloads/                       # Download cache
├── backup/                         # Backup files
└── config/
    └── update_cache.json           # Update cache
```

## Error Handling

### **Download Errors**
- Network connectivity issues
- File not found errors
- Download corruption
- User cancellation

### **Installation Errors**
- Permission issues
- File access conflicts
- Backup creation failures
- Restart failures

### **Recovery**
- Automatic rollback on failure
- Backup restoration
- Error logging and reporting
- User notification

## Security Features

### **Integrity Verification**
- SHA256 checksum validation
- File size verification
- Download completion verification

### **Backup System**
- Automatic backup creation
- Multiple backup retention
- Rollback capability
- Safe installation process

### **Safe Installation**
- Graceful shutdown before update
- Atomic file replacement
- Verification after installation
- Automatic cleanup

## Performance

### **Background Processing**
- Non-blocking downloads
- Threaded operations
- Progress callbacks
- Memory efficient

### **Caching**
- Download progress caching
- Update information caching
- Automatic cleanup
- Storage optimization

## Troubleshooting

### **Common Issues**

#### **Download Fails**
- Check internet connection
- Verify GitHub repository access
- Check firewall settings
- Try manual download

#### **Installation Fails**
- Check file permissions
- Ensure application is not running
- Verify backup creation
- Check disk space

#### **Update Not Detected**
- Check GitHub API access
- Verify version comparison
- Check cache settings
- Force manual check

### **Recovery Steps**

1. **Manual Rollback**:
   - Go to backup directory
   - Replace executable with backup
   - Restart application

2. **Clean Installation**:
   - Download manually from GitHub
   - Replace executable
   - Restart application

3. **Reset Cache**:
   - Delete `update_cache.json`
   - Restart application
   - Check for updates

## Future Enhancements

### **Planned Features**
- **Delta Updates**: Only download changed files
- **Scheduled Updates**: Update at specific times
- **Update Notifications**: System tray notifications
- **Update History**: Track update history
- **Beta Channel**: Support for beta releases

### **Advanced Features**
- **Multi-platform Support**: Linux and macOS support
- **Update Channels**: Stable, beta, and nightly channels
- **Rollback UI**: Graphical rollback interface
- **Update Analytics**: Usage and performance tracking

## Support

For issues with live update functionality:

1. Check the logs in `logs/` directory
2. Verify network connectivity
3. Check GitHub repository access
4. Try manual download as fallback
5. Contact support with error details

## Conclusion

The Live Update feature provides a modern, user-friendly way to keep DevServer Manager up to date. With automatic detection, seamless installation, and comprehensive error handling, users can enjoy the latest features and improvements without manual intervention.

The system is designed to be reliable, secure, and user-friendly, providing both automatic and manual update options to suit different user preferences and network conditions.
