import time
import yt_dlp as ydl
from typing import Dict, Any, Optional, Union
import logging
from DownloadManager.WorkerSignals import WorkerSignals
from config.config_manager import Config_Manager
from pathlib import Path
from Services.Services import Service
from PySide6.QtCore import QRunnable
from Gui.toast_message import show_toast_notification
class VideoOrAudioDownload(QRunnable):
    """Handles downloading video/audio files with retry logic and UI updates."""

    _logger_initialized = False
    _logger = None

    @classmethod
    def _initialize_logger(cls):
        if not cls._logger_initialized:
            log_path = Path.home() / '.ytdownloader' / 'youtube_downloader.log'
            log_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
            logging.basicConfig(
                filename=log_path,
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filemode='a'
            )
            cls._logger = logging.getLogger(cls.__name__)
            cls._logger_initialized = True

    def __init__(self, widget_parent, ydl_opts: Dict[str, Any], video_data: Dict[str, Any]):
        super().__init__()
        self.widget_parent = widget_parent
        self.ydl_opts = ydl_opts.copy()  # Avoid mutating external dict
        self.signals = WorkerSignals()
        self.url = video_data.get('url')
        if self.url is None:
            self.url = video_data.get('id')
        self.video_data = video_data
        # Initialize flags if not present
        if not hasattr(self.widget_parent, 'cancel_flag'):
            self.widget_parent.cancel_flag = False
        if not hasattr(self.widget_parent, 'pause_flag'):
            self.widget_parent.pause_flag = False

        self.cancel_flag = False

        self._initialize_logger()
        self.logger = self._logger

    def run(self) -> None:
        """Main download process with UI updates and error handling."""
        if self.video_data.get('current_downloading_status', False):
            self.logger.warning("Download already in process.")
            return

        self.video_data['current_downloading_status'] = True
        self.signals.status.emit("Initializing download...")

        # Enable UI buttons safely
        if hasattr(self.widget_parent, 'get_pause_button'):
            pause_btn = self.widget_parent.get_pause_button()
            if pause_btn:
                pause_btn.setEnabled(True)
        if hasattr(self.widget_parent, 'get_cancel_button'):
            cancel_btn = self.widget_parent.get_cancel_button()
            if cancel_btn:
                cancel_btn.setEnabled(True)

        try:
            self.logger.info(f"Starting download for URL: {self.url}")
            if not self.url or not isinstance(self.url, str) or not self.url.strip():
                show_toast_notification("url not found in downloading url")
                raise ValueError("Invalid URL: URL is empty or not a string.")

            if not self.check_internet():
                # check_internet handles emitting status and completing the download if canceled
                show_toast_notification("Internet Not Connected")
                return

            # Add progress tracking hooks
            self.ydl_opts['progress_hooks'] = [self.progress_hook]

            # Start the download with retries
            success, status_msg = self.download_with_retry()
            self.complete_download(success, status_msg)

        except Exception as e:
            self.logger.error(f"Download failed with exception: {e}", exc_info=True)
            self.signals.finished.emit(False, f"Download error: {str(e)}")
            self.video_data['current_downloading_status'] = False

    def check_internet(self) -> bool:
        """Checks internet availability and retries if needed."""
        try:
            while not Service.is_internet_available():
                self.signals.status.emit("No internet connection. Retrying in 5 seconds...")
                if getattr(self.widget_parent, 'cancel_flag', False):
                    msg = "Download canceled due to no internet connection."
                    self.logger.info(msg)
                    self.complete_download(False, msg)
                    return False
                time.sleep(5)
            return True
        except Exception as e:
            self.logger.error(f"Internet check failed: {e}", exc_info=True)
            return False

    def download_with_retry(self) :
        """Manages download attempts with retry logic."""
        max_retries = Config_Manager().get_max_retries()
        retry_delay = 3  # seconds delay between retries

        for attempt in range(1, max_retries + 1):
            if getattr(self.widget_parent, 'cancel_flag', False):
                self.complete_download(False, "Download cancelled by user")
                return False, "Download cancelled by user"

            self.logger.info(f"Download attempt {attempt}/{max_retries}")
            self.signals.status.emit(f"Downloading... (Attempt {attempt} of {max_retries})")

            try:
                with ydl.YoutubeDL(self.ydl_opts) as ytdl:
                    ytdl.download([self.url])
                return True, None

            except ydl.utils.DownloadError as e:
                error_msg = str(e)
                if "Requested format is not available" in error_msg:
                    self.logger.error(f"Format unavailable error on attempt {attempt}: {error_msg}")
                    self.signals.status.emit("Error: Requested format is not available.")
                    return False, "Error: Format unavailable."
                self.logger.error(f"Download error on attempt {attempt}: {error_msg}", exc_info=True)

            except Exception as e:
                self.logger.error(f"Unexpected error on attempt {attempt}: {e}", exc_info=True)

            # Wait before retrying unless it was the last attempt
            if attempt < max_retries:
                self.signals.status.emit(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

        return False, "Download failed after multiple attempts."

    def complete_download(self, success: bool, status_msg: Optional[str] = None) -> None:
        """Handles post-download cleanup and UI updates."""
        self.video_data['current_downloading_status'] = False

        if status_msg is None:
            status_msg = "Download completed successfully" if success else "Download failed"

        self.signals.status.emit(status_msg)
        self.signals.finished.emit(success, status_msg)
        self.logger.info(status_msg)

    def progress_hook(self, d: Dict[str, Any]) -> None:
        """Handles progress updates and cancellation logic."""
        try:
            if getattr(self.widget_parent, 'cancel_flag', False):
                self.complete_download(False, "Download cancelled")
                self.logger.info("Cancelling download due to cancel_flag...")
                raise KeyboardInterrupt

            while getattr(self.widget_parent, 'pause_flag', False):
                if getattr(self.widget_parent, 'cancel_flag', False):
                    self.complete_download(False, "Download cancelled")
                    self.logger.info("Cancelling download due to cancel_flag during pause...")
                    raise KeyboardInterrupt
                time.sleep(0.1)

            status = d.get('status')
            if status == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0

                if total > 0:
                    progress = int((downloaded / total) * 100)
                    self.signals.progress.emit(progress)
                    self.signals.status.emit(f'Downloaded {downloaded / 1024 / 1024:.1f} MB / {total / 1024 / 1024:.1f} MB')

            elif status == 'finished':
                self.signals.progress.emit(100)
                self.signals.status.emit("Download finished, processing...")

        except KeyboardInterrupt:
            # Expected interruption on cancel
            pass
        except Exception as e:
            self.logger.error(f"Progress hook error: {e}", exc_info=True)

