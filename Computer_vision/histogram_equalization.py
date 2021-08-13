import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('images/Capture.PNG')
img = cv2.resize(img, (0,0), None, 0.5, 0.5)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

equa = cv2.equalizeHist(img)
res = np.hstack((img,equa))
cv2.imshow('output',res)
cv2.waitKey(0)

hist,bins = np.histogram(equa.flatten(),256,[0,256])
cdf = hist.cumsum()
cdf_normalized = cdf * float(hist.max()) / cdf.max()
plt.plot(cdf_normalized, color = 'b')
plt.hist(equa.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()