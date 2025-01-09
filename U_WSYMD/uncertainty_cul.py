# coding=utf-8
import torch
import torch.nn as nn


def calculate_uncertainty(cfg, model, data_loader, return_box=False):
    model.eval()
    model.cuda()
    dataset = data_loader.dataset
    print('>>> Computing Instance Uncertainty...')
    uncertainty = torch.zeros(len(dataset)).cuda(torch.cuda.current_device())
    for i, data in enumerate(data_loader):
        with torch.no_grad():
            data['img'][0] = data['img'][0].cuda()
            data.update({'x': data.pop('img')})
            y_head_f_1, y_head_f_2, y_head_cls = model(return_loss=False, rescale=True, return_box=return_box, **data)
            y_head_f_1 = torch.cat((y_head_f_1), 0)
            y_head_f_2 = torch.cat((y_head_f_2), 0)
            y_head_f_1 = nn.Sigmoid()(y_head_f_1)
            y_head_f_2 = nn.Sigmoid()(y_head_f_2)
            loss_l2_p = (y_head_f_1 - y_head_f_2).pow(2)
            uncertainty_all_N = loss_l2_p.mean(dim=1)
            arg = uncertainty_all_N.argsort()
            uncertainty_single = uncertainty_all_N[arg[-cfg.k:]].mean()
            uncertainty[i] = uncertainty_single
            if i % 1000 == 0:
                print('>>> ', i, '/', len(dataset))
    return uncertainty.cpu()


# 假设一张图片有50个anchor，两个不同的分类器对同一个anchor进行分类
# y_head_f_1, y_head_f_2为两个分类器的结果（anchors，classes）
# 利用两个分类器的 l2 范式值来计算该anchor不确定性


def cal_u(y_head_f_1, y_head_f_2):
    loss_l2_p = (y_head_f_1 - y_head_f_2).pow(2)
    # print(loss_l2_p)
    uncertainty_N = loss_l2_p.mean(dim=2)
    # print(loss_l2_p)# 这里得到每个anchor的不确定性
    # uncertainty, indices = torch.sort(uncertainty_N)  # 这里得到每个anchor的不确定性排序
    # # 如果不加主动学习到这就结束了
    # #一般的模型会直接mean输出整个图像的不确定性
    # k = 5  # K是容忍度，允许前k个值
    # uncertainty = uncertainty[-k:].mean()  # 这里得到最终的图像不确定性，用于主动学习来挑选
    # 主动学习挑选图像级不确定性大的图像，而不是示例级的
    return uncertainty_N

def cal_u_resnet(y_head_f_1, y_head_f_2):
    loss_l2_p = (y_head_f_1 - y_head_f_2).pow(2)
    # uncertainty=torch.softmax(loss_l2_p,dim=1)
    uncertainty= loss_l2_p # 这里得到每个anchor的不确定性
    # uncertainty, indices = torch.sort(uncertainty_N)  # 这里得到每个anchor的不确定性排序
    # # 如果不加主动学习到这就结束了
    # #一般的模型会直接mean输出整个图像的不确定性
    # k = 5  # K是容忍度，允许前k个值
    # uncertainty = uncertainty[-k:].mean()  # 这里得到最终的图像不确定性，用于主动学习来挑选
    # 主动学习挑选图像级不确定性大的图像，而不是示例级的
    return uncertainty

# y_head_f_1 = torch.rand([32,100, 2])
# y_head_f_2 = torch.rand([32,100, 2])
# a=torch.rand([32,100,4096])
# b=cal_u(y_head_f_1, y_head_f_2)
# print(b)
# # a=a.view(a.shape[0]*a.shape[1],-1)
# # b=b.view(b.shape[0]*b.shape[1])
# b=b.unsqueeze(2)
# c=b*a
# print(c)