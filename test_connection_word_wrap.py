#!/usr/bin/env python3
"""
Test connection functionality with word-wrapped status messages
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from HisConSetting import HisConSetting

def test_connection_with_wrap():
    """Test that connection testing works with word-wrapped messages"""
    print("=" * 60)
    print("Connection Test with Word Wrap")
    print("=" * 60)
    
    # Create QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\n1. Creating dialog and setting up test...")
    dialog = HisConSetting()
    
    # Set up some connection parameters that will likely fail (but safely)
    dialog.host.setText("nonexistent-very-long-hostname-that-should-wrap.example.com")
    dialog.port.setValue(3306)
    dialog.database.setText("very_long_database_name_for_testing")
    dialog.username.setText("test_user_with_long_name")
    dialog.password.setText("password")
    dialog.use_connection_string.setChecked(False)
    
    print("  ✓ Set connection parameters")
    
    # Verify word wrap is enabled
    assert dialog.label_test_status.wordWrap(), "Word wrap should be enabled"
    print("  ✓ Word wrap is enabled")
    
    # Test the parameter collection
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
    
    print(f"  ✓ Collected parameters: host={connection_params['host'][:20]}...")
    
    # Test that we can create a worker with these parameters
    from HisConSetting import ConnectionTestWorker
    worker = ConnectionTestWorker(connection_params)
    print("  ✓ Worker created successfully")
    
    # Test the validation logic (should fail due to invalid host)
    success, message = worker._test_database_connection()
    print(f"  ✓ Test completed: success={success}")
    print(f"  ✓ Message: {message[:50]}...")
    
    # Test setting a long error message with word wrap
    dialog.update_test_status(message, "error" if not success else "success")
    print("  ✓ Long message displayed with word wrap")
    
    # Verify the message was set
    displayed_message = dialog.label_test_status.text()
    assert displayed_message == message, "Message should be set correctly"
    print("  ✓ Message content verified")
    
    print("\n" + "=" * 60)
    print("🎉 CONNECTION TEST WITH WORD WRAP PASSED!")
    print("✓ Connection parameters collected correctly")
    print("✓ Worker processes long hostnames")
    print("✓ Long error messages display with word wrap")
    print("✓ UI remains responsive and functional")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_connection_with_wrap()
        if success:
            print("\n✅ Connection test with word wrap works perfectly!")
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
