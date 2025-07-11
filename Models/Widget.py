from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox,
    QProgressBar, QPushButton
)
from PySide6.QtCore import (
    Qt, QSize, QTimer, QPropertyAnimation,
    QEasingCurve, QPoint, QThreadPool
)
from PySide6.QtGui import QIcon, QPixmap, QMovie
from Services import ThemeManager
from Gui.toast_message import show_toast_notification
from .ThumbnailDisplay import ThumbnailDisplay
from .MetaInfoDisplay import MetaInfoDisplay
from .ProgressDisplay import ProgressDisplay
from .ControlButtons import ControlButtons
from .QualitySelector import QualitySelector

class SquareWidget(QFrame):
    def __init__(self, parent=None, content_area=None,controller="progress_controller",isAnimation=True):
        super().__init__()
        self.prnt = parent
        self.content_area = content_area
        self.controller = controller
        self.pause_flag = False
        self.cancel_flag = False

        self.isAnimation = isAnimation
        self.video_data = None
        self.url = None

        self.setFixedWidth(300)
   
        # Components
        self.thumbnail_display = ThumbnailDisplay(self)
        self.meta_info_display = MetaInfoDisplay(self)
        self.progress_display = ProgressDisplay(self)
        self.control_buttons = ControlButtons(self)
        self.quality_selector = QualitySelector(self)

        # Layouts
        self.layout_box = QVBoxLayout() 
        self.layout_box.addLayout(self.thumbnail_display.layout)

        # Add meta info display (channel name, duration, max quality, title)
        self.layout_box.addLayout(self.meta_info_display.layout)
        if controller == "progress_controller" :
            self.setFixedHeight(370)
            self.enable_progress_control()
            self.set_download_control()
        elif controller == "play_controller":
            self.setFixedHeight(320)
            play_box = QHBoxLayout()
            play_box.addWidget(self.control_buttons.play)
            self.control_buttons.play.clicked.connect(self.play_video)
            self.layout_box.addLayout(play_box)

        self.layout_box.addStretch(1)
        self.setLayout(self.layout_box)

        # Animation and timer
        self.hold_timer = QTimer(self)
        self.hold_timer.setSingleShot(True)
        self.hold_timer.timeout.connect(self.on_hold_timeout)
        self.holding = False
        self.start_pos = None
        self.move_animation = QPropertyAnimation(self, b"pos")
        self.move_animation.setDuration(300)
        self.move_animation.setEasingCurve(QEasingCurve.OutQuad)

        # Connect buttons to methods
        self.control_buttons.pause_button.clicked.connect(self.pause_downloading)
        self.control_buttons.cancel_button.clicked.connect(self.cancel_downloading)
        self.control_buttons.download_button.clicked.connect(self.start_download)

        self.animation()
        self.apply_Theme(ThemeManager.ThemeManager.get_current_theme())

    def set_download_control(self):
                # Quality Selector + Download Button Layout
        Hlayout_quality = QHBoxLayout()
        Hlayout_quality.addWidget(self.quality_selector.quality_selector)
        Hlayout_quality.addWidget(self.control_buttons.download_button)
        self.layout_box.addLayout(Hlayout_quality)
    def enable_progress_control(self):
                # Progress Label
        self.layout_box.addWidget(self.progress_display.progress_label, alignment=Qt.AlignLeft)

        # ProgressBar + Pause + Cancel Buttons Layout
        Hlayout_progress = QHBoxLayout()
        Hlayout_progress.addWidget(self.progress_display.progress_Bar)
        Hlayout_progress.addWidget(self.control_buttons.pause_button)
        Hlayout_progress.addWidget(self.control_buttons.cancel_button)
        self.layout_box.addLayout(Hlayout_progress)

    def animation(self):
        from config.config_manager import Config_Manager
        config = Config_Manager()
        if config.get_loading_animation():
            self.meta_info_display.start_loading_animations()
            self.thumbnail_display.start_loading_animation()

    def mousePressEvent(self, event):
        self.start_pos = event.pos()
        self.holding = False
        self.hold_timer.start(300)  # 0.3 second
        super().mousePressEvent(event)

    def on_hold_timeout(self):
        self.holding = True

    def mousePressEvent(self, event):
        self.start_pos = event.pos()
        self.holding = False
        self.hold_timer.start(300)  # 0.3second
        super().mousePressEvent(event)

    def on_hold_timeout(self):
        self.holding = True  # User held for 1 second
   
    def mouseMoveEvent(self, event):
        """Handle mouse move event."""
        if self.holding and self.isAnimation:
            if self.video_data:
                dx = event.pos().x() - self.start_pos.x()
                if dx > 100:  # User dragged right by at least 100 pixels
                    self.animate_frame_move(dx, direction="right")
                    self.hold_timer.stop()
                    self.holding = False
                    print("dragged right")
                elif dx < -100:  # User dragged left by at least 100 pixels
                    self.animate_frame_move(dx, direction="left")
                    self.hold_timer.stop()
                    self.holding = False
                    print("dragged left")
                super().mouseMoveEvent(event)
            else:
                show_toast_notification('Please wait until it loads...')

    def animate_frame_move(self, dx, direction):
        """Animate the frame moving left or right before deletion, with smooth transition."""
        current_pos = self.pos()
        
        # Calculate the target position based on direction
        if direction == "right":
            target_pos = QPoint(current_pos.x() + abs(dx), current_pos.y())
            self.show_animation(target_pos,current_pos,'right')
        elif direction == "left":
            target_pos = QPoint(current_pos.x() - abs(dx), current_pos.y())
            self.show_animation(target_pos,current_pos,'left')
        else:
            return  # No valid direction
        

    def show_animation(self,current_pos,target_pos,movement):
            # Setup animation
            self.move_animation = QPropertyAnimation(self, b"pos")
            self.move_animation.setDuration(400)  # Duration in milliseconds
            self.move_animation.setStartValue(current_pos)
            self.move_animation.setEndValue(target_pos)
            
            # Set easing curve for smooth movement
            self.move_animation.setEasingCurve(QEasingCurve.OutCubic)  # You can try InOutQuad, OutElastic, etc.

            from Gui.Wishlist import Wishlist
            if 'right'  in movement:
                if  isinstance(self.prnt,Wishlist) :
                    self.move_animation.finished.connect(self.remove_wishlist)
                else:
                    self.move_animation.finished.connect(self.delete_widget)
            else:
                if  isinstance(self.prnt,Wishlist) :
                    self.move_animation.finished.connect(self.add_to_container)

                else:
                    self.move_animation.finished.connect(self.add_wishlist)

            self.move_animation.start()

    def mouseReleaseEvent(self, event):
        self.hold_timer.stop()
        self.holding = False
        super().mouseReleaseEvent(event)
    

    def add_to_container(self):
        from Gui.Ui_Setup import Ui
        Ui().get_content_area().add_new_widget(self.video_data)
        show_toast_notification('addend in Main screen')


    def remove_wishlist(self):
        from Database.sqlDatabase import Database
        if Database().update_wishlist(self.video_data.get('id'),False):
            show_toast_notification('removed from wishlist')
            self.setDisabled(True)
            self.deleteLater()
            self.prnt.update()

    def add_wishlist(self):
        from Database.sqlDatabase import Database
        if Database().update_wishlist(self.video_data.get('id'),True):
            show_toast_notification('added to wishlist')

    def delete_widget(self):
        """Handle the end of the animation."""
        # Ensure the parent is a valid QWidget
        show_toast_notification('Widget Deleted Successfully')
        from Services.Quality_Checking_Manager import QualityCheckingManager
        
        QualityCheckingManager().delete_url(self.url)  # Remove from search list
        self.deleteLater()  # Schedule deletion
        from Gui.Ui_Setup import Ui
        QTimer.singleShot(0, lambda: Ui().update_container_layout())  # Call layout update after event loop processes deletion
    def get_quality(self):
        return  self.quality_selector.quality_selector.currentText().strip()
    def play_video(self):
        path =  self.video_data.get('downloaded_path')
        if path:
            self.prnt.play(path)

    def get_download_button(self):
        return self.control_buttons.download_button
    
    def get_pause_button(self):
        return self.control_buttons.pause_button
    
    def get_cancel_button(self):
        return self.control_buttons.cancel_button
    
    def set_all_button_disabled(self):
        self.control_buttons.download_button.setEnabled(False)
        self.control_buttons.pause_button.setEnabled(False)
        self.control_buttons.cancel_button.setEnabled(False)

    def start_download(self):
        
        from Services.Downloading_Manager import Downloading_Manager
        quality = self.quality_selector.quality_selector.currentText().strip()
        Downloading_Manager().start_download(self, self.video_data, quality)

    def pause_downloading(self):
        if self.pause_flag:
            self.control_buttons.pause_button.setIcon(QIcon(self.control_buttons.pause_icon_path))
            self.pause_flag = False
        else:
            self.pause_flag = True
            self.control_buttons.pause_button.setIcon(QIcon(self.control_buttons.play_icon_path))

    def update_video_data(self, video_data:dict):
        self.video_data = video_data
        
        self.url = video_data.get('url')


    def update_data(self, data: dict):
        self.video_data = data
        self.url = data.get('url')

        self.update_quality_selector(data.get('qualities', ''))
        self.update_channel_name(data.get('uploader', ''))
        self.update_title(data.get('title', ''))
        self.update_duration(data.get('duration', 0))
        self.update_max_quality(data.get('highest_quality'))
        self.update_thumbnail()

    def update_quality_selector(self, qualities):
        self.quality_selector.update_quality_selector(qualities)

    def update_channel_name(self, uploader):
        self.meta_info_display.update_channel_name(uploader)

    def update_title(self, title):
        if self.controller == "progress_controller":
            if len(title) > 60:
                title = title[:60] + "..."
        else:
            self.meta_info_display.title_label.setWordWrap(True)
        self.meta_info_display.update_title(title)
        
    def update_duration(self, duration):
        self.meta_info_display.update_duration(duration)

    def update_max_quality(self, highest_quality):
        self.meta_info_display.update_max_quality(highest_quality)

    def update_thumbnail(self):
        self.thumbnail_display.update_thumbnail(self.video_data)

    def enable_download_button(self):
        self.control_buttons.download_button.setEnabled(True)

    def cancel_downloading(self):
        self.cancel_flag = True

    def update_progress_bar(self, value):
        self.progress_display.update_progress_bar(value)

    def update_progress_label(self, value):
        self.progress_display.update_progress_label(value)
    
    def update_quality_selector(self, qualities):
        self.quality_selector.update_quality_selector(qualities)
        self.control_buttons.download_button.setEnabled(True)

    def apply_Theme(self, theme):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {theme['widget_bg']};
                border: 1px solid {theme['border']};
                border-radius: 20px;
            }}

            QFrame:hover {{
                border: 1px solid #aaaaaa;
            }}

            QLabel {{
                color: {theme['text']};
            }}

            QPushButton {{
                background-color: {theme['button']};
                color: {theme['button_text']};
                border: none;
            }}
        """)

        self.thumbnail_display.apply_theme(theme)
        self.meta_info_display.apply_theme(theme)
        self.progress_display.apply_theme(theme)
        self.quality_selector.apply_theme(theme)
        self.control_buttons.apply_theme(theme)


