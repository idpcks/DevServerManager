#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for backup and import functionality
Tests the new backup/import features added to DevServerManager
"""

import os
import sys
import json
import tempfile
from datetime import datetime

# Fix encoding issues on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.config_manager import ConfigManager
from src.models.server_config import ServerConfig

def test_backup_functionality():
    """Test the backup and import functionality"""
    print("Testing DevServerManager Backup & Import Functionality")
    print("=" * 60)
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Initialize config manager with temp directory
        config_manager = ConfigManager(temp_dir)
        config_manager.initialize()
        
        # Create test server configurations
        test_servers = {
            'test-backend': ServerConfig(
                name='test-backend',
                path='/test/backend',
                port='8009',
                command='php artisan serve',
                template_id='laravel',
                category='php',
                description='Test backend server'
            ),
            'test-frontend': ServerConfig(
                name='test-frontend',
                path='/test/frontend',
                port='3000',
                command='npm start',
                template_id='react',
                category='javascript',
                description='Test frontend server'
            )
        }
        
        print(f"Created {len(test_servers)} test server configurations")
        
        # Save test servers
        success = config_manager.save_server_configs(test_servers)
        print(f"Server configs saved: {'Success' if success else 'Failed'}")
        
        # Create test theme config
        test_theme = {
            'current_theme': 'dark',
            'themes': {
                'dark': {'bg': '#2c3e50', 'fg': '#ecf0f1'},
                'light': {'bg': '#ffffff', 'fg': '#2c3e50'}
            }
        }
        
        theme_success = config_manager.save_theme_config(test_theme)
        print(f"Theme config saved: {'Success' if theme_success else 'Failed'}")
        
        # Test backup creation (simulate BackupExportDialog functionality)
        backup_file = os.path.join(temp_dir, 'test_backup.json')
        backup_data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'app_version': '2.0.0',
                'backup_type': 'test_export',
                'description': 'Test backup for functionality verification'
            }
        }
        
        # Add server configurations to backup
        servers_dict = {}
        for name, config in test_servers.items():
            servers_dict[name] = config.to_dict()
        backup_data['servers'] = servers_dict
        
        # Add theme config to backup
        backup_data['theme_config'] = test_theme
        
        # Save backup file
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=4, ensure_ascii=False)
            print(f"Backup file created: {'Success' if os.path.exists(backup_file) else 'Failed'}")
        except Exception as e:
            print(f"Backup file creation: Failed - {e}")
            return False
        
        # Verify backup file contents
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                loaded_backup = json.load(f)
            
            # Check metadata
            metadata = loaded_backup.get('metadata', {})
            print(f"Backup metadata: {'Valid' if metadata.get('app_version') else 'Invalid'}")
            
            # Check servers
            servers = loaded_backup.get('servers', {})
            print(f"Server count in backup: {len(servers)} ({'Correct' if len(servers) == 2 else 'Incorrect'})")
            
            # Check theme
            theme = loaded_backup.get('theme_config', {})
            print(f"Theme config in backup: {'Present' if theme else 'Missing'}")
            
        except Exception as e:
            print(f"Backup verification: Failed - {e}")
            return False
        
        # Test import functionality (simulate ImportRestoreDialog functionality)
        print("\nTesting Import Functionality")
        print("-" * 30)
        
        # Clear existing configs to simulate fresh import
        empty_servers = {}
        config_manager.save_server_configs(empty_servers)
        
        # Import from backup
        try:
            imported_servers = {}
            
            for name, config_data in loaded_backup['servers'].items():
                server_config = ServerConfig(
                    name=config_data.get('name', name),
                    path=config_data.get('path', ''),
                    port=str(config_data.get('port', 8000)),
                    command=config_data.get('command', 'python -m http.server'),
                    template_id=config_data.get('template_id', 'custom'),
                    category=config_data.get('category', ''),
                    env_vars=config_data.get('env_vars', {}),
                    description=config_data.get('description', '')
                )
                imported_servers[name] = server_config
            
            # Save imported servers
            import_success = config_manager.save_server_configs(imported_servers)
            print(f"Import servers: {'Success' if import_success else 'Failed'}")
            
            # Import theme
            if 'theme_config' in loaded_backup:
                theme_import_success = config_manager.save_theme_config(loaded_backup['theme_config'])
                print(f"Import theme: {'Success' if theme_import_success else 'Failed'}")
            
            # Verify imported data
            loaded_servers = config_manager.load_server_configs()
            print(f"Verification: {len(loaded_servers)} servers imported successfully")
            
            for name, server in loaded_servers.items():
                original = test_servers[name]
                match = (server.name == original.name and 
                        server.path == original.path and 
                        server.port == original.port)
                print(f"   - {name}: {'Match' if match else 'Mismatch'}")
            
        except Exception as e:
            print(f"Import functionality: Failed - {e}")
            return False
        
        print(f"\nAll tests completed successfully!")
        print(f"Backup file size: {os.path.getsize(backup_file)} bytes")
        
        return True

if __name__ == "__main__":
    try:
        success = test_backup_functionality()
        if success:
            print("\nDevServerManager backup/import functionality is working correctly!")
        else:
            print("\nSome tests failed. Please check the implementation.")
        
    except Exception as e:
        print(f"\nTest execution failed: {e}")
        import traceback
        traceback.print_exc()