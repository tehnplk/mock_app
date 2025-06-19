#!/usr/bin/env python3
"""
Simple test to check if HisConSetting window can start
"""

import sys
import os
from PyQt6.QtWidgets import QApplication

# Add the parent directory to Python path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_hisconsetting_window():
    """Test that HisConSetting window can be created and shown"""
    
    print("Testing HisConSetting window startup...")
    
    try:
        # Import the modules
        from HisConSetting import HisConSetting
        print("✓ Successfully imported HisConSetting")
        
        # Create application instance
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✓ QApplication created")
        
        # Create the dialog
        dialog = HisConSetting()
        print("✓ HisConSetting dialog created successfully")
        
        # Try to show the dialog
        dialog.show()
        print("✓ Dialog shown successfully")
        
        # Check that all expected UI elements exist
        expected_attributes = [
            'his_name', 'db_system', 'host', 'port', 'database', 
            'username', 'password', 'charset', 'ssl',
            'use_connection_string', 'connection_string',
            'btn_test_connection', 'btn_save', 'btn_cancel',
            'label_test_status'
        ]
        
        missing_attributes = []
        for attr in expected_attributes:
            if not hasattr(dialog, attr):
                missing_attributes.append(attr)
        
        if missing_attributes:
            print(f"✗ Missing UI attributes: {missing_attributes}")
            return False
        else:
            print("✓ All expected UI attributes present")
        
        # Test that the dialog is properly configured
        assert dialog.windowTitle() == "HIS Database Connection Settings"
        assert dialog.isModal() == True
        print("✓ Dialog properties configured correctly")
        
        # Close the dialog
        dialog.close()
        print("✓ Dialog closed successfully")
        
        print("\n🎉 HisConSetting window test PASSED!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_hisconsetting_window()
    
    if success:
        print("\n✅ HisConSetting window can start successfully!")
        sys.exit(0)
    else:
        print("\n❌ HisConSetting window failed to start.")
        sys.exit(1)
