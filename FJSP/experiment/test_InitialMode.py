'''
初始化方式的实验对比
论证阿基米德算法的初始化方法的有效性，主要对比4种，采用随机初始化的AOA、采用基于机器负荷的初始化AOA、采用基于最短加工时间的AOA和本文的初始化方法。
'''
'''
    使用随机算例进行阿基米德灵敏度分析实验--静态单目标
'''

from FJSP.Algo.AOA.aoa import *
from FJSP.Algo.AOA.FJSP_problem import *
from FJSP.Instance.Instance_extraction import Instance
from FJSP.Shop_Floor.utils import *
import pickle
import os
import matplotlib.pyplot as plt

# 静态
test_name="Mk01"
file=r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\Instance\FJSP_Instance'+'/' + test_name+'.pkl'
n, m, PT, MT, ni = Instance(file)
SJS=None
# 初始种群的最优解完工时间和种群平均完工时间的对比
numOfObj, \
lowerBound, \
upperBound, \
maximumIteration, \
c1, c2, c3, c4, \
function, dim, positionLimit, \
limitFunction, fitness, \
Job_shop, J_site, M_option, OS=Static_FJSP_Info(n, m, PT, MT, ni, numofObj=100,  #种群数量
                                                lowerBound=-10,  #上下界
                                                upperBound=10,
                                                maximumIteration=100,  #迭代次数
                                                C1=2,  # 位置更新参数
                                                C2=6,
                                                C3=2,
                                                C4=0.5, )
Min_score,Ave_Score=[[] for _ in range(6)],[[] for _ in range(6)]
#运行10次
label=['RS','MLS','SPTS','SPTS+RS','MLS+RS','SPTS+MLS+RS']
GL_value=[(0,0),(1,0),(0,1),(0,0.4),(0.4,0),(0.5,0.2)]
print('------------------------初始化种群质量的评估----------------------------------')
for i in range(10):
    # print('-------------------','第',_+1,'次迭代-------------------')
    #随机初始化方法:RS
    for _ in range(len(GL_value)):
        Pop=generatePopulation(numOfObj,lowerBound,upperBound,mainFunction,dim,positionLimit,limitFunction,copy.deepcopy(Job_shop),J_site,M_option,OS,copy.deepcopy(SJS),Grate=GL_value[_][0],Lrate=GL_value[_][1])
        score=[pi.fitness for pi in Pop]
        # print(label[_],'最优解完工时间：',min(score),'种群平均完工时间：',round(sum(score)/len(score),2))
        Min_score[_].append(min(score))
        Ave_Score[_].append(round(sum(score)/len(score),2))

for i in range(6):
    print(label[i],'最优解完工时间：',round(sum(Min_score[i])/10,2),'种群平均完工时间：',round(sum(Ave_Score[i])/10,2))



Min_score,Ave_Score=[[] for _ in range(6)],[[] for _ in range(6)]
#运行10次
print('------------------------最终解种群质量的评估----------------------------------')
BV=[[] for _ in range(10)]  #用于记录迭代曲线
for i in range(10):
    #随机初始化方法:RS
    for _ in range(len(GL_value)):
        solution, population, best_val=AOA(numOfObj,lowerBound,upperBound,maximumIteration,
                                c1,c2,c3,c4,function, dim, positionLimit,limitFunction, fitness,Job_shop, J_site, M_option, OS,Grate=GL_value[_][0],Lrate=GL_value[_][1])
        score=[pi.fitness for pi in population]
        print(label[_],'最优解完工时间：',solution.fitness,'种群平均完工时间：',round(sum(score)/len(score),2))
        Min_score[_].append(solution.fitness)
        Ave_Score[_].append(round(sum(score)/len(score),2))
        BV[i].append(best_val)


print('-------------最终解10次迭代的最终统计结果----------------------')
for i in range(6):
    print(label[i],'最优解完工时间：',round(sum(Min_score[i])/10,2),'种群平均完工时间：',round(sum(Ave_Score[i])/10,2))


