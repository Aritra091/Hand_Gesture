import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

x1 = y1 = x2 = y2 = 0
cooldown_time = 0.1
last_volume_change_time = time.time()
volume_history = []

webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

def calculate_distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def smooth_distance(distances, window_size=5):
    if len(distances) >= window_size:
        return np.mean(distances[-window_size:])
    return distances[-1]

def scale_to_volume(distance, max_distance, min_distance=30, max_volume=100):
    distance = np.clip(distance, min_distance, max_distance)
    volume = np.interp(distance, [min_distance, max_distance], [0, max_volume])
    return int(volume)

max_distance = 200

while True:
    _, image = webcam.read()
    image = cv2.flip(image, 1)
    frame_height, frame_width, _ = image.shape

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x1 = x
                    y1 = y

                if id == 4:
                    cv2.circle(image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y

            dist = calculate_distance(x1, y1, x2, y2)
            volume_history.append(dist)

            smoothed_dist = smooth_distance(volume_history)

            volume_level = scale_to_volume(smoothed_dist, max_distance)

            current_time = time.time()
            if current_time - last_volume_change_time > cooldown_time:
                # Control system volume smoothly using pyautogui
                pyautogui.press("volumedown") if volume_level < 50 else pyautogui.press("volumeup")
                last_volume_change_time = current_time

            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

            cv2.putText(image, f'Volume: {volume_level}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Hand volume control using python", image)

    key = cv2.waitKey(10)
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()
