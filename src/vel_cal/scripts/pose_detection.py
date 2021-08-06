#!/usr/bin/python3

import cv2
import mediapipe as mp
import time
import numpy as np


class pose_detection():
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.Focal_length_found = 540.2045454545455 
        self.Known_width = 44.0 # sholder_width of the person 
        
    def coordinates(self, results, h, w):
        """
        Params:
        @ results: contains all the detected cooridates (32 points)
        @ h : height of the frame
        @ w : width of the frame
        
        Return:
        (x,y) coordinates of hip and shoulder (Right & Left ) """
        
        landmarks = results.pose_landmarks.landmark
        Rshoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        Lshoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER] 
        Rhip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP] 
        Lhip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP] 
        RSHcoordinate = (int(Rshoulder.x*w), int(Rshoulder.y*h))
        LSHcoordinate = (int(Lshoulder.x*w), int(Lshoulder.y*h))
        RHcoordinate =  (int(Rhip.x*w), int(Rhip.y*h))
        LHcoordinate =  (int(Lhip.x*w), int(Lhip.y*h))

        return RSHcoordinate, LSHcoordinate, RHcoordinate, LHcoordinate

    def line_intersect(self,Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
        """ 
        Params:
        @ Ax1, Ay1 : Coordinates of Left Shoulder
        @ Ax2, Ay2 : Coordinates of Right Hip
        @ Bx1, By1 : Coordinates of Right Shoulder
        @ Bx2, By2 : Coordinates of Left Hip
        
        Returns:
        (x, y) tuple or None if there is no intersection """

        d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
        if d:
            uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
            uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        else:
            return
        if not(0 <= uA <= 1 and 0 <= uB <= 1):
            return
        x = Ax1 + uA * (Ax2 - Ax1)
        y = Ay1 + uA * (Ay2 - Ay1)

        return int(x), int(y)    
    
    def distance_from_center(self, w, pt):
        """ 
        Params:
        @ w : width of the frame
        @ pt : x value computed from line intersect
        
        Returns:
        Number pixels away from the center of the frame """
    
        return (int(w/2)-pt[0])
    
    def Distance_finder(self, Focal_Length, real_shoulder_width, shoulder_width_in_frame):
        """ 
        Params:
        @ Focal_Length : Focal legth of the camera
        @ real_sholuder_width : Measured value of the user / person (known width)
        @ shoulder_width_in_frame : shoulder width computed using eculidean distance
        
        Return:
        The distance of person in accordance with camera """
    
        return (real_shoulder_width * Focal_Length)/shoulder_width_in_frame
    
    def distances(self, img_from_ros):
        """ 
        Params:
        @ img_from_ros: frame that is being sent from the ros
        
        Return:
        The lateral_deviation(pixels) and depth(cm) of person """

        with self.mp_pose.Pose(min_detection_confidence=0.2,min_tracking_confidence=0.2) as pose:
            
            h, w, _ = img_from_ros.shape
            mid_line = (int(w/2), 0 ),(int(w/2),int(h))
            image = cv2.flip(img_from_ros, 1)

            results = pose.process(img_from_ros)
            pt = (0,0)
            if results.pose_landmarks is not None:
                RSHcoordinate, LSHcoordinate, RHcoordinate, LHcoordinate = self.coordinates(results,h, w)
                shoulder_width_in_frame = int(np.sqrt((LSHcoordinate[0]-RSHcoordinate[0])**2+(LSHcoordinate[1]-RSHcoordinate[1])**2))
                Distance = self.Distance_finder(self.Focal_length_found, self.Known_width, shoulder_width_in_frame)
                depth = round(Distance, 2) 
                (a, b), (c, d) = LSHcoordinate, RHcoordinate  
                (e, f), (g, h) = RSHcoordinate, LHcoordinate  
                pt = self.line_intersect(a, b, c, d, e, f, g, h)
                if pt is not  None:
                    lateral_deviation = self.distance_from_center(w, pt)
            else:
            	lateral_deviation= 0
            	depth = 0
 
        return lateral_deviation, depth
