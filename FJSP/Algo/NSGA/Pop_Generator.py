import random
import copy
from FJSP.Algo.NSGA.Individual import Popi

# 种群
class Pop:
    def __init__(self,Pop_size,Job_Shop,*args):
        '''
        :param Pop_size: 初始种群规模
        :param Job_Shop: 车间环境
        :param RI_rate: 采用随机初始化种群的概率
        :param LI_rate: 采用局部初始化种群的概率
        :param GI_rate: 采用全局初始化种群的概率
        '''
        self.Pop_size=Pop_size
        self.JS=Job_Shop
        self.RI_rate=0.3
        self.LI_rate=0.2
        self.GI_rate=0.5
        self.args=args
        self.P=[]     #种群

    #获取编码相关的信息
    def In_Initial(self):
        self.os_list = []  # 工序序列
        self.ms_list, self.J_site = [], []  # 机器序列和工序对应的位置
        self.ms_minpt = []

        for i in range(self.JS.n):
            self.os_list.extend([i for _ in range(self.JS.Jobs[i].O_num)][self.JS.Jobs[i].cur_op:])
            self.ms_list.extend([len(pi) for pi in self.JS.Jobs[i].processing_machine][self.JS.Jobs[i].cur_op:])
            self.J_site.extend([(i, j) for j in range(self.JS.Jobs[i].O_num)][self.JS.Jobs[i].cur_op:])
            self.ms_minpt.extend([pi.index(min(pi)) for pi in self.JS.Jobs[i].processing_time][self.JS.Jobs[i].cur_op:])

    # 随机初始化方式
    def RI(self):
        for i in range(int(self.Pop_size*self.RI_rate)):
            random.shuffle(self.os_list)        # 打乱工序序列
            chs1=copy.deepcopy(self.os_list)
            chs2=[random.randint(0,_-1) for _ in self.ms_list]
            pi=Popi(copy.copy(self.JS),chs1,chs2,self.J_site,self.args)
            self.P.append(pi)

    # 局部初始化方式
    def LI(self):
        for i in range(int(self.Pop_size*self.LI_rate)):
            random.shuffle(self.os_list)        # 打乱工序序列
            chs1=copy.deepcopy(self.os_list)
            pi=Popi(copy.copy(self.JS),chs1,self.ms_minpt,self.J_site,self.args)
            self.P.append(pi)

    #全局初始化方式
    def GI(self):
        for i in range(int(self.Pop_size*self.GI_rate)):
            random.shuffle(self.os_list)        # 打乱工序序列
            chs1=copy.deepcopy(self.os_list)    # 工序序列
            m_load=[0 for _ in range(self.JS.m)]
            chs2=[0 for _ in range(len(self.ms_list))]
            op=[_.cur_op for _ in self.JS.Jobs]
            for ci in chs1:
                m_l=[]
                for i in range(len(self.JS.Jobs[ci].processing_machine[op[ci]])):
                    k=self.JS.Jobs[ci].processing_machine[op[ci]][i]
                    load=m_load[k-1]
                    pt=self.JS.Jobs[ci].processing_time[op[ci]][i]
                    m_l.append(load+pt)
                min_ml=min(m_l)
                m_idx=m_l.index(min_ml)
                o_idx=self.J_site.index((ci,op[ci]))
                chs2[o_idx]=m_idx
                m_load[self.JS.Jobs[ci].processing_machine[op[ci]][m_idx]-1]=min_ml
                op[ci] += 1
            pi=Popi(copy.deepcopy(self.JS),chs1,chs2,self.J_site,self.args)
            self.P.append(pi)

    def Get_Pop(self):
        # 种群初始化
        self.In_Initial()
        self.RI()
        self.LI()
        self.GI()
        return self.P

if __name__=="__main__":

    from FJSP.Shop_Floor.Job_Shop import Job_shop
    from FJSP.Instance.Instance_extraction import Instance
    from FJSP.Shop_Floor.utils import *

    n,m,PT,MT,ni=Instance(r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\Instance\FJSP_Instance' + "/Mk01.pkl")
    JS=Job_shop(n,m,ni,MT,PT)
    JS.reset()
    p=Pop(10,JS)
    pi=p.Get_Pop()
    Gantt(pi[0].JS.Machines)
    SJS=copy.deepcopy(pi[0].JS)
    PT=[[[5, 4], [3, 5, 1], [4, 2], [5, 6, 1], [1], [6, 6, 3]], [[6], [1], [2], [6, 6], [5, 6, 1]], [[6], [4, 2], [5, 6, 1], [4, 6, 6], [1, 5]]]
    MT=[[[1, 3], [5, 3, 2], [3, 6], [6, 2, 1], [3], [6, 3, 4]], [[2], [3], [1], [2, 4], [6, 2, 1]], [[2], [3, 6], [6, 2, 1], [3, 2, 6], [1, 5]]]
    Gantt(pi[0].JS.Machines)
    JS=pi[0].JS
    JS.resched(10, MT, PT)
    p = Pop(10, JS,SJS)
    pi = p.Get_Pop()
    Gantt(pi[0].JS.Machines)

