# Distance-Computer
Dynamic tracking of human to compute the lateral_deviation and Depth with pose detection [Mediapipe](https://google.github.io/mediapipe/solutions/pose.html) and depth estimation [OpenCV](https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/) in the FOV of monocular camera.
  
## Computation of Lateral-Deviation
Marking is made with the help of coordiantes detected by Mediapipe. The intersection of point made by the line drawn from right_shoulder(12), left_hip(23) and left_shoulder(11) and righ_hip(24)

![alt text](https://github.com/stimson06/Human-Follow/blob/master/pose_detection.png)

## Computation of depth
Using the focal length formula, \
\
![Depth](https://latex.codecogs.com/png.image?\dpi{110}%20\frac{shoulder_width(original)%20X%20Focal%20length}{computed_shoulder_width})

shoulder_width(original) = physical measurement \
computed_shoulder_width = Distance computed from the coordinates 11 & 12

## Execution of code
clone the repository and move to the human follow directory
```
$ cd Distance-Computer
```
Build all the dependencies and source it
```
$ catkin_make
$ source ./devel/setup.bash
```
Launch the file
```
$ roslaunch vel_cal compute-distance.launch
```
# Behind the screen
https://user-images.githubusercontent.com/44506282/132972245-5cf46b11-e8b2-4a63-a760-da2badf30c08.mp4

# Actual output
![disatance computer](https://user-images.githubusercontent.com/44506282/132972422-3e9d2c2c-cca3-4822-a37d-153daca0aba4.png)


## Issues
* Offset of 10 - 20 cm in depth and 0.5 - 1.5 cm in lateral deviation.
* False calculation when shoulder of the person is not aligned parallel to the camera.

#### ROS version: Noetic
#### Tested on: ubuuntu 20.04 LTS

