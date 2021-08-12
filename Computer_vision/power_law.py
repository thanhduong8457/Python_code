import numpy as np
import cv2
# Load the image
img = cv2.imread('images/picture_1.jpg')
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