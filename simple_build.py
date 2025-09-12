#!/usr/bin/env python3
"""
Simple build script for DevServerManager
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """Clean previous build"""
    dirs = ['build', 'dist', '__pycache__']
    for d in dirs:
        if os.path.exists(d):
            print(f"Cleaning {d}...")
            shutil.rmtree(d)

def build():
    """Build executable"""
    print("Building DevServerManager...")
    
    clean_build()
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed", 
        "--name=DevServerManager",
        "--icon=assets/app_icon.ico",
        "main.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("Build completed!")
        
        exe_path = "dist/DevServerManager.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"Executable: {exe_path} ({size_mb:.1f} MB)")
            return True
        else:
            print("ERROR: Executable not found!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)