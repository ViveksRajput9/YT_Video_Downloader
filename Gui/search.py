
### Updated in: Gui/SearchBar.py

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget
from PySide6.QtCore import Qt
from Services import ThemeManager
from Gui import settingDialog
from Database.SearchHistory import SearchHistory
from Gui.SuggestionList import SuggestionList
import threading

class SearchBar(QWidget):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.mainParent = None
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        search_bar_box = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter URL...")
        self.search_bar.setToolTip("Enter the URL of the video to download")
        self.search_bar.textChanged.connect(self.update_suggestions)
        self.search_bar.returnPressed.connect(self.on_search_clicked)
        self.search_bar.focusInEvent = self.on_focus_in
        self.search_bar.focusOutEvent = self.on_focus_out
        search_bar_box.addWidget(self.search_bar)

        self.suggestion_list = SuggestionList(self.search_bar, self.select_suggestion)
        self.suggestion_list.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.suggestion_list.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        search_bar_box.addWidget(self.suggestion_list)

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

        main_layout.addLayout(search_bar_box)
        main_layout.addSpacing(5)
        main_layout.addLayout(button_box)
        self.apply_styles()

    def on_search_clicked(self):
        from Gui import toast_message
        from Services.Services import Service
        if not Service.is_internet_available():
            toast_message.show_toast_notification("Internet Not Available")
            return

        toast_message.show_toast_notification("Searching...")
        url = self.search_bar.text().strip()
        if not hasattr(self, "quality_manager"):
            from Services.Quality_Checking_Manager import Quality_Checking_Manager
            self.quality_manager = Quality_Checking_Manager()
        self.quality_manager.check_qualities(url)

    def get_list(self):
        return SearchHistory().get_search_history()

    def update_suggestions(self):
        query = self.search_bar.text().strip().lower()
        if not query:
            self.isEmpty_show_suggestion()
            return

        titles = self.get_list()
        query_lower = query.lower()
        filtered = [str(title[1]) for title in titles if query_lower in str(title[1]).lower() or query_lower in str(title[0]).lower()]
        self.suggestion_list.show_suggestions(filtered)

    def select_suggestion(self, text):
        for url, title in self.get_list():
            if title.lower() in text.lower():
                self.search_bar.setText(url)
                break

    def isEmpty_show_suggestion(self):
        items = [i[1] for i in self.get_list()]
        self.suggestion_list.show_suggestions(items)

    def on_focus_in(self, event):
        if self.search_bar.text().strip():
            self.suggestion_list.show()
        else:
            self.search_bar.setText(' ')
            self.isEmpty_show_suggestion()
        super().focusInEvent(event)

    def on_focus_out(self, event):
        if not self.search_bar.text().strip():
            self.search_bar.setText('')
        self.suggestion_list.hide_suggestions()
        super().focusOutEvent(event)

    def show_settings_dialog(self):
        self.settings_popup = settingDialog.SettingsPopup()
        self.settings_popup.setModal(True)
        self.settings_popup.show()

    def apply_styles(self):
        self.search_bar.setStyleSheet(ThemeManager.ThemeManager.get_line_edit_style())
        self.search_button.setStyleSheet(ThemeManager.ThemeManager.get_button_style())
        self.settings_button.setStyleSheet(ThemeManager.ThemeManager.get_button_style())
        self.suggestion_list.setStyleSheet(ThemeManager.ThemeManager.get_list_widget_style())
