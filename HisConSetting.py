# -*- coding: utf-8 -*-
"""
HIS Database Connection Settings Dialog
Refactored to use AppSetting for all settings management
"""
import sys
import os
from datetime import datetime

from PyQt6.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

from HisConSetting_ui import HisConSetting_ui
from AppSetting import app_settings

# Database connection imports
import pymysql
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class ConnectionTestWorker(QThread):
    """Worker thread for testing database connections"""
    
    # Signals
    test_completed = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, connection_params):
        super().__init__()
        self.connection_params = connection_params
    
    def run(self):
        """Run the connection test in a separate thread"""
        try:
            success, message = self._test_database_connection()
            self.test_completed.emit(success, message)
        except Exception as e:
            self.test_completed.emit(False, f"Unexpected error: {str(e)}")
    
    def _test_database_connection(self):
        """Test database connection with the provided parameters"""
        try:
            # Extract connection parameters
            use_connection_string = self.connection_params.get('use_connection_string', False)
            
            if use_connection_string:
                # Use the provided connection string
                connection_string = self.connection_params.get('connection_string', '')
                if not connection_string.strip():
                    return False, "Connection string is empty"
                
                # Test connection using SQLAlchemy
                engine = create_engine(connection_string, pool_pre_ping=True)
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT 1"))
                    result.fetchone()
                engine.dispose()
                return True, "Connection successful using connection string"
            
            else:
                # Use individual connection parameters
                db_system = self.connection_params.get('db_system', 'mysql').lower()
                host = self.connection_params.get('host', '')
                port = self.connection_params.get('port', 3306)
                database = self.connection_params.get('database', '')
                username = self.connection_params.get('username', '')
                password = self.connection_params.get('password', '')
                charset = self.connection_params.get('charset', 'utf8mb4')
                ssl = self.connection_params.get('ssl', False)
                
                # Validate required parameters
                if not host or not database or not username:
                    return False, "Missing required connection parameters (host, database, username)"
                
                if db_system == 'mysql':
                    return self._test_mysql_connection(host, port, database, username, password, charset, ssl)
                elif db_system == 'postgresql':
                    return self._test_postgresql_connection(host, port, database, username, password, ssl)
                else:
                    return False, f"Unsupported database system: {db_system}"
                    
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"
    
    def _test_mysql_connection(self, host, port, database, username, password, charset, ssl):
        """Test MySQL/MariaDB connection"""
        try:
            # Configure SSL
            ssl_config = {}
            if ssl:
                ssl_config = {'ssl_disabled': False}
            else:
                ssl_config = {'ssl_disabled': True}
            
            # Test connection using PyMySQL
            connection = pymysql.connect(
                host=host,
                port=int(port),
                user=username,
                password=password,
                database=database,
                charset=charset,
                autocommit=True,
                **ssl_config
            )
            
            # Test with a simple query
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            
            connection.close()
            
            if result:
                return True, f"MySQL connection successful to {host}:{port}/{database}"
            else:
                return False, "MySQL connection established but test query failed"
                
        except pymysql.Error as e:
            return False, f"MySQL connection failed: {str(e)}"
        except Exception as e:
            return False, f"MySQL connection error: {str(e)}"
    
    def _test_postgresql_connection(self, host, port, database, username, password, ssl):
        """Test PostgreSQL connection"""
        try:
            # Configure SSL mode
            sslmode = 'require' if ssl else 'disable'
            
            # Test connection using psycopg2
            connection = psycopg2.connect(
                host=host,
                port=int(port),
                database=database,
                user=username,
                password=password,                sslmode=sslmode
            )
            
            # Test with a simple query
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            
            connection.close()
            
            if result:
                return True, f"PostgreSQL connection successful to {host}:{port}/{database}"
            else:
                return False, "PostgreSQL connection established but test query failed"
                
        except psycopg2.Error as e:
            return False, f"PostgreSQL connection failed: {str(e)}"
        except Exception as e:
            return False, f"PostgreSQL connection error: {str(e)}"


class HisConSetting(QDialog, HisConSetting_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Initialize worker thread
        self.connection_test_worker = None
        
        # Load existing settings first (before connecting signals)
        self.load_settings()
        
        # Connect UI signals after loading settings
        self.setup_connections()
    
    def setup_connections(self):
        """Connect UI signals to slots"""
        # Button connections
        self.btn_test_connection.clicked.connect(self.test_connection)
        self.btn_save.clicked.connect(self.save_settings)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_reset.clicked.connect(self.reset_to_defaults)
          # System selection changes - override UI's built-in handlers
        self.his_name.currentTextChanged.disconnect()  # Disconnect UI handler
        self.db_system.currentTextChanged.disconnect()  # Disconnect UI handler
        self.his_name.currentTextChanged.connect(self.on_his_name_changed)
        self.db_system.currentTextChanged.connect(self.on_db_system_changed)
          # Connection string checkbox
        self.use_connection_string.toggled.connect(self.on_use_connection_string_toggled)
    
    def load_settings(self):
        """Load settings from AppSetting"""
        # Get values from AppSetting with defaults
        host = str(app_settings.get_value('host', 'localhost'))
        port = int(app_settings.get_value('port', 3306))
        database = str(app_settings.get_value('database', ''))
        username = str(app_settings.get_value('username', ''))
        password = str(app_settings.get_value('password', ''))
        db_system = str(app_settings.get_value('db_system', 'mysql'))
        his_name = str(app_settings.get_value('his_name', 'HOSXP'))
        charset = str(app_settings.get_value('charset', 'utf8mb4'))
        ssl_value = app_settings.get_value('ssl', False)
        ssl = ssl_value == 'true' if isinstance(ssl_value, str) else bool(ssl_value)
        connection_string = str(app_settings.get_value('connection_string', ''))
        use_conn_str_value = app_settings.get_value('use_connection_string', False)
        use_connection_string = use_conn_str_value == 'true' if isinstance(use_conn_str_value, str) else bool(use_conn_str_value)
        
        # Set UI values
        self.host.setText(host)
        self.port.setValue(port)
        self.database.setText(database)
        self.username.setText(username)
        self.password.setText(password)
        self.charset.setCurrentText(charset)
        self.ssl.setChecked(ssl)
        self.connection_string.setText(connection_string)
        self.use_connection_string.setChecked(use_connection_string)
        
        # Set HIS name
        if his_name in ["HOSXP", "JHCIS", "Other"]:
            self.his_name.setCurrentText(his_name)
        else:
            self.his_name.setCurrentText("HOSXP")
        
        # Set database system - map from internal format to UI format
        db_system_mapping = {
            "mysql": "MySQL",
            "postgresql": "PostgreSQL"
        }
        ui_db_system = db_system_mapping.get(db_system.lower(), "MySQL")
        self.db_system.setCurrentText(ui_db_system)
        
        # Reconnect signals after loading is complete
        self.his_name.currentTextChanged.connect(self.on_his_name_changed)
        self.db_system.currentTextChanged.connect(self.on_db_system_changed)
        
        # Update UI state based on connection string checkbox
        self.on_use_connection_string_toggled(use_connection_string)
    
    def save_settings(self):
        """Save current settings to AppSetting"""
        # Map UI database system format to internal format
        ui_db_system = self.db_system.currentText()
        db_system_mapping = {
            "MySQL": "mysql",
            "MariaDB": "mysql",
            "PostgreSQL": "postgresql"
        }
        db_system = db_system_mapping.get(ui_db_system, "mysql")
        
        # Save all settings
        app_settings.set_value('host', self.host.text().strip())
        app_settings.set_value('port', self.port.value())
        app_settings.set_value('database', self.database.text().strip())
        app_settings.set_value('username', self.username.text().strip())
        app_settings.set_value('password', self.password.text())
        app_settings.set_value('db_system', db_system)
        app_settings.set_value('his_name', self.his_name.currentText())
        app_settings.set_value('charset', self.charset.currentText())
        app_settings.set_value('ssl', self.ssl.isChecked())
        app_settings.set_value('connection_string', self.connection_string.text().strip())
        app_settings.set_value('use_connection_string', self.use_connection_string.isChecked())
        
        # Force sync to storage
        app_settings.sync()
        
        # Show success message
        QMessageBox.information(self, "Settings Saved", "Database connection settings saved successfully!")
        
        # Close dialog
        self.accept()
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        # Set default values
        self.host.setText('localhost')
        self.port.setValue(3306)
        self.database.setText('')
        self.username.setText('')
        self.password.setText('')
        self.charset.setCurrentText('utf8mb4')
        self.ssl.setChecked(False)
        self.connection_string.setText('')
        self.use_connection_string.setChecked(False)
        self.his_name.setCurrentText('HOSXP')
        self.db_system.setCurrentText('MySQL')
        
        # Update UI state
        self.on_use_connection_string_toggled(False)
        
        # Update status
        self.update_test_status("Settings reset to defaults", "normal")
    
    def on_his_name_changed(self, his_name):
        """Handle HIS name selection change and load default profiles"""
        # Set defaults based on HIS system
        if his_name == "HOSXP":
            if not self.host.text():
                self.host.setText("192.168.1.10")
            if self.port.value() == 3306:
                self.port.setValue(3306)
            if not self.database.text():
                self.database.setText("hosxp_pcu")
            self.charset.setCurrentText("tis620")
            self.db_system.setCurrentText("MySQL")
        elif his_name == "JHCIS":
            if not self.host.text():
                self.host.setText("192.168.1.20")
            if self.port.value() == 3306:
                self.port.setValue(3306)
            if not self.database.text():
                self.database.setText("jhcisdb")
            self.charset.setCurrentText("utf8")
            self.db_system.setCurrentText("MySQL")
        else:  # Other
            if not self.host.text():
                self.host.setText("localhost")
            if self.port.value() == 3306:
                self.port.setValue(3306)
            self.charset.setCurrentText("utf8mb4")
            self.db_system.setCurrentText("MySQL")
    
    def on_db_system_changed(self, db_system):
        """Handle database system selection change"""
        if db_system == "PostgreSQL":
            # Update defaults for PostgreSQL
            if self.port.value() in [3306, 5432]:
                self.port.setValue(5432)
            self.charset.setCurrentText("utf8")
            self.ssl.setChecked(True)
        else:  # MySQL or MariaDB
            # Update defaults for MySQL/MariaDB
            if self.port.value() in [3306, 5432]:
                self.port.setValue(3306)
            self.charset.setCurrentText("utf8mb4")
    
    def on_use_connection_string_toggled(self, checked):
        """Handle connection string checkbox toggle"""
        # Enable/disable individual connection fields
        self.host.setEnabled(not checked)
        self.port.setEnabled(not checked)
        self.database.setEnabled(not checked)
        self.username.setEnabled(not checked)
        self.password.setEnabled(not checked)
        self.charset.setEnabled(not checked)
        self.ssl.setEnabled(not checked)
        
        # Enable/disable connection string field
        self.connection_string.setEnabled(checked)
    
    def test_connection(self):
        """Test database connection"""
        # Save current settings temporarily for testing
        self.save_test_settings()
          # Update UI
        self.btn_test_connection.setEnabled(False)
        self.update_test_status("Testing connection...", "testing")
        
        # Create connection parameters dictionary
        connection_params = {
            'use_connection_string': self.use_connection_string.isChecked(),
            'connection_string': self.connection_string.text().strip(),
            'host': self.host.text().strip(),
            'port': self.port.value(),
            'database': self.database.text().strip(),
            'username': self.username.text().strip(),
            'password': self.password.text(),
            'db_system': self._get_internal_db_system(),
            'charset': self.charset.currentText(),
            'ssl': self.ssl.isChecked()
        }
          # Create and start worker thread
        self.connection_test_worker = ConnectionTestWorker(connection_params)
        self.connection_test_worker.test_completed.connect(self.on_connection_test_completed)
        self.connection_test_worker.start()
    
    def save_test_settings(self):
        """Save current UI values temporarily for testing"""
        # Map UI database system format to internal format
        ui_db_system = self.db_system.currentText()
        db_system_mapping = {
            "MySQL": "mysql",
            "MariaDB": "mysql",
            "PostgreSQL": "postgresql"
        }
        db_system = db_system_mapping.get(ui_db_system, "mysql")
        
        # Save test values to a different key space or temporarily
        app_settings.set_value('test_host', self.host.text().strip())
        app_settings.set_value('test_port', self.port.value())
        app_settings.set_value('test_database', self.database.text().strip())
        app_settings.set_value('test_username', self.username.text().strip())
        app_settings.set_value('test_password', self.password.text())
        app_settings.set_value('test_db_system', db_system)
        app_settings.set_value('test_charset', self.charset.currentText())
        app_settings.set_value('test_ssl', self.ssl.isChecked())
        app_settings.set_value('test_connection_string', self.connection_string.text().strip())
        app_settings.set_value('test_use_connection_string', self.use_connection_string.isChecked())
        
        # Or temporarily overwrite the main settings for testing
        app_settings.set_value('host', self.host.text().strip())
        app_settings.set_value('port', self.port.value())
        app_settings.set_value('database', self.database.text().strip())
        app_settings.set_value('username', self.username.text().strip())
        app_settings.set_value('password', self.password.text())
        app_settings.set_value('db_system', db_system)
        app_settings.set_value('charset', self.charset.currentText())
        app_settings.set_value('ssl', self.ssl.isChecked())
        app_settings.set_value('connection_string', self.connection_string.text().strip())
        app_settings.set_value('use_connection_string', self.use_connection_string.isChecked())
    
    def _get_internal_db_system(self):
        """Convert UI database system format to internal format"""
        ui_db_system = self.db_system.currentText()
        db_system_mapping = {
            "MySQL": "mysql",
            "MariaDB": "mysql",
            "PostgreSQL": "postgresql"
        }
        return db_system_mapping.get(ui_db_system, "mysql")
    
    def on_connection_test_completed(self, success, message):
        """Handle connection test completion"""
        # Re-enable the test button
        self.btn_test_connection.setEnabled(True)
        
        # Update status based on result
        if success:
            self.update_test_status(message, "success")
        else:
            self.update_test_status(message, "error")
        
        # Clean up worker thread
        if self.connection_test_worker:
            self.connection_test_worker.deleteLater()
            self.connection_test_worker = None
    
    def closeEvent(self, event):
        """Handle dialog close event - clean up worker thread"""
        if self.connection_test_worker and self.connection_test_worker.isRunning():
            self.connection_test_worker.terminate()
            self.connection_test_worker.wait()
        event.accept()
    
    def update_test_status(self, message, status_type):
        """Update test status label with appropriate styling"""
        self.label_test_status.setText(message)
        
        # Apply styling based on status type
        styles = {
            "normal": "color: #333333;",
            "testing": "color: #0066cc; font-weight: bold;",
            "success": "color: #009900; font-weight: bold;",
            "error": "color: #cc0000; font-weight: bold;",
            "warning": "color: #ff6600;"
        }
        
        style = styles.get(status_type, styles["normal"])
        self.label_test_status.setStyleSheet(style)


if __name__ == "__main__":
    #Do not modify this part
    app = QApplication(sys.argv)
    dialog = HisConSetting()
    result = dialog.exec()
    sys.exit(app.exec())
