# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-8
function: Rotate transform and calculate new coordinates.
notice:The data format default as same as YOLO.
"""

import os
import sys
import shutil
import math
import cv2 as cv
sys.path.append("..")
from jinbo_lib.my_os import file_name,isimg,get_file_names
from jinbo_lib.image import warpAffine

pi = 3.141593
   
def newPosition(old,w,h,dushu):
	'''
	old:The coordinates on the original image,list[xmin,ymin,bboxw,bboxh]
	w,h:The width and height of the original image.
	'''
	angle = abs(dushu * pi / 180);# Convert to radians
	dushu = -dushu # Because the positive number is clockwise, the positive number in the previous C file represents counterclockwise
	BBS = [0,0,0,0]
	if(dushu >= 0):	
		BBS[0] = old[1] * math.sin(angle) + old[0] * math.cos(angle)
		BBS[1] = old[1] * math.cos(angle) + (w - old[0] - old[2]) * math.sin(angle)
	else:
		BBS[0] = (h - old[1] - old[3]) * math.sin(angle) + old[0] * math.cos(angle)
		BBS[1] = old[0] * math.sin(angle) + old[1] * math.cos(angle)
	BBS[2] = old[2] * math.cos(angle) + old[3] * math.sin(angle)
	BBS[3] = old[2] * math.sin(angle) + old[3] * math.cos(angle)
	return BBS

def main():
	init_name = 800000 # new name
	cnt = 1 # statistics
	# The optional parameter of data_format:[VOC2007,YOLO].VOC2007:[xmin,ymin,xmax,ymax].YOLO:[xcentre,ycentre,bboxw,bboxh]
	data_format = 'YOLO'
	oriImgPath = '../demo'
	oriTxtPath = '../demo/yolo_txt'
	warpImgPath = './warp/warpImg'
	warpTxtPath = './warp/warpTxt'
	angles = [-20,-10,-5,5,10,20] # Positive number --> clockwise.The absolute value of the angle cannot exceed 90
	oriImgNames = sorted(get_file_names(oriImgPath))
	total = len(oriImgNames) * len(angles)

	for oriImgName in oriImgNames:
		img = cv.imread(os.path.join(oriImgPath,oriImgName))
		h,w = img.shape[:2]
		# print('shape',h,w)
		for angle in angles:
			imgwarp = warpAffine(img,angle)
			saveWarpImgPath = os.path.join(warpImgPath,str(int(os.path.splitext(oriImgName)[0]) + init_name + cnt) + '.jpg')
			cv.imwrite(saveWarpImgPath,imgwarp)
			print('has processed %d,total:%d' % (cnt,total))
			with open(os.path.join(oriTxtPath,os.path.splitext(oriImgName)[0] + '.txt'),'r') as f:
				lines = f.readlines()
				content = ''
				for line in lines:
					info = line.split()
					label = info[0]
					# pos = [int(x) for x in info[1:5]] # xmin,ymin,w,h
					if(data_format == 'VOC2007'):
						pos = [float(info[1]),float(info[2]),float(info[3]) - float(info[1]),float(info[4]) - float(info[2])]
						# print(pos)
					if(data_format == 'YOLO'):
						'''
						YOLO foamat:XCentre,yCentre,w,h
						'''
						pos = [(float(info[1]) - float(info[3])/2.0) * w,\
							(float(info[2]) - float(info[4])/2.0) * h,\
							float(info[3]) * w,float(info[4]) * h]
					BBS = newPosition(pos,w,h,angle)
					content = content + label + ' ' + str(int(BBS[0])) + ' ' + str(int(BBS[1])) \
		 				+ ' ' + str(int(BBS[2])) + ' ' + str(int(BBS[3])) + '\n' 
					#print(BBS)
			#print(content)
			with open(os.path.join(warpTxtPath,str(int(os.path.splitext(oriImgName)[0]) + init_name + cnt) + '.txt'),'w') as fw:
				fw.write(content)
			cnt = cnt + 1
				
if __name__ == '__main__':
	main()

		 	

