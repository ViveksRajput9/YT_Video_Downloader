import os
from PySide6.QtCore import QRunnable, Signal
import requests
import time
from DownloadManager.WorkerSignals import WorkerSignals
from config.config_manager import Config_Manager
from Services.Services import Service
class TitleDownload(QRunnable): 
            
    Signals = WorkerSignals()
    def __init__(self,parent, fileName,title):
        super().__init__()
        self.fileName = fileName
        self.title = title
        self.parent = parent
    def run(self):

        try:
            title_path = os.path.join(Config_Manager().get_download_path(), f'{self.fileName}-title.txt')
            with open(title_path, 'w', encoding='utf-8') as f:
                f.write(self.title)  # Use the title from the video info
            self.Signals.finished.emit(True, "")
        except Exception as e:
            self.Signals.finished.emit(False, str(e))
