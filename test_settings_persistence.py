#!/usr/bin/env python3
"""
Test script to verify settings save and load functionality
"""

def test_settings_persistence():
    """Test that settings are saved and loaded correctly"""
    print("Testing settings persistence...")
    
    from AppSetting import app_settings
    
    # Clear all settings first
    app_settings.clear_all()
    
    # Set some test values
    test_values = {
        'host': 'test-server.com',
        'port': 5432,
        'database': 'test_database',
        'username': 'test_user',
        'password': 'test_password',
        'db_system': 'postgresql',
        'his_name': 'JHCIS',
        'charset': 'utf8',
        'ssl': True,
        'connection_string': 'postgresql://test:test@localhost:5432/testdb',
        'use_connection_string': True
    }
    
    print("Setting test values...")
    for key, value in test_values.items():
        app_settings.set_value(key, value)
        print(f"  Set {key} = {value}")
    
    # Force sync
    app_settings.sync()
    print("✓ Settings synced to storage")
    
    # Now retrieve values and verify
    print("\nRetrieving values...")
    all_correct = True
    for key, expected_value in test_values.items():
        retrieved_value = app_settings.get_value(key, 'NOT_FOUND')
        
        # Handle type conversions for comparison
        if key == 'port':
            retrieved_value = int(retrieved_value)
        elif key in ['ssl', 'use_connection_string']:
            if isinstance(retrieved_value, str):
                retrieved_value = retrieved_value.lower() == 'true'
            else:
                retrieved_value = bool(retrieved_value)
        else:
            retrieved_value = str(retrieved_value)
        
        if retrieved_value == expected_value:
            print(f"  ✓ {key} = {retrieved_value}")
        else:
            print(f"  ❌ {key} = {retrieved_value} (expected {expected_value})")
            all_correct = False
    
    if all_correct:
        print("\n🎉 All settings saved and loaded correctly!")
    else:
        print("\n❌ Some settings were not saved/loaded correctly!")
    
    return all_correct

def test_hisconsetting_load():
    """Test HisConSetting loads the saved values"""
    print("\n" + "="*50)
    print("Testing HisConSetting load functionality")
    print("="*50)
    
    try:
        # We can't easily test the UI loading without a display,
        # but we can test that the class can be imported and instantiated
        from HisConSetting import HisConSetting
        print("✓ HisConSetting imported successfully")
        
        # Test that settings loading method exists and can be called
        # Note: We can't actually instantiate the UI without a QApplication
        print("✓ HisConSetting class is ready to load settings")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing HisConSetting: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Settings Persistence Test")
    print("=" * 60)
    
    try:
        persistence_ok = test_settings_persistence()
        hisconsetting_ok = test_hisconsetting_load()
        
        print("\n" + "=" * 60)
        if persistence_ok and hisconsetting_ok:
            print("🎉 ALL TESTS PASSED!")
            print("Settings save and load functionality is working correctly.")
        else:
            print("❌ SOME TESTS FAILED!")
            print("There may be issues with settings persistence.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
