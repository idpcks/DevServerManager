#!/usr/bin/env python3
"""
Script untuk membuat release GitHub dengan versioning otomatis
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def get_current_version():
    """Ambil versi dari setup.py atau package.json"""
    try:
        # Coba ambil dari setup.py
        with open('setup.py', 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'version=' in line:
                    version = line.split('version=')[1].split(',')[0].strip().strip('"\'')
                    return version
    except Exception:
        pass
    
    # Fallback ke versi default
    return "1.0.0"

def update_version(new_version):
    """Update versi di setup.py"""
    try:
        with open('setup.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace version line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'version=' in line:
                lines[i] = f'    version="{new_version}",'
                break
        
        with open('setup.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"Updated version to {new_version} in setup.py")
        return True
    except Exception as e:
        print(f"Error updating version: {e}")
        return False

def create_changelog_entry(version, changes):
    """Buat changelog entry untuk versi baru"""
    changelog_file = "CHANGELOG.md"
    
    # Read existing changelog
    existing_content = ""
    if os.path.exists(changelog_file):
        with open(changelog_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # Create new entry
    date = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"""## [{version}] - {date}

### Added
{changes.get('added', '- No new features')}

### Changed
{changes.get('changed', '- No changes')}

### Fixed
{changes.get('fixed', '- No bug fixes')}

### Security
{changes.get('security', '- No security updates')}

---

"""
    
    # Write new changelog
    with open(changelog_file, 'w', encoding='utf-8') as f:
        f.write(new_entry + existing_content)
    
    print(f"Created changelog entry for version {version}")

def build_executable():
    """Build executable menggunakan build script"""
    print("Building executable...")
    try:
        result = subprocess.run([sys.executable, "build_executable.py"], 
                              check=True, capture_output=True, text=True)
        print("Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_release_package(version):
    """Buat package release dengan versioning"""
    print(f"Creating release package for version {version}...")
    
    # Create versioned release directory
    release_dir = f"release-v{version}"
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
        "config/server_config_example.json",
        "CHANGELOG.md"
    ]
    
    for file_path in files_to_copy:
        if os.path.exists(file_path):
            dest_path = os.path.join(release_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dest_path)
            print(f"Copied {file_path} to release directory")
    
    # Create version-specific user guide
    user_guide = f"""# DevServer Manager v{version} - Panduan Penggunaan

## Cara Menjalankan
1. Double-click file `DevServerManager.exe`
2. Aplikasi akan terbuka dengan splash screen
3. Gunakan interface untuk mengelola server development Anda

## File Konfigurasi
- `server_templates.json`: Template server yang tersedia
- `server_config_example.json`: Contoh konfigurasi server
- `CHANGELOG.md`: Daftar perubahan versi

## Troubleshooting
- Jika aplikasi tidak berjalan, pastikan Windows Defender tidak memblokir file
- Untuk masalah lain, silakan buat issue di repository GitHub

## Sistem Requirements
- Windows 10/11
- .NET Framework (biasanya sudah terinstall)

## Versi {version}
Lihat CHANGELOG.md untuk detail perubahan versi ini.
"""
    
    with open(os.path.join(release_dir, "PANDUAN_PENGGUNAAN.txt"), "w", encoding="utf-8") as f:
        f.write(user_guide)
    
    # Create ZIP package
    zip_name = f"DevServerManager-v{version}-Windows.zip"
    shutil.make_archive(f"DevServerManager-v{version}-Windows", 'zip', release_dir)
    
    print(f"Release package created: {zip_name}")
    return zip_name

def create_git_tag(version):
    """Buat git tag untuk release"""
    try:
        # Add and commit changes
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Release version {version}"], check=True)
        
        # Create tag
        tag_name = f"v{version}"
        subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {version}"], check=True)
        
        print(f"Created git tag: {tag_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating git tag: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python create_release.py <version> [--skip-build] [--skip-tag]")
        print("Example: python create_release.py 1.0.0")
        sys.exit(1)
    
    version = sys.argv[1]
    skip_build = "--skip-build" in sys.argv
    skip_tag = "--skip-tag" in sys.argv
    
    print(f"Creating release version {version}")
    print("=" * 50)
    
    # Update version in setup.py
    if not update_version(version):
        print("Failed to update version")
        sys.exit(1)
    
    # Create changelog entry
    changes = {
        'added': '- New features and improvements',
        'changed': '- Updated dependencies and configurations',
        'fixed': '- Bug fixes and stability improvements',
        'security': '- Security updates and patches'
    }
    create_changelog_entry(version, changes)
    
    # Build executable
    if not skip_build:
        if not build_executable():
            print("Build failed, aborting release")
            sys.exit(1)
    
    # Create release package
    zip_file = create_release_package(version)
    if not zip_file:
        print("Failed to create release package")
        sys.exit(1)
    
    # Create git tag
    if not skip_tag:
        if not create_git_tag(version):
            print("Failed to create git tag")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Release created successfully!")
    print(f"Version: {version}")
    print(f"Package: {zip_file}")
    print("\nNext steps:")
    print("1. Push changes: git push origin main")
    print("2. Push tags: git push origin --tags")
    print("3. GitHub Actions will automatically create the release")
    print("4. Or manually upload the ZIP file to GitHub Releases")

if __name__ == "__main__":
    main()
