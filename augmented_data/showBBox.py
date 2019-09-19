# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2018-4-8
function: Visualized bounding box.
notice:The txt file's data format:[xmin,ymin,bboxw,bboxh].
"""

import os
import sys
import cv2 as cv
import random
sys.path.append("..")
import jinbo_lib.my_os as jinbo


def main():
	oriImgPath = '../data/my_VOC2007/warp/imgs'
	oriTxtPath = '../data/my_VOC2007/warp/labels/'
	savePath = '../data/my_VOC2007/warp/bboxImages/'
	jinbo.mkdir(savePath)
	oriImgNames = sorted(jinbo.get_file_names(oriImgPath))
	total = len(oriImgNames)
	cnt = 1

	for oriImgName in oriImgNames:
		img = cv.imread(os.path.join(oriImgPath, oriImgName))
		h, w, _ = img.shape
		print('has processed %d,total:%d' % (cnt, total))
		with open(os.path.join(oriTxtPath, os.path.splitext(oriImgName)[0] + '.txt'), 'r') as f:
			lines = f.readlines()
			for line in lines:
				info = line.split()
				# print(info)
				info = info[:1] + [float(x) for x in info[1:5]]
				xmin = int((info[1] - info[3]/2) * w)
				ymin = int((info[2] - info[4]/2) * h)
				bboxw = int(info[3] * w)
				bboxh = int(info[4] * h)
				# print(info)

				label = info[0]
				# pos = [int(x) for x in info[1:5]]  # list[xmin, ymin, bboxw, bboxh]
				color = tuple(random.randint(0, 255) for _ in range(3))
				# cv.rectangle(img, (pos[0], pos[1]), (pos[0] + pos[2], pos[1] + pos[3]), color, 2)
				# cv.imwrite(os.path.join(savePath, oriImgName), img)
				cv.rectangle(img, (xmin, ymin), (xmin + bboxw, ymin + bboxh), color, 2)
				cv.imwrite(os.path.join(savePath, oriImgName), img)
		cnt = cnt + 1


if __name__ == '__main__':
	main()





