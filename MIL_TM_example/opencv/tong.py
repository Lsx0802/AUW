# coding=utf-8
#G:\1000tongue\东直门\0
import os
import numpy as np
import cv2 as cv
import math
#生成tong.png
def gen(path):
    imagename = path + 'label.png'
    ssImg = path + 'img.png'
    labelImage = cv.imread(imagename, cv.IMREAD_COLOR)
    imgImage = cv.imread(ssImg, cv.IMREAD_COLOR)
    print(labelImage.shape)
    print(imgImage.shape)
    h, w, c = labelImage.shape
    for row in range(h):
        for col in range(w):
            pv1 = labelImage[row, col, 0]         #蓝色分量
            pv2 = labelImage[row, col, 1]         #绿色分量
            pv3 = labelImage[row, col, 2]         #红色分量
            if pv1 > 0 or pv2 > 0 or pv3 > 0:
                labelImage[row, col, 0] = 255
                labelImage[row, col, 1] = 255
                labelImage[row, col, 2] = 255
    hh = cv.bitwise_and(imgImage, labelImage)     #与运算提取边界
    if os.path.exists(path + 'tt.png'):
        os.remove(path + 'tt.png')
    cv.imwrite(path + 'tong.png', hh)

def scan_files(directory):
    for root, sub_dirs, files in os.walk(directory):
       print(sub_dirs)
       if len(sub_dirs) > 0 :
           for sdir in sub_dirs:
                print(sdir)
                str = root +'/' + sdir
                #index = str.find('_0_')
                #print(str[0:index])
                gen(str + '/')
                #os.rename(str, str[0:index])
path = "F:/opencv_ins/TT/140829091953/tong.png"
#path = "G:\\1000tongue\\东直门\\0"
scan_files(path)
