import os
from PIL import Image
import numpy as np
import cv2
from shutil import copy

path_mark='TM_classify'
path_mark0=os.path.join(path_mark,'NTM')
path_mark1=os.path.join(path_mark,'TM')
patient_mark0=os.listdir(path_mark0)
patient_mark1=os.listdir(path_mark1)
patient_mark=patient_mark0+patient_mark1


save='dzm'
if not os.path.exists(save):
    os.makedirs(save)

save0='dzm/img'
if not os.path.exists(save0):
    os.makedirs(save0)

save1='dzm/instance'
if not os.path.exists(save1):
    os.makedirs(save1)

save2='dzm/original'
if not os.path.exists(save2):
    os.makedirs(save2)

for i in patient_mark0:
    json_path=os.path.join(path_mark0,i)
    json=os.listdir(json_path)

    for j in json:
        if j=='img.png':
            copy(os.path.join(json_path,j),os.path.join(save2,i+'.png'))
        elif j=='tong.png':
            copy(os.path.join(json_path, j), os.path.join(save0,i+'.png'))
        elif i in j:
            copy(os.path.join(json_path,j),os.path.join(save1,j))

for i in patient_mark1:
    json_path=os.path.join(path_mark1,i)
    json=os.listdir(json_path)

    for j in json:
        if j=='img.png':
            copy(os.path.join(json_path,j),os.path.join(save2,i+'.png'))
        elif j=='tong.png':
            copy(os.path.join(json_path, j), os.path.join(save0,i+'.png'))
        elif i in j:
            copy(os.path.join(json_path,j),os.path.join(save1,j))
#
