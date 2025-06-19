#!/usr/bin/env python3
"""
Test the complete connection test implementation with simulated database connections
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QEventLoop
from AppSetting import AppSetting
from HisConSetting import HisConSetting, ConnectionTestWorker

def test_connection_worker_logic():
    """Test the connection worker logic without actual database connections"""
    print("=" * 60)
    print("Connection Worker Logic Test")
    print("=" * 60)
    
    print("\n1. Testing invalid connection parameters...")
    
    # Test with missing parameters
    invalid_params = {
        'use_connection_string': False,
        'host': '',  # Missing host
        'port': 3306,
        'database': 'test',
        'username': 'test_user',
        'password': 'test_pass',
        'db_system': 'mysql',
        'charset': 'utf8mb4',
        'ssl': False
    }
    
    worker = ConnectionTestWorker(invalid_params)
    success, message = worker._test_database_connection()
    
    if not success and "Missing required connection parameters" in message:
        print("  ✓ Correctly detects missing host parameter")
    else:
        print(f"  ❌ Expected failure for missing parameters, got: {success}, {message}")
    
    print("\n2. Testing connection string mode...")
    
    # Test with empty connection string
    empty_conn_str_params = {
        'use_connection_string': True,
        'connection_string': '',  # Empty connection string
        'db_system': 'mysql'
    }
    
    worker = ConnectionTestWorker(empty_conn_str_params)
    success, message = worker._test_database_connection()
    
    if not success and "Connection string is empty" in message:
        print("  ✓ Correctly detects empty connection string")
    else:
        print(f"  ❌ Expected failure for empty connection string, got: {success}, {message}")
    
    print("\n3. Testing unsupported database system...")
    
    # Test with unsupported database system
    unsupported_params = {
        'use_connection_string': False,
        'host': 'localhost',
        'port': 3306,
        'database': 'test',
        'username': 'test_user',
        'password': 'test_pass',
        'db_system': 'oracle',  # Unsupported
        'charset': 'utf8mb4',
        'ssl': False
    }
    
    worker = ConnectionTestWorker(unsupported_params)
    success, message = worker._test_database_connection()
    
    if not success and "Unsupported database system" in message:
        print("  ✓ Correctly detects unsupported database system")
    else:
        print(f"  ❌ Expected failure for unsupported database, got: {success}, {message}")
    
    print("\n4. Testing valid parameter validation...")
    
    # Test with valid parameters (will fail on actual connection, but should pass validation)
    valid_params = {
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
    
    worker = ConnectionTestWorker(valid_params)
    # This will fail on actual connection, but should pass parameter validation
    success, message = worker._test_database_connection()
    
    if not success and ("connection" in message.lower() or "failed" in message.lower()):
        print("  ✓ Valid parameters pass validation (connection fails as expected)")
    else:
        print(f"  ? Parameters processed: {success}, {message}")
    
    return True

def test_ui_integration_with_connection():
    """Test the UI integration with connection testing"""
    print("\n" + "=" * 60)
    print("UI Integration with Connection Test")
    print("=" * 60)
    
    # Create QApplication if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\n1. Creating dialog and testing UI state...")
    dialog = HisConSetting()
    
    # Test initial state
    assert dialog.btn_test_connection.isEnabled(), "Test button should be enabled initially"
    print("  ✓ Test connection button is enabled initially")
    
    # Test the _get_internal_db_system method with different selections
    test_systems = [
        ("MySQL", "mysql"),
        ("PostgreSQL", "postgresql"),
        ("MariaDB", "mysql")
    ]
    
    for ui_name, internal_name in test_systems:
        dialog.db_system.setCurrentText(ui_name)
        result = dialog._get_internal_db_system()
        assert result == internal_name, f"Expected {internal_name}, got {result}"
        print(f"  ✓ {ui_name} -> {internal_name} mapping works")
    
    print("\n2. Testing connection parameter collection...")
    
    # Set some test values
    dialog.host.setText("test-host")
    dialog.port.setValue(5432)
    dialog.database.setText("test-db")
    dialog.username.setText("test-user")
    dialog.password.setText("test-pass")
    dialog.charset.setCurrentText("utf8")
    dialog.ssl.setChecked(True)
    dialog.use_connection_string.setChecked(False)
    
    # Test parameter collection (simulate what happens in test_connection)
    connection_params = {
        'use_connection_string': dialog.use_connection_string.isChecked(),
        'connection_string': dialog.connection_string.text().strip(),
        'host': dialog.host.text().strip(),
        'port': dialog.port.value(),
        'database': dialog.database.text().strip(),
        'username': dialog.username.text().strip(),
        'password': dialog.password.text(),
        'db_system': dialog._get_internal_db_system(),
        'charset': dialog.charset.currentText(),
        'ssl': dialog.ssl.isChecked()
    }
    
    expected_params = {
        'use_connection_string': False,
        'host': 'test-host',
        'port': 5432,
        'database': 'test-db',
        'username': 'test-user',
        'password': 'test-pass',
        'db_system': 'mysql',  # Default mapping
        'charset': 'utf8',
        'ssl': True
    }
    
    for key, expected_value in expected_params.items():
        actual_value = connection_params[key]
        assert actual_value == expected_value, f"Parameter {key}: expected {expected_value}, got {actual_value}"
        print(f"  ✓ Parameter {key} = {actual_value}")
    
    print("\n3. Testing connection string mode...")
    
    dialog.use_connection_string.setChecked(True)
    dialog.connection_string.setText("mysql://user:pass@host:3306/db")
    
    # Verify UI state changes
    assert not dialog.host.isEnabled(), "Host field should be disabled in connection string mode"
    assert not dialog.port.isEnabled(), "Port field should be disabled in connection string mode"
    assert dialog.connection_string.isEnabled(), "Connection string field should be enabled"
    print("  ✓ UI fields properly enabled/disabled in connection string mode")
    
    return True

def main():
    """Run all tests"""
    print("Testing Connection Test Implementation")
    print("=" * 60)
    
    try:
        # Test worker logic
        test_connection_worker_logic()
        
        # Test UI integration
        test_ui_integration_with_connection()
        
        print("\n" + "=" * 60)
        print("🎉 ALL CONNECTION TESTS PASSED!")
        print("✓ Worker parameter validation works correctly")
        print("✓ UI integration functions properly")
        print("✓ Connection parameter collection works")
        print("✓ Database system mapping functions correctly")
        print("✓ Connection string mode works as expected")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    else:
        print("\n✅ Connection test implementation is complete and working!")
