import os
from PySide6.QtCore import QRunnable, Signal
import requests
import time
from DownloadManager.WorkerSignals import WorkerSignals
from config.config_manager import Config_Manager

class TagsDownload(QRunnable):
    Signals = WorkerSignals()
    def __init__(self,title, tags ):
        super().__init__()
        self.tags = tags
        self.title = title
        print(title)
        print(tags)

    
    def run(self):
        try:
            # Ensure download path exists
            download_path = Config_Manager().get_download_path()
            os.makedirs(download_path, exist_ok=True)  # Creates folder if it doesn't exist
    
            # Define file path for saving tags
            tags_path = os.path.join(download_path, f'{self.title}-tags.txt')
    
            # Write tags to the file
            with open(tags_path, 'w', encoding='utf-8') as f:
                if self.tags:
                    f.write(', '.join(self.tags))
                else:
                    f.write("No tags available")
    
            # Emit success signal
            self.Signals.finished.emit(True, f"Tags saved successfully:")
    
        except Exception as e:
            # Log error and emit failure signal
            # self.logger.error(f"Error saving tags: {str(e)}", exc_info=True)
            self.Signals.finished.emit(False, f"Failed to save tags: {str(e)}")