from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QProgressBar, QPushButton
from PySide6.QtCore import Qt , QSize,QTimer, QPropertyAnimation, QEasingCurve, QRect, QPoint, QThreadPool
from PySide6.QtGui import QIcon, QPixmap, QMovie
import sys
from Gui.toast_message import show_toast_notification

from PySide6.QtWidgets import QFrame
# Assuming ThumbnailDisplay is already defined elsewhere
# from Gui.ThumbnailDisplay import ThumbnailDisplay
from Services import ThemeManager
class SquareWidget(QFrame):
    def __init__(self,parent = None, content_area=None):
        super().__init__()
        self.prnt = parent
        self.content_area = content_area
        self.pause_flag = False
        self.cancel_flag = False
        self.video_data = {}
        self.hold_timer = QTimer(self)
        self.hold_timer.setSingleShot(True)
        self.hold_timer.timeout.connect(self.on_hold_timeout)
        self.holding = False
        self.start_pos = None

        self.setFixedSize(300, 370)  # Set the fixed size of the square widget
        self.play_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\YTDownloader\\icon\\video-play-icon-11403.png"  # Path to your play icon
        loading_animation_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\YTDownloader\\icon\\Ellipsis@1x-2.0s-200px-200px.gif" # Path to your loading animation"icon\\Ellipsis@1x-2.0s-200px-200px.gif"
        self.pause_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\YTDownloader\\icon\\pause.png"  # Path to your pause icon
        close_button_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\YTDownloader\\icon\\close-button-png-30227.png"  # Path to your close button icon
        download_icon_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\YTDownloader\\icon\\pngwing.com.png"  # Path to your download icon
        circle_animation_path = "C:\\Users\\Abhishek Rajput\\Downloads\\GuiProjects-main\\GuiProjects-main\\YTDownloader\\icon\\Spinner@1x-1.0s-200px-200px(1).gif"
       
       
       
        # Initialize thumbnail label with loading placeholder
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(275, 160)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)  # Align the label content to the center

        self.thumbnail_loading_movie = QMovie(circle_animation_path)  # Add your GIF file here
        self.thumbnail_loading_movie.setScaledSize(QSize(150, 160))  # Scale the GIF to fit the label size
        self.thumbnail_label.setMovie(self.thumbnail_loading_movie)
        # Center the thumbnail by adding it to a QHBoxLayout
        thumbnail_layout = QHBoxLayout()
        thumbnail_layout.addStretch(1)  # Add space before the thumbnail
        thumbnail_layout.addWidget(self.thumbnail_label)  # Add the thumbnail widget
        thumbnail_layout.addStretch(1)  # Add space after the thumbnail
        thumbnail_layout.setAlignment(Qt.AlignCenter)  # Align content center
        # Adjust the layout of the square widget to include this centered thumbnail layout
        layout = QVBoxLayout()
        layout.addLayout(thumbnail_layout)  # Use the thumbnail_layout to center the thumbnail



        # Views Label
        self.channel_name = QLabel()
        self.channel_name.setAlignment(Qt.AlignLeft)  # Align views count to the left
        self.channel_name.setFixedHeight(20)  # Set a fixed height for proper alignment
        # Set the loading animation for the channel name label
        self.channel_name_loading_movie = QMovie(loading_animation_path)  # Add your GIF file here
        self.channel_name_loading_movie.setScaledSize(QSize(30, 30))  # Scale the GIF to fit the label size
        self.channel_name.setMovie(self.channel_name_loading_movie)




        # Duration Label
        self.duration = QLabel()
        self.duration.setAlignment(Qt.AlignCenter)
        self.duration.setFixedHeight(10)  # Set a fixed height for proper alignment
        # Set the loading animation for the duration label
        self.duration_loading_movie = QMovie(loading_animation_path)  # Add your GIF file here
        self.duration_loading_movie.setScaledSize(QSize(30, 30))  # Scale the GIF to fit the label size
        self.duration.setMovie(self.duration_loading_movie)

      
      
      
        # Max Quality Label
        self.max_Quality_Label = QLabel()  # Initial loading text
                # Apply theme to the max quality label
        self.max_Quality_Label.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: #FF073A;
                font-size: 12px;
                font-weight: bold;
                border: None;
            }}
        """)
        self.max_Quality_Label.setAlignment(Qt.AlignRight)
        self.max_Quality_Label.setFixedHeight(20)  # Set a fixed height for proper alignment
        # Set the loading animation for the max quality label
        self.max_Quality_Label_loading_movie = QMovie(loading_animation_path)  # Add your GIF file here
        self.max_Quality_Label_loading_movie.setScaledSize(QSize(30, 30))  # Scale the GIF to fit the label size
        self.max_Quality_Label.setMovie(self.max_Quality_Label_loading_movie)




        # Title Label
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignLeft)  # Align title to the left
        # self.title_label.setFixedHeight(30)  # Set a fixed height for proper alignment
        # Set the loading animation for the title label
        self.title_label_loading_movie = QMovie(loading_animation_path)  # Add your GIF file here
        self.title_label_loading_movie.setScaledSize(QSize(30, 30))  # Scale the GIF to fit the label size
        self.title_label.setMovie(self.title_label_loading_movie)
    
    
    
        # Progress Bar
        self.progress_Bar = QProgressBar()
        # Progress Label
        self.progress_label = QLabel("0%")
        self.progress_label.setAlignment(Qt.AlignLeft)



        # Pause resume Button
        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon(self.pause_icon_path))
        self.pause_button.setIconSize(QSize(27, 27))  # Set icon size to 30x30 pixels
        self.pause_button.setFixedSize(50, 50)  # Set the size of the button
        self.pause_button.setEnabled(False)
        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)

        self.pause_button.clicked.connect(self.pause_downloading)



        # Cancel Button
        self.cancel_button = QPushButton()
        self.cancel_button.setIcon(QIcon(close_button_icon_path))
        self.cancel_button.setIconSize(QSize(30, 30))  # Set icon size to 30x30 pixels
        self.cancel_button.setFixedSize(50, 50)  # Set the size of the button
        self.cancel_button.setEnabled(False)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)

        self.cancel_button.clicked.connect(self.cancel_downloading)


        # Quality Selector
        self.download_selector = ['Title','Description','Thumbnail','Tags']
        self.quality_selector = QComboBox()  # Make it instance variable
        self.quality_selector.setMaximumWidth(400)


        # download button
        self.download_button  = QPushButton()
        self.download_button.setEnabled(False)
        self.download_button.setIcon(QIcon(download_icon_path))
        self.download_button.setFixedSize(QSize(30,30))
        self.download_button.setIconSize(QSize(30, 30))  # Set icon size to 30x30 pixels
        self.download_button.setFixedSize(50, 50)  # Set the size of the button
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)        # Connect to a method instead of calling it directly
        self.download_button.clicked.connect(self.start_download)

     
        # Add a horizontal layout for views and max quality
        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.channel_name, alignment=Qt.AlignLeft)  # Align views count to the left
        Hlayout.addWidget(self.duration,alignment=Qt.AlignCenter)
        Hlayout.addWidget(self.max_Quality_Label, alignment=Qt.AlignRight)  # Align max quality to the right
        layout.addLayout(Hlayout)


        # Title Label
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        layout.addLayout(title_layout)
        # Progress label
        layout.addWidget(self.progress_label, alignment=Qt.AlignLeft)


        # Progress Bar + Pause/Cancel Buttons
        Hlayout_progress = QHBoxLayout()
        Hlayout_progress.addWidget(self.progress_Bar)  # Allow progress bar to stretch
        Hlayout_progress.addWidget(self.pause_button)
        Hlayout_progress.addWidget(self.cancel_button)
        layout.addLayout(Hlayout_progress)

       
        # Quality Selector + Checkbox
        Hlayout_quality = QHBoxLayout()
        Hlayout_quality.addWidget(self.quality_selector)
        Hlayout_quality.addWidget(self.download_button)
        layout.addLayout(Hlayout_quality)

        
        # Add a stretch to keep everything top-aligned
        layout.addStretch(1)
        self.animation()
        self.setLayout(layout)
        self.apply_Theme(ThemeManager.ThemeManager.get_current_theme())


        # Animation for moving the frame
        self.move_animation = QPropertyAnimation(self, b"pos")
        self.move_animation.setDuration(300)  # Animation duration in milliseconds
        self.move_animation.setEasingCurve(QEasingCurve.OutQuad)
  
  
  
  
    def animation(self):
        from config.config_manager import Config_Manager
        config = Config_Manager()
        if( config.get_loading_animation() == True):
            self.duration_loading_movie.start()
            self.max_Quality_Label_loading_movie.start()      
            self.thumbnail_loading_movie.start()       
            self.channel_name_loading_movie.start()
            self.title_label_loading_movie.start()
  

  
    def mousePressEvent(self, event):
        self.start_pos = event.pos()
        self.holding = False
        self.hold_timer.start(500)  # 1 second
        super().mousePressEvent(event)

    def on_hold_timeout(self):
        self.holding = True  # User held for 1 second

   
    def mouseMoveEvent(self, event):
        """Handle mouse move event."""
        if self.holding:
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
        QualityCheckingManager().search_list.discard(self.video_data.get('url','Unkhown'))  # Remove from search list
        self.deleteLater()  # Schedule deletion
        from Gui.Ui_Setup import Ui
        QTimer.singleShot(0, lambda: Ui().update_container_layout())  # Call layout update after event loop processes deletion


    def get_download_button(self):
        return self.download_button

    def start_download(self):
        """Handle download button click"""
      
        from Services.Downloading_Manager import Downloading_Manager
        quality = self.quality_selector.currentText().strip()
        Downloading_Manager().start_download(self,self.video_data, quality)


    def update_video_data(self,video_data):
        self.video_data = video_data


    def pause_downloading(self):
        """pause and resume video """

        if self.pause_flag is True:
           self.pause_button.setIcon(QIcon(self.pause_icon_path))
           self.pause_flag = False
        else:
            self.pause_flag = True
            self.pause_button.setIcon(QIcon(self.play_icon_path))


    def update_data(self,data:dict):
        print("in widget updating ")
        self.video_data = data

        self.update_quality_selector(data.get('qualities',''))
        self.update_channel_name(data.get('uploader', ''))
        self.update_title(data.get('title',''))
        self.update_duration(data.get('duration', '0'))
        self.update_max_quality(data.get('highest_quality'))
        self.update_thumbnail()

    def cancel_downloading(self):
        """Cancel video downloading"""
        self.cancel_flag = True

    def update_thumbnail(self, pixmap=None):
        """Update thumbnail with downloaded image"""

        if self.thumbnail_loading_movie.state() == QMovie.Running :
            # Stop the loading animation
            self.thumbnail_loading_movie.stop()
            self.thumbnail_label.setMovie(None)

        from FetchData.ThumbnailWorker import ThumbnailWorker
        worker = ThumbnailWorker(self.video_data)
        
        self.thread_pool = QThreadPool()
        worker.signals.finished.connect(self.set_thumbnail)
        self.thread_pool.start(worker)


    def set_thumbnail(self,pixmap):
            """Update thumbnail with downloaded image"""
            if pixmap is None:
                self.thumbnail_label.setText("Failed to load thumbnail")
            elif isinstance(pixmap, QLabel):
                self.thumbnail_label.setPixmap(pixmap.pixmap())
            elif isinstance(pixmap, QPixmap):
#                 self.thumbnail_label.setPixmap(
#     pixmap.scaled(275, 160, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
# )

                self.thumbnail_label.setPixmap(pixmap)
            else:
                self.thumbnail_label.setText("Invalid thumbnail format")


    def update_progress_bar(self, value):
        """Update progress bar """
        self.progress_Bar.setValue(value)


    def update_progress_label(self,value):
        """Update progress label """
        self.progress_label.setText(f"{value}%")


    def update_quality_selector(self, qualities):
        """Update quality selector with new qualities"""
        self.quality_selector.clear()
        self.quality_selector.addItems(self.download_selector)
        self.quality_selector.addItems(qualities)
        self.download_button.setEnabled(True)

    def update_title(self, title):
        """Update video title"""
        # Stop the loading animation
        if self.title_label_loading_movie.state() == QMovie.Running :
            self.title_label_loading_movie.stop()
            self.title_label.setMovie(None)

        # Set the title text
        if len(title) > 50: # Truncate title if too long
            title = title[:50] + "..."
        self.title_label.setText(title)
     
    def update_channel_name(self, channel_name):
        """Update channel name"""
        # Stop the loading animation
        
        if self.channel_name_loading_movie.state() == QMovie.Running :
            self.channel_name_loading_movie.stop()
            self.channel_name.setMovie(None)

        # Set the channel name text
        if len(channel_name) > 25: # Truncate channel name if too long
            channel_name = channel_name[:25] + "..."
        # Set the channel name text
        self.channel_name.setText(channel_name)

    def update_duration(self, duration_seconds):
        """Update video duration"""
        # Stop the loading animation
        if self.duration_loading_movie.state() == QMovie.Running :
            self.duration_loading_movie.stop()
            self.duration.setMovie(None)
        # Convert seconds to HH:MM:SS format
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.duration_text = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.duration.setText(self.duration_text)

    def update_max_quality(self, quality):
        """Update max quality label"""
        # Stop the loading animation
        if self.max_Quality_Label_loading_movie.state() == QMovie.Running:
                        # Set the max quality label to a blank state
            self.max_Quality_Label_loading_movie.stop()
            self.max_Quality_Label.setMovie(None)            # Set the max quality label to a blank state

        # Set the max quality text
        self.max_Quality_Label.setText(f"{quality}p")

    def apply_Theme(self, theme):
        """Apply theme to the widget using the provided theme dictionary."""
        # Apply theme to the main widget
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

        # Apply theme to the thumbnail label
        self.thumbnail_label.setStyleSheet(f"""
            QLabel {{
                background-color: {theme['widget_bg']};
                border-radius: 10px;
            }}
        """)

        # Apply theme to the progress bar
        self.progress_Bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {theme['border']};
                border-radius: 4px;
                background-color: {theme['widget_bg']};
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {theme['accent']};
                border-radius: 3px;
            }}
        """)

        # Apply theme to the quality selector
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

        # Apply theme to the progress label
        self.progress_label.setStyleSheet(f"""
            QLabel {{
                color: {theme['text']};
                font-size: 10px;
                font-weight: bold;
            }}
        """)

        # Apply theme to the title label
        self.title_label.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: {theme['text']};
                font-size: 12px;
                font-weight: bold;
                border: None;
            }}
        """)

        # Apply theme to the channel name label
        self.channel_name.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: {theme['text']};
                font-size: 12px;
                font-weight: bold;
                border: None;
            }}
        """)

        # Apply theme to the duration label
        self.duration.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: {theme['text']};
                font-size: 12px;
                font-weight: bold;
                border: None;
            }}
        """)