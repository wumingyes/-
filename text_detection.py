from imutils.object_detection import non_max_suppression
import imutils
import numpy as np
import argparse
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",type=str,help="path to input image")
ap.add_argument("-east","--east",type=str,help="path to input EAST text detector")
ap.add_argument("-c","--min-confidence",type=float,default=0.5,help=
    "minimum probability required to inspect a region")
ap.add_argument("-w","--width",type=int,default=320,
    help="resized image width (should be multiple of 32")
ap.add_argument("-e","--height",type=int,default=320,
    help="resized image height (should be multiple of 32)")
args = vars(ap.parse_args())
print(args)

image = cv2.imread(r"D:/python/others/20200308115400_4.jpg")
orig = image.copy()
(h,w) = image.shape[:2]
(neww,newh) = (args["width"],args["height"])
rw = w/float(neww)
rh = h/float(newh)
hsv = cv2.cvtColor(orig,cv2.COLOR_BGR2HSV)
cv2.imshow('hsv',hsv)
lower_blue = np.array([242,242,158])
upper_blue = np.array([213,127,85])

mask = cv2.inRange(orig,lower_blue,upper_blue)
res = cv2.bitwise_and(orig,orig,mask=mask)

cv2.imshow('orig',orig)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
# image = imutils.resize(image,width = 320)
# (h,w) = image.shape[:2]
# cv2.imshow('resized',image)
# gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# skeleton = imutils.skeletonize(gray,size=(13,13))
# cv2.imshow("skeleton",skeleton)
# plt.imshow(imutils.opencv2matplotlib(image))
# edgeMap = imutils.auto_canny(gray)
# cv2.imshow('edgeMap',edgeMap)
# cv2.imshow('orig',orig)
# crop = orig[123:345,234:400]
# cv2.imshow('crop',crop)
cv2.waitKey(0)


