# -*- coding:utf-8 -*-
'''
time: 2018-4-28
@author: Jinbo
function: 
'''
import os,sys,shutil
import cv2 as cv
import numpy as np


sys.path.append("..") #将环境变量设置为上一级（父目录），同 是也可以调用同目录的module
from jinbo_lib.image import mirror 
from jinbo_lib.os import *

def main():
	file_name = 800000
	ini = file_name
	img_path = './VOC2007/benttodesk'
	img_mirror_path = './VOC2007/benttodesk_mirror'
	if not os.path.exists(img_mirror_path):
		os.mkdir(img_mirror_path)
	imgnames = [x for x in get_file_names(img_path) if os.path.splitext(x)[1] == '.jpg']
	#print(imgnames)
	total = len(imgnames)
	for img in imgnames:
		file_name += 1
		pic = cv.imread(os.path.join(img_path,img))
		h,w = pic.shape[:-1]
		 
		lr = mirror(pic,'LR')
		cv.imwrite(os.path.join(img_mirror_path,str(file_name) + '.jpg'),lr)
		if((file_name - ini) % 50 == 0):
				print('has processed %6f%%' % (100 * (file_name - ini) / total))
	print('has processed %6f%%' % (100 * (file_name - ini) / total))

if __name__ == '__main__':
	main() 



