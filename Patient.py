import sys
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication

from Patient_ui import Patient_ui

class Patient(QWidget, Patient_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connect button signals
        self.add_button.clicked.connect(self.add_patient)
        self.edit_button.clicked.connect(self.edit_patient)
        self.delete_button.clicked.connect(self.delete_patient)
        self.refresh_button.clicked.connect(self.refresh_data)
    
    def add_patient(self):
        """
        Handle add patient button click.
        """
        QMessageBox.information(self, "Add Patient", "Add Patient functionality will be implemented here.")
    
    def edit_patient(self):
        """
        Handle edit patient button click.
        """
        selected_rows = self.patient_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Edit Patient", "Please select a patient to edit.")
            return
        
        QMessageBox.information(self, "Edit Patient", "Edit Patient functionality will be implemented here.")
    
    def delete_patient(self):
        """
        Handle delete patient button click.
        """
        selected_rows = self.patient_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Delete Patient", "Please select a patient to delete.")
            return
        
        reply = QMessageBox.question(self, "Delete Patient", 
                                   "Are you sure you want to delete the selected patient?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove selected row
            row = selected_rows[0].row()
            self.model.removeRow(row)
            QMessageBox.information(self, "Delete Patient", "Patient deleted successfully.")
    
    def refresh_data(self):
        """
        Handle refresh button click.
        """
        # Re-setup the table model with fresh data
        self.setup_table_model()
        QMessageBox.information(self, "Refresh", "Data refreshed successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Patient()
    window.show()
    sys.exit(app.exec())
