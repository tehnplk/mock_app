import sys
import os
from datetime import datetime

from PyQt6.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, QSettings

from HisConSetting_ui import HisConSetting_ui

# Import database connection libraries
try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    import pymysql
    import psycopg2
except ImportError as e:
    print(f"Database libraries not found: {e}")


class ConnectionTestThread(QThread):
    """Thread for testing database connections without blocking the UI"""
    
    test_finished = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, connection_params):
        super().__init__()
        self.connection_params = connection_params
    
    def run(self):
        """Test the database connection in a separate thread"""
        try:
            success, message = self._test_real_connection()
            self.test_finished.emit(success, message)
            
        except Exception as e:
            self.test_finished.emit(False, f"❌ Connection Fail: {str(e)}")
    
    def _test_real_connection(self):
        """Perform actual database connection test"""
        host = self.connection_params.get('host', '')
        port = self.connection_params.get('port', 3306)
        database = self.connection_params.get('database', '')
        username = self.connection_params.get('username', '')
        password = self.connection_params.get('password', '')
        db_system = self.connection_params.get('db_system', 'MySQL')
        ssl = self.connection_params.get('ssl', False)
        charset = self.connection_params.get('charset', 'utf8mb4')
        connection_string = self.connection_params.get('connection_string', '')
        
        # Validate required parameters
        if not all([host, database, username]):
            return False, "❌ Connection Fail: Missing required connection parameters (host, database, username)"
        
        try:
            # Use custom connection string if provided
            if connection_string and connection_string.strip():
                connection_url = connection_string.strip()
            else:
                # Build connection string based on database system
                if db_system in ['MySQL', 'MariaDB']:
                    # MySQL/MariaDB connection string
                    connection_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset={charset}"
                    if ssl:
                        connection_url += "&ssl_disabled=false"
                        
                elif db_system == 'PostgreSQL':
                    # PostgreSQL connection string
                    connection_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
                    if ssl:
                        connection_url += "?sslmode=require"
                else:
                    return False, f"❌ Connection Fail: Unsupported database system - {db_system}"
            
            # Create engine and test connection
            engine = create_engine(
                connection_url,
                pool_timeout=10,
                pool_recycle=3600,
                echo=False
            )
            
            # Test connection by executing a simple query
            with engine.connect() as connection:
                if db_system == 'PostgreSQL':
                    result = connection.execute(text("SELECT version() as version"))
                else:  # MySQL/MariaDB
                    result = connection.execute(text("SELECT VERSION() as version"))
                
                # Simple success message
                return True, "✅ Connection Success"
                
        except SQLAlchemyError as e:
            error_msg = str(e)
            if "Access denied" in error_msg:
                return False, "❌ Connection Fail: Invalid username or password"
            elif "Can't connect" in error_msg or "Connection refused" in error_msg:
                return False, "❌ Connection Fail: Cannot connect to server - Check host and port"
            elif "Unknown database" in error_msg:
                return False, f"❌ Connection Fail: Database '{database}' does not exist"
            else:
                return False, f"❌ Connection Fail: {error_msg}"
                
        except Exception as e:
            return False, f"❌ Connection Fail: {str(e)}"



class HisConSetting(QDialog, HisConSetting_ui):
    """
    HIS Database Connection Settings Dialog.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Initialize variables
        self.test_thread = None
        self.settings = QSettings("HospitalApp", "HIS_Database_Settings")
        
        # Connect signals
        self.setup_connections()
        
        # Load existing settings
        self.load_settings()
        
        # Set initial state
        self.update_test_status("Ready to test connection", "normal")
    
    def setup_connections(self):
        """Connect UI signals to their handlers"""
        # Button connections
        self.btn_test_connection.clicked.connect(self.test_connection)
        self.btn_save.clicked.connect(self.save_settings)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_reset.clicked.connect(self.reset_to_defaults)
          # Connect HIS name and database system change handlers
        self.his_name.currentTextChanged.connect(self.on_his_name_changed)
        self.db_system.currentTextChanged.connect(self.on_db_system_changed)
        
    def on_his_name_changed(self):
        """Handle HIS name selection change"""
        his_name = self.his_name.currentText()
        # Set default values based on HIS selection
        if his_name == "HOSXP":
            self.host.setText("192.168.1.1")
            self.port.setValue(3306)
            self.database.setText("hosxp_pcu")
            self.username.setText("root")
            self.password.setText("")
            self.charset.setCurrentText("tis620")
        elif his_name == "JHCIS":
            self.host.setText("192.168.1.1")
            self.port.setValue(3333)
            self.database.setText("jhcisdb")
            self.username.setText("sa")
            self.password.setText("")
            self.charset.setCurrentText("utf8")
        else:  # Other
            self.host.setText("localhost")
            self.port.setValue(3306)
            self.database.clear()
            self.username.clear()
            self.password.clear()
            self.charset.setCurrentText("utf8mb4")
            
    def on_db_system_changed(self):
        """Handle database system selection change"""
        db_system = self.db_system.currentText()
        # Set default port based on database system
        if db_system == "MySQL" or db_system == "MariaDB":
            self.port.setValue(3306)
        elif db_system == "PostgreSQL":
            self.port.setValue(5432)
        else:
            self.port.setValue(3306)
    
    def test_connection(self):
        """Test the database connection"""
        # Get connection parameters
        connection_params = self.get_current_connection_params()
        
        if not connection_params:
            QMessageBox.warning(self, "Warning", "Please fill in all required connection fields")
            return
        
        # Disable test button during testing
        self.btn_test_connection.setEnabled(False)
        self.btn_test_connection.setText("Testing...")
        
        # Clear previous results
        self.text_test_results.clear()
        his_name = self.his_name.currentText()
        db_system = self.db_system.currentText()
        self.update_test_status(f"Testing {his_name} ({db_system}) connection...", "testing")
        
        # Start connection test in a separate thread
        self.test_thread = ConnectionTestThread(connection_params)
        self.test_thread.test_finished.connect(self.on_test_finished)
        self.test_thread.start()
    
    def get_current_connection_params(self):
        """Get connection parameters from the single tab"""
        return {
            'his_name': self.his_name.currentText(),
            'db_system': self.db_system.currentText(),
            'host': self.host.text(),
            'port': self.port.value(),
            'database': self.database.text(),
            'username': self.username.text(),
            'password': self.password.text(),
            'charset': self.charset.currentText(),
            'ssl': self.ssl.isChecked(),
            'connection_string': self.connection_string.text(),
            'type': f"{self.his_name.currentText()}_{self.db_system.currentText()}"
        }
    
    def on_test_finished(self, success, message):
        """Handle connection test completion"""
        # Re-enable test button
        self.btn_test_connection.setEnabled(True)
        self.btn_test_connection.setText("Test Connection")
        
        # Update UI with results
        self.text_test_results.setText(message)
        
        if success:
            self.update_test_status("Connection test passed", "success")
        else:
            self.update_test_status("Connection test failed", "error")
    
    def update_test_status(self, message, status_type="normal"):
        """Update the test status label with appropriate styling"""
        self.label_test_status.setText(message)
        
        if status_type == "success":
            self.label_test_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        elif status_type == "error":
            self.label_test_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        elif status_type == "testing":
            self.label_test_status.setStyleSheet("color: #f39c12; font-weight: bold;")
        else:
            self.label_test_status.setStyleSheet("color: #7f8c8d; font-style: italic;")

    def save_settings(self):
        """Save all connection settings using QSettings"""
        try:
            # Save current connection settings
            self.settings.beginGroup("Current")
            self.settings.setValue("his_name", self.his_name.currentText())
            self.settings.setValue("db_system", self.db_system.currentText())
            self.settings.setValue("host", self.host.text())
            self.settings.setValue("port", self.port.value())
            self.settings.setValue("database", self.database.text())
            self.settings.setValue("username", self.username.text())
            self.settings.setValue("password", self.password.text())
            self.settings.setValue("charset", self.charset.currentText())
            self.settings.setValue("ssl", self.ssl.isChecked())
            self.settings.setValue("connection_string", self.connection_string.text())
            self.settings.endGroup()
            
            # Save metadata
            self.settings.setValue("last_saved", datetime.now().isoformat())
            
            # Sync to ensure data is written
            self.settings.sync()
            
            QMessageBox.information(
                self, 
                "Success", 
                "Save Success"
            )
            
            # Close dialog
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Save Error", 
                f"Failed to save settings:\n\n{str(e)}"
            )

    def load_settings(self):
        """Load connection settings using QSettings"""
        try:
            # Load current connection settings
            self.settings.beginGroup("Current")
            self.his_name.setCurrentText(self.settings.value("his_name", "HOSXP"))
            self.db_system.setCurrentText(self.settings.value("db_system", "MySQL"))
            self.host.setText(self.settings.value("host", "192.168.1.1"))
            self.port.setValue(int(self.settings.value("port", 3306)))
            self.database.setText(self.settings.value("database", "hosxp_pcu"))
            self.username.setText(self.settings.value("username", "root"))
            self.password.setText(self.settings.value("password", ""))
            self.charset.setCurrentText(self.settings.value("charset", "tis620"))
            self.ssl.setChecked(self.settings.value("ssl", False, type=bool))
            self.connection_string.setText(self.settings.value("connection_string", ""))
            self.settings.endGroup()
            
            print("Settings loaded from QSettings")
                
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
            # Continue with default values
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to default values?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset to defaults (HOSXP profile)
            self.his_name.setCurrentText("HOSXP")
            self.db_system.setCurrentText("MySQL")
            self.host.setText("192.168.1.1")
            self.port.setValue(3306)
            self.database.setText("hosxp_pcu")
            self.username.setText("root")
            self.password.setText("")
            self.charset.setCurrentText("tis620")
            self.ssl.setChecked(False)
            self.connection_string.clear()
            
            # Clear test results
            self.text_test_results.clear()
            self.update_test_status("Settings reset to defaults", "normal")
    
    def get_connection_settings(self, db_type):
        """Get connection settings for a specific database type from QSettings"""
        try:
            self.settings.beginGroup(db_type.upper())
            settings = {
                'host': self.settings.value('host', 'localhost'),
                'port': int(self.settings.value('port', 3306)),
                'database': self.settings.value('database', ''),
                'username': self.settings.value('username', ''),
                'password': self.settings.value('password', ''),
                'charset': self.settings.value('charset', 'utf8'),
                'ssl': self.settings.value('ssl', False, type=bool)
            }
            self.settings.endGroup()
            return settings
        except Exception as e:
            print(f"Error loading {db_type} settings: {str(e)}")
        
        return {}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = HisConSetting()
    result = dialog.exec()
    sys.exit(app.exec())
