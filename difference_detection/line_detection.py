import cv2
import numpy as np
import json
import os
import uuid

class LineDetector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.lines = None

    def load_image(self):
        self.image = cv2.imread(self.image_path)

        if self.image is None:
            raise Exception(f"Image could not be opened: {self.image_path}")

    def detect_lines(self):
        # Convert image to grayscale  
        lower_white = np.array([200, 200, 200])  
        upper_white = np.array([255, 255, 255])  

        mask = cv2.inRange(self.image, lower_white, upper_white)  
    
        res = cv2.bitwise_and(self.image, self.image, mask=mask)  
    
        gray_res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)  

        blurred = cv2.GaussianBlur(gray_res, (5, 5), 0)  

        edges = cv2.Canny(blurred, 50, 150)  
        self.lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)  


    def draw_lines(self):
        for line in self.lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(self.image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    def display_image(self):
        cv2.imshow('Detected Lines', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_lines_to_json(self):

        line_data = [{"rho": line[0][0], "theta": line[0][1]} for line in self.lines]
        json_file_path = os.path.join("/imageData", str(uuid.uuid4()) + ".json")