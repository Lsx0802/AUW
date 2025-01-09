import os
from shutil import copy

path='../data1108'

save='../data1108_2'
if not os.path.exists(save):
    os.makedirs(save)

patient=os.listdir(path)

for i in patient:
    json_path=os.path.join(path,i)
    copy(json_path,os.path.join(save,i[0:12]+'.jpg'))


