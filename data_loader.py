import os
import re

import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

import config
from modules.config import head_set, MEANS
from modules.utils.augmentations import SSDAugmentation

LABEL_CLASS = ['person']
cfg, temp = config.get_config()
now_path = os.getcwd()
father_path = os.path.abspath(os.path.dirname(now_path) + os.path.sep + '.')


def detection_collate(batch):
    """Custom collate fn for dealing with batches of images that have a different
    number of associated object annotations (bounding boxes).

    Arguments:
        batch: (tuple) A tuple of tensor images and lists of annotations

    Return:
        A tuple containing:
            1) (tensor) batch of images stacked on their 0 dim
            2) (list of tensors) annotations for a given image are stacked on
                                 0 dim
    """
    targets = []
    imgs = []
    for sample in batch:
        imgs.append(sample[0])
        targets.append(torch.FloatTensor(sample[1]))
    return torch.stack(imgs, 0), targets


def get_all_data(pos_txt, if_all=False):
    datafile = []
    targets = []

    df1 = pd.read_csv(pos_txt, sep=',', index_col=False, encoding='utf-8-sig')
    df2 = pd.read_csv(cfg.pos_test_data, sep=',', index_col=False, encoding='utf-8-sig')
    ndf1 = np.array(df1).tolist()
    ndf2 = np.array(df2).tolist()
    ndf = ndf1 + ndf2

    if if_all:
        for i in range(len(ndf)):
            if not (ndf[i][0] in datafile):
                datafile.append(ndf[i][0])
                targets.append([np.hstack((ndf[i][2:6], ndf[i][1]))])
            else:
                targets[len(targets) - 1].append(np.hstack((ndf[i][2:6], ndf[i][1])))
    else:
        for i in range(len(ndf1)):
            if not (ndf1[i][0] in datafile):
                datafile.append(ndf1[i][0])
                targets.append([np.hstack((ndf1[i][2:6], ndf1[i][1]))])
            else:
                targets[len(targets) - 1].append(np.hstack((ndf1[i][2:6], ndf1[i][1])))

    return datafile, targets


def get_train_loader(pos_train_data,
                     batch_size,
                     num_workers=4,
                     is_shuffle=True
                     ):
    train_set = MyDataset(pos_data_file=pos_train_data,
                          transform=SSDAugmentation(head_set["min_dim"], MEANS))
    train_loader = DataLoader(train_set, batch_size=batch_size,
                              num_workers=num_workers, shuffle=is_shuffle, collate_fn=detection_collate,
                              pin_memory=True)
    return train_loader


class MyDataset(Dataset):

    def __init__(self, pos_data_file, transform):
        self.img_path, self.targets = get_all_data(pos_txt=pos_data_file, if_all=True)
        self.transform = transform

    def __len__(self):
        return len(self.img_path)

    def __getitem__(self, index):
        img = cv2.imread(self.img_path[index])
        height, width, channels = img.shape
        targets = np.array(self.targets[index], dtype=float)

        if self.transform is not None:
            boxes = targets[:, :4]
            # Frame normalization
            boxes[:, 0] /= width
            boxes[:, 1] /= height
            boxes[:, 2] /= width
            boxes[:, 3] /= height

            # Data enhancement
            img, boxes, labels = self.transform(img, boxes, targets[:, 4])

            # to rgb
            img = img[:, :, (2, 1, 0)]
            targets = np.hstack((boxes, np.expand_dims(labels, axis=1)))

        return torch.from_numpy(img).permute(2, 0, 1), targets
