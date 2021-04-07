# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 14:05:35 2021

@author: 89748
"""

import cv2
import numpy as np
from HarrisCornerPointDetector import HarrisCornerPointDetector

img = cv2.imread('./img/easy.jpg',0)

#   创建Harris角点检测类
#   构造函数参数:(self,img,gaussian_filter_size,nonmaximum_size,r=0.04,threshold=0.01)
###   img:传入的灰度图像
###   gaussian_filter_size:产生g(Ixx)的时候采用的高斯滤波器的窗口大小
###   nonmaximum_size:做极大极小值抑制的时候的窗口大小
###   r:计算R的时候选择的k值,通常取0.04-0.06
###   threhold:最后筛选角点的时候响应度占最大响应度的比例的阈值
harris_detector = HarrisCornerPointDetector(img,gaussian_filter_size=5,nonmaximum_size=5,r=0.04,threshold=0.01)
#调用execute函数会返回根据响应度画圆圈的图像
img=harris_detector.execute()

cv2.namedWindow('img')
cv2.imshow("img",img)

cv2.waitKey(0)
