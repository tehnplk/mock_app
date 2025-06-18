import sys
from PyQt6.QtWidgets import QMainWindow, QMdiSubWindow, QTextEdit, QApplication
from PyQt6.QtGui import QAction

from Main_ui import Main_ui
from About import About
from House import House
from Patient import Patient
from Person import Person
from Visit import Visit


class Main(QMainWindow, Main_ui):
    def __init__(self, parent=None, username=None, hash_cid=None):
        super().__init__(parent)
        self.setupUi(self)
        print("Main hash_cid:", hash_cid)

        # Track open windows
        self.open_windows = {}
        # Store current user information
        self.current_username = username
        self.current_hash_cid = hash_cid

        # Set window title with user info if provided
        if username and hash_cid:
            self.setWindowTitle(
                f"Hospital Management System - User: {username} ({hash_cid})"
            )
        elif username:
            self.setWindowTitle(f"Hospital Management System - User: {username}")
        elif hash_cid:
            self.setWindowTitle(f"Hospital Management System - User: {hash_cid}")

        # Connect About action
        self.about_action.triggered.connect(self.show_about)
        # Connect toolbar actions
        self.house_action.triggered.connect(self.show_house)
        self.person_action.triggered.connect(self.show_person)
        self.patient_action.triggered.connect(self.show_patient)
        self.visit_action.triggered.connect(self.show_visit)
        self.appoint_action.triggered.connect(self.show_appoint)

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
        """
        # Check if window is already open
        if (
            window_key in self.open_windows
            and self.open_windows[window_key].isVisible()
        ):
            # Bring existing window to front and activate it
            existing_window = self.open_windows[window_key]
            self.mdi_area.setActiveSubWindow(existing_window)
            existing_window.raise_()
            existing_window.activateWindow()
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
        sub_window.destroyed.connect(lambda: self.open_windows.pop(window_key, None))

        # Add to MDI area
        self.mdi_area.addSubWindow(sub_window)

        # Resize to 90% of parent MDI area (for main windows)
        if window_key in ["house", "person", "patient", "visit", "appoint"]:
            mdi_size = self.mdi_area.size()
            window_width = int(mdi_size.width() * 0.9)
            window_height = int(mdi_size.height() * 0.9)
            sub_window.resize(window_width, window_height)

            # Center the window in the MDI area
            x = (mdi_size.width() - window_width) // 2
            y = (mdi_size.height() - window_height) // 2
            sub_window.move(x, y)

        sub_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec())
