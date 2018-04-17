import os
import sys
import shutil
from jinbo_os_lib import file_name,postfix,isimg

JPEGImages = './test/JPEGImages/'
Annotations = './test/Annotations-class2/'
do_not_need_xml = './test/do_not_need_xml/'

imgnames = []
xmlnames = []
def file_name(names,file_dir):   
	for root, dirs, files in os.walk(file_dir):  
		#print('root:',root) #当前目录路径  
		#print('dirs:',dirs) #当前路径下所有子目录
		#print('files:',files) #当前路径下所有非目录子文件
		names.append(files)
file_name(imgnames,JPEGImages)
file_name(xmlnames,Annotations)
for xml in xmlnames[0]:
	if postfix(xml)[0] not in [postfix(x)[0] for x in imgnames[0]]:
		shutil.move(Annotations + xml,do_not_need_xml + xml)
#print(imgnames[0])
#print(xmlnames[0])
