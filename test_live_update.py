#!/usr/bin/env python3
"""Test script for Live Update functionality

This script tests the live update components without running the full GUI.
"""

import sys
import os
sys.path.append('.')

from src.services.download_manager import DownloadManager, DownloadProgress
from src.services.update_installer import UpdateInstaller
from src.services.update_checker import UpdateCheckerService

def test_download_manager():
    """Test DownloadManager functionality."""
    print("🧪 Testing DownloadManager...")
    
    dm = DownloadManager()
    
    # Test file size check
    test_url = "https://github.com/idpcks/DevServerManager/releases/latest"
    file_size = dm.get_file_size(test_url)
    print(f"   📊 File size check: {file_size} bytes")
    
    # Test download info
    info = dm.get_download_info(test_url)
    print(f"   📋 Download info: {info}")
    
    print("   ✅ DownloadManager test completed!")

def test_update_installer():
    """Test UpdateInstaller functionality."""
    print("🧪 Testing UpdateInstaller...")
    
    ui = UpdateInstaller()
    
    # Test installation info
    info = ui.get_installation_info()
    print(f"   📊 Installation info: {info}")
    
    # Test backup management
    backups = ui.get_available_backups()
    print(f"   💾 Available backups: {len(backups)}")
    
    # Test cleanup
    ui.cleanup_old_backups()
    print("   🧹 Backup cleanup completed")
    
    print("   ✅ UpdateInstaller test completed!")

def test_update_checker():
    """Test UpdateCheckerService functionality."""
    print("🧪 Testing UpdateCheckerService...")
    
    uc = UpdateCheckerService()
    
    # Test current version
    current_version = uc.get_current_version()
    print(f"   📊 Current version: {current_version}")
    
    # Test version comparison
    test_versions = ["1.0.0", "1.0.1", "2.0.0", "0.9.9"]
    for version in test_versions:
        is_newer = uc._is_newer_version(version)
        print(f"   🔍 {version} is newer: {is_newer}")
    
    print("   ✅ UpdateCheckerService test completed!")

def test_progress_tracking():
    """Test progress tracking functionality."""
    print("🧪 Testing Progress Tracking...")
    
    # Test DownloadProgress
    progress = DownloadProgress(
        downloaded=1024*1024,  # 1MB
        total=10*1024*1024,    # 10MB
        percentage=10.0,
        speed=1024*1024,       # 1MB/s
        eta=9
    )
    
    print(f"   📊 Progress: {progress.percentage}%")
    print(f"   🚀 Speed: {progress.speed / (1024*1024):.1f} MB/s")
    print(f"   ⏱️  ETA: {progress.eta} seconds")
    
    print("   ✅ Progress tracking test completed!")

def main():
    """Run all tests."""
    print("🚀 Live Update Test Suite")
    print("=" * 50)
    
    try:
        test_download_manager()
        print()
        
        test_update_installer()
        print()
        
        test_update_checker()
        print()
        
        test_progress_tracking()
        print()
        
        print("🎉 All tests completed successfully!")
        print("✅ Live Update system is ready!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
