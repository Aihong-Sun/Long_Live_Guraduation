'''
对多目标算法进行测试

'''

from FJSP.Algo.AOA.aoa import AOA,IAOA
from FJSP.Algo.AOA.FJSP_problem import *
from FJSP.Shop_Floor.Job_Shop import Job_shop
from FJSP.Instance.Simulation_instance import *
from FJSP.Shop_Floor.utils import *
import pickle
import os
import copy
import time
from FJSP.Shop_Floor.Job_Shop import Job_shop
from FJSP.Instance.Instance_extraction import Instance
from FJSP.Shop_Floor.utils import *
from FJSP.Algo.GA.Pop_Generator import *
from FJSP.Instance.Simulation_instance import *
from FJSP.Algo.NSGA.Operator import Operate
from FJSP.Algo.NSGA.nsga import NSGA
from FJSP.Algo.utils import *
from FJSP.Algo.MOEA_D.moead import *
from Eva_Indicators import *



# AOA 算法

# 初始化相关参数
numOfObj,\
lowerBound,\
upperBound,\
maximumIteration,\
C1,C2,C3, C4,\
function, dim, positionLimit,\
limitFunction, fitness,\
Job_shop, J_site, M_option, OS=Static_FJSP_Info(n, m, PT, MT, ni, numofObj=100,         #种群数量
                                                    lowerBound=-10,          #上下界
                                                    upperBound=10,
                                                    maximumIteration=100,   #迭代次数
                                                    C1=2,                   #位置更新参数
                                                    C2=6,
                                                    C3=2,
                                                    C4=0.5,EC=EC,ESPC=ESPC)

t1=time.time()
EP1, population, best_val=AOA(numOfObj,lowerBound,upperBound,maximumIteration,
        C1,C2,C3, C4,function, dim, positionLimit,limitFunction, fitness,Job_shop, J_site, M_option, OS)
t2=time.time()

BF=[]
n=8

p = Pop(100, Job_shop)
pi = p.Get_Pop()
#NSGA-Ⅱ
ga=NSGA(Pop_size=100,gene_size=100)
EP2, C_max1, ec1=ga.main(pi,Operate,Job_shop)

#MOEA/D
algo=MOEA_D(Pop_size=100,gene_size=100)
EP3, C_max2, ec2=algo.main(pi,Operate,Job_shop)

Plot_NonDominatedSet(EP1, shape='.', G_label='AOA', xlable='Cmax', ylable='Total Energy Comsumption')
Plot_NonDominatedSet(EP2, shape='.', G_label='NSGA-II', xlable='Cmax', ylable='Total Energy Comsumption')
Plot_NonDominatedSet(EP3, shape='.', G_label='MOEA/D', xlable='Cmax', ylable='Total Energy Comsumption')
plt.show()

print('计算spacing指标值')
#计算spacing指标值
sol=[]
for ei in EP1:
    sol.append(ei.fitness)
sol=np.array((sol))
spacing=sp_indicator(sol)
print('AOA算法：',spacing)

sol=[]
for ei in EP2:
    sol.append(ei.fitness)
sol=np.array((sol))
spacing=sp_indicator(sol)
print('NSGA-II算法：',spacing)
sol=[]
for ei in EP3:
    sol.append(ei.fitness)
sol=np.array((sol))
spacing=sp_indicator(sol)
print('MOEA/D算法：',spacing)