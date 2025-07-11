from PySide6.QtCore import QObject, QThreadPool, Signal, Slot, QTimer
from Services.Services import Service
from pathlib import Path
from Models.Widget import SquareWidget
from Database.Database import Database
from config.config_manager import Config_Manager
from FetchData.YTVideoDataFetcher import FetchData
from FetchData.video_metadata_fetcher import VideoMetadataFetcher
from Gui import toast_message
import threading
import logging
from PySide6.QtCore import QRunnable, QMetaObject, Qt, Q_ARG,QSemaphore

from pytube import YouTube, Playlist
import logging
from PySide6.QtCore import QObject, QRunnable, Signal
from pytube import YouTube, Playlist
import logging
import re
import time
from typing import Set
from PySide6.QtCore import QThread, Signal
from FetchData.load_balancer import load_balancer
class PlaylistProcessor(QThread):
    progress = Signal(str)  # Signal to update UI with processed video URLs

    def __init__(self, url_list):
        super().__init__()
        self.url_list = url_list

    def run(self):
        count = 0
        length= len(self.url_list)
        for video_url in self.url_list:
            print(video_url)
            if(length>=10):
                count += 1

                if(count>10):
                    time.sleep(2.5)
                    count = 0
                
            if not QualityCheckingManager().is_url_exits(video_url):
                time.sleep(0.5)
                self.progress.emit(video_url)  # Emit progress update


class QualityCheckingManager(QObject):  # Inherit from QObject
    show_message = Signal(str, str, str)  # Define the signal (type, title, message)

    _instance = None
    _lock = threading.Lock()
    search_list = []

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        super().__init__()  # Initialize QObject
        self._initialized = True
        self.cache = {}
        self.current_column = 0
        self.current_row = 0

        # Setup logging
        logging.basicConfig(
            filename=Path.home() / '.ytdownloader' / 'youtube_downloader.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.temp_widget = []
        # Thread pool for quality checking   
        max_threads = Config_Manager().get_total_thread()
        self.quality_thread_pool = QThreadPool.globalInstance()  # 🔐 Controls concurrent threads

    def is_url_exits(self, url):
        print(self.search_list)
        if url in self.search_list:
            toast_message.show_toast_notification("Already has in list")
            return True
        else:
            self.search_list.append(url)
            return False
    def delete_url(self,url):
        self.search_list.remove(url)
    def check_qualities(self, url):

        if not url:
            toast_message.show_toast_notification("Please enter a valid YouTube URL")
            return

        toast_message.show_toast_notification("Searching...")
        try:
            QThreadPool.globalInstance().start(
                self._process_url(url)
            )
        except Exception as e:
            logging.error(f"Error checking qualities: {str(e)}")
            toast_message.show_toast_notification(f"Failed to check qualities: {str(e)}")

    def _process_url(self, url):
        try:
            print(url)
            if 'playlist' in url or 'list=' in url:
                playlist = Playlist(url)
                self.process_urls(playlist.video_urls)
                
            elif YouTube(url) or self.isVideoUrl(url):
                if not self.is_url_exits(url):
                    QThreadPool.globalInstance().start(self.create_widget_task(url))
                else:
                    logging.warning(f"URL {url} already exists in the search list.")
    
        except Exception as e:
            # urls = VideoMetadataFetcher.fetch_url_using_keyword(url,10)
            # self.process_urls(urls)
            toast_message.show_toast_notification("Invalid url")

    def process_urls(self,urls):
        processor = PlaylistProcessor(urls)
        processor.setParent(self)  # Ensures the thread is properly managed
        processor.progress.connect(self.create_widget_task)
        processor.start()

    def isVideoUrl(self,url):
        """Extract YouTube video ID and ensure it's safe for filenames"""
        match = re.search(r"(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})", url)
        if match:
            return True  # Replace hyphens with underscores for extra safety
        return False
    
    def create_widget_task(self, video_url):
        print('creating')
        widget = SquareWidget(self)
        QTimer.singleShot(0, lambda: self.update_container_layout(video_url, widget))  # Delay 100ms
        logging.info(f"Adding task for video_url: {video_url}")
        # self.__loadBalancing.add_task(video_url, widget)
        self.start_quality_check(video_url,widget)

    # Add widget incrementally
    def start_quality_check(self, url, widget:SquareWidget):
        logging.info(f"start_quality_check called for url: {url}")
        try:
            print("FETCHING")
            quality_thread = FetchData(url)
            quality_thread.signals.finished.connect(lambda result: self._handle_quality_check_finished(widget, result))
            quality_thread.signals.update_Ui.connect(widget.update_data)
            quality_thread.signals.quality_selector.connect(widget.update_quality_selector)
            quality_thread.signals.channel_name.connect(widget.update_channel_name)
            quality_thread.signals.title.connect(widget.update_title)
            quality_thread.signals.duration.connect(widget.update_duration)
            quality_thread.signals.max_quality.connect(widget.update_max_quality)
            quality_thread.signals.video_data.connect(widget.update_video_data)
            quality_thread.signals.thumbnail.connect(widget.update_thumbnail)
            self.quality_thread_pool.start(quality_thread)

        except Exception as e:
            logging.error(f"Error starting quality check for URL '{url}': {str(e)}")
            toast_message.show_toast_notification(f"Failed to start quality check: {str(e)}")

    def _handle_quality_check_finished(self, widget, result):
        if result .get('error'):
            if not Service.is_internet_available():
                toast_message.show_toast_notification("Internet Not Available")
            else:

                logging.warning(f"Critical Error: Failed to fetch video qualities:\n{result['error']}")
            widget.delete_widget()
        else:
            widget.enable_download_button()
            # Handle successful quality check results
            logging.info(f"Quality check finished successfully for widget: {widget}")
        
    def update_container_layout(self, video_url, widget):
        from Gui.Ui_Setup import Ui
        try:
            Ui().get_content_area().add_widget(widget)  # Place below the button
        except Exception as e:
            logging.error(f"Error updating container layout for video URL '{video_url}': {str(e)}")
            toast_message.show_toast_notification(f"Failed to update layout: {str(e)}")