# Automatic Scale Selection

**Preview:**

> Harris Corner Point Detector is an effective way to capture feature point in an image. Though it's rotation invariance, it's not the best way for paranomo stitching due to its invariance to image scale tranformation.

Intuitively, It's a good way to construct a function $f(scale)$ to find characristic region size.

## 0.SIFT Preview

### 0.1 Gaussian Cell Function Characristics

- Scale-invariant cell function
- Can be approximated by DoG (***Why***)

### 0.2 Definition of $L(x,y,\sigma)$

$L(x,y,\sigma)=\frac{1}{2\pi\sigma^2}exp(-\frac{(x-x_i)^2+(y-y_i)^2}{2\sigma^2})$

$L(x,y,\sigma)=G(x,y,\sigma)*I(x,y)$

### 0.3 Steps

1. filter out feature points
2. locate feature points and define their directions
3. build descriptor
4. match

## 1.Common Approach Of Scale Selection 

Build a function which is "scale invariant" and take a local **extremum** of the function.The extremum is achieved should be **covariant to image scale**; this scale covariant region size is found in each image independently.

**Good function:** on stable sharp peak response to region size.

![image-20210408213230353](C:\Users\89748\AppData\Roaming\Typora\typora-user-images\image-20210408213230353.png)

## 2.Laplacian-of-Gaussian And Characristic Scale

We define the **characteristic scale** as the scale that produces peak of scale‐normalized **Laplacian‐of‐Gaussian** response.



**Spatial selection:** the magnitude of the scale‐normalized Laplacian‐of‐Gaussian response will achieve an extremum at the center of the blob, provided that its scale is “matched” to the scale of the blob

