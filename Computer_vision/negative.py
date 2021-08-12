import cv2
import numpy as np
img = cv2.imread('images/picture_1.jpg')
img = cv2.resize(img, (0,0), None, 0.3, 0.3)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# To ascertain total numbers of rows and columns of the image, size of the image
m,n = img.shape
# To find the maximum grey level value in the image
L = img.max()
# Maximum grey level value  minus the original image gives the negative image
img_neg = L-img
# Display the images in subplots
img1 = cv2.hconcat([img,img_neg])
cv2.imshow('Negative', img1)
cv2.waitKey(0)