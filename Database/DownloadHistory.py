import sqlite3
from datetime import datetime
import threading
from pathlib import Path

class DownloadHistory:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        self.database_path = Path.home() / '.ytdownloader' /'download_history.db'
        self.__init_database()  # Call _init_database when the object is created
    def __init_database(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(255) UNIQUE NOT NULL,
                    url VARCHAR(255),
                    format VARCHAR(255),
                    quality VARCHAR(255),
                    download_path VARCHAR(255),
                    download_date DATETIME,
                    status VARCHAR(255),
                    download_count INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def add_download_history(self, title, url, format_type, quality, download_path, status="Completed"):
        """Add a new entry to the downloads history."""
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO downloads (title, url, format, quality, download_path, download_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, url, format_type, quality, download_path, datetime.now(), status))
            conn.commit()

    def __download_history(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM downloads ORDER BY download_date DESC')
            return cursor.fetchall()

    def __clear_history(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM downloads')
            conn.commit()

    def get_download_history(self):
        return self.__download_history()

    def clear_history(self):
        self.__clear_history()

