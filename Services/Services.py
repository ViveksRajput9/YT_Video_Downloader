from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import Slot
from Database.DownloadHistory import DownloadHistory
import socket
import threading

from Models import HistoryDialog

class Service:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def show_history(self):
        history_dialog = HistoryDialog.HistoryDialog()
        history_dialog.populate_table(DownloadHistory().get_download_history())
        history_dialog.clear_button.clicked.connect(Service.clear_history)
        history_dialog.exec()

    def clear_history(self):
        DownloadHistory().clear_history()
        history_dialog = HistoryDialog.HistoryDialog()
        history_dialog.populate_table([])

    @staticmethod
    def is_internet_available():
        try:
            # Connect to the host -- tells us if the host is actually reachable
            socket.create_connection(("www.google.com", 80), timeout=10)
            return True
        except OSError:
            return False

    @staticmethod
    def show_directory():
        QFileDialog.getExistingDirectory(None, "Select Output Folder")
