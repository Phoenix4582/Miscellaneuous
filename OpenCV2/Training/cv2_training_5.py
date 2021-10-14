import cv2
import numpy as np

# PERSPECTIVE WARPPING
img = cv2.imread("example.png")
points1 = np.float32([[coor1_x, coor1_y],[coor2_x, coor2_y],[coor3_x, coor3_y],[coor4_x, coor4_y]])
points2 = np.float32([[0, 0],[width, 0],[0, height],[width, height]])
matrix = cv2.getPerspectiveTransform(points1, points2)
imgWarpped = cv2.warpPerspective(img, matrix, (width, height))

cv2.imshow("Image", img)
cv2.imshow("Warpped Image", imgWarpped)
cv2.waitKey(0)
