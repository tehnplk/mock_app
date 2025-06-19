#!/usr/bin/env python3
"""
Detailed debugging of the button visibility issue
"""

import sys
from PyQt6.QtWidgets import QApplication
from HisConSetting import HisConSetting

def debug_button_issue():
    """Debug why the Test Connection button is not visible"""
    print("=" * 60)
    print("Debug Button Visibility Issue")
    print("=" * 60)
    
    # Create QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\n1. Creating dialog and checking hierarchy...")
    dialog = HisConSetting()
    
    print(f"  Dialog class: {type(dialog)}")
    print(f"  Dialog size: {dialog.size()}")
    print(f"  Dialog visible: {dialog.isVisible()}")
    
    # Check if button exists
    if hasattr(dialog, 'btn_test_connection'):
        btn = dialog.btn_test_connection
        print(f"\n2. Button properties:")
        print(f"  Button exists: True")
        print(f"  Button type: {type(btn)}")
        print(f"  Button text: '{btn.text()}'")
        print(f"  Button visible: {btn.isVisible()}")
        print(f"  Button enabled: {btn.isEnabled()}")
        print(f"  Button size: {btn.size()}")
        print(f"  Button parent: {btn.parent()}")
        
        # Check parent hierarchy
        parent = btn.parent()
        level = 1
        while parent and level < 5:
            print(f"  Parent {level}: {type(parent)} - visible: {parent.isVisible()}")
            parent = parent.parent()
            level += 1
            
        # Try to show the button explicitly
        print(f"\n3. Trying to make button visible...")
        btn.show()
        print(f"  Button visible after show(): {btn.isVisible()}")
        
        # Check if parent widgets are visible
        if btn.parent():
            btn.parent().show()
            print(f"  Parent visible after show(): {btn.parent().isVisible()}")
    else:
        print("  ❌ Button does not exist!")
        return False
    
    # Check if label exists and is visible
    if hasattr(dialog, 'label_test_status'):
        label = dialog.label_test_status
        print(f"\n4. Label properties:")
        print(f"  Label visible: {label.isVisible()}")
        print(f"  Label text: '{label.text()}'")
        print(f"  Label parent: {label.parent()}")
    
    # Show the dialog to see what's actually displayed
    print(f"\n5. Showing dialog for visual inspection...")
    dialog.show()
    print(f"  Dialog shown")
    
    return True

if __name__ == "__main__":
    debug_button_issue()
    print("\n🔍 Debug complete. Check the output above for clues.")
