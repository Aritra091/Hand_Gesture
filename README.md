# Hand_Gesture

This project allows you to control your system's volume using hand gestures detected through your webcam. By utilizing the **MediaPipe** library to track hand landmarks, the distance between your thumb and index finger is used to adjust the system volume up or down.

## Features
-Real-time Hand Tracking**: Uses MediaPipe to track hand movements in real-time.
-Volume Control**: Adjusts system volume based on the distance between thumb and index finger.
-No External API**: Uses `pyautogui` to simulate volume control without requiring external system APIs.
