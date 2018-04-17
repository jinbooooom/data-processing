# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-4
function: Match Annotation and JPEGImages
"""

import os
import sys
import shutil
from jinbo_os_lib import file_name,postfix,isimg

JPEGImages = './test2/jpg/'
Annotations = './test2/xml/'
do_not_need_xml = './test2/no_xml/'
do_not_need_img = './test2/no_img/'

imgnames = []
xmlnames = []

file_name(imgnames,JPEGImages)
file_name(xmlnames,Annotations)
#print(1,imgnames)
#print(2,xmlnames)
for img in imgnames[0]:#移除没有对应xml的图片
	if postfix(img)[0] not in [postfix(x)[0] for x in xmlnames[0]]:
		shutil.move(JPEGImages + img,do_not_need_img + img)
#imgnames = []#重新清空，不然调用file_name是向列表尾添加元素
#file_name(imgnames,JPEGImages)#更新imgnames存储的JPEGImages里的文件名
'''其实上面两行注释掉不影响程序的功能'''
for xml in xmlnames[0]:#移除没有对应img的xml
	if postfix(xml)[0] not in [postfix(x)[0] for x in imgnames[0]]:
		shutil.move(Annotations + xml,do_not_need_xml + xml)
#xmlnames = []
#file_name(xmlnames,Annotations)
#print(3,imgnames[0])
#print(4,xmlnames[0])
