import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFileDialog, QVBoxLayout
from PySide6.QtGui import QPixmap

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Viewer")
        
        # Create QLabel with fixed size
        self.label = QLabel(self)
        self.label.setFixedSize(275, 160)
        self.label.setStyleSheet("border: 1px solid black;")
        self.label.setScaledContents(True)  # Ensures full resolution display without alteration

        # Button to select image
        self.button = QPushButton("Select Image", self)
        self.button.clicked.connect(self.openImage)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def openImage(self):
        # fileName, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        # print(fileName)
        # if fileName:
            pixmap = QPixmap("C:\\Users\\Abhishek Rajput\\.ytdownloader\\thumbnails\\UkxwV613b0g.png")
            self.label.setPixmap(pixmap)  # Original quality displayed without scaling

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())