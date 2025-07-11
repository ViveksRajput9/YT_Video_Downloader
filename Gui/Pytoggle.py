from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import QEasingCurve, Qt, QPropertyAnimation, QPoint, Property
from PySide6.QtGui import QPainter, QColor

class Pytoggle(QCheckBox):
    def __init__(
            self,
            width=60,
            bg_color="#777",
            circle_color="#000",
            active_color="#48eb1e",
            animation_curve=QEasingCurve.OutBounce
    ):
        QCheckBox.__init__(self)

        # set default parameters
        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)
        # colors 
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color 

        # Create animation 
        self._circle_position = 3 
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500) # time in milliseconds

        # connect state changed
        self.stateChanged.connect(self.start_transition)
    
    # Create new set and get property
    @Property(float)# Get
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transition(self, value):
        self.animation.stop() # stop animation if running 
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)
        # start animation
        self.animation.start()
        
        print(f"status:{self.isChecked()}")

    # set new hit area 
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
    
    # draw new items
    def paintEvent(self, _):
        # set painter
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # set as no pen 
        p.setPen(Qt.NoPen)

        # Draw rectangle
        rect = self.rect()
        if not self.isChecked():
           #Draw bg 
           p.setBrush(QColor(self._bg_color))
           p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)
           
           # Draw circle 
           p.setBrush(QColor(self._circle_color))
           p.drawEllipse(self._circle_position, 3, 22, 22)
            
        else:
           #Draw bg
           p.setBrush(QColor(self._active_color))
           p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

           # Draw circle 
           p.setBrush(QColor(self._circle_color))
           p.drawEllipse(self._circle_position, 3, 22, 22)

        # End draw 
        p.end()

    def set_light_theme(self):
        self._bg_color = "#777"
        self._circle_color = "#000"
        self._active_color = "#48eb1e"
        self.update()

    def set_dark_theme(self):
        # CSS for Pytoggle in dark theme
        self._bg_color = "#FFF"
        self._circle_color ="#444"
        self._active_color = "#48eb1e"
        self.update()

    def set_theme(self, theme):
        """Apply the given theme to the Pytoggle component."""
        # Extract colors from the CSS string
        self._bg_color = self._extract_color(theme.CHECKBOX_CSS, "background-color", "#777")
        self._circle_color = self._extract_color(theme.CHECKBOX_CSS, "circle-color", "#000")
        self._active_color = self._extract_color(theme.CHECKBOX_CSS, "active-color", "#48eb1e")
        self.update()

    def _extract_color(self, css: str, property_name: str, default: str) -> str:
        """Extract a color value from a CSS string."""
        try:
            for line in css.splitlines():
                if property_name in line:
                    return line.split(":")[1].strip().replace(";", "")
        except Exception:
            pass
        return default