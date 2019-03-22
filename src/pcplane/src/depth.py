import pyrealsense2 as rs
import numpy as np
import sys
import cv2
import math

DRAW_GRID = True


def grid(color_image, row_length, col_length, w_color, h_color, thickness):
    for i in range(1, 5):
        # horizontal lines
        cv2.line(color_image, (0, i*row_length), (640, i*row_length), (w_color, 0, 0), thickness, 1)
    for i in range(1, 8):
        # vertical line
        cv2.line(color_image, (i*col_length, 0), (i*col_length, 480), (0, 0, h_color), thickness, 1)

if DRAW_GRID:
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

rad = lambda a: a*(math.pi/180.0)

pipeline = rs.pipeline()

config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# Start streaming
pipeline.start(config)

# filters
hole_filling = rs.hole_filling_filter()

# get camera intrinsics
profile = pipeline.get_active_profile()
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

col_length = int(640*(1.0/8.0))
row_length = int(480*(1.0/5.0))

while True:
    # This call waits until a new coherent set of frames is available on a devicepip3 install opencv-python
    # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable
    print('Getting frame data now')
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # depth_frame = hole_filling.process(depth_frame)
    if not depth_frame or not color_frame:
        continue

    depth_image = np.asanyarray(depth_frame.get_data())

    left_image = depth_image[ 2*row_length:3*row_length  , 0:col_length ]
    left_distances = depth_scale*left_image
    left_distances_filtered = left_distances[left_distances > 0]

    center_image = depth_image[ 2*row_length: 3*row_length, 3*col_length:5*col_length]
    center_distances = depth_scale*center_image
    center_distances_filtered = center_distances[center_distances > 0]

    right_image = depth_image[  2*row_length:3*row_length, 7*col_length:8*col_length ]
    right_distances = depth_scale*right_image
    right_distances_filtered = right_distances[right_distances > 0]

    # right_distances_projected = right_distances_filtered*math.sin(rad(42.6))

    print(np.mean(left_distances_filtered), np.mean(center_distances_filtered), np.mean(right_distances_filtered))

    if DRAW_GRID:
        color_image = np.asanyarray(color_frame.get_data())
        cv2.rectangle(
                color_image,
                (0, 2*row_length ),
                (col_length,3*row_length ),
                (0, 255, 0),
                3,
                2
             )

        cv2.rectangle(
                color_image,
                (3*col_length, 2*row_length ),
                (5*col_length, 3*row_length ),
                (0, 255, 0),
                3,
                2
             )

        cv2.rectangle(
                color_image,
                (7*col_length, 2*row_length ),
                (8*col_length, 3*row_length ),
                (0, 255, 0),
                3,
                2
             )

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        # Stack both images horizontally
        grid(color_image, row_length, col_length, 255, 255, 2)
        images = np.hstack((color_image, depth_colormap))
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

pipeline.stop()
