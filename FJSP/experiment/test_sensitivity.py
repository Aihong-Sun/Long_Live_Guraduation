from FJSP.Algo.AOA.aoa import AOA
from FJSP.Algo.AOA.FJSP_problem import *
from FJSP.Shop_Floor.Job_Shop import Job_shop
from FJSP.Instance.Instance_extraction import Instance
from FJSP.Shop_Floor.utils import *
import pickle
import os


test='static'   # static/dynamic,其中static表示静态调度，dynamic表示动态调度

# 静态
Test_name=['15_8']

C1=[1,2,3,4]
C2=[2,4,6,8]
C3=[1,2,3,4]
C4=[0.5,1,1.5,2]

Pair = [[1, 1, 1, 1],
        [1, 2, 2, 2],
        [1, 3, 3, 3],
        [1, 4, 4, 4],
        [2, 1, 2, 3],
        [2, 2, 1, 4],
        [2, 3, 4, 1],
        [2, 4, 3, 2],
        [3, 1, 2, 4],
        [3, 2, 4, 3],
        [3, 3, 1, 2],
        [3, 4, 2, 1],
        [4, 1, 4, 2],
        [4, 2, 3, 1],
        [4, 3, 2, 4],
        [4, 4, 1, 3]]

import matplotlib.pyplot as plt

#绘制参数水平趋势图
def plot_param_select(value,Pair):
    plt.rcParams['font.sans-serif'] = 'Times New Roman'
    font = {'family': 'serif', 'style': 'italic','weight':'normal', 'color':'black', 'size':12 }    #设置字体格式
    C=[[[] for _ in range(4)] for _ in range(4)]
    for j in range(len(Pair)):
        pi=Pair[j]
        for i in range(len(pi)):
            C[i][pi[i]-1].append(value[j])
    C_v=[[] for i in range(4)]
    for i in range(len(C)):
        K=C[i]
        for ki in K:
            C_v[i].append(round(sum(ki)/len(ki),2))
    f, ax = plt.subplots(1,4)
    # 设置主标题
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    # plt.xlabel(fontsize=13)
    # plt.ylabel(fontsize=13)
    for i in range(len(C_v)):
        ax[i].set_title('C'+str(i+1),fontdict=font)
        ax[i].plot([1,2,3,4],C_v[i],color='black',linewidth=1,marker='o',markersize=5)
        # ax[i].scatter([1, 2, 3, 4], C_v[i],color='r')
        if i>0:
            ax[i].set_yticks([])
        if i==0:
            ax[i].set_ylabel('Cmax',fontsize=13)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.15)
    plt.show()

for test_name in Test_name:
    print('---------Start Experimenting-------Scale:',test_name,'----------')
    file = r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\Instance\Stochastic_Ins' + '/' + test_name + '.pkl'
    n, m, PT, MT, ni = Instance(file)
    Value = []
    for pi in Pair:
        S=[]
        print('---------------------testing_object:',pi)
        for i in range(10):
            numOfObj,\
            lowerBound,\
            upperBound,\
            maximumIteration, \
            c1, c2, c3, c4,\
            function, dim, positionLimit,\
            limitFunction, fitness,\
            Job_shop, J_site, M_option, OS=Static_FJSP_Info(n, m, PT, MT, ni, numofObj=100,         #种群数量
                                                                lowerBound=-10,          #上下界
                                                                upperBound=10,
                                                                maximumIteration=10,   #迭代次数
                                                                C1=C1[pi[0]-1],                   #位置更新参数
                                                                C2=C2[pi[1]-1],
                                                                C3=C3[pi[2]-1],
                                                                C4=C4[pi[3]-1])
            solution, population, best_val=AOA(numOfObj,lowerBound,upperBound,maximumIteration,
                    c1,c2,c3,c4,function, dim, positionLimit,limitFunction, fitness,Job_shop, J_site, M_option, OS)

            JS = Get_JS(solution.position, Job_shop, J_site, M_option, OS)
            result_path = r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\static_sched'
            dic = {'job_shop_env': JS, 'score': solution.fitness}
            with open(os.path.join(result_path, test_name + ".pkl"), "wb") as f:
                pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)
            S.append(solution.fitness)
            # x = [_ for _ in range(len(best_val))]
            # plt.plot(x, best_val)
            # plt.show()
        print('平均分值：',round(sum(S)/len(S),3),'C1:',c1,'C2:',c2,'C3:',c3,'C4:',c4)
        Value.append(round(sum(S)/len(S),2))
    plot_param_select(Value,Pair)