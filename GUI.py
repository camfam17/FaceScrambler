import cv2 as cv
import customtkinter as ctk
from tkinter import filedialog
import FaceScrambler as scram


class MainFrame(ctk.CTkFrame):
	
	def __init__(self, container):
		super().__init__(container)
		
		self.select_image = ctk.CTkButton(master=self, text='Select Image', command=self.select_image_func)
		self.select_image.grid(row=1, column=1, padx=10, pady=10)
		
		self.use_webcam = ctk.CTkButton(master=self, text='Use Webcam', command=self.use_webcam_func)
		self.use_webcam.grid(row=2, column=1, padx=10, pady=10)
		
		print('hi')
	
	
	def use_webcam_func(self):
		
		print('hi')
		
		webcam = cv.VideoCapture(0)
		
		
		
		while True:
			check, frame = webcam.read()
			print(check, frame)
			
			scrambler = scram.FaceScrambler(image=frame)
			frame = scrambler.get_scrambled_image(frame)
			
			cv.imshow('video', frame)
			
			key = cv.waitKey(1)
			if key == 27:
				break
		
		webcam.release()
		cv.destroyAllWindows()
	
	
	def select_image_func(self):
		
		self.image_name = filedialog.askopenfilename()
		print(self.image_name)
		# self.image = cv.imread(self.image_name)
		
		scrambler = scram.FaceScrambler(self.image_name)
		
		self.blank = scrambler.get_blank_image()
		self.scrambled_image = scrambler.get_scrambled_image()
		
		cv.imshow('image', self.scrambled_image)


class Root(ctk.CTk):
	
	def __init__(self):
		super().__init__()
		
		self.geometry('200x200')
		
		self.mainframe = MainFrame(container=self)
		self.mainframe.pack()


if __name__ == '__main__':
	
	root = Root()
	root.mainloop()
