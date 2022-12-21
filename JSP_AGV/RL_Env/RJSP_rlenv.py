import random

from JSP_AGV.JSP_AGV_Env.Shop_RJSP import RJSP
import copy
import numpy as np
from JSP_AGV.RL_Env.action import action_translator

class Env:
    def __init__(self,args):
        self.n, self.m, self.agv_num = args.n, args.m, args.agv_num
        self.PT = args.PT
        self.MT = args.MT
        self.TT = args.TT
        self.L_U = args.m
        self.Jobs = []
        self.C_max = 0
        self.W=args.W
        self.H=args.H

    def reset(self):
        self.u = 0
        self.done = False
        self.SF = RJSP(self.n, self.m, self.agv_num, self.PT, self.MT, self.TT, self.L_U)
        self.SF.reset()
        self.max_o_len=max([len(Pi) for Pi in self.PT])
        self.s = np.zeros([4, self.W,self.H], dtype=float)
        for i in range(self.n):
            last_site=self.m
            for j in range(len(self.PT[i])):
                self.s[0][i][j*2]=self.TT[last_site][self.MT[i][j]]
                self.s[0][i][j*2+1]=self.PT[i][j]
                last_site=self.MT[i][j]
        # print(self.s)
        fs=self.features()
        return [self.s,fs],self.done

    def update_state(self,Job):
        O_num=self.SF.Jobs[Job].cur_op-1
        AGV_ut=self.SF.Jobs[Job].PRE_AGV.using_time[-1]
        Machine_ut=self.SF.Jobs[Job].PRE_Machine.using_time[-1]
        self.s[0][Job][O_num*2],self.s[0][Job][O_num*2+1]=0,0
        self.s[1][Job][O_num * 2], self.s[2][Job][O_num * 2]=AGV_ut[0],AGV_ut[1]
        self.s[1][Job][O_num * 2+1], self.s[2][Job][O_num * 2+1] = Machine_ut[0], Machine_ut[1]
        Cmax=self.SF.C_max
        M_U=[float(Mi.total)/float(Cmax) for Mi in self.SF.Machines]
        AGV_U=[float(AGVi.total)/float(Cmax) for AGVi in self.SF.AGVs]
        for i in range(self.n):
            for j in range(self.SF.Jobs[i].cur_op):
                self.s[3][i][j*2]=AGV_U[self.SF.Jobs[i]._onAGV[j]]
                if self.MT[i][j]!=4:
                    self.s[3][i][j*2+1]=M_U[self.MT[i][j]]
                else:
                    self.s[3][i][j * 2 + 1] =0
        return self.s

    def features(self):
        S_=[]
        Jobs = [Job for Job in self.SF.Jobs if not Job.Finished]
        Remain_t=0
        DT=0
        for Ji in Jobs:
            Remain_t+=sum(Ji.PT[Ji.cur_op:])
            PRR=Ji.MT[Ji.cur_op-1:]
            PRR0=PRR[0]
            del PRR[0]
            for PRRi in PRR:
                DT+=self.SF.TT[PRR0][PRRi]
                PRR0=PRRi

        # average remaining effective transportation time
        PRRT=DT/len(self.SF.AGVs)

        S_.append(PRRT)
        #  the average remaining processing time of all jobs
        if len(Jobs)!=0:
            PT_art=Remain_t/len(Jobs)
        else:
            PT_art = 0
        S_.append(PT_art)

        # the current total transportation time of robot Ri to the current robot completion time
        PRT_R=[]
        for Ri in self.SF.AGVs:
            if Ri.end!=0:
                PRT_R.append(Ri.total_trans/Ri.end)
            else:
                PRT_R.append(0)
        S_.extend(PRT_R)
        # the ratio of the current load of the machine Mi to the current completion time of the machine
        PML=[]
        PMLt=0
        for Mi in self.SF.Machines:
            if Mi.end!=0:
                PML.append(Mi.total/Mi.end)
            else:
                PML.append(0)
            PMLt+=Mi.total
        S_.extend(PML)
        #the ratio of the total load of the machine to the completion time of the machine
        PMLI=PMLt/len(self.SF.Machines)
        S_.append(PMLI)
        return S_

    def u_update(self):
        P = 0
        for agv in self.SF.AGVs:
            P += agv.total
        for m in self.SF.Machines:
            P += m.total
        C_max = self.SF.C_max
        if C_max == 0:
            self.u = 0
        else:
            self.u = float(P) / (float(C_max) * (self.m + self.agv_num))

    def step(self,action):
        Job_i, agvi = action_translator(action, self.SF)
        self.SF.decode(Job_i, agvi)
        self.s = self.update_state(Job_i.idx)
        fs = self.features()
        u1 = copy.copy(self.u)
        self.u_update()
        u2 = copy.copy(self.u)
        r = u2 - u1
        num_Finished = 0
        for Ji in self.SF.Jobs:
            if Ji.Finished:
                num_Finished += 1
        if num_Finished == self.n:
            self.done = True
        return [self.s, fs], r, self.done

if __name__=="__main__":
    from JSP_AGV.Instance.Text_extract import data
    from JSP_AGV.Experiment.params import get_args, change_Envargs, change_RLargs

    Ci = "C1"
    Ki = '11'
    f = r'..\Instance\Bilge_Ulusoy' + '/' + Ci + '/' + 'E' + Ki + '.pkl'
    n, m, PT, agv_trans, MT, agv_num = data(f)
    args = get_args(n, m, agv_num, PT, MT, agv_trans, W=n, H=8, per=False, Network_type='CNN_DNN', DDQN=False,
                    GAMMA=0.95, BATCH_SIZE=128, LR=0.0001, Q_NETWORK_ITERATION=50)
    for i in range(1):
        env = Env(args)
        env.reset()
        re=0
        while True:
            k=4
            next_state, reward, done = env.step(k)
            re+=reward
            if done:
                break
