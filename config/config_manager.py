from pathlib import Path
import json
from typing import Any, Dict
import logging
import threading

class Config_Manager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.__initialize()
            return cls._instance

    def __initialize(self):
        self.logger = logging.getLogger(__name__)
        self.config_file = Path.home() / '.ytdownloader' / 'config.json' 
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.__update_json()
        import multiprocessing
        # Determine the number of threads available in the system
        self.total_threads = multiprocessing.cpu_count()  

    def __default_config(self) -> Dict[str, Any]:
        return {
            "max_concurrent_downloads": 3 ,
            "download_path": self.__ensure_download_path_exists(),
            "theme": "Dark Mode",
            "search_history": True,
            "max_search_history": 10,
            "download_history": True,
            "max_download_history": 10,    
            "language": "en",
            "preferred_format": "mp4",
            "auto_convert": False,
            "max_retries": 3,
            "chunk_size": 1024 * 1024,
            "timeout": 30,
            "defaultTheme": "Dark Mode",
            "loadingAnimation": True,
            "container_width":300,
            "suggestion":True,
            "video_quality":"None",
            "isDefault_Download_Enable":False
        }

    def __load_config(self) -> Dict[str, Any]:
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
            else:
                data = self.__default_config()
                self.__save_config(data)
            return data
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return self.__default_config()
        

    def __update_json(self):
        """Compare only keys of two JSON configurations."""
        config1= self.__load_config()
        config2 = self.__default_config()
        keys1 = set(config1.keys())
        keys2 = set(config2.keys())

        missing_in_config1 = keys2 - keys1
        missing_in_config2 = keys1 - keys2
        if len(missing_in_config1) :
            print('json updated')
            for data in config1:
                config1[data] = config2.get(data)
                self.__save_config(config2)
        print( {
            "missing_in_config1": list(missing_in_config1),
            "missing_in_config2": list(missing_in_config2)
        })
    def compare_json_key(config1: dict, config2: dict) -> bool:
        """Check if two JSON objects have the same keys."""
        return set(config1.keys()) == set(config2.keys())
    

    def __save_config(self, data: Dict[str, Any]) -> None:
        try:
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")

    def reset_config(self):
        self.__save_config(self.__default_config)

    def __ensure_download_path_exists(self) -> str:
        download_path = Path.home() / 'Downloads' / 'YTDownloads'
        if not download_path.exists():
            download_path.mkdir(parents=True, exist_ok=True)
        return str(download_path)

    # Getter methods
    def get_isSuggestion(self)-> bool:
        return self.__load_config().get('suggestion',True)
    
    def get_container_width(self)-> int:
        return self.__load_config().get('container_width',300)
    
    def get_max_concurrent_downloads(self) -> int:
        return self.__load_config().get('max_concurrent_downloads')

    def get_theme(self) -> str:
        return self.__load_config().get('theme', 'Dark Mode')

    def get_language(self) -> str:
        return self.__load_config().get('language', 'en')

    def get_save_history(self) -> bool:
        return self.__load_config().get('download_history', True)

    def get_auto_convert(self) -> bool:
        return self.__load_config().get('auto_convert', False)

    def get_preferred_format(self) -> str:
        return self.__load_config().get('preferred_format', 'mp4')

    def get_download_path(self) -> str:
        return self.__load_config().get('download_path', str(self.__ensure_download_path_exists()))

    def get_max_retries(self) -> int:
        return self.__load_config().get('max_retries', 3)

    def get_chunk_size(self) -> int:
        return self.__load_config().get('chunk_size', 1024 * 1024)

    def get_timeout(self) -> int:
        return self.__load_config().get('timeout', 30)

    def get_default_theme(self) -> str:
        return self.__load_config().get('defaultTheme', 'Dark Mode')

    def get_loading_animation(self) -> bool:
        return self.__load_config().get('loadingAnimation', True)
    
    def get_search_history(self) -> bool:
        return self.__load_config().get('search_history', True)
    
    def get_max_search_history(self) -> int:
        return self.__load_config().get('max_search_history', 10)       
    def get_download_history(self) -> bool:
        return self.__load_config().get('download_history', True)

    def get_max_download_history(self) -> int:
        return self.__load_config().get('max_download_history', 10)
    
    def get_total_thread(self) -> int:
 
        return   max(2, self.total_threads // 2)  # Use half of the threads, but ensure at least 2
    
    def get_default_video_quality(self)->str:
        return self.__load_config().get('video_quality')
    
    def get_default_download_toggle(self):
        return self.__load_config().get('isDefault_Download_Enable')
    


    #  setters
    def set_default_video_quality(self,value):
        try:
            data = self.__load_config()
            data['video_quality'] = value
            self.__save_config(data)
        except Exception as e :
            self.logger.error(f"Failed to update default quality {str(e)}")

    def set_default_download_enable(self,toggle:bool):
        try :
            data = self.__load_config()
            data['isDefault_Download_Enable'] = toggle
            self.__save_config(data)
        except Exception as e :   
            self.logger.error(f"Failed to update suggestion {str(e)}")    

    def set_isSuggestion(self,value:bool)-> None:
        try :
            data = self.__load_config()
            data['suggestion'] = value
            self.__save_config(data)
        except Exception as e :   
            self.logger.error(f"Failed to update suggestion {str(e)}")

    def set_max_concurrent_downloads(self, value: int) -> None:

        try:
            value = int(value)
            data = self.__load_config()
            data['max_concurrent_downloads'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update max_concurrent_downloads: {e}")

    def set_theme(self, value: str) -> None:
        try:
            data = self.__load_config()
            data['theme'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update theme: {e}")

    def set_language(self, value: str) -> None:
        try:
            data = self.__load_config()
            data['language'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update language: {e}")

    def set_download_history(self, value: bool) -> None:
        try:
            data = self.__load_config()
            data['download_history'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update save_history: {e}")

    def set_auto_convert(self, value: bool) -> None:
        try:
            data = self.__load_config()
            data['auto_convert'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update auto_convert: {e}")

    def set_preferred_format(self, value: str) -> None:
        try:
            data = self.__load_config()
            data['preferred_format'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update preferred_format: {e}")

    def set_download_path(self, value: str) -> None:
        try:
            data = self.__load_config()
            data['download_path'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update download_path: {e}")

    def set_max_retries(self, value: int) -> None:
        try:
            data = self.__load_config()
            data['max_retries'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update max_retries: {e}")

    def set_chunk_size(self, value: int) -> None:
        try:
            data = self.__load_config()
            data['chunk_size'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update chunk_size: {e}")

    def set_timeout(self, value: int) -> None:
        try:
            data = self.__load_config()
            data['timeout'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update timeout: {e}")

    def set_default_theme(self, value: str) -> None:
        try:
            data = self.__load_config()
            data['defaultTheme'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update defaultTheme: {e}")

    def set_loading_animation(self, value: bool) -> None:
        try:
            data = self.__load_config()
            data['loadingAnimation'] = value
            print(f"loading animation status :{value}")
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update loadingAnimation: {e}")
    

    def set_search_history(self, value: bool) -> None:
        try:
            data = self.__load_config()
            data['search_history'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update search_history: {e}")

    def set_max_search_history(self, value: int) -> None:
        try:
            data = self.__load_config()
            data['max_search_history'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update max_search_history: {e}")

    def set_max_download_history(self, value: int) -> None:
        try:
            data = self.__load_config()
            data['max_download_history'] = value
            self.__save_config(data)
        except Exception as e:
            self.logger.error(f"Failed to update max_download_history: {e}")    