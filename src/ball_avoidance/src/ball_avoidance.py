#!/usr/bin/env python
import rospy
import rospkg
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from time import time

from detector import Detector

from sensor_msgs.msg import Image
from std_msgs.msg import Bool


from threading import Event

class BallAvoidance(object):
    def __init__(self, detector):
        self.event = Event()
        self.event.set()
        self.bridge = CvBridge()

        self.detector = detector

        # Publishes object recognition prediction
        self.ball_avoidance_pub = rospy.Publisher(
            'ball_avoidance/out',
             Bool,
             queue_size=1
         )

        # Subscribes to rs_camera color
        self.image_sub = rospy.Subscriber(
            '/camera/color/image_raw',
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

            contains = self.detector.contains(image)
            if contains:
                print "ball detected."
                self.ball_avoidance_pub.publish(True)
            else:
                print "no ball detected."
                self.ball_avoidance_pub.publish(False)
            self.event.set()


if __name__ == '__main__':
    rospy.init_node('ball_avoidance', anonymous=True)
    r = None
    detector = Detector((320, 240), 200)
    BallAvoidance(detector)
    rospy.spin()
