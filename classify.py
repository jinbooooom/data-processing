import os
import re
import cv2 as cv
import shutil


def isimg(img):
	img_feature = ['.jpg','.png','.bmp']
	for img_postfix in img_feature:
		if(img_postfix in img.lower()):
			return True
	return False

def postfix(filename):
	img_postfix = filename[len(filename)-3:len(filename)] # 获得文件后缀'jpg'
	img_name = filename[:len(filename)-3] # 把1.jpg分解成为img_name = '1.'，img_postfix = 'jpg'
	list_file_name = [img_name,img_postfix]
	return list_file_name

path = '/home/jinbo/program/test/'
dirs = ['oriimg','saveimg','othersimg','savetxt'] #path下含有4个文件夹
labels = ('Normal','Inclined','BentToDesk')

full_dir = [path + mydir + '/' for mydir in dirs] #这不是路径拼接是字符串相加所以要加一个'/'
#print(full_dir,sep="\n-------------\n")
oriimgs = os.listdir(full_dir[0]) #只有名称，如1.jpg，没有路径。
for oriimg in oriimgs: 
	if(isimg(oriimg)):
		oriimg_path = full_dir[0] + oriimg	#图片完整路径
		pic = cv.imread(oriimg_path) 
		# 这里注意oriimg是图片路径，是字符串，而pic是具体的图片，是mat
		#print(full_dir[0] + oriimg)
		cv.imshow(oriimg,pic)
		key = cv.waitKey() # time.sleep(秒)推迟进程来达到延迟，会造成图片全黑。
		if(key == ord('1')):
			try:			
				font = cv.FONT_HERSHEY_SIMPLEX
				#cv.putText(pic,'choice a label:',(int(pic.shape[0]/4),int(pic.shape[1]/2)), font, 1,(0,0,255),1)
				cv.putText(pic,'enter 1,2,3 again',(30,30), font, 1,(0,0,255),2)
				cv.putText(pic,'to choice a label:',(30,70), font, 1,(0,0,255),2)
				cv.imshow(oriimg,pic)
				key2 = cv.waitKey()
				if(key2 == ord('1')):
					label = labels[key2 - ord('1')] # Normal
					cv.putText(pic,'%s'%(label),(int(pic.shape[0]/3.0),int(pic.shape[1]/3.0)), font, 2,(0,0,255),2)
					cv.imshow(oriimg,pic)
					cv.waitKey(800)
				elif(key2 == ord('2')):
					label = labels[key2 - ord('1')] # Inclined
					cv.putText(pic,'%s'%(label),(int(pic.shape[0]/3.0),int(pic.shape[1]/3.0)), font, 2,(0,0,255),2)
					cv.imshow(oriimg,pic)
					cv.waitKey(800)
				elif(key2 == ord('3')):
					label = labels[key2 - ord('1')] # BentToDesk
					cv.putText(pic,'%s'%(label),(int(pic.shape[0]/3.0),int(pic.shape[1]/3.0)), font, 2,(0,0,255),2)
					cv.imshow(oriimg,pic)
					cv.waitKey(800)
				else:
					continue
					cv.destroyWindow(oriimg)
				#print(postfix(oriimg)[0],'+',postfix(oriimg)[1])
				
				txt_path = full_dir[3] + postfix(oriimg)[0] + 'txt'
				with open(txt_path,'w') as f:
					f.write("%s 0 %d %d %d %d 0 0 0 0 0 0 0\n"%(label,5,5,pic.shape[1] - 10,pic.shape[0] - 10)) # shape[0]:高
				shutil.move(oriimg_path,full_dir[1]) #按键1剪切图片到../test/saveimg
			except:
				print("移动 %s 到 %s失败！"%(oriimg_path,full_dir[1]))
		elif(key == ord('2')):
			try:
				shutil.move(oriimg_path,full_dir[2]) #按键2剪切图片到../test/othersimg
			except:
				print("移动 %s 到 %s失败！"%(oriimg_path,full_dir[2]))
		cv.destroyWindow(oriimg)
#print("test successfully",txt,sep='\n----------------\n',end='\n')
