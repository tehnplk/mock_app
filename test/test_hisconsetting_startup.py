#!/usr/bin/env python3
"""
Simple test to verify HisConSetting window can start
"""

import sys
import os
from PyQt6.QtWidgets import QApplication

# Add the parent directory to Python path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_hisconsetting_startup():
    """Test that HisConSetting window can be created and shown"""
    
    # Create application instance
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("Testing HisConSetting window startup...")
    
    try:
        # Import and create the HisConSetting dialog
        from HisConSetting import HisConSetting
        
        print("✓ Successfully imported HisConSetting")
        
        # Create the dialog
        dialog = HisConSetting()
        print("✓ Successfully created HisConSetting dialog")
        
        # Set window title for identification
        dialog.setWindowTitle("HIS Connection Settings - Test")
        
        # Show the dialog (don't use exec() to avoid blocking)
        dialog.show()
        print("✓ Successfully showed HisConSetting dialog")
        
        # Check that essential UI elements exist
        assert hasattr(dialog, 'his_name'), "Missing his_name combobox"
        assert hasattr(dialog, 'db_system'), "Missing db_system combobox"
        assert hasattr(dialog, 'host'), "Missing host field"
        assert hasattr(dialog, 'port'), "Missing port field"
        assert hasattr(dialog, 'database'), "Missing database field"
        assert hasattr(dialog, 'username'), "Missing username field"
        assert hasattr(dialog, 'password'), "Missing password field"
        assert hasattr(dialog, 'btn_test_connection'), "Missing test connection button"
        assert hasattr(dialog, 'btn_save'), "Missing save button"
        assert hasattr(dialog, 'btn_cancel'), "Missing cancel button"
        
        print("✓ All essential UI elements are present")
        
        # Test that settings are loaded correctly
        assert dialog.his_name.currentText() in ["HOSXP", "JHCIS", "Other"], "Invalid HIS name selection"
        assert dialog.db_system.currentText() in ["MySQL", "MariaDB", "PostgreSQL"], "Invalid DB system selection"
        
        print("✓ Default values are set correctly")
        
        # Test getting connection parameters
        params = dialog.get_connection_params()
        assert isinstance(params, dict), "get_connection_params should return a dict"
        required_keys = ['host', 'port', 'database', 'username', 'password', 'db_system', 'his_name']
        for key in required_keys:
            assert key in params, f"Missing key '{key}' in connection parameters"
        
        print("✓ Connection parameters method works correctly")
        
        # Close the dialog
        dialog.close()
        print("✓ Successfully closed dialog")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_only():
    """Test that the UI file works independently"""
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting HisConSetting_ui independently...")
    
    try:
        from PyQt6.QtWidgets import QDialog
        from HisConSetting_ui import HisConSetting_ui
        
        print("✓ Successfully imported HisConSetting_ui")
        
        # Create a dialog and set up the UI
        dialog = QDialog()
        ui = HisConSetting_ui()
        ui.setupUi(dialog)
        
        print("✓ Successfully set up UI")
        
        # Show the dialog briefly
        dialog.setWindowTitle("HIS Connection Settings UI - Test")
        dialog.show()
        
        print("✓ Successfully showed UI dialog")
        
        # Check UI elements exist
        assert hasattr(ui, 'his_name'), "Missing his_name combobox"
        assert hasattr(ui, 'db_system'), "Missing db_system combobox"
        
        print("✓ UI elements are present")
        
        dialog.close()
        print("✓ Successfully closed UI dialog")
        
        return True
        
    except Exception as e:
        print(f"✗ UI test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = True
    
    try:
        # Test UI independently first
        success &= test_ui_only()
        
        # Test full HisConSetting dialog
        success &= test_hisconsetting_startup()
        
        if success:
            print("\n✅ All startup tests passed! HisConSetting window can start successfully.")
        else:
            print("\n❌ Some startup tests failed.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
