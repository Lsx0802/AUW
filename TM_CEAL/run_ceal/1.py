# coding=utf-8
import json
import matplotlib.pyplot as plt
import skimage.io as io
from labelme import utils #这页代码要在labelme环境下运行
import re

def main():
    json_path = '150628071122.json'
    data = json.load(open(json_path))
    img = io.imread('%s/%s'%('../run_ceal/',data['imagePath']))
    lab, lab_names = utils.labelme_shapes_to_label(img.shape, data['shapes'])
    captions = ['%d: %s' % (l, name) for l, name in enumerate(lab_names)]
    lab_ok = utils.draw_label(lab, img, captions)

    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.imshow(lab_ok)
    plt.show()


if __name__ == '__main__':
    main()