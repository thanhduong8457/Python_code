import numpy as np
import cv2
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, help="path to the input source image")
args = vars(ap.parse_args())

# load the source and reference images
print("[INFO] loading source images...")
img = cv2.imread(args["source"])

# img = cv2.imread('images/picture_1.jpg')
img = cv2.resize(img, (0,0), None, 0.3, 0.3)

# Apply Gamma=0.5 on the normalised image and then multiply by scaling constant (For 8 bit, c=255)
gamma_0_5 = np.array(255*(img/255)**0.5,dtype='uint8')

# Similarly, Apply Gamma=1
gamma_1 = np.array(255*(img/255)**1,dtype='uint8')

# Similarly, Apply Gamma=2
gamma_2 = np.array(255*(img/255)**2,dtype='uint8')

# Similarly, Apply Gamma=3
gamma_4 = np.array(255*(img/255)**4,dtype='uint8')

# Display the images in subplots
img1 = cv2.hconcat([gamma_0_5,gamma_1])
img2 = cv2.hconcat([gamma_2,gamma_4])

cv2.imshow('output_1_2',img1)
cv2.imshow('output_3_4',img2)

cv2.waitKey(0)
