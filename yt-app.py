from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from Gui.Ui_Setup import Ui
from PySide6.QtCore import Qt, Slot, QThreadPool
from PySide6.QtGui import QBrush, QColor, QIcon
from Gui.painter import QPainterContext
from typing import Set, List
from queue import Queue
import logging
from BlurWindow.blurWindow import blur
import threading
from Services.Quality_Checking_Manager import QualityCheckingManager
from pathlib import Path
import sys
from Database.DownloadHistory import DownloadHistory
from Services.FFmpegHandler import FFmpegHandler
class YouTubeDownloader(QMainWindow):
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
        super().__init__()
        self._initialized = True

        # Initialize config
        self.setMinimumSize(1000, 700)
        DownloadHistory()  # Initialize download history database


        # Setup logging
        logging.basicConfig(
            filename=Path.home() / '.ytdownloader' / 'youtube_downloader.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Initialize Quality Manager
        if not hasattr(self, "quality_manager"):
            self.quality_manager = QualityCheckingManager()

        # Initialize variables
        self.downloading_list: List = []
        self.selected_list: List = []
        self.searched_list: Set = set()
        self.square_count: int = 0
        self.download_queue = Queue()
        self.download_location = None

        # Check for FFmpeg before initializing UI
        # import os
        # import tempfile
        # print("Temp Directory Path:", tempfile.gettempdir())
        # print(os.listdir(tempfile.gettempdir()))
        # Set up the main window
        self.setWindowIcon(QIcon("C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\YTDownloader\\icon\\app_icon.png"))
        self.setWindowTitle("YouTube Downloader")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(1.52)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        self.old_position = None
        blur(self.winId())

        # Initialize UI
        self.ui = Ui(self)
        self.setCentralWidget(self.ui.get_container())
        # Connect header buttons to parent methods
        self.ui.get_header().minimize_button.clicked.connect(self.showMinimized)
        self.ui.get_header().fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.ui.get_header().close_button.clicked.connect(self.sys_close)

    def sys_close(self):
        """Handle application exit."""
        QThreadPool.globalInstance().clear()  # Clear all threads in the thread pool
        sys.exit(0)

    # Enable Window Dragging
    def mousePressEvent(self, event):
        """Start dragging only if the header is clicked."""
        header = self.ui.get_header()
        if event.button() == Qt.LeftButton and header.get_container().underMouse():
            self.old_position = event.globalPos()
        else:
            self.old_position = None

    def mouseMoveEvent(self, event):
        """Move the window only if dragging started from the header."""
        if self.old_position:
            delta = event.globalPos() - self.old_position
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_position = event.globalPos()
            self.ui.get_search_bar().update_suggestion_position()            
    def mouseReleaseEvent(self, event):
        """Stop dragging."""
        if event.button() == Qt.LeftButton:
            self.old_position = None

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def resizeEvent(self, event):
        """Update layout on resize."""
        Ui().update_container_layout()
        super().resizeEvent(event)

    # Custom Paint Event for Shadow Effect
    def paintEvent(self, event):
        """Draw custom shadow effect."""
        super().paintEvent(event)
        with QPainterContext(self) as painter:
            shadow = QBrush(QColor(0, 0, 0, 100))
            painter.setBrush(shadow)
            painter.drawRoundedRect(self.rect(), 15, 15)

    @Slot(str, str, str)
    def show_message_box(self, type_name, title, message):
        """Show a message box."""
        if type_name == "critical":
            QMessageBox.critical(self, title, message)
        elif type_name == "warning":
            QMessageBox.warning(self, title, message)
        elif type_name == "information":
            QMessageBox.information(self, title, message)


if __name__ == "__main__":
    app = QApplication([])
    ffmpeg_handler = FFmpegHandler()
    if(ffmpeg_handler.check_ffmpeg()):
        window = YouTubeDownloader()
        window.show()
        app.exec()