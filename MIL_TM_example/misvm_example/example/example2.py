#!/usr/bin/env python
from __future__ import print_function, division

import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, \
    confusion_matrix, roc_auc_score
from misvmio import parse_c45, bag_set
import misvm
from modelVGG import vgg
# coding=utf-8
import os
import json

import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from model2 import resnet34
from tqdm import tqdm

def model_l(path):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(224),
         # transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    img_path3 = path
    img = Image.open(img_path3)
    # plt.imshow(img)
    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    # create model
    model = resnet34(num_classes=2).to(device)

    # load model weights
    weights_path = "weight/Resnet34_t_o_pre_4_2.pkl"
    assert os.path.exists(weights_path), "file: '{}' dose not exist.".format(weights_path)
    model.load_state_dict(torch.load(weights_path, map_location=device))

    # prediction
    model.eval()
    with torch.no_grad():
        # predict class
        feature, output=model(img.to(device))
        feature=torch.squeeze(feature).cpu().numpy()

    return feature

def main():
    train0 = ['140831074407.png', '140905081746.png', '140910083516.png', '141104080824.png', '141024073828.png',
              '140920075912.png', '141025073242.png', '141029082903.png', '140826070711.png', '140830074131.png',
              '140913083727.png', '141028080238.png', '140915071811.png', '141025073759.png', '140915073217.png',
              '140827083300.png', '140905072759.png', '140912082548.png', '140910073725.png', '140825074453.png',
              '141027085601.png', '140919084002.png', '141105090831.png', '141026085033.png', '141105075938.png',
              '141027084325.png', '140911082640.png', '141027072656.png', '140825094844.png', '140905071229.png',
              '141027072333.png', '140919072920.png', '140828085042.png', '141029072220.png', '140914073756.png',
              '140903085830.png', '140912072159.png', '141027090224.png', '140903084823.png', '140912080030.png',
              '141025084929.png', '140910075214.png', '141026083539.png', '141028073329.png', '140909071953.png',
              '140916083007.png', '140912083044.png', '140901072615.png', '140903082154.png', '141030074439.png',
              '140911075933.png', '141101084657.png', '140912081548.png', '141030080120.png', '140916075128.png',
              '140913083247.png', '140831071127.png', '140901074540.png', '140911080507.png', '141024080653.png',
              '140831075759.png', '141030073743.png', '141105093615.png', '141102090617.png', '141023083412.png',
              '140901074046.png', '140901072125.png', '140917075201.png', '140909075009.png', '140910072524.png',
              '141030080946.png', '141101082420.png', '141029080750.png', '141031073225.png', '140825072742.png',
              '140825082152.png', '140913082831.png', '140922080827.png', '140906071358.png', '140915084513.png',
              '141025090810.png', '140920080407.png', '141025072150.png', '140918074838.png', '141027075124.png',
              '141104073307.png', '140913075921.png', '141026084120.png', '140825075117.png', '140916083515.png',
              '140826075145.png', '141028074242.png', '141101091958.png', '140904092406.png', '140914090406.png',
              '140905080243.png', '140829090254.png', '141024072636.png', '140913162311.png', '140827072129.png',
              '140911074246.png', '141103073634.png', '140923071741.png', '140826080854.png', '140909084907.png',
              '140826074236.png', '140827082254.png', '140922080328.png', '140904090318.png', '140903080613.png',
              '141027080836.png', '140906080427.png', '141104082854.png', '141025081640.png', '141101072308.png',
              '140903071607.png', '140909074012.png', '140913082243.png', '140917072259.png', '140911081318.png',
              '140828073532.png', '140906072157.png', '141104074959.png', '140830072915.png', '140906073225.png',
              '141027082453.png', '140915084301.png', '141030075521.png', '141105085607.png', '140902082629.png',
              '141027090729.png', '140920073223.png', '140904083804.png', '140830071851.png', '141103074303.png',
              '141105083705.png', '141101072802.png', '140910072828.png', '140914075008.png', '140918073701.png',
              '140916072507.png', '141105082240.png', '140904083234.png', '140905075855.png', '140909070801.png',
              '141026072920.png', '140825092009.png', '140825073705.png', '141029090313.png', '140902075758.png']
    train1 = ['140825091314.png', '140913072809.png', '140831080636.png', '140829081241.png', '140901075437.png',
              '141028073850.png', '140914081743.png', '140913072314.png', '141026081420.png', '140911081808.png',
              '140903091044.png', '140915082629.png', '140829091429.png', '141028072851.png', '140915090748.png',
              '140917080751.png', '141024093002.png', '140922073231.png', '140902091603.png', '140904091614.png',
              '141104083424.png', '140829073805.png', '140916080711.png', '140906074207.png', '140830081752.png',
              '140913071333.png', '141029074525.png', '140828075215.png', '141025081031.png', '140914082139.png',
              '140829084351.png', '141023081428.png', '140827080347.png', '140910081821.png', '140903075521.png',
              '140911083107.png', '141030090031.png', '140830073822.png', '141105083107.png', '140829091018.png',
              '140901070318.png', '140903072040.png', '140913074346.png', '140905073114.png', '140921071637.png',
              '140912072449.png', '140906075857.png', '140912084204.png', '141023082131.png', '140831081534.png',
              '141029075031.png', '141030072712.png', '140918085044.png', '140923073802.png', '140904080713.png',
              '140916082444.png', '141024084313.png', '140911085949.png', '140828082728.png', '140827071341.png',
              '141101085724.png', '140915082900.png', '140826071656.png', '140902071342.png', '140921072206.png',
              '140911082242.png', '140910071154.png', '140921075546.png', '141102074913.png', '140830083826.png',
              '140831085047.png', '141024071256.png', '140826070921.png', '140825084527.png', '140922075420.png',
              '140829085304.png', '140902080416.png', '140918075908.png', '140918091432.png', '141025075846.png',
              '140914075600.png', '141023091758.png', '141028074635.png', '141025083138.png', '141023090323.png',
              '140901070701.png', '140831084532.png', '141023082853.png', '140909075318.png', '140906073747.png',
              '140919071325.png', '140904071228.png', '140913081005.png', '140902075057.png', '140923081911.png',
              '141101075325.png', '141102072832.png']
    val0 = ['140910082406.png', '141103081152.png', '141028081222.png', '141029072757.png', '141026075115.png',
            '141101091659.png', '140922072053.png', '141104091905.png', '140920080840.png', '140909081209.png',
            '140906074626.png', '140831081101.png', '140915150715.png', '140914084643.png', '140913075035.png',
            '141025090113.png', '140910082046.png', '141029080308.png', '140919073221.png', '141105081603.png',
            '141027094351.png', '140905080808.png', '140901071112.png', '140920082952.png', '141031082425.png',
            '141025091211.png', '141102080019.png', '141104072517.png', '141026080519.png', '141030082905.png',
            '140831074750.png', '140827073504.png', '140904073804.png', '140904070538.png', '140829074446.png',
            '141104091244.png', '140911075718.png', '140910075631.png', '140911085040.png', '140828073135.png',
            '141027075912.png', '140922073643.png', '140919080840.png', '140826073513.png', '141029074156.png',
            '140909083337.png', '140910080614.png', '141026075943.png', '141029073250.png', '140916073610.png']
    val1 = ['140916080003.png', '140830091037.png', '140829075306.png', '140912073618.png', '140920084406.png',
            '140913084203.png', '141025083436.png', '141028083438.png', '141105082654.png', '140921083111.png',
            '140920081245.png', '140829074831.png', '140923074834.png', '140827071752.png', '141025072440.png',
            '140829093031.png', '140829091953.png', '141027073006.png', '140827091455.png', '141031090317.png',
            '140902081622.png', '140902072836.png', '140903074034.png', '140827081234.png', '140915080548.png',
            '140912075124.png', '140911085325.png', '140827071018.png', '140918074323.png', '141026083201.png',
            '140913071803.png', '140914081132.png', '141024072202.png']

    # load image
    img_path1 = "data/original"
    assert os.path.exists(img_path1), "file: '{}' dose not exist.".format(img_path1)


    bag_val_feature = []
    bag_train_feature=[]

    for i in tqdm(train0):
        img_path3 = os.path.join(img_path1, i)
        feature = model_l(img_path3)
        bag_train_feature.append(np.array(feature))
    for i in tqdm(train1):
        img_path3 = os.path.join(img_path1, i)
        feature = model_l(img_path3)
        bag_train_feature.append(np.array(feature))
    for i in tqdm(val0):
        img_path3 = os.path.join(img_path1, i)
        feature = model_l(img_path3)
        bag_val_feature.append(np.array(feature))
    for i in tqdm(val1):
        img_path3 = os.path.join(img_path1, i)
        feature = model_l(img_path3)
        bag_val_feature.append(np.array(feature))

    bag_train_label=[]
    bag_val_label = []
    for i in range(len(train0)):
        bag_train_label.append(-1)
    for i in range(len(train1)):
        bag_train_label.append(1)

    for i in range(len(val0)):
        bag_val_label.append(-1)
    for i in range(len(val1)):
        bag_val_label.append(1)

    bag_train_label = np.array(bag_train_label)
    bag_val_label=np.array(bag_val_label)

    classifier= misvm.SVM(kernel='linear', C=1.0)

    classifier.fit(bag_train_feature, bag_train_label)
    patient_pred = np.sign(classifier.predict(bag_val_feature))

    patient_true=bag_val_label

    accuracy = accuracy_score(patient_true, patient_pred)
    precision = precision_score(patient_true, patient_pred)
    recall = recall_score(patient_true, patient_pred)
    f1 = f1_score(patient_true, patient_pred)

    print("accuracy:{:.4f} precision:{:.4f} recall:{:.4f} f1:{:.4f}  ".format(accuracy, precision, recall, f1))

if __name__ == '__main__':
    main()
