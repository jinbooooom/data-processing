# -*- coding: utf-8 -*-
"""
function:
根据已生成的xml，制作VOC2007数据集中的trainval.txt;train.txt;test.txt和val.txt  
trainval占总数据集的50%，test占总数据集的50%；train占trainval的50%，val占trainval的50%；  
上面所占百分比可根据自己的数据集修改，如果数据集比较少，test和val可少一些  

""" 

import os,sys
import random

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

xmlfilepath = './Annotations'
txtsavepath = './ImageSets/Main'
mkdir(xmlfilepath)
mkdir(txtsavepath)
trainval_percent = .2  # trainval占整个数据集的百分比，剩下部分就是test所占百分比
train_percent = .8  # train占trainval的百分比，剩下部分就是val所占百分比

names = [x for x in os.listdir(xmlfilepath)]
total = len(names)
test_num = int(total * (1 - trainval_percent))
train_num = int(total * trainval_percent * train_percent)
# print(names)
print('total:%d, test:%d, train:%d, val:%d.' % (total, test_num, train_num, total - test_num - train_num))
random.shuffle(names)
# names = random.sample(names[0],total) #这行也可以：随机返回names[0]中total个元素
# print(names)
with open(os.path.join(txtsavepath, 'test.txt'), 'w') as ftest:
	test = names[:test_num]
	# print(test)
	for x in test:
		ftest.write(x[:6] + '\n')
with open(os.path.join(txtsavepath, 'train.txt'), 'w') as ftrain:
	train = names[test_num:test_num + train_num]
	for x in train:
		ftrain.write(x[:6] + '\n')
with open(os.path.join(txtsavepath, 'val.txt'), 'w') as fval:
	val = names[test_num + train_num:]
	for x in val:
		fval.write(x[:6] + '\n')
with open(os.path.join(txtsavepath, 'trainval.txt'), 'w') as ftrainval:
	trainval = names[test_num:]
	for x in trainval:
		ftrainval.write(x[:6] + '\n')	


