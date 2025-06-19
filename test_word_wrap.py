#!/usr/bin/env python3
"""
Test the word wrap functionality for the test status label
"""

import sys
from PyQt6.QtWidgets import QApplication
from HisConSetting import HisConSetting

def test_word_wrap():
    """Test that the test status label supports word wrapping"""
    print("=" * 60)
    print("Test Status Label Word Wrap Test")
    print("=" * 60)
    
    # Create QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\n1. Creating HisConSetting dialog...")
    try:
        dialog = HisConSetting()
        print("  ✓ Dialog created successfully")
        
        # Check if the label has word wrap enabled
        if hasattr(dialog, 'label_test_status'):
            word_wrap_enabled = dialog.label_test_status.wordWrap()
            if word_wrap_enabled:
                print("  ✓ Word wrap is enabled on test status label")
            else:
                print("  ❌ Word wrap is NOT enabled on test status label")
                return False
        else:
            print("  ❌ label_test_status not found")
            return False
        
        print("\n2. Testing with a long message...")
        
        # Test with a very long error message
        long_message = "This is a very long connection error message that should wrap to multiple lines. MySQL connection failed: (2003, \"Can't connect to MySQL server on 'nonexistent-host.example.com' (110)\"). This message is intentionally long to test the word wrapping functionality of the status label."
        
        dialog.update_test_status(long_message, "error")
        print(f"  ✓ Set long message: {long_message[:50]}...")
        
        # Verify the message was set
        current_text = dialog.label_test_status.text()
        if current_text == long_message:
            print("  ✓ Long message set successfully")
        else:
            print("  ❌ Message not set correctly")
            return False
        
        print("\n3. Testing with different message types...")
        
        # Test different message types
        test_messages = [
            ("This is a normal short message", "normal"),
            ("Connection successful to very-long-hostname-that-might-cause-wrapping.example.com:3306/very_long_database_name_that_should_wrap", "success"),
            ("Testing connection to server with extremely long hostname and detailed error information...", "testing"),
            ("Warning: Connection parameters may be incorrect for this very long hostname configuration", "warning")
        ]
        
        for message, status_type in test_messages:
            dialog.update_test_status(message, status_type)
            print(f"  ✓ Tested {status_type} message: {message[:30]}...")
        
        print("\n" + "=" * 60)
        print("🎉 WORD WRAP TEST PASSED!")
        print("✓ Label has word wrap enabled")
        print("✓ Long messages can be set")
        print("✓ Different message types work correctly")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_word_wrap()
    if not success:
        sys.exit(1)
    else:
        print("\n✅ Word wrap functionality is working correctly!")
