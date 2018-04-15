# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-8
function: 放射变换后求新坐标，并保存图和新txt
"""

import os
import sys
import shutil
import math
from jinbo_lib.jinbo_os import file_name,postfix,isimg
from jinbo_lib.jinbo_image import warpAffine
import cv2 as cv

pi = 3.141593
cnt = 1 #rename
oriImgPath = './JPEGImages/'
oriTxtPath = './txt/'
warpImgPath = './warp/warpImg/'
warpTxtPath = './warp/warpTxt/'
angles = [-80,-60,-40,-20,20,40,60,80] #正数->顺时针

def newPosition(old,w,h,dushu): #old在oriImg上的位置,w:oriW，h:oriH。
	angle = abs(dushu * pi / 180);#化为弧度
	dushu = -dushu # 因为正数是顺时针，而之前的C文件正数代表逆时针。
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


oriImgNames = []
file_name(oriImgNames,oriImgPath)
#print(oriImgNames)
total = len(oriImgNames[0]) * len(angles)

for oriImgName in oriImgNames[0]:
	img = cv.imread(oriImgPath + oriImgName)
	h,w = img.shape[:2]
	for angle in angles:
		imgwarp = warpAffine(img,angle)
		cv.imwrite(warpImgPath + str(int(oriImgName[:6]) + 100000 + cnt) + '.jpg',imgwarp)
		print('has processed %d,total:%d' % (cnt,total))
		with open(oriTxtPath + postfix(oriImgName)[0]+ 'txt','r') as f:
			lines = f.readlines()
			content = '% bbGt version=3\n' #content:after warpAffine new pos
			for line in lines:
				if 'bbGt' not in line:
					info = line.split()
					label = info[0]
					pos = [int(x) for x in info[1:5]]
					#print(img.shape)
				
					BBS = newPosition(pos,w,h,angle)
					content = content + label + ' ' + str(int(BBS[0])) + ' ' + str(int(BBS[1])) \
	 				+ ' ' + str(int(BBS[2])) + ' ' + str(int(BBS[3])) + ' ' + '0 0 0 0 0 0 0\n' 
					#print(BBS)
		#print(content)
		with open(warpTxtPath + str(int(oriImgName[:6]) + 100000 + cnt) + '.txt','w') as fw:
			fw.write(content)
		cnt = cnt + 1
				


		 	

