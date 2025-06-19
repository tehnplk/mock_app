#!/usr/bin/env python3
"""
Test script to verify the complete HisConSetting implementation
"""

import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings

def test_hisconsetting_implementation():
    """Test the complete HisConSetting implementation"""
    
    print("Testing complete HisConSetting implementation...")
    
    try:
        # Create application instance
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Clear any existing settings for clean test
        settings = QSettings('YourCompany', 'HISApp')
        settings.clear()
        
        # Import and create HisConSetting
        from HisConSetting import HisConSetting
        dialog = HisConSetting()
        
        print("✓ HisConSetting dialog created successfully")
        
        # Test UI elements are present
        ui_elements = [
            'his_name', 'db_system', 'host', 'port', 'database',
            'username', 'password', 'charset', 'ssl',
            'use_connection_string', 'connection_string',
            'btn_test_connection', 'btn_save', 'btn_cancel', 'btn_reset',
            'label_test_status', 'text_test_results'
        ]
        
        missing_elements = []
        for element in ui_elements:
            if not hasattr(dialog, element):
                missing_elements.append(element)
        
        if missing_elements:
            print(f"✗ Missing UI elements: {missing_elements}")
            return False
        
        print("✓ All UI elements present")
        
        # Test default settings loading
        assert dialog.his_name.currentText() == "HOSXP"
        assert dialog.db_system.currentText() == "MySQL"
        print("✓ Default settings loaded correctly")
        
        # Test HIS name change functionality
        dialog.his_name.setCurrentText("JHCIS")
        # Should trigger profile loading
        assert dialog.database.text() == "jhcisdb"
        print("✓ HIS name change functionality works")
        
        # Test database system change
        dialog.db_system.setCurrentText("PostgreSQL")
        assert dialog.port.value() == 5432
        assert dialog.ssl.isChecked() == True
        print("✓ Database system change functionality works")
        
        # Test connection string toggle
        dialog.use_connection_string.setChecked(True)
        assert dialog.host.isEnabled() == False
        assert dialog.connection_string.isEnabled() == True
        print("✓ Connection string toggle works")
        
        # Test getting connection parameters
        params = dialog.get_connection_params()
        assert 'host' in params
        assert 'db_system' in params
        assert params['db_system'] == 'postgresql'  # Should be lowercase
        print("✓ Connection parameters retrieval works")
        
        # Test settings save/load
        dialog.host.setText("test-host")
        dialog.database.setText("test-db")
        test_params = dialog.get_connection_params()
        
        # Save settings
        for key, value in test_params.items():
            dialog.settings.setValue(key, value)
        
        # Create new dialog and verify settings loaded
        dialog2 = HisConSetting()
        assert dialog2.host.text() == "test-host"
        assert dialog2.database.text() == "test-db"
        print("✓ Settings save/load functionality works")
        
        # Test reset to defaults
        dialog2.reset_to_defaults()
        assert dialog2.his_name.currentText() == "HOSXP"
        print("✓ Reset to defaults functionality works")
        
        # Clean up
        dialog.close()
        dialog2.close()
        
        print("\n🎉 All HisConSetting implementation tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_hisconsetting_implementation()
    
    if success:
        print("\n✅ HisConSetting implementation is complete and functional!")
        sys.exit(0)
    else:
        print("\n❌ HisConSetting implementation has issues.")
        sys.exit(1)
