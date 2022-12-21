import random
import copy
from FJSP.Algo.GA.Individual import Popi

# 种群
class Pop:
    def __init__(self,Pop_size,Job_Shop,SJS=None):
        '''
        :param Pop_size: 初始种群规模
        :param Job_Shop: 车间环境
        :param RI_rate: 采用随机初始化种群的概率
        :param LI_rate: 采用局部初始化种群的概率
        :param GI_rate: 采用全局初始化种群的概率
        '''
        self.Pop_size=Pop_size
        self.JS=Job_Shop
        self.RI_rate=0.2
        self.LI_rate=0.2
        self.GI_rate=0.6
        self.GLS_rate=0
        self.args=SJS
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

    #华科张国辉老师的博士论文的全局初始化方式
    def GS_MS(self):
        n_lis=[_ for _ in range(self.JS.n)]
        op=[0 for _ in range(self.JS.n)]
        m_load=[0 for _ in range(self.JS.m)]
        chs2=[0 for _ in range(len(self.os_list))]
        while n_lis!=[]:
            J_idx=random.choice(n_lis)
            for j in range(len(self.JS.Jobs[J_idx].processing_machine)):
                m_l = []
                for i in range(len(self.JS.Jobs[J_idx].processing_machine[op[J_idx]])):
                    k = self.JS.Jobs[J_idx].processing_machine[op[J_idx]][i]
                    load = m_load[k - 1]
                    pt = self.JS.Jobs[J_idx].processing_time[op[J_idx]][i]
                    m_l.append(load + pt)
                min_ml = min(m_l)
                m_idx = m_l.index(min_ml)
                o_idx = self.J_site.index((J_idx, op[J_idx]))
                chs2[o_idx] = m_idx
                m_load[self.JS.Jobs[J_idx].processing_machine[op[J_idx]][m_idx] - 1] = min_ml
                op[J_idx] += 1
            n_lis.remove(J_idx)
        return chs2

    #全局初始化
    def GLS(self):
        for i in range(int(self.Pop_size * self.GLS_rate)):
            random.shuffle(self.os_list)  # 打乱工序序列
            chs1 = copy.deepcopy(self.os_list)
            chs2=self.GS_MS()
            pi = Popi(copy.copy(self.JS), chs1, chs2, self.J_site, self.args)
            self.P.append(pi)

    def Get_Pop(self):
        # 种群初始化
        self.In_Initial()
        self.RI()
        self.LI()
        self.GI()
        self.GLS()
        return self.P
