#!/usr/bin/env python
import rospy
import rospkg
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from time import time

from detect_stop_sign import Detector

from sensor_msgs.msg import Image
from std_msgs.msg import Bool


from threading import Event

class StopSign(object):
    def __init__(self, detector):
        self.event = Event()
        self.bridge = CvBridge()

        self.img_width = 320
        self.img_height = 240
        self.img_ch = 3

        self.detector = detector

        self.input_shape = (self.img_height, self.img_width, 3)

        # Publishes object recognition prediction
        self.stop_sign_pub = rospy.Publisher(
            'stop_sign/out',
             Bool,
             queue_size=1
         )

        # Subscribes to rs_camera color
        self.image_sub = rospy.Subscriber(
            '/camera/color/image_rect_color',
            Image,
            self.image_callback,
            queue_size=1,
            buff_size=320000000
        )

    def image_callback(self, msg):
        # Perform prediction per the set frequency
        if self.event.isSet():
    	    self.event.clear()
            # Convert ros image to cv image
            try:
                image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            except CvBridgeError, e:
                return

            if image.shape != (self.img_width, self.img_height, 3):
                image = cv2.resize(image, (self.img_width, self.img_height))

            contains = self.detector.contains_ss(image)

            if contains:
                print "Stop sign detected."
                self.stop_sign_pub.publish(True)
            else:
                print "No stop sign detected."
                self.stop_sign_pub.publish(False)
            self.event.set()

if __name__ == '__main__':
    rospy.init_node('stop_sign', anonymous=True)
    r = None
    try:
        r = rospkg.RosPack()
        target = r.get_path("adv_robotics")+"/stop_sign/data/stop_sign.png"
    except IOError, e:
        print e

    detector = Detector(cv2.imread(target))
    StopSign(detector)
    rospy.spin()
