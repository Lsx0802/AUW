# Authors: rafik gouiaa <rafikgouiaaphd@gmail.com>, ...

from typing import Optional, Callable

from torchvision.models import resnet34
from torch.utils.data import DataLoader
from torch.nn.functional import softmax
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch
import torch.optim as Optimizer
import logging


logging.basicConfig(format="%(levelname)s:%(name)s: %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class ResNet(object):
    """
    Encapsulate the pretrained resnet model
    Parameters
    ----------
    n_classes : int, default(256)
        the new number of classes
    device: Optional[str] 'cuda' or 'cpu', default(None)
            if None: cuda will be used if it is available
    """

    def __init__(self, n_classes: int = 2, device: Optional[str] = None):

        self.n_classes = n_classes
        self.model = resnet34(pretrained=True, progress=True)

        # self.__freeze_all_layers()
        self.__change_last_layer()
        if device is None:
            self.device = torch.device(
                "cuda:0" if torch.cuda.is_available() else "cpu")
        logger.info('The code is running on {} '.format(self.device))

    def __freeze_all_layers(self) -> None:
        """
        freeze all layers in resnet
        Returns
        -------
        None
        """

        for param in self.model.parameters():
            param.requires_grad = False

    def __change_last_layer(self) -> None:
        """
        change last layer to accept n_classes instead of 1000 classes
        Returns
        -------
        None
        """

        self.model.fc = nn.Linear(512, self.n_classes)

    def __add_softmax_layer(self) -> None:
        """
        Add softmax layer to resnet model
        Returns
        -------

        """
        # add softmax layer
        self.model = nn.Sequential(self.model, nn.LogSoftmax(dim=1))

    def __train_one_epoch(self, train_loader: DataLoader,
                          optimizer: Optimizer,
                          criterion: Callable,
                          valid_loader: DataLoader = None,
                          epoch: int = 0,
                          each_batch_idx: int = 300) -> None:
        """
        Train resnet for one epoch
        Parameters
        ----------
        train_loader : DataLoader
        criterion :  Callable
        optimizer : Optimizer (torch.optim)
        epoch : int
        each_batch_idx : int
            print training stats after each_batch_idx

        Returns
        -------
        None
        """
        train_loss = 0
        data_size = 0

        for batch_idx, sample_batched in enumerate(train_loader):
            # load data and label
            data, label = sample_batched['image'], sample_batched['label']

            # convert data and label to be compatible with the device
            data = data.to(self.device)
            data = data.float()
            label = label.to(self.device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # run forward
            pred_prob = self.model(data)

            # calculate loss
            loss = criterion(pred_prob, label)

            # calculate gradient (backprop)
            loss.backward()

            # total train loss
            train_loss += loss.item()
            data_size += label.size(0)

            # update weights
            optimizer.step()

            if batch_idx % each_batch_idx == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data),
                    len(train_loader.sampler.indices),
                    100. * batch_idx / len(train_loader.sampler.indices),
                    loss.item()))
        if valid_loader:
            acc = self.evaluate(test_loader=valid_loader)
            print('Accuracy on the valid dataset {}'.format(acc))

        print('====> Epoch: {} Average loss: {:.4f}'.
              format(epoch,
                     train_loss / data_size))

    def train(self, epochs: int, train_loader: DataLoader,
              valid_loader: DataLoader = None) -> None:
        """
        Train resnet for several epochs
        Parameters
        ----------
        epochs : int
            number of epochs
        train_loader:  DataLoader
            training set
        valid_loader : DataLoader, Optional

        Returns
        -------
        None
        """

        self.model.to(self.device)
        self.model.train()
        # optimizer = optim.SGD(
        #     filter(lambda p: p.requires_grad, self.model.parameters()),
        #     lr=0.001, momentum=0.9)
        optimizer=optim.Adam(filter(lambda p: p.requires_grad,self.model.parameters()),lr=1e-4,weight_decay=1e-4)

        criterion = nn.CrossEntropyLoss()
        for epoch in range(epochs):
            self.__train_one_epoch(train_loader=train_loader,
                                   optimizer=optimizer,
                                   criterion=criterion,
                                   valid_loader=valid_loader,
                                   epoch=epoch
                                   )

    def evaluate(self, test_loader: DataLoader) -> float:
        """
        Calaculate resnet accuracy on test data
        Parameters
        ----------
        test_loader: DataLoader

        Returns
        -------
        accuracy: float
        """
        correct = 0
        total = 0
        with torch.no_grad():
            for batch_idx, sample_batched in enumerate(test_loader):
                data, labels = sample_batched['image'], \
                               sample_batched['label']
                data = data.to(self.device)
                data = data.float()
                labels = labels.to(self.device)
                outputs = self.model(data)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        return 100 * correct / total

    def predict(self, test_loader):
        """
        Run the inference pipeline on the test_loader data
        Parameters
        ----------
        test_loader: DataLoader
            test data

        Returns
        -------

        """
        self.model.eval()
        self.model.to(self.device)
        predict_results = np.empty(shape=(0, 2))
        with torch.no_grad():
            for batch_idx, sample_batched in enumerate(test_loader):
                data, _ = sample_batched['image'], \
                          sample_batched['label']
                data = data.to(self.device)
                data = data.float()
                outputs = self.model(data)
                outputs2 = softmax(outputs)
                predict_results = np.concatenate(
                    (predict_results, outputs2.cpu().numpy()))
        return predict_results
        # return outputs.cpu().numpy()
