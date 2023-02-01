import cv2 as cv
import random

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')


img = cv.imread('face1.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('img', img)
cv.imshow('gray', gray)

face_rect = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5) # shrink rectangle width for tighter fit
print(face_rect)

x, y, w, h = face_rect[0]


cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 10)
cv.imshow('img2', img)

face_roi = img[y:(y+h), x:(x+w)]
cv.imshow('face', face_roi)


img3 = img.copy()

img3[0:h, 0:w] = face_roi
cv.imshow('faceroi', img3)

# generalize this section to create p^2 blocks where p = 3,4,5 etc
block_width = int(w/3)
block_height = int(h/3)
blocks = []
for i in range(3):
		for j in range(3):
			blocks.append((int(x + (i*block_width)), int(y + (j*block_height))))
print(blocks)

img4 = img.copy()
for block in blocks:
	cv.rectangle(img4, (block[0], block[1]), (block[0]+block_width, block[1]+block_height), (0, 255, 0), 4)
cv.imshow('img4', img4)


# shuffle = []
# while True:
	
# 	rand = random.randrange(1, 10)
	
# 	if rand not in shuffle:
# 		shuffle.append(rand)
	
# 	if len(shuffle) == 9:
# 		break

# print(shuffle)


nums = [1, 2, 3, 4, 5, 6 ,7, 8, 9]
shuffle = []
while len(nums) > 0:
	rand = random.randrange(0, len(nums))
	shuffle.append(nums.pop(rand))

print('shuffle', shuffle)

# for i in range(3):
# 	shuffle_mat[i][0:3] = shuffle[]

# shuffle_mat[0][0:3] = shuffle[0:3]
# shuffle_mat[1][0:3] = shuffle[3:6]
# shuffle_mat[2][0:3] = shuffle[6:9]

shuffle_mat = []
shuffle_mat.append(shuffle[0:3])
shuffle_mat.append(shuffle[3:6])
shuffle_mat.append(shuffle[6:9])
print(shuffle_mat)

cv.waitKey(0)
cv.destroyAllWindows()