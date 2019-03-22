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

PUBLISHER_TOPIC = "depth_frame"
NODE_NAME = "depth_publisher"

def depth_publisher():
	pub = rospy.Publisher(PUBLISHER_TOPIC, Float32, queue_size=10)
	rospy.init_node(NODE_NAME, anonymous=True)
	rate = rospy.Rate(1) #10hz
	try:
		pipeline = rs.pipeline()
		profile = pipeline.get_active_profile()
		depth_sensor = profile.get_device().first_depth_sensor()
		depth_scale = depth_sensor.get_depth_scale()

		config = rs.config()
		config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
		# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
		# Start streaming
		pipeline.start(config)
		# filters
		# hole_filling = rs.hole_filling_filter()
		# get camera intrinsics

		h_portion = int(640*(1.0/5.0))
		w_portion = int(480*(1.0/5.0))

		while not rospy.is_shutdown():
			print('Getting frame data now')
			frames = pipeline.wait_for_frames()
			depth_frame = frames.get_depth_frame()
			# color_frame = frames.get_color_frame()

			# depth_frame = hole_filling.process(depth_frame)
			if not depth_frame:
			    continue

			depth_image = np.asanyarray(depth_frame.get_data())
			right_image = depth_image[ 2*w_portion:4*w_portion , 4*h_portion: ]
			right_distances = depth_scale*right_image

			right_distances_filtered = right_distances[right_distances > 0]
			# right_distances_projected = right_distances_filtered*math.sin(rad(42.6))
			mean = np.mean(right_distances_filtered)

			pub.publish(mean)

			rate.sleep()
		pipeline.stop()

	except Exception as e:
		print('except : ', e)
		pass

if __name__ == '__main__':
	try:
		depth_publisher()
	except rospy.ROSInterruptException:
		pass
