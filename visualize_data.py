import numpy as np
from os import listdir
from os.path import isfile, join
import cv2
import pickle


path = './labels/'
list = [f for f in listdir(path) if isfile(join(path, f))]

img_path = './image_data/'
colours = [[255,0,0],[0,255,0],[0,0,255],[255,0,255]]

for i,x in enumerate(list):
	print x
	img = cv2.imread(img_path + x.split('.')[0]+'.jpg')
	rect_list = pickle.load(open(path + x,'rb'))
	for i,rec in enumerate(rect_list):
		cv2.rectangle(img, rec[0], rec[1], color=colours[i], thickness=5, lineType=8, shift=0)
	cv2.imshow('Image',img)
	key = cv2.waitKey() & 0xFF
	if key == 27:
		break
cv2.destroyAllWindows() 