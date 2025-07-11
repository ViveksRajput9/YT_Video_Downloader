from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox
from Services.ThemeManager import ThemeManager
from Services.SearchFilters import FilterManager
import threading
from Gui.ContentArea import ContentArea
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from Gui.toast_message import show_toast_notification

class FilterBar:
    def __init__(self,parent,content_area:ContentArea):
        self.filter_layout = QHBoxLayout()
        self.content_area = content_area
        self.parent = parent
        self.download_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\New folder\\icon\\pngwing.com.png"
        self._initialize_components()
        self._connect_signals()
        self.apply_styles()

    def _initialize_components(self):
        """Initialize all components of the filter bar."""
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Filter videos...")
        self.filter_layout.addWidget(self.search_filter)


        self.refresh_button = QPushButton("🔄")
        self.refresh_button.setToolTip("refresh")
        self.filter_layout.addWidget(self.refresh_button)


        from Gui import Wishlist,OfflineVideos
        if not isinstance(self.parent,OfflineVideos.OfflineVideos or Wishlist.Wishlist):
            self.initialize_download_button()

        self.clear_list_button = QPushButton("🗑️")
        self.clear_list_button.setToolTip("clear all widgets")
        self.filter_layout.addWidget(self.clear_list_button)


        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
           "Select", "Newest", "Oldest", "Highest Quality", "Lowest Quality",
            "Title", "Title (Descending)", "Duration", "Duration (Descending)"
        ])
        self.filter_layout.addWidget(self.sort_combo)


    def initialize_download_button(self):
        self.downloadAll_button = QPushButton()
        self.downloadAll_button.setToolTip("Download all videos")
        self.downloadAll_button.setIcon(QIcon(self.download_icon_path))
        self.downloadAll_button.setIconSize(QSize(15, 18))
        self.downloadAll_button.clicked.connect(self.content_area.downloadAll_video)
        self.filter_layout.addWidget(self.downloadAll_button)
        self.downloadAll_button.setStyleSheet(ThemeManager.get_button_style())

    def _connect_signals(self):
        """Connect signals to their respective slots."""
        self.search_filter.textChanged.connect(lambda text: self.filter_video(text))
        self.refresh_button.clicked.connect(self.refresh_list)
        self.sort_combo.currentTextChanged.connect(lambda text: self.sort_video(text))
        self.clear_list_button.clicked.connect(self.content_area.clearAllWidgets)

    def apply_styles(self):
        """Apply styles to the filter bar components."""
        self.search_filter.setStyleSheet(ThemeManager.get_line_edit_style())
        self.refresh_button.setStyleSheet(ThemeManager.get_button_style())

        self.clear_list_button.setStyleSheet(ThemeManager.get_button_style())
        self.sort_combo.setStyleSheet(ThemeManager.get_line_edit_style())

    def filter_video(self,text:str):
        widgets = FilterManager().filter_videos(text,self.content_area)
        width = self.parent.get_container_width()
        self.content_area.update_container_layout(widgets ,width)

    def sort_video(self,text):
        widgets = FilterManager().sort_videos(text,self.content_area)
        width = self.parent.get_container_width()
        self.content_area.update_container_layout(widgets ,width)


    def refresh_list(self,widgets=None):

        """Update the container layout (placeholder method)."""
        show_toast_notification("refresing")
        from Gui import Wishlist,OfflineVideos,Ui_Setup
        if isinstance(self.parent,Wishlist.Wishlist or OfflineVideos.OfflineVideos):
            self.parent.update_list()
        elif isinstance(self.parent,Ui_Setup.Ui):
            width = self.parent.get_container_width()
            self.content_area.update_container_layout(None,width)

    def get_layout(self):
        """Return the layout for the filter bar."""
        return self.filter_layout