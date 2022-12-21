'''
DQN network with CNN

'''

import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    """docstring for Net"""

    def __init__(self,
                 W,
                 H,
                 NUM_ACTIONS,feature_len
                 ):
        super(Net, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=4,  # input shape (3,J_num,O_max_len)
                out_channels=12,
                kernel_size=3,
                stride=1,
                padding=1,  # 使得出来的图片大小不变P=（3-1）/2,
            ),  # output shape (3,J_num,O_max_len)
            nn.ReLU(),
            # nn.MaxPool2d(kernel_size=2, ceil_mode=True)  # output shape:  (6,int(J_num/2),int(O_max_len/2))
        )
        # summary(self.conv1, (4, 7, 5))
        self.fc1 = nn.Linear(12*W*H+feature_len, 258)
        self.fc2 = nn.Linear(258, 258)
        self.fc3 = nn.Linear(258, 258)
        self.out = nn.Linear(258, NUM_ACTIONS)

    def forward(self, x,y):
        x = self.conv1(x)
        x = x.view(x.size(0), -1)
        x=torch.cat((x, y), 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = F.relu(x)
        action_prob = self.out(x)
        return action_prob