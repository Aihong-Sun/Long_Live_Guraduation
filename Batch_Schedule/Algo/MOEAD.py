from Batch_Schedule.Algo.utils import *
import random

class MOEA_D:
    def __init__(self,Pop_size,gene_size,T=5,pc_max=0.8,pc_min=0.6,pm_max=0.1,pm_min=0.05):
        self._lambda=bi_VGM(Pop_size)   # bi-objective weight vectors
        self.T=T                        # the closest weight vectors T
        self.gene_size=gene_size
        self.pc_max=pc_max
        self.pc_min=pc_min
        self.pm_max=pm_max
        self.pm_min=pm_min
        self._z=[0,0]                      # the reference point

    def main(self,Pop,Evolute):

        self.Evolution = Evolute        #进化方式

        # ----------------------------------Initialization---------------------------------
        # to obtain Populations and weight vectors
        self.Pop_size = len(self._lambda)
        self.Pop=Pop
        B = Neighbor(self._lambda, self.T)  # work out the T closest weight vectors to each weight vector
        EP = []  # EP is used to store non-dominated solutions found during the search
        # ----------------------------------Iteration---------------------------------
        _z1=[1e+50,1e+50]
        C_max,T_tard=[],[]
        for gi in range(self.gene_size):
            # Adaptive operator rate
            self.pc = self.pc_max - ((self.pc_max - self.pc_min) / self.gene_size) * gi
            self.pm = self.pm_max - ((self.pm_max - self.pm_min) / self.gene_size) * gi
            for i in range(len(self.Pop)):
                # Randomly select two indexes k,l from B(i)
                j = random.randint(0, self.T - 1)
                k = random.randint(0, self.T - 1)
                # generate new solution from pop[j] and pop[k] by using genetic operators
                pop1, pop2 = self.Evolution(self.Pop[B[i][j]], self.Pop[B[i][k]])
                if Tri_Dominate(pop1, pop2):
                    y = pop1
                else:
                    y = pop2
                # update of the reference point z
                for zi in range(len(_z1)):
                    if _z1[zi] > y.fitness[zi]:
                        _z1[zi] = y.fitness[zi]
                # update of Neighboring solutions
                for bi in range(len(B[i])):
                    Ta = Tchebycheff(self.Pop[B[i][bi]], self._z, self._lambda[B[i][bi]])
                    Tb = Tchebycheff(y, self._z, self._lambda[B[i][bi]])
                    if Tb < Ta:
                        self.Pop[B[i][j]] = y
                # Update of EP
                if EP == []:
                    EP.append(y)
                else:
                    dominateY = False  # 是否有支配Y的解
                    _remove = []  # Remove from EP all the vectors dominated by y
                    for ei in range(len(EP)):
                        if Tri_Dominate(y, EP[ei]):
                            _remove.append(EP[ei])
                        elif Tri_Dominate(EP[ei], y):
                            dominateY = True
                            break
                    # add y to EP if no vectors in EP dominated y
                    if not dominateY:
                        EP.append(y)
                        for j in range(len(_remove)):
                            EP.remove(_remove[j])
            self._z=_z1
            # 绘图
            C_maxi,T_tradi=[],[]
            for pi in EP:
                C_maxi.append(pi.fitness[0])
                T_tradi.append(pi.fitness[1])
            C_max.append(min(C_maxi))
            T_tard.append(min(T_tradi))
        return EP,C_max,T_tard