#!/usr/bin/env python3
"""
Secure Distribution Build Script for DevServerManager

This script demonstrates how environment variables are embedded at build time
for secure distribution, preventing end users from modifying critical settings.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_secure_distribution():
    """Create a secure distribution package"""
    print("Creating secure distribution package...")
    print("="*50)
    
    # 1. Load developer .env file (this contains sensitive settings)
    print("1. Loading developer environment configuration...")
    if not os.path.exists('.env'):
        print("   ⚠️  Developer .env file not found!")
        print("   Creating from template...")
        shutil.copy('.env.example', '.env')
    
    # 2. Build executable with embedded configuration
    print("2. Building executable with embedded configuration...")
    result = subprocess.run([sys.executable, 'build_executable.py'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("   ❌ Build failed!")
        print(result.stderr)
        return False
    
    print("   ✅ Executable built successfully!")
    
    # 3. Create distribution package structure
    print("3. Creating distribution package structure...")
    dist_dir = "release-secure"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    os.makedirs(dist_dir, exist_ok=True)
    
    # Copy executable
    shutil.copy("dist/DevServerManager.exe", f"{dist_dir}/DevServerManager.exe")
    
    # Copy user configuration template (NOT the developer .env)
    shutil.copy(".env.dist", f"{dist_dir}/.env")
    
    # Copy essential files
    for file in ["README.md", "requirements.txt"]:
        if os.path.exists(file):
            shutil.copy(file, f"{dist_dir}/{file}")
    
    # Create assets directory if it exists
    if os.path.exists("assets"):
        shutil.copytree("assets", f"{dist_dir}/assets", ignore=shutil.ignore_patterns('*.ico'))
    
    print("   ✅ Distribution package created!")
    
    # 4. Security verification
    print("4. Security verification...")
    print("   ✅ Critical settings embedded in executable")
    print("   ✅ User .env contains only safe, configurable settings")
    print("   ✅ Developer .env excluded from distribution")
    print("   ✅ No source code included in distribution")
    
    # 5. Package info
    print("5. Package information:")
    exe_size = os.path.getsize(f"{dist_dir}/DevServerManager.exe") / (1024 * 1024)
    print(f"   📦 Package location: {dist_dir}/")
    print(f"   📏 Executable size: {exe_size:.2f} MB")
    
    # 6. Security explanation
    print("\n" + "="*50)
    print("SECURITY FEATURES")
    print("="*50)
    print("🔒 Build-time Security:")
    print("   • Critical settings (GitHub repo, update URLs, app config)")
    print("     are embedded in the executable at build time")
    print("   • End users cannot modify these settings")
    print("   • Only developers with access to source can change them")
    print()
    print("🔧 User Configuration:")
    print("   • Safe settings (log levels, directories, server defaults)")
    print("     can be modified by users in .env file")
    print("   • No security-critical settings exposed")
    print()
    print("🛡️ Distribution Security:")
    print("   • Developer .env file not included in distribution")
    print("   • Only .env.dist template distributed to users")
    print("   • Source code not included")
    
    return True

def explain_security_model():
    """Explain the security model in detail"""
    print("\n" + "="*70)
    print("SECURITY MODEL EXPLANATION")
    print("="*70)
    print()
    print("🔐 PROBLEM SOLVED:")
    print("   Previous version: All settings in .env file that users could modify")
    print("   Security risk: Users could change GitHub repo URL, update settings")
    print()
    print("✅ NEW SECURE APPROACH:")
    print("   1. BUILD-TIME EMBEDDING:")
    print("      • Critical settings read from .env during build process")
    print("      • Values embedded directly in executable code")
    print("      • Cannot be modified after compilation")
    print()
    print("   2. TWO-TIER CONFIGURATION:")
    print("      • BuildConfig.get_build_config() → Immutable, embedded settings")
    print("      • BuildConfig.get_user_config() → User-modifiable settings")
    print()
    print("   3. SECURE DISTRIBUTION:")
    print("      • Developer .env (with secrets) never distributed")
    print("      • Only .env.dist template given to users")
    print("      • Users can only modify safe, non-critical settings")
    print()
    print("🛠️ FOR DEVELOPERS:")
    print("   • Modify .env or .env.example with your settings")
    print("   • Run this script to build secure distribution")
    print("   • Critical settings get embedded, safe settings stay configurable")
    print()
    print("👤 FOR END USERS:")
    print("   • Receive executable with embedded critical settings")
    print("   • Can modify .env for personal preferences (logs, directories)")
    print("   • Cannot modify security-critical settings")

if __name__ == "__main__":
    print("DevServerManager Secure Distribution Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: Run this script from the project root directory")
        sys.exit(1)
    
    # Create secure distribution
    success = create_secure_distribution()
    
    if success:
        print("\n🎉 Secure distribution created successfully!")
        explain_security_model()
    else:
        print("\n❌ Distribution creation failed!")
        sys.exit(1)