import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                               QSlider, QFileDialog, QLabel, QHBoxLayout, QMessageBox, QComboBox)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QVideoSink, QVideoFrame
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl, QTime
from PySide6.QtGui import QPalette, QColor, QPixmap


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate Video Player")
        self.setMinimumSize(900, 500)
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        # UI Elements
        self.open_button = QPushButton("Open Video")
        self.play_button = QPushButton("Play")
        self.mute_button = QPushButton("Mute")
        self.fullscreen_button = QPushButton("Fullscreen")
        self.subtitle_button = QPushButton("Load Subtitle")
        self.capture_button = QPushButton("Capture GIF")
        self.stream_button = QPushButton("Stream Video")
        self.audio_track_dropdown = QComboBox()

        self.position_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)

        self.time_label = QLabel("00:00 / 00:00")
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(160, 90)
        self.thumbnail_label.setVisible(False)

        # Layouts
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.mute_button)
        control_layout.addWidget(self.fullscreen_button)
        control_layout.addWidget(self.subtitle_button)
        control_layout.addWidget(self.capture_button)
        control_layout.addWidget(self.stream_button)
        control_layout.addWidget(self.audio_track_dropdown)
        control_layout.addWidget(self.position_slider)
        control_layout.addWidget(self.time_label)
        control_layout.addWidget(self.volume_slider)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.video_widget)
        main_layout.addWidget(self.thumbnail_label)
        main_layout.addLayout(control_layout)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        # Dark Mode UI
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # Thumbnail Preview
        self.video_sink = QVideoSink()
        self.video_widget.videoSink()
        self.video_sink.videoFrameChanged.connect(self._update_thumbnail)

    def _connect_signals(self):
        self.open_button.clicked.connect(self.open_file)
        self.play_button.clicked.connect(self.play_pause)
        self.mute_button.clicked.connect(self.toggle_mute)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.subtitle_button.clicked.connect(self.load_subtitle)
        self.capture_button.clicked.connect(self.capture_gif)
        self.stream_button.clicked.connect(self.stream_video)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.volume_slider.sliderMoved.connect(self.set_volume)
        self.audio_track_dropdown.currentIndexChanged.connect(self.change_audio_track)

        self.media_player.positionChanged.connect(self._update_position)
        self.media_player.durationChanged.connect(self._update_duration)
        self.media_player.playbackStateChanged.connect(self._update_play_button)
        self.media_player.errorOccurred.connect(self._handle_error)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open Video File")
        file_dialog.setNameFilters(["Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv)", "All Files (*)"])
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.populate_audio_tracks()
            self.play_button.setEnabled(True)
            self.position_slider.setRange(0, 0)

    def play_pause(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def toggle_mute(self):
        self.audio_output.setMuted(not self.audio_output.isMuted())

    def toggle_fullscreen(self):
        if self.fullscreen_button.text() == "Fullscreen":
            self.showFullScreen()
            self.fullscreen_button.setText("Exit Fullscreen")
        else:
            self.showNormal()
            self.fullscreen_button.setText("Fullscreen")

    def set_position(self, position):
        self.media_player.setPosition(position)

    def set_volume(self, volume):
        self.audio_output.setVolume(volume / 100)

    def _update_position(self, position):
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(position)
        self.position_slider.blockSignals(False)
        self._update_time_label(position, self.media_player.duration())

    def _update_duration(self, duration):
        self.position_slider.setRange(0, duration)

    def _update_time_label(self, position, duration):
        position_time = QTime(0, 0).addMSecs(position)
        duration_time = QTime(0, 0).addMSecs(duration)
        self.time_label.setText(f"{position_time.toString('hh:mm:ss')} / {duration_time.toString('hh:mm:ss')}")

    def _update_play_button(self, state):
        self.play_button.setText("Pause" if state == QMediaPlayer.PlayingState else "Play")

    def _handle_error(self, error, error_string):
        QMessageBox.critical(self, "Error", error_string)

    def _update_thumbnail(self, frame: QVideoFrame):
        if frame.isValid():
            pixmap = QPixmap.fromImage(frame.toImage())
            self.thumbnail_label.setPixmap(pixmap)
            self.thumbnail_label.setVisible(True)

    def load_subtitle(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open Subtitle File")
        file_dialog.setNameFilters(["Subtitle Files (*.srt *.vtt)", "All Files (*)"])
        if file_dialog.exec() == QFileDialog.Accepted:
            subtitle_file = file_dialog.selectedFiles()[0]
            self.media_player.setSubtitleSource(QUrl.fromLocalFile(subtitle_file))

    def populate_audio_tracks(self):
        self.audio_track_dropdown.clear()
        for index in range(self.media_player.audioTracks()):
            self.audio_track_dropdown.addItem(f"Track {index + 1}", index)

    def change_audio_track(self, index):
        self.media_player.setActiveAudioTrack(index)

    def stream_video(self):
        url, _ = QFileDialog.getOpenFileUrl(self, "Enter Video URL")
        if url:
            self.media_player.setSource(url)

    def capture_gif(self):
        pixmap = self.video_widget.grab()
        pixmap.save("captured_gif.gif", "GIF")
        QMessageBox.information(self, "GIF Captured", "Saved as captured_gif.gif")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())