import os
from shutil import copytree

path0='1000tongue/东直门/00'
path1='1000tongue/东直门/11'

patient0=os.listdir(path0)
patient1=os.listdir(path1)

save='1000tongue/dzm'
if not os.path.exists(save):
    os.makedirs(save)

save0='1000tongue/dzm/0'
if not os.path.exists(save0):
    os.makedirs(save0)

save1='1000tongue/dzm/1'
if not os.path.exists(save1):
    os.makedirs(save1)

for i in patient0:
    json_path=os.path.join(path0,i)
    copytree(json_path,save0+'/'+i[:-15])

for i in patient1:
    json_path=os.path.join(path1,i)
    copytree(json_path,save1+'/'+i[:-15])


