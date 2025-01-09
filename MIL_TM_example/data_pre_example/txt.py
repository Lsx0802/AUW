# coding=utf-8
import os
import random
import numpy as np
image_path='tooth_mark'
low_path=os.path.join(image_path,'dzm_non_toothmark')
high_path=os.path.join(image_path,'dzm_toothmark')

high_patient=os.listdir(high_path)
low_patient=os.listdir(low_path)
total_patient=high_patient+low_patient

random.seed(2021)
random.shuffle(low_patient)
random.seed(2021)
random.shuffle(high_patient)


train_01=low_patient[int(len(low_patient)*0.25):]
train_11=high_patient[int(len(high_patient)*0.25):]

val_01=low_patient[0:int(len(low_patient)*0.25)]
val_11=high_patient[0:int(len(high_patient)*0.25)]

train_02=low_patient[0:int(len(low_patient)*0.25)]+low_patient[int(len(low_patient)*0.5):]
train_12=high_patient[0:int(len(high_patient)*0.25)]+high_patient[int(len(high_patient)*0.5):]

val_02=low_patient[int(len(low_patient)*0.25):int(len(low_patient)*0.5)]
val_12=high_patient[int(len(high_patient)*0.25):int(len(high_patient)*0.5)]

train_03=low_patient[0:int(len(low_patient)*0.5)]+low_patient[int(len(low_patient)*0.75):]
train_13=high_patient[0:int(len(high_patient)*0.5)]+high_patient[int(len(high_patient)*0.75):]

val_03=low_patient[int(len(low_patient)*0.5):int(len(low_patient)*0.75)]
val_13=high_patient[int(len(high_patient)*0.5):int(len(high_patient)*0.75)]

train_04=low_patient[0:int(len(low_patient)*0.75)]
train_14=high_patient[0:int(len(high_patient)*0.75)]

val_04=low_patient[int(len(low_patient)*0.75):]
val_14=high_patient[int(len(high_patient)*0.75):]


train_01_=[]
train_11_=[]
val_01_=[]
val_11_=[]

train_02_=[]
train_12_=[]
val_02_=[]
val_12_=[]

train_03_=[]
train_13_=[]
val_03_=[]
val_13_=[]

train_04_=[]
train_14_=[]
val_04_=[]
val_14_=[]

for i in train_01:
    train_01_.append(i[0:12]+'.png')
for i in train_11:
    train_11_.append(i[0:12]+'.png')
for i in val_01:
    val_01_.append(i[0:12]+'.png')
for i in val_11:
    val_11_.append(i[0:12] + '.png')

for i in train_02:
    train_02_.append(i[0:12]+'.png')
for i in train_12:
    train_12_.append(i[0:12]+'.png')
for i in val_02:
    val_02_.append(i[0:12]+'.png')
for i in val_12:
    val_12_.append(i[0:12] + '.png')

for i in train_03:
    train_03_.append(i[0:12]+'.png')
for i in train_13:
    train_13_.append(i[0:12]+'.png')
for i in val_03:
    val_03_.append(i[0:12]+'.png')
for i in val_13:
    val_13_.append(i[0:12] + '.png')

for i in train_04:
    train_04_.append(i[0:12]+'.png')
for i in train_14:
    train_14_.append(i[0:12]+'.png')
for i in val_04:
    val_04_.append(i[0:12]+'.png')
for i in val_14:
    val_14_.append(i[0:12] + '.png')


with open("train1_t.txt","w") as f:
    for i in train_01_:
        f.write(i+' '+'0')
        f.write('\n')
    for i in train_11_:
        f.write(i + ' ' + '1')
        f.write('\n')

with open("val1_t.txt","w") as f:
    for i in val_11_:
        f.write(i+' '+'1')
        f.write('\n')
    for i in val_01_:
        f.write(i+' '+'0')
        f.write('\n')


with open("train2_t.txt","w") as f:
    for i in train_02_:
        f.write(i+' '+'0')
        f.write('\n')
    for i in train_12_:
        f.write(i + ' ' + '1')
        f.write('\n')

with open("val2_t.txt","w") as f:
    for i in val_12_:
        f.write(i+' '+'1')
        f.write('\n')
    for i in val_02_:
        f.write(i+' '+'0')
        f.write('\n')


with open("train3_t.txt","w") as f:
    for i in train_03_:
        f.write(i+' '+'0')
        f.write('\n')
    for i in train_13_:
        f.write(i + ' ' + '1')
        f.write('\n')

with open("val3_t.txt","w") as f:
    for i in val_13_:
        f.write(i+' '+'1')
        f.write('\n')
    for i in val_03_:
        f.write(i+' '+'0')
        f.write('\n')

with open("train4_t.txt","w") as f:
    for i in train_04_:
        f.write(i+' '+'0')
        f.write('\n')
    for i in train_14_:
        f.write(i + ' ' + '1')
        f.write('\n')

with open("val4_t.txt","w") as f:
    for i in val_14_:
        f.write(i+' '+'1')
        f.write('\n')
    for i in val_04_:
        f.write(i+' '+'0')
        f.write('\n')
#
instance_path='dzm/instance'
instance=os.listdir(instance_path)

train_01__=[]
train_11__=[]
val_01__=[]
val_11__=[]

train_02__=[]
train_12__=[]
val_02__=[]
val_12__=[]


train_03__=[]
train_13__=[]
val_03__=[]
val_13__=[]


train_04__=[]
train_14__=[]
val_04__=[]
val_14__=[]


with open("train1_i.txt","w") as f:
    for i in instance:
        if i[0:12]+'.png' in train_11_:
            train_11__.append(i)
            f.write(i+' '+'1')
            f.write('\n')
        if i[0:12]+'.png' in train_01_:
            train_01__.append(i)
            f.write(i+' '+'0')
            f.write('\n')

with open("val1_i.txt","w") as f:
    for i in instance:
        if i[0:12]+'.png' in val_11_:
            val_11__.append(i)
            f.write(i+' '+'1')
            f.write('\n')
        if i[0:12]+'.png' in val_01_:
            val_01__.append(i)
            f.write(i+' '+'0')
            f.write('\n')

with open("train2_i.txt","w") as f:
    for i in instance:
        if i[0:12]+'.png' in train_12_:
            train_12__.append(i)
            f.write(i+' '+'1')
            f.write('\n')
        if i[0:12]+'.png' in train_02_:
            train_02__.append(i)
            f.write(i+' '+'0')
            f.write('\n')

with open("val2_i.txt","w") as f:
    for i in instance:
        if i[0:12]+'.png' in val_12_:
            val_12__.append(i)
            f.write(i+' '+'1')
            f.write('\n')
        if i[0:12]+'.png' in val_02_:
            val_02__.append(i)
            f.write(i+' '+'0')
            f.write('\n')

with open("train3_i.txt","w") as f:
    for i in instance:
        if i[0:12]+'.png' in train_13_:
            train_13__.append(i)
            f.write(i+' '+'1')
            f.write('\n')
        if i[0:12]+'.png' in train_03_:
            train_03__.append(i)
            f.write(i+' '+'0')
            f.write('\n')

with open("val3_i.txt","w") as f:
    for i in instance:
        if i[0:12]+'.png' in val_13_:
            val_13__.append(i)
            f.write(i+' '+'1')
            f.write('\n')
        if i[0:12]+'.png' in val_03_:
            val_03__.append(i)
            f.write(i+' '+'0')
            f.write('\n')

with open("train4_i.txt","w") as f:
    for i in instance:
        if i[0:12]+'.png' in train_14_:
            train_14__.append(i)
            f.write(i+' '+'1')
            f.write('\n')
        if i[0:12]+'.png' in train_04_:
            train_04__.append(i)
            f.write(i+' '+'0')
            f.write('\n')

with open("val4_i.txt","w") as f:
    for i in instance:
        if i[0:12]+'.png' in val_14_:
            val_14__.append(i)
            f.write(i+' '+'1')
            f.write('\n')
        if i[0:12]+'.png' in val_04_:
            val_04__.append(i)
            f.write(i+' '+'0')
            f.write('\n')

with open("label1_i.txt","w") as f:
    f.write('train_i_0=')
    f.write(str(train_01__))
    f.write('\n')
    f.write('train_i_1=')
    f.write(str(train_11__))
    f.write('\n')
    f.write('val_i_0=')
    f.write(str(val_01__))
    f.write('\n')
    f.write('val_i_1=')
    f.write(str(val_11__))
    f.write('\n')

with open("label2_i.txt","w") as f:
    f.write('train_i_0=')
    f.write(str(train_02__))
    f.write('\n')
    f.write('train_i_1=')
    f.write(str(train_12__))
    f.write('\n')
    f.write('val_i_0=')
    f.write(str(val_02__))
    f.write('\n')
    f.write('val_i_1=')
    f.write(str(val_12__))
    f.write('\n')


with open("label3_i.txt","w") as f:
    f.write('train_i_0=')
    f.write(str(train_03__))
    f.write('\n')
    f.write('train_i_1=')
    f.write(str(train_13__))
    f.write('\n')
    f.write('val_i_0=')
    f.write(str(val_03__))
    f.write('\n')
    f.write('val_i_1=')
    f.write(str(val_13__))
    f.write('\n')

with open("label4_i.txt","w") as f:
    f.write('train_i_0=')
    f.write(str(train_04__))
    f.write('\n')
    f.write('train_i_1=')
    f.write(str(train_14__))
    f.write('\n')
    f.write('val_i_0=')
    f.write(str(val_04__))
    f.write('\n')
    f.write('val_i_1=')
    f.write(str(val_14__))
    f.write('\n')


with open("label1.txt","w") as f:
    f.write('train0=')
    f.write(str(train_01_))
    f.write('\n')
    f.write('train1=')
    f.write(str(train_11_))
    f.write('\n')
    f.write('val0=')
    f.write(str(val_01_))
    f.write('\n')
    f.write('val1=')
    f.write(str(val_11_))
    f.write('\n')

with open("label2.txt","w") as f:
    f.write('train0=')
    f.write(str(train_02_))
    f.write('\n')
    f.write('train1=')
    f.write(str(train_12_))
    f.write('\n')
    f.write('val0=')
    f.write(str(val_02_))
    f.write('\n')
    f.write('val1=')
    f.write(str(val_12_))
    f.write('\n')

with open("label3.txt","w") as f:
    f.write('train0=')
    f.write(str(train_03_))
    f.write('\n')
    f.write('train1=')
    f.write(str(train_13_))
    f.write('\n')
    f.write('val0=')
    f.write(str(val_03_))
    f.write('\n')
    f.write('val1=')
    f.write(str(val_13_))
    f.write('\n')

with open("label4.txt","w") as f:
    f.write('train0=')
    f.write(str(train_04_))
    f.write('\n')
    f.write('train1=')
    f.write(str(train_14_))
    f.write('\n')
    f.write('val0=')
    f.write(str(val_04_))
    f.write('\n')
    f.write('val1=')
    f.write(str(val_14_))
    f.write('\n')
