from __future__ import division
import numpy as np
from os import listdir
from os.path import isfile, join
import cv2
import pickle
import math
import pandas as pd

def disp(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		print x,y
		g_x,g_y = locate_grid(x,y)
		print g_x,g_y

def locate_grid(x,y):
	grid_x = int(x/20)
	grid_y = int(y/20)
	print "Grid:",grid_x,grid_y
	return grid_x,grid_y

def box_convert_center(pt_box):
	if(pt_box[0]!=None):
		(x1,y1),(x2,y2) = pt_box
		c_x = int((x2-x1)/2) + x1
		c_y = int((y2-y1)/2) + y1
		w = x2-x1
		h = y2-y1 
		return (c_x,c_y,w,h)
	else:
		return (None,None,None,None)

def box_convert_pt(center_box):
	(c_x,c_y,w,h) = center_box
	x1 = c_x - int(w/2)
	x2 = x1 + w
	y1 = c_y - int(h/2)
	y2 = y1 + h
	return ((int(x1),int(y1)),(int(x2),int(y2)))

def create_label_array(rect_list,img):
	colours = [[255,0,0],[0,0,0],[0,165,255],[192,192,192]]
	label = np.zeros((32,24,6))
	for i,rec in enumerate(rect_list):
		center_box = box_convert_center(rec)
		if(rec[0] !=None):
			bx,by = locate_grid(center_box[0],center_box[1])
			label[bx,by,0] = 1
			label[bx,by,1] = (center_box[0]%20)/20
			label[bx,by,2] = (center_box[1]%20)/20
			label[bx,by,3] = center_box[2]/20
			label[bx,by,4] = center_box[3]/20
			label[bx,by,5] = i
			# print label[bx,by,:]
			# pt_box = box_convert_label(label[bx,by,:],bx,by)
			# cv2.rectangle(img, pt_box[0], pt_box[1], color=[255,255,255], thickness=5, lineType=8, shift=0)
	return label

def generate_class_labels(rect_list,img):
	class_list = []
	class_list.append(img.split('.')[0]+'.jpg')
	for i,rec in enumerate(rect_list):
		if rec[0]==None:
			class_list.append(0)
		else:
			class_list.append(1)
	return class_list

def box_convert_label(label,bx,by):
	c_x = label[1]*20+20*bx
	c_y = label[2]*20+20*by
	w = label[3]*20
	h = label[4]*20
	pt_box = box_convert_pt((c_x,c_y,w,h))
	return pt_box

path = './bbox_coordinates/'
list = [f for f in listdir(path) if isfile(join(path, f))]

img_path = './image_data/'

cv2.namedWindow('Image')
cv2.setMouseCallback('Image',disp)
colours = [[255,0,0],[0,0,0],[0,165,255],[192,192,192]]

class_labels = []
for count,x in enumerate(list):
	img = cv2.imread(img_path + x.split('.')[0]+'.jpg')
	height,width,_ = img.shape
	
	#Drawing the grids for visualization
	for i in range(int(width/20)):
		cv2.line(img, (i*int(width/32),0), (i*int(width/32),height), (0, 0, 0), 1, 1)
	for i in range(int(height/20)):
		cv2.line(img, (0,i*int(height/24)), (width,i*int(height/24)), (0, 0, 0), 1, 1)
	
	rect_list = pickle.load(open(path + x,'rb'))
	class_list = generate_class_labels(rect_list,x)
	class_labels.append(class_list)
	# for i,x in enumerate(rect_list):
	# 	cv2.rectangle(img, x[0], x[1], color=colours[i], thickness=3, lineType=8, shift=0)

	label = create_label_array(rect_list,img)
	pickle.dump(label,open('./labels/'+list[count].split('.')[0] + ".p","wb"),protocol=2)
	cv2.imshow('Image',img)
	key = cv2.waitKey(1) & 0xFF
labels_df = pd.DataFrame(class_labels,index=None)
labels_df.columns = ["image_name","class1","class2","class3","class4"]
labels_df.to_csv("./classification_labels/class_labels.csv",index=False) 

cv2.destroyAllWindows() 