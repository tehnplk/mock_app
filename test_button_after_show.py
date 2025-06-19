#!/usr/bin/env python3
"""
Test button visibility after showing the dialog
"""

import sys
from PyQt6.QtWidgets import QApplication
from HisConSetting import HisConSetting

def test_button_after_show():
    """Test button visibility after showing the dialog"""
    print("=" * 60)
    print("Test Button Visibility After Show")
    print("=" * 60)
    
    # Create QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\n1. Creating HisConSetting dialog...")
    dialog = HisConSetting()
    print("  ✓ Dialog created")
    
    # Check visibility before showing
    if hasattr(dialog, 'btn_test_connection'):
        print(f"  Button visible before show: {dialog.btn_test_connection.isVisible()}")
    
    # Show the dialog
    print("\n2. Showing dialog...")
    dialog.show()
    app.processEvents()  # Process any pending events
    print("  ✓ Dialog shown and processed")
    
    # Check visibility after showing
    if hasattr(dialog, 'btn_test_connection'):
        btn = dialog.btn_test_connection
        print(f"\n3. Button properties after show:")
        print(f"  Button visible: {btn.isVisible()}")
        print(f"  Button enabled: {btn.isEnabled()}")
        print(f"  Button text: '{btn.text()}'")
        
        if btn.parent():
            print(f"  Parent visible: {btn.parent().isVisible()}")
            print(f"  Parent type: {type(btn.parent())}")
        
        # Test the status label too
        if hasattr(dialog, 'label_test_status'):
            label = dialog.label_test_status
            print(f"  Status label visible: {label.isVisible()}")
            print(f"  Status label text: '{label.text()}'")
        
        # Test button functionality
        print(f"\n4. Testing button functionality...")
        original_text = btn.text()
        print(f"  Original button text: '{original_text}'")
        
        # Test that we can update the status
        dialog.update_test_status("Button visibility test successful!", "success")
        if hasattr(dialog, 'label_test_status'):
            new_status = dialog.label_test_status.text()
            print(f"  Updated status text: '{new_status}'")
        
        if btn.isVisible() and btn.isEnabled():
            print(f"\n🎉 SUCCESS!")
            print(f"✓ Test Connection button is now VISIBLE and functional")
            print(f"✓ Status label is working correctly")
            return True
        else:
            print(f"\n❌ Button still not visible or enabled")
            return False
    else:
        print("  ❌ Button attribute not found")
        return False

if __name__ == "__main__":
    success = test_button_after_show()
    if success:
        print("\n✅ Test Connection button is working correctly!")
    else:
        print("\n❌ Button visibility issue persists")
        sys.exit(1)
