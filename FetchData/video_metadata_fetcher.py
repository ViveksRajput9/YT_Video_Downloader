import yt_dlp 

class VideoMetadataFetcher:
    def __init__(self, url):
        self.url = url
        self.ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'force_generic_extractor': True,
            'geo_bypass': True,
            'noplaylist': True
        }

    def fetch(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as y:
            return y.extract_info(self.url, download=False)
    @staticmethod
    def fetch_url_using_keyword(query, max_results=25):
        search_url = f"ytsearch{max_results}:{query}"
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
            return [  entry['url'] for entry in info['entries']]
    