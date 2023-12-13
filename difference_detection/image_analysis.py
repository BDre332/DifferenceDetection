import cv2
import numpy as np
from skimage.segmentation import slic
from skimage.measure import label
from skimage.color import label2rgb, rgb2lab, deltaE_cie76

class ImageAnalyzer:
    def __init__(self, image1_path, image2_path):
        self.image1 = cv2.imread(image1_path)
        self.image2 = cv2.imread(image2_path)

    def create_superpixels(self, n_segments=1000):
        self.superpixels1 = slic(self.image1, n_segments=n_segments, start_label=1)
        self.superpixels2 = slic(self.image2, n_segments=n_segments, start_label=1)

    def compare_superpixels(self):
        labels1 = label(self.superpixels1)
        labels2 = label(self.superpixels2)

        image1_lab = rgb2lab(label2rgb(labels1, self.image1, kind='avg'))
        image2_lab = rgb2lab(label2rgb(labels2, self.image2, kind='avg'))

        deltaE = deltaE_cie76(image1_lab, image2_lab)

        return deltaE

    def highlight_differences(self, threshold=50):  
        self.create_superpixels()  
        deltaE = self.compare_superpixels()  
        differences = np.where(deltaE > threshold)  
    
        # Create a blank mask of zeros  
        mask = np.zeros_like(self.image2)  
        
        # Mark differences in the mask  
        mask[differences] = 255  
    
        # Convert mask to grayscale  
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  
    
        # Find contours in the mask  
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
    
        # Create a copy of the original image to draw bounding box  
        result_image = self.image2.copy()  
    
        # Draw bounding box around each contour  
        for contour in contours:  
            x, y, w, h = cv2.boundingRect(contour)  
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)  
    
        return result_image  
