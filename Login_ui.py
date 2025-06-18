import sys
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QApplication,
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
from config_auth import AUTH_CONFIG


class Login_ui(object):
    """
    UI class for Login window with WebEngine support.
    """

    def setupUi(self, Login_ui):
        """
        Set up the user interface for Login window.
        """
        # Set window properties
        Login_ui.setWindowTitle("Login - Hospital Management System")

        # Center and resize window to match Main window (80% of screen)
        self.center_and_resize_window(Login_ui)        # Create main layout with top margin
        self.main_layout = QVBoxLayout(Login_ui)
        self.main_layout.setContentsMargins(0, 15, 0, 0)  # Top margin 15px
        self.main_layout.setSpacing(0)

        # Panel 1: WebView Panel (for OAuth/web authentication)
        self.panel1 = QWidget()
        panel1_layout = QVBoxLayout(self.panel1)
        # Calculate margins for 95% width (2.5% on each side)
        screen = QApplication.primaryScreen()
        screen_width = int(screen.availableGeometry().width() * 0.8)  # Window is 80% of screen
        margin_x = int(screen_width * 0.025)  # 2.5% margin for 95% content width
        panel1_layout.setContentsMargins(margin_x, 10, margin_x, 10)
        panel1_layout.setSpacing(0)

        # Web view - 95% of parent width, centered
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("""
            QWebEngineView { 
                border: 1px solid #dfe6e9; 
                border-radius: 8px;
            }
        """)
        panel1_layout.addWidget(self.web_view, 1)  # stretch factor = 1 for full area
        
        # Panel 2: Progress Status and Button Panel (single column)
        self.panel2 = QWidget()
        panel2_layout = QVBoxLayout(self.panel2)
        panel2_layout.setContentsMargins(20, 40, 20, 40)
        panel2_layout.setSpacing(25)
        panel2_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Progress status label
        self.label_progress_login_status = QLabel("กำลังดำเนินการเข้าสู่ระบบ...")
        self.label_progress_login_status.setStyleSheet(
            """
            QLabel {
                color: #0984e3; 
                font-size: 18px; 
                margin: 20px; 
                padding: 20px; 
                font-weight: bold;
                text-align: center;
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                min-height: 60px;
                line-height: 1.6;
                max-width: 600px;
            }
        """
        )
        self.label_progress_login_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_progress_login_status.setWordWrap(True)
        panel2_layout.addWidget(self.label_progress_login_status)

        # Start Main Window button
        self.btn_start_main_window = QPushButton("เริ่มใช้งานระบบ")
        self.btn_start_main_window.setStyleSheet(
            """
            QPushButton {
                background-color: #00b894;
                color: white;
                border: none;
                padding: 20px 60px;
                border-radius: 12px;
                font-size: 20px;
                font-weight: bold;
                margin: 10px;
                max-width: 400px;
                min-height: 60px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #00a085;
            }
            QPushButton:pressed {
                background-color: #008f72;
            }
        """
        )        # Initially hide the button - will show after getting hash_cid
        self.btn_start_main_window.setVisible(False)
        panel2_layout.addWidget(self.btn_start_main_window)        # Add panels to main layout
        self.main_layout.addWidget(self.panel1, 1)  # panel1 expands to full area
        self.main_layout.addWidget(self.panel2)  # panel2 size according to content

        # Initially hide panel2 (will show when authentication is complete)
        self.panel2.setVisible(False)
        
        # Apply main window styles
        self.set_ui_styles(Login_ui)

    def set_ui_styles(self, Login_ui):
        """Set the UI style for the main window and all components"""
        Login_ui.setStyleSheet(
            """
            QWidget {
                background-color: #f5f6f7;
            }
            QLabel {
                color: #2d3436;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton {
                background-color: #0984e3;
                color: white;
                border: none;
                padding: 8px 16px;                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0878d4;
            }
        """
        )

    def center_and_resize_window(self, Login_ui):
        """
        Center the window horizontally and set it to 80% of screen size with 20px top margin.
        """
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Calculate 80% of screen dimensions
        width = int(screen_geometry.width() * 0.8)
        height = int(screen_geometry.height() * 0.8)

        # Calculate center position horizontally, 90px from top
        x = (screen_geometry.width() - width) // 2
        y = 90  # 90px top margin from screen        # Set window geometry
        Login_ui.setGeometry(x, y, width, height)

    def retranslateUi(self, Login_ui):
        """
        Retranslate the user interface.
        """
        Login_ui.setWindowTitle("Login - Hospital Management System")
        self.btn_start_main_window.setText("เริ่มใช้งานระบบ")
        self.label_progress_login_status.setText("กำลังดำเนินการเข้าสู่ระบบ...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    ui = Login_ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
