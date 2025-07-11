import os
from PySide6.QtCore import QRunnable, Signal
import requests
import re
from PIL import Image
from io import BytesIO
from DownloadManager.WorkerSignals import WorkerSignals
from config.config_manager import Config_Manager
from Database.Database import Database
from pathlib import Path
class ThumbnailDownload(QRunnable):
    Signals = WorkerSignals()

    def __init__(self, thumbnail_url, title,id):
        super().__init__()
        self.thumbnail_url = thumbnail_url
        self.title = title
        self.id = id
        self.file_path = Path.home() / '.ytdownloader' / 'thumbnails'
        self.img_path = os.path.join(self.file_path, f"{self.extract_safe_video_id(id)}.png") # Define full save path

    def run(self):
        try:
            output_path = os.path.join(Config_Manager().get_download_path(), f"{self.title}.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            if os.path.exists(self.img_path):
                img = Image.open(self.img_path)
                img.save(output_path)
            else:
                response = requests.get(self.thumbnail_url)
                img_data = Image.open(BytesIO(response.content))
                img_data.save(output_path)
            self.Signals.finished.emit(True, "")
        except Exception as e:
            self.Signals.finished.emit(False, str(e))
    def extract_safe_video_id(self,url):
        """Extract YouTube video ID and ensure it's safe for filenames"""
        match = re.search(r"(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})", url)
        if match:
            return match.group(1).replace("-", "_")  # Replace hyphens with underscores for extra safety
        return None