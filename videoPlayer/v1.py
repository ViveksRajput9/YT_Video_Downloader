import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QFileDialog,
    QLabel, QHBoxLayout, QMessageBox, QMenu
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl, QTime, QTimer, QPoint
from PySide6.QtGui import QPixmap, QKeySequence, QMouseEvent, QDragEnterEvent, QDropEvent, QShortcut, QCursor
import threading
class VideoPlayer(QWidget):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,parent=None):
        if hasattr(self, "_initialized") and self._initialized:
            return  # Prevent reinitialization
        super().__init__(parent)
        self._initialized = True
        self.setWindowTitle("Enhanced PySide6 Video Player")
        self.setMinimumSize(600, 400)
        self.setAcceptDrops(True)
        self._is_muted = False
        self._is_fullscreen = False
        self._is_looping = False
        self._recent_files = []
        self._setup_ui()
        self._connect_signals()
        self._set_initial_values()
        self._setup_shortcuts()

    def _setup_ui(self):
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        self.open_button = QPushButton("Open Video")
        self.recent_button = QPushButton("Recent")
        self.play_button = QPushButton("Play")
        self.mute_button = QPushButton("Mute")
        self.fullscreen_button = QPushButton("Fullscreen")
        self.capture_frame_button = QPushButton("Capture Frame")
        self.loop_button = QPushButton("Loop")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.position_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.time_label = QLabel("00:00 / 00:00")
        self.volume_label = QLabel("Volume")
        self.speed_label = QLabel("1.0x")

        for btn in [self.play_button, self.mute_button, self.fullscreen_button,
                    self.capture_frame_button, self.loop_button]:
            btn.setEnabled(False)

        self.mute_button.setCheckable(True)
        self.fullscreen_button.setCheckable(True)
        self.loop_button.setCheckable(True)
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        self.position_slider.setRange(0, 0)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.recent_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.mute_button)
        control_layout.addWidget(self.fullscreen_button)
        control_layout.addWidget(self.loop_button)
        control_layout.addWidget(self.capture_frame_button)
        control_layout.addWidget(QLabel("Speed"))
        control_layout.addWidget(self.speed_slider)
        control_layout.addWidget(self.speed_label)
        control_layout.addWidget(self.position_slider)
        control_layout.addWidget(self.time_label)
        control_layout.addWidget(self.volume_label)
        control_layout.addWidget(self.volume_slider)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.video_widget)
        main_layout.addLayout(control_layout)

    def _connect_signals(self):
        self.open_button.clicked.connect(self.open_file)
        self.recent_button.clicked.connect(self.show_recent_files_menu)
        self.play_button.clicked.connect(self.play_pause)
        self.mute_button.clicked.connect(self.mute_unmute)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.loop_button.clicked.connect(self.toggle_loop)
        self.capture_frame_button.clicked.connect(self.capture_frame)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.volume_slider.sliderMoved.connect(self.set_volume)
        self.speed_slider.sliderMoved.connect(self.set_speed)
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)
        self.media_player.playbackStateChanged.connect(self._update_play_button)
        self.media_player.errorOccurred.connect(self._handle_error)


    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Space"), self, self.play_pause)
        QShortcut(QKeySequence("F"), self, self.toggle_fullscreen)
        QShortcut(QKeySequence("M"), self, self.mute_unmute)
        QShortcut(QKeySequence("L"), self, self.toggle_loop)
        QShortcut(QKeySequence(Qt.Key_Right), self, lambda: self.skip_video(10))
        QShortcut(QKeySequence(Qt.Key_Left), self, lambda: self.skip_video(-10))

    def _set_initial_values(self):
        self.audio_output.setVolume(self.volume_slider.value() / 100)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open Video File")
        file_dialog.setNameFilters(["Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv)", "All Files (*)"])
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            print(file_path)
            self.load_video(file_path)

    def load_video(self, file_path):
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        self._enable_controls()
        self._reset_ui()
        if file_path not in self._recent_files:
            self._recent_files.insert(0, file_path)
            if len(self._recent_files) > 5:
                self._recent_files.pop()

    def show_recent_files_menu(self):
        menu = QMenu(self)
        for path in self._recent_files:
            action = menu.addAction(os.path.basename(path))
            action.triggered.connect(lambda checked=False, p=path: self._load_video(p))
        menu.exec(QCursor.pos())

    def _enable_controls(self):
        for btn in [self.play_button, self.mute_button, self.fullscreen_button,
                    self.capture_frame_button, self.loop_button]:
            btn.setEnabled(True)

    def _reset_ui(self):
        self.play_button.setText("Play")
        self.position_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")

    def play_pause(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def mute_unmute(self):
        self._is_muted = self.mute_button.isChecked()
        self.audio_output.setMuted(self._is_muted)
        self.mute_button.setText("Unmute" if self._is_muted else "Mute")

    def toggle_fullscreen(self):
        self._is_fullscreen = self.fullscreen_button.isChecked()
        if self._is_fullscreen:
            self.showFullScreen()
            self.fullscreen_button.setText("Exit Fullscreen")
        else:
            self.showNormal()
            self.fullscreen_button.setText("Fullscreen")

    def toggle_loop(self):
        self._is_looping = self.loop_button.isChecked()
        self.media_player.setLoops(-1 if self._is_looping else 1)

    def capture_frame(self):
        pixmap = self.video_widget.grab()
        pixmap.save("captured_frame.png", "PNG")
        QMessageBox.information(self, "Frame Captured", "Saved as captured_frame.png")

    def set_position(self, position):
        self.media_player.setPosition(position)

    def set_volume(self, volume):
        self.audio_output.setVolume(volume / 100)

    def set_speed(self, speed_value):
        rate = speed_value / 100
        self.media_player.setPlaybackRate(rate)
        self.speed_label.setText(f"{rate:.1f}x")

    def _on_position_changed(self, position):
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(position)
        self.position_slider.blockSignals(False)
        self._update_time_label(position, self.media_player.duration())

    def _on_duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
        self._update_time_label(self.media_player.position(), duration)

    def _update_time_label(self, position, duration):
        pos_time = QTime(0, 0).addMSecs(position)
        dur_time = QTime(0, 0).addMSecs(duration)
        self.time_label.setText(f"{pos_time.toString('hh:mm:ss')} / {dur_time.toString('hh:mm:ss')}")

    def _update_play_button(self, state):
        self.play_button.setText("Pause" if state == QMediaPlayer.PlayingState else "Play")

    def _handle_error(self, error, error_string):
        if error != QMediaPlayer.NoError:
            QMessageBox.critical(self, "Media Player Error", error_string)

    # Drag and Drop Support
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self._load_video(file_path)

    # Double-click fullscreen toggle
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        self.fullscreen_button.toggle()
        self.toggle_fullscreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
