import sys

from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTableView, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class House_ui(object):
    """
    UI class for House management.
    """

    def setupUi(self, House_ui):
        """
        Set up the user interface for House management.
        """
        # Set window properties
        House_ui.setWindowTitle("House Management")
        House_ui.resize(800, 600)
        
        # Create main layout
        self.main_layout = QVBoxLayout(House_ui)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Create title label
        self.title_label = QLabel("House Management System", House_ui)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        self.main_layout.addWidget(self.title_label)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        
        # Create action buttons
        self.add_button = QPushButton("Add House", House_ui)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.button_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("Edit House", House_ui)
        self.edit_button.setStyleSheet("""
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
        """)
        self.button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Delete House", House_ui)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.button_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Refresh", House_ui)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """)
        self.button_layout.addWidget(self.refresh_button)
        
        # Add stretch to push buttons to the left
        self.button_layout.addStretch()
        
        # Add button layout to main layout
        self.main_layout.addLayout(self.button_layout)
        
        # Create table view
        self.house_table = QTableView(House_ui)
        self.house_table.setStyleSheet("""
            QTableView {
                gridline-color: #bdc3c7;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #3498db;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTableView::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableView::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        self.house_table.setAlternatingRowColors(True)
        self.house_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.house_table.setSortingEnabled(True)
        
        # Create and set model for the table
        self.setup_table_model()
        
        # Add table to layout
        self.main_layout.addWidget(self.house_table)
        
    def setup_table_model(self):
        """
        Set up the table model with sample data.
        """
        # Create model
        self.model = QStandardItemModel(0, 6)
        
        # Set headers
        headers = ["House ID", "Address", "City", "State", "Zip Code", "Status"]
        self.model.setHorizontalHeaderLabels(headers)
        
        # Add sample data
        sample_data = [
            ["H001", "123 Main St", "Springfield", "IL", "62701", "Available"],
            ["H002", "456 Oak Ave", "Springfield", "IL", "62702", "Occupied"],
            ["H003", "789 Pine Rd", "Springfield", "IL", "62703", "Maintenance"],
            ["H004", "321 Elm St", "Springfield", "IL", "62704", "Available"],
            ["H005", "654 Maple Dr", "Springfield", "IL", "62705", "Occupied"],
        ]
        
        for row_data in sample_data:
            row = []
            for field in row_data:
                item = QStandardItem(field)
                item.setEditable(False)  # Make items read-only
                row.append(item)
            self.model.appendRow(row)
        
        # Set model to table view
        self.house_table.setModel(self.model)
        
        # Resize columns to content
        self.house_table.resizeColumnsToContents()

    def retranslateUi(self, House_ui):
        """
        Retranslate the user interface.
        """
        House_ui.setWindowTitle("House Management")
        self.title_label.setText("House Management System")
        self.add_button.setText("Add House")
        self.edit_button.setText("Edit House")
        self.delete_button.setText("Delete House")
        self.refresh_button.setText("Refresh")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    ui = House_ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
