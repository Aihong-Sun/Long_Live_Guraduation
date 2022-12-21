import random
from FJSP.Algo.GA.operator import *
import numpy as np

class GA:
    def __init__(self,pm,pc,pop_size,Iteration,N_elite):
        self.pm=pm
        self.pc=pc
        self.pop_size=pop_size
        self.Iteration=Iteration
        self.N_elite=N_elite

    def Elite(self):
        Fit = dict(enumerate(self.Fit))
        Fit = list(sorted(Fit.items(), key=lambda x: x[1]))
        idx = []
        for i in range(self.N_elite):
            idx.append(Fit[i][0])
        return idx

    def fitness(self):
        self.Fit = []
        for Pi in self.Pop:
            self.Fit.append(Pi.fitness)

    def Select(self,Fit):
        return np.random.choice(np.arange(len(self.Fit)), size=2, replace=True,
                               p=(Fit) / (Fit.sum()))

    def next_Generation(self):

        Fit = []
        for i in range(len(self.Fit)):
            fit = 1 / self.Fit[i]
            Fit.append(fit)
        Fit = np.array(Fit)
        new_pop = []
        idx=self.Elite()
        for i in idx:
            new_pop.append(self.Pop[i])
        while len(new_pop)<self.pop_size:
            idx=self.Select(Fit)
            Pop1, Pop2 = self.Pop[idx[0]], self.Pop[idx[1]]
            if random.random()<self.pc:
                Pop1, Pop2 = cross_operator(Pop1, Pop2, copy.deepcopy(self.JS))
            if random.random()<self.pm:
                Pop1 = OS_mutation(Pop1, JS, SJS=None)
                Pop2 = OS_mutation(Pop2, JS, SJS=None)
            new_pop.extend([Pop1, Pop2])
        self.Pop=new_pop

    def main(self,Pop,JS):
        self.Pop=Pop
        self.JS=JS
        Fit_best = []
        self.fitness()
        Best_Fit = min(self.Fit)
        Best_P=None
        for i in range(self.Iteration):
            # self.Select()
            self.next_Generation()
            self.fitness()
            Min_Fit = min(self.Fit)
            if Min_Fit <= Best_Fit:
                Best_Fit = Min_Fit
                Best_P=self.Pop[self.Fit.index(Min_Fit)]
            Fit_best.append(Best_Fit)
        return Best_P,Fit_best

if __name__=='__main__':
    from FJSP.Shop_Floor.Job_Shop import Job_shop
    from FJSP.Instance.Instance_extraction import Instance
    from FJSP.Shop_Floor.utils import *
    from FJSP.Algo.GA.Pop_Generator import *
    from FJSP.Instance.Simulation_instance import *

    BF=[]
    for i in range(100):
        # n, m, PT, MT, ni = Instance(
        #     r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\Instance\FJSP_Instance' + "/Mk01.pkl")
        n=8
        JS = Job_shop(n, m, ni, MT, PT)
        JS.reset()

        p = Pop(100, JS)
        pi = p.Get_Pop()
        import time
        t1=time.time()
        ga=GA(pm=0.05,pc=0.8,pop_size=100,Iteration=100,N_elite=5)
        Best_P, best_val=ga.main(pi,JS)
        t2=time.time()
        Gantt(Best_P.JS.Machines)

        print(f"Best Solution \nBestScore: { Best_P.fitness} "
              f"\n CPU(s): {round(t2 - t1, 2)}\n"
              )
        BF.append( Best_P.fitness)
        print(BF)
        import os
        import pickle
        result_path = r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\static_sched'
        dic = {'job_shop_env': Best_P.JS, 'score': best_val[-1]}
        with open(os.path.join(result_path, 'sim' + ".pkl"), "wb") as f:
            pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)
        import matplotlib.pyplot as plt

        x = [_ for _ in range(len(best_val))]
        plt.plot(x, best_val)
        plt.show()
