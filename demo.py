import cv2
import os
import numpy as np
from PIL import Image
url = 'http://192.168.0.101:8080/video'
cap = cv2.VideoCapture(url)
ret = True
f1=0
i=0
circles = np.zeros((4, 2), np.int)
counter = 0
while ret:
    ret, frame = cap.read()
    if f1==0:
        print("press s to scan")
        f1=f1+1

    cv2.imshow('camera feed',frame)
    k=cv2.waitKey(1)
    if k==ord('s'):
        cv2.destroyWindow("camera feed")
        cv2.imshow("scanned photo",frame)
        print("press u if unreadable")
        print("press b for black and white")
        print("press c to detect original document")
        k=cv2.waitKey(0)
        if k==ord('u'):
            cv2.destroyWindow('Scanned photo')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            new=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,155,1)
            cv2.imwrite("/Users/subhadey/Desktop/pdf/scanned%d.jpeg"%i,new)
            i=i+1
            print("press 'q' to crop and quit")
            continue

        elif k == ord('b'):
            cv2.destroyWindow('Scanned photo')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("/Users/subhadey/Desktop/pdf/scanned%d.jpeg"%i,gray)
            i = i + 1

            print("press 'q' to crop and quit")
            continue

        elif k == ord('c'):
            cv2.destroyWindow('Scanned photo')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 30, 200)
            contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


            def biggestRectangle(contours):  #document detection
                biggest = None
                max_area = 0
                indexReturn = -1
                for index in range(len(contours)):
                    i = contours[index]
                    area = cv2.contourArea(i)
                    if area > 10000:
                        peri = cv2.arcLength(i, True)
                        approx = cv2.approxPolyDP(i, 0.1 * peri, True)
                        if area > max_area and len(approx)==4:
                            biggest = approx
                            max_area = area
                            indexReturn = index
                return indexReturn
            indexReturn = biggestRectangle(contours)
            hull = cv2.convexHull(contours[indexReturn])
            cv2.imwrite("/Users/subhadey/Desktop/pdf/scanned%d.jpeg" % i, cv2.drawContours(frame, [hull], 0, (0, 255, 0), 3))
            i = i + 1
            print("press 'q' to crop and quit")
            continue

    elif k==ord('q'):
        ret=False
        break


#cropping the image

def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:

        circles[counter] = x, y
        counter = counter + 1
        print(circles)


img = cv2.imread("/Users/subhadey/Desktop/pdf/scanned%d.jpeg"%(i-1))
while True:

    if counter == 4:
        width, height = 500, 500
        pts1 = np.float32([circles[0], circles[1], circles[3], circles[2]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgOutput = cv2.warpPerspective(img, matrix, (width, height))
        cv2.imshow("press q to save and exit ", imgOutput)

    for x in range(0, 4):
        cv2.circle(img, (circles[x][0], circles[x][1]),
                   3, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Original Image ", img)
    cv2.setMouseCallback("Original Image ", mousePoints)
    if(cv2.waitKey(1) == ord('q')):
        print("saving and quitting")
        cv2.imwrite("/Users/subhadey/Desktop/pdf/scanned%d.jpeg" % (i-1),imgOutput)
        break

cv2.destroyAllWindows()
imagelist = os.listdir("/Users/subhadey/Desktop/pdf")
for image in imagelist:

    image = Image.open(r'/Users/subhadey/Desktop/pdf/scanned%d.jpeg'%(i-1))
    im1 = image.convert('RGB')
    im1.save(r'/Users/subhadey/Desktop/your_file.pdf')
