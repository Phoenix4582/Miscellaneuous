import cv2
import mediapipe as mp


class MeshDetector:
    def __init__(self, thickness=1, circle_radius=1, static_image_mode=False, max_faces=1, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.mdc = min_detection_confidence
        self.mtc = min_tracking_confidence
        self.static_image_mode = static_image_mode
        self.max_faces = max_faces

        self.drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.drawing.DrawingSpec(thickness=thickness, circle_radius=circle_radius)
        self.mesh = mp.solutions.face_mesh

    def findMesh(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        with self.mesh.FaceMesh(self.static_image_mode, self.max_faces, self.mdc, self.mtc) as face_mesh:
            results = face_mesh.process(imageRGB)
            if draw and results.multi_face_landmarks:
                for landmark in results.multi_face_landmarks:
                    self.drawing.draw_landmarks(
                        image=image,
                        landmark_list=landmark,
                        connections=self.mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=self.drawing_spec,
                        connection_drawing_spec=self.drawing_spec,
                    )

        return image
