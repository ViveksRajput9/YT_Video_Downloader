from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QCheckBox, QGridLayout,QWidget,QScrollArea
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from Gui.Pytoggle import Pytoggle 
from Models.Widget import SquareWidget
from Services import ThemeManager,SearchFilters,Quality_Checking_Manager,Services
from Gui import settingDialog
import threading
class ContentArea:
    def __init__(self,parent=None,width=0):
        self.width = width
        self.prnt = parent
        # Prevent reinitialization
        self._initialized = True
        self.layout = QVBoxLayout()
        self.ScrollArea = QScrollArea()
        self.ScrollArea.setWidgetResizable(True)
        # self.ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create a container widget for the scroll area
        self.content_widget = QWidget()
        self.content_layout = QGridLayout()  # Use QGridLayout for grid arrangement
        self.content_widget.setLayout(self.content_layout)
        self.ScrollArea.setWidget(self.content_widget)
        self.layout.addWidget(self.ScrollArea)
    def get_layout(self):
        return self.layout
    def get_widgets(self):
       return  self.content_widget.findChildren(SquareWidget)
    def add_new_widget(self,data:dict):
        widget =  SquareWidget()
        widget.update_data(data)
        self.add_widget(widget)
    def remove(self,widget):
        self.content_layout.removeWidget(widget)
    def get_scrollArea(self):
        return self.ScrollArea
    
    def get_container_width(self=None):
        return self.content_widget.width()
    def update_widget_theme(self, theme):
        # Set the current theme and apply it to the main window
        widgets = self.get_widgets()
        for widget in widgets:
            print("updating widget theme")
            widget.apply_Theme(theme)
        

    def update_container_layout(self, widgets=None, container_width=900):
        """Update the layout of the content area."""
        widget_width = 300

        if self.width==0:
            container_width = container_width -10
        else:
            container_width = self.width
        columns = max(1, container_width // widget_width)
        if not widgets :
            widgets = self.get_widgets()
        for widget in widgets:
            self.content_layout.removeWidget(widget)
        for i, widget in enumerate(widgets):
            
            row, col = divmod(i, columns)
            widget.apply_Theme(ThemeManager.ThemeManager.get_current_theme())
            self.content_layout.addWidget(widget, row, col)
    def remove_all_widgets(self,widgets=None):
        if not widgets or widgets is None:
            widgets = self.get_widgets()
        for widget in widgets:
            self.content_layout.removeWidget(widget)
    
    def add_widget(self,widget):

        widget_width = 300
        count = len(self.get_widgets())
        if self.width==0:
            container_width = self.content_widget.width() -15
        else:
            container_width = self.width
        items_per_row = container_width // widget_width
        current_row = count // items_per_row
        column_item = count % items_per_row
        self.content_layout.addWidget(widget, current_row, column_item)
        return True
    
    def downloadAll_video(self):
        
        widgets = self.get_widgets()
        from Services.Downloading_Manager import Downloading_Manager
        d = Downloading_Manager()
        for w in widgets:
            quality = w.get_quality()
            d.start_download(w, w.video_data, quality)

    def clearAllWidgets(self):
    
        widgets = self.get_widgets()
        for w in widgets:
            w.deleteLater()
        self.update_container_layout()