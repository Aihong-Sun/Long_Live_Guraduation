'''
单个个体
'''
import copy

class Popi:
    def __init__(self,Job_Shop,chs1,chs2,J_site,SJS):
        '''
        :param Job_Shop: 车间环境参数
        :param chs1: 工序编码
        :param chs2: 机器编码
        :param args: 若为重调度，则为原方案调度结果
        '''
        self.JS=copy.deepcopy(Job_Shop)
        self.ms_minpt = []
        for i in range(self.JS.n):
            self.ms_minpt.extend([pi.index(min(pi)) for pi in self.JS.Jobs[i].processing_time][self.JS.Jobs[i].cur_op:])
        self.J_site=J_site
        self.chs1,self.chs2=chs1,chs2
        self.n=self.JS.n
        self.fitness=self.Initial_decode(SJS)


    #初始调度方案的解码
    def Initial_decode(self,SJS):
        for i in self.chs1:     #依次读取工序编码进行解码
            O_num=self.JS.Jobs[i].cur_op   #获取当前解码工件已解码工序
            m_idx = self.J_site.index((i, O_num))   #获取对应工序的机器索引
            self.JS.decode(i,self.chs2[m_idx])      #解码
        if SJS:  # 双目标
            num_Dp = self.JS.Scheme_Comparison(SJS)
            return self.JS.C_max, num_Dp
        elif self.JS.Energy_Consumption != None and SJS != None:  # 三目标
            num_Dp = self.JS.Scheme_Comparison(SJS)
            T_ec = self.JS.Total_Energy_Comsumption()
            return self.JS.C_max, num_Dp, T_ec
        elif self.JS.Energy_Consumption != None and SJS == None:
            T_ec = self.JS.Total_Energy_Comsumption()
            return self.JS.C_max, T_ec
        else:  # 单目标
            return self.JS.C_max




