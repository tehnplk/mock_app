#!/usr/bin/env python3
"""
Test runner for HIS Application tests
"""

import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def run_all_tests():
    """Run all tests in the test directory"""
    
    print("=" * 60)
    print("Running HIS Application Test Suite")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Window Startup Test
    print("\n1. Testing Window Startup...")
    try:
        from test_window_startup import test_hisconsetting_window
        result = test_hisconsetting_window()
        test_results.append(("Window Startup", result))
    except Exception as e:
        print(f"✗ Window startup test failed: {e}")
        test_results.append(("Window Startup", False))
    
    # Test 2: HisConSetting Startup Test
    print("\n2. Testing HisConSetting Startup...")
    try:
        from test_hisconsetting_startup import test_hisconsetting_startup
        result = test_hisconsetting_startup()
        test_results.append(("HisConSetting Startup", result))
    except Exception as e:
        print(f"✗ HisConSetting startup test failed: {e}")
        test_results.append(("HisConSetting Startup", False))
    
    # Test 3: Integration Test
    print("\n3. Testing HisConSetting Integration...")
    try:
        from test_hisconsetting_integration import test_settings_integration, test_connection_test
        result1 = test_settings_integration()
        result2 = test_connection_test()
        result = result1 and result2
        test_results.append(("HisConSetting Integration", result))
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        test_results.append(("HisConSetting Integration", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "PASS" if result else "FAIL"
        icon = "✅" if result else "❌"
        print(f"{icon} {test_name}: {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {len(test_results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
