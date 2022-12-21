

class Popi:
    def __init__(self,Job_Shop,chs1=[],chs2=None,chs3=None,chs4=None,Op_site=None):
        '''
        :param Job_Shop:
        :param chs1:  批量分割层
        :param chs2: 工艺路径选择层
        :param chs3: 工序排序层
        :param chs4: 机器选择层
        :param Op_site: 工序对应位置
        '''
        self.Op_site=Op_site
        # print(self.Op_site)
        self.JS=Job_Shop
        self.chs1,self.chs2,self.chs3,self.chs4=chs1,chs2,chs3,chs4
        if self.chs1==[]:
            self.fitness=self.decode_Normal()
        else:
            if isinstance(self.chs2[0],list):
                self.fitness = self.Decode_Consistent_Improve()
            else:
                self.fitness=self.Decode_consistent()
        self.n=len(self.JS.Ord_Set)

    #b不考虑分批的解码
    def decode_Normal(self):
        self.JS.reset()         #初始化
        self.JS.order_reset()

        for i in self.chs3:     #读取工序排序层
            O_num=self.JS.Ord_Set[i].cur_op     #判断当前工件对应的工序
            M_idx=self.chs4[self.Op_site.index([i,O_num])]      #解码获取加工位置
            if self.chs2[i]==1:
                if O_num==1:        #当工艺具有柔性时，解码过程
                    M_idx=self.chs4[self.Op_site.index([i,2])]
                elif O_num==2:
                    M_idx = self.chs4[self.Op_site.index([i, 1])]
            Opath=self.chs2[i]
            self.JS.decode(i,M_idx,Opath)
        return self.JS.C_max,self.JS.T_tard,self.JS.tard_num

    #考虑分批的解码
    def Decode_consistent(self):
        self.JS.reset()     #初始化机器
        self.JS.order_spilt(self.chs1)  #初始化订单及子批划分情况
        C_stage=dict(enumerate([0 for _ in range(self.JS.Ord_num)]))     #用于记录每阶段各工件批的完工时间
        for i in range(self.JS.Op_num):
            for i in self.chs3:
                ft=self.JS.decode_Consistent(i,self.chs2[i])      #对第i批工件进行解码，返回值为批次最后一个子批的完工时间
                C_stage[i]=ft
            C_stage=dict(sorted(C_stage.items(),key=lambda x:x[1]))
            self.chs3=[k for k,v in C_stage.items()]
        return self.JS.C_max, self.JS.T_tard, self.JS.tard_num

    def Decode_Consistent_Improve(self):
        self.JS.reset()  # 初始化机器
        self.JS.order_spilt(self.chs1)  # 初始化订单及子批划分情况
        C_stage = dict(enumerate([0 for _ in range(self.JS.Ord_num)]))  # 用于记录每阶段各工件批的完工时间
        for i in range(self.JS.Op_num):
            for i in self.chs3:
                ft = self.JS.decode_Consistent_Improved(i, self.chs2[i])  # 对第i批工件进行解码，返回值为批次最后一个子批的完工时间
                C_stage[i] = ft
            C_stage = dict(sorted(C_stage.items(), key=lambda x: x[1]))
            self.chs3 = [k for k, v in C_stage.items()]
        return self.JS.C_max, self.JS.T_tard, self.JS.tard_num
