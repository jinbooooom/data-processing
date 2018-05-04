# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-12
function: Match Annotations and JPEGImages.Then read .xml information. According to these tag information, classify pictures and labels into corresponding folders.
reference: https://www.cnblogs.com/cmt110/p/7464944.html(About how to use xml.dom)
"""

import os,sys,shutil
import xml.dom.minidom
from xml.etree import ElementTree as ET
from jinbo_lib.os import *

def match(Annotations,JPEGImages):
	'''
	Match Annotations and JPEGImages
	'''	
	no_xml = './VOC2007/do_not_need_xml'
	no_img = './VOC2007/do_not_need_img'
	if(not os.path.exists(no_xml)):
		os.mkdir(no_xml)
	if(not os.path.exists(no_img)):
		os.mkdir(no_img)
	xmlnames = get_file_names(Annotations)
	imgnames = get_file_names(JPEGImages)
	'''
	# so slow
	for img in imgnames: # remove img files which without corresponding xml files
		if os.path.splitext(img)[0] not in [os.path.splitext(x)[0] for x in xmlnames]:
			shutil.move(os.path.join(JPEGImages,img),os.path.join(no_img,img))
	for xml in xmlnames: # remove xml files which without corresponding img files
		if os.path.splitext(xml)[0] not in [os.path.splitext(x)[0] for x in imgnames]:
			shutil.move(os.path.join(Annotations,xml),os.path.join(no_xml,xml))
	'''
	# updata in 2018-5-3
	xml_sets = set([os.path.splitext(xml)[0] for xml in xmlnames])
	img_sets = set([os.path.splitext(img)[0] for img in imgnames])
	unnecessary_xml = [(xml + '.xml') for xml in xml_sets - img_sets]
	unnecessary_img = [(img + '.jpg') for img in img_sets - xml_sets]
	print('there are some unnecessary xml files:\n',unnecessary_xml,sep = '')
	print('there are some unnecessary images:\n',unnecessary_img,sep = '')
	for xml in unnecessary_xml:
		shutil.move(os.path.join(Annotations,xml),os.path.join(no_xml,xml))
	for img in unnecessary_img:
		shutil.move(os.path.join(JPEGImages,img),os.path.join(no_img,img))


def main():

	Annotations = './VOC2007/Annotations'
	JPEGImages = './VOC2007/JPEGImages'
	match(Annotations,JPEGImages)

	abnormal_dir = './VOC2007/abnormal'
	delete_dir = './VOC2007/delete'
	blur_dir = './VOC2007/blur'
	normal_dir = './VOC2007/normal'
	inclined_dir = './VOC2007/inclined'
	benttodesk_dir = './VOC2007/benttodesk'

	if(not os.path.exists(abnormal_dir)):
		os.mkdir(abnormal_dir)
	if(not os.path.exists(delete_dir)):
		os.mkdir(delete_dir)
	if(not os.path.exists(blur_dir)):
		os.mkdir(blur_dir)

	if(not os.path.exists(normal_dir)):
		os.mkdir(normal_dir)
	if(not os.path.exists(inclined_dir)):
		os.mkdir(inclined_dir)
	if(not os.path.exists(benttodesk_dir)):
		os.mkdir(benttodesk_dir)
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
			#elif('abnormal' in labels):
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
				'''
				shutil.move(os.path.join(Annotations,filename),\
				os.path.join(normal_dir,filename))
				shutil.move(os.path.join(JPEGImages,os.path.splitext(filename)[0] + '.jpg'),os.path.join(normal_dir,os.path.splitext(filename)[0] + '.jpg'))
				'''
			elif('benttodesk' in labels):
				cnt_benttodesk += 1
				shutil.move(os.path.join(Annotations,filename),\
				os.path.join(benttodesk_dir,filename))
				shutil.move(os.path.join(JPEGImages,os.path.splitext(filename)[0] + '.jpg'),os.path.join(benttodesk_dir,os.path.splitext(filename)[0] + '.jpg'))
				break
			elif('inclined' in labels):
				cnt_inclined += 1
				shutil.move(os.path.join(Annotations,filename),\
				os.path.join(inclined_dir,filename))
				shutil.move(os.path.join(JPEGImages,os.path.splitext(filename)[0] + '.jpg'),os.path.join(inclined_dir,os.path.splitext(filename)[0] + '.jpg'))
				break
			else:
				error_file_sets.append(filename)
		if((cnt_normal + cnt_inclined + cnt_benttodesk ) % 500 == 0):
			print('delete: %d,blur: %d,abnormal: %d,normal: %d,inclined: %d,benttodesk: %d' % \
			(cnt_delete,cnt_blur,cnt_abnormal,cnt_normal,cnt_inclined,cnt_benttodesk))
			#print('This are a number of files with invalid labels\n',error_file_sets)
	
	print('delete: %d,blur: %d,abnormal: %d,normal: %d,inclined: %d,benttodesk: %d' % \
			(cnt_delete,cnt_blur,cnt_abnormal,cnt_normal,cnt_inclined,cnt_benttodesk))
	if(error_file_sets):
		print('There are a number of files with invalid labels\n',error_file_sets)

if __name__ == '__main__':
	main()












	
