import torch
import numpy as np


class ReplayBuffer:
    def __init__(self, args):
        self.xs = np.zeros((args.batch_size,4,args.W,args.H))
        self.ys=np.zeros((args.batch_size,args.feature_len))
        self.a = np.zeros((args.batch_size, 1))
        self.a_logprob = np.zeros((args.batch_size, 1))
        self.r = np.zeros((args.batch_size, 1))
        self.xs_ = np.zeros((args.batch_size, 4, args.W, args.H))
        self.ys_ = np.zeros((args.batch_size, args.feature_len))
        self.dw = np.zeros((args.batch_size, 1))
        self.done = np.zeros((args.batch_size, 1))
        self.count = 0

    def store(self, s, a, a_logprob, r, s_, dw, done):
        self.xs[self.count] = s[0]
        self.ys[self.count] = s[1]
        self.a[self.count] = a
        self.a_logprob[self.count] = a_logprob
        self.r[self.count] = r
        self.xs_[self.count] = s_[0]
        self.ys_[self.count] = s_[1]
        self.dw[self.count] = dw
        self.done[self.count] = done
        self.count += 1

    def numpy_to_tensor(self):
        xs = torch.tensor(self.xs, dtype=torch.float)
        ys=torch.tensor(self.ys, dtype=torch.float)
        a = torch.tensor(self.a, dtype=torch.long)  # In discrete action space, 'a' needs to be torch.long
        a_logprob = torch.tensor(self.a_logprob, dtype=torch.float)
        r = torch.tensor(self.r, dtype=torch.float)
        xs_ = torch.tensor(self.xs_, dtype=torch.float)
        ys_ = torch.tensor(self.ys_, dtype=torch.float)
        dw = torch.tensor(self.dw, dtype=torch.float)
        done = torch.tensor(self.done, dtype=torch.float)
        return xs,ys, a, a_logprob, r, xs_,ys_, dw, done
