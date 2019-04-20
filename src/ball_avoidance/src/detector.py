import cv2
import numpy as np

class Detector(object):
    def __init__(self, image_size, max_radius, debug=False):
        self.image_shape = image_size
        self.max_radius = max_radius
        self.debug = debug

    def preprocess(self, image):
        if image.shape != self.image_shape:
            image = cv2.resize(image, self.image_shape)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # helps remove snp noise
        image = cv2.medianBlur(image, 5)

        """
             try:
                 2. follow up with errosion and dialation
                    for removing texture artifacts
                 1. gaussian blur
        """

        image = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return image

    def contains(self, image):
        img_prep = self.preprocess(image)

        circles = cv2.HoughCircles(
            img_prep, cv2.HOUGH_GRADIENT, 1, 260,
            param1=30, param2=65,
            minRadius=0, maxRadius=self.max_radius
        )

        if self.debug:
            for (x, y, r) in circles[0]:
                cv2.circle(image, (x, y), r, (0, 255, 0), 3)

        if circles != None and len(circles) >= 1:
            return True
        return False
