#!/usr/bin/env python3
"""
Script untuk build executable DevServer Manager menggunakan PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    """Membersihkan direktori build dan dist sebelumnya"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name} directory")

def build_executable():
    """Build executable menggunakan PyInstaller"""
    print("Starting build process...")
    
    # Pastikan icon file ada
    icon_path = "assets/app_icon.ico"
    if not os.path.exists(icon_path):
        print(f"Warning: Icon file {icon_path} not found")
        icon_path = None
    
    # Command PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=DevServerManager",      # Nama executable
        "--distpath=dist",              # Output directory
        "--workpath=build",             # Work directory
        "--specpath=.",                 # Spec file location
    ]
    
    # Tambahkan icon jika ada
    if icon_path:
        cmd.extend(["--icon", icon_path])
    
    # Tambahkan data files yang diperlukan
    data_files = [
        "--add-data=config;config",
        "--add-data=assets;assets",
        "--add-data=src;src",
        "--add-data=utils;utils"
    ]
    cmd.extend(data_files)
    
    # Hidden imports untuk dependencies
    hidden_imports = [
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=pystray",
        "--hidden-import=threading",
        "--hidden-import=json",
        "--hidden-import=subprocess",
        "--hidden-import=psutil"
    ]
    cmd.extend(hidden_imports)
    
    # Main file
    cmd.append("main.py")
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_release_package():
    """Membuat package release dengan file yang diperlukan"""
    print("Creating release package...")
    
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    os.makedirs(release_dir)
    
    # Copy executable
    exe_path = "dist/DevServerManager.exe"
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, release_dir)
        print(f"Copied {exe_path} to release directory")
    else:
        print(f"Error: Executable {exe_path} not found")
        return False
    
    # Copy essential files
    files_to_copy = [
        "README.md",
        "requirements.txt",
        "config/server_templates.json",
        "config/server_config_example.json"
    ]
    
    for file_path in files_to_copy:
        if os.path.exists(file_path):
            dest_path = os.path.join(release_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dest_path)
            print(f"Copied {file_path} to release directory")
    
    # Create user guide
    user_guide = """
# DevServer Manager - Panduan Penggunaan

## Cara Menjalankan
1. Double-click file `DevServerManager.exe`
2. Aplikasi akan terbuka dengan splash screen
3. Gunakan interface untuk mengelola server development Anda

## File Konfigurasi
- `server_templates.json`: Template server yang tersedia
- `server_config_example.json`: Contoh konfigurasi server

## Troubleshooting
- Jika aplikasi tidak berjalan, pastikan Windows Defender tidak memblokir file
- Untuk masalah lain, silakan buat issue di repository GitHub

## Sistem Requirements
- Windows 10/11
- .NET Framework (biasanya sudah terinstall)
"""
    
    with open(os.path.join(release_dir, "PANDUAN_PENGGUNAAN.txt"), "w", encoding="utf-8") as f:
        f.write(user_guide)
    
    print(f"Release package created in '{release_dir}' directory")
    return True

def main():
    """Main function"""
    print("DevServer Manager Build Script")
    print("=" * 40)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if not build_executable():
        print("Build failed!")
        sys.exit(1)
    
    # Create release package
    if not create_release_package():
        print("Failed to create release package!")
        sys.exit(1)
    
    print("\nBuild completed successfully!")
    print("Executable location: dist/DevServerManager.exe")
    print("Release package: release/")

if __name__ == "__main__":
    main()