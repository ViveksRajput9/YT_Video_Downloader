from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
import threading
from PySide6.QtCore import QPropertyAnimation

class ToastMessage(QWidget):
    # _instance = None
    # _lock = threading.Lock()

    # def __new__(cls, *args, **kwargs):
    #     with cls._lock:
    #         if cls._instance is None:
    #             cls._instance = super().__new__(cls)
    #             cls._instance._initialized = False  # Ensures the flag is always defined
    #     return cls._instance

    def __init__(self, message, parent=None):
        # if self._initialized:
        #     # Update the message if already initialized
        #     self.update_message(message)
        #     return
        
        super().__init__(parent)  # Properly initialize QWidget
        self._initialized = True  # Mark as initialized

 
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # Set up the layout and label
        layout = QVBoxLayout(self)
        self.label = QLabel(message, self)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_message(self, message):
        """Update the message of the toast."""
        self.remove()
        self.label.setText(message)
        self.show_toast()

    def show_toast(self, duration=3000):
        """Show the toast message for the specified duration (in milliseconds)."""
        self.adjustSize()
        # self.animation()
        self.move_to_center()
        self.show()
        self.remove(duration)

    def remove(self, duration=3000):
        duration = int(duration)
        QTimer.singleShot(duration, self.deleteLater)

    def animation(self):
        """Fade out the toast before closing."""
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(1000)  # Duration of fade-out (in milliseconds)
        animation.setStartValue(1.0)  # Start fully visible
        animation.setEndValue(0.0)  # End fully transparent
        animation.finished.connect(self.deleteLater)  # Close window after animation
        animation.start()
        
        # Auto-remove after the specified duration
    def move_to_center(self):
        """Position the toast message at the center of the parent widget or screen."""
        if self.parent():
            parent_geometry = self.parent().geometry()
            self.move(
                parent_geometry.x() + (parent_geometry.width() - self.width()) // 2,
                parent_geometry.y() + (parent_geometry.height() - self.height()) // 1.2
            )
        else:
            screen_geometry = self.screen().geometry()
            self.move(
                (screen_geometry.width() - self.width()) // 2,
                (screen_geometry.height() - self.height()) // 1.2
            )

def show_toast_notification(message, parent=None, duration=2000):
    """Display a toast notification."""
    from Gui.Ui_Setup import Ui
    parent = Ui().get_content_area().get_scrollArea().window()

    toast = ToastMessage(message, parent)
    toast.show_toast(duration)
