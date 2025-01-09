# coding=utf-8
import os
import numpy as np
import cv2 as cv
import math
import random
#无齿痕切割，沿边缘切割
def gleftItem(rgbImage, CropImage, start_h, h, w):
    C_r = 0
    C_c = 0
    for row in range(start_h, h):
        b_r = False
        for col in range(w):
            pv0 = rgbImage[row, col, 0]
            pv1 = rgbImage[row, col, 1]
            pv2 = rgbImage[row, col, 2]
            if pv0 > 0 or pv1 > 0 or pv2 > 0:        #从舌体中段开始向下，从左到右判断像素体是否为舌体，判断为舌体边缘时停止
                print(row, col)
                C_r = row
                C_c = col
                b_r = True
                break
        if b_r == True:
            print('stop----------------------')
            break
    if C_c < 128:
        imCrop = CropImage[C_r - 128:C_r + 128, 0: 256]
    else:
        imCrop = CropImage[C_r - 128:C_r + 128, C_c - 128 : C_c+ 128]
    return C_r, C_c, imCrop

def genleftBox(path, fileName, N=10):
    # 沿舌头左边边缘切割
    print('file name============', fileName)
    imagename = path + 'tong.png'
    rgbImage = cv.imread(imagename, cv.IMREAD_COLOR)
    CropImage = cv.imread(imagename, cv.IMREAD_COLOR)
    h, w, c = rgbImage.shape
    step = 50 #步长
    start_h = int(h / 2)
    #找到第一个像素点
    C_r, C_c, imCrop = gleftItem(rgbImage, CropImage, start_h, h, w)
    cv.imwrite(path + fileName + '_' + str(0) + '.png', imCrop)
    for i in range(1, int(N/2)):
        C_r, C_c, imCrop = gleftItem(rgbImage, CropImage, C_r + step * i, h, w)
        if len(imCrop) > 0:
            cv.imwrite(path + fileName + '_' + str(i) + '.png', imCrop)      #截取舌体边缘图像

def gRightItem(rgbImage, CropImage, start_h, h, w):
    C_r = 0
    C_c = 0
    for row in range(start_h, h):
        b_r = False
        for col in range(w - 1, -1, -1):
            pv0 = rgbImage[row, col, 0]
            pv1 = rgbImage[row, col, 1]
            pv2 = rgbImage[row, col, 2]
            if pv0 > 0 or pv1 > 0 or pv2 > 0:
                print(row, col)
                C_r = row
                C_c = col
                b_r = True
                break
        if b_r == True:
            print('stop----------------------')
            break
    if C_c < 128:
        imCrop = CropImage[C_r - 128:C_r + 128, 0: 256]
    else:
        imCrop = CropImage[C_r - 128:C_r + 128, C_c - 128: C_c + 128]
    return C_r, C_c, imCrop
def genrightBox(path, fileName, N=10):
    #沿舌头右边边缘切割
    print('file name============', fileName)
    imagename = path + 'tong.png'
    rgbImage = cv.imread(imagename, cv.IMREAD_COLOR)
    CropImage = cv.imread(imagename, cv.IMREAD_COLOR)
    h, w, c = rgbImage.shape
    step = 50
    start_h = int(h / 2)
    #找到第一个像素点
    C_r, C_c, imCrop = gRightItem(rgbImage, CropImage, start_h, h, w)
    cv.imwrite(path + fileName + 'right_' + str(0) + '.png', imCrop)
    for i in range(1, int(N/2)):
        C_r, C_c, imCrop = gRightItem(rgbImage, CropImage, C_r + step * i, h, w)
        if len(imCrop) > 0:
            cv.imwrite(path + fileName + 'right_' + str(i) + '.png', imCrop)
def scan_files(directory):
    for root, sub_dirs, files in os.walk(directory):
       print(sub_dirs)
       if len(sub_dirs) > 0 :
           for sdir in sub_dirs:
                print(sdir)
                str = root +'/' + sdir
                #index = str.find('_0_')
                #print(str[0:index])
                genleftBox(str + '/', sdir)
                genrightBox(str + '/', sdir)
                #os.rename(str, str[0:index])
path = "F:/opencv_ins/TT/140829091953/tong.png"
#genleftBox('F:/opencv_ins/test/140825091314/', '140825091314', 100)
#genrightBox('F:/opencv_ins/test/140825091314/', '140825091314', 100)
#path = "G:\\1000tongue\\东直门\\0"
for i in range(1, 5):
    print(i)
scan_files(path)