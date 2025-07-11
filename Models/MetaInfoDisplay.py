from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, QLabel
)
from PySide6.QtCore import (
    Qt, QSize
)
from PySide6.QtGui import QMovie
from Gui.TextLabel import MarqueeLabel


class MetaInfoDisplay:
    def __init__(self, parent=None):
        super().__init__()
        loading_animation_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\New folder\\icon\\Ellipsis@1x-2.0s-200px-200px.gif"

        # Channel name
        self.channel_name = QLabel()
        self.channel_name.setAlignment(Qt.AlignLeft)
        self.channel_name.setFixedHeight(20)
        self.channel_name_loading_movie = QMovie(loading_animation_path)
        self.channel_name_loading_movie.setScaledSize(QSize(30,30))
        self.channel_name.setMovie(self.channel_name_loading_movie)

        # Duration
        self.duration = QLabel()
        self.duration.setAlignment(Qt.AlignCenter)
        self.duration.setFixedHeight(10)
        self.duration_loading_movie = QMovie(loading_animation_path)
        self.duration_loading_movie.setScaledSize(QSize(30,30))
        self.duration.setMovie(self.duration_loading_movie)

        # Max Quality Label
        self.max_Quality_Label = QLabel()
        self.max_Quality_Label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #FF073A;
                font-size: 12px;
                font-weight: bold;
                border: None;
            }
        """)
        self.max_Quality_Label.setAlignment(Qt.AlignRight)
        self.max_Quality_Label.setFixedHeight(20)
        self.max_Quality_Label_loading_movie = QMovie(loading_animation_path)
        self.max_Quality_Label_loading_movie.setScaledSize(QSize(30,30))
        self.max_Quality_Label.setMovie(self.max_Quality_Label_loading_movie)

        # Title Label
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label_loading_movie = QMovie(loading_animation_path)
        self.title_label_loading_movie.setScaledSize(QSize(30,30))
        self.title_label.setMovie(self.title_label_loading_movie)

        # Layouts
        self.layout = QVBoxLayout()
        # Views, Duration, Max Quality horizontal layout
        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.channel_name, alignment=Qt.AlignLeft)
        Hlayout.addWidget(self.duration, alignment=Qt.AlignCenter)
        Hlayout.addWidget(self.max_Quality_Label, alignment=Qt.AlignRight)
        self.layout.addLayout(Hlayout)

        # Title Layout
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        self.layout.addLayout(title_layout)


    def apply_theme(self, theme):
        self.channel_name.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: {theme['text']};
                font-size: 12px;
                font-weight: bold;
                border: None;
            }}
        """)
        self.duration.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: {theme['text']};
                font-size: 12px;
                font-weight: bold;
                border: None;
            }}
        """)
        self.max_Quality_Label.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: #FF073A;
                font-size: 12px;
                font-weight: bold;
                border: None;
            }}
        """)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: {theme['text']};
                font-size: 12px;
                font-weight: bold;
                border: None;
            }}
        """)

    def start_loading_animations(self):
        self.channel_name_loading_movie.start()
        self.duration_loading_movie.start()
        self.max_Quality_Label_loading_movie.start()
        self.title_label_loading_movie.start()

    def stop_loading_animations(self):
        if self.channel_name_loading_movie.state() == QMovie.Running:
            self.channel_name_loading_movie.stop()
            self.channel_name.setMovie(None)
        if self.duration_loading_movie.state() == QMovie.Running:
            self.duration_loading_movie.stop()
            self.duration.setMovie(None)
        if self.max_Quality_Label_loading_movie.state() == QMovie.Running:
            self.max_Quality_Label_loading_movie.stop()
            self.max_Quality_Label.setMovie(None)
        if self.title_label_loading_movie.state() == QMovie.Running:
            self.title_label_loading_movie.stop()
            self.title_label.setMovie(None)

    def update_channel_name(self, channel_name):
        if len(channel_name) > 25:
            channel_name = channel_name[:25] + "..."
        self.channel_name.setText(channel_name)

    def update_duration(self, duration_seconds):
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_text = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.duration.setText(duration_text)

    def update_max_quality(self, quality):
        self.max_Quality_Label.setText(f"{quality}p")

    def update_title(self, title):
        self.title_label.setText(title)


