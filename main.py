

import torch
import torch.nn as nn
from torch.distributions import  MultivariateNormal
# means = torch.zeros(5)
# stds = torch.eye(5)
# print("means: ",means)
# print("stds: ",stds)
#
# dist = MultivariateNormal(means, stds)
# action =dist.sample()
# print("action: ",action)


"""
Result: 
means:  tensor([0., 0., 0., 0., 0.])
stds:  tensor([[1., 0., 0., 0., 0.],
        [0., 1., 0., 0., 0.],
        [0., 0., 1., 0., 0.],
        [0., 0., 0., 1., 0.],
        [0., 0., 0., 0., 1.]])
action:  tensor([-1.4557, -1.4514,  0.7863,  0.3571, -0.2956])
"""
class Policy(nn.Module):
    def __init__(self, in_dim, n_hidden_1, n_hidden_2, num_outputs):
        super(Policy, self).__init__()
        self.layer = nn.Sequential(
            nn.Linear(in_dim, n_hidden_1),
            nn.ReLU(True),
            nn.Linear(n_hidden_1, n_hidden_2),
            nn.ReLU(True),
            nn.Linear(n_hidden_2, num_outputs)
        )

class Normal(nn.Module):
    def __init__(self, num_outputs):
        super().__init__()
        self.stds = nn.Parameter(torch.zeros(num_outputs))
    def forward(self, x):
        dist = torch.distributions.Normal(loc=x, scale=self.stds.exp())
        action = dist.sample()
        return action

if __name__ == '__main__':
    policy = Policy(4,20,20,5)
    normal = Normal(5)
    observation = torch.Tensor(4)
    action = normal.forward(policy.layer( observation))
    print("action: ",action)