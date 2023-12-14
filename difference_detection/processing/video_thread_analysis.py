import sys  
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel  
from PyQt5.QtGui import QImage, QPixmap  
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot  
from image_analysis import ImageAnalyzer
import cv2 


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self._run_flag = False
        self.cap = None
        self.camera_index = 0

    def run(self):
        self._run_flag = True
        self.cap = cv2.VideoCapture(self.camera_index)
        while self._run_flag:
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)

    def stop(self):
        self._run_flag = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            
    def start_video(self):  
        if not self.video_thread.isRunning():  # Only start the video thread if it's not already running  
            self.video_thread = VideoThread()  # Create a new VideoThread object  
            self.video_thread.change_pixmap_signal.connect(self.update_image)  # Connect the signal to the slot  
            self.video_thread.start()  # Start the video thread 
        
    def set_camera_index(self, index):
        self.camera_index = index
        if self._run_flag:
            self.stop()
            self.start()
