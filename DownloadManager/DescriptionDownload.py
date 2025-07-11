import os
from PySide6.QtCore import QRunnable, Signal
import requests
import time
from DownloadManager.WorkerSignals import WorkerSignals
from config.config_manager import Config_Manager

class DescriptionDownload(QRunnable):
            Signals = WorkerSignals()
            def __init__(self,title, description):
                super().__init__()
                self.title = title
                self.description = description

            def run(self):

                try:
                    description_path = os.path.join(Config_Manager().get_download_path(), f'{self.title}-description.txt')
                    with open(description_path, 'w', encoding='utf-8') as f:
                        f.write(self.description)
                    self.Signals.finished.emit(True, "")
                except Exception as e:
                    self.Signals.finished.emit(False, str(e))

