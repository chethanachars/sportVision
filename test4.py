import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Initialize Kalman filter parameters
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], np.float32)

kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], np.float32)

kalman.processNoiseCov = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]], np.float32) * 0.03

# Initialize video capture
cap = cv2.VideoCapture('test.mp4')  # Replace 'your_video.mp4' with the path to your video

# Variables for dribble counting
prev_position = np.array([[0], [0]], dtype=np.float32)  # Initialize with a dummy value
dribble_count = 0
is_ball_upward = False  # Flag to track upward motion

# Lists to store ball positions for plotting
ball_positions_x = []
ball_positions_y = []
ball_positions_z = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for yellow color in HSV
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    # Threshold the image to get a binary mask of the yellow region
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply morphological operations to enhance ball detection
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Adjust the area threshold as needed
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Predict the next state using the Kalman filter
            prediction = kalman.predict()

            # Correct the state based on the measured values
            measurement = np.array([[x + w / 2], [y + h / 2]], dtype=np.float32)
            kalman.correct(measurement)

            # Draw the predicted and corrected positions on the frame
            cv2.circle(frame, (int(prediction[0]), int(prediction[1])), 5, (255, 0, 0), -1)
            cv2.circle(frame, (int(measurement[0]), int(measurement[1])), 5, (0, 255, 0), -1)

            # Draw the bounding box around the ball
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

            # Count dribble if the ball moves upward (change this based on your video)
            if prev_position is not None and measurement[1] < prev_position[1] and not is_ball_upward:
                dribble_count += 1
                is_ball_upward = True
            elif prev_position is not None and measurement[1] > prev_position[1]:
                is_ball_upward = False

            prev_position = measurement

            # Store ball positions for plotting
            ball_positions_x.append(measurement[0][0])
            ball_positions_y.append(measurement[1][0])
            ball_positions_z.append(len(ball_positions_x))  # Use the frame count as the z-axis

    # Display dribble count on the video
    cv2.putText(frame, f'Dribbles: {dribble_count}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Draw simple pose estimation lines
    if len(ball_positions_x) > 1:
        cv2.line(frame, (int(ball_positions_x[-1]), int(ball_positions_y[-1])),
                 (int(ball_positions_x[-2]), int(ball_positions_y[-2])), (0, 0, 255), 2)

    # Show the frame
    cv2.imshow('Tracking and Counting Dribbles', frame)

    if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

# Plot 3D scatter plot of ball positions
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.scatter(ball_positions_x, ball_positions_y, ball_positions_z, c='r', marker='o', label='Ball Position')
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Frame Count')
ax.set_title('Ball Position in 3D')
ax.legend()

# Plot 2D pose estimation lines
ax2 = fig.add_subplot(122)
ax2.plot(ball_positions_x, ball_positions_y, label='Ball Position')
ax2.set_xlabel('X Position')
ax2.set_ylabel('Y Position')
ax2.set_title('Pose Estimation Lines')
ax2.legend()

plt.show()
