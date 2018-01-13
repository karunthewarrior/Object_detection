import numpy as np
from os import listdir
from os.path import isfile, join
import cv2
import pickle

def box_convert_center(pt_box):
	if(pt_box[0]!=None):
		(x1,y1),(x2,y2) = pt_box
		c_x = (x2-x1)/2 + x1
		c_y = (y2-y1)/2 + y1
		w = x2-x1
		h = y2-y1 
		return (c_x,c_y,w,h)
	else:
		return (None,None,None,None)

def box_convert_pt(center_box):
	(c_x,c_y,w,h) = center_box
	x1 = c_x - w/2
	x2 = x1 + w
	y1 = c_y - h/2
	y2 = y1 + h
	return ((x1,y1),(x2,y2))

def box_convert_label(label,bx,by):
	c_x = label[1]*32+32*bx
	c_y = label[2]*32+24*by
	w = label[3]*32
	h = label[4]*24
	pt_box = box_convert_pt((c_x,c_y,w,h))
	return pt_box

	
path = './bbox_coordinates/'
list = [f for f in listdir(path) if isfile(join(path, f))]

img_path = './image_data/'
colours = [[255,0,0],[0,0,0],[0,165,255],[192,192,192]]

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