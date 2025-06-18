import sys
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication

from Person_ui import Person_ui

class Person(QWidget, Person_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connect button signals
        self.add_button.clicked.connect(self.add_person)
        self.edit_button.clicked.connect(self.edit_person)
        self.delete_button.clicked.connect(self.delete_person)
        self.refresh_button.clicked.connect(self.refresh_data)
    
    def add_person(self):
        """
        Handle add person button click.
        """
        QMessageBox.information(self, "Add Person", "Add Person functionality will be implemented here.")
    
    def edit_person(self):
        """
        Handle edit person button click.
        """
        selected_rows = self.person_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Edit Person", "Please select a person to edit.")
            return
        
        QMessageBox.information(self, "Edit Person", "Edit Person functionality will be implemented here.")
    
    def delete_person(self):
        """
        Handle delete person button click.
        """
        selected_rows = self.person_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Delete Person", "Please select a person to delete.")
            return
        
        reply = QMessageBox.question(self, "Delete Person", 
                                   "Are you sure you want to delete the selected person?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove selected row
            row = selected_rows[0].row()
            self.model.removeRow(row)
            QMessageBox.information(self, "Delete Person", "Person deleted successfully.")
    
    def refresh_data(self):
        """
        Handle refresh button click.
        """
        # Re-setup the table model with fresh data
        self.setup_table_model()
        QMessageBox.information(self, "Refresh", "Data refreshed successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Person()
    window.show()
    sys.exit(app.exec())
