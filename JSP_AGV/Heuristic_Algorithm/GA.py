import random
from JS_Env.RJSP import *
from JS_Env.Gantt_Graph import *
import copy
from JS_Env.operator_choose_rule import action_translator
from Instance.GS_Instance import Instance
from Single_RL.DQN_series.DQN import DQN
from Single_RL.Params import get_args
from RL_Env.Agent_Env2 import Env


def dispatching_rule(env,a=7):
    initial_Pop=[]
    for i in range(200):
        Pop_i=[]
        state, done = env.reset()
        ep_reward = 0
        while True:
            action = a
            Job_i = action_translator(a, env)
            Pop_i.append(Job_i)
            next_state, reward, done = env.step(Job_i)
            ep_reward += reward
            if done == True:
                break
        initial_Pop.append(Pop_i)
    return initial_Pop

class GA:
    def __init__(self,n,m,agv_num,PT,MT,agv_trans,pop_size=200,gene_size=100,pc=0.9,pm=0.1,N_elite=10):
        self.N_elite=N_elite
        self.rjsp=RJSP(n,m,agv_num,PT,MT,agv_trans,m)
        self.Pop_size=pop_size
        self.gene_size=gene_size
        self.pc=pc
        self.pm=pm
        op_num=[len(Pi) for Pi in self.rjsp.PT]
        self.Chromo_list=[]
        self.best_chs=None
        self.best_c=99999
        for i in range(len(op_num)):
            self.Chromo_list.extend([i for _ in range(op_num[i])])

    def initial_population(self):
        self.Pop=[]
        for i in range(self.Pop_size):
            random.shuffle(self.Chromo_list)
            self.Pop.append(copy.copy(self.Chromo_list))


    #POX:precedence preserving order-based crossover
    def POX(self,CHS1, CHS2):
        Job_list = [i for i in range(self.rjsp.n)]
        random.shuffle(Job_list)
        r = random.randint(3, self.rjsp.n - 2)
        Set1 = Job_list[0:r]
        new_CHS1 = list(np.zeros(len(self.Chromo_list), dtype=int))
        new_CHS2 = list(np.zeros(len(self.Chromo_list), dtype=int))
        for k, v in enumerate(CHS1):
            if v in Set1:
                new_CHS1[k] = v + 1
        for i in CHS2:
            if i not in Set1:
                Site = new_CHS1.index(0)
                new_CHS1[Site] = i + 1

        for k, v in enumerate(CHS2):
            if v not in Set1:
                new_CHS2[k] = v + 1
        for i in CHS2:
            if i in Set1:
                Site = new_CHS2.index(0)
                new_CHS2[Site] = i + 1

        new_CHS1 = np.array([j - 1 for j in new_CHS1])
        new_CHS2 = np.array([j - 1 for j in new_CHS2])
        # print(CHS1)
        # print(CHS2)
        # print('--------------')
        # print(new_CHS1)
        # print(new_CHS2)
        return new_CHS1, new_CHS2


    #交换变异
    def swap_mutation(self,p1):
        D = len(p1)
        c1 = p1.copy()
        r = np.random.uniform(size=D)
        for idx1, val in enumerate(p1):
            if r[idx1] <= self.pm:
                idx2 = np.random.choice(np.delete(np.arange(D), idx1))
                c1[idx1], c1[idx2] = c1[idx2], c1[idx1]
        return c1

    def Elite(self):
        Fit=dict(enumerate(self.Fit))
        Fit=list(sorted(Fit.items(),key=lambda x:x[1]))
        idx=[]
        for i in range(self.N_elite):
            idx.append(Fit[i][0])
        return idx

    # 选择
    def Select(self):
        idx1=self.Elite()
        Fit = []
        for i in range(len(self.Fit)):
            fit = 1 / self.Fit[i]
            Fit.append(fit)
        Fit = np.array(Fit)
        idx = np.random.choice(np.arange(len(self.Fit)), size=len(self.Fit)-self.N_elite, replace=True,
                               p=(Fit) / (Fit.sum()))
        Pop=[]
        idx=list(idx)
        idx.extend(idx1)
        for i in idx:
            Pop.append(self.Pop[i])
        self.Pop=Pop

    def decode(self,Ci):
        self.rjsp = RJSP(n, m, agv_num, PT, MT, agv_trans, m)
        self.rjsp.reset()
        for i in Ci:
            self.rjsp.VAA_decode(i)
        if self.rjsp.C_max<self.best_c:
            self.best_c=self.rjsp.C_max
            self.best_chs=self.rjsp
        return self.rjsp.C_max

    def fitness(self):
        self.Fit=[]
        for Pi in self.Pop:
            self.Fit.append(self.decode(Pi))

    def crossover_operator(self):
        random.shuffle(self.Pop)
        Pop1,Pop2=self.Pop[:int(self.Pop_size/2)],self.Pop[int(self.Pop_size/2):]
        for i in range(len(Pop1)):
            if random.random()<self.pc:
                p1,p2=self.POX(Pop1[i],Pop2[i])
                Pop1[i],Pop2[i]=p1,p2
        self.Pop=Pop1+Pop2

    def mutation_operator(self):
        for i in range(len(self.Pop)):
            if random.random()<self.pm:
                p=self.swap_mutation(self.Pop[i])
                self.Pop[i]=p

    def run_one_chromo(self,Ci):
        self.rjsp = RJSP(n, m, agv_num, PT, MT, agv_trans, m)
        self.rjsp.reset()
        for i in Ci:
            self.rjsp.VAA_decode(i)
        Gantt(self.rjsp.Machines, self.rjsp.AGVs)
        return self.rjsp.C_max

    def main(self,name):
        import matplotlib.pyplot as plt

        Fit_best=[]
        self.initial_population()
        self.fitness()
        Best_Fit=min(self.Fit)
        for i in range(self.gene_size):
            self.Select()
            self.crossover_operator()
            self.mutation_operator()
            self.fitness()
            Min_Fit=min(self.Fit)
            # print("迭代次数：",i,'----->>>最小完工时间',Best_Fit,'----->>>平均完工时间',sum(self.Fit)/len(self.Fit))
            # Gantt(self.rjsp.Machines, self.rjsp.AGVs)
            if Min_Fit<Best_Fit:
                Best_Fit=Min_Fit
        # Gantt(self.rjsp.Machines, self.rjsp.AGVs)
            Fit_best.append(Best_Fit)
        x=[_ for _ in range(self.gene_size)]
        # plt.plot(x,Fit_best)

        # plt.savefig(r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\self_GeneIns_results'+name+'.png')
        # plt.xlabel("step")
        # plt.ylabel("makespan")
        return Best_Fit,self.best_chs
        # print(self.Pop)


if __name__=="__main__":
    from Instance.Text_extract import data
    import time
    from Instance.GS_Instance import Instance

    import argparse



    Ins=[[10,6,2]]

    result=[]
    for Insi in Ins:
        name='n'+str(Insi[0])+'_m'+str(Insi[1])+'_agv'+str(Insi[2])
        n, m, agv_num,PT, MT, agv_trans=Instance(name)
        args = get_args(n, m, agv_num, PT, MT, agv_trans, W=n, H=8, per=False, Network_type='CNN_DNN', DDQN=False,
                        GAMMA=0.95, BATCH_SIZE=128, LR=0.0001, Q_NETWORK_ITERATION=50)

        result_i=[]
        BEST_CHS=[]
        for i in range(10):
            t1=time.time()
            ga=GA(n,m,agv_num,PT,MT,agv_trans)
            best,best_chs=ga.main(name)
            t2=time.time()
            # print('runs:',i+1,'times','Instance：',name,'best makespan：',best,'using time:',t2-t1)
            result_i.append(best)
            BEST_CHS.append(best_chs)
            print('Instance：',name,'best_results',min(result_i))
        result.append(min(result_i))
        BC=BEST_CHS[result_i.index(min(result_i))]
        Gantt(BC.Machines, BC.AGVs,
              r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\self_GeneIns_results' +'/'+name + '.png',str(Insi[0])+'_'+str(Insi[1])+'_'+str(Insi[2]),BC.C_max)

