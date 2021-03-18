# Before starting to write this code, we watched several Python tutorials
# We are not familiar with Python so naturally, we used some parts from the tutorials
# such as " cap = cv2.VideoCapture(0) " .
# Some parts can have few resemblance because of the chosen variable names etc.

# Add necessary libraries.
import os
import cv2
import numpy as np
import math
import time

# ----------------- Roadmap of the project ---------------------
# - Binarize the region of interest (roi=hand)
# - Convert to grayscale, blur to reduce/remove noise, threshold to binarize image
# - Find contours to get the list of boundary points around each blob
# - Find and draw the convex hull


def imageFiltering(frame):

    # region of interest (roi = hand)
    roi = frame[y:y + h, x:x + w]

    # applying gaussian blur to reduce the noise
    blur = cv2.GaussianBlur(roi, (5, 5), 0)
    # converting from coloured to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # applying a mask which makes skin color white and others black
    mask = cv2.inRange(hsv, np.array([2, 50, 50]), np.array([20, 255, 255]))

    kernel = np.ones((5, 5))
    # reducing noise
    filtered = cv2.GaussianBlur(mask, (3, 3), 0)
    ret, thresh = cv2.threshold(filtered, 127, 255, 0)  # thesholding the image
    thesh = cv2.GaussianBlur(thresh, (5, 5), 0)  # reducing the noise
    # finding contours in the image. Will be used later in complex hull algorithm
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return roi, thresh, contours


cap = cv2.VideoCapture(0)

# dimensions and coordinates of the box
x = 50
y = 50
w = 220
h = 220

while True:
    ret, frame = cap.read()  # read video frame by frame
    # create a rectangle around roi
    cv2.rectangle(frame, (y, x), (y + h, x + w), (0, 255, 0), 2)

    roi, thresh, contours = imageFiltering(frame)  # getting the filtered image

    # blank image which will be used to show the contours and defects
    drawing = np.zeros(roi.shape, np.uint8)
    try:
        # finding contour with max area
        contour = max(contours, key=lambda x: cv2.contourArea(x), default=0)

        # make convex hull around hand
        hull = cv2.convexHull(contour)

        # convex hull. This creates a convex polygon.
        areaCont = cv2.contourArea(contour)
        areaHull = cv2.contourArea(hull)

        areaRatio = ((areaHull - areaCont) / areaCont) * 100

        # draw contours
        cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

        # finding defects in the convex polygon formed using convex hull algorithm
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, hull)

        count_defects = 0  # defaults initially set to 0 (no defects)

        # finding defects and displaying them on the image
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]  # defect returns 4 arguments
            # using start, end, far to find the defects location
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])

            # finding the angle of the defect using cosine law
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

            # we know, angle between 2 fingers is within 90 degrees.
            # so anything greater than that isn;t considered
            if angle <= 90:
                count_defects += 1
                cv2.circle(drawing, far, 5, [0, 0, 255], -1)  # displaying defect

            cv2.line(drawing, start, end, [0, 255, 0], 2)

        count_defects += 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        if count_defects == 1:
            if areaCont < 2000:
                cv2.putText(frame, 'Put hand in the box', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            else:
                if areaRatio < 12:
                    cv2.putText(frame, "CHANNEL DOWN", (50, 50), font , 2, (0, 0, 255), 2)
                    os.system("irsend SEND_ONCE Samsung_TV KEY_CHANNELDOWN")
                    os.system("irsend SEND_ONCE Samsung_TV KEY_OK")
                elif areaRatio < 17.5:
                    cv2.putText(frame, "6", (50, 50), font , 2, (0, 0, 255), 2)
                    os.system("irsend SEND_ONCE Samsung_TV KEY_6")
                    os.system("irsend SEND_ONCE Samsung_TV KEY_OK")
                else:
                    cv2.putText(frame, '1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    os.system("irsend SEND_ONCE Samsung_TV KEY_1")
                    os.system("irsend SEND_ONCE Samsung_TV KEY_OK")


        elif count_defects == 2:
            cv2.putText(frame, "2", (5, 50), font, 2, (0, 0, 255), 2)
            os.system("irsend SEND_ONCE Samsung_TV KEY_2")
            os.system("irsend SEND_ONCE Samsung_TV KEY_OK")

        elif count_defects == 3:
            if areaRatio < 27:
                cv2.putText(frame, "3", (50, 50), font, 2, (0, 0, 255), 2)
                os.system("irsend SEND_ONCE Samsung_TV KEY_3")
                os.system("irsend SEND_ONCE Samsung_TV KEY_OK")
            else:
                # BEST OF LUCK GESTURE
                cv2.putText(frame, "CHANNEL UP", (50, 50), font, 2, (0, 0, 255), 2)
                os.system("irsend SEND_ONCE Samsung_TV KEY_CHANNELUP")
                os.system("irsend SEND_ONCE Samsung_TV KEY_OK")

        elif count_defects == 4:
            cv2.putText(frame, "4", (50, 50), font, 2, (0, 0, 255), 2)
            os.system("irsend SEND_ONCE Samsung_TV KEY_4")
            os.system("irsend SEND_ONCE Samsung_TV KEY_OK")

        elif count_defects == 5:
            cv2.putText(frame, '5', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            os.system("irsend SEND_ONCE Samsung_TV KEY_5")
            os.system("irsend SEND_ONCE Samsung_TV KEY_OK")

        elif count_defects == 6:
            cv2.putText(frame, 'reposition', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

        else:
            cv2.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

    except:
        pass
    # displaying result
    cv2.imshow("thresh", thresh)
    cv2.imshow("drawing", drawing)
    cv2.imshow("img", frame)

    k = cv2.waitKey(30) & 0xff  # exit if Esc is pressed
    if k == 27:
        break

cap.release()  # release the webcam
cv2.destroyAllWindows()  # destroy the window