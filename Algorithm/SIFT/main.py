# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 21:50:42 2021

@author: 89748
"""

import cv2
import numpy as np

from GaussianFiltering import GaussianMask 

img = cv2.imread('./img/tjusse.jpg',0)
cv2.namedWindow('img')
cv2.imshow('img',img)

dst = GaussianMask(img,1,3)

gaussian=[img]
for i in range(1,6):
    dst.set_sigma(i)
    gaussian.append(dst.execute())
dog=[]
for i in range(5):
    dog.append(gaussian[i+1]-gaussian[i])

cv2.waitKey(0)
cv2.destroyAllWindows()