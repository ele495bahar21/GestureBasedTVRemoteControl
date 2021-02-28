# Real Time TV Control with Specified Sign Language Commands
# TOBB ETU EEE Spring Project - February 2021
# Group 6 - BND & ABV
# Buse Nur Düzgün - 161201052
# Ahmet Berk Vıcıl - 161201069

# Code for creating our own dataset

# import necessary libraries:
import numpy as np
import cv2
import os
import time

def nothing(x):
    pass


# Create a new directory for dataset:
def newFolder(commandName):
    if not os.path.exists('./handGestures/train/' + commandName):
        os.mkdir('./handGestures/train/' + commandName)
    if not os.path.exists('./handGestures/test/' + commandName):
        os.mkdir('./handGestures/test/' + commandName)


# Capture images for the created dataset directory:
def captureImages(commandName):
    newFolder(str(commandName))

# If you have only 1 camera, the index would be '0' for VideoCapture.
# Search for camera ID if there are cameras more than 1.
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Video")


# Create a trackbar to adjust HSV values to segment hand color of the user.
    cv2.namedWindow("HSV Trackbars")
    cv2.createTrackbar("L - H", "HSV Trackbars", 0, 179, nothing)
    cv2.createTrackbar("L - S", "HSV Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - V", "HSV Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - H", "HSV Trackbars", 179, 179, nothing)
    cv2.createTrackbar("U - S", "HSV Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - V", "HSV Trackbars", 255, 255, nothing)

    listImage = [1, 2, 3, 4, 5]
    for loop in listImage:
        while True:
            # Read & Flip captured video.
            ret, frame = cap.read()
            frame = cv2.flip(frame,1)

            lowerHue = cv2.getTrackbarPos("L - H", "HSV Trackbars")
            lowerSaturation = cv2.getTrackbarPos("L - S", "HSV Trackbars")
            lowerValue = cv2.getTrackbarPos("L - V", "HSV Trackbars")
            upperHue = cv2.getTrackbarPos("U - H", "HSV Trackbars")
            upperSaturation = cv2.getTrackbarPos("U - S", "HSV Trackbars")
            upperValue = cv2.getTrackbarPos("U - V", "HSV Trackbars")

            # Starting coordinate, here (425, 100)
            startPoint = (425, 100)
            # Ending coordinate, here (625, 300)
            endPoint = (625, 300)
            # Green color in BGR
            color = (0, 255, 0)
            # Line thickness of 2 px
            thickness = 2

            # Draws a simple, thick or filled up-right rectangle.
            # Further info: https://docs.opencv.org/3.4/d6/d6e/group__imgproc__draw.html
            img = cv2.rectangle(frame, startPoint, endPoint, color, thickness, lineType=8, shift=0)

            lowerBlue = np.array([lowerHue, lowerSaturation, lowerValue])
            upperBlue = np.array([upperHue, upperSaturation, upperValue])
            croppedImage = img[102:298, 427:623]

            hsvImg = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2HSV)
            maskedImg = cv2.inRange(hsvImg, lowerBlue, upperBlue)
            finalImg = cv2.bitwise_and(croppedImage, croppedImage, mask=maskedImg)

            # We will categorize collected images in 'test' and 'train' folders.
            # For testing, we will use 50 images.
            # For training we will use 450 images.
            # Training images can be more, it's upto the users (us).
            # We didn't restricted our code's training part to feel free to create dataset
            # as many as we wanted in the future, for the possible lack of accuracy.
            imgCount = 0
            tCount = 1
            trainingImageName = 1
            testImageName = 1

            # Print captured data numbers on video and show it with final and masked videos.
            # font:
            font = cv2.FONT_HERSHEY_DUPLEX
            # org:
            org = (30, 400)
            cv2.putText(frame, str(imgCount), org, font, fontScale=1.5, color=(0, 0, 255))
            cv2.imshow("Final", finalImg)
            cv2.imshow("Video", frame)
            cv2.imshow("Masked", maskedImg)



            # To capture hand gestures, get the position you want and press 'c'.
            if cv2.waitKey(1) == ord('c'):
                if tCount <= 350:
                    imgX, imgY = 64, 64

                    # Resize and save captured images in training dataset.
                    # Image names will start from '1.png' and increase with each pressed 'c' button.
                    imageName = "./handGestures/train/" +str(commandName) + "/{}.png".format(trainingImageName)
                    saveImage = cv2.resize(maskedImg, (imgX, imgY))
                    cv2.imwrite(imageName, saveImage)

                    # Control step
                    print("{} captured".format(imageName))

                    trainingImageName += 1

                if tCount > 350 and tCount <= 400:
                    imageName = "./handGestures/test/" +str(commandName) + "/{}.png".format(testImageName)
                    saveImage = cv2.resize(maskedImg, (imgX, imgY))
                    cv2.imwrite(imageName, saveImage)

                    # Control step
                    print("{} captured".format(imageName))

                    testImageName += 1

                    if testImageName > 250:
                        break

                tCount += 1

                if tCount == 401:
                    tCount = 1
                imgCount += 1

            elif cv2.waitKey(1) == 27:
                break
        if testImageName > 250:
            break

    cap.release()
    cv2.destroyAllWindows()
commandName = input("Enter command name: ")
captureImages(commandName)






################################################
################################################

"""
# import libraries
import numpy as np
import cv2
import os
import time
import uuid
# import preprocess as ipu    # ipu:image pre-process

IMG_PATH_1 = 'handGestures/workspace/images/collectedimages'
command_labels = ['Welcome!', 'See You!', 'Volume Up', 'Volume Down', 'Next Channel', 'Previous Channel']

IMG_PATH_2 = 'handGestures/workspace/images/collectedimages'
number_labels = ['1', '2', '3', '4', '5', '6']

# pose numbers we're gonna collect when we collect our images:
img_numbers = 15

exit = '**'

try:
    os.mkdir(IMG_PATH_1)
except:
    print('Directory already exists!')

sub_IMG_PATH_1 = input('Enter sub directory name or press ** to exit: ')

if sub_IMG_PATH_1 == exit:
    print('exit')
else:
    path1 = IMG_PATH_1 + '/'+ sub_IMG_PATH_1+ '/'
    try:
        os.mkdir(path1)
    except:
        print('Sub directory already exists!')

camera = cv2.VideoCapture(0)
print('Now camera window will be open, then \n')
print('1) Place your hand gesture in ROI and press c key to start capturing images. \n')
print('2) Press esc key to exit.')

count = 0

for label1 in command_labels:
    os.mkdir('handGestures\workspace\images\collectedimages\\'+label1)
    captureVid = cv2.VideoCapture(0)
    print('Collecting images for {}'.format(label1))
    # wait 5s to capture image in another position
    time.sleep(5)
    for imageNums in range(img_numbers):
        ret, frame = captureVid.read()
        img_name = os.path.join(IMG_PATH_1, label1, label1+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(img_name, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    captureVid.release()

"""
