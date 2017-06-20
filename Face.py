import sys, os
import cv2
import urllib
import shutil

from Tkinter import *
from os import walk
from urlparse import urlparse

class Face:

    def detect(self,path):
        img = cv2.imread(path)
        cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        rects = cascade.detectMultiScale(img, 1.01, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

        if len(rects) == 0:
            return [], img
        rects[:, 2:] += rects[:, :2]
        return rects, img

    def box(self,rects, img, file_name,folder):

        i = 0   #   Track how many faces found
        printLabel = "thisLabel"
        for x1, y1, x2, y2 in rects:
            i += 1  
            #   Increment the face counter
            #print "Found " + str(i) + " face!"  #   Tell us what's going on
            cut = img[y1:y2, x1:x2] #   Defines the rectangle containing a face
            file_name = file_name.replace('.jpg','_')   #   Prepare the filename 
            file_name = file_name + str(i) + '.jpg'
            file_name = file_name.replace('\n','')
            printLabel =  'Writing ' + file_name

            cv2.imwrite('detected/'+ str(folder)+'/'+ str(file_name), cut)   #   Write the file
        return printLabel
    
 
if __name__ == "__main__":
    main()