# -*- coding: utf-8 -*-
'''
function:获得文件绝对路径并保存到txt
'''

import os,sys
from jinbo_lib.os import get_file_names

JPEGImages = './VOC2007/JPEGImages'
save_filename = './all_names.txt'

imgnames = get_file_names(JPEGImages)
with open(save_filename,'w') as f:
	for img in imgnames:		
		#print(os.path.join(os.path.abspath('./teacher_pic/img'),img))
		f.write(os.path.join(os.path.abspath(JPEGImages),img))
		f.write('\n')

