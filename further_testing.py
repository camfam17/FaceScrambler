import cv2 as cv
import random

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
blocks_num = 3

blank = cv.imread('face3.jpg')
img = blank.copy()
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

face_rect = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5) # shrink rectangle width for tighter fit
print('face_rect', face_rect)

x, y, w, h = face_rect[0]

x /= blocks_num
x = int(x)
x *= blocks_num
y /= blocks_num
y = int(y)
y *= blocks_num

cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 10)
cv.imshow('img2', img)

block_width = int(w/blocks_num)
block_height = int(h/blocks_num)

blocks = []
for i in range(blocks_num):
		for j in range(blocks_num): # may need to flip x, y coordinates in img[] especially if the face rectangle stops being a square
			blocks.append((x + (i*block_width), y + (j*block_height)))
			# blocks.append((y + (j*block_height), x + (i*block_width)))
print('blocks', blocks)

img4 = img.copy()
for block in blocks:
	cv.rectangle(img4, (block[0], block[1]), (block[0]+block_width, block[1]+block_height), (0, 255, 0), 4)
	# cv.addText(img4, str(block[0]) + ':' + str(block[0]+block_width) + ', ' + str(block[1]) + ':' + str(block[1]+block_height), (block[0]+int(block_width/2), block[1]+int(block_height/2)), 'arial')
	# cv.putText(img=img4, text=str(block[0]) + ':' + str(block[0]+block_width) + ', ' + str(block[1]) + ':' + str(block[1]+block_height), org=(block[0]+int(block_width/200), block[1]+int(block_height/3)), fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.5, color=(255, 0, 255, 255), thickness=1, bottomLeftOrigin=False)
	cv.putText(img=img4, text=str(block[1]) + ':' + str(block[1]+block_height), org=(block[0]+int(block_width/100), block[1]+int(block_height/2)), fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.7, color=(255, 0, 255, 255), thickness=1, bottomLeftOrigin=False)
	cv.putText(img=img4, text=str(block[0]) + ':' + str(block[0]+block_width) + ', ', org=(block[0]+int(block_width/100), block[1]+int(block_height/3)), fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.7, color=(255, 0, 255, 255), thickness=1, bottomLeftOrigin=False)
cv.imshow('img4', img4)