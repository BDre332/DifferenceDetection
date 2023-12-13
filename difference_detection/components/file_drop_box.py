from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from .image_display import ImageDisplay
import os

class FileDropBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):  
        self.layout = QVBoxLayout(self)  
        self.imageDisplay = ImageDisplay(self)  
        self.layout.addWidget(self.imageDisplay)  
        self.label = QLabel("Drag and drop an image or video here.", self)  
        self.label.setAlignment(Qt.AlignCenter)  
        self.layout.addWidget(self.label)  
  
    def dragEnterEvent(self, event: QDragEnterEvent):  
        if event.mimeData().hasUrls():  
            file_path = event.mimeData().urls()[0].toLocalFile()  
            if self.is_image_or_video(file_path):  
                event.accept()  
            else:  
                event.ignore()  

    def dropEvent(self, event: QDropEvent):  
        files = [u.toLocalFile() for u in event.mimeData().urls()]  
        self.file_path = files[0]  
        if self.is_video(self.file_path):  
            self.imageDisplay.displayVideoSymbol(self.file_path)  
        else:  
            self.imageDisplay.displayImage(self.file_path)  

    def is_image_or_video(self, file_path):  
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}  
        video_extensions = {".mp4", ".avi", ".mov", ".flv", ".mkv"}  
        _, extension = os.path.splitext(file_path)  
        return extension.lower() in image_extensions or extension.lower() in video_extensions  
  
    def is_video(self, file_path):  
        video_extensions = {".mp4", ".avi", ".mov", ".flv", ".mkv"}  
        _, extension = os.path.splitext(file_path)  
        return extension.lower() in video_extensions  