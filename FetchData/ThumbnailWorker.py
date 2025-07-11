import requests
from io import BytesIO
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage, QPixmap, QPainter, QPainterPath
from PIL import Image, ImageFilter
from Services.Signals import WorkerSignals
from pathlib import Path
import os
class ThumbnailWorker(QThread):
    def __init__(self, video_data):
        super().__init__()

        self.thumbnail_url = video_data.get('thumbnail','')
        self.id = video_data.get('id','')
        print(self.id)
        self.signals = WorkerSignals()
        self.file_path = Path.home() / '.ytdownloader' / 'thumbnails'
        self.img_path = os.path.join(self.file_path, f"{self.id}.png") # Define full save path
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)  # Ensure the directory exists

    def run(self):
        try:
            if os.path.exists(self.img_path):
                img = QPixmap(self.img_path)
                self.apply_rounded_corners(img)
            else:     
                img = self.download_image()
                self.save_img(img)
                img = QPixmap(self.img_path)
                self.update_img(img)

        except Exception as e:
            print("ThumbnailWorker Error:", e)
            img = self.download_image()
            self.save_img(img)
            self.update_img(img)
    def update_img(self,img):
        # Step 5: Apply rounded corners and send
        self.apply_rounded_corners(img)

    def download_image(self):
            # Step 1: Download image (full quality)
            response = requests.get(self.thumbnail_url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGBA")
            return img
        
    def save_img(self, image):
        """Save an image with a specified filename."""
        image.save(self.img_path)  # Explicitly save as PNG
        # image.save("output.png", icc_profile=None)

    def apply_rounded_corners(self, pixmap: QPixmap, radius=16) -> QPixmap:
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
            # Emit final image
        self.signals.finished.emit(rounded)