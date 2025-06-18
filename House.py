import sys

from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication

from House_ui import House_ui

class House(QWidget, House_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connect button signals
        self.add_button.clicked.connect(self.add_house)
        self.edit_button.clicked.connect(self.edit_house)
        self.delete_button.clicked.connect(self.delete_house)
        self.refresh_button.clicked.connect(self.refresh_data)
    
    def add_house(self):
        """
        Handle add house button click.
        """
        QMessageBox.information(self, "Add House", "Add House functionality will be implemented here.")
    
    def edit_house(self):
        """
        Handle edit house button click.
        """
        selected_rows = self.house_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Edit House", "Please select a house to edit.")
            return
        
        QMessageBox.information(self, "Edit House", "Edit House functionality will be implemented here.")
    
    def delete_house(self):
        """
        Handle delete house button click.
        """
        selected_rows = self.house_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Delete House", "Please select a house to delete.")
            return
        
        reply = QMessageBox.question(self, "Delete House", 
                                   "Are you sure you want to delete the selected house?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove selected row
            row = selected_rows[0].row()
            self.model.removeRow(row)
            QMessageBox.information(self, "Delete House", "House deleted successfully.")
    
    def refresh_data(self):
        """
        Handle refresh button click.
        """
        # Re-setup the table model with fresh data
        self.setup_table_model()
        QMessageBox.information(self, "Refresh", "Data refreshed successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = House()
    window.show()
    sys.exit(app.exec())
