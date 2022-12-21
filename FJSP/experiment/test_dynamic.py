'''
用于测试动态调度问题
'''

from FJSP.Algo.AOA.aoa import AOA,IAOA
from FJSP.Algo.AOA.FJSP_problem import *
from FJSP.Shop_Floor.utils import *
import pickle
import os
import copy
from FJSP.Instance.Simulation_instance import *


#载入静态调度方案
file=r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\static_sched\sim.pkl'
resched_t=10     #重调度时刻
MT1=[MT[8]]     #重调度工件加工机器
PT1=[PT[8]]     #重调度工件加工时间

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
                                                      maximumIteration=10,  # 迭代次数
                                                      C1=2,  # 位置更新参数
                                                      C2=6,
                                                      C3=2,
                                                      C4=0.5)
solution, population, best_val = AOA(numOfObj, lowerBound, upperBound, maximumIteration,
                                     C1, C2, C3, C4, function, dim, positionLimit, limitFunction, fitness, Job_shop,
                                     J_site, M_option, OS,SJS)

for s in solution:
    JS = Get_JS(s.position, copy.deepcopy(Job_shop), J_site, M_option, OS)
    result_path = r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\dyna_sched'
    dic = {'job_shop_env': JS, 'score': s.fitness}
    Gantt(JS.Machines)
    print(f"Best Solution \nBestScore: {s.fitness} "
          )
    with open(os.path.join(result_path, 'sim_dyna' + ".pkl"), "wb") as f:
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)
