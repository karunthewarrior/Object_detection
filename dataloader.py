import os
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from os import listdir
from os.path import isfile, join
import cv2
import pickle

class MyDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, root_dir,transform=None):

        self.root_dir = root_dir
        self.transform = transform
        self.labels_path = self.root_dir + 'labels/'
        self.img_path = self.root_dir + 'image_data/'
        self.label_list = [f.split('.')[0] for f in listdir(self.labels_path) if isfile(join(self.labels_path, f))]
        self.image_list = [f for f in listdir(self.img_path) if isfile(join(self.img_path, f)) if f.split('.')[0] in self.label_list]
        
    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        image = cv2.imread(self.img_path + self.image_list[idx])
        shape = image.shape
        sample = image
        sample = cv2.cvtColor(sample,cv2.COLOR_BGR2RGB)
        
        label = pickle.load(open(self.labels_path + self.image_list[idx].split('.')[0] + '.p','rb'))
        label = label.transpose(2,1,0)
        label = torch.from_numpy(label)
        if self.transform:
            sample = self.transform(sample)
        
        return sample,label