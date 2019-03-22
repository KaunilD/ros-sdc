#!/usr/bin/env python
"""
    Computes depth and publishes it to "depth_frame" topic
"""

import pyrealsense2 as rs
import rospy
import numpy as np
import sys
import cv2
from std_msgs.msg import String, Float32
from geometry_msgs.msg import Twist

PUBLISHER_TOPIC = "depth_frame"
NODE_NAME = "depth_publisher"

def depth_publisher():
	pub = rospy.Publisher(PUBLISHER_TOPIC, Twist, queue_size=10)
	rospy.init_node(NODE_NAME, anonymous=True)
	rate = rospy.Rate(10) #10hz
	pipeline = rs.pipeline()

	config = rs.config()
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

	# Start streaming
	pipeline.start(config)

	profile = pipeline.get_active_profile()
	depth_sensor = profile.get_device().first_depth_sensor()
	depth_scale = depth_sensor.get_depth_scale()

	col_length = int(640*(1.0/8.0))
	row_length = int(480*(1.0/5.0))

	while not rospy.is_shutdown():
		print('Getting frame data now')
		frames = pipeline.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		if not depth_frame:
			continue

		depth_image = np.asanyarray(depth_frame.get_data())

		left_image = depth_image[ 3*row_length:4*row_length  , 0:col_length ]
		left_distances = depth_scale*left_image
		left_distances_filtered = left_distances[left_distances > 0]

		center_image = depth_image[ 3*row_length: 4*row_length, 3*col_length:5*col_length]
		center_distances = depth_scale*center_image
		center_distances_filtered = center_distances[center_distances > 0]

		right_image = depth_image[  3*row_length:4*row_length, 7*col_length:8*col_length ]
		right_distances = depth_scale*right_image
		right_distances_filtered = right_distances[right_distances > 0]

		mean = Twist()
		mean.linear.x = np.mean(left_distances_filtered)
		mean.linear.y = np.mean(center_distances_filtered)
		mean.linear.z = np.mean(right_distances_filtered)
		print(mean)
		pub.publish(mean)
		rate.sleep()

	pipeline.stop()

if __name__ == '__main__':
	try:
		depth_publisher()
	except rospy.ROSInterruptException:
		pass
