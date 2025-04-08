import mediapipe as mp
import cv2
from .angle_utils import calculate_angle

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

    def find_pose(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        landmarks = {}

        if results.pose_landmarks:
            for idx, lm in enumerate(results.pose_landmarks.landmark):
                h, w, _ = frame.shape
                landmarks[idx] = (int(lm.x * w), int(lm.y * h))
            self.mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return landmarks

    def get_key_angles(self, landmarks, joints):
        angles = {}
        for joint in joints:
            p1, p2, p3 = joint.split("_")
            idx1, idx2, idx3 = int(p1), int(p2), int(p3)
            if idx1 in landmarks and idx2 in landmarks and idx3 in landmarks:
                angles[joint] = calculate_angle(
                    landmarks[idx1], landmarks[idx2], landmarks[idx3]
                )
        return angles
