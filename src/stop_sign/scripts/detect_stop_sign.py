from skimage.transform import pyramid_gaussian
import argparse
import cv2
import time
import numpy as np
import glob
from matplotlib import pyplot as plt

class Detector(object):
    __init__(self, target, win_size=16, threshold = 8e-5, step_size=2):
        self.win_size = win_size
        self.target = cv2.resize(target, (win_size, win_size))
        self.threshold = threshold
        self.step_size = step_size

    def sliding_window(self, image):
        for y in range(0, image.shape[0], self.step_size):
            for x in range(0, image.shape[1], self.step_size):
                yield (x, y, image[y:y+self.win_size[1], x:x+self.win_size[1]])

    def meanSquareError(self, image):
        assert image.shape == self.target.shape, "Images must be the same shape."
        error = np.sum((image.astype("float") - self.target.astype("float")) ** 2)
        error = error/float(image.shape[0] * image.shape[1] * image.shape[2])
        return error

    def get_ssim(image, debug = False):
        start = time.time()

        max_ssim = -1
        max_img = None
        max_bbox = []

        while image.shape[0] > 16 and  image.shape[1] > 16:
            image = cv2.pyrDown(image)
            for (x, y, window) in sliding_window(image, step_size=2, window_size=(16, 16)):
                if window.shape[0] != 16 or window.shape[1] != 16:
                    continue

                ssim = compareImages(self.target, image[y:y+16, x:x+16])
                if ssim > max_ssim:
                    max_ssim = ssim
                    max_img = image.copy()
                    max_bbox = [(x, y), (x + 16, y + 16)]

                if debug:
                    clone = image.copy()
                    cv2.rectangle(clone, (x, y), (x + 16, y + 16), (255, 0, 0), 2)
                    cv2.imshow("Window",clone)
                    cv2.waitKey(1)
                    time.sleep(0.025)

        if debug:
            if max_ssim < self.threshold:
                cv2.rectangle(max_img, max_bbox[0], max_bbox[1], (0, 0, 255), 2)
            else:
                cv2.rectangle(max_img, max_bbox[0], max_bbox[1], (0, 255, 0), 2)

            cv2.imwrite("{}.png".format(name), max_img)
            cv2.destroyAllWindows()

        end = time.time()
        return max_ssim

    def contains_ss(image, debug=False):
        max_ssim = self.get_ssim(image)
        return max_ssim > self.threshold

    @staticmethod
    def compareImages(a, b):
        return 1./meanSquareError(a, b)
