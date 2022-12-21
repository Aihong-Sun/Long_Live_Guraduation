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
        self.action_dim=NUM_ACTIONS
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
        self.value_stream_layer = torch.nn.Sequential(torch.nn.Linear(12*W*H+feature_len, 258),
                                                      torch.nn.ReLU())
        self.advantage_stream_layer = torch.nn.Sequential(torch.nn.Linear(12*W*H+feature_len, 258),
                                                          torch.nn.ReLU())
        self.value = torch.nn.Linear(258, 1)
        self.advantage = torch.nn.Linear(258, NUM_ACTIONS)
        # summary(self.conv1, input_size=(-1, 4, n,max_o_len))

    def forward(self, x,y):
        x = self.conv1(x)
        x = x.view(x.size(0), -1)
        s = torch.cat((x, y), 1)
        value = self.value(self.value_stream_layer(s))
        x=self.advantage_stream_layer(s)
        advantage = self.advantage(x)
        action_value = value + (advantage - (1 / self.action_dim) * advantage.sum())
        return action_value