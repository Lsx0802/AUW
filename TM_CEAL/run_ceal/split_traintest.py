import xlrd
from shutil import copy
import os
import cv2

# with open("label.txt", "r") as f:
#     with open("test.txt", "w") as ftest:
#         with open("train.txt", "w") as ftrain:
#             lines=f.readlines()
#             high = 0
#             low = 0
#             for line in lines:
#                 line = line.strip('\n')  # 去掉列表中每一个元素的换行符
#                 if line[-1] == '1' and high < 41:
#                     # 707:401=low:high
#                     # 70：41=low:high   (test=0.1)
#                     ftest.write(line+'\n')
#                     high=high+1
#                     continue
#                 if line[-1] == '0' and low < 70:
#                     ftest.write(line+'\n')
#                     low=low+1
#                     continue
#                 print(high,low)
#                 ftrain.write(line+'\n')

path=r'C:\Users\hello\PycharmProjects\tongue\data1108mask\image'
fh = open('test.txt', 'r')
# 按照传入的路径和txt文本参数，以只读的方式打开这个文本
save=r'C:\Users\hello\PycharmProjects\tongue\TM_CEAL\run_ceal\temp\images'
for line in fh:  # 迭代该列表#按行循环txt文本中的内
    line = line.strip('\n')
    line = line.rstrip('\n')
    # 删除 本行string 字符串末尾的指定字符，这个方法的详细介绍自己查询python
    words = line.split()
    if words[1]=='1':
        img=cv2.imread(os.path.join(path,words[0]+'.jpg'))
        img=cv2.resize(img,(224,224))

        cv2.imwrite(os.path.join(save,words[0]+'.jpg'),img)
        # copy(os.path.join(path,words[0]+'.jpg'),os.path.join(save,words[0]+'.jpg'))