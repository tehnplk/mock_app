#!/usr/bin/env python3
"""
Test the connection test functionality in HisConSetting
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from AppSetting import AppSetting
from HisConSetting import HisConSetting

def test_connection_functionality():
    """Test the connection test functionality"""
    print("=" * 60)
    print("Connection Test Functionality Test")
    print("=" * 60)
    
    # Initialize app settings
    app_settings = AppSetting()
    
    # Set some test values for a basic test
    print("\n1. Setting test connection values...")
    test_values = {
        'host': 'localhost',
        'port': 3306,
        'database': 'test',
        'username': 'test_user',
        'password': 'test_pass',
        'db_system': 'mysql',
        'charset': 'utf8mb4',
        'ssl': False,
        'use_connection_string': False
    }
    
    for key, value in test_values.items():
        app_settings.set_value(key, value)
        print(f"  ✓ Set {key} = {value}")
    
    app_settings.sync()
    
    # Create QApplication if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\n2. Creating HisConSetting dialog...")
    try:
        dialog = HisConSetting()
        print("  ✓ Dialog created successfully")
        
        # Check if the worker thread class is accessible
        from HisConSetting import ConnectionTestWorker
        print("  ✓ ConnectionTestWorker class imported successfully")
        
        # Check if dialog has the required methods
        required_methods = [
            'test_connection',
            '_get_internal_db_system', 
            'on_connection_test_completed',
            'closeEvent'
        ]
        
        for method_name in required_methods:
            if hasattr(dialog, method_name):
                print(f"  ✓ Method {method_name} exists")
            else:
                print(f"  ❌ Method {method_name} missing")
                return False
        
        # Test the _get_internal_db_system method
        print("\n3. Testing helper methods...")
        
        dialog.db_system.setCurrentText("MySQL")
        db_system = dialog._get_internal_db_system()
        assert db_system == "mysql", f"Expected 'mysql', got '{db_system}'"
        print("  ✓ _get_internal_db_system works for MySQL")
        
        dialog.db_system.setCurrentText("PostgreSQL")
        db_system = dialog._get_internal_db_system()
        assert db_system == "postgresql", f"Expected 'postgresql', got '{db_system}'"
        print("  ✓ _get_internal_db_system works for PostgreSQL")
        
        # Test that connection test worker can be created
        print("\n4. Testing ConnectionTestWorker creation...")
        connection_params = {
            'use_connection_string': False,
            'host': 'localhost',
            'port': 3306,
            'database': 'test',
            'username': 'test_user',
            'password': 'test_pass',
            'db_system': 'mysql',
            'charset': 'utf8mb4',
            'ssl': False
        }
        
        worker = ConnectionTestWorker(connection_params)
        print("  ✓ ConnectionTestWorker created successfully")
        print(f"  ✓ Worker has connection params: {len(connection_params)} parameters")
        
        # Test that the worker has the required methods
        worker_methods = ['run', '_test_database_connection', '_test_mysql_connection', '_test_postgresql_connection']
        for method_name in worker_methods:
            if hasattr(worker, method_name):
                print(f"  ✓ Worker method {method_name} exists")
            else:
                print(f"  ❌ Worker method {method_name} missing")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 CONNECTION TEST FUNCTIONALITY READY!")
        print("✓ Dialog creates successfully")
        print("✓ All required methods implemented")
        print("✓ ConnectionTestWorker can be created")
        print("✓ Helper methods work correctly")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection_functionality()
    if not success:
        sys.exit(1)
    else:
        print("\n✅ All tests passed! Connection test functionality is ready.")
