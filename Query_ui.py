import sys

from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                             QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QSplitter, QComboBox, QLineEdit, QGroupBox, QApplication)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Query_ui(object):
    """
    UI class for Query module.
    """
    
    def setupUi(self, Query_ui):
        """
        Set up the user interface for Query module.
        """
        Query_ui.setWindowTitle("Database Query Tool")
        Query_ui.setMinimumSize(800, 600)
          # Main vertical layout directly on the widget
        main_layout = QVBoxLayout(Query_ui)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create header section
        self.create_header_section(main_layout)
        
        # Create query input section
        self.create_query_section(main_layout)
        
        # Create results section
        self.create_results_section(main_layout)
        
        # Create status section
        self.create_status_section(main_layout)
    
    def create_header_section(self, parent_layout):
        """Create the header section with database info"""
        header_group = QGroupBox("Database Connection")
        header_layout = QHBoxLayout(header_group)
        
        # Database selection
        db_label = QLabel("Database:")
        self.combo_database = QComboBox()
        self.combo_database.addItems(["HOSXP", "JHCIS", "MySQL Local"])
        self.combo_database.setMinimumWidth(150)
        
        # Connection status
        self.label_connection_status = QLabel("Status: Connected")
        self.label_connection_status.setStyleSheet("color: green; font-weight: bold;")
        
        # Refresh button
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.setMaximumWidth(80)
        
        header_layout.addWidget(db_label)
        header_layout.addWidget(self.combo_database)
        header_layout.addStretch()
        header_layout.addWidget(self.label_connection_status)
        header_layout.addWidget(self.btn_refresh)
        
        parent_layout.addWidget(header_group)
    
    def create_query_section(self, parent_layout):
        """Create the SQL query input section"""
        query_group = QGroupBox("SQL Query")
        query_layout = QVBoxLayout(query_group)
        
        # Query input area
        self.text_query = QTextEdit()
        self.text_query.setMaximumHeight(150)
        self.text_query.setPlaceholderText("Enter your SQL query here...")
        
        # Set font for query text
        font = QFont("Consolas", 10)
        if not font.exactMatch():
            font = QFont("Courier New", 10)
        self.text_query.setFont(font)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Execute button
        self.btn_execute = QPushButton("Execute Query")
        self.btn_execute.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        
        # Clear button
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setMaximumWidth(80)
        
        # Sample queries button
        self.btn_samples = QPushButton("Sample Queries")
        self.btn_samples.setMaximumWidth(120)
        
        button_layout.addWidget(self.btn_execute)
        button_layout.addWidget(self.btn_clear)
        button_layout.addWidget(self.btn_samples)
        button_layout.addStretch()
        
        query_layout.addWidget(self.text_query)
        query_layout.addLayout(button_layout)
        
        parent_layout.addWidget(query_group)
    
    def create_results_section(self, parent_layout):
        """Create the results display section"""
        results_group = QGroupBox("Query Results")
        results_layout = QVBoxLayout(results_group)
        
        # Results table
        self.table_results = QTableWidget()
        self.table_results.setAlternatingRowColors(True)
        self.table_results.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_results.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 5px;
                font-weight: bold;
            }
        """)
        
        # Export buttons
        export_layout = QHBoxLayout()
        
        self.btn_export_csv = QPushButton("Export to CSV")
        self.btn_export_csv.setMaximumWidth(120)
        
        self.btn_export_excel = QPushButton("Export to Excel")
        self.btn_export_excel.setMaximumWidth(120)
        
        # Results info label
        self.label_results_info = QLabel("No query executed")
        self.label_results_info.setStyleSheet("color: #6c757d; font-style: italic;")
        
        export_layout.addWidget(self.btn_export_csv)
        export_layout.addWidget(self.btn_export_excel)
        export_layout.addStretch()
        export_layout.addWidget(self.label_results_info)
        
        results_layout.addWidget(self.table_results)
        results_layout.addLayout(export_layout)
        
        parent_layout.addWidget(results_group)
    
    def create_status_section(self, parent_layout):
        """Create the status section"""
        status_layout = QHBoxLayout()
        
        # Query execution time
        self.label_execution_time = QLabel("Execution time: --")
        self.label_execution_time.setStyleSheet("color: #6c757d;")
        
        # Row count
        self.label_row_count = QLabel("Rows: 0")
        self.label_row_count.setStyleSheet("color: #6c757d;")
        
        status_layout.addWidget(self.label_execution_time)
        status_layout.addStretch()
        status_layout.addWidget(self.label_row_count)
        
        parent_layout.addLayout(status_layout)

    def retranslateUi(self, Query_ui):
        """
        Retranslate the user interface.
        """
        Query_ui.setWindowTitle("Database Query Tool")
        self.btn_execute.setText("Execute Query")
        self.btn_clear.setText("Clear")
        self.btn_samples.setText("Sample Queries")
        self.btn_export_csv.setText("Export to CSV")
        self.btn_export_excel.setText("Export to Excel")
        self.btn_refresh.setText("Refresh")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    ui = Query_ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
