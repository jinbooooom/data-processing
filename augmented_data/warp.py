# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-8
function: Rotate transform and calculate new coordinates.
notice:The data format default as same as YOLO.
"""

import os
import sys
import math
import cv2 as cv
sys.path.append("..")
import jinbo_lib.my_os as jinbo
from os.path import join as opj
from jinbo_lib.image import warpAffine
pi = 3.141593


def newPosition(old, w, h, dushu):
	"""
	:param old: The coordinates on the original image, list[xmin, ymin, bboxw, bboxh]
	:param w, h: The width and height of the original image.
	:param dushu: Angle, not radian
	:return: The coordinates on the new image
	"""
	angle = abs(dushu * pi / 180)  # Convert to radians
	# Because the positive number is clockwise,
	# the positive number in the previous C file represents counterclockwise
	dushu = -dushu
	bbox = [0, 0, 0, 0]
	if(dushu >= 0):	
		bbox[0] = old[1] * math.sin(angle) + old[0] * math.cos(angle)
		bbox[1] = old[1] * math.cos(angle) + (w - old[0] - old[2]) * math.sin(angle)
	else:
		bbox[0] = (h - old[1] - old[3]) * math.sin(angle) + old[0] * math.cos(angle)
		bbox[1] = old[0] * math.sin(angle) + old[1] * math.cos(angle)
	bbox[2] = old[2] * math.cos(angle) + old[3] * math.sin(angle)
	bbox[3] = old[2] * math.sin(angle) + old[3] * math.cos(angle)
	return bbox


if __name__ == '__main__':
	gap = 100
	init_name = 800000  # new name
	cnt = 0  # statistics
	# The optional parameter of data_format:[VOC2007,YOLO].
	# VOC2007:[xmin, ymin, xmax, ymax].
	# YOLO:[xcentre, ycentre, bboxw, bboxh]
	data_format = 'YOLO'
	oriImgPath = '../data/my_VOC2007/JPEGImages'
	oriTxtPath = '../data/my_VOC2007/labels'
	warpImgPath = '../data/my_VOC2007/warp/imgs'
	warpTxtPath = '../data/my_VOC2007/warp/labels'
	jinbo.mkdir(warpImgPath)
	jinbo.mkdir(warpTxtPath)
	# Positive number --> clockwise.The absolute value of the angle cannot exceed 90
	angles = [-7, -3, 3, 7]
	oriImgNames = sorted(jinbo.get_file_names(oriImgPath))
	total = len(oriImgNames) * len(angles)

	for oriImgName in oriImgNames:
		img = cv.imread(opj(oriImgPath, oriImgName))
		h, w = img.shape[:2]
		for angle in angles:
			imgwarp = warpAffine(img, angle)
			new_h, new_w, _ = imgwarp.shape
			saveWarpImgPath = opj(warpImgPath,str(int(os.path.splitext(oriImgName)[0]) + init_name + cnt) + '.jpg')
			cv.imwrite(saveWarpImgPath, imgwarp)
			with open(opj(oriTxtPath, os.path.splitext(oriImgName)[0] + '.txt'), 'r') as f:
				lines = f.readlines()
				content = ''
				for line in lines:
					info = line.split()
					label = info[0]
					# pos = [int(x) for x in info[1:5]] # save format: xmin,ymin,w,h
					if(data_format == 'VOC2007'):
						pos = [float(info[1]),
								float(info[2]),
								float(info[3]) - float(info[1]),
								float(info[4]) - float(info[2])]
						# Eliminate 10,000 codes.
						# Customize it in your own style.

					if data_format == 'YOLO':
						"""
						save as YOLO foamat:XCentre,yCentre,w,h
						"""
						pos = [(float(info[1]) - float(info[3])/2.0) * w,
								(float(info[2]) - float(info[4])/2.0) * h,
								float(info[3]) * w,
								float(info[4]) * h]
						# now pos:[xmin, ymin, w, h], This is intput format of function newPosition(old, w, h, dushu)
						# print('old_bbox', pos)
						bbox = newPosition(pos, w, h, angle)  # h, w is ori_img's shape
						# print('new_bbox', bbox)
						# translate to [XCentre, yCentre, w, h]
						bbox = [(bbox[0] + bbox[2]/2.0) / new_w,
								(bbox[1] + bbox[3]/2.0) / new_h,
								bbox[2] / new_w,
								bbox[3] / new_h, ]

						content = content + label + ' ' + str(bbox[0]) + ' ' + str(bbox[1]) \
							+ ' ' + str(bbox[2]) + ' ' + str(bbox[3]) + '\n'
						pass

			with open(opj(warpTxtPath, str(int(os.path.splitext(oriImgName)[0]) + init_name + cnt) + '.txt'), 'w') as fw:
				fw.write(content)

			cnt += 1
			if cnt >= gap and cnt % gap == 0:
				print("has processed {:%}, {} files,".format(cnt / total, cnt))
			elif cnt == total:
				print("Mission completed! {:%}, {} files,".format(cnt / total, cnt))

