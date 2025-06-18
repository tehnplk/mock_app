import sys
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTableView, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class Patient_ui(object):
    """
    UI class for Patient management.
    """

    def setupUi(self, Patient_ui):
        """
        Set up the user interface for Patient management.
        """
        # Set window properties
        Patient_ui.setWindowTitle("Patient Management")
        Patient_ui.resize(900, 700)
        
        # Create main layout
        self.main_layout = QVBoxLayout(Patient_ui)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Create title label
        self.title_label = QLabel("Patient Management System", Patient_ui)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        self.main_layout.addWidget(self.title_label)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        
        # Create action buttons
        self.add_button = QPushButton("Add Patient", Patient_ui)
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
        
        self.edit_button = QPushButton("Edit Patient", Patient_ui)
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
        
        self.delete_button = QPushButton("Delete Patient", Patient_ui)
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
        
        self.refresh_button = QPushButton("Refresh", Patient_ui)
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
        self.patient_table = QTableView(Patient_ui)
        self.patient_table.setStyleSheet("""
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
        self.patient_table.setAlternatingRowColors(True)
        self.patient_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.patient_table.setSortingEnabled(True)
        
        # Create and set model for the table
        self.setup_table_model()
        
        # Add table to layout
        self.main_layout.addWidget(self.patient_table)
        
    def setup_table_model(self):
        """
        Set up the table model with sample data.
        """
        # Create model
        self.model = QStandardItemModel(0, 8)
        
        # Set headers
        headers = ["Patient ID", "First Name", "Last Name", "Age", "Gender", "Phone", "Email", "Status"]
        self.model.setHorizontalHeaderLabels(headers)
        
        # Add sample data
        sample_data = [
            ["P001", "John", "Doe", "35", "Male", "555-0101", "john.doe@email.com", "Active"],
            ["P002", "Jane", "Smith", "28", "Female", "555-0102", "jane.smith@email.com", "Active"],
            ["P003", "Robert", "Johnson", "42", "Male", "555-0103", "robert.johnson@email.com", "Inactive"],
            ["P004", "Emily", "Davis", "31", "Female", "555-0104", "emily.davis@email.com", "Active"],
            ["P005", "Michael", "Wilson", "55", "Male", "555-0105", "michael.wilson@email.com", "Active"],
            ["P006", "Sarah", "Brown", "27", "Female", "555-0106", "sarah.brown@email.com", "Active"],
            ["P007", "David", "Taylor", "39", "Male", "555-0107", "david.taylor@email.com", "Inactive"],
            ["P008", "Lisa", "Anderson", "33", "Female", "555-0108", "lisa.anderson@email.com", "Active"],
        ]
        
        for row_data in sample_data:
            row = []
            for field in row_data:
                item = QStandardItem(field)
                item.setEditable(False)  # Make items read-only
                row.append(item)
            self.model.appendRow(row)
        
        # Set model to table view
        self.patient_table.setModel(self.model)
        
        # Resize columns to content
        self.patient_table.resizeColumnsToContents()

    def retranslateUi(self, Patient_ui):
        """
        Retranslate the user interface.
        """
        Patient_ui.setWindowTitle("Patient Management")
        self.title_label.setText("Patient Management System")
        self.add_button.setText("Add Patient")
        self.edit_button.setText("Edit Patient")
        self.delete_button.setText("Delete Patient")
        self.refresh_button.setText("Refresh")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    ui = Patient_ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
