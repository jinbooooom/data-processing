import cv2 as cv
import numpy as np

def warpAffine(image, angle):  
        # grab the dimensions of the image and then determine the  
        # center  
	(h, w) = image.shape[:2]  
	(cX, cY) = (w // 2, h // 2)  
      
# grab the rotation matrix (applying the negative of the  
        # angle to rotate clockwise), then grab the sine and cosine  
        # (i.e., the rotation components of the matrix)  
	M = cv.getRotationMatrix2D((cX, cY), -angle, 1.0)  
	cos = np.abs(M[0, 0])  
	sin = np.abs(M[0, 1])  
      
        # compute the new bounding dimensions of the image  
	nW = int((h * sin) + (w * cos))  
	nH = int((h * cos) + (w * sin))  
      
        # adjust the rotation matrix to take into account translation  
	M[0, 2] += (nW / 2) - cX  
	M[1, 2] += (nH / 2) - cY      
        # perform the actual rotation and return the image
	return cv.warpAffine(image, M, (nW, nH))

def mirror(image,op = 'LR'):
	'''
	op = 'LR',flip_left_right
	op = 'UD',flip_up_down
	'''
	h,w = image.shape[:-1]
	if(op == 'LR' or op == 'lr'):
		iLR = np.zeros(image.shape)
		for c in range(w // 2):
			iLR[:,w - 1 - c],iLR[:,c] = image[:,c],image[:,w - 1 - c]
		return iLR
	elif(op == 'UD' or op == 'ud'):
		iUD = np.zeros(image.shape)
		for r in range(h // 2):
			iUD[h - 1 - r],iUD[r] = image[r],image[h - 1 - r]
		return iUD
	else:
		print('Please enter the operation you need')
		#pass









