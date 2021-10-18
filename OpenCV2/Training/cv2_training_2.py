import cv2
import numpy as np

# SIMPLE FUNCTIONS IN CV2
img = cv2.imread("Resources/example.png")
kernel = np.ones((5, 5), dtype = np.uint8)

# YOU MAY PLAY WITH THE PARAMETERS
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7), 0)
imgCanny = cv2.Canny(img, 100, 100)
imgDilation = cv2.dilate(imgCanny, kernel, iterations=3)
imgEroded = cv2.erode(imgDilation, kernel, iterations=1)

cv2.imshow("Gray Image", imgGray)
cv2.imshow("Blur Image", imgBlur)
cv2.imshow("Canny Image", imgCanny)
cv2.imshow("Dilated Image", imgDilation)
cv2.imshow("Eroded Image", imgEroded)


cv2.waitKey(0)