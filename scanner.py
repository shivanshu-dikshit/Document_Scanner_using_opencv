#execute the whole code from top to bottom there is a function name as scanner and after executing it can be 
#with the name of the image as argument and the results can be visualized

import numpy as np
import cv2

def rectify(tod):
    tod = tod.reshape((4,2))
    tod_new = np.zeros((4,2),dtype = np.float32)

    add = tod.sum(1)
    tod_new[0] = tod[np.argmin(add)]
    tod_new[2] = tod[np.argmax(add)]

    diff = np.diff(tod,axis = 1)
    tod_new[1] = tod[np.argmin(diff)]
    tod_new[3] = tod[np.argmax(diff)]

    return tod_new
    
    
def scanner(image):
    """
    scanner object must be called with scanner('file_name.jpg')
    and if the file is not in the working directory then along 
    with proper path
    """
#first of all importing the image which is to be processed and then resizing it to a particular size so that further
#operations can be done

    img = cv2.imread(image)
    img = cv2.resize(img, (800,800))
    cv2.imshow('original', img)
    cv2.waitKey()
    cv2.destroyAllWindows()

#there after applying blurring in order to reduce any kind of noise present in the image
#and apply canny edges in order to detect the edges prsent in the image

    blur = cv2.GaussianBlur(img, (5,5), 0)
    #edges = cv2.Canny(blur, 0, 50)
    edges = cv2.Canny(blur, 60, 180)
    cv2.imshow('original', edges)
    cv2.waitKey()
    cv2.destroyAllWindows()

#there after using the cv2's find contour function in order to get the boundary of the various objects prsent in the 
#image
    
    _, cnt, hier = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(cnt, key = cv2.contourArea, reverse = True)

#there after using the arc length frunction in order to process over the detected countours and the
#retrieving only those which have 4 sides 
#like the document we want to detect
    
    for c in contours:
        p = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*p, True)
    
        if len(approx)==4:
            target = approx
            break

#visualizing the document we detcted in the image and the boundary around the document
   
    cv2.drawContours(img, [target], 0,(0, 255, 0), 3)
    cv2.imshow("Outline", img)
    cv2.imwrite('contour.jpg', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#there after applying the perspective transform in order to get a top down look of the document taht is 90 degree from
#top by defining a new mapping for the pixels
    
    approx = rectify(target)
    pts2 = np.float32([[0,0],[800,0],[800,800],[0,800]])

    M = cv2.getPerspectiveTransform(approx,pts2)
    dst = cv2.warpPerspective(img,M,(800,800))

    cv2.drawContours(img, [target], -1, (0, 255, 0), 2)
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    
##applying thresholding to get the content of the image  various methods are provided so that the best oes an be chosed
    
    ret,th1 = cv2.threshold(dst,125,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(dst,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(dst,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    ret2,th4 = cv2.threshold(dst,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#visualizing the results
    
    cv2.imshow("Thresh Binary.jpg", th1)
    cv2.imshow("Thresh mean.jpg", th2)
    cv2.imshow("Thresh gauss.jpg", th3)
    cv2.imshow("Otsu's.jpg", th4)
    cv2.imshow("dst.jpg", dst)
    cv2.waitKey()
    cv2.destroyAllWindows()


#calling the function by providing image as an argument in " name of file.jpg "
scanner('desk.jpg')