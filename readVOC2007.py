# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-12
function: read .xml information and remove some .xml which we don't need
reference: https://www.cnblogs.com/cmt110/p/7464944.html
"""

import os,sys,shutil
import xml.dom.minidom
from xml.etree import ElementTree as ET

Annotations = './test_xml/Annotations'
abnormal_dir = './test_xml/abnormal'
delete_dir = './test_xml/delete'
blur_dir = './test_xml/blur'

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

for filename in os.listdir(Annotations):
	print(os.path.join(Annotations,filename))
	#dom = xml.dom.minidom.parse(os.path.join(Annotations,filename))
	#root = dom.documentElement
	per = ET.parse(os.path.join(Annotations,filename))
	#print(dom,root)
	p = per.findall('./object')
	for label in p:
		for child in label.getchildren():
			if child.tag == 'name':
				print(child.tag,':',child.text)
				if(child.text == 'delete'):
					cnt_delete += 1
					shutil.move(os.path.join(Annotations,filename),\
					os.path.join(delete_dir,filename))
					break
				elif(child.text == 'blur'):
					cnt_blur += 1
					shutil.move(os.path.join(Annotations,filename),\
					os.path.join(blur_dir,filename))
					break
				elif(child.text == 'abnormal'):
					cnt_abnormal += 1
					shutil.move(os.path.join(Annotations,filename),\
					os.path.join(abnormal_dir,filename))
					break
				elif(child.text == 'normal'):
					cnt_normal += 1
	print('delete: %d,blur: %d,abnormal: %d,normal: %d' % \
	(cnt_delete,cnt_blur,cnt_abnormal,cnt_normal))
				















	
