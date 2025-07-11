from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QWidget

class MarqueeLabel(QLabel):
    def __init__(self, text: str="None", parent: QWidget = None, animation_duration: int = 5000):
        super().__init__(text, parent)
        self.textlabel = text
        self.animation_duration = animation_duration  # Allow configurable animation duration
        self.setFont(QFont("Arial", 10, QFont.Bold))  # Set font size and style
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: 0px;
                color: black;
            }
        """)
        self.setAlignment(Qt.AlignLeft)
        self.setFixedWidth(300)  # Set width of the label, adjust as per your requirement
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Optional, makes text selectable

        # Set the animation for scrolling the text
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setLoopCount(-1)  # Infinite loop
        self.animation.setEasingCurve(QEasingCurve.Linear)  # Smooth linear animation

    def start_moving(self):
        """Starts the marquee animation."""
        text_width = self.fontMetrics().boundingRect(self.textlabel).width()

        if self.parent() is not None:  # Ensure parent exists before accessing its width
            start_pos = QPoint(self.parent().width(), 0)  # Start offscreen to the right
        else:
            start_pos = QPoint(self.width(), 0)  # Fallback to label width

        end_pos = QPoint(-text_width, 0)  # End offscreen to the left

        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.setDuration(self.animation_duration)  # Use configurable duration
        self.animation.start()
    def update_text(self,text):
        self.textlabel = text
    def showEvent(self, event):
        """Override showEvent to start the animation when the widget is fully shown."""
        super().showEvent(event)
        self.start_moving()  # Start moving text after the widget is shown
