import os
import shutil
import subprocess
from pathlib import Path
from PySide6.QtWidgets import QMessageBox, QFileDialog, QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class FFmpegHandler(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setModal(True)
        self.setWindowTitle("FFmpeg Required")
        self.setFixedSize(400, 200)
        self.layout = QVBoxLayout(self)

        self.message_label = QLabel(
            "FFmpeg is required to use this application.\n"
            "Please locate or install FFmpeg to proceed."
        )
        self.message_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.message_label)

        self.locate_button = QPushButton("Locate FFmpeg")
        self.locate_button.clicked.connect(self._request_ffmpeg_location)
        self.layout.addWidget(self.locate_button)

        self.exit_button = QPushButton("Exit Application")
        self.exit_button.clicked.connect(self._exit_application)
        self.layout.addWidget(self.exit_button)

        # Define the FFmpeg storage path
        self.ffmpeg_storage_path = Path.home() / '.ytdownloader' / 'ffmpeg.exe'

    def check_ffmpeg(self):
        """Check if FFmpeg is available for the Windows platform."""
        # Check if ffmpeg is in system PATH
        if self._is_ffmpeg_in_path():
            return True

        # Check the custom storage path
        if self.ffmpeg_storage_path.exists():
            os.environ["PATH"] += os.pathsep + str(self.ffmpeg_storage_path.parent)
            return self._is_ffmpeg_in_path()  # Verify if FFmpeg works after adding the custom path

        self.exec()  # Show the modal dialog if FFmpeg is not found
        return False

    def _is_ffmpeg_in_path(self):
        """Check if ffmpeg is available in system PATH."""
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _request_ffmpeg_location(self):
        """Ask user to locate ffmpeg.exe."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select ffmpeg.exe",
            "",
            "Executable files (*.exe)"
        )

        if file_path and os.path.exists(file_path):
            if self._verify_ffmpeg(file_path):
                self._setup_ffmpeg(file_path)
                self.accept()  # Close the dialog if FFmpeg is successfully located
            else:
                QMessageBox.critical(self, "Error", "Selected file is not a valid FFmpeg executable.")
        else:
            QMessageBox.warning(self, "FFmpeg Required", "Please locate a valid FFmpeg executable to proceed.")

    def _verify_ffmpeg(self, file_path):
        """Verify if the selected file is actually ffmpeg."""
        try:
            result = subprocess.run(
                [file_path, '-version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return b'ffmpeg version' in result.stdout.lower()
        except Exception:
            return False

    def _setup_ffmpeg(self, source_path):
        """Copy ffmpeg to the custom storage path and add to PATH."""
        try:
            # Ensure the directory exists
            self.ffmpeg_storage_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy ffmpeg to the custom storage path
            shutil.copy2(source_path, self.ffmpeg_storage_path)

            # Add the directory to PATH
            os.environ["PATH"] += os.pathsep + str(self.ffmpeg_storage_path.parent)

            # Verify if FFmpeg works after setup
            if not self._is_ffmpeg_in_path():
                raise Exception("FFmpeg setup failed. The executable is not working.")
            QMessageBox.information(self,"success","Congratulation ffmepg successfully setup")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup FFmpeg: {str(e)}")

    def _exit_application(self):
        """Exit the application if FFmpeg is not found or located."""
        self.reject()  # Close the dialog
        QMessageBox.critical(None, "Application Exit", "FFmpeg is required to run this application. Exiting now.")
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()  # Ensure the application exits properly

