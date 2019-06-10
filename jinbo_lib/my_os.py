# -*- coding: utf-8 -*-
"""
function:my personal function
"""

import os
import sys
import shutil


def isimg(img_name,img_features = ['.jpg']): # img_feature is list.
	for img_feature in img_features:
		if(os.path.splitext(img_name)[1].lower() in img_features):
			return True
	return False

def file_name(file_name,file_dir): 
	#file_name = []
	for root, dirs, files in os.walk(file_dir):  
		#print('root:',root) #当前目录路径  
		#print('dirs:',dirs) #当前路径下所有子目录
		#print('files:',files) #当前路径下所有非目录子文件
		return file_name.append(files)

def get_file_names(dir_path):
	'''
	Don't contain folders,only files.
	'''
	return [x for x in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path,x))]

def get_folders_names(dir_path):
	'''
	Don't contain files,only folders.
	'''
	return [x for x in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path,x))]


def mkdir(path):
	"""
	Create a multi-tier directory
	:param path: path you want to create
	:return: directory
	"""
	path = path.strip()
	isExists = os.path.exists(path)
	if not isExists:
		os.makedirs(path)
	else:
		pass

def main():
	#print(get_file_names('./1'))
	#print([x for x in os.listdir('1') if os.path.isdir(os.path.join('./1',x))])
	pass

if __name__ == '__main__':
	main()

