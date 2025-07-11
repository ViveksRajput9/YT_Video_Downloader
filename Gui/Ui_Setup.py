from PySide6.QtWidgets import QVBoxLayout, QWidget
from .Header import Header
from .SearchBar import SearchBar
from .FilterBar import FilterBar
from .ContentArea import ContentArea
from Services.ThemeManager import ThemeManager
import threading

class Ui(QWidget):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,parent=None):
        if hasattr(self, "_initialized") and self._initialized:
            return  # Prevent reinitialization
        super().__init__()
        self._initialized = True
      

        self.container = QWidget()
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.container.setLayout(self.main_layout)

        self.header = None
        self.search_bar = None
        self.filter_bar = None
        self.content_area = None
        self.footer = None

        self.content_area = ContentArea()
        self._initialize_components()
        self.apply_style()

    def _initialize_components(self):
        """Initialize all UI components."""
        self._initialize_header()
        self._initialize_search_bar()
        self._initialize_filter_bar()
        self._initialize_content_area()


    def _initialize_header(self):
        """Initialize the header component."""
        self.header = Header()

        self.main_layout.addWidget(self.header.get_container())
        self.main_layout.addSpacing(2)  # Add spacing between header and search bar

    def _initialize_search_bar(self):
        """Initialize the search bar component."""
        self.search_bar = SearchBar(self)
        self.main_layout.addWidget(self.search_bar)


    def _initialize_filter_bar(self):
        """Initialize the filter bar component."""
        self.filter_bar = FilterBar(self,self.content_area)
        self.main_layout.addLayout(self.filter_bar.get_layout())


    def _initialize_content_area(self):
        """Initialize the content area component."""
  
        self.main_layout.addLayout(self.content_area.get_layout())


    def update_container_layout(self, widgets=None, container_width=900):
        """Update the layout of the content area."""
        container_width = self.container.width()
        self.content_area.update_container_layout(widgets, container_width)


    def get_container_width(self):
        return self.container.width()
    

    def apply_style(self):
        theme = ThemeManager.get_current_theme()
        """Apply styles to the main container and its components."""
        self.container.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['background']};
                color: {theme['text']};
                border-radius: 15px;
            }}
            QPushButton {{
                background-color: {theme['button']};
                color: {theme['button_text']};
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {theme['accent']};
            }}
            QComboBox {{
                background-color: {theme['widget_bg']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 5px;
            }}
        """)


    def get_container(self):
        """Return the main container widget."""
        return self.container
    
    # Methods to get instances of all components
    def get_header(self):
        """Return the instance of the Header component."""
        return self.header

    def get_search_bar(self):
        """Return the instance of the SearchBar component."""
        return self.search_bar

    def get_filter_bar(self):
        """Return the instance of the FilterBar component."""
        return self.filter_bar

    def get_content_area(self):
        """Return the instance of the ContentArea component."""
        return self.content_area


    def update_widget_theme(self):
        # Set the current theme and apply it to the main window
        widgets = self.get_content_area().get_widgets()
     
        for widget in widgets:
            widget.apply_Theme(ThemeManager.get_current_theme())

    # Update the main window's theme
    def update_theme(self):
        """Update the theme based on the selected theme name."""
        # Apply styles to all components
        self.get_header().apply_styles()
        self.get_filter_bar().apply_styles()
        self.get_search_bar().apply_styles()
        self.apply_style()
        self.update_widget_theme()

