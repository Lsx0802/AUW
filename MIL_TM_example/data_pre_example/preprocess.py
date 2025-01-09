import os
from PIL import Image
import numpy as np
import cv2

path_mark = 'tooth_mark'
path_mark0 = os.path.join(path_mark, 'dzm_non_toothmark')
path_mark1 = os.path.join(path_mark, 'dzm_toothmark')
patient_mark0 = os.listdir(path_mark0)
patient_mark1 = os.listdir(path_mark1)
patient_mark_ = patient_mark0 + patient_mark1
patient_mark = []
for i in patient_mark_:
    patient_mark.append(i[:-14])

path_image = '1000tongue/dzm'
path_image0 = os.path.join(path_image, '0')
path_image1 = os.path.join(path_image, '1')

patient_image0 = os.listdir(path_image0)
patient_image1 = os.listdir(path_image1)
patient_image = patient_image0 + patient_image1

save = 'dzm'
if not os.path.exists(save):
    os.makedirs(save)

save0 = 'dzm/img'
if not os.path.exists(save0):
    os.makedirs(save0)

save1 = 'dzm/mask'
if not os.path.exists(save1):
    os.makedirs(save1)

save2 = 'dzm/original'
if not os.path.exists(save2):
    os.makedirs(save2)

for i in patient_image0:
    if i in patient_mark:
        json_path = os.path.join(path_image0, i)
        json = os.listdir(json_path)

        for j in json:
            image_path = os.path.join(json_path, 'img.png')
            label_path = os.path.join(json_path, 'label.png')

            image = cv2.imread(image_path)
            cv2.imwrite(save2 + '/' + i+ '.png', image)
            label = cv2.imread(label_path)

            h, w, c = image.shape

            for row in range(h):
                for con in range(w):
                    pv0 = label[row, con, 0]
                    pv1 = label[row, con, 1]
                    pv2 = label[row, con, 2]
                    if pv0 > 0 or pv1 > 0 or pv2 > 0:
                        label[row, con, 0] = 255
                        label[row, con, 1] = 255
                        label[row, con, 2] = 255

            image = cv2.bitwise_and(image, label)
            # cv2.imshow('image',image)
            #
            # cv2.waitKey(0)  # 等待按键
            cv2.imwrite(save0 + '/' + i + '.png', image)
            cv2.imwrite(save1 + '/' + i + '.png', label)
    print('0')

for i in patient_image1:
    if i in patient_mark:
        json_path = os.path.join(path_image1, i)
        json = os.listdir(json_path)

        for j in json:
            image_path = os.path.join(json_path, 'img.png')
            label_path = os.path.join(json_path, 'label.png')

            image = cv2.imread(image_path)
            cv2.imwrite(save2 + '/' + i + '.png', image)
            label = cv2.imread(label_path)

            h, w, c = image.shape

            for row in range(h):
                for con in range(w):
                    pv0 = label[row, con, 0]
                    pv1 = label[row, con, 1]
                    pv2 = label[row, con, 2]
                    if pv0 > 0 or pv1 > 0 or pv2 > 0:
                        label[row, con, 0] = 255
                        label[row, con, 1] = 255
                        label[row, con, 2] = 255

            image = cv2.bitwise_and(image, label)
            # cv2.imshow('image',image)
            #
            # cv2.waitKey(0)  # 等待按键
            cv2.imwrite(save0 + '/' + i + '.png', image)
            cv2.imwrite(save1 + '/' + i + '.png', label)
    print('1')
