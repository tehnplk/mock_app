# HIS Application Tests

This folder contains all test files for the HIS Application.

## Test Files

- `test_window_startup.py` - Tests basic window creation and startup
- `test_hisconsetting_startup.py` - Tests HisConSetting dialog startup
- `test_hisconsetting_integration.py` - Tests integration between HisConSetting and DbPerform
- `run_tests.py` - Test runner that executes all tests

## Running Tests

### Run all tests:
```bash
python test/run_tests.py
```

### Run individual tests:
```bash
python test/test_window_startup.py
python test/test_hisconsetting_startup.py
python test/test_hisconsetting_integration.py
```

## Test Structure

All tests follow a similar pattern:
1. Import required modules
2. Set up test environment
3. Execute test operations
4. Verify results
5. Clean up resources

Tests are designed to be independent and can be run in any order.
