from Batch_Schedule.Algo.Individual import Popi
import random
import copy
import numpy as np

# 不考虑分批
class Pop_NotSpilt:
    def __init__(self,Pop_size,Job_Shop):
        self.Pop_size=Pop_size
        self.JS=Job_Shop

    # 获取初始工序编码、工序所在位置及分批后的工件数量
    def Get_InitialInfo(self):
        self.JS.order_reset()
        self.Op_Site=[]
        self.OS_lis=[]
        self.Job_num=len(self.JS.Ord_Set)
        for i in range(self.Job_num):
            for j in range(self.JS.Op_num):
                self.Op_Site.append([i,j])
                self.OS_lis.append(i)

    def Initial_Random(self):
        Pop=[]
        self.Get_InitialInfo()
        for i in range(self.Pop_size):
            chs2=[random.randint(0,1) for _ in range(self.Job_num)]
            random.shuffle(self.OS_lis)
            chs3=copy.copy(self.OS_lis)
            chs4=[]
            for k in range(self.Job_num):
                for j in range(len(self.JS.Mac_Lis)):
                    chs4.append(random.randint(0,len(self.JS.Mac_Lis[j])-1))
            Pi=Popi(self.JS,chs2=chs2,chs3=chs3,chs4=chs4,Op_site=self.Op_Site)
            Pop.append(Pi)
        return Pop

#等量分批
class Pop_Equalbatch():
    def __init__(self,Pop_size,Job_Shop):
        self.Pop_size=Pop_size
        self.JS=Job_Shop

    #设置最大批次数
    def Max_BatchNum(self):
        self.MB=[]
        for i in range(len(self.JS.Ord_Lis['orderId'])):
            if self.JS.Ord_Lis['count']<5000:
                self.MB.append(1)
            else:
                self.MB.append(min(int(self.JS.Ord_Lis['count']/3000),10))

    # 获取初始工序编码、工序所在位置及分批后的工件数量
    def Get_InitialInfo(self):
        self.Op_Site=[]
        self.OS_lis=[]
        self.Job_num=len(self.JS.Ord_Set)
        for i in range(self.Job_num):
            for j in range(self.JS.Op_num):
                self.Op_Site.append([i,j])
                self.OS_lis.append(i)

    #初始化批次:BS+OS段，BS表示各订单的分批次数情况，OS
    def Bacth_Initial(self):
        #
        self.BS=[]
        for i in range(self.Pop_size):
            self.BS.append([random.randint(0,_) for _ in self.MB])

    def Initial_NotSpiltInfo(self):
        Pop=[]
        self.Get_InitialInfo()
        for i in range(self.Pop_size):
            chs2=[random.randint(0,1) for _ in range(self.Job_num)]
            random.shuffle(self.OS_lis)
            chs3=copy.copy(self.OS_lis)
            chs4=[random.randint(0,len(self.JS.Mac_Lis[_])-1) for _ in range(len(self.JS.Mac_Lis))]
            Pi=Popi(self.JS,chs2=chs2,chs3=chs3,chs4=chs4,Op_site=self.Op_Site)
            Pop.append(Pi)
        return Pop

# 可变分批：vaviable sub-lots
class Pop_VariSublot():
    pass

#一致分批：consistent sublots
# [1]张彪,孟磊磊,桑红燕,卢超.多目标变分批混合流水车间调度算法自动设计[J/OL].计算机集成制造系统:1-26[2022-11-16].
# [2]Zhang, Biao,Pan, Quan-ke,Meng, Lei-lei,Lu, Chao,Mou, Jian-hui,Li, Jun-qing.An automatic multi-objective
# evolutionary algorithm for the hybrid flowshop scheduling problem with consistent sublots[J].KNOWLEDGE-BASED SYSTEMS,2022,238
class Pop_ConsSublot:
    def __init__(self,Pop_size,Job_Shop,max_SpiltNum):
        self.Pop_size=Pop_size
        self.JS=Job_Shop
        self.max_SpiltNum=max_SpiltNum

    # Uniform initialization: lot split matrix
    def UI_LSMatrix(self):
        ls_Matrix=np.zeros((len(self.JS.Ord_Lis['orderId']),self.max_SpiltNum),dtype=int)
        self.Ord_Set = []
        for i in range(len(self.JS.Ord_Lis['orderId'])):
            if self.JS.Ord_Lis['count'][i]>5000:
                Lis = [int(self.JS.Ord_Lis['count'][i]/ self.max_SpiltNum) for _ in range(self.max_SpiltNum)]  # 批量等量分割
                rest = self.JS.Ord_Lis['count'][i] % self.max_SpiltNum
                for j in range(rest):
                    Lis[j] += 1
            else:
                Lis=[0 for _ in range(self.max_SpiltNum)]
                Lis[0]=self.JS.Ord_Lis['count'][i]
            ls_Matrix[i] = Lis
        # import pandas as pd
        # ls=pd.DataFrame(ls_Matrix)
        # ls.to_excel('R.xlsx')
        return ls_Matrix

    # Random initialization: lot split matrix
    def RI_LSMatrix(self):
        ls_Matrix = np.zeros((len(self.JS.Ord_Lis['orderId']), self.max_SpiltNum), dtype=int)
        self.Ord_Set = []
        for i in range(len(self.JS.Ord_Lis['orderId'])):
            Lis=[]
            k=0
            rest=self.JS.Ord_Lis['count'][i]
            while k<self.max_SpiltNum-1:
                if rest>8000:
                    ri=random.randint(2000,6000)
                else:
                    ri=rest
                Lis.append(ri)
                rest-=ri
                k+=1
            Lis.append(rest)
            ls_Matrix[i] = Lis
        # import pandas as pd
        # ls = pd.DataFrame(ls_Matrix)
        # ls.to_excel('R.xlsx')

        return ls_Matrix

    # Mixed initialization: lot split matrix
    def MI_LSMatrix(self):
        ls_Matrix = np.zeros((len(self.JS.Ord_Lis['orderId']), self.max_SpiltNum), dtype=int)
        self.Ord_Set = []
        for i in range(len(self.JS.Ord_Lis['orderId'])):
            Lis = [int(self.JS.Ord_Lis['count'][i] / self.max_SpiltNum) for _ in range(self.max_SpiltNum)]  # 批量等量分割
            rest = self.JS.Ord_Lis['count'][i] % self.max_SpiltNum
            SP_lis=[_ for _ in range(self.max_SpiltNum)]
            random.shuffle(SP_lis)
            for li in range(rest):
                Lis[SP_lis[li]]+=1
            for j in range(int(self.max_SpiltNum/2)):
                r=random.randint(0, int(Lis[j]/2))
                Lis[j]-=r
                Lis[int(self.max_SpiltNum/2)+j]+=r
            ls_Matrix[i]=Lis
        return ls_Matrix

    def Initial(self):
        os = [_ for _ in range(len(self.JS.Ord_Lis['orderId']))]
        Pop=[]
        # BatchSpilt=[self.UI_LSMatrix,self.MI_LSMatrix,self.RI_LSMatrix]
        for i in range(self.Pop_size):
            random.shuffle(os)
            # BM=random.choice(BatchSpilt)
            if random.random()<=0.4:
                chs1=self.MI_LSMatrix()
            elif random.random()<0.9:
                chs1 = self.UI_LSMatrix()
            else:
                chs1 = self.RI_LSMatrix()
            chs2=[random.randint(0,1) for i in range(self.JS.Ord_num)]
            chs3=copy.copy(os)
            pi=Popi(self.JS,chs1=chs1,chs2=chs2,chs3=chs3,chs4=None,Op_site=None)
            Pop.append(pi)
        return Pop

class Pop_ConsSublot_Improved:
    def __init__(self,Pop_size,Job_Shop,max_SpiltNum):
        self.Pop_size=Pop_size
        self.JS=Job_Shop
        self.max_SpiltNum=max_SpiltNum

    # Uniform initialization: lot split matrix
    def UI_LSMatrix(self):
        ls_Matrix=np.zeros((len(self.JS.Ord_Lis['orderId']),self.max_SpiltNum),dtype=int)
        self.Ord_Set = []
        for i in range(len(self.JS.Ord_Lis['orderId'])):
            Lis = [int(self.JS.Ord_Lis['count'][i]/ self.max_SpiltNum) for _ in range(self.max_SpiltNum)]  # 批量等量分割
            rest = self.JS.Ord_Lis['count'][i] % self.max_SpiltNum
            for j in range(rest):
                Lis[j] += 1
            ls_Matrix[i]=Lis
        return ls_Matrix

    # Random initialization: lot split matrix
    def RI_LSMatrix(self):
        ls_Matrix = np.zeros((len(self.JS.Ord_Lis['orderId']), self.max_SpiltNum), dtype=int)
        self.Ord_Set = []
        for i in range(len(self.JS.Ord_Lis['orderId'])):
            Lis=[]
            k=0
            rest=self.JS.Ord_Lis['count'][i]
            while k<self.max_SpiltNum-1:
                if rest>2000:
                    ri=random.randint(2000,rest)
                else:
                    ri=rest
                Lis.append(ri)
                rest-=ri
                k+=1
            Lis.append(rest)
            ls_Matrix[i] = Lis
        return ls_Matrix

    # Mixed initialization: lot split matrix
    def MI_LSMatrix(self):
        ls_Matrix = np.zeros((len(self.JS.Ord_Lis['orderId']), self.max_SpiltNum), dtype=int)
        self.Ord_Set = []
        for i in range(len(self.JS.Ord_Lis['orderId'])):
            Lis = [int(self.JS.Ord_Lis['count'][i] / self.max_SpiltNum) for _ in range(self.max_SpiltNum)]  # 批量等量分割
            rest = self.JS.Ord_Lis['count'][i] % self.max_SpiltNum
            SP_lis=[_ for _ in range(self.max_SpiltNum)]
            random.shuffle(SP_lis)
            for li in range(rest):
                Lis[SP_lis[li]]+=1
            for j in range(int(self.max_SpiltNum/2)):
                r=random.randint(0, Lis[j])
                Lis[j]-=r
                Lis[int(self.max_SpiltNum/2)+j]+=r
            ls_Matrix[i]=Lis
        return ls_Matrix

    #随机工艺路径生成
    def RI_RoutePath(self):
        chs2=[]
        for i in range(self.JS.Ord_num):
            chs2i=[random.randint(0,1) for _ in range(self.max_SpiltNum)]
            chs2.append(chs2i)
        return chs2

    def Initial(self):
        os = [_ for _ in range(len(self.JS.Ord_Lis['orderId']))]
        Pop=[]
        BatchSpilt=[self.UI_LSMatrix,self.MI_LSMatrix,self.RI_LSMatrix]
        for i in range(self.Pop_size):
            random.shuffle(os)
            BM=random.choice(BatchSpilt)
            chs1=BM()
            chs2=self.RI_RoutePath()
            chs3=copy.copy(os)
            pi=Popi(self.JS,chs1=chs1,chs2=chs2,chs3=chs3,chs4=None,Op_site=None)
            Pop.append(pi)
        return Pop

if __name__=='__main__':
    from Batch_Schedule.Shop_Floor.Shop import SF_env
    sf = SF_env(r'/Batch_Schedule\experiment/shang_Data.xlsx')
    sf.reset()
    Initial_Pop1 = Pop_ConsSublot(Pop_size=10, Job_Shop=sf, max_SpiltNum=10).Initial()
