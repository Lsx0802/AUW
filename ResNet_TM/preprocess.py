import  os
import numpy as np
from  PIL import Image
from shutil import copy

original=r'C:\Users\hello\PycharmProjects\ResNet_t\original'

low_image_path=os.path.join(original,'0')
high_image_path=os.path.join(original,'1')

low_image=os.listdir(low_image_path)
high_image=os.listdir(high_image_path)

total=low_image+high_image

print(len(low_image))
print(len(high_image))

fold=[0,20,40,60,80,100]

val1=low_image[fold[0]:fold[1]]+high_image[fold[0]:fold[1]]
train1=[]
for i in total:
    if  i not in val1:
        train1.append(i)
print(len(val1))
print(len(train1))

val2=low_image[fold[1]:fold[2]]+high_image[fold[1]:fold[2]]
train2=[]
for i in total:
    if  i not in val2:
        train2.append(i)
print(len(val2))
print(len(train2))

val3=low_image[fold[2]:fold[3]]+high_image[fold[2]:fold[3]]
train3=[]
for i in total:
    if  i not in val3:
        train3.append(i)
print(len(val2))
print(len(train3))

val4=low_image[fold[3]:fold[4]]+high_image[fold[3]:fold[4]]
train4=[]
for i in total:
    if  i not in val4:
        train4.append(i)
print(len(val4))
print(len(train4))

val5=low_image[fold[4]:fold[5]]+high_image[fold[4]:fold[5]]
train5=[]
for i in total:
    if  i not in val5:
        train5.append(i)
print(len(val5))
print(len(train5))

save_path=r'C:\Users\hello\PycharmProjects\ResNet_t\dataset'

save_path1=os.path.join(save_path,'fold1')
if not os.path.exists(save_path1):
    os.makedirs(save_path1)
    
save_path2=os.path.join(save_path,'fold2')
if not os.path.exists(save_path2):
    os.makedirs(save_path2)

save_path3=os.path.join(save_path,'fold3')
if not os.path.exists(save_path3):
    os.makedirs(save_path3)

save_path4=os.path.join(save_path,'fold4')
if not os.path.exists(save_path4):
    os.makedirs(save_path4)

save_path5=os.path.join(save_path,'fold5')
if not os.path.exists(save_path5):
    os.makedirs(save_path5)

def make_fold(save_path,high_image,high_image_path,val,train):
    
    save_path1_train=os.path.join(save_path,'train')
    if not os.path.exists(save_path1_train):
        os.makedirs(save_path1_train)
    save_path1_val=os.path.join(save_path,'val')
    if not os.path.exists(save_path1_val):
        os.makedirs(save_path1_val)

    for i in val:
        if i in high_image:
            image_path=os.path.join(high_image_path,i)
            save_path2=os.path.join(save_path1_val,'1')
        else:
            image_path = os.path.join(low_image_path, i)
            save_path2 = os.path.join(save_path1_val, '0')

        if not os.path.exists(save_path2):
            os.makedirs(save_path2)

        copy(image_path,save_path2)

    for i in train:
        if i in high_image:
            image_path=os.path.join(high_image_path,i)
            save_path2=os.path.join(save_path1_train,'1')
        else:
            image_path = os.path.join(low_image_path, i)
            save_path2 = os.path.join(save_path1_train, '0')

        if not os.path.exists(save_path2):
            os.makedirs(save_path2)


        copy(image_path,save_path2)

make_fold(save_path1,high_image,high_image_path,val1,train1)
make_fold(save_path2,high_image,high_image_path,val2,train2)
make_fold(save_path3,high_image,high_image_path,val3,train3)
make_fold(save_path4,high_image,high_image_path,val4,train4)
make_fold(save_path5,high_image,high_image_path,val5,train5)