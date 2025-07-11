from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QListWidget
from PySide6.QtCore import Qt
from Services import ThemeManager
from Gui import settingDialog
from Database.SearchHistory import SearchHistory
import threading
from config.config_manager import Config_Manager

class SuggestionList(QListWidget):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if hasattr(self, "_initialized") and self._initialized:
            return
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.hide()
        
        self.config = Config_Manager()
        self._initialized = True
        self.searchInstance = SearchHistory()
        self.update_history_list()

    def update_history_list(self):
        self.titles = self.searchInstance.get_search_history()

    def update_suggestions(self, query:str):
        self.clear()
        if not self.config.get_isSuggestion():
            self.hide()
            return
        if not query:
            self.show_all_suggestions()
            return
        query = query.strip().lower()

        filtered = [str(title[1]).lower() for title in self.titles if   query in str(title[1]).lower() or query in str(title[0]).lower()]  
    
        if filtered:
            self.show_suggestions(filtered)
        else:
            self.show_suggestions([])

    
    def show_all_suggestions(self):
        items = [i[1] for i in self.titles] if self.titles else []
        self.show_suggestions(items)

    def show_suggestions(self, suggestions):
        self.hide()
        self.clear()
        if suggestions:
            self.addItems(suggestions)
            self.adjust_size(len(suggestions))
            self.update_position()
            self.raise_()
            self.show()
        else:
            self.addItem("no matches found")
            self.adjust_size(1)
            self.update_position()
            self.raise_()
            self.show()

    def select_suggestion(self, item):
        print("Item clicked:", item.text())  # Debugging statement
        for i in self.titles:
            title = str(i[1]).lower()
            if title in item.text().lower():
                url = i[0]
                return str(url)
        self.hide()

    def update_position(self):
        if self.parent() and hasattr(self.parent(), 'search_bar'):
            pos = self.parent().search_bar.mapToGlobal(self.parent().search_bar.rect().bottomLeft())
            self.move(pos)

    def adjust_size(self, item_count):
        max_height = min(item_count * 20, 150)
        self.setMaximumHeight(max_height)
        if self.parent() and hasattr(self.parent(), 'search_bar'):
            self.setFixedWidth(self.parent().search_bar.width())

    def hide_suggestions(self):
        self.hide()

    def handle_key_enter(self):
        print("Handling enter key")  # Debugging statement
        if self.isVisible():
            selected = self.currentItem()
            if selected:
                self.select_suggestion(selected)
