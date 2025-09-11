#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backup Script for DevServerManager
Creates a backup of all configuration files before updating
"""

import os
import sys
import shutil
import json
from datetime import datetime
import zipfile

# Fix encoding issues on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def create_backup():
    """Create a comprehensive backup of all configuration files"""
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    backup_zip = f"devserver_backup_{timestamp}.zip"
    
    print(f"Creating backup: {backup_zip}")
    
    try:
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Files and directories to backup
        backup_items = [
            "config/",
            "main.py",
            "requirements.txt",
            "pyproject.toml",
            "theme_config.json"
        ]
        
        # Copy files to backup directory
        for item in backup_items:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.copytree(item, os.path.join(backup_dir, item), dirs_exist_ok=True)
                    print(f"Backed up directory: {item}")
                else:
                    shutil.copy2(item, backup_dir)
                    print(f"Backed up file: {item}")
            else:
                print(f"Item not found: {item}")
        
        # Create backup info file
        backup_info = {
            "backup_date": datetime.now().isoformat(),
            "backup_version": "DevServerManager Backup v1.0",
            "items_backed_up": backup_items,
            "notes": "Backup created before updating DevServerManager"
        }
        
        with open(os.path.join(backup_dir, "backup_info.json"), 'w') as f:
            json.dump(backup_info, f, indent=4)
        
        # Create ZIP archive
        with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_dir)
                    zipf.write(file_path, arcname)
        
        # Remove temporary backup directory
        shutil.rmtree(backup_dir)
        
        print(f"Backup created successfully: {backup_zip}")
        print(f"Backup size: {os.path.getsize(backup_zip)} bytes")
        
        # List contents of backup
        print("\nBackup contents:")
        with zipfile.ZipFile(backup_zip, 'r') as zipf:
            for info in zipf.infolist():
                print(f"   {info.filename}")
        
        return backup_zip
        
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def verify_backup(backup_file):
    """Verify the backup file integrity"""
    try:
        print(f"\nVerifying backup: {backup_file}")
        
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            # Test the zip file
            bad_file = zipf.testzip()
            if bad_file:
                print(f"Corrupted file in backup: {bad_file}")
                return False
            
            # Check if essential files are present
            files = zipf.namelist()
            essential_files = ["backup_info.json"]
            
            for essential in essential_files:
                if essential not in files:
                    print(f"Missing essential file: {essential}")
            
            print("Backup verification successful")
            return True
            
    except Exception as e:
        print(f"Error verifying backup: {e}")
        return False

if __name__ == "__main__":
    print("DevServerManager Backup Tool")
    print("=" * 40)
    
    # Change to runserver directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create backup
    backup_file = create_backup()
    
    if backup_file:
        # Verify backup
        if verify_backup(backup_file):
            print(f"\nBackup process completed successfully!")
            print(f"Backup file: {os.path.abspath(backup_file)}")
            print("\nTo restore from backup:")
            print(f"   1. Extract {backup_file}")
            print("   2. Copy config/ folder back to runserver/")
            print("   3. Copy other files as needed")
        else:
            print("\nBackup verification failed!")
    else:
        print("\nBackup process failed!")