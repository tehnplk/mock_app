#!/usr/bin/env python3
"""
Integration test for HisConSetting UI functionality.
Tests that the UI properly loads and saves settings.
"""

import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import Qt
from AppSetting import AppSetting
from HisConSetting import HisConSetting

def test_ui_integration():
    """Test the complete UI integration."""
    print("=" * 60)
    print("HisConSetting UI Integration Test")
    print("=" * 60)
    
    # Initialize app settings
    app_settings = AppSetting()
    
    # Set some test values
    print("\n1. Setting test values in AppSetting...")
    test_values = {
        'host': 'ui-test-server.com',
        'port': 8080,
        'database': 'ui_test_db',
        'username': 'ui_test_user',
        'password': 'ui_test_pass',
        'db_system': 'postgresql',
        'his_name': 'JHCIS',
        'charset': 'utf8',
        'ssl': True,
        'connection_string': 'postgresql://ui:test@localhost:8080/uitest',
        'use_connection_string': False
    }
    
    for key, value in test_values.items():
        app_settings.set_value(key, value)
        print(f"  ✓ Set {key} = {value}")
    
    # Sync settings
    app_settings.sync()
    print("  ✓ Settings synced to storage")
    
    # Create QApplication if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\n2. Creating HisConSetting dialog...")
    try:
        dialog = HisConSetting()
        print("  ✓ Dialog created successfully")
        
        # Verify UI values match saved settings
        print("\n3. Verifying UI values match saved settings...")
        
        # Test text fields
        assert dialog.host.text() == test_values['host'], f"Host mismatch: {dialog.host.text()} != {test_values['host']}"
        print(f"  ✓ Host: {dialog.host.text()}")
        
        assert dialog.port.value() == test_values['port'], f"Port mismatch: {dialog.port.value()} != {test_values['port']}"
        print(f"  ✓ Port: {dialog.port.value()}")
        
        assert dialog.database.text() == test_values['database'], f"Database mismatch"
        print(f"  ✓ Database: {dialog.database.text()}")
        
        assert dialog.username.text() == test_values['username'], f"Username mismatch"
        print(f"  ✓ Username: {dialog.username.text()}")
        
        assert dialog.password.text() == test_values['password'], f"Password mismatch"
        print(f"  ✓ Password: {dialog.password.text()}")
        
        # Test comboboxes
        assert dialog.his_name.currentText() == test_values['his_name'], f"HIS name mismatch"
        print(f"  ✓ HIS Name: {dialog.his_name.currentText()}")
        
        assert dialog.charset.currentText() == test_values['charset'], f"Charset mismatch"
        print(f"  ✓ Charset: {dialog.charset.currentText()}")
        
        # Test checkboxes
        assert dialog.ssl.isChecked() == test_values['ssl'], f"SSL mismatch"
        print(f"  ✓ SSL: {dialog.ssl.isChecked()}")
        
        assert dialog.use_connection_string.isChecked() == test_values['use_connection_string'], f"Use connection string mismatch"
        print(f"  ✓ Use Connection String: {dialog.use_connection_string.isChecked()}")
        
        # Test connection string
        assert dialog.connection_string.text() == test_values['connection_string'], f"Connection string mismatch"
        print(f"  ✓ Connection String: {dialog.connection_string.text()}")
        
        print("\n4. Testing settings save...")
        
        # Change some values in the UI
        dialog.host.setText("modified-host.com")
        dialog.port.setValue(9999)
        dialog.database.setText("modified_db")
        
        # Trigger save
        dialog.save_settings()
        print("  ✓ Settings saved via save_settings()")
        
        # Verify the changes were saved
        saved_host = app_settings.get_value('host')
        saved_port = app_settings.get_value('port')
        saved_database = app_settings.get_value('database')
        
        assert saved_host == "modified-host.com", f"Host not saved correctly: {saved_host}"
        assert int(saved_port) == 9999, f"Port not saved correctly: {saved_port}"
        assert saved_database == "modified_db", f"Database not saved correctly: {saved_database}"
        
        print(f"  ✓ Modified host saved: {saved_host}")
        print(f"  ✓ Modified port saved: {saved_port}")
        print(f"  ✓ Modified database saved: {saved_database}")
        
        print("\n" + "=" * 60)
        print("🎉 UI INTEGRATION TEST PASSED!")
        print("✓ Dialog loads settings correctly")
        print("✓ Dialog saves settings correctly")
        print("✓ All UI elements work as expected")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ui_integration()
    if not success:
        sys.exit(1)
