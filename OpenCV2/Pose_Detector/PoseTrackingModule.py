import cv2
import mediapipe as mp


class poseDetector:

    def __init__(self, mode=False, ubo=False, smooth_lms=False, min_dc=0.5, min_tc=0.5):
        self.mode = mode
        self.upper_body_only = ubo
        self.smooth_landmarks = smooth_lms
        self.min_dc = min_dc
        self.min_tc = min_tc

        self.mpPoses = mp.solutions.pose
        self.poses = self.mpPoses.Pose(
            static_image_mode=self.mode,
            upper_body_only=self.upper_body_only,
            smooth_landmarks=self.smooth_landmarks,
            min_detection_confidence=self.min_dc,
            min_tracking_confidence=self.min_tc,
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findPoses(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.poses.process(imageRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(image, self.results.pose_landmarks, self.mpPoses.POSE_CONNECTIONS)

        return image

    def findNose(self, image, draw=True):

        if self.results.pose_landmarks:
            myPose = self.results.pose_landmarks
            h, w, _ = image.shape

            cx = int(myPose.landmark[self.mpPoses.PoseLandmark.NOSE].x * w)
            cy = int(myPose.landmark[self.mpPoses.PoseLandmark.NOSE].y * h)
            print(f"Nose coordinates: ({cx} , {cy})")
            if draw:
                cv2.circle(image, (cx, cy), 7, (255, 0, 0), cv2.FILLED)


