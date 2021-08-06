# Human-Follow
Dynamic tracking of human to compute the lateral_deviation and Depth with pose detection [Mediapipe](https://google.github.io/mediapipe/solutions/pose.html) and depth estimation [OpenCV](https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/) in the FOV of monocular camera.
  
# Computation of Lateral-Deviation
Marking is made with the help of coordiantes detected by Mediapipe. The intersection of point made by the line drawn from right_shoulder(12), left_hip(23) and left_shoulder(11) and righ_hip(24)

![alt text](https://github.com/stimson06/Human-Follow/blob/master/pose_detection.png)

# Computation of depth
Using the focal length formula 
```math
(shoulder_width(original) X Focal length) / computed_shoulder_width 
```
shoulder_width(original) = physical measurement
computed_shoulder_width = Distance computed from the coordinates 11 & 12

# Execution of code
clone the repository and move to the human follow directory
```
$ cd Human-Follow
```
Build all the dependencies and source it
```
$ catkin_make
$ source ./devel/setup.bash
```
Launch the file
```
$ roslaunch vel_cal human_follow.launch
```

# Known issues
* False calculation when shoulder of the person is not aligned parallel to the camera.

#### Tested on: ubuuntu 20.04 LTS
