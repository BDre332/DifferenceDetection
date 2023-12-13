from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap
from components.image_drop_box import ImageDropBox
from image_analysis import ImageAnalyzer
import sys
import cv2


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Difference Analyzer")
        widget = QWidget()
        self.layout = QVBoxLayout(widget)
        self.dropbox1 = ImageDropBox(self)
        self.dropbox2 = ImageDropBox(self)
        self.layout.addWidget(self.dropbox1)
        self.layout.addWidget(self.dropbox2)
        self.button = QPushButton('Analyze Images', self)
        self.button.clicked.connect(self.analyze_images)
        self.layout.addWidget(self.button)
        self.setCentralWidget(widget)

    def analyze_images(self):
        analyzer = ImageAnalyzer(self.dropbox1.image_path, self.dropbox2.image_path)
        analyzer.create_superpixels(n_segments=500)
        result = analyzer.highlight_differences(threshold=30)
        self.displayImage(result)

    def displayImage(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.dropbox1.label.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio))
