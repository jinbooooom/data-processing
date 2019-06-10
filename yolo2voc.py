# -*- coding: utf-8 -*-
"""
@author: Jinbo
time: 2019-6-8
function: Convert .txt file in YOLO format to .xml file in VOC format.
"""

import cv2
import os
import jinbo_lib.my_os as jinbo

xml_head = '''<annotation>
    <folder>JPEGImages</folder>
    <filename>{}</filename>
    <path>{}</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>{}</width>
        <height>{}</height>
        <depth>{}</depth>
    </size>
    <segmented>0</segmented>
    '''

xml_obj = '''<object>
        <name>{}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>
    '''
xml_end = '''</annotation>
'''


VOC_path = "/home/jinbo/data/VOCdevkit/VOC2007"  # 仿照VOC2007格式创建文件夹，把YOLO格式的标签放在VOC2007下的labels文件夹下
classes = ['0','1','2','3','4','5','6','7','8','9','local','point']  # classes for datasets


if __name__ == "__main__":
    yolo_names = sorted([x for x in os.listdir(os.path.join(VOC_path, 'labels'))])
    jpg_names = sorted([x for x in os.listdir(os.path.join(VOC_path, 'JPEGImages'))])
    jinbo.mkdir('./Annotations')

    total = len(yolo_names)
    cnt = 0
    gap = 100  # 每隔 gap 次打印信息

    for yolo_name, jpg_name in zip(yolo_names, jpg_names):
        jpg_name = os.path.join(VOC_path, 'JPEGImages', jpg_name)
        im = cv2.imread(jpg_name)
        im_h, im_w, channel = im.shape
        head = xml_head.format(os.path.split(jpg_name)[1], jpg_name, im_w, im_h, channel)

        obj = ''
        with open(os.path.join(VOC_path, 'labels', yolo_name)) as f_yolo:
            for info in f_yolo.readlines():
                info = info.strip().split()
                label = int(info[0])
                cx, cy, w, h = [float(x) for x in info[1:]]
                xmin = int((cx - w/2) * im_w)
                ymin = int((cy - h/2) * im_h)
                xmax = int((cx + w/2) * im_w)
                ymax = int((cy + h/2) * im_h)
                obj += xml_obj.format(classes[label], xmin, ymin, xmax, ymax)

        xml_name = yolo_name.replace('.txt', '.xml')
        xml_path = os.path.join(VOC_path, 'Annotations', xml_name)
        with open(xml_path, 'w') as f_xml:
            f_xml.write(head + obj + xml_end)

        cnt += 1
        if cnt >= gap and cnt % gap == 0:
            print("has processed {:%}, {} files,".format(cnt/total, cnt))
        elif cnt == total:
            print("has processed {:%}, {} files,".format(cnt/total, cnt))


