import cv2
import numpy as np

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path

    def combine_frames(self):
        cap = cv2.VideoCapture(self.video_path)
        frames = []

        while True:
            ret, frame = cap.read()

            if not ret:
                break
            
            frames.append(frame)

        last_30_frames = frames[-30:]
        combined_image = np.mean(last_30_frames, axis=0).astype(np.uint8)

        return combined_image
