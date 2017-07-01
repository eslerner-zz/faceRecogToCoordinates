import cv2
import sys
import numpy as np

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret2, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierachy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    im3 = cv2.drawContours(im2, contours, -1, (0,255,0), int(.25))
    cv2.imwrite("image.bmp", im3)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
quit()