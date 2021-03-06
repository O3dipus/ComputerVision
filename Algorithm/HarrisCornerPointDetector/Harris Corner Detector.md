# Harris Corner Detector

**Key property:** in the region around a corner, image gradient has two or more dominant directions

Corners are **repeatable** and **distinctive**



**Intuitively:** when shifting a window in any direction,corner should give a large change

![image-20210407180454187](C:\Users\89748\AppData\Roaming\Typora\typora-user-images\image-20210407180454187.png)



The change of intensity level can be describe as $S_x(\Delta x,\Delta y)=\Sigma _{(x_i,y_i)\in w}(f(x+\Delta x,y+\Delta y)-f(x,y))^2$

$\because f(x+\Delta x,y+\Delta y)\approx f(x,y)+\Delta{x}\frac{\partial{f(x,y)}}{\partial{x}}+\Delta{y}\frac{\partial{f(x,y)}}{\partial{y}}$

$\therefore S_x(\Delta{x},\Delta{y})=(\Delta{x}\frac{\partial{f(x,y)}}{\partial{x}}+\Delta{y}\frac{\partial{f(x,y)}}{\partial{y}})^2$ 

$\Delta{x}\frac{\partial{f(x,y)}}{\partial{x}}+\Delta{y}\frac{\partial{f(x,y)}}{\partial{y}}=\begin{bmatrix} \frac{\partial{f(x,y)}}{\partial{x}} &\frac{\partial{f(x,y)}}{\partial{y}}\end{bmatrix} \begin{bmatrix} \Delta{x}\\ \Delta{y}\end{bmatrix}$

$S_x(\Delta{x},\Delta{y})=\begin{bmatrix} \Delta{x}\\ \Delta{y}\end{bmatrix}^T \Sigma\begin{bmatrix} \frac{\partial{f(x,y)}}{\partial{x}}^2&\frac{\partial{f(x,y)}}{\partial{x}}\frac{\partial{f(x,y)}}{\partial{y}}\\ \frac{\partial{f(x,y)}}{\partial{x}}\frac{\partial{f(x,y)}}{\partial{y}}&\frac{\partial{f(x,y)}}{\partial{y}}^2\end{bmatrix} \begin{bmatrix} \Delta{x}\\ \Delta{y}\end{bmatrix}$

$M=\begin{bmatrix}I_x^2&I_xI_y\\I_xI_y&I_y^2\end{bmatrix}$

$M\ is\ a\ real\ symmetric\ matrix(also\ a\ semidefinite\ matrix,which\ leads\ to\ the\ simplication\ of\ response\ measurement)$

$diagonalization:M=R^{-1}\begin{bmatrix}\lambda_1&0\\0&\lambda_2\end{bmatrix}R$

$R=detM-k(traceM)^2=\lambda_1\lambda_2-k(\lambda_1+\lambda_2)^2$

$k=0.04-0.06$



## Step of HCPD

1. Calculate   $I_x,I_y$

2. Calculate  $I_x^2,I_y^2,I_xI_y$

3. Gaussian Filtering $g(I_x^2),g(I_y^2),g(I_xI_y)$
4. Caluculate Cornerness Function $R=g(I_x^2)g(I_y^2)-[g(I_xI_y)]^2-\alpha[g(I_x^2)+g(I_y^2)]^2$
5. Nonmaximum Suppression



## Python

```python
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
    
    #????????????Harris???????????????????????????????????????????????????
    def execute(self):
        self.derivative()
        self.gaussian()
        self.calculateR(self.r)
        threshold=self.R.max()*self.threshold
        self.nonmaximam_suppression(threshold)
        self.draw_circle()
    
        return self.img
    
    #????????????????????????Ix,Iy,????????????Ix^2,Iy^2,Ix*Iy
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
    
    #???????????????Ix2,Iy2,Ixy??????????????????
    def gaussian(self):
        self.gIx2=self.gaussian_filtering(self.Ix2, self.gaussian_filter_size)
        self.gIy2=self.gaussian_filtering(self.Iy2, self.gaussian_filter_size)
        self.gIxy=self.gaussian_filtering(self.Ixy, self.gaussian_filter_size)
        
        return self.gIx2,self.gIy2,self.gIxy
    
    #?????????????????????R
    def calculateR(self,k):
        self.R=self.gIx2*self.gIy2-self.gIxy**2-k*(self.gIx2+self.gIy2)**2
        return self.R
    
    #?????????????????????????????????????????????????????????
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
    
    #?????????????????????????????????
    def draw_circle(self):
        self.img=np.uint8(self.img)
        self.img=cv2.cvtColor(self.img,cv2.COLOR_GRAY2BGR)

        for i in range(self.res.shape[0]):
            for j in range(self.res.shape[1]):
                if self.res[i,j]!=0:
                    r = int(round(float(self.res[i,j])/3))
                    cv2.circle(self.img,(j,i),r,(0, 0, 255))
    
    #???????????????????????????
    def gaussian2d(self,sigma,window_size):
        radius = (window_size-1) // 2
        
        gauss=np.zeros([window_size,window_size])
        
        for i in range(-radius,radius+1):
            for j in range(-radius,radius+1):
                gauss[i+radius,j+radius]=np.exp(-(i**2+j**2)/(2*sigma**2))
                
        gauss=gauss/gauss.sum()
        
        return gauss
    
    #??????????????????????????????????????????
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
        
        
    
    
```

