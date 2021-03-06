#!/usr/bin/env python
"""
    Recieves depth from "depth_frame" and sends appropriate control to "cmd_vel"
"""

import rospy
from std_msgs.msg import String, Float32
from geometry_msgs.msg import Twist
import numpy as np
import signal
import sys

class Echo(object):
    def __init__(self, threshold_large=0.5, threshold_small=0.2, delta=1):

        self.NAME = "depth_controller"
        self.PUBLISHER_TOPIC = "/cmd_vel"
        self.SUBSCRIBER_TOPIC = "depth_frame"

        self.value = 0
        self.threshold_large = threshold_large
        self.threshold_small = threshold_small
        self.center = (self.threshold_large + self.threshold_small)*0.5
        self.delta = delta
        self.curr_position = Twist()

        rospy.init_node(self.NAME)

        self.pub = rospy.Publisher(self.PUBLISHER_TOPIC, Twist, queue_size=5, latch=True)
        rospy.Subscriber(self.SUBSCRIBER_TOPIC, Twist, self.update_value)

    def Pcontrol_steer(self):
        left = self.curr_position.linear.x
        center = self.curr_position.linear.y
        right = self.curr_position.linear.z

        if center > 5:
            return 5
        else:
            if left > right:
                return 5 + (left - right)*2
            else:
                return 5 + (left - right)*0.5


    def signal_handler(self, sig, frame):
        velocity_control = Twist()
        velocity_control.linear.x = 0
        velocity_control.angular.z = 5
        print("sigint called")
        self.pub.publish(velocity_control)
        sys.exit(0)

    def update_value(self, msg):
        self.curr_position = msg
        rospy.loginfo(self.curr_position)

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            velocity_control = Twist()
            velocity_control.linear.x = 2
            velocity_control.angular.z = self.Pcontrol_steer()
            self.pub.publish(velocity_control)
            r.sleep()



if __name__ == '__main__':
    try:
        echo = Echo()
        signal.signal(signal.SIGINT, echo.signal_handler)
        echo.run()
    except rospy.ROSInterruptException: pass
