# DevServerManager Backup & Import Guide

## 🔄 Overview

DevServerManager includes comprehensive backup and import functionality that enables seamless configuration management across different installations. This powerful feature allows you to:

- **Export** server configurations and settings to portable backup files
- **Import** configurations from backup files on any DevServerManager installation
- **Migrate** settings between different computers or DevServerManager instances
- **Create** automated and manual backups for safety and version control
- **Share** configurations with team members for consistent development environments

## 📤 Exporting Settings (Creating Backups)

### Method 1: Export Settings Dialog
1. Navigate to **File** → **Backup & Import** → **Export Settings...**
2. Configure export options:
   - ✅ **Server configurations** (always included - contains all your server setups)
   - ☑️ **Theme settings** (optional - includes your UI theme preferences)
   - ☑️ **Application settings** (optional - includes app-specific configurations)
3. Choose export location:
   - Default: `Desktop/devserver_backup.json`
   - Custom: Click **Browse** to select preferred location
4. Review the **Backup Preview** to see what will be included
5. Click **Create Backup** to generate the backup file

### Method 2: Toolbar Quick Access
1. In the **Server Controls** panel (left side), locate the **Backup & Import** section
2. Click **📦 Export Settings** button
3. Follow the same dialog process as Method 1

### Method 3: Comprehensive Manual Backup
1. Use **File** → **Backup & Import** → **Create Backup...**
2. This executes the comprehensive backup script that includes:
   - All configuration files (`config/` directory)
   - Application main files (`main.py`, `requirements.txt`, etc.)
   - Theme configurations
   - Complete system state backup
3. Creates a timestamped ZIP file with full system backup

## 📥 Importing Settings (Restoring from Backup)

### Step-by-Step Import Process
1. **Access Import Dialog:**
   - **File Menu:** File → Backup & Import → Import Settings...
   - **Toolbar:** Click **📥 Import Settings** in the Backup & Import section

2. **Select Backup File:**
   - Click **📁 Browse** to locate your backup file (.json format)
   - Or manually enter the file path in the text field

3. **Review Backup Preview:**
   - **Metadata:** Creation date, version, backup type
   - **Server Count:** Number of server configurations included
   - **Theme Settings:** Whether theme configurations are included
   - **Compatibility:** Version compatibility information

4. **Configure Import Options:**
   - **Import Mode:**
     - **Merge** (recommended): Combines with existing settings
     - **Replace**: Overwrites all existing settings
   - **Components to Import:**
     - ☑️ Server configurations
     - ☑️ Theme settings
     - ☑️ Application settings

5. **Execute Import:**
   - Click **📥 Import Settings**
   - Confirm the import operation
   - Wait for completion notification

6. **Post-Import Steps:**
   - **Restart DevServerManager** to apply all changes
   - Verify all imported servers appear in the server list
   - Test server functionality to ensure proper import

## 📋 Backup File Format & Structure

### JSON Format Overview
Backup files use structured JSON format for maximum compatibility and readability:

```json
{
  "metadata": {
    "created_at": "2025-09-11T13:47:54.123456",
    "app_version": "2.0.0",
    "backup_type": "user_export",
    "description": "User-created backup of DevServerManager settings",
    "export_options": {
      "include_servers": true,
      "include_theme": true,
      "include_app_settings": false
    }
  },
  "servers": {
    "backend-api": {
      "name": "backend-api",
      "path": "Z:/Dev/etiket/backend",
      "port": "8009",
      "command": "php artisan serve",
      "template_id": "laravel",
      "category": "php",
      "env_vars": {
        "APP_ENV": "development",
        "DB_CONNECTION": "mysql"
      },
      "alternative_commands": [
        "php artisan serve --host=0.0.0.0",
        "php artisan serve --port=8010"
      ],
      "description": "Backend API for mobile Flutter eTicket application"
    },
    "frontend-app": {
      "name": "frontend-app",
      "path": "Z:/Dev/etiket/frontend/onedesk",
      "port": "3000",
      "command": "flutter run -d chrome",
      "template_id": "flutter",
      "category": "mobile",
      "env_vars": {},
      "description": "Flutter frontend application"
    }
  },
  "theme_config": {
    "current_theme": "dark",
    "themes": {
      "dark": {
        "bg": "#2c3e50",
        "fg": "#ecf0f1",
        "frame_bg": "#34495e",
        "button_bg": "#3498db"
      },
      "light": {
        "bg": "#ffffff",
        "fg": "#2c3e50",
        "frame_bg": "#f8f9fa",
        "button_bg": "#007bff"
      }
    }
  },
  "app_settings": {
    "auto_start_servers": false,
    "minimize_to_tray": true,
    "check_for_updates": true,
    "log_level": "INFO"
  }
}
```

### File Naming Conventions
- **User Exports:** `devserver_backup_YYYYMMDD_HHMMSS.json`
- **Manual Backups:** `devserver_backup_YYYYMMDD_HHMMSS.zip`
- **Team Configs:** `team_config_[project]_[date].json`
- **Migration Files:** `migration_[old_version]_to_[new_version].json`

## ✨ Features & Benefits

### 🔒 **Data Safety & Integrity**
- **Metadata Tracking:** Every backup includes creation timestamp and version info
- **File Validation:** Comprehensive validation before import prevents corruption
- **Error Recovery:** Robust error handling with detailed error messages
- **Preview Mode:** See exactly what will be imported before making changes
- **Atomic Operations:** Import operations are all-or-nothing to prevent partial corruption

### 🚀 **Enhanced User Experience**
- **Intuitive Dialogs:** Step-by-step wizards with clear instructions
- **Real-time Feedback:** Progress indicators and status updates during operations
- **File Browser Integration:** Native file selection dialogs
- **Smart Defaults:** Sensible default settings with customization options
- **Automatic Refresh:** UI updates automatically after successful operations

### 🔄 **Migration & Collaboration**
- **Cross-Platform:** Works seamlessly on Windows, macOS, and Linux
- **Human-Readable:** JSON format allows manual editing if needed
- **Version Awareness:** Handles compatibility between different DevServerManager versions
- **Team Sharing:** Perfect for standardizing development environments
- **Selective Import:** Choose which components to import from backups

### ⚙️ **Flexibility & Control**
- **Granular Options:** Select exactly what to include in backups
- **Multiple Access Methods:** File menu, toolbar, and keyboard shortcuts
- **Batch Operations:** Import multiple configurations efficiently
- **Merge Strategies:** Intelligent merging with existing configurations
- **Rollback Capability:** Easy restoration from previous backups

## 🛠️ Best Practices & Workflows

### Regular Backup Strategy
```
Daily:    Export settings after significant configuration changes
Weekly:   Create comprehensive manual backups (ZIP format)
Monthly:  Archive backups to cloud storage or external drives
Release:  Create tagged backups before major version updates
```

### Team Collaboration Workflow
1. **Standardization:**
   - Create a "master" configuration backup for your team
   - Include all common servers and development tools
   - Document any team-specific customizations

2. **Distribution:**
   - Share backup files via version control (Git)
   - Use descriptive filenames: `team_etiket_dev_2025-09-11.json`
   - Include README with setup instructions

3. **Onboarding:**
   - New team members import the standard configuration
   - Reduces setup time from hours to minutes
   - Ensures consistent development environments

### Migration Strategy
```
Pre-Migration:
1. Create full backup of current installation
2. Document any custom modifications
3. Note installed plugins or extensions
4. Export all server configurations

Migration:
1. Install DevServerManager on new system
2. Import configuration backup
3. Verify all paths are correct for new system
4. Test each server individually
5. Update any system-specific paths

Post-Migration:
1. Create new backup of migrated system
2. Update team documentation
3. Archive old system backup for rollback
```

## 🚨 Troubleshooting Guide

### Common Import Issues

#### File Format Errors
**Symptoms:** "Invalid backup file format" error
**Solutions:**
- Verify file is valid JSON using online JSON validator
- Check file wasn't corrupted during transfer
- Ensure file extension is `.json`
- Try opening file in text editor to inspect content

#### Permission Errors
**Symptoms:** "Access denied" or "Permission error"
**Solutions:**
- Run DevServerManager as administrator (Windows)
- Check file/folder permissions
- Ensure target drive has sufficient space
- Verify backup file isn't read-only

#### Missing Servers After Import
**Symptoms:** Servers don't appear after import
**Solutions:**
- **Restart DevServerManager completely** (most common fix)
- Check if import actually completed successfully
- Verify backup file contains server configurations
- Check application logs for import errors

#### Path Issues
**Symptoms:** Servers imported but won't start
**Solutions:**
- Update server paths for new system
- Check if referenced directories exist
- Verify permissions on server directories
- Update commands for new environment

### Export/Backup Issues

#### Cannot Save Backup File
**Symptoms:** "Failed to create backup" error
**Solutions:**
- Check available disk space
- Verify write permissions to target directory
- Try different export location
- Close any applications that might lock the file

#### Incomplete Backups
**Symptoms:** Backup file smaller than expected
**Solutions:**
- Ensure all DevServerManager services are running
- Check for configuration file corruption
- Verify no servers are in "locked" state
- Review export options to ensure all desired components are selected

#### Large File Sizes
**Note:** This is typically normal behavior
- JSON format is text-based and human-readable
- Large configurations with many servers create larger files
- ZIP backups include additional files and are larger
- Consider selective exports for specific use cases

### Performance Optimization

#### Large Configuration Sets
- Use selective import for specific servers only
- Break large configurations into smaller, focused backups
- Regular cleanup of unused server configurations
- Archive old configurations instead of keeping all active

#### Network/Cloud Storage
- Compress backup files for cloud storage
- Use version control for team backup management
- Consider backup file retention policies
- Regular cleanup of old backup files

## 🔧 Advanced Usage

### Command Line Integration
For advanced users, backup operations can be integrated into scripts:

```bash
# Create manual backup
cd /path/to/devservermanager
python backup_config.py

# Automated backup script (example)
#!/bin/bash
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/backups/devservermanager"
python backup_config.py
mv devserver_backup_*.zip "$BACKUP_DIR/backup_$DATE.zip"
```

### Automation Ideas
- **Pre-commit hooks:** Create backups before major code changes
- **CI/CD integration:** Include configuration backups in deployment pipelines
- **Scheduled backups:** Use cron jobs or Task Scheduler for regular backups
- **Cloud sync:** Automatically sync backups to cloud storage

### Custom Backup Scripts
The backup system is extensible for custom needs:
- Modify `backup_config.py` for custom backup content
- Add custom metadata to backup files
- Implement custom validation rules
- Create specialized backup formats for specific use cases

## 📞 Support & Resources

### Getting Help
1. **Application Logs:** Check logs directory for detailed error information
2. **JSON Validation:** Use online tools to validate backup file format
3. **Test Environment:** Try import in clean DevServerManager installation
4. **Documentation:** Review this guide and other documentation files

### Related Documentation
- `docs/CONFIGURATION.md` - General configuration management
- `docs/TROUBLESHOOTING.md` - General troubleshooting guide
- `docs/USER_GUIDE.md` - Complete user manual
- `CHANGELOG.md` - Version history and feature updates

### Community Resources
- GitHub Issues: Report bugs and request features
- Discussions: Share configurations and best practices
- Wiki: Community-maintained tips and tricks

---

*This guide covers DevServerManager v2.0.0 and later. For older versions, some features may not be available.*