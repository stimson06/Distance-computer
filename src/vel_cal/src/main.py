#!/usr/bin/python3

import cv2

import rospy
#from sensor_msgs.msg import Image
from std_msgs.msg import Int8
from scripts.pose_detection import pose_detection

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
	
	detect = pose_detection()
	angle = detect.angular_distance(vid)
	print('[INFO] Angle :',angle)
    
    # angle_pub = Int8();
	angle_msg = Int8()
	angle_msg.data = angle
	# Int8.data = angle

	pub.publish(angle_msg)	
	rate.sleep()

# De-allocate any associated memory usage
cap.release()
# Close the window
cv2.destroyAllWindows() 