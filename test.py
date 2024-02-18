import cv2
import numpy as np

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

    # Find contours in the binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Adjust the area threshold as needed
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

    # Show the frame
    cv2.imshow('Tracking Yellow Ball', frame)

    if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
