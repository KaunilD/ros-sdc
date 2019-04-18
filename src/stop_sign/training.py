import os
import sys
import shutil
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import os
from PIL import Image
import numpy as np
import torch

import torchvision.transforms as transforms

idx2label = {
    0: 'Speed limit (20km/h)',
    1: 'Speed limit (30km/h)',
    2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)',
    4: 'Speed limit (70km/h)',
    5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)',
    7: 'Speed limit (100km/h)',
    8: 'Speed limit (120km/h)',
    9: 'No passing',
    10: 'No passing for vehicles over 3.5 metric tons',
    11: 'Right-of-way at the next intersection',
    12: 'Priority road',
    13: 'Yield',
    14: 'Stop',
    15: 'No vehicles',
    16: 'Vehicles over 3.5 metric tons prohibited',
    17: 'No entry',
    18: 'General caution',
    19: 'Dangerous curve to the left',
    20: 'Dangerous curve to the right',
    21: 'Double curve',
    22: 'Bumpy road',
    23: 'Slippery road',
    24: 'Road narrows on the right',
    25: 'Road work',
    26: 'Traffic signals',
    27: 'Pedestrians',
    28: 'Children crossing',
    29: 'Bicycles crossing',
    30: 'Beware of ice/snow',
    31: 'Wild animals crossing',
    32: 'End of all speed and passing limits',
    33: 'Turn right ahead',
    34: 'Turn left ahead',
    35: 'Ahead only',
    36: 'Go straight or right',
    37: 'Go straight or left',
    38: 'Keep right',
    39: 'Keep left',
    40: 'Roundabout mandatory',
    41: 'End of no passing',
    42: 'End of no passing by vehicles over 3.5 metric tons'
}

classnames = [
    'Speed limit (20km/h)',
    'Speed limit (30km/h)',
    'Speed limit (50km/h)',
    'Speed limit (60km/h)',
    'Speed limit (70km/h)',
    'Speed limit (80km/h)',
    'End of speed limit (80km/h)',
    'Speed limit (100km/h)',
    'Speed limit (120km/h)',
    'No passing',
    'No passing for vehicles over 3.5 metric tons',
    'Right-of-way at the next intersection',
    'Priority road',
    'Yield',
    'Stop',
    'No vehicles',
    'Vehicles over 3.5 metric tons prohibited',
    'No entry',
    'General caution',
    'Dangerous curve to the left',
    'Dangerous curve to the right',
    'Double curve',
    'Bumpy road',
    'Slippery road',
    'Road narrows on the right',
    'Road work',
    'Traffic signals',
    'Pedestrians',
    'Children crossing',
    'Bicycles crossing',
    'Beware of ice/snow',
    'Wild animals crossing',
    'End of all speed and passing limits',
    'Turn right ahead',
    'Turn left ahead',
    'Ahead only',
    'Go straight or right',
    'Go straight or left',
    'Keep right',
    'Keep left',
    'Roundabout mandatory',
    'End of no passing',
    'End of no passing by vehicles over 3.5 metric tons']


class GTSRBLoader(torch.utils.data.Dataset):

    def __init__(self, data_dir, split, custom_transforms=None, list_dir=None,
                 out_name=False,  crop_size=None, num_classes=43, phase=None):

        self.data_dir = data_dir
        self.split = split
        self.phase = split if phase is None else phase
        self.crop_size = 32 if crop_size is None else crop_size
        self.out_name = out_name
        self.idx2label = idx2label
        self.classnames = classnames

        self.num_classes = num_classes
        self.mean = np.array([0.3337, 0.3064, 0.3171])
        self.std = np.array([0.2672, 0.2564, 0.2629])
        self.image_list, self.label_list = None, None
        self.read_lists()
        self.transforms = self.get_transforms(custom_transforms)


    def __getitem__(self, index):
        im = Image.open('{}/{}'.format(self.data_dir, self.image_list[index]))
        data = [self.transforms(im)]
        data.append(self.label_list[index])
        if self.out_name:
            data.append(self.image_list[index])
        return tuple(data)


    def __len__(self):
        return len(self.image_list)


    def get_transforms(self, custom_transforms):
        if custom_transforms:
            return custom_transforms

        if 'train' == self.phase:
            return transforms.Compose([
                transforms.Resize((self.crop_size, self.crop_size)),
                transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0),
                transforms.ToTensor(),
                transforms.Normalize(mean=self.mean, std=self.std),
            ])
        else:
            return transforms.Compose([
                transforms.Resize((self.crop_size, self.crop_size)),
                transforms.ToTensor(),
                transforms.Normalize(mean=self.mean, std=self.std),
            ])


    def read_lists(self):
        image_path = os.path.join(self.data_dir, self.split + '_images.txt')
        assert os.path.exists(image_path)
        self.image_list = [line.strip().split()[0] for line in open(image_path, 'r')]
        self.label_list = [int(line.strip().split()[1]) for line in open(image_path, 'r')]
        assert len(self.image_list) == len(self.label_list)

    def unprocess_image(self, im, plot=False):
        im = im.squeeze().numpy().transpose((1, 2, 0))
        im = self.std * im + self.mean
        im = np.clip(im, 0, 1)
        im = im * 255
        im = Image.fromarray(im.astype(np.uint8))

        if plot:
            plt.imshow(im)
            plt.show()
        else:
            return im

    def unprocess_batch(self, input):
        for i in range(input.size(1)):
            input[:,i,:,:] = self.std[i] * input[:,i,:,:]
            input[:,i,:,:] = input[:,i,:,:] + self.mean[i]
            input[:,i,:,:] = np.clip(input[:,i,:,:], 0, 1)

        return input

class LeNet(nn.Module):
    def __init__(self, num_classes=43, input_channels=3):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(input_channels, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1   = nn.Linear(16*5*5, 120)
        self.fc2   = nn.Linear(120, 84)
        self.fc3   = nn.Linear(84, num_classes)
        self.softmax = nn.LogSoftmax(dim=1)


    def forward(self, x):
        out = F.relu(self.conv1(x))
        out = F.max_pool2d(out, 2)
        out = F.relu(self.conv2(out))
        out = F.max_pool2d(out, 2)
        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))
        out = F.relu(self.fc2(out))
        out = self.fc3(out)

        out = self.softmax(out)
        return out

def accuracy(pred, target, top_k = 1):
    maxk = 1
    batch_size = target.size(0)

    _, pred = pred.topk(maxk, 1, True, True)
    pred = pred.t()

    correct = pred.eq(target.view(1, -1).expand_as(pred))
    correct_k = correct[:maxk].view(-1).float().sum(0)
    correct_k.mul_(1.0 / batch_size)
    res = correct_k.clone()

    return res.item()


def test(val_loader, model, criterion):
    model.eval()
    overall_loss = 0
    acc = 0
    with torch.no_grad():
        for i, (inp, target_class, name) in enumerate(val_loader):
            batch_size = inp.size(0)
            label = target_class.numpy()
            inp, target_class = inp.to('cuda').requires_grad_(), target_class.to('cuda')
            output = model(inp)
            acc_ = accuracy(output, target_class)
            acc+=acc_
    return acc/len(val_loader)

def train(train_loader, model, criterion, optimizer, epoch):

    model.train()
    running_loss = 0
    for i, (inp, target_class) in enumerate(train_loader):
        batch_size = inp.size(0)
        optimizer.zero_grad()

        inp, target_class = inp.to('cuda').requires_grad_(), target_class.to('cuda')
        output = model(inp)
        loss = criterion(output, target_class)
        loss.backward()

        optimizer.step()

        running_loss+=loss.item()
    return running_loss

if __name__ == '__main__':

    train_loader = torch.utils.data.DataLoader(
            GTSRBLoader(
                data_dir='./data',split='train',
                phase='train', num_classes=43, crop_size=32
            ),
            batch_size=32, shuffle=True, num_workers=1
    )

    val_loader = torch.utils.data.DataLoader(
            GTSRBLoader(
                data_dir='./data', split='val',
                phase='test', out_name=True, num_classes=43
            ),
        batch_size=128, shuffle=False, num_workers=1
    )
    model = LeNet()
    criterion = nn.CrossEntropyLoss(ignore_index=255)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, amsgrad=False)

    model.to('cuda')
    criterion.to('cuda')

    is_best = True
    best_acc = 0
    best_epoch = 0
    EPOCH = 30
    print("training started.")
    for epoch in range(0, EPOCH+1):

        train_loss = train( train_loader, model, criterion, optimizer, epoch )
        val_acc = test( val_loader, model, criterion )

        prev_lr =  optimizer.param_groups[0]['lr']

        is_best = val_acc > best_acc
        best_acc = max(val_acc, best_acc)
        if True == is_best:
            best_epoch = epoch
        print('EPOCH:[{}]/[{}] train_loss: {} val_acc: {} lr:{}'.format(
            epoch+1, 30, train_loss, val_acc, optimizer.param_groups[0]['lr']
        ))
        torch.save({
            'epoch': epoch + 1,
            'state_dict': model.state_dict(),
            'best_score': best_acc
        }, 'model-{}.ptm'.format(epoch))
