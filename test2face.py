import cv2 as cv
import random



def shuffle_blocks1(blocks, shuffle_mat):
	shuffle_blocks = []
	for i in range(blocks_num):
		for j in range(blocks_num):
			shuffle_blocks.append(blocks[shuffle_mat[i][j]])
	print('shuffle_blocks', shuffle_blocks)
	
	return shuffle_blocks

def get_shuffle_mat():
	
	# shuffle the set 0, 1, 2, ... ,blocks_num^2 - 1
	nums = [num for num in range(0, pow(blocks_num, 2))]
	shuffle = []
	while len(nums) > 0:
		rand = random.randrange(0, len(nums))
		if nums[rand] != len(shuffle):
			shuffle.append(nums.pop(rand))
	# IDEA: place limits on the above output to ensure no block is in its original place and no two neighbouring blocks are still neighbouring each other on the same side
	print('shuffle', shuffle)

	# turn that 1xblock_nums2 array into block_nums-x-block_nums matrix
	shuffle_mat = []
	for i in range(0, pow(blocks_num, 2)-2, blocks_num):
		x = i
		y = i+blocks_num
		shuffle_mat.append(shuffle[x:y])
		# shuffle_mat.append(shuffle[i:i+blocks_num])
	print('shuffle_mat', shuffle_mat)
	
	return shuffle_mat



def get_blocks(x, y, block_width, block_height):
	blocks = []
	for i in range(blocks_num):
			for j in range(blocks_num): # may need to flip x, y coordinates in img[] especially if the face rectangle stops being a square
				blocks.append((x + (i*block_width), y + (j*block_height)))
				# blocks.append((y + (j*block_height), x + (i*block_width)))
	print('blocks', blocks)
	
	return blocks


if __name__ == '__main__':
	face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
	blocks_num = 3

	blank = cv.imread('faces3.jpg')
	# blank = cv.resize(blank, (0, 0), fx=0.5, fy=0.5)
	img = blank.copy()
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	face_rect = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5) # shrink rectangle width for tighter fit
	print('face_rect', face_rect)



	img5 = blank.copy()
	img6 = blank.copy()
	
	# shuffle_blocks_list = []
	for x, y, w, h in face_rect:
		
		block_width = int(w/blocks_num)
		block_height = int(h/blocks_num)
		
		blocks = get_blocks(x, y, block_width, block_height)
		
		shuffle_mat = get_shuffle_mat()
		
		# shuffle_blocks_list.append(shuffle_blocks(blocks, shuffle_mat))
		
		shuffle_blocks = shuffle_blocks1(blocks, shuffle_mat)
		k = 0
		for i in range(blocks_num):
			for j in range(blocks_num): # may need to flip x, y coordinates in img[] especially if the face rectangle stops being a square
				# img5[x+i*block_width:x+(i*block_width)+block_width, y+j*block_height:y+(j*block_height)+block_height] = img6[shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width, shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height]
				# img5[y+j*block_height:y+(j*block_height)+block_height, x+i*block_width:x+(i*block_width)+block_width] = img6[shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width, shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height]
				img5[y+j*block_height:y+(j*block_height)+block_height, x+i*block_width:x+(i*block_width)+block_width] = img6[shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height, shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width]
				k += 1

	cv.imshow('scramble', img5)

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
# reshuffle button to scramble the blocks differently
# ability to ensure two adjacent blocks (before shuffling) don't end up in the same position relative to each other after shuffling
# i.e make sure blocks are sufficiently scrambled