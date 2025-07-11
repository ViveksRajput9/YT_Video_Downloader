from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget
from PySide6.QtCore import Qt
from Services import ThemeManager
from Gui import settingDialog
from Database.SearchHistory import SearchHistory
import threading
from config.config_manager import Config_Manager
from .SuggestionList import SuggestionList
from PySide6.QtCore import Qt
from Services import ThemeManager
from Gui import settingDialog
from Database.SearchHistory import SearchHistory
import threading
from config.config_manager import Config_Manager

class SearchBar(QWidget):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,parent=None):
        super().__init__(parent)
        self.mainParent = parent
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        self.config = Config_Manager()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.search_bar_box = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter URL...")
        self.search_bar.setToolTip("Enter the URL of the video to download")
        self.search_bar_box.addWidget(self.search_bar)

        button_box = QHBoxLayout()

        self.search_button = QPushButton("🔍")
        self.search_button.setToolTip("Search")
        self.search_button.clicked.connect(self.on_search_clicked)
        button_box.addWidget(self.search_button)
        button_box.addSpacing(3)

        self.settings_button = QPushButton("⚙️")
        self.settings_button.setToolTip("Settings")
        self.settings_button.clicked.connect(self.show_settings_dialog)
        button_box.addWidget(self.settings_button, alignment=Qt.AlignRight)
        button_box.addSpacing(3)

        self.wishlist_button = QPushButton("🛒")
        self.wishlist_button.setToolTip("Wishlist")
        self.wishlist_button.clicked.connect(self.show_wishlist)
        button_box.addWidget(self.wishlist_button)
        button_box.addSpacing(3)

        self.offline_video = QPushButton("⏬")
        self.offline_video.setToolTip("offline videos")
        self.offline_video.clicked.connect(self.show_downloaded_video)
        button_box.addWidget(self.offline_video)


        main_layout.addLayout(self.search_bar_box)
        main_layout.addSpacing(5)
        main_layout.addLayout(button_box)

        # Create and assign SuggestionList instance
        self.suggestion_list = SuggestionList(self)
        self.search_bar.textChanged.connect(self.on_text_changed)
        self.search_bar.returnPressed.connect(self.on_search_clicked)
        self.search_bar.focusInEvent = self.on_focus_in
        self.search_bar.focusOutEvent = self.on_focus_out



        # Connect itemClicked signal to set_url method
        self.suggestion_list.itemPressed.connect(self.set_url)

        self.search_bar_box.addWidget(self.suggestion_list)
        self.apply_styles()

    def on_text_changed(self, text):
        self.suggestion_list.update_suggestions(text)

    def set_url(self, item):
        url = self.suggestion_list.select_suggestion(item)
        
        self.search_bar.setText(url)
        self.suggestion_list.clear()
        self.suggestion_list.hide()  # Hide suggestions after selection
        self.on_search_clicked()
        self.search_bar.clear()
    def show_wishlist(self):
        from Gui.Wishlist import Wishlist
        wishlist = Wishlist(self.mainParent)
        wishlist.setModal(True)
        wishlist.view()
    def show_downloaded_video(self):
        from Gui.OfflineVideos import OfflineVideos
        offline_video = OfflineVideos(self.mainParent)
        offline_video.setModal(True)
        offline_video.view()
        
    def on_search_clicked(self):
        url = self.search_bar.text().strip()
        print(f"url--->{url}")
        if not hasattr(self, "quality_manager"):
            from Services.Quality_Checking_Manager import QualityCheckingManager
            self.quality_manager = QualityCheckingManager()
        self.quality_manager.check_qualities(url)
        self.suggestion_list.update_history_list()

    def on_focus_in(self, event):
        if self.config.get_isSuggestion():
            if self.search_bar.text().strip():
                self.suggestion_list.update_suggestions(self.search_bar.text())
            else:
                self.suggestion_list.show_all_suggestions()
        super().focusInEvent(event)

    def on_focus_out(self, event):
        if not self.search_bar.text().strip():
            self.search_bar.setText('')
        self.suggestion_list.hide_suggestions()
        super().focusOutEvent(event)

    def update_suggestion_position(self):
        self.suggestion_list.update_position()

    def show_settings_dialog(self):
        self.settings_popup = settingDialog.SettingsPopup()
        self.settings_popup.setModal(True)
        self.settings_popup.show()

    def apply_styles(self):
        button_style = ThemeManager.ThemeManager.get_button_style()
        self.search_bar.setStyleSheet(ThemeManager.ThemeManager.get_line_edit_style())
        self.search_button.setStyleSheet(button_style)
        self.settings_button.setStyleSheet(button_style)
        self.wishlist_button.setStyleSheet(button_style)
        self.offline_video.setStyleSheet(button_style)
        self.suggestion_list.setStyleSheet(ThemeManager.ThemeManager.get_list_widget_style())
