import sys
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTableView, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class Person_ui(object):
    """
    UI class for Person management.
    """

    def setupUi(self, Person_ui):
        """
        Set up the user interface for Person management.
        """
        # Set window properties
        Person_ui.setWindowTitle("Person Management")
        Person_ui.resize(900, 700)
        
        # Create main layout
        self.main_layout = QVBoxLayout(Person_ui)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Create title label
        self.title_label = QLabel("Person Management System", Person_ui)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        self.main_layout.addWidget(self.title_label)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        
        # Create action buttons
        self.add_button = QPushButton("Add Person", Person_ui)
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
        
        self.edit_button = QPushButton("Edit Person", Person_ui)
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
        
        self.delete_button = QPushButton("Delete Person", Person_ui)
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
        
        self.refresh_button = QPushButton("Refresh", Person_ui)
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
        self.person_table = QTableView(Person_ui)
        self.person_table.setStyleSheet("""
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
        self.person_table.setAlternatingRowColors(True)
        self.person_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.person_table.setSortingEnabled(True)
        
        # Create and set model for the table
        self.setup_table_model()
        
        # Add table to layout
        self.main_layout.addWidget(self.person_table)
        
    def setup_table_model(self):
        """
        Set up the table model with sample data.
        """
        # Create model
        self.model = QStandardItemModel(0, 9)
        
        # Set headers
        headers = ["Person ID", "First Name", "Last Name", "Date of Birth", "Gender", "Address", "Phone", "Email", "Type"]
        self.model.setHorizontalHeaderLabels(headers)
        
        # Add sample data
        sample_data = [
            ["PR001", "Alice", "Johnson", "1985-03-15", "Female", "123 Oak St, Springfield", "555-0201", "alice.johnson@email.com", "Employee"],
            ["PR002", "Bob", "Williams", "1978-07-22", "Male", "456 Pine Ave, Springfield", "555-0202", "bob.williams@email.com", "Contractor"],
            ["PR003", "Carol", "Brown", "1992-11-08", "Female", "789 Elm Rd, Springfield", "555-0203", "carol.brown@email.com", "Employee"],
            ["PR004", "Daniel", "Davis", "1980-01-30", "Male", "321 Maple Dr, Springfield", "555-0204", "daniel.davis@email.com", "Visitor"],
            ["PR005", "Emma", "Wilson", "1975-09-12", "Female", "654 Cedar Ln, Springfield", "555-0205", "emma.wilson@email.com", "Employee"],
            ["PR006", "Frank", "Taylor", "1988-05-03", "Male", "987 Birch St, Springfield", "555-0206", "frank.taylor@email.com", "Contractor"],
            ["PR007", "Grace", "Anderson", "1995-12-25", "Female", "147 Spruce Ave, Springfield", "555-0207", "grace.anderson@email.com", "Student"],
            ["PR008", "Henry", "Martinez", "1983-04-18", "Male", "258 Willow Rd, Springfield", "555-0208", "henry.martinez@email.com", "Employee"],
        ]
        
        for row_data in sample_data:
            row = []
            for field in row_data:
                item = QStandardItem(field)
                item.setEditable(False)  # Make items read-only
                row.append(item)
            self.model.appendRow(row)
        
        # Set model to table view
        self.person_table.setModel(self.model)
        
        # Resize columns to content
        self.person_table.resizeColumnsToContents()

    def retranslateUi(self, Person_ui):
        """
        Retranslate the user interface.
        """
        Person_ui.setWindowTitle("Person Management")
        self.title_label.setText("Person Management System")
        self.add_button.setText("Add Person")
        self.edit_button.setText("Edit Person")
        self.delete_button.setText("Delete Person")
        self.refresh_button.setText("Refresh")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    ui = Person_ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
