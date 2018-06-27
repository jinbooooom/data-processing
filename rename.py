# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4
function: rename images
"""

import os,sys
import cv2 as cv
from jinbo_lib.my_os import *

first_name = 101135 # 110000
rename_path = './a'
path = './a'

cnt = 0

imgnames = sorted(get_file_names(path),key = str.lower)
# print(imgnames)

for oriimg in imgnames:
	if(isimg(oriimg,['.jpg'])):
		first_name = first_name + 1
		s1 = os.path.join(path,oriimg)
		s2 = os.path.join(rename_path,str(first_name) + '.jpg')
		os.rename(s1,s2)
		print(s1,s2,sep = '-->')
		cnt += 1

print("successfully",sep='\n----------------\n',end='\n')
print('has renamed %d file.' % cnt)


