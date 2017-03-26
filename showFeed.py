import cv2
import qrtools
import csv
import time
from matplotlib.path import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shutil import copyfile


RL2 = [(0,150),(0,430),(250,285),(250,285),(0.,0.),]
RL3 = [(60,398),(250,494),(250,285),(250,285),(0.,0.),]
RL1 = [(250,0),(0,150),(250,285),(250,285),(0.,0.),]
BL2 = [(1000,150),(1000,430),(750,285),(750,285),(0.,0.),]
BL3 = [(940,398),(750,494),(750,285),(750,285),(0.,0.),]
BL1 = [(750,0),(1000,150),(750,285),(750,285),(0.,0.),]
RLS = [(60,398),(0,520),(200,630),(250,494),(0.,0.),]
BLS = [(940,398),(1000,520),(800,630),(750,494),(0.,0.),]
codes = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY,]

def region(x,y):
	
	if Path(RL1,codes).contains_point((x,y)):
		return "Red Lift 1"
	if Path(RL2,codes).contains_point((x,y)):
		return "Red Lift 2"
	if Path(RL3,codes).contains_point((x,y)):
		return "Red Lift 3"
	if Path(BL1,codes).contains_point((x,y)):
		return "Blue Lift 1"
	if Path(BL2,codes).contains_point((x,y)):
		return "Blue Lift 2"
	if Path(BL3,codes).contains_point((x,y)):
		return "Blue Lift 3"
	if Path(RLS,codes).contains_point((x,y)):
		return "Red LS"
	if Path(BLS,codes).contains_point((x,y)):
		return "Blue LS"

	return "Other"

def show_webcam(mirror=False):
	tempString = ""
	SETUP_LIST = 'setupList.csv'
	EVENT_LIST = 'eventList.csv'
	inputString = ""
	cam = cv2.VideoCapture(0)
	iAr = []
	file = "test_image.png"
	timeToWait = 0
	while True:
		ret_val, img = cam.read()
		camera_capture = img
		if mirror: 
			img = cv2.flip(img, 1)
		cv2.imshow('1089 Scouting Scanner', img)
		if cv2.waitKey(1) == 27: 
			break  # esc to quit
		time.sleep(timeToWait)
		timeToWait = 0
		cv2.imwrite(file, camera_capture)
		qr = qrtools.QR()
		qr.decode(file) 
		if qr.data != "NULL" and qr.data != tempString:
			inputString = qr.data
			iAr = inputString.strip().split(",")
			team=iAr[2]
			match=iAr[1]
			scouter=iAr[0]
			dstfile = "QRCodes\\"+team+"_"+match+".png"
			copyfile(file, dstfile)
			chunks = lambda iAr, n=10: [iAr[i:i+n] for i in range(0, len(iAr), n)]
			with open(SETUP_LIST, 'ab+') as csvfile:
				csvWrite = csv.writer(csvfile, dialect='excel', delimiter=',')
#				print chunks(iAr)
#				print len(iAr)
				csvWrite.writerow(iAr[:7] + iAr[len(iAr)-7:])
			with open(EVENT_LIST, 'ab+') as csvfile:
				csvWrite = csv.writer(csvfile, dialect='excel', delimiter=',')
				setupArr = [team,match]
				newEvent = iAr	
				del newEvent[:7]
				del newEvent[len(newEvent)-7:]
				chunklen = len(chunks(newEvent))
				for i in chunks(newEvent)[:chunklen-1]:
					y=750-float(i[3])
					x=float(i[2])
					action=i[5]
					if action == '4':
						i.append(region(x,y))
					else:
						i.append("Other")
					i.append(scouter)
					i.append(time.time())
					time.sleep(.001)
					csvWrite.writerow(setupArr + i)
			tempString = qr.data
			print "Saved - ", scouter, ":", team,":", match 
#			s_img = cv2.imread("check.png", -1)
#			l_img = cv2.imread(file)
#			x_offset=y_offset=50
#			for c in range(0,3):
#				l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1], c] =  s_img[:,:,c] * (s_img[:,:,3]/255.0) +  l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1], c] * (1.0 - s_img[:,:,3]/255.0)
#			camera_capture = l_img
#			cv2.putText(camera_capture, 'This one!', (230, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
#			cv2.imshow('1089 Scouting Scanner', s_img)
#			time.sleep(2)
		else:
			camera_capture = img
	cv2.destroyAllWindows()

def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()