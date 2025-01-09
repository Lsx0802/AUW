#G:\1000tongue\东直门\0
import os
import numpy as np
import cv2 as cv
import math
import time
from PIL import Image
#切割齿痕区域
def genBox(path_cul):
    # print('file name============', fileName)
    # imagename = path + 'tong.png'
    rgbImage = cv.imread(path_cul, cv.IMREAD_COLOR)
    h, w, c = rgbImage.shape
    fator = 48
    for row in range(h):
        for col in range(w):
            for t in range(c):
                pv = rgbImage[row, col, t]
                rgbImage[row, col, t] = math.floor(pv / fator) * fator
    rgbImage = cv.cvtColor(rgbImage, cv.COLOR_RGB2GRAY)
    rgbImage = cv.resize(rgbImage, (224, 224))
    min = rgbImage[0, 0]
    for r in range(h):
        for c in range(w):
            pv = rgbImage[r, c]
            if pv < min:
                min = pv
    # print("first min", min)
    smin = min
    first = False
    for row in range(h):
        for col in range(w):
            pv = rgbImage[row, col]
            if pv > min:
                if first == False:
                    smin = pv
                    first = True
                if pv < smin:
                    smin = pv            #选取阈值
    # print("second min", smin)
    ret, binary = cv.threshold(rgbImage, smin, 255, cv.THRESH_BINARY)      #对灰度图进行二值化处理，检测图像边缘，返回当前阈值ret和结果图像binary

    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)      #寻找图像轮廓，mode为只检索最外面的轮廓，method为压缩水平的、垂直的和斜的部分；返回图像的轮廓坐标
    # print("contours len ===", len(contours))
    drawNum = 0
    CropImage = cv.imread(path_cul, cv.IMREAD_COLOR)
    CropImage = cv.resize(CropImage, (224, 224))
    for i in range(len(contours)):
        hull = cv.convexHull(contours[i], returnPoints=False)     #寻找图像凸包
        length = len(hull)
        if length > 5:
            drawNum += 1
            defects = cv.convexityDefects(contours[i], hull)           #计算轮廓凹陷数量
            has = hasattr(defects, 'shape')
            if has == True:
                # print('draw ---------------------------', i)
                for n in range(defects.shape[0]):
                    s, e, f, d = defects[n, 0]
                    start = tuple(contours[i][e][0])
                    end = tuple(contours[i][s][0])
                    far = tuple(contours[i][f][0])
                    centerPointX = (start[0] + end[0] + far[0]) / 3
                    centerPointY = (start[1] + end[1] + far[1]) / 3
                    h = 1.5 * math.fabs(start[1] - end[1])
                    w = 0.8 * h
                    if w >= 32:
                        x_1 = int(centerPointX - w / 2)
                        if x_1 < 0 :
                            x_1 = 0
                        y_1 = int(centerPointY - h / 2)
                        rX = (x_1, y_1)

                        imCrop = CropImage[rX[1]: rX[1] + 256, rX[0]:rX[0] + 256]    #绘制凹陷处矩形边框再进行裁剪
                        # cv.imwrite(path + fileName + "_" + str(n) + '.png', imCrop)

def scan_files(directory):
    for root, sub_dirs, files in os.walk(directory):
       print(sub_dirs)
       if len(sub_dirs) > 0 :
           for sdir in sub_dirs:
                print(sdir)
                str = root +'/' + sdir
                genBox(str + '/', sdir)     #
                #os.rename(str, str[0:index])

path = 'C:/Users/hello/PycharmProjects/tongue/tongue_resnet_WSDDN/cul_time'
cul = os.listdir(path)
before = time.time()
for patient in cul:
    path_cul = path + '/' + patient
    path_cul = path_cul + '/' + 'tong.png'
    genBox(path_cul)

after = time.time()
print(str((after-before)/10))

#
# path = "C:/Users/hello/PycharmProjects/tongue/tongue_resnet_WSDDN/cul_time/140825084527/tong.png"
# genBox(path, '140825084527_1')
# #path = "G:\\1000tongue\\东直门\\0"
# #scan_files(path)
# #print(cv.__version__)
# cv.waitKey(0)