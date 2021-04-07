# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:48:01 2021

@author: 89748
"""
import numpy as np
import cv2

class HarrisCornerPointDetector:    
    def __init__(self,img,gaussian_filter_size,nonmaximum_size,r=0.04,threshold=0.01):
        self.img=img
        self.gaussian_filter_size=gaussian_filter_size
        self.nonmaximum_size=nonmaximum_size
        self.r=r
        self.threshold=threshold
        
        if self.img.dtype==np.dtype('uint8'):
            self.img=np.float64(self.img)
    
    #执行所有Harris角点检测的步骤，产生画圈的目标图像
    def execute(self):
        self.derivative()
        self.gaussian()
        self.calculateR(self.r)
        threshold=self.R.max()*self.threshold
        self.nonmaximam_suppression(threshold)
        self.draw_circle()
    
        return self.img
    
    #对于图像求导计算Ix,Iy,进而求得Ix^2,Iy^2,Ix*Iy
    def derivative(self):       
        pad=np.array([])
        pad.resize(self.img.shape[0]+2,self.img.shape[1]+2)
        
        Ix=np.zeros(self.img.shape)
        Iy=np.zeros(self.img.shape)
        
        pad[1:-1,1:-1]=self.img
        pad[0,1:-1]=self.img[0,:]
        pad[-1,1:-1]=self.img[-1,:]
        pad[1:-1,0]=self.img[:,0]
        pad[1:-1,-1]=self.img[:,-1]
        
        for i in range(1,self.img.shape[0]+1):
            for j in range(1,self.img.shape[1]+1):
                Ix[i-1,j-1]=pad[i,j+1]-pad[i,j-1]
                Iy[i-1,j-1]=pad[i+1,j]-pad[i-1,j]
        self.Ix2=Ix*Ix
        self.Iy2=Iy*Iy
        self.Ixy=Ix*Iy
       
        return self.Ix2,self.Iy2,self.Ixy
    
    #对于求得的Ix2,Iy2,Ixy进行高斯滤波
    def gaussian(self):
        self.gIx2=self.gaussian_filtering(self.Ix2, self.gaussian_filter_size)
        self.gIy2=self.gaussian_filtering(self.Iy2, self.gaussian_filter_size)
        self.gIxy=self.gaussian_filtering(self.Ixy, self.gaussian_filter_size)
        
        return self.gIx2,self.gIy2,self.gIxy
    
    #计算响应度矩阵R
    def calculateR(self,k):
        self.R=self.gIx2*self.gIy2-self.gIxy**2-k*(self.gIx2+self.gIy2)**2
        return self.R
    
    #进行极大极小值抑制，同时加上阈值的筛选
    def nonmaximam_suppression(self,threhold):
        radius = (self.nonmaximum_size+1)//2
        
        pad=np.zeros([self.R.shape[0]+2*radius,self.R.shape[1]+2*radius])
        pad[radius:-radius,radius:-radius]=self.R
        res=np.zeros(self.R.shape)
        
        for i in range(radius,radius+self.R.shape[0]):
            for j in range(radius,radius+self.R.shape[1]):
                if pad[i,j]<pad[i-radius:i+radius+1,j-radius:j+radius+1].max() or pad[i,j]<threhold:
                    res[i-radius,j-radius]=0
                else:
                    res[i-radius,j-radius]=pad[i,j]
                    
        res=(res-res.min())*255/(res.max()-res.min())
        self.res=np.uint8(np.round(res))
        
        return self.res
    
    #在图像上面绘制响应度圆
    def draw_circle(self):
        self.img=np.uint8(self.img)
        self.img=cv2.cvtColor(self.img,cv2.COLOR_GRAY2BGR)

        for i in range(self.res.shape[0]):
            for j in range(self.res.shape[1]):
                if self.res[i,j]!=0:
                    r = int(round(float(self.res[i,j])/3))
                    cv2.circle(self.img,(j,i),r,(0, 0, 255))
    
    #产生高斯滤波的模板
    def gaussian2d(self,sigma,window_size):
        radius = (window_size-1) // 2
        
        gauss=np.zeros([window_size,window_size])
        
        for i in range(-radius,radius+1):
            for j in range(-radius,radius+1):
                gauss[i+radius,j+radius]=np.exp(-(i**2+j**2)/(2*sigma**2))
                
        gauss=gauss/gauss.sum()
        
        return gauss
    
    #对于图像（矩阵）进行高斯滤波
    def gaussian_filtering(self,mat,window_size):
        radius = (window_size-1) // 2
        
        pad=np.zeros([mat.shape[0]+2*radius,mat.shape[1]+2*radius])
        pad[radius:-radius,radius:-radius]=mat
        res=np.zeros(mat.shape)
        
        gauss_filter=self.gaussian2d(1,window_size)
        
        for i in range(radius,mat.shape[0]+radius):
            for j in range(radius,mat.shape[1]+radius):
                res[i-radius,j-radius]=(pad[i-radius:i+radius+1,j-radius:j+radius+1]*gauss_filter).sum()
                
        return res
        
        
    
    