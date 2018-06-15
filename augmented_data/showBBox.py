# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-8
function: Visualized bounding box.
notice:The txt file's data format:[xmin,ymin,bboxw,bboxh].
"""

import os
import sys
import shutil
import math
import cv2 as cv
import random
sys.path.append("..")
from jinbo_lib.my_os import file_name,isimg,get_file_names

def main():
	oriImgPath = './warp/warpImg'
	oriTxtPath = './warp/warpTxt'
	savePath = './warp/BBoxImages'

	oriImgNames = sorted(get_file_names(oriImgPath))
	total = len(oriImgNames)
	cnt = 1

	for oriImgName in oriImgNames:
		img = cv.imread(os.path.join(oriImgPath,oriImgName))
		print('has processed %d,total:%d' % (cnt,total))
		with open(os.path.join(oriTxtPath,os.path.splitext(oriImgName)[0] + '.txt'),'r') as f:
			lines = f.readlines()
			for line in lines:
				info = line.split()
				label = info[0]
				pos = [int(x) for x in info[1:5]] # list[xmin,ymin,bboxw,bboxh]
				color = tuple(random.randint(0,255) for x in range(3))
				cv.rectangle(img,(pos[0],pos[1]),(pos[0] + pos[2],pos[1] + pos[3]),color,2)
				cv.imwrite(os.path.join(savePath,oriImgName),img)
		cnt = cnt + 1

if __name__ == '__main__':
	main()





