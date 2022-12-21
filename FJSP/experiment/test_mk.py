'''
对mk系列进行测试

'''

from FJSP.Algo.AOA.aoa import AOA,IAOA
from FJSP.Algo.AOA.FJSP_problem import *
from FJSP.Shop_Floor.Job_Shop import Job_shop
from FJSP.Instance.Instance_extraction import Instance
from FJSP.Shop_Floor.utils import *
import pickle
import os
import time

# 静态
test_name="Mk02"
file=r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\Instance\FJSP_Instance'+'/' + test_name+'.pkl'
n, m, PT, MT, ni = Instance(file)

# #动态
# test_name="Mk01"
# file=r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\static_sched'+'/' + test_name+'.pkl'

for i in range(10):
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
                                                        C4=0.5,)
    t1=time.time()
    solution, population, best_val=IAOA(numOfObj,lowerBound,upperBound,maximumIteration,
            C1,C2,C3, C4,function, dim, positionLimit,limitFunction, fitness,Job_shop, J_site, M_option, OS)
    t2=time.time()

    print(f"Best Solution \nBestScore: {solution.fitness} "
          f"\n CPU(s): {round(t2 - t1, 2)}\n"
          )
    JS = Get_JS(solution.position, Job_shop, J_site, M_option, OS)
    result_path = r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\static_sched'
    dic = {'job_shop_env': JS, 'score': solution.fitness}
    with open(os.path.join(result_path, test_name + ".pkl"), "wb") as f:
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)
