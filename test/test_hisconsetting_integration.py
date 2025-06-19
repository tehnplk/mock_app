#!/usr/bin/env python3
"""
Test script to verify HisConSetting integration with DbPerform
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings

# Add the parent directory to Python path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from HisConSetting import HisConSetting
from DbPerform import DbPerform


def test_settings_integration():
    """Test that HisConSetting and DbPerform use the same settings"""
    
    # Create application instance
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("Testing HisConSetting and DbPerform integration...")
    
    # Clear any existing settings for clean test
    settings = QSettings('YourCompany', 'HISApp')
    settings.clear()
    
    # Set test connection parameters
    test_params = {
        'host': 'localhost',
        'port': 3306,
        'database': 'test_db',
        'username': 'test_user',
        'password': 'test_pass',
        'db_system': 'mysql',
        'his_name': 'HOSXP',
        'charset': 'utf8mb4',
        'ssl': False,
        'use_connection_string': False,
        'connection_string': ''
    }
    
    # Save test parameters using QSettings directly (as DbPerform expects)
    for key, value in test_params.items():
        settings.setValue(key, value)
    
    print("✓ Test parameters saved to QSettings")
    
    # Test DbPerform can read the settings
    try:
        db_perform = DbPerform()
        db_settings = db_perform._get_connection_settings()
        
        print("✓ DbPerform successfully read settings:")
        for key, value in db_settings.items():
            print(f"  {key}: {value}")
        
        # Verify key values match
        assert db_settings['host'] == test_params['host']
        assert db_settings['port'] == test_params['port']
        assert db_settings['database'] == test_params['database']
        assert db_settings['username'] == test_params['username']
        assert db_settings['db_system'] == test_params['db_system']
        
        print("✓ DbPerform settings match expected values")
        
    except Exception as e:
        print(f"✗ DbPerform settings test failed: {e}")
        return False
    
    # Test HisConSetting can read the same settings
    try:
        his_con_setting = HisConSetting()
        
        # The load_settings method should have been called during __init__
        # Check that UI fields have the correct values
        assert his_con_setting.host.text() == test_params['host']
        assert his_con_setting.port.value() == test_params['port']
        assert his_con_setting.database.text() == test_params['database']
        assert his_con_setting.username.text() == test_params['username']
        assert his_con_setting.his_name.currentText() == test_params['his_name']
        
        print("✓ HisConSetting successfully loaded settings into UI")
        
        # Test getting parameters from UI
        ui_params = his_con_setting.get_connection_params()
        
        # Verify the UI returns correct db_system format (lowercase for DbPerform)
        assert ui_params['db_system'] == 'mysql'  # Should be lowercase
        assert ui_params['host'] == test_params['host']
        assert ui_params['port'] == test_params['port']
        
        print("✓ HisConSetting UI parameters correct")
        
    except Exception as e:
        print(f"✗ HisConSetting test failed: {e}")
        return False
    
    # Test connection string creation
    try:
        connection_string = db_perform._create_connection_string(db_settings)
        expected = "mysql+pymysql://test_user:test_pass@localhost:3306/test_db"
        
        assert connection_string == expected
        print(f"✓ Connection string created correctly: {connection_string}")
        
    except Exception as e:
        print(f"✗ Connection string test failed: {e}")
        return False
    
    print("\n🎉 All integration tests passed!")
    return True


def test_connection_test():
    """Test the connection testing functionality"""
    print("\nTesting connection functionality...")
    
    # Test with invalid settings (should fail gracefully)
    settings = QSettings('YourCompany', 'HISApp')
    settings.setValue('host', 'invalid_host_12345')
    settings.setValue('port', 3306)
    settings.setValue('database', 'test')
    settings.setValue('username', 'test')
    settings.setValue('password', 'test')
    settings.setValue('db_system', 'mysql')
    
    try:
        db_perform = DbPerform()
        success, message = db_perform.test_connection()
        
        print(f"✓ Connection test completed: success={success}")
        print(f"  Message: {message}")
        
        # Should fail with invalid host, but not crash
        assert not success
        assert "Connection Fail" in message
        
        print("✓ Connection test handles invalid connection gracefully")
        
    except Exception as e:
        print(f"✗ Connection test failed unexpectedly: {e}")
        return False
    
    return True


if __name__ == '__main__':
    success = True
    
    try:
        success &= test_settings_integration()
        success &= test_connection_test()
        
        if success:
            print("\n✅ All tests passed! HisConSetting and DbPerform are properly integrated.")
        else:
            print("\n❌ Some tests failed.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        sys.exit(1)
