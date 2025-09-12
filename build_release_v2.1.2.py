#!/usr/bin/env python3
"""Build Release Script for DevServer Manager v2.1.2

This script builds the Windows release with environment variable support.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def clean_build_dirs():
    """Clean build directories."""
    print("Cleaning build directories...")
    
    try:
        dirs_to_clean = ['build', 'dist', '__pycache__']
        for dir_name in dirs_to_clean:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"Removed {dir_name}/")
        
        # Clean .pyc files
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.pyc'):
                    os.remove(os.path.join(root, file))
        
        return True
    except Exception as e:
        print(f"Error cleaning directories: {e}")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    success, output = run_command("pip install -r requirements.txt")
    if not success:
        print(f"Error installing dependencies: {output}")
        return False
    
    print("Dependencies installed successfully")
    return True

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=DevServerManager-v2.1.2",
        "--icon=assets/app_icon.ico",
        "--add-data=config;config",
        "--add-data=assets;assets",
        "--add-data=.env.example;.",
        "--hidden-import=dotenv",
        "--hidden-import=psutil",
        "--hidden-import=watchdog",
        "main.py"
    ]
    
    success, output = run_command(" ".join(cmd))
    if not success:
        print(f"Error building executable: {output}")
        return False
    
    print("Executable built successfully")
    return True

def create_release_package():
    """Create the release package."""
    print("Creating release package...")
    
    # Create release directory
    release_dir = Path("release-v2.1.2")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy executable
    exe_path = Path("dist/DevServerManager-v2.1.2.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, release_dir / "DevServerManager-v2.1.2.exe")
    
    # Copy configuration files
    config_files = [
        ".env.example",
        "README.md",
        "CHANGELOG.md",
        "LICENSE"
    ]
    
    for file_name in config_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, release_dir / file_name)
    
    # Copy config directory
    if os.path.exists("config"):
        shutil.copytree("config", release_dir / "config")
    
    # Copy assets directory
    if os.path.exists("assets"):
        shutil.copytree("assets", release_dir / "assets")
    
    # Create .env from .env.example
    env_example = release_dir / ".env.example"
    env_file = release_dir / ".env"
    if env_example.exists():
        shutil.copy2(env_example, env_file)
    
    print(f"Release package created in {release_dir}/")
    return True

def create_zip_package():
    """Create ZIP package for distribution."""
    print("Creating ZIP package...")
    
    import zipfile
    
    zip_name = "DevServerManager-v2.1.2-Windows.zip"
    release_dir = Path("release-v2.1.2")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(release_dir)
                zipf.write(file_path, arc_path)
    
    print(f"ZIP package created: {zip_name}")
    return True

def main():
    """Main build process."""
    print("=" * 60)
    print("DevServer Manager v2.1.2 - Build Release Script")
    print("=" * 60)
    print(f"Build started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Build steps
    steps = [
        ("Cleaning build directories", clean_build_dirs),
        ("Installing dependencies", install_dependencies),
        ("Building executable", build_executable),
        ("Creating release package", create_release_package),
        ("Creating ZIP package", create_zip_package),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ Failed: {step_name}")
            return False
        print(f"✅ Success: {step_name}")
    
    print("\n" + "=" * 60)
    print("Build completed successfully!")
    print("=" * 60)
    print(f"Build finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nRelease files:")
    print("- DevServerManager-v2.1.2-Windows.zip")
    print("- release-v2.1.2/")
    print("\nNext steps:")
    print("1. Test the executable")
    print("2. Create GitHub release")
    print("3. Upload ZIP file")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
