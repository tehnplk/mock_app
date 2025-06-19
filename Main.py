import sys
import os

from PyQt6.QtWidgets import QMainWindow, QMdiSubWindow, QTextEdit, QApplication, QDialog, QDialog
from PyQt6.QtGui import QAction, QShortcut, QKeySequence, QIcon
from PyQt6.QtCore import QTimer

from Main_ui import Main_ui
from About import About
from House import House
from Patient import Patient
from Person import Person
from Visit import Visit
from Query import Query
from HisConSetting import HisConSetting


class Main(QMainWindow, Main_ui):
    def __init__(self, parent=None, username=None, hash_cid=None):
        super().__init__(parent)
        self.setupUi(self)
        print("Main hash_cid:", hash_cid)

        # Set custom application icon
        self.set_application_icon()

        # Track open windows
        self.open_windows = {}
        # Store current user information
        self.current_username = username
        self.current_hash_cid = hash_cid# Set window title with user info if provided
        if username and hash_cid:
            self.setWindowTitle(
                f"Hospital Management System - User: {username} ({hash_cid})"
            )
        elif username:
            self.setWindowTitle(f"Hospital Management System - User: {username}")
        elif hash_cid:
            self.setWindowTitle(f"Hospital Management System - User: {hash_cid}")
          # Set up auto-quit timer for 30 seconds
        self.setup_auto_quit_timer(seconds=30)
        
        # Connect About action
        self.about_action.triggered.connect(self.show_about)        # Connect toolbar actions
        self.house_action.triggered.connect(self.show_house)
        self.person_action.triggered.connect(self.show_person)
        self.patient_action.triggered.connect(self.show_patient)
        self.visit_action.triggered.connect(self.show_visit)
        self.appoint_action.triggered.connect(self.show_appoint)
        self.query_action.triggered.connect(self.show_query)
        self.settings_action.triggered.connect(self.show_settings)
        
        # Add keyboard shortcut to cancel auto-quit timer (Ctrl+K)
        self.cancel_timer_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        self.cancel_timer_shortcut.activated.connect(self.cancel_auto_quit)

    def set_application_icon(self):
        """
        Set custom application icon with Finding Data theme.
        """
        try:
            # Get the directory where the script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "app_icon.png")
            
            if os.path.exists(icon_path):
                # Set window icon using the custom icon
                self.setWindowIcon(QIcon(icon_path))
                # Also set application icon for taskbar
                QApplication.instance().setWindowIcon(QIcon(icon_path))
                print(f"Application icon set from: {icon_path}")
            else:
                # Fallback: create icon from text if file doesn't exist
                print("Icon file not found, using fallback text icon")
                self.setWindowIcon(self.create_fallback_icon())
                QApplication.instance().setWindowIcon(self.create_fallback_icon())
        except Exception as e:
            print(f"Error setting application icon: {e}")
            # Use fallback icon
            self.setWindowIcon(self.create_fallback_icon())

    def create_fallback_icon(self):
        """
        Create a fallback icon using text/emoji if icon file is not available.
        """
        from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor
        from PyQt6.QtCore import Qt
        
        size = 32
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        font = QFont("Segoe UI Emoji", size - 8)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor("#2980b9"))  # Blue color
        
        # Use magnifying glass emoji as fallback
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "🔍")
        painter.end()
        
        return QIcon(pixmap)

    def set_user(self, username):
        """
        Set the current logged-in user.
        """
        self.current_username = username
        # Update window title to show logged-in user
        self.setWindowTitle(f"Hospital Management System - User: {username}")

    def get_current_user(self):
        """
        Get the current logged-in username.
        """
        return self.current_username

    def setup_auto_quit_timer(self, seconds=15):
        """
        Set up a timer to automatically quit the application after a specified number of seconds.
        """
        self.quit_countdown = seconds  # Use the specified countdown value

        # Main timer for quitting the application
        self.quit_timer = QTimer()
        self.quit_timer.setSingleShot(True)  # Timer runs only once
        self.quit_timer.timeout.connect(self.auto_quit_application)
        self.quit_timer.start(seconds * 1000)  # Convert seconds to milliseconds

        # Countdown timer for updating status bar every second
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown_display)
        self.countdown_timer.start(1000)  # Update every second

        print(f"Auto-quit timer started: Application will close in {seconds} seconds")
        self.update_countdown_display()  # Show initial countdown

    def update_countdown_display(self):
        """
        Update the status bar with countdown information.
        """
        if self.quit_countdown > 0:
            self.statusbar.showMessage(f"⏰ Auto-close in {self.quit_countdown}s | Press Ctrl+K to cancel")
            self.quit_countdown -= 1
        else:
            self.statusbar.showMessage("Closing application...")

    def auto_quit_application(self):
        """
        Automatically quit the application.
        """
        print("Auto-quit timer expired: Closing application...")
        self.countdown_timer.stop()  # Stop the countdown timer
        self.statusbar.showMessage("Application closed automatically")
        self.close()
        QApplication.quit()

    def cancel_auto_quit(self):
        """
        Cancel the auto-quit timer if user wants to continue using the application.
        """
        if hasattr(self, 'quit_timer') and self.quit_timer.isActive():
            self.quit_timer.stop()
            self.countdown_timer.stop()
            self.statusbar.showMessage("Auto-quit timer cancelled - Application will remain open")
            print("Auto-quit timer cancelled by user")
            return True
        return False

    def show_about(self):
        """
        Show the About dialog as a child window.
        """
        about_dialog = About(self)
        about_dialog.exec()

    def show_house(self):
        """
        Show the House management view.
        """
        self.show_window_single_instance("house", "House Management", House)

    def show_person(self):
        """
        Show the Person management view.
        """
        self.show_window_single_instance("person", "Person Management", Person)

    def show_patient(self):
        """
        Show the Patient management view.
        """
        self.show_window_single_instance("patient", "Patient Management", Patient)

    def show_visit(self):
        """
        Show the Visit management view.
        """
        self.show_window_single_instance("visit", "Visit Management", Visit)

    def show_appoint(self):
        """
        Show the Appointment management view.
        """

        def create_appoint_widget():
            text_edit = QTextEdit()
            text_edit.setPlainText(
                "Appointment Management System\n\nManage appointments here."
            )
            return text_edit

        self.show_window_single_instance(
            "appoint", "Appointments", create_appoint_widget
        )

    def show_query(self):
        """
        Show the Database Query tool.
        """
        self.show_window_single_instance("query", "Database Query Tool", Query)

    def show_settings(self):
        """
        Show the HIS Database Connection Settings dialog.
        """
        settings_dialog = HisConSetting(self)
        result = settings_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            # Settings were saved, you might want to update connections or notify other components
            self.statusbar.showMessage("Database settings updated successfully")
            print("HIS Database settings were updated")

    def create_mdi_window(self, title, content):
        """
        Create a new MDI window with the specified title and content.
        """
        # Create a new text editor
        text_edit = QTextEdit()
        text_edit.setPlainText(content)

        # Create MDI sub window
        sub_window = QMdiSubWindow()
        sub_window.setWidget(text_edit)
        sub_window.setWindowTitle(title)
        # Add to MDI area
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

    def show_window_single_instance(self, window_key, title, create_widget_func):
        """
        Show a window with single instance prevention.
        """        # Check if window is already open
        if (
            window_key in self.open_windows
            and self.open_windows[window_key].isVisible()
        ):
            # Bring existing window to front and activate it
            existing_window = self.open_windows[window_key]
            
            # First set as active sub window in MDI area
            self.mdi_area.setActiveSubWindow(existing_window)
            
            # Bring window to front
            existing_window.raise_()
            existing_window.show()  # Ensure it's visible
            existing_window.activateWindow()
            
            # Also set focus to the window
            existing_window.setFocus()
            
            # Update status bar to show which window was activated
            self.statusbar.showMessage(f"Activated existing {title} window")
            
            print(f"Activated existing {window_key} window")
            return

        # Create widget using the provided function
        widget = create_widget_func()

        # Create MDI sub window
        sub_window = QMdiSubWindow()
        sub_window.setWidget(widget)
        sub_window.setWindowTitle(title)

        # Store reference to prevent multiple instances
        self.open_windows[window_key] = sub_window

        # Connect window close event to clean up reference
        sub_window.destroyed.connect(lambda: self.open_windows.pop(window_key, None))        # Add to MDI area
        self.mdi_area.addSubWindow(sub_window)        # Resize to 90% of parent MDI area (for main windows)
        if window_key in ["house", "person", "patient", "visit", "appoint", "query"]:
            mdi_size = self.mdi_area.size()
            window_width = int(mdi_size.width() * 0.9)
            window_height = int(mdi_size.height() * 0.9)
            sub_window.resize(window_width, window_height)

            # Center the window in the MDI area
            x = (mdi_size.width() - window_width) // 2
            y = (mdi_size.height() - window_height) // 2
            sub_window.move(x, y)

        # Show and activate the new window
        sub_window.show()
        
        # Make sure the new window is active and on top
        self.mdi_area.setActiveSubWindow(sub_window)
        sub_window.raise_()
        sub_window.activateWindow()
        sub_window.setFocus()
        
        # Update status bar
        self.statusbar.showMessage(f"Opened new {title} window")
        
        print(f"Created new {window_key} window")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec())
