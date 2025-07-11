import time
import yt_dlp as ydl
from typing import Dict, Any
import logging
from DownloadManager.WorkerSignals import WorkerSignals
from config.config_manager import Config_Manager
from pathlib import Path
from Gui.toast_message import show_toast_notification
from Services.Services import Service
from PySide6.QtCore import QRunnable, QThreadPool

class VideoOrAudioDownload(QRunnable):
    """Handles downloading video/audio files with retry logic and UI updates."""
    
    def __init__(self, widget_parent, ydl_opts, video_data):
        super().__init__()
        self.widget_parent = widget_parent
        self.ydl_opts = ydl_opts
        self.signals = WorkerSignals()
        self.url = video_data.get('url')
        self.video_data = video_data
        self.cancel_flag = False

        # Ensure flags exist
        self.widget_parent.cancel_flag = False
        self.widget_parent.pause_flag = False

        # Setup logging
        log_path = Path.home() / '.ytdownloader' / 'youtube_downloader.log'
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Main download process with UI updates and error handling."""
        if self.video_data.get('current_downloading_status'):
            self.logger.warning("Download is already in process.")
            return

        self.video_data['current_downloading_status'] = True
        self.signals.status.emit("Initializing download...")

        # Enable UI buttons safely
        if hasattr(self.widget_parent, 'get_pause_button()'):
            self.widget_parent.get_pause_button().setEnabled(True)
        if hasattr(self.widget_parent, 'get_cancel_button()'):
            self.widget_parent.get_cancel_button().setEnabled(True)

        try:
            self.logger.info(f"Starting download for URL: {self.url}")
            if not self.url:
                raise ValueError("Invalid URL: URL is empty.")

            # Ensure internet connectivity
            if not self.check_internet():
                
                return

            # Add progress tracking hooks
            self.ydl_opts['progress_hooks'] = [self.progress_hook]

            # Start the download with retries
            success = self.download_with_retry()
            self.complete_download(success)

        except Exception as e:
            self.logger.error(f"Download failed: {e}", exc_info=True)
            self.signals.finished.emit(False, f"Download error: {str(e)}")

    def check_internet(self):
        """Checks internet availability and retries if needed."""
        try:
            while not Service.is_internet_available():
                self.signals.status.emit("No internet. Retrying...")
                if self.widget_parent.cancel_flag:
                    msg = "Download canceled due to no internet."
                    self.logger.info(msg)
                    self.complete_download(False,msg)
                    return False
                time.sleep(5)
        
            return True
        except Exception as e:
            self.logger.error(f"Internet check failed: {e}")
            return False

    def download_with_retry(self) -> bool:
        """Manages download attempts with retry logic."""
        max_retries = Config_Manager().get_max_retries()

        for attempt in range(1, max_retries + 1):
            try:
                if self.widget_parent.cancel_flag:
                    self.complete_download(False)
                    return False

                self.logger.info(f"Download attempt {attempt}/{max_retries}")
                self.signals.status.emit("Downloading...")

                with ydl.YoutubeDL(self.ydl_opts) as ytdl:
                    ytdl.download([self.url])

                return True

            except (ydl.utils.DownloadError, Exception) as e:
                if "Requested format is not available" in str(e):
                    self.signals.status.emit("Error: Format unavailable.")
                    return "Error: Format unavailable."
                self.logger.error(f"Attempt {attempt} failed: {e}")
                
        return False

    def complete_download(self, success ,status_msg=None):
        """Handles post-download cleanup and UI updates."""
        self.video_data['current_downloading_status'] = False
        if not status_msg:
          status_msg = "Download completed successfully" if success else "Download failed"
        if success =="Error: Format unavailable.":
            status_msg = "Error: Format unavailable."
        self.signals.status.emit(status_msg)
        self.signals.finished.emit(success, status_msg)
        self.logger.info(status_msg)

    def progress_hook(self, d: Dict[str, Any]):
        """Handles progress updates and cancellation logic."""
        try:
            if self.widget_parent.cancel_flag:
                self.complete_download(False,"Download cancelled")
                self.logger.info("Cancelling download...")
                raise KeyboardInterrupt
                
            while self.widget_parent.pause_flag:
                if self.widget_parent.cancel_flag:
                    self.complete_download(False,"Download cancelled")
                    self.logger.info("Cancelling download...")
                    raise KeyboardInterrupt
                time.sleep(0.1)

            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

                if total:
                    progress = int((downloaded / total) * 100)
                    self.signals.progress.emit(progress)
                    self.signals.status.emit(f'Downloaded {downloaded/1024/1024:.1f}MB / {total/1024/1024:.1f}MB')

            elif d['status'] == 'finished':
                self.signals.progress.emit(100)
                self.signals.status.emit("Processing...")
        except Exception as e:
            self.logger.error(f"Progress hook error: {e}")