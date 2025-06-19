import sys

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QGroupBox,
    QTabWidget,
    QWidget,
    QTextEdit,
    QMessageBox,
    QApplication,
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QLocale


class HisConSetting_ui(object):
    """
    UI class for HIS Database Connection Settings Dialog.
    """
    
    def setupUi(self, HisConSetting_ui):
        """
        Set up the user interface for HIS Connection Settings.
        """
        # Set locale to US English for number formatting
        QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        
        HisConSetting_ui.setWindowTitle("HIS Database Connection Settings")
        HisConSetting_ui.setModal(True)  # Make it modal
        HisConSetting_ui.setFixedWidth(600)  # Set window width to 600px        # Main layout
        main_layout = QVBoxLayout(HisConSetting_ui)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create connection form directly
        self.create_connection_form(main_layout)
        # Create connection test section
        self.create_test_section(main_layout)
        # Create button section
        self.create_button_section(main_layout)

    def create_connection_form(self, parent_layout):
        """Create connection form directly without tabs"""        # System Selection group
        system_group = QGroupBox("System Selection")
        system_layout = QFormLayout(system_group)
        
        # HIS Name selection
        self.his_name = QComboBox()
        self.his_name.addItems(["HOSXP", "JHCIS", "Other"])
        self.his_name.setCurrentText("HOSXP")  # Default selection
        self.his_name.setStyleSheet(
            "QComboBox { padding: 8px; font-size: 12px; min-height: 20px; }"
        )
        
        # Database System selection
        self.db_system = QComboBox()
        self.db_system.addItems(
            [
                "MySQL",
                "MariaDB",
                "PostgreSQL",
            ]
        )
        self.db_system.setCurrentText("MySQL")
        self.db_system.setStyleSheet(
            "QComboBox { padding: 8px; font-size: 12px; min-height: 20px; }"
        )        # Add widgets to form layout for full width
        system_layout.addRow("HIS:", self.his_name)
        system_layout.addRow("Database:", self.db_system)
        
        # Connection Settings group
        conn_group = QGroupBox("Connection Settings")
        conn_layout = QFormLayout(conn_group)
        
        self.host = QLineEdit()
        self.host.setText("localhost")
        self.host.setPlaceholderText("localhost or IP address")
        self.host.setStyleSheet(
            "QLineEdit { padding: 8px; font-size: 12px; min-height: 20px; }"
        )

        self.port = QSpinBox()
        self.port.setRange(1, 65535)
        self.port.setValue(3306)
        self.port.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        self.port.setStyleSheet(
            "QSpinBox { padding: 8px; font-size: 12px; min-height: 20px; }"
        )

        self.database = QLineEdit()
        self.database.setPlaceholderText("Database name")
        self.database.setStyleSheet(
            "QLineEdit { padding: 8px; font-size: 12px; min-height: 20px; }"
        )

        self.username = QLineEdit()
        self.username.setPlaceholderText("Database username")
        self.username.setStyleSheet(
            "QLineEdit { padding: 8px; font-size: 12px; min-height: 20px; }"
        )

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Database password")
        self.password.setStyleSheet(
            "QLineEdit { padding: 8px; font-size: 12px; min-height: 20px; }"
        )

        self.charset = QComboBox()
        self.charset.addItems(["utf8", "utf8mb4", "tis620", "latin1", "ascii"])
        self.charset.setCurrentText("utf8mb4")

        # Connection string with checkbox
        self.use_connection_string = QCheckBox("Use Connection String")
        self.connection_string = QLineEdit()
        self.connection_string.setPlaceholderText("Custom connection string (optional)")
        self.connection_string.setStyleSheet(
            "QLineEdit { padding: 8px; font-size: 12px; min-height: 20px; }"
        )
        self.connection_string.setEnabled(False)  # Initially disabled

        conn_layout.addRow("Server Host:", self.host)
        conn_layout.addRow("Port:", self.port)
        conn_layout.addRow("Database:", self.database)
        conn_layout.addRow("Username:", self.username)
        conn_layout.addRow("Password:", self.password)
        conn_layout.addRow("Charset:", self.charset)
        conn_layout.addRow(self.use_connection_string, self.connection_string)

        # Advanced Settings group
        adv_group = QGroupBox("Advanced Settings")
        adv_layout = QFormLayout(adv_group)

        self.ssl = QCheckBox("Use SSL/Secure Connection")

        adv_layout.addRow("SSL:", self.ssl)
        
        # Connect signals for dynamic updates
        self.his_name.currentTextChanged.connect(self.on_his_name_changed)
        self.db_system.currentTextChanged.connect(self.on_db_system_changed)
        self.use_connection_string.toggled.connect(self.connection_string.setEnabled)

        parent_layout.addWidget(system_group)
        parent_layout.addWidget(conn_group)
        parent_layout.addWidget(adv_group)

    def on_his_name_changed(self, his_name):
        """Handle HIS name selection change"""
        if his_name == "HOSXP":
            self.host.setText("192.168.1.1")
            self.port.setValue(3306)
            self.database.setText("hosxp_pcu")
            self.charset.setCurrentText("tis620")
        elif his_name == "JHCIS":
            self.host.setText("192.168.1.1")
            self.port.setValue(3333)
            self.database.setText("jhcisdb")
            self.charset.setCurrentText("utf8")
        else:
            self.host.setText("localhost")
            self.port.setValue(3306)
            self.database.clear()
            self.charset.setCurrentText("utf8mb4")

    def on_db_system_changed(self, db_system):
        """Handle database system selection change"""
        if db_system == "MySQL" or db_system == "MariaDB":
            self.port.setValue(3306)
            self.charset.setCurrentText("utf8mb4")
        elif db_system == "PostgreSQL":
            self.port.setValue(5432)
            self.charset.setCurrentText("utf8")
            self.ssl.setChecked(True)
        else:
            self.port.setValue(3306)
            self.charset.setCurrentText("utf8mb4")

        # Ensure controls are properly enabled
        self.port.setEnabled(True)
        self.host.setText("localhost")
        self.host.setPlaceholderText("localhost or IP address")

    def create_test_section(self, parent_layout):
        """Create connection test section"""
        test_group = QGroupBox("Connection Test")
        test_layout = QVBoxLayout(test_group)        # Test button and status
        test_button_layout = QHBoxLayout()

        self.btn_test_connection = QPushButton("Test Connection")
        self.btn_test_connection.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """
        )

        self.label_test_status = QLabel("Ready to test connection")
        self.label_test_status.setStyleSheet("color: #7f8c8d; font-style: italic;")
        self.label_test_status.setWordWrap(True)  # Enable word wrapping for long messages

        test_button_layout.addWidget(self.btn_test_connection)
        test_button_layout.addSpacing(20)  # Add small fixed spacing instead of stretch
        test_button_layout.addWidget(self.label_test_status)
        test_button_layout.addStretch()  # Move stretch to the end to push everything left

        test_layout.addLayout(test_button_layout)

        parent_layout.addWidget(test_group)

    def create_button_section(self, parent_layout):
        """Create dialog buttons"""
        button_layout = QHBoxLayout()        # Save button
        self.btn_save = QPushButton("Save")
        self.btn_save.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """
        )

        # Cancel button
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet(
            """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #566573;
            }
        """
        )

        # Reset button
        self.btn_reset = QPushButton("Reset to Defaults")
        self.btn_reset.setStyleSheet(
            """
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
        """
        )

        button_layout.addWidget(self.btn_reset)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        parent_layout.addLayout(button_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = QDialog()
    ui = HisConSetting_ui()
    ui.setupUi(dialog)
    dialog.setWindowIcon(QIcon("icon.png"))  # Set your icon path here
    dialog.show()
    sys.exit(app.exec())