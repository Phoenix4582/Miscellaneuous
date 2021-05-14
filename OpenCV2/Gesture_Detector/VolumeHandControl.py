import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Hyperparameters
wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]
minLength = 50
maxLength = 300
vol = 0
volBar = 400
volPer = 0


def getLength(img, lmList, pos1: int, pos2: int, show=False, draw=True) -> float:
    length = 0
    if len(lmList) != 0:
        if show:
            print(lmList[pos1], lmList[pos2])
        x1, y1 = lmList[pos1][1], lmList[pos1][2]
        x2, y2 = lmList[pos2][1], lmList[pos2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 255, 0), cv2.FILLED)
            # return x1, y1, x2, y2

        length = math.hypot(x2 - x1, y2 - y1)

    return length


def changeVolume(img, length: float, minVol: float, maxVol: float, draw=True):
    vol = np.interp(length, [minLength, maxLength], [minVol, maxVol])
    volBar = np.interp(length, [minLength, maxLength], [400, 150])
    volPer = np.interp(length, [minLength, maxLength], [0, 100])
    volume.SetMasterVolumeLevel(vol, None)
    if draw:
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 225, 0), 3)


if __name__ == '__main__':
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        # print(lmList)
        length = getLength(img, lmList, 4, 8)
        changeVolume(img, length, minVol, maxVol)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
