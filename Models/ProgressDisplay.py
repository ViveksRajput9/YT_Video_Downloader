from PySide6.QtWidgets import (
     QVBoxLayout, QFrame, QLabel, QProgressBar
)
from PySide6.QtCore import Qt


class ProgressDisplay:
    def __init__(self, parent=None):
        super().__init__()
        self.progress_Bar = QProgressBar()
        self.progress_label = QLabel("0%")
        self.progress_label.setAlignment(Qt.AlignLeft)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.progress_Bar)
        self.layout.addWidget(self.progress_label, alignment=Qt.AlignLeft)

    def update_progress_bar(self, value):
        self.progress_Bar.setValue(value)

    def update_progress_label(self, value):
        self.progress_label.setText(f"{value}%")

    def apply_theme(self, theme):
        self.progress_Bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {theme['border']};
                border-radius: 4px;
                background-color: {theme['widget_bg']};
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {theme['accent']};
                border-radius: 3px;
            }}
        """)
        self.progress_label.setStyleSheet(f"""
            QLabel {{
                color: {theme['text']};
                font-size: 10px;
                font-weight: bold;
            }}
        """)

