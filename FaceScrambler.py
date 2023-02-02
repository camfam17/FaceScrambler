import cv2 as cv
import random


face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
blocks_num = 3


class FaceScrambler():
	
	def __init__(self, file='faces2.jpg'):
		
		blank = cv.imread(file)
		# blank = cv.resize(blank, (0, 0), fx=0.5, fy=0.5)
		blank = cv.resize(blank, self.smart_dimensions(blank.shape, 1000, 1000))
		img = blank.copy()
		gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
		
		face_rects = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5) # shrink rectangle width for tighter fit
		print('Number of faces detected:', len(face_rects))
		print('face_rects', face_rects)
		
		scram = self.scramble_faces(blank, face_rects)
		
		cv.imshow('scramble', scram)
		
		# cv.waitKey(0)
		# cv.destroyAllWindows()
	
	
	# resize the image to fit within the image label but keep original proportions
	# i.e. rescale the image to fit within the label, returns new dimensions
	def smart_dimensions(self, image_shape, label_width, label_height):
		
		height, width = image_shape[0], image_shape[1]
		
		width_scale = label_width/width
		height_scale = label_height/height
		
		selec = min(width_scale, height_scale)
		
		new_shape = (int(width*selec), int(height*selec))
		
		return new_shape
	
	# returns original image with all faces scrambled
	def scramble_faces(self, blank, face_rects):
		
		copy = blank.copy()
		paste = blank.copy()
		
		for x, y, w, h in face_rects:
			
			block_width = int(w/blocks_num)
			block_height = int(h/blocks_num)
			
			blocks = self.get_blocks(x, y, block_width, block_height)
			
			shuffle_mat = self.get_shuffle_mat()
			
			shuffle_blocks = self.shuffle_blocks1(blocks, shuffle_mat)
			k = 0
			for i in range(blocks_num):
				for j in range(blocks_num): # may need to flip x, y coordinates in img[] especially if the face rectangle stops being a square
					# img5[x+i*block_width:x+(i*block_width)+block_width, y+j*block_height:y+(j*block_height)+block_height] = img6[shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width, shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height]
					# img5[y+j*block_height:y+(j*block_height)+block_height, x+i*block_width:x+(i*block_width)+block_width] = img6[shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width, shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height]
					paste[y+j*block_height:y+(j*block_height)+block_height, x+i*block_width:x+(i*block_width)+block_width] = copy[shuffle_blocks[k][1]:shuffle_blocks[k][1]+block_height, shuffle_blocks[k][0]:shuffle_blocks[k][0]+block_width]
					k += 1
		
		return paste
	
	
	def shuffle_blocks1(self, blocks, shuffle_mat):
		shuffle_blocks = []
		for i in range(blocks_num):
			for j in range(blocks_num):
				shuffle_blocks.append(blocks[shuffle_mat[i][j]])
		# print('shuffle_blocks', shuffle_blocks)
		
		return shuffle_blocks
	
	
	def get_shuffle_mat(self):
		
		# shuffle the set 0, 1, 2, ... ,blocks_num^2 - 1
		nums = [num for num in range(0, pow(blocks_num, 2))]
		shuffle = []
		while len(nums) > 0:
			rand = random.randrange(0, len(nums))
			# if nums[rand] != len(shuffle):
			shuffle.append(nums.pop(rand))
		# IDEA: place limits on the above output to ensure no block is in its original place and no two neighbouring blocks are still neighbouring each other on the same side
		print('shuffle', shuffle)
		
		# turn that 1xblock_nums^2 array into block_nums-x-block_nums matrix
		shuffle_mat = []
		for i in range(0, pow(blocks_num, 2)-2, blocks_num):
			x = i
			y = i+blocks_num
			shuffle_mat.append(shuffle[x:y])
			# shuffle_mat.append(shuffle[i:i+blocks_num])
		print('shuffle_mat', shuffle_mat)
		
		return shuffle_mat



	def get_blocks(self, x, y, block_width, block_height):
		blocks = []
		for i in range(blocks_num):
				for j in range(blocks_num): # may need to flip x, y coordinates in img[] especially if the face rectangle stops being a square
					blocks.append((x + (i*block_width), y + (j*block_height)))
					# blocks.append((y + (j*block_height), x + (i*block_width)))
		# print('blocks', blocks)
		
		return blocks


if __name__ == '__main__':
	
	FaceScrambler()
	
	cv.waitKey(0)
	cv.destroyAllWindows()