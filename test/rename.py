import os,sys
import cv2 as cv

first_name = 305517#110000
rename_path = './modify_name/' #改名后的图片文件夹路径
path = './addimg/'#原图片文件夹路径
postfix = '.jpg'
imgnames = []

def isimg(img):
	img_feature = ['.jpg'] #,'.png','.bmp','.jpeg','.gif']
	# 只处理.jpg的图像，其它格式的会就是原文件夹剩下的，用美图秀秀批处理转格式
	for img_postfix in img_feature:
		if(img_postfix in img.lower()):
			return True
	return False

def file_name(file_dir):   
	for root, dirs, files in os.walk(file_dir):  
		#print('root:',root) #当前目录路径  
		#print('dirs:',dirs) #当前路径下所有子目录
		#print('files:',files) #当前路径下所有非目录子文件
		imgnames.append(files)


file_name(path)
#print(imgnames[0],len(imgnames))

#for i in range(len(imgnames)):
#	print(imgnames[1])
#	#s1 = path + imgnames[i]
#	s2 = rename_path + str(100000 + i) + postfix
#	print(s2)

for oriimg in imgnames[0]:
	if(isimg(oriimg) and first_name < 905518):
		first_name = first_name + 42 #相邻图片名字隔15
		s1 = path + oriimg
		s2 = rename_path + str(first_name) + postfix
		os.rename(s1,s2)
		print(s1,s2,sep = '-->')

#txt = imgnames
print("successfully",sep='\n----------------\n',end='\n')
