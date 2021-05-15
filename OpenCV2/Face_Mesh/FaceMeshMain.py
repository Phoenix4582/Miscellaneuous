import cv2
import FaceMeshModule as fmm
import time


def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = fmm.MeshDetector()

    while True:
        success, img = cap.read()
        img = detector.findMesh(img, draw=True)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("FaceMesh", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
