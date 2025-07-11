import sqlite3
from datetime import datetime
import threading
from pathlib import Path

class SearchHistory:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.__initialize()
            return cls._instance
    def __initialize(self):
        self.database_path = Path.home() / '.ytdownloader' / 'search_history.db'
        self.__init_database()  # Call _init_database when the object is created

    def __init_database(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    url TEXT PRIMARY KEY,
                    search_text TEXT NOT NULL,
                    search_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def __add_url(self, url, search_text):
        
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO search_history (url, search_text)
                VALUES (?, ?)
            ''', (url, search_text))
            conn.commit()

    def __add_title(self, url, title):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE search_history
                SET search_text = ?
                WHERE url = ?
            ''', (title, url))
            conn.commit()

    def __title_by_url(self, url):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT search_text FROM search_history WHERE url = ?
            ''', (url,))
            result = cursor.fetchone()
            return result[0] if result else None

    def __search_title_by_character(self, url):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT search_text FROM search_history WHERE url LIKE ?
            ''', (url,))
            result = cursor.fetchone()
            return result if result else None

    def get_search_history(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM search_history ORDER BY search_date DESC')
            return cursor.fetchall()

    def __clear_search_history(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM search_history')
            conn.commit()

    def __delete_search_history(self, url):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM search_history WHERE url = ?', (url,))
            conn.commit()

    def set_url(self, url,title):
        self.__add_url(url,title)

    def set_title(self, url, title):
        self.__add_title(url, title)

    def get_title_by_url(self, url):
        return self.__title_by_url(url)

    def get_title_by_character(self, url):
        return self.__search_title_by_character(url)

    def clear_search_history(self):
        self.__clear_search_history()

    def delete_search_history(self, url):
        self.__delete_search_history(url)