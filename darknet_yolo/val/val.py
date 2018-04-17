# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-14
function: 
"""

import os,sys
import xml.dom.minidom
from xml.etree import ElementTree as ET

yolo_test = './yolo_test-c2g4w.txt'
test_set = './2007_test.txt' # test sets,record all test image path
save_result = './test_results.txt'
Annotations = './VOC2007_7316c2/Annotations'

labels = ['abnormal','normal']

def read_xml(Annotations,filename): 
	filename = os.path.splitext(filename)[0] + '.xml'
	per = ET.parse(os.path.join(Annotations,filename))
	p = per.findall('./object')
	labels_xml1 = []
	for label in p:		
		for child in label.getchildren():
			if child.tag == 'name':
				#print(child.tag,':',child.text)
				labels_xml1.append(child.text)
				#print(labels_xml1)
	return labels_xml1

def processing_data():
	if(os.path.exists(save_result)):
		print('Please delete the existing files: %s' % save_result)
		exit(0)
	first = True
	with open(yolo_test,'r') as f:
		lines = f.readlines()
		for line in lines:
			#file_name = os.path.split(line)
			#print(file_name)
			with open(save_result,'a') as fsave:
				if('JPEGImages' in line):
					if(first):
						first = False
					else:
						fsave.write('END\n')	
					file_name = os.path.split(line[:-33])[1]
					fsave.write('filename ' + file_name + '\n')
					has_label = 0
				elif line.split(':')[0] in labels:		
					label,probability = line.split(':')[0],line.split(':')[1].split()[0]
					#print(line.split(':')[1].split()[0]) # obtain the probability of a target				
					has_label = 1
					fsave.write('info ' + label + ' ' + probability + ' ')
				elif(has_label): # Each label has a corresponding coordinate
					position = line.split()
					for x in position:
						fsave.write(x + ' ')
					fsave.write('\n')
					has_label = 0
		with open(save_result,'a') as fsave:
			fsave.write('END\n')

def accurary(): # Statistical accuracy for single target
	true_label = 0
	false_label = 0
	with open(save_result,'r') as f:
		lines = f.readlines()
		for line in lines:
			line_list = line.split()
			if line_list[0] == 'filename':
				filename = line_list[1]			
				prediction = []
			elif line_list[0] == 'info':
				prediction.append(line_list[1]) # only obtain label.			
			else: # line_list == 'END' 
				print('%s :' % filename)
				print('predictive labels :',prediction)
				#print('\n')
				'''
				filename = os.path.splitext(filename)[0] + '.xml'
				per = ET.parse(os.path.join(Annotations,filename))
				p = per.findall('./object')
				labels_xml1 = []
				for label in p:				
					for child in label.getchildren():
						if child.tag == 'name':
							#print(child.tag,':',child.text)
							labels_xml1.append(child.text)
							#print(labels_xml1)
				'''
				labels_xml = []
				labels_xml = read_xml(Annotations,filename)
				print('the correct labels: ',labels_xml)
				if(len(labels_xml) == 1):
					if(len(prediction) == 1 and labels_xml[0] == prediction[0]):
						true_label += 1
					else:
						false_label += 1
				else:
					print('The XML file contains multiple labels. Do not participate in Statistics.')
				if(true_label + false_label):
					print('true:%d  false:%d  precision:%f%%' % (true_label,false_label,true_label / (true_label + false_label) * 100))		
	#print(true_label / (true_label + false_label))				
				

def main():
	#processing_data()
	accurary()

if __name__ == '__main__':
	main()




































