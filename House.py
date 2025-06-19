import sys

from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from House_ui import House_ui
from DbPerform import DbPerform


class House(QWidget, House_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Initialize database performance class
        self.db = DbPerform()
        
        # Connect button signals
        self.add_button.clicked.connect(self.add_house)
        self.edit_button.clicked.connect(self.edit_house)
        self.delete_button.clicked.connect(self.delete_house)
        self.refresh_button.clicked.connect(self.refresh_data)        # Load house data on startup
        self.load_house_data()
    
    def load_house_data(self):
        """Load house data from database using DbPerform with query parameters"""
        try:
            # Define house data queries for different HIS systems
            house_queries = [
                # HOSXP house table
                "SELECT housecode as house_id, address, tambon as city, amp as state, zip_code, status FROM house LIMIT 100",
                
                # JHCIS village table
                "SELECT village_id as house_id, village_name as address, tambon as city, amp as state, zip_code, 'Active' as status FROM villages LIMIT 100",
                
                # Patient table with house information
                "SELECT houseno as house_id, houseaddr as address, tambon_name as city, amp_name as state, zip_code, 'Active' as status FROM patient LIMIT 100",
                
                # Generic house table
                "SELECT house_id, address, city, state, zip_code, status FROM houses LIMIT 100",
                
                # Another common pattern
                "SELECT id as house_id, house_address as address, district as city, province as state, postal_code as zip_code, house_status as status FROM house_master LIMIT 100"
            ]
            
            # Try to execute multiple queries and get first successful result
            success, house_data, query_index = self.db.execute_multiple_queries(house_queries)
            
            if success and house_data:
                # Update table model with real data
                self.update_table_with_data(house_data)
                print(f"Successfully loaded {len(house_data)} house records from database using query {query_index + 1}")
            else:
                # If specific queries fail, try to find house-related tables
                print("Specific house queries failed, searching for house-related tables...")
                success = self._try_generic_house_approach()
                
                if not success:
                    # Fallback to sample data if all database attempts fail
                    print(f"All database queries failed: {house_data}")
                    QMessageBox.warning(self, "Database Warning", 
                                      f"Could not load house data from database.\nUsing sample data instead.")
                    self.setup_table_model()
                
        except Exception as e:
            print(f"Error loading house data: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to load house data:\n{str(e)}\n\nUsing sample data instead.")
            # Fallback to sample data
            self.setup_table_model()
    
    def _try_generic_house_approach(self):
        """Try to find and query house-related tables using generic approach"""
        try:
            # Find house-related tables
            patterns = ['%house%', '%village%', '%address%']
            success, tables = self.db.find_tables_by_pattern(patterns)
            
            if success and tables:
                print(f"Found house-related tables: {tables}")
                
                # Try to get data from each table
                for table_name in tables:
                    query = f"SELECT * FROM {table_name} LIMIT 100"
                    success, data = self.db.execute_query(query)
                    
                    if success and data:
                        print(f"Successfully loaded {len(data)} records from {table_name}")
                        self.update_table_with_data(data)
                        return True
            
            return False
            
        except Exception as e:
            print(f"Error in generic house approach: {str(e)}")
            return False
    
    def update_table_with_data(self, data):
        """Update table model with database data"""
        # Create model
        self.model = QStandardItemModel(0, 6)
        
        # Set headers
        headers = ["House ID", "Address", "City", "State", "Zip Code", "Status"]
        self.model.setHorizontalHeaderLabels(headers)
        
        # Add data rows
        for row_data in data:
            row = []
            # Ensure we have 6 columns, pad with empty strings if needed
            row_values = list(row_data)
            while len(row_values) < 6:
                row_values.append("")
            
            # Take only first 6 columns
            row_values = row_values[:6]
            
            for field in row_values:
                item = QStandardItem(str(field) if field is not None else "")
                item.setEditable(False)  # Make items read-only
                row.append(item)
            self.model.appendRow(row)
        
        # Set model to table view
        self.house_table.setModel(self.model)
        
        # Resize columns to content
        self.house_table.resizeColumnsToContents()
        
        print(f"Table updated with {len(data)} records")
    
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
        
        if reply == QMessageBox.StandardButton.Yes:            # Remove selected row
            row = selected_rows[0].row()
            self.model.removeRow(row)
            QMessageBox.information(self, "Delete House", "House deleted successfully.")
    
    def refresh_data(self):
        """
        Handle refresh button click - reload data from database.
        """
        # Reload house data from database
        self.load_house_data()
        QMessageBox.information(self, "Refresh", "Data refreshed successfully from database.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = House()
    window.show()
    sys.exit(app.exec())
