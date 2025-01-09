import torch
import torch.nn as nn
import torch.nn.functional as F
from math import floor
import math
from uncertainty_cul import cal_u
from spp_layer import spatial_pyramid_pool

class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_channel, out_channel, stride=1, downsample=None, **kwargs):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=in_channel, out_channels=out_channel,
                               kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channel)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(in_channels=out_channel, out_channels=out_channel,
                               kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channel)
        self.downsample = downsample

    def forward(self, x):
        identity = x
        if self.downsample is not None:
            identity = self.downsample(x)

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        out += identity
        out = self.relu(out)

        return out


class Bottleneck(nn.Module):
    """
    注意：原论文中，在虚线残差结构的主分支上，第一个1x1卷积层的步距是2，第二个3x3卷积层步距是1。
    但在pytorch官方实现过程中是第一个1x1卷积层的步距是1，第二个3x3卷积层步距是2，
    这么做的好处是能够在top1上提升大概0.5%的准确率。
    可参考Resnet v1.5 https://ngc.nvidia.com/catalog/model-scripts/nvidia:resnet_50_v1_5_for_pytorch
    """
    expansion = 4

    def __init__(self, in_channel, out_channel, stride=1, downsample=None,
                 groups=1, width_per_group=64):
        super(Bottleneck, self).__init__()

        width = int(out_channel * (width_per_group / 64.)) * groups

        self.conv1 = nn.Conv2d(in_channels=in_channel, out_channels=width,
                               kernel_size=1, stride=1, bias=False)  # squeeze channels
        self.bn1 = nn.BatchNorm2d(width)
        # -----------------------------------------
        self.conv2 = nn.Conv2d(in_channels=width, out_channels=width, groups=groups,
                               kernel_size=3, stride=stride, bias=False, padding=1)
        self.bn2 = nn.BatchNorm2d(width)
        # -----------------------------------------
        self.conv3 = nn.Conv2d(in_channels=width, out_channels=out_channel * self.expansion,
                               kernel_size=1, stride=1, bias=False)  # unsqueeze channels
        self.bn3 = nn.BatchNorm2d(out_channel * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x):
        identity = x
        if self.downsample is not None:
            identity = self.downsample(x)

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        out += identity
        out = self.relu(out)

        return out


class WSDDN_res(nn.Module):
    def __init__(self,  blocks_num =[3, 4, 6, 3], block=BasicBlock,numclasses=2):
        super(WSDDN_res, self).__init__()
        self.groups = 1
        self.in_channel = 64
        self.width_per_group = 64

        self.conv1 = nn.Conv2d(3, self.in_channel, kernel_size=7, stride=2,
                               padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(self.in_channel)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, 64, blocks_num[0])
        self.layer2 = self._make_layer(block, 128, blocks_num[1], stride=2)
        self.layer3 = self._make_layer(block, 256, blocks_num[2], stride=2)
        self.layer4 = self._make_layer(block, 512, blocks_num[3], stride=2)

        self.fc6 = nn.Linear(4096, 4096)
        self.fc7 = nn.Linear(4096, 4096)
        self.fc8c = nn.Linear(4096, numclasses)
        self.fc8d = nn.Linear(4096, numclasses)

    def _make_layer(self, block, channel, block_num, stride=1):
        downsample = None
        if stride != 1 or self.in_channel != channel * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.in_channel, channel * block.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(channel * block.expansion))

        layers = []
        layers.append(block(self.in_channel,
                            channel,
                            downsample=downsample,
                            stride=stride,
                            groups=self.groups,
                            width_per_group=self.width_per_group))
        self.in_channel = channel * block.expansion

        for _ in range(1, block_num):
            layers.append(block(self.in_channel,
                                channel,
                                groups=self.groups,
                                width_per_group=self.width_per_group))

        return nn.Sequential(*layers)

    def through_spp_new(self, x, ssw):
        for i in range(x.size(0)):
            for j in range(ssw.size(1)):
                fmap_piece = torch.unsqueeze(x[i, :, floor(ssw[i, j, 0]) : floor(ssw[i, j, 0] + ssw[i, j, 2]),
                                      floor(ssw[i, j, 1]) : floor(ssw[i, j, 1] + ssw[i, j, 3])], 0)
                fmap_piece = spatial_pyramid_pool(previous_conv = fmap_piece, num_sample = 1,
                                        previous_conv_size = [fmap_piece.size(2),fmap_piece.size(3)], out_pool_size = [2, 2])
                if j == 0:
                    y_piece = fmap_piece
                    #print('fmap_piece.shape', fmap_piece.shape)
                else:
                    # print('fmap_piece.shape', fmap_piece.shape)
                    y_piece = torch.cat((y_piece, fmap_piece))

            if i == 0:
                y = torch.unsqueeze(y_piece, 0)
                #print('y_piece', y_piece.shape)
            else:
                y = torch.cat((y, torch.unsqueeze(y_piece, 0)))
        return y

    def forward(self, x,ssw_get):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.through_spp_new(x, ssw_get)

        x = F.relu(self.fc6(x))
        x = F.relu(self.fc7(x))
        x_c = F.relu(self.fc8c(x))
        x_d = F.relu(self.fc8d(x))

        u=cal_u(x_c,x_d)
        uncertainty=u.mean(dim=1)
        u=u.unsqueeze(2)
        segma_c = F.softmax(x_c*u, dim=2)
        segma_d = F.softmax(x_d*u, dim=1)
        x = segma_c * segma_d
        x = torch.sum(x, dim=1)
        # print(x.shape)
        return x, segma_d, segma_c,uncertainty


if __name__ == '__main__':

    BATCH_SIZE = 32
    R = 100

    net_test = WSDDN_res(numclasses=2)
    x_test = torch.randn(BATCH_SIZE, 3, 224, 224)
    ssw_spp = torch.zeros(BATCH_SIZE, R, 4)
    for i in range(BATCH_SIZE):
        for j in range(R):
            ssw_spp[i, j, 0] = 0
            ssw_spp[i, j, 1] = 0
            ssw_spp[i, j, 2] = 4
            ssw_spp[i, j, 3] = 4
    out_test = net_test(x_test, ssw_spp)
    print(out_test[0].shape)
    '''
    ssw_spp = torch.zeros(BATCH_SIZE, R, 4)
    for i in range(BATCH_SIZE):
        for j in range(R):
            ssw_spp[i, j, 0] = 0
            ssw_spp[i, j, 1] = 0
            ssw_spp[i, j, 2] = 4
            ssw_spp[i, j, 3] = 4
    map_test = torch.randn(BATCH_SIZE, 512, 14, 14)
    y_test = select_fmap(map_test, ssw_spp)
    print(y_test.shape)
    '''
    
    '''
    spp_test = torch.randn(BATCH_SIZE, R, 512, 14, 14)
    out_test = through_spp(spp_test)
    print(out_test.shape)
    '''
#pretrained_model_path = 
#net_wsddn = WSDDN('VGG11')
#state_dict = torch.load(pretrained_model_path)
#net_wsddn.load_state_dict({k: v for k, v in state_dict.items() if k in net_wsddn.state_dict()})
