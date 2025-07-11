import os
from DownloadManager import DescriptionDownload, TitleDownload, ThumbnailDownload, TagsDownload,VideoOrAudioDownload,v
from PySide6.QtCore import  QThreadPool, QObject, Signal
import subprocess
from Services import CheckDuplicate, Services
from config.config_manager import Config_Manager
from Gui import toast_message
from Database.sqlDatabase import Database
from Models.Widget import SquareWidget
class Downloading_Manager(QObject):
    _instance = None  # Class-level variable to hold the singleton instance
    show_message = Signal(str, str, str)  # type, title, message

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Downloading_Manager, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        # Avoid reinitialization in case __init__ is called again
        if hasattr(self, '_initialized') and self._initialized:
            return

        super().__init__()
        self.parent = parent
        self.thread_pool = QThreadPool()
        self.config = Config_Manager()
        self.thread_pool.setMaxThreadCount(self.config.get_max_concurrent_downloads())
        self.status = True  # Initialize status

        self._initialized = True  # Mark as initialized

    def download_description(self, filename, description):
        if not description:
            self.show_message.emit("critical", "Error", "No description available.")
            return

        description_thread = DescriptionDownload.DescriptionDownload(filename, description)
        description_thread.Signals.finished.connect(self.on_description_download_finished)
        self.thread_pool.start(description_thread)

    def on_description_download_finished(self, success, message):
        if success:
            toast_message.show_toast_notification(" Description downloaded successfully!")
        else:
            toast_message.show_toast_notification(" Description download failed!")

    def download_title(self, filename, title):
        if not title:
            self.show_message.emit("critical", "Error", "No title available.")
            return

        title_thread = TitleDownload.TitleDownload(self, filename, title)
        title_thread.Signals.finished.connect(self.on_title_download_finished)
        self.thread_pool.start(title_thread)

    def on_title_download_finished(self, success, message):
        if success:
            toast_message.show_toast_notification(" Title downloaded successfully!")
        else:
            toast_message.show_toast_notification(" Title download failed!")

    def download_thumbnail(self, filename, thumbnail_url,video_id):
        if not thumbnail_url:
            self.show_message.emit("critical", "Error", "No thumbnail URL found.")
            return

        thumbnail_thread = ThumbnailDownload.ThumbnailDownload(thumbnail_url, filename,video_id)
        thumbnail_thread.Signals.finished.connect(self.on_thumbnail_download_finished)
        self.thread_pool.start(thumbnail_thread)

    def on_thumbnail_download_finished(self, success, message):
        if success:
            toast_message.show_toast_notification(" Thumbnail downloaded successfully!")
        else:
            toast_message.show_toast_notification(" Thumbnail download failed!")

    def download_tags(self, filename, tags):
        if not tags:
            self.show_message.emit("critical", "Error", "No tags available.")
            return
        tags_thread = TagsDownload.TagsDownload(filename, tags)
        tags_thread.Signals.finished.connect(self.on_tags_download_finished)
        self.thread_pool.start(tags_thread)

    def on_tags_download_finished(self, success, message):
        if success:
            toast_message.show_toast_notification(message)
        else:
            print(message)
            toast_message.show_toast_notification(message)
 
    def start_download(self,widget_parent, video_data:dict, quality):
        self.status = True
        print('start')
        if not Services.Service.is_internet_available():
            toast_message.show_toast_notification("Internet not connected")
            return
        if not self.config.get_download_path():
            self.show_message.emit("critical", "Error", "Please select an output folder.")
            return
        
        if  quality == 'Select Quality':
            toast_message.show_toast_notification("Select Quality")
            return
        if 'Title' in quality:
            self.download_title(video_data.get('filename',''), video_data.get('title',''))

        elif 'Description' in quality:

            self.download_description(video_data.get('filename',''), video_data.get('description',''))

        elif 'Thumbnail' in quality:

            self.download_thumbnail(video_data.get('filename', ''), video_data.get('thumbnail',''),video_data.get('id',''))

        elif 'Tags' in quality:

            self.download_tags(video_data.get('filename', ''), video_data.get('tags',''))
           
        else: 
            self.handle_video_download(widget_parent,video_data, quality)

    def setup_audio_download_options(self, quality, filename):
        abr = ''.join(filter(str.isdigit, quality.split('-')[1]))
        # self.ydl_opts = {
        #     'format': f'bestaudio[abr<={abr}]',
        #     'outtmpl': os.path.join(self.config.get_download_path(), f'{filename}.%(ext)s'),
        #     'force_generic_extractor': True,
        #     'geo_bypass': True,
        #     'noplaylist': True
        # }
        self.ydl_opts = {
    'format': f'bestaudio[abr<={abr}]',  # Selects best audio within given bitrate limit
    'outtmpl': os.path.join(self.config.get_download_path(), f'{filename}.%(ext)s'),  # Defines output path
    'quiet': True,  # Suppresses unnecessary console output for clean execution
    'no_warnings': True,  # Prevents warning messages
    # 'geo_bypass': True,  # Attempts to bypass geo-restrictions
    'noplaylist': True,  # Ensures only a single item is downloaded, avoiding full playlist processing
    'extract_audio': True,  # Ensures only audio extraction is performed
    'audio_format': 'mp3',  # Converts audio to MP3 format for universal compatibility
    'audio_quality': 5,  # Ensures balanced audio quality (range: 0 = best, 10 = worst)
    'prefer_ffmpeg': True,  # Uses FFmpeg for better format handling
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '5'
    }]
}
    def setup_video_download_options(self, quality, filename, video_data):
        resolution = ''.join(filter(str.isdigit, quality.split('-')[0]))
        format = ''.join(filter(str.isdigit, quality.split('-')[1].split('p')[0]))
        if int(format) <= 720:
            selected_format = f'bestvideo[format_id*={resolution}]+bestaudio[abr<={70}]'
        else:
            selected_format = f'bestvideo[format_id*={resolution}]+bestaudio[abr<={130}]'

        # self.ydl_opts = {
        #     'outtmpl': os.path.join(self.config.get_download_path(), f'{filename}.%(ext)s'),
        #     'format': selected_format,
        #     'quiet': True,
        #     'force_generic_extractor': True,
        #     'geo_bypass': True,
        #     'noplaylist': True
        # }
        self.ydl_opts = {
         'outtmpl': os.path.join(self.config.get_download_path(), f'{filename}.%(ext)s'),  # Defines output template
         'format': selected_format,  # Ensures correct format selection
         'quiet': True,  # Suppresses console output for cleaner execution
         'no_warnings': True,  # Suppresses non-critical warnings for a smoother experience
        #  'geo_bypass': True,  # Attempts to bypass regional restrictions
         'noplaylist': True,  # Prevents automatic downloading of full playlists
         'merge_output_format': 'mp4',  # Ensures merged formats result in a standard output type
         'prefer_ffmpeg': True,  # Prioritizes FFmpeg for better format handling and conversions
         'postprocessors': [{
             'key': 'FFmpegVideoConvertor',
             'preferedformat': 'mp4'  # Converts output to MP4 for compatibility
         }]
        }     
        video_data['selected_format'] = selected_format

    def handle_video_download(self,widget_parent:SquareWidget, video_data, quality):
        if not quality:
            self.show_message.emit("critical", "Error", "Please select a video quality.")
            return
        
        widget_parent.get_download_button().setEnabled(False)
        widget_parent.get_pause_button().setEnabled(True)
        widget_parent.get_cancel_button().setEnabled(True) 
        filename = video_data.get('filename','')
        if 'Audio' in quality:
            self.setup_audio_download_options(quality, filename)
        else:
            self.setup_video_download_options(quality, filename, video_data)

        self.check_duplicate = CheckDuplicate.CheckDuplicates(self,self.ydl_opts, video_data)
        if self.status:
            print('helllll')
            worker = VideoOrAudioDownload.VideoOrAudioDownload(widget_parent,self.ydl_opts, video_data)
            worker.signals.progress.connect( widget_parent.update_progress_bar)
            worker.signals.finished.connect(lambda success, message: self.download_finished(success, message,  quality, video_data,widget_parent))
            worker.signals.status.connect(widget_parent.update_progress_label)
            self.thread_pool.start(worker)
        else:
            widget_parent.get_download_button().setEnabled(True)
            print("cancelled")

    def download_finished(self, success, message, quality, video_data, widget_parent):
        """Handle the completion of a download."""
        from Database.DownloadHistory import DownloadHistory
        from Database.sqlDatabase import Database
        video_data['current_downloading_status'] = False
        widget_parent.get_download_button().setEnabled(True)
        widget_parent.get_pause_button().setEnabled(False)
        widget_parent.get_cancel_button().setEnabled(False) 
        
        if success:
            
            # if 'Audio' in quality:
            #     self.search_and_convert_to_mp3(video_data)
            filename =video_data.get('filename','')
            id = video_data.get('id','')

            downloaded_video_path = os.path.join(self.config.get_download_path(), f'{filename}.mp4')
            # Create full output path
            print(downloaded_video_path)
            Database().update_downloaded_path(id,downloaded_video_path)
            if(self.config.get_download_history()):
                try:
                  DownloadHistory().add_download_history(video_data.get('title', ''),video_data.get('url', ''),video_data.get('selected_format',''),quality,self.config.get_download_path())
                except Exception as e:
                    print(str(e))
            toast_message.show_toast_notification("Download successfully")
        else:
            if message == "Download cancelled":
                toast_message.show_toast_notification("Download cancelled")
            else:
                toast_message.show_toast_notification("Download Failed")
    def search_and_convert_to_mp3(self, video_data):
        filename = str(video_data['filename'])
        for root, dirs, files in os.walk(self.config.get_download_path()):
            for file in files:
                # Check if the file name starts with the base filename (ignores extension)
                if file.startswith(filename):
                    file_path = os.path.join(root, file)
                    print(f"Found file: {file_path}")
                    
                    # Define the output MP3 file path
                    output_path = os.path.join(root, f"{filename}.mp3")
                    
                    # Convert to MP3 using subprocess and ffmpeg
                    try:
                        subprocess.run(
                            [
                                "ffmpeg", "-i", file_path, "-acodec", "libmp3lame", "-b:a", "160k", output_path
                            ],
                            check=True
                        )
                        os.remove(file_path)
                        print(f"Successfully converted {file} to MP3 at {output_path}")
                    except subprocess.CalledProcessError as e:
                        print(f"Error occurred during conversion: {e}")
                    return  # Exit after the first match (or you can modify to continue if needed)
        print(f"File with base name '{video_data['filename']}' not found in directory {self.config.get_download_path()}")
