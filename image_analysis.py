import cv2
import numpy as np
from skimage.segmentation import slic
from skimage.measure import label
from skimage.color import label2rgb, rgb2lab, deltaE_cie76

class ImageAnalyzer:
    def __init__(self, image1_path, image2_path):
        self.image1 = cv2.cvtColor(cv2.imread(image1_path), cv2.COLOR_BGR2RGB)
        self.image2 = cv2.cvtColor(cv2.imread(image2_path), cv2.COLOR_BGR2RGB)
        self.superpixels1 = None
        self.superpixels2 = None

    def create_superpixels(self, n_segments=100):
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
        deltaE = self.compare_superpixels()
        differences = np.where(deltaE > threshold)

        result_image = self.image1.copy()
        result_image[differences] = [255, 0, 0]  # highlight differences in red

        return result_image
