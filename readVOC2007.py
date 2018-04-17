# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-12
function: read .xml information. According to these tag information, classify pictures and labels into corresponding folders.
reference: https://www.cnblogs.com/cmt110/p/7464944.html
"""

import os,sys,shutil
import xml.dom.minidom
from xml.etree import ElementTree as ET

Annotations = './VOC2007c3_6954_20180416/Annotations'
JPEGImages = './VOC2007c3_6954_20180416/JPEGImages'
abnormal_dir = './VOC2007c3_6954_20180416/abnormal'
delete_dir = './VOC2007c3_6954_20180416/delete'
blur_dir = './VOC2007c3_6954_20180416/blur'

if(not os.path.exists(abnormal_dir)):
	os.mkdir(abnormal_dir)
if(not os.path.exists(delete_dir)):
	os.mkdir(delete_dir)
if(not os.path.exists(blur_dir)):
	os.mkdir(blur_dir)
'''
print(os.listdir())
for dirpath,dirnames,filenames in os.walk('./test_xml'):
	print(dirpath,dirnames,filenames)
'''

cnt_abnormal = cnt_normal = cnt_delete = cnt_blur = 0
cnt_benttodesk = cnt_inclined = 0

error_file_sets = []
for filename in os.listdir(Annotations):
	#print(os.path.join(Annotations,filename))
	#dom = xml.dom.minidom.parse(os.path.join(Annotations,filename))
	#root = dom.documentElement
	
	per = ET.parse(os.path.join(Annotations,filename))
	#print(dom,root)
	p = per.findall('./object')
	for label in p:
		labels = []
		for child in label.getchildren():
			if child.tag == 'name':
				#print(child.tag,':',child.text)
				labels.append(child.text)
				#print(labels)
		#print(labels)
		if('delete' in labels):
			cnt_delete += 1
			shutil.move(os.path.join(Annotations,filename),\
			os.path.join(delete_dir,filename))
			shutil.move(os.path.join(JPEGImages,os.path.splitext(filename)[0] + '.jpg'),os.path.join(delete_dir,os.path.splitext(filename)[0] + '.jpg'))
			#print('delete')
			break
		elif('blur' in labels):
			cnt_blur += 1
			shutil.move(os.path.join(Annotations,filename),\
			os.path.join(blur_dir,filename))
			shutil.move(os.path.join(JPEGImages,os.path.splitext(filename)[0] + '.jpg'),os.path.join(blur_dir,os.path.splitext(filename)[0] + '.jpg'))
			#print('blur')
			break
		elif('abnormal' in labels):
			cnt_abnormal += labels.count('abnormal')
			shutil.move(os.path.join(Annotations,filename),\
			os.path.join(abnormal_dir,filename))
			shutil.move(os.path.join(JPEGImages,os.path.splitext(filename)[0] + '.jpg'),os.path.join(abnormal_dir,os.path.splitext(filename)[0] + '.jpg'))
			#print('abnormal')
			break
		elif('normal' in labels):
			#print('normal')
			cnt_normal += labels.count('normal')
		elif('benttodesk' in labels):
			cnt_benttodesk += 1
		elif('inclined' in labels):
			cnt_inclined += 1
		else:
			error_file_sets.append(filename)
	if((cnt_normal + cnt_inclined + cnt_benttodesk ) % 500 == 0):
		print('delete: %d,blur: %d,abnormal: %d,normal: %d,inclined: %d,benttodesk: %d' % \
		(cnt_delete,cnt_blur,cnt_abnormal,cnt_normal,cnt_inclined,cnt_benttodesk))
		print('This are a number of files with invalid labels\n',error_file_sets)
	
print('delete: %d,blur: %d,abnormal: %d,normal: %d,inclined: %d,benttodesk: %d' % \
		(cnt_delete,cnt_blur,cnt_abnormal,cnt_normal,cnt_inclined,cnt_benttodesk))
print('This are a number of files with invalid labels\n',error_file_sets)












	
