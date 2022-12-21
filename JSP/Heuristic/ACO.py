import numpy as np

class ACO:
    def __init__(self, alpha, beta, O_num,n,m):
        self.alpha=alpha
        self.beta=beta
        self.O_num = O_num      # numbers of operation
        self.Ph_matrix=np.ones((O_num+1,O_num+1))     # Pheromone Matrix
        self.n=n
        self.m=m
        self.CulOp=np.zeros((n))    # current processing state
        self.Idx_op=[(i,j) for i in range(self.n) for j in range(self.m)]
        self.Initial_Candi=[(0,i) for i in range(self.n) ]

    # operation candidate set
    def candidate_Op(self):
        pass

    def main(self):
        pass
