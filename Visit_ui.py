import sys

from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTableView, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class Visit_ui(object):
    """
    UI class for Visit management.
    """

    def setupUi(self, Visit_ui):
        """
        Set up the user interface for Visit management.
        """
        # Set window properties
        Visit_ui.setWindowTitle("Visit Management")
        Visit_ui.resize(1000, 700)
        
        # Create main layout
        self.main_layout = QVBoxLayout(Visit_ui)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Create title label
        self.title_label = QLabel("Visit Management System", Visit_ui)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        self.main_layout.addWidget(self.title_label)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        
        # Create action buttons
        self.add_button = QPushButton("Add Visit", Visit_ui)
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
        
        self.edit_button = QPushButton("Edit Visit", Visit_ui)
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
        
        self.delete_button = QPushButton("Delete Visit", Visit_ui)
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
        
        self.refresh_button = QPushButton("Refresh", Visit_ui)
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
        self.visit_table = QTableView(Visit_ui)
        self.visit_table.setStyleSheet("""
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
        self.visit_table.setAlternatingRowColors(True)
        self.visit_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.visit_table.setSortingEnabled(True)
        
        # Create and set model for the table
        self.setup_table_model()
        
        # Add table to layout
        self.main_layout.addWidget(self.visit_table)
        
    def setup_table_model(self):
        """
        Set up the table model with sample data.
        """
        # Create model
        self.model = QStandardItemModel(0, 10)
        
        # Set headers
        headers = ["Visit ID", "Patient ID", "Patient Name", "Visit Date", "Visit Time", "Doctor", "Department", "Reason", "Status", "Notes"]
        self.model.setHorizontalHeaderLabels(headers)
        
        # Add sample data
        sample_data = [
            ["V001", "P001", "John Doe", "2024-12-18", "09:00", "Dr. Smith", "Cardiology", "Regular Checkup", "Completed", "Normal examination"],
            ["V002", "P002", "Jane Smith", "2024-12-18", "10:30", "Dr. Johnson", "Dermatology", "Skin Rash", "Completed", "Prescribed medication"],
            ["V003", "P003", "Robert Johnson", "2024-12-18", "14:00", "Dr. Williams", "Orthopedics", "Knee Pain", "In Progress", "X-ray scheduled"],
            ["V004", "P004", "Emily Davis", "2024-12-19", "08:30", "Dr. Brown", "Pediatrics", "Vaccination", "Scheduled", "Annual immunization"],
            ["V005", "P005", "Michael Wilson", "2024-12-19", "11:00", "Dr. Davis", "Internal Medicine", "Diabetes Follow-up", "Scheduled", "Blood sugar monitoring"],
            ["V006", "P006", "Sarah Brown", "2024-12-19", "15:30", "Dr. Miller", "Gynecology", "Annual Exam", "Scheduled", "Routine checkup"],
            ["V007", "P007", "David Taylor", "2024-12-20", "09:15", "Dr. Wilson", "Neurology", "Headaches", "Scheduled", "Neurological assessment"],
            ["V008", "P008", "Lisa Anderson", "2024-12-20", "13:45", "Dr. Taylor", "Ophthalmology", "Eye Exam", "Scheduled", "Vision test"],
        ]
        
        for row_data in sample_data:
            row = []
            for field in row_data:
                item = QStandardItem(field)
                item.setEditable(False)  # Make items read-only
                row.append(item)
            self.model.appendRow(row)
        
        # Set model to table view
        self.visit_table.setModel(self.model)
        
        # Resize columns to content
        self.visit_table.resizeColumnsToContents()

    def retranslateUi(self, Visit_ui):
        """
        Retranslate the user interface.
        """
        Visit_ui.setWindowTitle("Visit Management")
        self.title_label.setText("Visit Management System")
        self.add_button.setText("Add Visit")
        self.edit_button.setText("Edit Visit")
        self.delete_button.setText("Delete Visit")
        self.refresh_button.setText("Refresh")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    ui = Visit_ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
