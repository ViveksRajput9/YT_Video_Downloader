from PySide6.QtCore import QEasingCurve
from PySide6.QtWidgets import  QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog,QHBoxLayout, QComboBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from Gui.Pytoggle import Pytoggle
from config.config_manager import Config_Manager
from Services import Services
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint
from PySide6.QtGui import QPainter, QPainterPath, QColor

from Services.ThemeManager import ThemeManager
class SettingsPopup(QDialog):

    """A class to create a settings dialog for the application."""
    def __init__(self ):
        super().__init__()
        self.setWindowTitle("settings")

        self.setFixedWidth(400)  # Set a fixed size for the dialog
        self.setMaximumHeight(500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Keep the dialog on top of other windows
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Ensures transparency
        
        # Add animation for smooth pop-in effect
        self.show_animation()
        layout = QVBoxLayout()
        # layout.setSpacing(0)  # ✅ Ensures elements don't push against the border
        self.config = Config_Manager()
        padding = 20  # Set padding size
        self.setGeometry(self.x() + padding, self.y() + padding, self.width() - (padding * 2), self.height() - (padding * 2))

        header_box = QHBoxLayout()
        header_label = QLabel(" ⚙️ Setting")
        header_label.setFont(QFont("Arial", 12, QFont.Bold))
        header_box.addWidget(header_label)
        header_box.addStretch()
        closeButton = QPushButton("✕")
        closeButton.setFixedSize(30,30)
        closeButton.clicked.connect(self.cls)
        header_box.addWidget(closeButton)
        layout.addLayout(header_box)

        path_box = QHBoxLayout()

        path_box.setAlignment(Qt.AlignTop)


        # Label and Line Edit for displaying the selected path
        self.path_entry = QLineEdit()
        self.path_entry.setReadOnly(True)  # Make it read-only
        self.path_entry.setText(self.config.get_download_path())  # Set the default path from config

        # Browse Button
        self.browse_button = QPushButton("📁 Browse")
        self.browse_button.setToolTip("Select Location")
        self.browse_button.clicked.connect(self.browse_directory)

       # Add widgets to layout
        path_box.addWidget(self.path_entry)
        path_box.addWidget(self.browse_button)
        layout.addLayout(path_box)

        # Animation layout 2
        animation_layout = QHBoxLayout()
        animation_layout.setAlignment(Qt.AlignTop)
        animation_label = QLabel("Loading Animation")
        animation_label.setToolTip("Enable/Disable Loading Animation")
        animation_layout.addWidget(animation_label)
     
        # animation toggle button
        self.animation_button = Pytoggle()
        self.animation_button.setChecked(self.config.get_loading_animation())  # Set default state to checked
        self.animation_button.setToolTip("Toggle Animation")
        self.animation_button.stateChanged.connect(self.on_animation_toggle)
        animation_layout.addWidget(self.animation_button)
        layout.addLayout(animation_layout)

        # dropdown layout 3
        dropdown_layout = QHBoxLayout() 
        dropdown_layout.setAlignment(Qt.AlignTop)
        dropdown_label = QLabel("Theme")
        comboBox = QComboBox()
        comboBox.addItems(ThemeManager.get_theme_names())
        comboBox.setCurrentText(self.config.get_default_theme())  # Set the default theme from config
        comboBox.setPlaceholderText("Select Theme")
        dropdown_label.setToolTip("Select Theme")
        dropdown_layout.addWidget(dropdown_label)
        
        # concurrent downloads box 4
        max_download_box = QHBoxLayout()
        max_download_box.setAlignment(Qt.AlignTop)
        # max concurrent downloads dropdown
        self.max_concurrent_downloads_label = QLabel("Max Concurrent Downloads")
        self.max_concurrent_downloads_label.setToolTip("Set Max Concurrent Downloads")
        max_download_box.addWidget(self.max_concurrent_downloads_label)
        self.max_concurrent_downloads = QComboBox()
        
        self.max_concurrent_downloads.setPlaceholderText("Max Concurrent Downloads")
        self.max_concurrent_downloads.setToolTip("Set Max Concurrent Downloads")
        self.max_concurrent_downloads.currentTextChanged.connect(self.config.set_max_concurrent_downloads)
        max_download_box.addWidget(self.max_concurrent_downloads)    
        layout.addLayout(max_download_box)
        self.update_thread_count()    

         # download history box
        download_history_box = QHBoxLayout()
        download_history_box.setAlignment(Qt.AlignTop)
        
        # download history checkbox
        self.download_history_label = QLabel("Download History")
        self.download_history_label.setToolTip("Enable/Disable Download History")
        download_history_box.addWidget(self.download_history_label)
        
        # Pytoggle for download history
        self.download_history = Pytoggle()
        self.download_history.setChecked(self.config.get_download_history())  # Set default state to checked
        self.download_history.stateChanged.connect(self.set_download_history)
        self.download_history.setToolTip("want to save  Download History")
        download_history_box.addWidget(self.download_history)


        self.history_button = QPushButton("View")
        self.history_button.setFixedWidth(50)
        self.history_button.clicked.connect(self.show_download_history)
        download_history_box.addWidget(self.history_button)
        # Add the layout to the main layout
        layout.addLayout(download_history_box)

        # search history box 6
        search_history_box = QHBoxLayout()
        search_history_box.setAlignment(Qt.AlignTop)
        # search history checkbox
        self.search_history_label = QLabel("Search History")
        self.search_history_label.setToolTip("Enable/Disable Search History")
        search_history_box.addWidget(self.search_history_label)
        self.search_history_button = Pytoggle()
        self.search_history_button.setChecked(self.config.get_search_history())  # Set default state to checked
        self.search_history_button.stateChanged.connect(self.search_history)
        self.search_history_button.setToolTip("Toggle Search History")
        search_history_box.addWidget(self.search_history_button)
        layout.addLayout(search_history_box)
        

        # set default theme
        theme_box = QHBoxLayout()
        theme_label = QLabel("Themes")
        theme_label.setToolTip("set Default Theme")
        theme_box.addWidget(theme_label)

        theme_selector = QComboBox()
        theme_selector.addItems(ThemeManager.get_theme_names())
        # Use the current theme name instead of the theme dictionary
        theme_selector.setCurrentIndex(theme_selector.findText(self.config.get_default_theme() ))
        theme_selector.currentTextChanged.connect(self.set_default_theme)
        theme_selector.setToolTip("set Default Theme")
        theme_box.addWidget(theme_selector)
        layout.addLayout(theme_box)



        suggestion_box = QHBoxLayout()
        suggestion_label= QLabel("Search Suggestion")
        suggestion_label.setToolTip("set Search list show or not")
        suggestion_box.addWidget(suggestion_label)
        suggestion_button = Pytoggle()
        suggestion_button.setChecked(self.config.get_isSuggestion())  # Set default state to checked
        suggestion_button.stateChanged.connect(self.update_suggestion)
        suggestion_button.setToolTip("Toggle Search suggestion List")
        suggestion_box.addWidget(suggestion_button)
        layout.addLayout(suggestion_box)
        
        default_quality_boxV = QVBoxLayout()
        default_quality_box = QHBoxLayout()
        default_quality_label= QLabel(" default_quality")
        default_quality_label.setToolTip("set default download quality")
        quality_selector = QComboBox()

        quality_selector.addItems([
    "Audio-60-webm",
    "Audio-78-webm",
    "Audio-51-webm",
    "Audio-68-webm",
    "Audio-129-m4a",
    "Audio-150-webm",
    "Audio-125-webm",
    "144p-mp4",
    "144p-webm",
    "240p-mp4",
    "240p-webm",
    "360p-mp4",
    "360p-webm",
    "480p-mp4",
    "480p-webm",
    "720p-mp4",
    "720p-webm",
    "720p60-mp4",
    "720p60-webm",
    "1080p-mp4",
    "1080p-webm",
    "1080p60-mp4",
    "1080p60-webm",
    "1440p60-webm",
    "2160p60-webm"
])
        quality_selector.setCurrentText(self.config.get_default_video_quality())
        quality_selector.currentTextChanged.connect(self.config.set_default_video_quality)
        default_quality_button = Pytoggle()
        default_quality_button.setChecked(self.config.get_default_download_toggle())  # Set default state to checked
        default_quality_button.stateChanged.connect(self.set_default_download_enable)
        default_quality_button.setToolTip("Toggle default download quality")
        default_quality_boxV.addWidget(default_quality_label)
        default_quality_box.addWidget(quality_selector)
        default_quality_box.addWidget(default_quality_button)
        default_quality_boxV.addLayout(default_quality_box)
        layout.addLayout(default_quality_boxV)

        # Save Button
        self.Reset_button = QPushButton("Reset")
        self.Reset_button.setToolTip("Reset Default Settings")
        self.Reset_button.clicked.connect(self.reset)  # Close the dialog when clicked
        layout.addWidget(self.Reset_button)

        self.setLayout(layout)

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
        from Gui.Ui_Setup import Ui
        parent = Ui().get_content_area().get_scrollArea().window()

        parent_geometry = parent.geometry()  # Get the parent window size
        x_pos = parent_geometry.right() - self.width() - 5  # 20px margin from right
        y_pos = parent_geometry.top() + 100  # 20px margin from top
    
        self.move(QPoint(x_pos, y_pos))  # Set position before animation starts
    
        # Apply animation
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(500)
        self.animation.setStartValue(QPoint(x_pos, y_pos + 50))  # Start lower
        self.animation.setEndValue(QPoint(x_pos, y_pos))  # Move to final position
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.start()
    
    def cls(self):
        self.close()
        self.deleteLater()

    def show_download_history(self):
        self.cls()
        Services.Service().show_history()

    def set_default_theme(self,theme):
        self.config.set_default_theme(theme)
        from Gui.Ui_Setup import Ui
        ui =Ui().get_header()
        ui.theme_selector.setCurrentIndex(ui.theme_selector.findText(theme))


    def update_suggestion(self,value):
        self.config.set_isSuggestion(value)

    def browse_directory(self):
        """Open a file dialog to select a directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if directory:
            self.path_entry.setText(directory)  # Set the selected path in the line edit
            self.config.set_download_path(directory)

    def on_animation_toggle(self, state):
        # Convert state to a boolean (True if checked, False if unchecked)
        is_checked = state == 2
        # Get the singleton instance of Config_Manager and set the loading animation
        self.config.set_loading_animation(is_checked)  # Now you can call the method on the instance

    def set_download_history(self, state):
        # Convert state to a boolean (True if checked, False if unchecked)
        is_checked = state == 2
        # Get the singleton instance of Config_Manager and set the loading animation
        self.config.set_download_history(is_checked)  # Now you can call the method on the instance

    def search_history(self, state):
        # Convert state to a boolean (True if checked, False if unchecked)
        is_checked = state == 2
        # Get the singleton instance of Config_Manager and set the loading animation
        self.config.set_search_history(is_checked)
    def set_default_download_enable(self, state):
        # Convert state to a boolean (True if checked, False if unchecked)
        is_checked = state == 2
        # Get the singleton instance of Config_Manager and set the loading animation
        self.config.set_default_download_enable(is_checked)
    def update_thread_count(self):
        count = self.config.get_total_thread()
        for i in range(count):
           self.max_concurrent_downloads.addItem(str(i+1))
        
        self.max_concurrent_downloads.setCurrentIndex(self.config.get_max_concurrent_downloads()-1)
   
    def reset(self):
        self.config.reset_config()
        self.cls()