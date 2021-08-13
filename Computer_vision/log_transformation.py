import cv2
import numpy as np
   
# Read an image
img = cv2.imread('images/picture_1.jpg')
img = cv2.resize(img, (0,0), None, 0.5, 0.5)
   
# Apply log transformation method
c = 255 / np.log(1 + np.max(img))
log_image = c * (np.log(img + 1))
   
# Specify the data type so that
# float value will be converted to int
log_image = np.array(log_image, dtype = np.uint8)
   
# Display both images
cv2.imshow('img',img)
cv2.imshow('log_img',log_image)
cv2.waitKey(0)
