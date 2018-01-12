import cv2
import numpy as np 

cap = cv2.VideoCapture(1)
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
c = 0
while(1):

	_, frame = cap.read()
	frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_CUBIC)
	cv2.imshow('Frame',frame)

	key = cv2.waitKey(1) & 0xFF
	if key == 32:
		cv2.imwrite("./data/"+str(c)+".jpg",frame)
		c+=1
	if key == 113:
		break

cap.release()
cv2.destroyAllWindows() 