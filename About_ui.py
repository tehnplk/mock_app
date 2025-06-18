import sys

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QDialog
from PyQt6.QtCore import Qt

class About_ui(object):
    """
    UI class for About dialog.
    """
    
    def __init__(self):
        """
        Initialize the UI.
        """
        pass

    def setupUi(self, About_ui):
        """
        Set up the user interface for About dialog.
        """
        # Set dialog properties
        About_ui.setWindowTitle("About")
        About_ui.setFixedSize(400, 300)
        About_ui.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Create main layout
        self.main_layout = QVBoxLayout(About_ui)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        
        # Create title label
        self.title_label = QLabel("Main Application", About_ui)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.main_layout.addWidget(self.title_label)
        
        # Create version label
        self.version_label = QLabel("Version 1.0", About_ui)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        self.main_layout.addWidget(self.version_label)
        
        # Create description label
        self.description_label = QLabel("A PyQt6 application with menu system.\n\nBuilt with Python and PyQt6 framework.", About_ui)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setStyleSheet("font-size: 12px; color: #34495e; line-height: 1.5;")
        self.description_label.setWordWrap(True)
        self.main_layout.addWidget(self.description_label)
        
        # Add spacer
        self.main_layout.addStretch()
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        
        # Create OK button
        self.ok_button = QPushButton("OK", About_ui)
        self.ok_button.setFixedSize(80, 30)
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addStretch()
        
        # Add button layout to main layout
        self.main_layout.addLayout(self.button_layout)
        
        # Connect OK button
        self.ok_button.clicked.connect(About_ui.accept)

    def retranslateUi(self, About_ui):
        """
        Retranslate the user interface.
        """
        About_ui.setWindowTitle("About")
        self.title_label.setText("Main Application")
        self.version_label.setText("Version 1.0")
        self.description_label.setText("A PyQt6 application with menu system.\n\nBuilt with Python and PyQt6 framework.")
        self.ok_button.setText("OK")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QDialog()
    ui = About_ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
