# -*- coding: utf-8 -*-
'''
@author: Jinbo
Time: 2018-4-11
function: Create Annotations from text file. At present,only single target.
'''

import xml.dom.minidom as XmlDocument
from jinbo_lib.os import *
import cv2 as cv

def createVOC2007xml(save_path,txt_name,label,bbs,resolution,channel):
	'''txt translate VOC2007'''
	#定义XML文档对象doc
	doc = XmlDocument.Document()
	#创建根节点Annotation
	Annotation = doc.createElement('annotations')
	doc.appendChild(Annotation)

	#添加节点
	Floder = doc.createElement('folder')
	Annotation.appendChild(Floder)
	Floder.appendChild(doc.createTextNode('VOC2007'))

	Filename = doc.createElement('filename')
	Annotation.appendChild(Filename)
	Filename.appendChild(doc.createTextNode(txt_name))

	Source = doc.createElement('source')
	Annotation.appendChild(Source)
	Database = doc.createElement('database')
	Source.appendChild(Database)
	Database.appendChild(doc.createTextNode('My Database'))
	Annotation2 = doc.createElement('annotation')
	Source.appendChild(Annotation2)
	Annotation2.appendChild(doc.createTextNode('VOC2007'))
	Image = doc.createElement('image')
	Source.appendChild(Image)
	Image.appendChild(doc.createTextNode('flickr'))
	Flickrid = doc.createElement('flickrid')
	Source.appendChild(Flickrid)
	Flickrid.appendChild(doc.createTextNode('NULL'))

	Owner = doc.createElement('owner')
	Annotation.appendChild(Owner)
	Name = doc.createElement('name')
	Owner.appendChild(Name)
	Name.appendChild(doc.createTextNode('Jinbo'))

	Size = doc.createElement('size')
	Annotation.appendChild(Size)
	Width = doc.createElement('width')
	Size.appendChild(Width)
	Width.appendChild(doc.createTextNode(str(resolution[0])))
	Height = doc.createElement('height')
	Size.appendChild(Height)
	Height.appendChild(doc.createTextNode(str(resolution[1])))
	Depth = doc.createElement('depth')
	Size.appendChild(Depth)
	Depth.appendChild(doc.createTextNode(str(channel)))

	Segmented = doc.createElement('segmented')
	Annotation.appendChild(Segmented)
	Segmented.appendChild(doc.createTextNode('0'))

	Object = doc.createElement('object')
	Annotation.appendChild(Object)
	Name2 = doc.createElement('name')
	Object.appendChild(Name2)
	Name2.appendChild(doc.createTextNode(label))
	Pose = doc.createElement('pose')
	Object.appendChild(Pose)
	Pose.appendChild(doc.createTextNode('Unspecified'))
	Truncated = doc.createElement('truncated')
	Object.appendChild(Truncated)
	Truncated.appendChild(doc.createTextNode('0'))
	Difficult = doc.createElement('difficult')
	Object.appendChild(Difficult)
	Difficult.appendChild(doc.createTextNode('0'))
	Bndbox = doc.createElement('bndbox')
	Object.appendChild(Bndbox)
	Xmin = doc.createElement('xmin')
	Bndbox.appendChild(Xmin)
	Xmin.appendChild(doc.createTextNode(bbs[0]))
	Ymin = doc.createElement('ymin')
	Bndbox.appendChild(Ymin)
	Ymin.appendChild(doc.createTextNode(bbs[1]))
	Xmax = doc.createElement('xmax')
	Bndbox.appendChild(Xmax)
	Xmax.appendChild(doc.createTextNode(str(int(bbs[2]) + int(bbs[0]))))
	Ymax = doc.createElement('ymax')
	Bndbox.appendChild(Ymax)
	Ymax.appendChild(doc.createTextNode(str(int(bbs[3]) + int(bbs[1]))))
	'''
	notice:
	xmin: x
	ymin: y
	xmax: x + w
	ymax: y + h
	'''

	with open(os.path.join(save_path,os.path.splitext(txt_name)[0] + '.xml'),'w') as f:
	    f.write((doc.toxml(encoding='utf-8')).decode('utf8'))


def main_old():
	'''
	txt都是单个小文件。形如100000.txt。内容:
	bbGT ~
	label1 x y w h 0 0 0 0 0 0 0
	label2 x y w h 0 0 0 0 0 0 0
	'''
	txt_path = './warp/warpTxt/'
	img_path = './warp/warpImg/'
	save_annotations_path = './Annotations/'
	
	txt_names = []
	file_name(txt_names,txt_path)
	cnt = 0
	total = len(txt_names[0])
	for txt in txt_names[0]:
		cnt += 1
		if(cnt % 10 == 0):
			print('has processed %d,total:%d' % (cnt,total))
		with open(txt_path + txt,'r') as f:
			lines = f.readlines()
			for line in lines:		
				if 'bbGt' in line:
					continue	
				info = line.split()
				#print(info)
				#label,x,y,bbsw,bbsh = info[:5]
				img = cv.imread(img_path + txt[:6] + '.jpg')
				#h,w,deep = img.shape #
				#print(label,x,y,bbsw,bbsh,h,w,deep)
				label,bbs = info[0],info[1:5] # 标签，包围框坐标,str
				resolution,channel = (img.shape[1],img.shape[0]),img.shape[2] # 分辨率，通道数,int
				#print(label,bbs,resolution,channel)
				createVOC2007xml(save_annotations_path,txt,label,bbs,resolution,channel)


def main():
	'''
	txt 是用 val.py计算出来的形式。
	'''
	txt_path = './test_results.txt'
	img_path = './VOC2007/JPEGImages'
	save_annotations_path = './VOC2007/Annotations'

	cnt_line = 0
	with open(txt_path,'r') as f:
		lines = f.readlines()
		total = len(lines)
		for line in lines:		
			if 'filename' in line:
				filename = line.split()[1]
				img = cv.imread(os.path.join(img_path,filename))
				resolution,channel = (img.shape[1],img.shape[0]),img.shape[2]
				cnt_line += 1
				continue
			if 'info' in line:
				info = line.split()
				label,bbs = info[1],info[3:7]
				cnt_line += 1
				continue
			if 'END' in line:
				createVOC2007xml(save_annotations_path,filename,label,bbs,resolution,channel)
				cnt_line += 1
			if(cnt_line % 500 == 0):
				print('has processed %6f%%' % (100 * cnt_line / total))
		print('has processed %6f%%' % (100 * cnt_line / total))

if __name__ == '__main__':
	main()
