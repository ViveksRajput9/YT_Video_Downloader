from PySide6.QtWidgets import (QHBoxLayout, QFrame, QLabel)
from PySide6.QtCore import Qt, QSize,QThread,QObject
from PySide6.QtGui import  QPixmap, QMovie

class ThumbnailDisplay(QObject):
    def __init__(self, parent=None):
        super().__init__()
        circle_animation_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\New folder\\icon\\Spinner@1x-1.0s-200px-200px(1).gif"
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(275, 160)

        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_loading_movie = QMovie(circle_animation_path)
        self.thumbnail_loading_movie.setScaledSize(QSize(150, 160))
        self.thumbnail_label.setMovie(self.thumbnail_loading_movie)

        self.layout = QHBoxLayout()
        self.layout.addStretch(1)
        self.layout.addWidget(self.thumbnail_label)
        self.layout.addStretch(1)
        self.layout.setAlignment(Qt.AlignCenter)

    def start_loading_animation(self):
        self.thumbnail_loading_movie.start()

    def stop_loading_animation(self):
        if self.thumbnail_loading_movie.state() == QMovie.Running:
            self.thumbnail_loading_movie.stop()
            self.thumbnail_label.setMovie(None)

    def set_thumbnail(self, pixmap):
        self.thumbnail_label.setScaledContents(True)  # Ensures full resolution display without alteration
        if pixmap is None:
            self.thumbnail_label.setText("Failed to load thumbnail")
        elif isinstance(pixmap, QPixmap):
            self.thumbnail_label.setPixmap(pixmap)
        else:
            self.thumbnail_label.setText("Invalid thumbnail format")

    def update_thumbnail(self, video_data):
        """Update thumbnail with downloaded image"""

        if self.thumbnail_loading_movie.state() == QMovie.Running :
            # Stop the loading animation
            self.thumbnail_loading_movie.stop()
            self.thumbnail_label.setMovie(None)

        from FetchData.ThumbnailWorker import ThumbnailWorker
        worker = ThumbnailWorker(video_data)
        worker.setParent(self) 
        worker.signals.finished.connect(self.set_thumbnail)
        worker.start()

    def apply_theme(self, theme):
        self.thumbnail_label.setStyleSheet(f"""
            QLabel {{
                background-color: {theme['widget_bg']};
                border-radius: 10px;
            }}
        """)

