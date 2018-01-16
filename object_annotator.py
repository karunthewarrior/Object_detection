import numpy as np
from os import listdir
from os.path import isfile, join
import cv2
import pickle
import random


global done_flag,init_pt,final_pt

done_flag = 0 
def draw_rect(event,x,y,flags,param):
	global done_flag,init_pt,final_pt
	if event == cv2.EVENT_LBUTTONDOWN:
		init_pt = (x,y)
		# print x,y

	if event == cv2.EVENT_LBUTTONUP:
		final_pt = (x,y)
		done_flag = 1

def draw_grid(img):
	for i in range(0,img.shape[1],20):
		cv2.line(img, (0, i), (img.shape[1], i), (0, 0, 0), 1, 1)
	for i in range(0,img.shape[1],20):
		cv2.line(img, (i, 0), (i, img.shape[0]), (0, 0, 0), 1, 1)
	return img

print "Welcome to KTW's object annotator!"
print "1 - Blue racecar(class 0)\n2 - Black car(class 1)\n3 - Orange Truck(class 2)\n4 - Heatsink(class 3)\n"
print "Press space to save bounding boxes, R to redo, Esc to exit. "

labels_path = './bbox_coordinates/'
labels_list = [f.split('.')[0] for f in listdir(labels_path) if isfile(join(labels_path, f))]


path = './image_data/'
image_list= [f for f in listdir(path) if isfile(join(path, f)) if f.split('.')[0] not in labels_list]


cv2.namedWindow('Image')
cv2.setMouseCallback('Image',draw_rect)
count = 0
rect_list =  [(None,None),(None,None),(None,None),(None,None)]
rect_class = 0 
colours = [[255,0,0],[0,0,0],[0,165,255],[192,192,192]]
print "You have " + str(len(image_list)) +" images to go. All the best. :)"
print image_list[count]
words = ["Insane","Awesome","Wow","Oh wow","You are a superstar"]
while(1):
	img = cv2.imread(path + image_list[count])
	img = draw_grid(img)
	if(done_flag == 1):
		rect_list[rect_class] = ((init_pt,final_pt))
		done_flag = 0
	for i,x in enumerate(rect_list):
		cv2.rectangle(img, x[0], x[1], color=colours[i], thickness=3, lineType=8, shift=0)
	cv2.imshow('Image',img)
	key = cv2.waitKey(5) & 0xFF
	if key == 49:
		rect_class = 0
	if key == 50:
		rect_class = 1
	if key == 51:
		rect_class = 2
	if key == 52:
		rect_class = 3
	if key == 114:
		rect_list =  [(None,None),(None,None),(None,None),(None,None)]
		rect_class = 0 
		continue
	if key == 32:
		pickle.dump(rect_list,open('./bbox_coordinates/'+image_list[count].split('.')[0] + ".p","wb"),protocol=2)
		count+=1
		if count%5 == 0:
			print words[random.randint(0,len(words))-1] +"! Only " + str(len(image_list)-count+1) + " left!"
		if count%12 == 0:
			print "Come on, you can do it!"
		print image_list[count]
		rect_list =  [(None,None),(None,None),(None,None),(None,None)]
		rect_class = 0 
		continue
	if key == 27:
		break
cv2.destroyAllWindows() 