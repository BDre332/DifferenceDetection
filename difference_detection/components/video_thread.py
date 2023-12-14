import sys  
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton  
from PyQt5.QtGui import QImage, QPixmap  
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot  
import cv2  
  
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.running = False
        self.cap = cv2.VideoCapture(0)

    def run(self):
        self.running = True
        print("VideoThread started")
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                print("Frame captured")
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)

    def stop(self):
        self.running = False
        self.cap.release()
        print("VideoThread stopped")

    def set_camera_index(self, index):
        self.stop()
        self.cap = cv2.VideoCapture(index)
        self.start()
