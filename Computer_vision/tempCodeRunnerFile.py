cv.imshow('img2',img2)
cv.imshow('img',img)
cv.waitKey(0)

img = cv.imread('images/picture_1.jpg')
img = cv.resize(img, (0,0), None, 0.3, 0.3)