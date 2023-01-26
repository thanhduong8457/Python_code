import cv2
import numpy as np
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, help="path to the input source image")
args = vars(ap.parse_args())

# load the source and reference images
print("[INFO] loading source images...")
img = cv2.imread(args["source"])

# img = cv2.imread('images/picture_1.jpg')
img = cv2.resize(img, (0, 0), None, 0.3, 0.3)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# To ascertain total numbers of rows and columns of the image, size of the image
m, n = img.shape

# To find the maximum grey level value in the image
L = img.max()

# Maximum grey level value  minus the original image gives the negative image
img_neg = L-img

# Display the images in subplots
img1 = cv2.hconcat([img, img_neg])
cv2.imshow('Negative', img1)

cv2.waitKey(0)
