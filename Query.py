import sys
import time
import csv
from datetime import datetime

from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog, QMenu, QTableWidgetItem
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from Query_ui import Query_ui


class QueryThread(QThread):
    """Thread for executing database queries without blocking the UI"""
    
    query_finished = pyqtSignal(list, list, float)  # results, headers, execution_time
    query_error = pyqtSignal(str)  # error_message
    
    def __init__(self, query, database_type):
        super().__init__()
        self.query = query
        self.database_type = database_type
    
    def run(self):
        """Execute the query in a separate thread"""
        try:
            start_time = time.time()
            
            # Simulate database connection and query execution
            # In a real implementation, you would connect to actual databases here
            results, headers = self.execute_mock_query(self.query, self.database_type)
            
            execution_time = time.time() - start_time
            self.query_finished.emit(results, headers, execution_time)
            
        except Exception as e:
            self.query_error.emit(str(e))
    
    def execute_mock_query(self, query, database_type):
        """Mock query execution - replace with actual database connections"""
        
        # Simulate processing time
        time.sleep(0.5)
        
        query_lower = query.lower().strip()
        
        # Sample data based on query type
        if "select" in query_lower:
            if "patient" in query_lower or "hn" in query_lower:
                headers = ["HN", "Name", "Age", "Gender", "Admission_Date"]
                results = [
                    ["HN001", "John Doe", "45", "Male", "2024-01-15"],
                    ["HN002", "Jane Smith", "32", "Female", "2024-01-16"],
                    ["HN003", "Bob Johnson", "67", "Male", "2024-01-17"],
                    ["HN004", "Alice Brown", "29", "Female", "2024-01-18"],
                    ["HN005", "Charlie Wilson", "54", "Male", "2024-01-19"]
                ]
            elif "doctor" in query_lower or "provider" in query_lower:
                headers = ["Doctor_ID", "Name", "Specialty", "Department"]
                results = [
                    ["D001", "Dr. Smith", "Cardiology", "Internal Medicine"],
                    ["D002", "Dr. Johnson", "Pediatrics", "Children's Ward"],
                    ["D003", "Dr. Brown", "Surgery", "Surgical Department"],
                    ["D004", "Dr. Davis", "Neurology", "Neurology Department"]
                ]
            elif "visit" in query_lower or "opd" in query_lower:
                headers = ["Visit_ID", "HN", "Visit_Date", "Doctor", "Diagnosis"]
                results = [
                    ["V001", "HN001", "2024-01-15", "Dr. Smith", "Hypertension"],
                    ["V002", "HN002", "2024-01-16", "Dr. Johnson", "Common Cold"],
                    ["V003", "HN003", "2024-01-17", "Dr. Brown", "Diabetes"],
                    ["V004", "HN004", "2024-01-18", "Dr. Davis", "Migraine"]
                ]
            else:
                # Generic sample data
                headers = ["ID", "Field1", "Field2", "Field3"]
                results = [
                    ["1", "Sample Data 1", "Value 1", "2024-01-15"],
                    ["2", "Sample Data 2", "Value 2", "2024-01-16"],
                    ["3", "Sample Data 3", "Value 3", "2024-01-17"]
                ]
        else:
            # For non-SELECT queries
            headers = ["Result"]
            results = [["Query executed successfully"]]
        
        return results, headers


class Query(QWidget, Query_ui):
    """
    Query module for database queries and data analysis.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Initialize variables
        self.current_results = []
        self.current_headers = []
        self.query_thread = None
        
        # Connect signals
        self.setup_connections()
        
        # Load sample queries
        self.sample_queries = self.get_sample_queries()
        
        # Set initial state
        self.update_ui_state(False)  # Disable export buttons initially
    
    def setup_connections(self):
        """Connect UI signals to their handlers"""
        self.btn_execute.clicked.connect(self.execute_query)
        self.btn_clear.clicked.connect(self.clear_query)
        self.btn_samples.clicked.connect(self.show_sample_queries)
        self.btn_refresh.clicked.connect(self.refresh_connection)
        self.btn_export_csv.clicked.connect(self.export_to_csv)
        self.btn_export_excel.clicked.connect(self.export_to_excel)
        self.combo_database.currentTextChanged.connect(self.on_database_changed)
    
    def execute_query(self):
        """Execute the SQL query"""
        query = self.text_query.toPlainText().strip()
        
        if not query:
            QMessageBox.warning(self, "Warning", "Please enter a SQL query")
            return
        
        # Disable execute button during query execution
        self.btn_execute.setEnabled(False)
        self.btn_execute.setText("Executing...")
        
        # Clear previous results
        self.table_results.clear()
        self.table_results.setRowCount(0)
        self.table_results.setColumnCount(0)
        
        # Update status
        self.label_results_info.setText("Executing query...")
        self.label_execution_time.setText("Execution time: --")
        self.label_row_count.setText("Rows: --")
        
        # Start query execution in a separate thread
        database_type = self.combo_database.currentText()
        self.query_thread = QueryThread(query, database_type)
        self.query_thread.query_finished.connect(self.on_query_finished)
        self.query_thread.query_error.connect(self.on_query_error)
        self.query_thread.start()
    
    def on_query_finished(self, results, headers, execution_time):
        """Handle successful query completion"""
        self.current_results = results
        self.current_headers = headers
        
        # Update results table
        self.populate_results_table(results, headers)
        
        # Update status
        self.label_execution_time.setText(f"Execution time: {execution_time:.3f}s")
        self.label_row_count.setText(f"Rows: {len(results)}")
        self.label_results_info.setText(f"Query completed successfully - {len(results)} rows returned")
        
        # Re-enable execute button
        self.btn_execute.setEnabled(True)
        self.btn_execute.setText("Execute Query")
        
        # Enable export buttons
        self.update_ui_state(True)
    
    def on_query_error(self, error_message):
        """Handle query execution error"""
        QMessageBox.critical(self, "Query Error", f"Error executing query:\n\n{error_message}")
        
        # Update status
        self.label_results_info.setText("Query failed")
        self.label_execution_time.setText("Execution time: --")
        self.label_row_count.setText("Rows: 0")
        
        # Re-enable execute button
        self.btn_execute.setEnabled(True)
        self.btn_execute.setText("Execute Query")
        
        # Disable export buttons
        self.update_ui_state(False)
    
    def populate_results_table(self, results, headers):
        """Populate the results table with query data"""
        if not results or not headers:
            return
        
        # Set table dimensions
        self.table_results.setRowCount(len(results))
        self.table_results.setColumnCount(len(headers))
        
        # Set headers
        self.table_results.setHorizontalHeaderLabels(headers)
        
        # Populate data
        for row_idx, row_data in enumerate(results):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.table_results.setItem(row_idx, col_idx, item)
        
        # Auto-resize columns
        self.table_results.resizeColumnsToContents()
    
    def clear_query(self):
        """Clear the query text and results"""
        self.text_query.clear()
        self.table_results.clear()
        self.table_results.setRowCount(0)
        self.table_results.setColumnCount(0)
        
        self.current_results = []
        self.current_headers = []
        
        # Reset status
        self.label_results_info.setText("No query executed")
        self.label_execution_time.setText("Execution time: --")
        self.label_row_count.setText("Rows: 0")
        
        # Disable export buttons
        self.update_ui_state(False)
    
    def show_sample_queries(self):
        """Show a menu with sample queries"""
        menu = QMenu(self)
        
        for category, queries in self.sample_queries.items():
            category_menu = menu.addMenu(category)
            for query_name, query_sql in queries.items():
                action = QAction(query_name, self)
                action.triggered.connect(lambda checked, sql=query_sql: self.text_query.setPlainText(sql))
                category_menu.addAction(action)
        
        # Show menu at button position
        button_pos = self.btn_samples.mapToGlobal(self.btn_samples.rect().bottomLeft())
        menu.exec(button_pos)
    
    def refresh_connection(self):
        """Refresh database connection"""
        database = self.combo_database.currentText()
        self.label_connection_status.setText(f"Refreshing {database}...")
        
        # Simulate connection refresh
        QApplication.processEvents()
        time.sleep(0.5)
        
        self.label_connection_status.setText("Status: Connected")
        self.label_connection_status.setStyleSheet("color: green; font-weight: bold;")
    
    def on_database_changed(self, database_name):
        """Handle database selection change"""
        self.label_connection_status.setText(f"Connected to {database_name}")
        self.clear_query()  # Clear previous results when switching databases
    
    def export_to_csv(self):
        """Export results to CSV file"""
        if not self.current_results:
            QMessageBox.warning(self, "Warning", "No data to export")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(self.current_headers)
                    writer.writerows(self.current_results)
                
                QMessageBox.information(self, "Success", f"Data exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export data:\n{str(e)}")
    
    def export_to_excel(self):
        """Export results to Excel file (placeholder)"""
        if not self.current_results:
            QMessageBox.warning(self, "Warning", "No data to export")
            return
        
        QMessageBox.information(self, "Excel Export", 
                               "Excel export functionality would require additional libraries (e.g., openpyxl).\n"
                               "For now, please use CSV export.")
    
    def update_ui_state(self, has_results):
        """Update UI state based on whether we have results"""
        self.btn_export_csv.setEnabled(has_results)
        self.btn_export_excel.setEnabled(has_results)
    
    def get_sample_queries(self):
        """Return sample queries organized by category"""
        return {
            "Patient Queries": {
                "All Patients": "SELECT * FROM patient LIMIT 10",
                "Patients by Age": "SELECT hn, fname, lname, age FROM patient WHERE age > 50 LIMIT 10",
                "Recent Admissions": "SELECT * FROM patient WHERE admission_date >= '2024-01-01' LIMIT 10"
            },
            "Visit Queries": {
                "Today's Visits": "SELECT * FROM opd_visit WHERE visit_date = CURDATE() LIMIT 10",
                "Visit Summary": "SELECT visit_date, COUNT(*) as visit_count FROM opd_visit GROUP BY visit_date LIMIT 10",
                "Visits by Doctor": "SELECT doctor_code, COUNT(*) as patient_count FROM opd_visit GROUP BY doctor_code LIMIT 10"
            },
            "Doctor/Provider Queries": {
                "All Doctors": "SELECT * FROM doctor LIMIT 10",
                "Active Providers": "SELECT name, specialty, department FROM provider WHERE status = 'active' LIMIT 10"
            },
            "Statistics": {
                "Patient Count by Gender": "SELECT sex, COUNT(*) as count FROM patient GROUP BY sex",
                "Monthly Visit Trends": "SELECT YEAR(visit_date) as year, MONTH(visit_date) as month, COUNT(*) as visits FROM opd_visit GROUP BY YEAR(visit_date), MONTH(visit_date) LIMIT 12"
            }
        }


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Query()
    window.show()
    sys.exit(app.exec())
