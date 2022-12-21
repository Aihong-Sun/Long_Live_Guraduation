from FJSP.Algo.utils import *
import copy
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

    def main(self,Pop,Evolute,JS,SJS=None):
        #初始化车间
        self.JS=JS
        self.SJS=SJS
        self.Evolution=Evolute      #进化方式
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
                pop1, pop2 = self.Evolution(self.Pop[B[i][j]], self.Pop[B[i][k]],copy.deepcopy(self.JS),copy.deepcopy(self.SJS))
                if Dominate(pop1, pop2):
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
                        if Dominate(y, EP[ei]):
                            _remove.append(EP[ei])
                        elif Dominate(EP[ei], y):
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

if __name__=='__main__':
    from FJSP.Shop_Floor.Job_Shop import Job_shop
    from FJSP.Instance.Instance_extraction import Instance
    from FJSP.Shop_Floor.utils import *
    from FJSP.Algo.GA.Pop_Generator import *
    from FJSP.Instance.Simulation_instance import *
    from FJSP.Algo.NSGA.Operator import Operate

    BF=[]
    for i in range(10):
        # n, m, PT, MT, ni = Instance(
        #     r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\Instance\FJSP_Instance' + "/Mk01.pkl")
        n=8
        JS = Job_shop(n, m, ni, MT, PT,EC,ESPC)
        JS.reset()

        p = Pop(100, JS)
        pi = p.Get_Pop()
        import time
        t1=time.time()
        algo=MOEA_D(Pop_size=100,gene_size=100)
        EP, C_max, T_tard=algo.main(pi,Operate,JS)
        t2=time.time()

        Plot_NonDominatedSet(EP, shape='.', G_label='', xlable='总完工时间', ylable='总能耗')
        # plt.scatter(C_max,T_tard)
        plt.show()
        for Ei in EP:
            print(f"Best Solution \nBestScore: { Ei.fitness} "
                  f"\n CPU(s): {round(t2 - t1, 2)}\n"
                  )
            Gantt(Ei.JS.Machines)
        BF.append( EP[0].fitness)
        print(BF)
