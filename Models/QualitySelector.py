
from PySide6.QtWidgets import (
    QHBoxLayout, QFrame, QComboBox)
from config.config_manager import Config_Manager

class QualitySelector:
    def __init__(self, parent=None):
        super().__init__()
        self.quality_selector = QComboBox()
        self.download_selector = ['Select Quality','Title','Description','Thumbnail','Tags']
        self.quality_selector.setMaximumWidth(400)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.quality_selector)

    def update_quality_selector(self, qualities):
        self.quality_selector.clear()
        self.quality_selector.addItems(self.download_selector)
        self.quality_selector.addItems(qualities)
        if Config_Manager().get_default_download_toggle():
            q =   Config_Manager().get_default_video_quality()
            q = q.split('-')
            
            s = q[0].strip()
            r = q[1].strip()
            selected_quality = None
            # qualities = qualities.reverse()
            for quality in qualities:
                if s in quality:
                    selected_quality = quality
                    if r in quality:
                       break

            self.quality_selector.setCurrentText(selected_quality or qualities[-1])


    def apply_theme(self, theme):
        self.quality_selector.setStyleSheet(f"""
            QComboBox {{
                background-color: {theme['widget_bg']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
