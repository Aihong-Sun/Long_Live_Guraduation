'''
对文献[5]	唐亮,程峰,吉卫喜,金志斌.改进ICA求解柔性作业车间插单重调度问题[J]计算机工程与应用,2022
中算例进行实验论证

'''
import matplotlib.pyplot as plt

from FJSP.Algo.AOA.aoa import AOA
from FJSP.Algo.AOA.FJSP_problem import *
from FJSP.Instance.Simulation_instance import *
from FJSP.Shop_Floor.utils import *
import pickle
import os


font = {'family' : 'Simsun',
'weight' : 'normal',
'size'   : 13,
        }

test='static'   # static/dynamic,其中static表示静态调度，dynamic表示动态调度

# 静态
test_name="Mk01"
# file=r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\Instance\FJSP_Instance'+'/' + test_name+'.pkl'
# n, m, PT, MT, ni = Instance(file)
# print('1',MT)
# n=8
# #动态
# test_name="Mk01"
file=r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\static_sched'+'/' + test_name+'.pkl'
resched_t=10 #重调度时刻
PT1=[[[5, 4], [3, 5, 1], [4, 2], [5, 6, 1], [1], [6, 6, 3]], [[6], [1], [2], [6, 6], [5, 6, 1]], [[6], [4, 2], [5, 6, 1], [4, 6, 6], [1, 5]]]
MT1=[[[1, 3], [5, 3, 2], [3, 6], [6, 2, 1], [3], [6, 3, 4]], [[2], [3], [1], [2, 4], [6, 2, 1]], [[2], [3, 6], [6, 2, 1], [3, 2, 6], [1, 5]]]

if test=='static':
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
                                                        C4=0.5)
    solution, population, best_val=AOA(numOfObj,lowerBound,upperBound,maximumIteration,
            C1,C2,C3, C4,function, dim, positionLimit,limitFunction, fitness,Job_shop, J_site, M_option, OS)

    JS = Get_JS(solution.position, Job_shop, J_site, M_option, OS)
    result_path = r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\static_sched'
    dic = {'job_shop_env': JS, 'score': solution.fitness}
    print(f"Best Solution \nBestScore: {solution.fitness} "
          # f"\n CPU(s): {round(t2 - t1, 2)}\n"
          )
    with open(os.path.join(result_path, test_name + ".pkl"), "wb") as f:
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)
    x = [_ for _ in range(len(best_val))]
    # b1=[_[0] for _ in best_val]
    # b2 = [_[1] for _ in best_val]
    Gantt(JS.Machines)
    plt.plot(x, best_val)
    plt.xlabel('迭代次数',font)
    plt.ylabel('完工时间',font)
    plt.show()
    # plt.plot(x, b2)
    # plt.show()

if test=='dynamic':
    numOfObj, \
    lowerBound, \
    upperBound, \
    maximumIteration, \
    C1, C2, C3, C4, \
    function, dim, positionLimit, \
    limitFunction, fitness, \
    Job_shop, J_site, M_option, OS,SJS = Dynamic_FJSP_Info(file,resched_t,MT1,PT1,
                                                      numofObj=100,  # 种群数量
                                                      lowerBound=-10,  # 上下界
                                                      upperBound=10,
                                                      maximumIteration=100,  # 迭代次数
                                                      C1=2,  # 位置更新参数
                                                      C2=6,
                                                      C3=2,
                                                      C4=0.5)
    solution, population, best_val = AOA(numOfObj, lowerBound, upperBound, maximumIteration,
                                         C1, C2, C3, C4, function, dim, positionLimit, limitFunction, fitness, Job_shop,
                                         J_site, M_option, OS,SJS)

    JS = decode(solution.position, Job_shop, J_site, M_option, OS)
    result_path = r'/FJSP/dyna_sched'
    dic = {'job_shop_env': JS, 'score': solution.fitness}
    with open(os.path.join(result_path, test_name + ".pkl"), "wb") as f:
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)
    x = [_ for _ in range(len(best_val))]
    plt.plot(x, best_val)
    plt.show()
