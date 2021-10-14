import cv2
import numpy as np

# RESIZING AND CROPPING TECHNIQUES
img = cv2.imread("Resources/example.png")
# print(img.shape)

# CHANGE THE SIZE AS YOU WISH
imgResized = cv2.resize(img, (640, 480))
imgCropped = img[h_start:h_end, w_start: w_end]

cv2.imshow("Example", img)
cv2.imshow("Resized Example", imgResized)
cv2.imshow("Cropped Example", imageCropped)

cv2.waitKey(0)
