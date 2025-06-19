#Don't modify this file. 
# using by 
# from AppSetting import app_settings
# then use app_settings methods to manage settings in other modules
from PyQt6.QtCore import QSettings
class AppSetting:
    def __init__(self):
        self.settings = QSettings("Plk Digital Health", "Super App")

    def set_value(self, key, value):
        """Set a value in settings"""
        self.settings.setValue(key, value)

    def get_value(self, key, default_value=None):
        """Get a value from settings"""
        return self.settings.value(key, default_value)

    def remove_key(self, key):
        """Remove a key from settings"""
        self.settings.remove(key)

    def clear_all(self):
        """Clear all settings"""
        self.settings.clear()

    def sync(self):
        """Force synchronization of settings to storage"""
        self.settings.sync()

app_settings = AppSetting()