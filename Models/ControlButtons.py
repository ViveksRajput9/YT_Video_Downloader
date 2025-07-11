from PySide6.QtWidgets import (
    QHBoxLayout,  QFrame,QPushButton
) 
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
class ControlButtons:
    def __init__(self, parent=None):
        super().__init__()
        self.pause_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\New folder\\icon\\pause.png"
        self.close_button_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\New folder\\icon\\close-button-png-30227.png"
        self.download_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\New folder\\icon\\pngwing.com.png"
        self.play_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\New folder\\icon\\video-play-icon-11403.png"

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon(self.pause_icon_path))
        self.pause_button.setIconSize(QSize(27, 27))
        self.pause_button.setFixedSize(50, 50)
        self.pause_button.setEnabled(False)
        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)

        self.cancel_button = QPushButton()
        self.cancel_button.setIcon(QIcon(self.close_button_icon_path))
        self.cancel_button.setIconSize(QSize(30, 30))
        self.cancel_button.setFixedSize(50, 50)
        self.cancel_button.setEnabled(False)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)

        self.download_button = QPushButton()
        self.download_button.setIcon(QIcon(self.download_icon_path))
        self.download_button.setIconSize(QSize(30, 30))
        self.download_button.setFixedSize(50, 50)
        self.download_button.setEnabled(False)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)


        self.play = QPushButton()
        self.play.setIcon(QIcon(self.play_icon_path))
        self.play.setIconSize(QSize(30, 30))
        self.play.setFixedSize(50, 50)
        self.play.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        


        self.layout = QHBoxLayout()
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.play)
    
    def apply_theme(self, theme):
        self.pause_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
        """)
        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
        """)
        self.download_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
        """)

