# -*- coding: utf-8 -*-
"""
function:一些个人编写的函数
reference: https://www.cnblogs.com/jiaxin359/p/7324077.html
"""

import os,sys,shutil


def isimg(img_name,img_features = ['.jpg']): # img_feature is list.
	#img_feature = ['.jpg'] #,'.png','.bmp','.jpeg','.gif']
	# 只处理.jpg的图像，其它格式的会就是原文件夹剩下的，用美图秀秀批处理转格式
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
	return [x for x in os.listdir(dir_path)]# if os.path.isfile(x)]

'''
def postfix(filename):	
	img_postfix = filename[len(filename)-3:len(filename)] # 获得文件后缀'jpg'
	img_name = filename[:len(filename)-3] # 把1.jpg分解成为img_name = '1.'，img_postfix = 'jpg'
	list_file_name = [img_name,img_postfix]
	return list_file_name	
	return filename.split('.')
'''

def main():
	print('i am main')
	

if __name__ == '__main__':
	main()

