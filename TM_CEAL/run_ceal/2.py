
import os
from PIL import Image
import cv2
from tqdm import tqdm
import numpy as np
bace_path = r'C:\Users\hello\PycharmProjects\tongue\labelme_mask'
save_path = r'C:\Users\hello\PycharmProjects\tongue\mask'
if not os.path.exists(save_path):
    os.makedirs(save_path)

patient=os.listdir(bace_path)


for im in tqdm(patient):
    p=os.path.join(bace_path,im,'label.png')

    label = cv2.imread(p)

    h, w, c = label.shape

    for row in range(h):
        for con in range(w):
            pv0 = label[row, con, 0]
            pv1 = label[row, con, 1]
            pv2 = label[row, con, 2]
            if pv0 > 0 or pv1 > 0 or pv2 > 0:
                label[row, con, 0] = 255
                label[row, con, 1] = 255
                label[row, con, 2] = 255
            cv2.imwrite(os.path.join(save_path,im[0:12],'.jpg'), label)