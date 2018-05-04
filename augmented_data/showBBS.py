# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-8
function: Visualized bounding box
"""

import os
import sys
import shutil
import math
from jinbo_lib.jinbo_os import file_name,postfix,isimg
import cv2 as cv

def visualization(pos,draw,savepath):			
	cv.rectangle(draw,(pos[0],pos[1]),(pos[0] + pos[2],pos[1] + pos[3]),(0,0,255),5)
	cv.imwrite(savepath,draw)

oriImgPath = './warp/warpImg/'
oriTxtPath = './warp/warpTxt/'
savePath = './warp/BBImages/'

oriImgNames = []
file_name(oriImgNames,oriImgPath)
#print(oriImgNames)
total = len(oriImgNames[0])
cnt = 1

for oriImgName in oriImgNames[0]:
	img = cv.imread(oriImgPath + oriImgName)
	print('has processed %d,total:%d' % (cnt,total))
	with open(oriTxtPath + postfix(oriImgName)[0]+ 'txt','r') as f:
		lines = f.readlines()
		for line in lines:
			if 'bbGt' not in line:
				info = line.split()
				label = info[0]
				pos = [int(x) for x in info[1:5]]
				#print(pos)
				cv.rectangle(img,(pos[0],pos[1]),(pos[0] + pos[2],pos[1] + pos[3]),(0,0,255),15)
				cv.imwrite(savePath + oriImgName,img)
	cnt = cnt + 1






