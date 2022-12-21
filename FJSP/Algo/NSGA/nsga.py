import random

import matplotlib.pyplot as plt

from FJSP.Algo.utils import *
import copy


class NSGA:
    def __init__(self,Pop_size,gene_size):

        '''
        :param pc: 交叉率
        :param pm: 变异率
        :param Pop_size: 种群大小
        :param gene_size: 迭代次数
        '''

        self.Pop_size=Pop_size
        self.gene_size=gene_size

    def offspring_Population(self):
        new_pop = []
        while len(new_pop) < self.Pop_size:
            pop_cross = random.sample(self.Pop,2)
            new_pop1, new_pop2 = self.Evolution(pop_cross[1],pop_cross[0],copy.deepcopy(self.JS),copy.deepcopy(self.SJS))
            new_pop.extend([new_pop1, new_pop2])
        return new_pop

    def main(self,Pop,Evolute,JS,SJS=None):
        #初始化车间
        self.JS=JS
        self.SJS=SJS
        self.Evolution=Evolute      #进化方式
        #
        # --------------------------------Initialization------------------------------
        self.Pop = Pop
        # ----------------------------------Iteration---------------------------------
        C_max,T_tard=[],[]
        for i in range(self.gene_size):
            new_pop = self.offspring_Population()  # use crossover and mutation to create a new population
            R_pop = self.Pop + new_pop  # combine parent and offspring population
            NDSet = fast_non_dominated_sort(R_pop)  # all nondominated fronts of R_pop
            C_maxi,T_tradi=[],[]
            for pi in NDSet[0]:
                C_maxi.append(pi.fitness[0])
                T_tradi.append(pi.fitness[1])
            C_max.append(min(C_maxi))
            T_tard.append(min(T_tradi))
            j = 0
            self.Pop = []
            while len(self.Pop) + len(NDSet[j]) <= self.Pop_size:  # until parent population is filled
                self.Pop.extend(NDSet[j])
                j += 1
            if len(self.Pop) < self.Pop_size:
                Ds = crowding_distance(copy.copy(NDSet[j]))  # calcalted crowding-distance
                k = 0
                while len(self.Pop) < self.Pop_size:
                    self.Pop.append(NDSet[j][Ds[k]])
                    k += 1
        EP = fast_non_dominated_sort(self.Pop)[0]
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
        ga=NSGA(Pop_size=100,gene_size=100)
        EP, C_max, T_tard=ga.main(pi,Operate,JS)
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
