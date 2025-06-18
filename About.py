import sys
from PyQt6.QtWidgets import QDialog, QApplication

from About_ui import About_ui

class About(QDialog, About_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Set parent-child relationship
        if parent:
            self.setParent(parent)
            # Center the dialog relative to parent
            self.center_on_parent()
    
    def center_on_parent(self):
        """
        Center the dialog on the parent window.
        """
        if self.parent():
            parent_geometry = self.parent().geometry()
            dialog_geometry = self.geometry()
            
            # Calculate center position
            x = parent_geometry.x() + (parent_geometry.width() - dialog_geometry.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - dialog_geometry.height()) // 2
            
            self.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = About()
    window.show()
    sys.exit(app.exec())
