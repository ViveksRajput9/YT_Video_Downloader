import sqlite3
import threading
import json
from pathlib import Path

class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.__initialize()
            return cls._instance

    def __initialize(self):
        """Initialize database and create tables if they don't exist"""
        self.db_path = Path.home() / '.ytdownloader' / "youtube_data.db"
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.enable_wal_mode()

        # Create table if not exists
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            error TEXT,
            qualities TEXT,
            highest_quality INTEGER,
            url TEXT,
            filename TEXT,
            thumbnail TEXT,
            uploader TEXT,
            title TEXT,
            duration INTEGER,
            description TEXT,
            view_count INTEGER,
            like_count INTEGER,
            channel TEXT,
            channel_follower_count INTEGER,
            original_url TEXT,
            tags TEXT,
            channel_url TEXT,
            upload_date TEXT,
            wishlist BOOLEAN,
            downloaded_path TEXT
        )""")

        # Check if the column exists, if not, add it
        self.cursor.execute("PRAGMA table_info(videos)")
        existing_columns = [column[1] for column in self.cursor.fetchall()]
        if "downloaded_path" not in existing_columns:
            self.cursor.execute("ALTER TABLE videos ADD COLUMN downloaded_path TEXT")

        # Adding index on frequently queried fields
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_wishlist ON videos (wishlist)")
        self.connection.commit()

    def enable_wal_mode(self):
        """Enable Write-Ahead Logging for better concurrent performance"""
        try:
            self.cursor.execute("PRAGMA journal_mode=WAL")
        except sqlite3.Error as e:
            print(f"Failed to enable WAL mode: {e}")

    def add_item(self, item):
        """Insert a new video record with exception handling"""
        if not item or "id" not in item:
            return "Invalid item data"

        try:
            self.cursor.execute("""
            INSERT INTO videos (id, error, qualities, highest_quality, url, filename, thumbnail, 
                                uploader, title, duration, description, view_count, like_count, channel, 
                                channel_follower_count, original_url, tags, channel_url, upload_date, wishlist, downloaded_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["id"], item.get("error"),
                json.dumps(item.get("qualities", [])),
                item.get("highest_quality"),
                item.get("url"), item.get("filename"),
                item.get("thumbnail"), item.get("uploader"),
                item.get("title"), item.get("duration"),
                item.get("description"), item.get("view_count"),
                item.get("like_count"), item.get("channel"),
                item.get("channel_follower_count"),
                item.get("url"), json.dumps(item.get("tags", [])),
                item.get("channel_url"), item.get("upload_date"),
                item.get("wishlist", False),
                item.get("downloaded_path","")  # New field
            ))
            self.connection.commit()
            return "Item added successfully"
        except sqlite3.IntegrityError:
            return "Item already exists"
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def create_video_dict(self, row):
        """Convert database row to dictionary"""
        return {
            "id": row[0], "error": row[1], "qualities": json.loads(row[2]), "highest_quality": row[3],
            "url": row[4], "filename": row[5], "thumbnail": row[6], "uploader": row[7],
            "title": row[8], "duration": row[9], "description": row[10], "view_count": row[11],
            "like_count": row[12], "channel": row[13], "channel_follower_count": row[14],
            "url": row[15], "tags": json.loads(row[16]), "channel_url": row[17], "upload_date": row[18],
            "wishlist": row[19], "downloaded_path": row[20]  # New field
        }

    def update_item(self, video_id, updated_item):
        """Update video details"""
        if not updated_item or "id" not in updated_item:
            return "Invalid data"

        try:
            self.cursor.execute("""
            UPDATE videos SET error=?, qualities=?, highest_quality=?, url=?, filename=?, 
                              thumbnail=?, uploader=?, title=?, duration=?, description=?, 
                              view_count=?, like_count=?, channel=?, channel_follower_count=?, 
                              url=?, tags=?, channel_url=?, upload_date=?, downloaded_path=?
            WHERE id=?
            """, (
                updated_item.get("error"),
                json.dumps(updated_item.get("qualities", [])),
                updated_item.get("highest_quality"), updated_item.get("url"),
                updated_item.get("filename"), updated_item.get("thumbnail"),
                updated_item.get("uploader"), updated_item.get("title"),
                updated_item.get("duration"), updated_item.get("description"),
                updated_item.get("view_count"), updated_item.get("like_count"),
                updated_item.get("channel"), updated_item.get("channel_follower_count"),
                updated_item.get("url"), json.dumps(updated_item.get("tags", [])),
                updated_item.get("channel_url"), updated_item.get("upload_date"),
                updated_item.get("downloaded_path"),  # New field
                video_id
            ))
            
            self.connection.commit()
            return "Item updated successfully"
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def remove_item(self, video_id):
        """Delete item by ID"""
        try:
            self.cursor.execute("DELETE FROM videos WHERE id=?", (video_id,))
            self.connection.commit()
            return "Item removed successfully"
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def get_data_by_id(self, video_id):
        """Fetch video data by ID"""
        try:
            self.cursor.execute("SELECT * FROM videos WHERE id=?", (video_id,))
            row = self.cursor.fetchone()
            return self.create_video_dict(row) if row else None
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def get_wishlist_videos(self):
        """Fetch all videos where wishlist is True"""
        try:
            self.cursor.execute("SELECT * FROM videos WHERE wishlist = ?", (True,))
            rows = self.cursor.fetchall()
            return [self.create_video_dict(row) for row in rows] if rows else []
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def update_wishlist(self, video_id: str, toggle: bool):
        """Update the wishlist status of a video"""
        try:
            self.cursor.execute("""
                UPDATE videos 
                SET wishlist = ? 
                WHERE id = ?
            """, (toggle, video_id))
            self.connection.commit()
            return f"Wishlist updated for video {video_id} → {toggle}"
        except sqlite3.Error as e:
            return f"Error updating wishlist: {e}"
    def update_downloaded_path(self, video_id: str, downloaded_path: str):
        """Update the downloaded path of a video based on ID"""
        try:
            self.cursor.execute("""
                UPDATE videos 
                SET downloaded_path = ? 
                WHERE id = ?
            """, (downloaded_path, video_id))
            self.connection.commit()
            return f"Downloaded path updated for video {video_id} → {downloaded_path}"
        except sqlite3.Error as e:
            return f"Error updating downloaded path: {e}"
        


    def get_videos_with_downloaded_path(self):
        """Fetch all videos where downloaded_path is not NULL or empty"""
        try:
            self.cursor.execute("""
                SELECT * FROM videos WHERE downloaded_path IS NOT NULL AND downloaded_path != ''
            """)
            rows = self.cursor.fetchall()
            return [self.create_video_dict(row) for row in rows] if rows else []
        except sqlite3.Error as e:
            return f"Database error: {e}"
    def close_connection(self):
        """Close database connection"""
        self.connection.close()