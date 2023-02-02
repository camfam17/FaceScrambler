import cv2 as cv
import random

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')


blank = cv.imread('face3.jpg')
img = blank.copy()
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('img', img)

face_rect = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5) # shrink rectangle width for tighter fit
print('face_rect', face_rect)

x, y, w, h = face_rect[0]


x /= 3
x = int(x)
x *= 3
y /= 3
y = int(y)
y *= 3

cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 10)
cv.imshow('img2', img)

face_roi = img[y:(y+h), x:(x+w)]
# cv.imshow('face', face_roi)


# img3 = img.copy()
# img3[0:h, 0:w] = face_roi
# cv.imshow('faceroi', img3)


# generalize this section to create p^2 blocks where p = 3,4,5 etc
block_width = int(w/3)
block_height = int(h/3)
blocks = []
for i in range(3):
		for j in range(3): # may need to flip x, y coordinates in img[] especially if the face rectangle stops being a square
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

# shuffle the set 1, 2, 3, ... ,8, 9
nums = [num for num in range(0, 9)]
shuffle = []
while len(nums) > 0:
	rand = random.randrange(0, len(nums))
	shuffle.append(nums.pop(rand))

print('shuffle', shuffle)

# turn that 1x9 array into 3x3 matrix
shuffle_mat = []
for i in range(0, 7, 3):
	shuffle_mat.append(shuffle[i:i+3])
print('shuffle_mat', shuffle_mat)

shuffle_blocks = []
for i in range(3):
	for j in range(3):
		shuffle_blocks.append(blocks[shuffle_mat[i][j]])
print('shuffle_blocks', shuffle_blocks)

img5 = blank.copy()
img6 = blank.copy()

# # for block in shuffle_blocks:
# 	img5[block[0]:block[0]+block_width, block[1]:block[1]+block_height] = img6[block[0]:block[0]+block_width, block[1]:block[1]+block_height]

k = 0
for i in range(3):
	for j in range(3): # may need to flip x, y coordinates in img[] especially if the face rectangle stops being a square
		# img5[x+i*block_width:x+(i*block_width)+block_width, y+j*block_height:y+(j*block_height)+block_height] = img6[shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width, shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height]
		# img5[y+j*block_height:y+(j*block_height)+block_height, x+i*block_width:x+(i*block_width)+block_width] = img6[shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width, shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height]
		img5[y+j*block_height:y+(j*block_height)+block_height, x+i*block_width:x+(i*block_width)+block_width] = img6[shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height, shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width]
		k += 1

cv.imshow('scrambe', img5)

cv.waitKey(0)
cv.destroyAllWindows()

# TODO
# custom number of blocks
# shrink rectangle
# error catrch if no face found
# ability to scramble multiple faces in one image
# take picture with webcam
# take live video with webcam with real time scrambling
# use arrow keys to shift face rectangle around a bit for user to centre it on the face