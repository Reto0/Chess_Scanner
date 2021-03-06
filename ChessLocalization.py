import cv2
import numpy as np
import os
import random 
import string
import time

def cropBorder(img, lines, type):
    dims = img.shape
    minX = float('inf')
    maxX = float('-inf')
    minY = float('inf')
    maxY = float('-inf')
    for line in lines:
        for x1, y1, x2, y2 in line:
            if(x1 < minX):
                minX = x1
            if(x2 < minX):
                minX = x2
            if(x1 > maxX):
                maxX = x1
            if(x2 > maxX):
                maxX = x2
            if(y1 < minY):
                minY = y1
            if(y2 < minY):
                minY = y2
            if(y1 > maxY):
                maxY = y1
            if(y2 > maxY):
                maxY = y2 
    # if(type == 0 or type == 1):
    #     if(minY > 1): 
    #         minY = minY-1
    #     if(minX > 1): 
    #         minX = minX-1
    #     if(dims[1] > maxX + 1): 
    #         maxX = maxX + 1
    #     if(dims[0] > maxY + 1): 
    #         maxY = maxY + 1
    crop = img[minY:maxY, minX:maxX]
    return crop



def localization(img):
    scriptDir = os.path.dirname(__file__)

    img_blur = cv2.GaussianBlur(img,(7,7),0)

    gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)


    # ret, thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    # cv2.imshow("temp", thresh1)
    dims = gray.shape
    # crop_r = img
    # crop_img = edges
    crop_r = img[130:dims[0]-40,500:dims[1]-590]
    crop_img = gray[130:dims[0]-40,500:dims[1]-590]
    
    edges = cv2.Canny(crop_img,80,200)
    # cv2.imshow("gray",gray)
    # cv2.imshow("edges",edges)
    # edges = cv2.Canny(crop_img,0,50,apertureSize = 3)
    # edges = cv2.Canny(crop_img,100,200)


    lines = cv2.HoughLinesP(edges,1,np.pi/180,15,50,20,20)
    # for line in lines:
    #     for x1,y1,x2,y2 in line:
    #         cv2.line(crop_r,(x1,y1),(x2,y2),(255,0,0),2)
    cannyPath = os.path.join(scriptDir, 'images/canny.png')
    cv2.imwrite(cannyPath, edges)
    crop_r_path = os.path.join(scriptDir, 'images/crop_r.png')
    cv2.imwrite(crop_r_path, crop_r)

    # cv2.imshow("temp-1", img)
    # cv2.imshow("temp",crop_img)
    # cv2.imshow("temp2", crop_r)
    # cv2.waitKey(0)
    # return crop_r

    crop = cropBorder(crop_r, lines, 0)
    dims = crop.shape
    crop = crop[10:dims[0]-10,10:dims[1]-10]
    img_blur = cv2.GaussianBlur(crop,(7,7),0)
    gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    # cv2.imshow("edge2", edges)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,15,50,50,10)
    # lines = cv2.HoughLinesP(edges,1,np.pi/180,15,50,300,20)
    # for line in lines:
    #     for x1,y1,x2,y2 in line:
    #         cv2.line(crop,(x1,y1),(x2,y2),(255,0,0),1)
    crop2 = cropBorder(crop, lines, 1)
    # cv2.imshow("1", crop)
    # cv2.imshow("2", crop2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return crop2


def get_random_name():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(20))
    return result_str

def dice(img):
    scriptDir = os.path.dirname(__file__)
    path = os.path.join(scriptDir,'dataset/Train')
    #path = os.path.join(scriptDir, 'dataset/Validation')
    print(path)
    dims = img.shape
    y = dims[0]//8
    x = dims[0]//8

    curX = 0
    curY = 0
    for i in range(8):
        for j in range(8): 
            print(str(i) + " " + str(j))
            cv2.imshow(str(i*8+j+1), img[curY:curY+y, curX:curX+x])
            # time.sleep(3)
            # piece = input("Enter the type: ")
            piece = "nothing"
            path2 = os.path.join(path, str(piece))
            path2 = os.path.join(path2, str(get_random_name()) + '.png')
            cv2.imwrite(path2, img[curY:curY+y, curX:curX+x])
            cv2.destroyAllWindows()
            curX += x
        curX = 0
        curY += y
    
    cv2.waitKey(0)
    return img