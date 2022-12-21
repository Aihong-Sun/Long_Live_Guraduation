import numpy as np
import random
from collections import namedtuple, deque

class SumTree:
    pointer = 0
    def __init__(self, capacity):
        """
        # of leaf nodes = capaticy
        # of all nodes in the tree = 2 * capacity -1
        """
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity -1)
        self.data = np.zeros(capacity, dtype =object)

    def total(self):
        return self.tree[0]

    def add(self, priority, data):
        """
        1. update tree
        2. add transition data
        3. adjust pointer
        """
        # update tree
        tree_idx = self.pointer + self.capacity -1
        self.update(tree_idx, priority)
        # add transition data
        self.data[self.pointer] = data
        # adjust pointer; when exceed the capacity, restart from the beginning
        self.pointer += 1
        if self.pointer >= self.capacity:
            self.pointer = 0

    def update(self, tree_idx, priority):
        """
        1. update the leaf node priority
        2. update all the related parent nodes (add change to the old parent node value)
        """
        # difference between the new value and old value
        change = priority - self.tree[tree_idx]

        # update the leaf node priority
        self.tree[tree_idx]  = priority

        while tree_idx !=0:
            tree_idx = (tree_idx - 1)//2 # the index of parent node
            self.tree[tree_idx] += change

    def _retrieve(self, idx, s):
        """
        idx: parent node index
        left: left child node index
        right: right child node index
        """
        left = 2 * idx + 1
        right = left + 1

        # reach bottom, end search
        if left >= len(self.tree):
            return idx

        if s <= self.tree[left]:
            # put the left child node as the new parent node, keep searching
            return self._retrieve(left, s)
        else:
            # put the right child node as the new parent node, keep searching
            return self._retrieve(right, s-self.tree[left])

    def get(self, s):
        idx = self._retrieve(0, s)
        dataIdx = idx - self.capacity + 1
        return (idx, self.tree[idx], self.data[dataIdx])

class PrioritizedBuffer:

    experience = namedtuple("Experience", field_names=["index","IS_weight","state", "action", "reward", "next_state",'done'])
    alpha = 0.6 # mixing pure greedy prioritization and uniform random sampling
    beta = 0.4 # compensate for the non-uniform probabilities
    beta_increment_per_sampling = 0.001
    epsilon = 0.01 # small amount to avoid zero priority
    current_length = 0

    def __init__(self, size = int(1e5), seed = 1234) :
        self.size = size
        self.seed = random.seed(seed)
        self.memory = SumTree(capacity = self.size)

    def push(self, state, action, reward, next_state,done):
        """push new experience(s) to memory"""
        max_p = self.memory.tree[-self.memory.capacity:].max()
        priority = 1.0 if self.current_length == 0 else max_p
        data = (state, action, reward, next_state,done)
        self.memory.add(priority, data)
        self.current_length = self.current_length + 1

    def sample(self,batch_size):
        sum_priority = self.memory.total()
        segment = sum_priority/batch_size
        samples = []
        for i in range(batch_size):
            a, b = segment * i, segment *(i+1)
            s = random.uniform(a,b)
            (idx, priority, data) = self.memory.get(s)
            p = priority/sum_priority
            IS_weight = (batch_size * p)**(-self.beta)
            samples.append(self.experience(idx, IS_weight, data[0], data[1], data[2], data[3],data[4]))

        self.beta = np.min([1., self.beta + self.beta_increment_per_sampling])  # max = 1

        batch = self.experience(*zip(*samples))

        index = np.asarray(batch.index)

        IS_weight = np.asarray(batch.IS_weight)
        max_weight = IS_weight.max()
        IS_weight = IS_weight/max_weight

        states = np.asarray(batch.state)
        actions = np.asarray(batch.action)
        rewards = np.asarray(batch.reward)
        next_states = np.asarray(batch.next_state)
        done=np.asarray(batch.done)

        return  (index, IS_weight, states, actions, rewards, next_states,done)

    def update_priority(self, idxs, td_errors):
        """update priority for the replayed transitions"""
        for idx, td_error in zip(idxs, td_errors):
            priority = (td_error + self.epsilon)**self.alpha
            self.memory.update(idx, priority)

    def __len__(self):
        return self.current_length