# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2019-6-8
function: Crop each object in the original image and save it to folder ./createNewImg/material. Combine the saved image with the original image to synthesize a new image for training.
notice:The input and output format of labels default as same as YOLO.
"""

import cv2
import os
import jinbo_lib.my_os as jinbo
from os .path import join as opj
import numpy as np
import random

if __name__ == "__main__":
    # classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'local', 'point']  # classes for datasets
    num_classes = 12
    VOC_path = "/home/jinbo/gitme/data-processing/data/led/VOC2007"
    crop_name_cnt = 100000
    new_name_cnt = 600000
    cnt = 0
    gap = 100
    want = 500
    # 创建由 digit_col 个数字字符和站digit_point 个小数点字符组成的字符串
    digit_col = 4
    digit_point = 2
    crop_and_save = False  # 是否已经从原图里裁剪出了各个类别，若是则不再执行该操作

    # Create dir
    createNewImg_path = opj(VOC_path, 'createNewImg')
    new_imgs_path = opj(createNewImg_path, 'imgs')
    material_path = opj(createNewImg_path, 'material')
    new_labels_path = opj(createNewImg_path, 'labels')
    jinbo.mkdir(new_imgs_path)
    jinbo.mkdir(new_labels_path)
    [jinbo.mkdir(opj(material_path, str(x))) for x in range(num_classes)]

    img_names = sorted(jinbo.get_file_names(opj(VOC_path, 'JPEGImages')))
    yolo_names = sorted(jinbo.get_file_names(opj(VOC_path, 'labels')))
    total = len(img_names)

    # Prepare to crop images
    if crop_and_save:
        print("已经从原图里裁剪出了各个类别")
    else:
        for img_name, yolo_name in zip(img_names, yolo_names):
            img = cv2.imread(opj(VOC_path, 'JPEGImages', img_name))
            im_h, im_w, channel = img.shape
            with open(opj(VOC_path, 'labels', yolo_name), 'r') as f:
                for info in f.readlines():
                    info = info.strip().split()
                    label = int(info[0])
                    cx, cy, w, h = [float(x) for x in info[1:]]
                    xmin = int((cx - w/2) * im_w)
                    ymin = int((cy - h/2) * im_h)
                    xmax = int((cx + w/2) * im_w)
                    ymax = int((cy + h/2) * im_h)

                    ymin = ymin if ymin > 0 else 1
                    ymax = ymax if ymax < im_h else im_h - 1
                    xmin = xmin if xmin > 0 else 1
                    xmax = xmax if xmax < im_w else im_w - 1

                    tmpImg = img[ymin:ymax, xmin:xmax]
                    crop_name_cnt += 1
                    crop_img_name = opj(material_path, str(label), str(crop_name_cnt) + '.jpg')
                    cv2.imwrite(crop_img_name, tmpImg)

                cnt += 1
                if cnt >= gap and cnt % gap == 0:
                    print("Crop phase has processed {:%}, {} files,".format(cnt / total, cnt))
                elif cnt == total:
                    print("Crop phase has processed {:%}, {} files,".format(cnt / total, cnt))

    # Create new images
    cnt = 0
    crop_imgs_path = []
    for x in range(num_classes):
        x_names = jinbo.get_file_names(opj(material_path, str(x)))
        x_path = [opj(material_path, str(x), y) for y in x_names]
        crop_imgs_path.append(x_path)  # crop_imgs_path[i] 指所有类别为 i 的 crop 图的路径的集合

    for epoch in range(want):
        if cnt >= want:  # 若没有这个条件，将循环 want * len(img_name) 次
            break
        for img_name, yolo_name in zip(img_names, yolo_names):
            if cnt >= want:  # 若没有这个条件，将循环 want * len(img_name) 次
                break
            img = cv2.imread(opj(VOC_path, 'JPEGImages', img_name))
            im_h, im_w, channel = img.shape
            with open(opj(VOC_path, 'labels', yolo_name), 'r') as f:
                new_content = ''
                for info in f.readlines():
                    info = info.strip().split()
                    label = int(info[0])
                    cx, cy, w, h = [float(x) for x in info[1:]]
                    xmin = int((cx - w / 2) * im_w)
                    ymin = int((cy - h / 2) * im_h)
                    xmax = int((cx + w / 2) * im_w)
                    ymax = int((cy + h / 2) * im_h)

                    ex = 0.05
                    ymin = int(ymin - w * im_w * ex)
                    ymax = int(ymax + w * im_w * ex)
                    xmin = int(xmin - h * im_h * ex)
                    xmax = int(xmax + h * im_h * ex)

                    ymin = ymin if ymin > 0 else 1
                    ymax = ymax if ymax < im_h else im_h - 1
                    xmin = xmin if xmin > 0 else 1
                    xmax = xmax if xmax < im_w else im_w - 1

                    if label != 10:
                        if label != 11:
                            r_d = random.randint(0, num_classes - 3)  # 不包括类别10和11
                        else:
                            r_d = 11
                        r_im = random.choice(crop_imgs_path[r_d])
                        im = cv2.imread(r_im)

                        im = cv2.resize(im, (xmax - xmin, ymax - ymin))
                        #print(img[ymin:ymax, xmin:xmax].shape)
                        img[ymin:ymax, xmin:xmax] = im
                    else:
                        r_d = 10

                    new_content = new_content + str(r_d) + ' ' \
                                  + str((xmax + xmin)/2.0 /im_w) + ' ' \
                                  + str((ymax + ymin)/2.0 / im_h) + ' ' \
                                  + str((xmax - xmin) / im_w) + ' ' \
                                  + str((ymax - ymin) / im_h) + '\n'



            cnt += 1
            if cnt >= gap and cnt % gap == 0:
                print("Create new images phase has processed {:%}, {} files,".format(cnt / want, cnt))
            elif cnt == total:
                print("Create new images phase has processed {:%}, {} files,".format(cnt / want, cnt))

            new_name_cnt += 1
            new_img_name = opj(new_imgs_path, str(new_name_cnt) + '.jpg')
            cv2.imwrite(new_img_name, img)

            with open(opj(new_labels_path, str(new_name_cnt) + '.txt'), 'w') as fw:
                fw.write(new_content)

    pass
