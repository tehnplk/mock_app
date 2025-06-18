import sys
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication

from Visit_ui import Visit_ui

class Visit(QWidget, Visit_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connect button signals
        self.add_button.clicked.connect(self.add_visit)
        self.edit_button.clicked.connect(self.edit_visit)
        self.delete_button.clicked.connect(self.delete_visit)
        self.refresh_button.clicked.connect(self.refresh_data)
    
    def add_visit(self):
        """
        Handle add visit button click.
        """
        QMessageBox.information(self, "Add Visit", "Add Visit functionality will be implemented here.")
    
    def edit_visit(self):
        """
        Handle edit visit button click.
        """
        selected_rows = self.visit_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Edit Visit", "Please select a visit to edit.")
            return
        
        QMessageBox.information(self, "Edit Visit", "Edit Visit functionality will be implemented here.")
    
    def delete_visit(self):
        """
        Handle delete visit button click.
        """
        selected_rows = self.visit_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Delete Visit", "Please select a visit to delete.")
            return
        
        reply = QMessageBox.question(self, "Delete Visit", 
                                   "Are you sure you want to delete the selected visit?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove selected row
            row = selected_rows[0].row()
            self.model.removeRow(row)
            QMessageBox.information(self, "Delete Visit", "Visit deleted successfully.")
    
    def refresh_data(self):
        """
        Handle refresh button click.
        """
        # Re-setup the table model with fresh data
        self.setup_table_model()
        QMessageBox.information(self, "Refresh", "Data refreshed successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Visit()
    window.show()
    sys.exit(app.exec())
