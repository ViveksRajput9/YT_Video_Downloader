import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QFileDialog,
    QLabel, QHBoxLayout,
)
from PySide6.QtCore import (
    QEvent, QPropertyAnimation, Qt, QUrl, QTime, QTimer, QPoint,
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtGui import QKeySequence, QMouseEvent, QShortcut
from Services.ThemeManager import ThemeManager

from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
class CustomVideoWidget(QVideoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)  # enable mouse move events without press

    def mouseMoveEvent(self, event: QMouseEvent):
        # Inform parent widget about mouse move so overlay can show
        if self.parent():
            self.parent().show_overlay()
            self.parent().hide_timer.start()
            self.parent().cursor_hide_timer.start()
        super().mouseMoveEvent(event)


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAcceptDrops(True)
        self._is_muted = False
        self._is_fullscreen = False
        self._is_looping = False
        self.slider_is_pressed = False

        # Timers for hiding overlay and cursor
        self.hide_timer = QTimer(self)
        self.hide_timer.setInterval(3000)
        self.hide_timer.timeout.connect(self.fade_out_overlay)

        self.cursor_hide_timer = QTimer(self)
        self.cursor_hide_timer.setInterval(3000)
        self.cursor_hide_timer.setSingleShot(True)
        self.cursor_hide_timer.timeout.connect(self.hide_cursor_and_overlay)

        self.last_mouse_pos = QPoint(-1, -1)

        self._setup_ui()
        self._connect_signals()
        self._setup_shortcuts()
        self.setMouseTracking(True)

        # Animation for overlay fade in/out
        self.overlay_animation = QPropertyAnimation(self.overlay_widget, b"windowOpacity")
        self.overlay_animation.setDuration(300)
        self.overlay_animation.setStartValue(0)
        self.overlay_animation.setEndValue(1)
        self.overlay_animation.finished.connect(self._on_fade_finished)

        # Style for active buttons
        self.active_style = "background-color: #337ab7; color: white;"  # nice blue accent
        self.inactive_style = ""  # default style
 

    def _setup_ui(self):

        header_box = QHBoxLayout()
        self.name_label = QLabel("YouTube Video Downloader")
        self.name_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.minimize_button = QPushButton("—")
        self.minimize_button.clicked.connect(self.showNormal)
        self.fullscreen_button = QPushButton("⛶")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen_with_style)
        self.close_button = QPushButton("✕")
        self.close_button.clicked.connect(self.stop)
        header_box.addWidget(self.name_label)
        header_box.addStretch()
        header_box.addWidget(self.minimize_button)
        header_box.addWidget(self.fullscreen_button)
        header_box.addWidget(self.close_button)


        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)

        # Use CustomVideoWidget to handle mouse move properly
        self.video_widget = CustomVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        self.overlay_widget = QWidget(self)
        self.overlay_widget.setFixedHeight(28)
        self.overlay_widget.setStyleSheet("background: rgba(0, 0, 0, 80%);")
        self.overlay_widget.setVisible(False)
        self.overlay_widget.setWindowOpacity(0)
        self.overlay_widget.setMouseTracking(True)

        self.open_button = QPushButton("Open")
        self.play_button = QPushButton("Play")
        self.mute_button = QPushButton("Mute")
        self.fullscreen_button = QPushButton("Fullscreen")
        self.loop_button = QPushButton("Loop")
        self.position_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.audio_output.setVolume(0.5)

        self.time_label = QLabel("00:00 / 00:00")

        control_layout = QHBoxLayout(self.overlay_widget)
        control_layout.setContentsMargins(3, 3, 3, 3)
        control_layout.setAlignment(Qt.AlignBottom)
        # control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.mute_button)
        # control_layout.addWidget(self.fullscreen_button)
        control_layout.addWidget(self.loop_button)
        control_layout.addStretch()  # Stretch before slider
        control_layout.addWidget(self.time_label)
        control_layout.addWidget(self.position_slider)  # Slider expands
        control_layout.addStretch()  # Stretch after slider
        control_layout.addWidget(self.volume_slider)
        
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(header_box)

        main_layout.addWidget(self.video_widget)
        main_layout.addWidget(self.overlay_widget)

        self.overlay_widget.installEventFilter(self)
        self.video_widget.installEventFilter(self)
    def eventFilter(self, obj, event):
        if obj in (self.video_widget, self.overlay_widget):
            if event.type() in {QEvent.Enter, QEvent.MouseMove}:
                self.show_overlay()
                self.hide_timer.stop()
                self.cursor_hide_timer.stop()
            elif event.type() == QEvent.Leave:
                self.hide_timer.start(1000)
        return super().eventFilter(obj, event)

    def show_overlay(self):
        if not self.overlay_widget.isVisible() or self.overlay_widget.windowOpacity() < 1:
            self.overlay_widget.setVisible(True)
            self.overlay_widget.raise_()
            self.overlay_animation.setDirection(QPropertyAnimation.Forward)
            self.overlay_animation.start()
        self.showCursorAndRestartTimer()

    def fade_out_overlay(self):
        if self.overlay_widget.isVisible() and self.overlay_widget.windowOpacity() > 0:
            self.overlay_animation.setDirection(QPropertyAnimation.Backward)
            self.overlay_animation.start()

    def _on_fade_finished(self):
        if self.overlay_animation.direction() == QPropertyAnimation.Backward:
            self.overlay_widget.setVisible(False)

    def hide_cursor_and_overlay(self):
        self.fade_out_overlay()
        self.setCursor(Qt.BlankCursor)

    def showCursorAndRestartTimer(self):
        if self.cursor().shape() == Qt.BlankCursor:
            self.setCursor(Qt.ArrowCursor)
        self.cursor_hide_timer.start()

    def mouseMoveEvent(self, event: QMouseEvent):
        current_pos = event.pos()
        if current_pos != self.last_mouse_pos:
            self.last_mouse_pos = current_pos
            self.show_overlay()
            self.hide_timer.start()
            self.cursor_hide_timer.start()

    def _connect_signals(self):
        self.open_button.clicked.connect(self.open_file)
        self.play_button.clicked.connect(self.play_pause)
        self.mute_button.clicked.connect(self.mute_unmute_with_style)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen_with_style)
        self.loop_button.clicked.connect(self.toggle_loop_with_style)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.volume_slider.sliderMoved.connect(self.set_volume)
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)
        self.position_slider.sliderPressed.connect(lambda: setattr(self, 'slider_is_pressed', True))
        self.position_slider.sliderReleased.connect(lambda: setattr(self, 'slider_is_pressed', False))

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Space"), self, self.play_pause)
        QShortcut(QKeySequence("F"), self, self.toggle_fullscreen_with_style)
        QShortcut(QKeySequence("M"), self, self.mute_unmute_with_style)
        QShortcut(QKeySequence("L"), self, self.toggle_loop_with_style)
        QShortcut(QKeySequence(Qt.Key_Right), self, lambda: self.skip_video(10))
        QShortcut(QKeySequence(Qt.Key_Left), self, lambda: self.skip_video(-10))
        QShortcut(QKeySequence(Qt.Key_Up), self, lambda: self.change_volume(5))
        QShortcut(QKeySequence(Qt.Key_Down), self, lambda: self.change_volume(-5))

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open Video File")
        file_dialog.setNameFilters([
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv)",
            "All Files (*)"
        ])
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.load_video(file_path)

    def load_video(self, file_path):
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        self.setWindowTitle(f"Video Player - {os.path.basename(file_path)}")
        self.media_player.play()
        self.play_button.setText("Pause")
        self.show_overlay()

    def play_pause(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText("Play")
        else:
            self.media_player.play()
            self.play_button.setText("Pause")

    # Modified to update button style when mute toggled
    def mute_unmute_with_style(self):
        self._is_muted = not self._is_muted
        self.audio_output.setMuted(self._is_muted)
        self._update_button_style(self.mute_button, self._is_muted)

    # Modified to update button style when fullscreen toggled
    def toggle_fullscreen_with_style(self):
        self._is_fullscreen = not self._is_fullscreen
        if self._is_fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()
        self._update_button_style(self.fullscreen_button, self._is_fullscreen)

    # Modified to update button style when loop toggled
    def toggle_loop_with_style(self):
        self._is_looping = not self._is_looping
        self.media_player.setLoops(-1 if self._is_looping else 1)
        self._update_button_style(self.loop_button, self._is_looping)

    def _update_button_style(self, button: QPushButton, active: bool):
        if active:
            button.setStyleSheet(self.active_style)
        else:
            button.setStyleSheet(self.inactive_style)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def set_volume(self, volume):
        self.audio_output.setVolume(volume / 100)

    def skip_video(self, seconds):
        new_position = self.media_player.position() + (seconds * 1000)
        self.media_player.setPosition(new_position)

    def _on_position_changed(self, position):
        if not self.slider_is_pressed:
            self.position_slider.setValue(position)
        self._update_time_label(position, self.media_player.duration())

    def _on_duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
        self._update_time_label(self.media_player.position(), duration)

    def _update_time_label(self, position, duration):
        pos_time = QTime(0, 0).addMSecs(position)
        dur_time = QTime(0, 0).addMSecs(duration)
        self.time_label.setText(f"{pos_time.toString('hh:mm:ss')} / {dur_time.toString('hh:mm:ss')}")

    def mouseMoveEvent(self, event: QMouseEvent):
        current_pos = event.pos()
        if current_pos != self.last_mouse_pos:
            self.last_mouse_pos = current_pos
            self.show_overlay()
            self.hide_timer.start()
            self.cursor_hide_timer.start()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self._is_fullscreen:
            self.toggle_fullscreen_with_style()
        elif event.key() == Qt.Key_Right:
            self.skip_video(10)
        elif event.key() == Qt.Key_Left:
            self.skip_video(-10)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            local_path = urls[0].toLocalFile()
            self._load_video(local_path)

    def change_volume(self, step):
        current_volume = self.volume_slider.value()
        new_volume = max(0, min(100, current_volume + step))
        self.volume_slider.setValue(new_volume)
        self.audio_output.setVolume(new_volume / 100)
    def stop(self):
        self.close()
        self.deleteLater()
    def apply_styles(self):
        """Apply styles to the header components."""
        self.minimize_button.setStyleSheet(ThemeManager.get_button_style())
        self.fullscreen_button.setStyleSheet(ThemeManager.get_button_style())
        self.close_button.setStyleSheet(ThemeManager.get_button_style())
