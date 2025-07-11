from PySide6.QtCore import QEasingCurve
from PySide6.QtWidgets import  QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog,QHBoxLayout, QComboBox,QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from Gui.Pytoggle import Pytoggle
from config.config_manager import Config_Manager
from Services import Services
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint
from PySide6.QtGui import QPainter, QPainterPath, QColor
from PySide6.QtWidgets import  QDialog
from PySide6.QtCore import Qt,QThreadPool
from Gui.ContentArea import ContentArea
from Database.sqlDatabase import Database
from Models.Widget import SquareWidget
from Gui import toast_message
from Services.ThemeManager import ThemeManager
from pathlib import Path
import threading
from Gui.FilterBar import FilterBar
class OfflineVideos(QDialog):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,parent):
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        super().__init__(parent)
        self._initialized = True

        self.setWindowTitle("Offline list")
        self.setFixedSize(360,600)  # Set a fixed size for the dialog

        self.setAttribute(Qt.WA_TranslucentBackground)        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setContentsMargins(0,0,0,0)
   
        # layout.setSpacing(0)  # ✅ Ensures elements don't push against the border
        layout = QVBoxLayout()

        header_box = QHBoxLayout()
        header_label = QLabel("⏬ Offline videos")
        header_label.setFont(QFont("Arial", 12, QFont.Bold))
        header_box.addWidget(header_label)
        header_box.addStretch()
        closeButton = QPushButton("✕")
        closeButton.setFixedSize(30,30)
        closeButton.clicked.connect(self.cls)
        header_box.addWidget(closeButton)
        layout.addLayout(header_box)

        self.content_area = ContentArea(self.width())
        self.filter_bar = FilterBar(self,self.content_area)
        layout.addLayout(self.filter_bar.get_layout())

        layout.addLayout(self.content_area.get_layout())
        self.database = Database()
        self.setLayout(layout)
     # Add animation for smooth pop-in effect
    def view(self):
        self.show()
        self.show_animation()
        self.update_list()

    def update_list(self):
        self.content_area.remove_all_widgets()
        list =   self.database.get_videos_with_downloaded_path()
        if not list :
            toast_message.show_toast_notification("Offline video Empty")
            
        for video_data in list:
            file_path = Path(video_data.get('downloaded_path'))
            
            if file_path.exists() and file_path.is_file():

                widget = SquareWidget(self,self.content_area,"play_controller",False)
                self.add(widget,video_data)
    def add(self,widget:SquareWidget,data:dict):
            self.content_area.add_widget(widget)
            widget.update_data(data)
    
    def play(self,path):
        from videoPlayer.v2 import VideoPlayer
        self.player = VideoPlayer()
        self.player.show()
        self.player.load_video(path)
        self.player.play_pause()
        self.cls()

    def remove(self,widget):
         self.content_area.remove(widget)

    def update(self):
         self.content_area.update_container_layout()

    def paintEvent(self, event):
        """Custom painting to create rounded borders with a black background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create a rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)  # Radius of 20
    
        # Fill the rounded box with black color
        painter.fillPath(path, QColor("black"))  # Set background color to black
        
        # Draw the rounded rectangle outline
        painter.setPen(Qt.black)  # Border color (change if needed)
        painter.drawPath(path)
    
    def show_animation(self):
        """Position dialog in the right corner and animate."""
        x_pos,y_pos = self.position()
        self.update_position()
        # Apply animation
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(500)
        self.animation.setStartValue(QPoint(x_pos, y_pos + 50))  # Start lower
        self.animation.setEndValue(QPoint(x_pos, y_pos))  # Move to final position
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.start()

    def position(self):
        from Gui.Ui_Setup import Ui
        parent = Ui().get_content_area().get_scrollArea().window()

        parent_geometry = parent.geometry()  # Get the parent window size
        x_pos = parent_geometry.right() - self.width() - 5  # 20px margin from right
        y_pos = parent_geometry.top() + 100  # 20px margin from top
    
        # self.move(QPoint(x_pos, y_pos))  # Set position before animation starts
        return x_pos,y_pos
    def update_position(self):
        if self.parent() and hasattr(self.parent(), 'search_bar'):
            pos = self.parent().search_bar.mapToGlobal(self.parent().search_bar.rect().bottomLeft())
            self.move(pos)
    def get_container_width(self):
        return self.width()

    def cls(self):
       self.close()
