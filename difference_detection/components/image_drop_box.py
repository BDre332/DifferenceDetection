from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from .image_display import ImageDisplay

class ImageDropBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.imageDisplay = ImageDisplay(self)
        self.layout.addWidget(self.imageDisplay)
        self.label = QLabel("Drag and drop and image here.", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.image_path = files[0]
        self.imageDisplay.displayImage(self.image_path)

