from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from .components.file_drop_box import FileDropBox
from .components.image_display import ImageDisplay
from .processing.image_analysis import ImageAnalyzer
from .processing.video_processor import VideoProcessor
import cv2
import os
 
  
class MainWindow(QMainWindow):  
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self.initUI()  
  
    def initUI(self):  
        self.setWindowTitle("File Difference Analyzer")  
        widget = QWidget()  
        self.layout = QVBoxLayout(widget)  
        self.dropbox1 = FileDropBox(self)  
        self.dropbox2 = FileDropBox(self)  
        self.layout.addWidget(self.dropbox1)  
        self.layout.addWidget(self.dropbox2)  
        self.button = QPushButton('Analyze Files', self)  
        self.button.clicked.connect(self.analyze_files)  
        self.layout.addWidget(self.button)  
        self.resultDisplay = ImageDisplay(self)  
        self.layout.addWidget(self.resultDisplay)  
        self.setCentralWidget(widget)  
  
    def analyze_files(self):    
        file1 = self.dropbox1.file_path    
        file2 = self.dropbox2.file_path    
    
        # Check file types and process accordingly  
        if self.is_video(file1):  
            processor1 = VideoProcessor(file1)  
            image1 = processor1.combine_frames()  
        else:  
            image1 = cv2.imread(file1)  
    
        if self.is_video(file2):    
            processor2 = VideoProcessor(file2)    
            image2 = processor2.combine_frames()  
        else:  
            image2 = cv2.imread(file2)  
    
        # Ensure images are successfully loaded/created  
        if image1 is None or image2 is None:  
            print("Failed to get image")  
            return  
    
        analyzer = ImageAnalyzer(image1, image2)  
        analyzer.create_superpixels(n_segments=500)    
        result = analyzer.highlight_differences(threshold=30)    
    
        self.displayImage(result)  
  
    def displayImage(self, image):  
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        h, w, ch = rgb_image.shape  
        bytes_per_line = ch * w  
        qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)  
        pixmap = QPixmap.fromImage(qimage)  
        self.resultDisplay.label.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio))  
  
    def is_video(self, file_path):  
        video_extensions = {".mp4", ".avi", ".mov", ".flv", ".mkv"}  
        _, extension = os.path.splitext(file_path)  
        return extension.lower() in video_extensions  