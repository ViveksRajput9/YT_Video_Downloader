from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QComboBox,QWidget, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from Gui.Pytoggle import Pytoggle
from Services.ThemeManager import ThemeManager
import threading

class Header:
    """A class to create a header for the application."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return  # Prevent reinitialization
        self._initialized = True
        """Initialize the header components."""
        self.container = QWidget()
        self.container.setContentsMargins(0, 0, 0, 0) # No margins
        self.container.setObjectName("header")
        self.container.setFixedHeight(45)  # Set a fixed height for the header
        self.main_layout = QHBoxLayout(self.container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.main_layout.setSpacing(5)  # Remove space between widgets
        self._initialize_components()
        self.apply_styles()

    def _initialize_components(self):
        """Initialize all components of the header."""
        self.logo_label = QLabel()
        pixmap = QPixmap("C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\New folder\\icon\\app_icon.png")
        pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setFixedSize(32, 32)

        self.name_label = QLabel("YouTube Video Downloader")
        self.name_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.minimize_button = QPushButton("—")
        self.fullscreen_button = QPushButton("⛶")
        self.close_button = QPushButton("✕")

        self.toggle_button  = Pytoggle()
        self.toggle_button.stateChanged.connect(self.toggle_theme)

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(ThemeManager.get_theme_names())
        ThemeManager.set_current_theme()
        # Use the current theme name instead of the theme dictionary
        self.theme_selector.setCurrentIndex(self.theme_selector.findText(ThemeManager.current_theme ))
        self.theme_selector.currentTextChanged.connect(self.update_theme)
        self.theme_selector.currentIndexChanged.connect(self.update_theme)

        self.main_layout.addWidget(self.logo_label)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.theme_selector)
        self.main_layout.addWidget(self.minimize_button)
        self.main_layout.addWidget(self.fullscreen_button)
        self.main_layout.addWidget(self.close_button)

    def get_layout(self):
        """Return the layout for the header."""
        return self.main_layout
    def get_container(self):
        """Return the container for the header."""
        return self.container
    def apply_styles(self):
        """Apply styles to the header components."""
        self.minimize_button.setStyleSheet(ThemeManager.get_button_style())
        self.fullscreen_button.setStyleSheet(ThemeManager.get_button_style())
        self.close_button.setStyleSheet(ThemeManager.get_button_style())
        # self.name_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {ThemeManager.get_label_style()}")

    def toggle_theme(self):
        # Increment the theme index and wrap around if it exceeds the number of themes
        current_index =  self.theme_selector.currentIndex()
        next_index = (current_index + 1) % len(ThemeManager.get_theme_names())
        self.theme_selector.setCurrentIndex(next_index)
    def update_widget_theme(self):
        # Set the current theme and apply it to the main window
        from Gui.Ui_Setup import Ui

        Ui().update_widget_theme()

    # Update the main window's theme
    def update_theme(self):
        """Update the theme based on the selected theme name."""
        from Gui.Ui_Setup import Ui

        Ui().update_theme()
        # Set the current theme in the ThemeManager
        selected_theme = self.theme_selector.currentText()
        ThemeManager.set_current_theme(selected_theme)
