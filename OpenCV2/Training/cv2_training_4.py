import cv2
import numpy as np

# DRAW SHAPES AND TEXTS

img = np.zeros((512, 512, 3), np.uint8)
# FILL COLOR IN SELECTED SECTIONS
img[start_x:end_x, start_y:end_y] = 255, 0, 0

cv2.line(img, (start_x, start_y), (end_x, start_y), (color), linewidth)
cv2.rectangle(img, (start_x, start_y), (end_x, start_y), (color), cv2.FILLED)
cv2.circle(img, (center_x, center_y), radius, (color), linewidth)
cv2.putText(img, "TEXT YOU WISH TO SHOW", (start_x, start_y), cv2.FONT_HERSHEY_COMPLEX, SCALE, (COLOR), THICKNESS)


cv2.imshow("Image", img)
cv2.waitKey(0)
