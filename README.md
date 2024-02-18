# SportVision
# Basketball Dribble Analysis with Computer Vision

## Overview

This project utilizes computer vision techniques to analyze basketball dribble movements in a video. The system employs OpenCV for ball tracking, Mediapipe for player pose estimation, and a Kalman filter for enhanced ball position tracking. Real-time visualization is provided to showcase dribble count, player pose, and ball movement.

## Technologies Used

- OpenCV
- Mediapipe Pose Model
- Kalman Filter
- Python

## Features

1. **Dribble Counting:**
   - The code tracks the movement of a yellow basketball in the video and counts the number of dribbles performed by the player.

2. **Player Pose Estimation:**
   - Utilizing the Mediapipe Pose model, the system estimates the player's pose, identifying key landmarks on the player's body.

3. **Real-time Visualization:**
   - Multiple windows are created for real-time visualization, including the main window displaying the tracked basketball, player's pose, ball movement, and player's skeleton.

4. **Hand Detection:**
   - The system determines which hand the player is using for dribbling by calculating the angle between thumb, wrist, and index finger landmarks.

## Algorithms Used

### Kalman Filter

The Kalman filter is employed for ball position prediction and correction. The main steps include:

1. **Initialization:**
   - Kalman filter parameters are initialized, including the measurement matrix, transition matrix, and process noise covariance.

2. **Prediction:**
   - The Kalman filter predicts the next state based on the current state, using the transition matrix.

3. **Correction:**
   - The predicted state is corrected based on the measured values obtained from ball tracking. This corrects for any errors and improves tracking accuracy.

## Dribble Counting

The dribble counting mechanism relies on detecting the upward motion of the ball. When the ball moves upward, a dribble is counted. This is determined by comparing the current ball position with the previous position.

## Future Work

1. **3D Reconstruction:**
   - Incorporate models like FrankMocap or OpenPose to reconstruct the player in 3D. Assign player movements to a 3D avatar for a more immersive analysis.

2. **GUI Application:**
   - Convert the code into a GUI application using Tkinter, allowing users to analyze basketball dribbles with real-time video from a webcam.

## Usage

### Requirements

- Python
- OpenCV
- Mediapipe
- NumPy
- Matplotlib

### Running the Main Code

```bash
python Main.py
