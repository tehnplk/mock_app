import sys
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QMenuBar, QStatusBar, QMdiArea, QApplication, QToolBar, QMainWindow
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

class Main_ui(object):
    """
    UI class for Main.
    """
    def setupUi(self, Main_ui):
        """
        Set up the user interface.
        """
        
        # Set window properties
        Main_ui.setWindowTitle("Main Application Window")
        Main_ui.setMinimumSize(800, 600)
        
        # Create menu bar
        self.menubar = QMenuBar(Main_ui)
        Main_ui.setMenuBar(self.menubar)

        # Create toolbar
        self.toolbar = QToolBar("Main Toolbar", Main_ui)
        self.toolbar.setMovable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        Main_ui.addToolBar(self.toolbar)

        # Create File menu
        self.file_menu = self.menubar.addMenu("File")
        self.edit_menu = self.menubar.addMenu("Edit")
        self.view_menu = self.menubar.addMenu("View")
        self.window_menu = self.menubar.addMenu("Window")
        self.help_menu = self.menubar.addMenu("Help")
        
        # Create actions for toolbar and menus
        self.house_action = QAction("House", Main_ui)
        self.house_action.setStatusTip("Go to house page")
        self.house_action.setShortcut("Ctrl+H")
        
        self.person_action = QAction("Person", Main_ui)
        self.person_action.setStatusTip("Manage person information")
        self.person_action.setShortcut("Ctrl+P")
        
        self.patient_action = QAction("Patient", Main_ui)
        self.patient_action.setStatusTip("Manage patient records")
        self.patient_action.setShortcut("Ctrl+T")
        
        self.visit_action = QAction("Visit", Main_ui)
        self.visit_action.setStatusTip("Manage patient visits")
        self.visit_action.setShortcut("Ctrl+V")
        
        self.appoint_action = QAction("Appoint", Main_ui)
        self.appoint_action.setStatusTip("Manage appointments")
        self.appoint_action.setShortcut("Ctrl+A")
        
        # Add actions to File menu
        self.file_menu.addAction(self.house_action)
        self.file_menu.addAction(self.person_action)
        self.file_menu.addAction(self.patient_action)
        self.file_menu.addAction(self.visit_action)
        self.file_menu.addAction(self.appoint_action)
        self.file_menu.addSeparator()
        
        # Add actions to toolbar
        self.toolbar.addAction(self.house_action)
        self.toolbar.addAction(self.person_action)
        self.toolbar.addAction(self.patient_action)
        self.toolbar.addAction(self.visit_action)
        self.toolbar.addAction(self.appoint_action)
        self.toolbar.addSeparator()
        
        # Create View toolbar actions
        self.cascade_toolbar_action = QAction("Cascade", Main_ui)
        self.cascade_toolbar_action.setStatusTip("Cascade all windows")
        
        self.tile_toolbar_action = QAction("Tile", Main_ui)
        self.tile_toolbar_action.setStatusTip("Tile all windows")
        
        # Add view actions to toolbar
        self.toolbar.addAction(self.cascade_toolbar_action)
        self.toolbar.addAction(self.tile_toolbar_action)
        
        # Create About action
        self.about_action = QAction("About", Main_ui)
        self.about_action.setStatusTip("Show information about this application")
        self.help_menu.addAction(self.about_action)
        
        # Create MDI area as central widget
        self.mdi_area = QMdiArea(Main_ui)
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        Main_ui.setCentralWidget(self.mdi_area)
        
        # Connect toolbar actions to MDI functionality (after MDI area is created)
        self.cascade_toolbar_action.triggered.connect(self.mdi_area.cascadeSubWindows)
        self.tile_toolbar_action.triggered.connect(self.mdi_area.tileSubWindows)
        
        # Add Window menu actions for MDI
        self.cascade_action = QAction("Cascade", Main_ui)
        self.cascade_action.setStatusTip("Cascade all windows")
        self.cascade_action.triggered.connect(self.mdi_area.cascadeSubWindows)
        self.window_menu.addAction(self.cascade_action)
        
        self.tile_action = QAction("Tile", Main_ui)
        self.tile_action.setStatusTip("Tile all windows")
        self.tile_action.triggered.connect(self.mdi_area.tileSubWindows)
        self.window_menu.addAction(self.tile_action)
        
        self.window_menu.addSeparator()
        
        self.close_all_action = QAction("Close All", Main_ui)
        self.close_all_action.setStatusTip("Close all windows")
        self.close_all_action.triggered.connect(self.mdi_area.closeAllSubWindows)
        self.window_menu.addAction(self.close_all_action)
        
        # Create status bar
        self.statusbar = QStatusBar(Main_ui)
        Main_ui.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")
        
        # Center and resize window to 80% of screen
        self.center_and_resize_window(Main_ui)

    def center_and_resize_window(self, Main_ui):
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
        y = 90  # 90px top margin from screen
        
        # Set window geometry
        Main_ui.setGeometry(x, y, width, height)

    def retranslateUi(self, Main_ui):
        """
        Retranslate the user interface.
        """
        Main_ui.setWindowTitle("Main Application Window")
        self.toolbar.setWindowTitle("Main Toolbar")
        self.house_action.setText("House")
        self.person_action.setText("Person")
        self.patient_action.setText("Patient")
        self.visit_action.setText("Visit")
        self.appoint_action.setText("Appoint")
        self.cascade_toolbar_action.setText("Cascade")
        self.tile_toolbar_action.setText("Tile")
        self.cascade_action.setText("Cascade")
        self.tile_action.setText("Tile")
        self.close_all_action.setText("Close All")
        self.statusbar.showMessage("Ready")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Main_ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
