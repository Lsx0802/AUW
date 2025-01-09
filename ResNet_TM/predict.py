import os
import json

import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt

from model import resnet34


def main(img, cam, label):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    # load image

    img_path = img
    assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
    img = Image.open(img_path)
    cam_img = Image.open(cam)

    plt.subplot(211)
    plt.imshow(img)
    plt.axis('off')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(212)
    plt.imshow(cam_img)
    plt.axis('off')
    plt.xticks([])
    plt.yticks([])

    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

    json_file = open(json_path, "r")
    class_indict = json.load(json_file)

    # create model
    model = resnet34(num_classes=2).to(device)

    # load model weights
    weights_path = "./resnet34_fold" + fold + ".pkl"
    assert os.path.exists(weights_path), "file: '{}' dose not exist.".format(weights_path)
    model.load_state_dict(torch.load(weights_path, map_location=device))

    # prediction
    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()

    print_res = "original:{} predict: {}  prob: {:.4}".format(label, class_indict[str(predict_cla)],
                                                              predict[predict_cla].numpy())
    plt.title(print_res)
    print(print_res)
    save_path = r'C:\Users\hello\PycharmProjects\ResNet_t\final_img/fold' + fold
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    final_path = os.path.join(save_path, i)
    plt.savefig(final_path)


if __name__ == '__main__':
    fold = '5'
    path = r'C:\Users\hello\PycharmProjects\ResNet_t\dataset\fold' + fold + '/val/'
    path0 = path + '0/'
    path1 = path + '1/'
    path00 = os.listdir(path0)
    path11 = os.listdir(path1)
    cam_path = r'C:\Users\hello\PycharmProjects\ResNet_t\save_img\fold' + fold + '/'
    cam = ''

    for i in path00:
        cam = cam_path + i[0:-4] + 'cam.jpg'
        path000 = path0 + i
        label = 'feianshe'
        main(path000, cam, label)

    for i in path11:
        cam = cam_path + i[0:-4] + 'cam.jpg'
        path111 = path1 + i
        label = 'anshe'
        main(path111, cam, label)
