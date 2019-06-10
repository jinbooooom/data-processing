# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-12
function: Match Annotations and JPEGImages.
"""

import argparse
import os,sys,shutil

def get_file_names(dir_path):
	'''
	Don't contain folders,only files.
	'''
	return [x for x in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path,x))]

def arg_parse():
	parser = argparse.ArgumentParser(description='Match Annotations and JPEGImages')
	parser.add_argument("--img", dest = 'img', help = 
			"img / Path to the original image folder",
			default = "img", type = str)
	parser.add_argument("--xml", dest = 'xml', help = 
			"xml / Path to the xml folder",
			default = "xml", type = str)
	return parser.parse_args()

def match(Annotations,JPEGImages):
	'''
	Match Annotations and JPEGImages
	'''	
	no_xml = './do_not_need_xml'
	no_img = './do_not_need_img'
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


if __name__ == '__main__':
	args = arg_parse()
	img = args.img
	xml = args.xml
	match(xml,img)









