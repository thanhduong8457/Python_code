import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('images/picture_1.jpg')
img = cv2.resize(img, (0,0), None, 0.3, 0.3)

hist,bins = np.histogram(img.flatten(),256,[0,256])
cdf = hist.cumsum()

cdf_normalized = cdf * float(hist.max()) / cdf.max()
plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')


cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
cdf = np.ma.filled(cdf_m,0).astype('uint8')

img2 = cdf[img]

equ = cv2.equalizeHist(img2)
res = np.hstack((img,equ)) #stacking images side-by-side
cv2.imshow('res.png',res)
cv2.waitKey(0)