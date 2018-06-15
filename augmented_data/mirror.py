# -*- coding:utf-8 -*-
'''
time: 2018-4-28
@author: Jinbo
function:mirror-like transformation
'''
import os,sys,shutil
import cv2 as cv
import numpy as np


sys.path.append("..") # Set the environment variable to the parent directory and also call the module of the current directory.
from jinbo_lib.image import mirror 
from jinbo_lib.my_os import *

def main():
	init_name = 800000
	file_name = init_name
	img_path = '../demo'
	img_mirror_path = './mirror'
	if not os.path.exists(img_mirror_path):
		os.mkdir(img_mirror_path)
	imgnames = sorted([x for x in get_file_names(img_path) if os.path.splitext(x)[1] == '.jpg'])
	#print(imgnames)
	total = len(imgnames) * 2
	for img in imgnames:
		pic = cv.imread(os.path.join(img_path,img))
		h,w = pic.shape[:-1]
		 
		lr = mirror(pic,'LR')
		file_name += 1
		cv.imwrite(os.path.join(img_mirror_path,str(file_name) + '.jpg'),lr)
		ud = mirror(pic,'UD')
		file_name += 1
		cv.imwrite(os.path.join(img_mirror_path,str(file_name) + '.jpg'),ud)
		if((file_name - init_name) % 50 == 0):
			print('has processed %6f%%' % (100 * (file_name - init_name) / total))
	print('has processed %6f%%' % (100 * (file_name - init_name) / total))

if __name__ == '__main__':
	main() 



