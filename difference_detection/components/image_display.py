from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2

class ImageDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)

    def displayImage(self, image_path):  
        # Load the image from the file  
        image = cv2.imread(image_path)  
        # Check if the image was correctly loaded  
        if image is None:  
            print(f"Failed to load image at {image_path}")  
            return  
        # Convert the image to RGB color space  
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        # Save the image  
        self.saveImage(rgb_image, image_path)  
        # Display the image  
        h, w, ch = rgb_image.shape  
        bytes_per_line = ch * w  
        qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)  
        pixmap = QPixmap.fromImage(qimage)  
        self.label.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio))  


    def displayVideoSymbol(self, video_path):
        # Load the video
        cap = cv2.VideoCapture(video_path)
        # Check if video opened successfully
        if (cap.isOpened()== False): 
            print("Error opening video file")
            return

        # Read until video is completed
        if cap.isOpened():
            # Read first frame
            ret, frame = cap.read()
            if ret == True:
                # Save first frame as image
                frame_path = '.testImages.firstframe.jpg'
                cv2.imwrite(frame_path, frame)
                # Display image
                self.displayImage(frame_path)
            else:
                print("Can't read video file")
        # Release video object
        cap.release()

            
    def saveImage(self, image, image_path):  
        # Create a new file path  
        save_path = image_path.replace('.jpg', '_rgb.jpg')  
        # Save the image  
        cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))  