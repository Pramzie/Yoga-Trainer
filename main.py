import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk
import pyttsx3
import json
import os
import time

from utils.angle_utils import calculate_angle
from utils.pose_module import PoseDetector
from utils.feedback import get_pose_feedback

# Setup TTS engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load poses from JSON files
def load_poses(folder="poses"):
    poses = {}
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file)) as f:
                poses[file[:-5]] = json.load(f)
    return poses

# GUI Pose Selector
class PoseSelector:
    def __init__(self, poses):
        self.selected_pose = None
        self.root = tk.Tk()
        self.root.title("Yoga Pose Trainer")

        label = ttk.Label(self.root, text="Select a Pose to Practice:", font=("Arial", 14))
        label.pack(pady=10)

        self.combo = ttk.Combobox(self.root, values=list(poses.keys()), font=("Arial", 12))
        self.combo.pack(pady=10)

        button = ttk.Button(self.root, text="Start", command=self.select_pose)
        button.pack(pady=10)

        self.root.mainloop()

    def select_pose(self):
        self.selected_pose = self.combo.get()
        self.root.destroy()

# Main App
if __name__ == "__main__":
    poses = load_poses()
    gui = PoseSelector(poses)

    if not gui.selected_pose:
        print("No pose selected. Exiting...")
        exit()

    target_pose = poses[gui.selected_pose]
    speak(f"Get ready to practice {gui.selected_pose.replace('_', ' ')}")

    cap = cv2.VideoCapture(0)
    detector = PoseDetector()

    last_feedback = []
    last_spoken_time = time.time() - 6  # Allow immediate feedback on start

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        landmarks = detector.find_pose(frame)

        if landmarks:
            user_angles = detector.get_key_angles(landmarks, target_pose.keys())
            feedback, success = get_pose_feedback(user_angles, target_pose)

            # Display feedback on screen
            for msg in feedback:
                cv2.putText(frame, msg, (10, 30 + 30 * feedback.index(msg)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Speak only once every 6 seconds
            if feedback != last_feedback and (time.time() - last_spoken_time > 6):
                if success:
                    speak("Excellent! You're doing it right!")
                else:
                    for msg in feedback:
                        speak(msg)
                last_spoken_time = time.time()
                last_feedback = feedback

        cv2.imshow("Yoga Trainer", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
