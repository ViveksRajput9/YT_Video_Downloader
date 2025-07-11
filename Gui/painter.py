from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QBrush, QColor

class QPainterContext:
    def __init__(self, widget):
        self.widget = widget
        self.painter = None

    def __enter__(self):
        self.painter = QPainter(self.widget)
        self.painter.setRenderHint(QPainter.Antialiasing)
        return self.painter

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.painter:
            self.painter.end()

