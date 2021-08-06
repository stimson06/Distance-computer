#!/usr/bin/python3

import cv2
import rospy
from std_msgs.msg import Int8
from pose_detection import pose_detection

# Capture frames from a camera
cap = cv2.VideoCapture(0)

#Initializing publisher
pub = rospy.Publisher("video_stream", Int8, queue_size=10)

rospy.init_node('stream_publisher', anonymous=True)

#Set rate for publisher
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    
	# Reads frames from a camera
	ret, vid = cap.read()
	
	#class declaration
	detect = pose_detection()
	lateral_deviation, depth = detect.distances(vid)
	print('[INFO] lateral_deviation (pixels) :',lateral_deviation,' Depth (cm) :', depth)
	
	x_distance = Int8()
	y_distance = Int8()
	x_distance.data = lateral_deviation
	y_distance.data = depth

	#publishing the data
	pub.publish(x_distance)
	pub.publish(y_distance)	
	rate.sleep()

# De-allocate any associated memory usage
cap.release()
# Close the window
cv2.destroyAllWindows() 
