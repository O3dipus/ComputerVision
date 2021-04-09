# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 21:50:44 2021

@author: 89748
"""

import cv2
import numpy as np

class GaussianMask:
    def __init__(self,img,sigma,window_size):
        self.img = img
        self.sigma = sigma
        self.window_size=window_size
        #产生高斯滤波的模板
    
    def execute(self):
        radius = (self.window_size-1) // 2
        
        pad=np.zeros([self.img.shape[0]+2*radius,self.img.shape[1]+2*radius])
        pad[radius:-radius,radius:-radius]=self.img
        self.res=np.zeros(self.img.shape)
        
        gauss_filter=self.gaussian2d()
        
        for i in range(radius,self.img.shape[0]+radius):
            for j in range(radius,self.img.shape[1]+radius):
                self.res[i-radius,j-radius]=(pad[i-radius:i+radius+1,j-radius:j+radius+1]*gauss_filter).sum()
        self.res = np.uint8(np.round(self.res))
        
        return self.res
    
    def set_sigma(self,sigma):
        self.sigma=sigma
    
    def gaussian2d(self):
        radius = (self.window_size-1) // 2
        
        gauss=np.zeros([self.window_size,self.window_size])
        
        for i in range(-radius,radius+1):
            for j in range(-radius,radius+1):
                gauss[i+radius,j+radius]=np.exp(-(i**2+j**2)/(2*self.sigma**2))
                
        gauss=gauss/gauss.sum()
        
        return gauss
    
    #对于图像（矩阵）进行高斯滤波

    