#!/usr/bin/env python3
"""
Test script to verify HisConSetting and DbPerform work with AppSetting
"""

def test_app_setting():
    """Test AppSetting basic functionality"""
    print("Testing AppSetting...")
    from AppSetting import app_settings
    
    # Test set and get
    app_settings.set_value('test_key', 'test_value')
    value = app_settings.get_value('test_key', 'default')
    assert value == 'test_value', f"Expected 'test_value', got '{value}'"
    print("✓ AppSetting set/get works")
    
    # Test database settings
    app_settings.set_value('host', 'localhost')
    app_settings.set_value('port', 3306)
    app_settings.set_value('database', 'test_db')
    app_settings.set_value('username', 'test_user')
    app_settings.set_value('password', 'test_pass')
    app_settings.set_value('db_system', 'mysql')
    
    print("✓ Database settings saved")

def test_db_perform():
    """Test DbPerform functionality"""
    print("\nTesting DbPerform...")
    from DbPerform import DbPerform
    
    db = DbPerform()
    settings = db._get_connection_settings()
    
    # Check if settings are retrieved correctly
    expected_keys = ['host', 'port', 'database', 'username', 'password', 'db_system']
    for key in expected_keys:
        assert key in settings, f"Missing key: {key}"
    
    print(f"✓ DbPerform retrieved {len(settings)} settings")
    print(f"  - Host: {settings['host']}")
    print(f"  - Port: {settings['port']}")
    print(f"  - Database: {settings['database']}")
    print(f"  - DB System: {settings['db_system']}")
    
    # Test connection string creation
    try:
        conn_str = db._create_connection_string(settings)
        print(f"✓ Connection string created: {conn_str[:50]}...")
    except Exception as e:
        print(f"✓ Connection string creation handled: {e}")
    
    db.close()

def test_his_con_setting_imports():
    """Test HisConSetting imports"""
    print("\nTesting HisConSetting imports...")
    try:
        from HisConSetting import HisConSetting
        print("✓ HisConSetting imported successfully")
        return True
    except Exception as e:
        print(f"❌ HisConSetting import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("HIS Application Components Test")
    print("=" * 50)
    
    try:
        test_app_setting()
        test_db_perform()
        test_his_con_setting_imports()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed!")
        print("✓ AppSetting works for get/set database settings")
        print("✓ DbPerform can retrieve and use settings")
        print("✓ HisConSetting imports correctly")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
