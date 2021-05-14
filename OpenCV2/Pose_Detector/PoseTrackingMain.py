import cv2
import time
import PoseTrackingModule as ptm


def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = ptm.poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPoses(img, draw=True)
        detector.findNose(img, draw=True)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
