#!/usr/bin/env python3
"""
Force visibility test and verify the dialog structure
"""

import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from HisConSetting import HisConSetting

def force_visibility_test():
    """Force all components to be visible and test the structure"""
    print("=" * 60)
    print("Force Visibility Test")
    print("=" * 60)
    
    # Create QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\n1. Creating dialog...")
    dialog = HisConSetting()
    
    # Force the dialog to show and update
    dialog.show()
    app.processEvents()
    
    print(f"  Dialog shown and processed")
    
    # Get all widgets in the dialog
    print(f"\n2. Checking all child widgets:")
    def print_widget_tree(widget, level=0):
        indent = "  " * level
        visible = "✓" if widget.isVisible() else "❌"
        print(f"{indent}{visible} {widget.__class__.__name__}: {getattr(widget, 'text', lambda: getattr(widget, 'title', lambda: str(widget))())()}")
        
        for child in widget.findChildren(QWidget):
            if child.parent() == widget:  # Only direct children
                print_widget_tree(child, level + 1)
                if level < 2:  # Prevent too deep recursion
                    break
    
    print_widget_tree(dialog)
    
    # Specifically check for our test section components
    print(f"\n3. Searching for test components...")
    
    # Find all QPushButton objects
    buttons = dialog.findChildren(type(dialog.btn_test_connection))
    print(f"  Found {len(buttons)} QPushButton(s):")
    for i, btn in enumerate(buttons):
        print(f"    Button {i}: '{btn.text()}' - Visible: {btn.isVisible()}")
        if 'test' in btn.text().lower():
            print(f"      This is our test button!")
            # Force it visible
            btn.show()
            btn.setVisible(True)
            if btn.parent():
                btn.parent().show()
                btn.parent().setVisible(True)
            print(f"      Forced visible: {btn.isVisible()}")
    
    # Find all QGroupBox objects
    from PyQt6.QtWidgets import QGroupBox
    groups = dialog.findChildren(QGroupBox)
    print(f"\n  Found {len(groups)} QGroupBox(es):")
    for i, group in enumerate(groups):
        print(f"    Group {i}: '{group.title()}' - Visible: {group.isVisible()}")
        if 'connection test' in group.title().lower() or 'test' in group.title().lower():
            print(f"      This is our test group!")
            # Force it visible
            group.show()
            group.setVisible(True)
            print(f"      Forced visible: {group.isVisible()}")
    
    # Update the display
    app.processEvents()
    
    print(f"\n4. Final check after forcing visibility...")
    if hasattr(dialog, 'btn_test_connection'):
        btn = dialog.btn_test_connection
        print(f"  Test button visible: {btn.isVisible()}")
        print(f"  Test button parent visible: {btn.parent().isVisible() if btn.parent() else 'No parent'}")
    
    # Keep the dialog open for visual inspection
    print(f"\n5. Dialog is now open for visual inspection...")
    print(f"   (Close the dialog window to continue)")
    
    # Don't actually exec the dialog as it would block, just show what we found
    return True

if __name__ == "__main__":
    force_visibility_test()
    print("\n✅ Test complete. Check if the button is now visible in the dialog.")
