import cv2

# LOAD IMAGES AND VIDEOS
image_url = "https://axiom-verge.fandom.com/wiki/Map?file=The_ultimate_Axiom_Verge_Map.png"

img = cv2.imread(image_url)

cv2.imshow("Title", img)
cv2.waitkey(0)

video_url = "http://godh.keruisizhiye.com/fgo/FGOseason_2.mp4"
cap = cv2.VideoCapture(video_url)

# cap = cv2.VideoCapture(0) # capture laptop camera
# cap.set(3, 640) # set width
# cap.set(4, 480) # set height
while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitkey(1) & 0xFF == ord('q'):
        break
