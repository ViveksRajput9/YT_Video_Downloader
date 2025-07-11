import yt_dlp as ydl
from PySide6.QtCore import QRunnable ,QThread,QTimer
from Services import Signals, Services
from config.config_manager import Config_Manager
from Database.SearchHistory import SearchHistory
from .size_formatter import SizeFormatter
from .video_metadata_fetcher import VideoMetadataFetcher
from .quality_parser import QualityParser
import re
import time
from Database.sqlDatabase import Database
class FetchData(QRunnable):
    def __init__(self, url):
        super().__init__()
        self.url = url
        
        self.video_id = self.extract_safe_video_id(url)

        self.signals = Signals.WorkerSignals()
        self.database = Database()
    def run(self):
        result = {
            'error': None, 'qualities': [], 'highest_quality': None, 'url': self.url,
            'thread': None, 'progress_bar': None, 'progress_label': None,
            'pause_flag': False, 'cancel_flag': False, 'current_downloading_status': False,
            'download_button': None, 'filename': None, 'selected_format': None
        }
        try:
            data = self.database.get_data_by_id(self.video_id)
            if data: 
                return self.one_signal(data) 
   
            else:
                if not Services.Service.is_internet_available():
                    self.signals.finished.emit({'error': 'No Internet Connection'})
                    return

                info_dict = VideoMetadataFetcher(self.url).fetch()
                formats = info_dict.get('formats', [])
                qualities, best_audio_quality, best_audio_size, audio_720_size, highest_quality = QualityParser.parse(formats)
    
                result={
                    'qualities': qualities,
                    'highest_quality': highest_quality,
                    'id':self.video_id,
                    'audio_720_size': audio_720_size,
                    'best_audio_quality': best_audio_quality,
                    'thumbnail': info_dict.get('thumbnail'),
                    'uploader': info_dict.get('uploader', ''),
                    'title': info_dict.get('title', ''),
                    'duration': info_dict.get('duration', '0'),
                    'description': info_dict.get('description', ''),
                    'view_count': info_dict.get('view_count', ''),
                    'like_count': info_dict.get('like_count', ''),
                    'channel': info_dict.get('channel', ''),
                    'channel_follower_count': info_dict.get('channel_follower_count', ''),
                    'url': info_dict.get('original_url',self.url),
                    'tags': info_dict.get('tags', []),
                    'channel_url': info_dict.get('channel_url', ''),
                    'upload_date': info_dict.get('upload_date', ''),
                    'filename': re.sub(r'[\\/*?:"<>|]', "_", info_dict.get('title', '')),
                    'wishlist':False
                }

                v=  self.database.add_item(result)
                self.send_signal(result)
                if Config_Manager().get_search_history():
                    try:
                        SearchHistory().set_url(self.url, result['title'])
                    except Exception as e:
                        print(str(e))

        except ydl.utils.DownloadError:
            self.signals.finished.emit({'error': 'Requested format is not available. Please check available formats.',
                                        'info_dict': None, 'qualities': [], 'highest_quality': None})
        except Exception as e:
            self.signals.finished.emit({'error': str(e), 'info_dict': None, 'qualities': [], 'highest_quality': None})
    def extract_safe_video_id(self,url):
        """Extract YouTube video ID and ensure it's safe for filenames"""
        match = re.search(r"(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})", url)
        if match:
            return match.group(1).replace("-", "_")  # Replace hyphens with underscores for extra safety
        return None
    
    def send_signal(self,result):
        # Emit signals
        self.signals.quality_selector.emit(result['qualities'])
        self.signals.channel_name.emit(result['uploader'])
        self.signals.title.emit(result['title'])
        self.signals.duration.emit(result['duration'])
        self.signals.max_quality.emit(result['highest_quality'])
        self.signals.video_data.emit(result)
        self.signals.thumbnail.emit(None)
        self.signals.finished.emit({'error': None})
    def one_signal(self,result):
        self.signals.update_Ui.emit(result)
        self.signals.finished.emit({'error': None})
