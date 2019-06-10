# -*- coding: utf-8 -*-
'''
function:Get the absolute path and file name of the file and save it to txt
'''

import os,sys

def get_file_names(dir_path):
	'''
	Don't contain folders,only files.
	'''
	return [x for x in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path,x))]

JPEGImages = './JPEGImages'
save_abs_filename = './abs_names.txt'
save_filename = './names.txt'

imgnames = sorted(get_file_names(JPEGImages))
with open(save_abs_filename,'w') as fabs:
	with open(save_filename,'w') as f:
		for img in imgnames:		
			fabs.write(os.path.join(os.path.abspath(JPEGImages),img))
			fabs.write('\n')
			f.write(os.path.splitext(img)[0])
			f.write('\n')

