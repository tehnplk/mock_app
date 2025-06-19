"""
HIS Connection Settings UI Elements Documentation

This document describes the UI elements in HisConSetting_ui.py and their purposes.

## System Selection Group
1. **HIS Name** (self.his_name)
   - Type: QComboBox
   - Options: ["HOSXP", "JHCIS", "Other"]
   - Purpose: Select the specific Hospital Information System being used
   - Default: "HOSXP"
   - Triggers: on_his_name_changed() when selection changes

2. **Database System** (self.db_system)
   - Type: QComboBox
   - Options: ["MySQL", "MariaDB", "PostgreSQL"]
   - Purpose: Select the database engine type
   - Default: "MySQL"
   - Triggers: on_db_system_changed() when selection changes

## Connection Settings Group
3. **Server Host** (self.host)
   - Type: QLineEdit
   - Purpose: Database server hostname or IP address
   - Default: "localhost"
   - Placeholder: "localhost or IP address"

4. **Port** (self.port)
   - Type: QSpinBox
   - Range: 1-65535
   - Purpose: Database server port number
   - Default: 3306 (MySQL/MariaDB) or 5432 (PostgreSQL)

5. **Database** (self.database)
   - Type: QLineEdit
   - Purpose: Database name to connect to
   - Placeholder: "Database name"

6. **Username** (self.username)
   - Type: QLineEdit
   - Purpose: Database login username
   - Placeholder: "Database username"

7. **Password** (self.password)
   - Type: QLineEdit
   - Purpose: Database login password
   - Echo Mode: Password (hidden text)
   - Placeholder: "Database password"

8. **Charset** (self.charset)
   - Type: QComboBox
   - Options: ["utf8", "utf8mb4", "tis620", "latin1", "ascii"]
   - Purpose: Character encoding for database connection
   - Default: "utf8mb4"

9. **Use Connection String** (self.use_connection_string)
   - Type: QCheckBox
   - Purpose: Toggle between individual parameters vs connection string
   - When checked: Disables individual fields, enables connection string field

10. **Connection String** (self.connection_string)
    - Type: QLineEdit
    - Purpose: Custom database connection string
    - Initially disabled (enabled when checkbox is checked)
    - Placeholder: "Custom connection string (optional)"

## Advanced Settings Group
11. **SSL** (self.ssl)
    - Type: QCheckBox
    - Purpose: Enable SSL/secure connection to database
    - Default: False (except PostgreSQL defaults to True)

## Connection Test Section
12. **Test Connection Button** (self.btn_test_connection)
    - Type: QPushButton
    - Purpose: Test the database connection with current settings
    - Style: Blue button with hover effects

13. **Test Status Label** (self.label_test_status)
    - Type: QLabel
    - Purpose: Display connection test status/results
    - Style: Colored text based on status (success/error/warning)

14. **Test Results** (self.text_test_results)
    - Type: QTextEdit
    - Purpose: Display detailed test results
    - Read-only, monospace font, limited height

## Button Section
15. **Reset Button** (self.btn_reset)
    - Type: QPushButton
    - Purpose: Reset all fields to default values
    - Style: Orange button

16. **Save Button** (self.btn_save)
    - Type: QPushButton
    - Purpose: Save current settings and close dialog
    - Style: Green button

17. **Cancel Button** (self.btn_cancel)
    - Type: QPushButton
    - Purpose: Close dialog without saving
    - Style: Gray button

## Data Flow
1. User selects HIS name → Triggers profile loading with predefined values
2. User selects database system → Adjusts port and other defaults
3. User fills connection details → Validates form fields
4. User tests connection → Shows results in test section
5. User saves settings → Stores to QSettings and closes dialog

## HIS Profiles
- **HOSXP**: Host=192.168.1.1, Port=3306, DB=hosxp_pcu, Charset=tis620
- **JHCIS**: Host=192.168.1.1, Port=3333, DB=jhcisdb, Charset=utf8
- **Other**: Host=localhost, Port=3306, Charset=utf8mb4

## Settings Storage
All values are stored in QSettings under:
- Organization: "HospitalApp"
- Application: "HIS_Database_Settings"
- Group: "Current"

Each UI element maps to a settings key with the same name.
"""
