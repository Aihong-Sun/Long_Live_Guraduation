
from Batch_Schedule.Shop_Floor.Shop import *
from Batch_Schedule.Algo.MOEAD import MOEA_D
from Batch_Schedule.Algo.NSGA import NSGA
from Batch_Schedule.Shop_Floor.ultis import *
from Batch_Schedule.Algo.Pop_Generator import *
from Batch_Schedule.Algo.Operators import *
from Batch_Schedule.Algo.utils import *
import time
# from Result_output import *

#算法测试
def Algo_test(Algo_list,Initial_Pop,Evolution_method,Pop_size,Iteration):
    EP,T_tard,C_max=[],[],[]
    cpu_t=[]
    for Algoi in Algo_list:
        t1=time.time()
        algoi=Algoi(Pop_size,Iteration)
        Epi,C_maxi,T_tardi=algoi.main(Initial_Pop,Evolution_method)
        EP.append(Epi)
        t2=time.time()
        C_max.append(C_maxi)
        T_tard.append(T_tardi)
        cpu_t.append(round(t2-t1,2))
    return EP,cpu_t,C_max,T_tard

def method_test(Algo,Initial_Pop,Evolution_method,Pop_size,Iteration):
    EP = []
    cpu_t = []
    C,T=[],[]
    for i in range(len(Initial_Pop)):
        t1 = time.time()
        algoi = Algo(Pop_size, Iteration)
        Epi,C_max,Ti = algoi.main(Initial_Pop[i], Evolution_method[i])
        C.append(C_max)
        T.append(Ti)
        EP.append(copy.copy(Epi))
        t2 = time.time()
        cpu_t.append(round(t2 - t1, 2))
    return EP, cpu_t,C,T

#结果展示
def Sched_Result(EP,label,title):
    for EPi in EP:
        Gantt(EPi[0].JS.Mac_Lis)    #随便选个前沿解绘制Gantt图
        Tard_barh(EPi[0].JS.Ord_Set)
    for i in range(len(EP)):
        Plot_NonDominatedSet(EP[i], shape='.', G_label=label[i], xlable='makespan', ylable='Total tardiniess')
    plt.title(title)
    plt.show()

test='method_compare' # 'Algo_Compare'/'method_compare'

# 算法对比
if test=='Algo_Compare':
    sf = SF_env('shang_Data.xlsx')
    sf.reset()
    Algo_list=[NSGA,MOEA_D]
    Initial_Pop=Pop_ConsSublot(Pop_size=200,Job_Shop=sf,max_SpiltNum=10).Initial()
    EP,cpu_t,C,T=Algo_test(Algo_list,Initial_Pop,Evolution_consistent,Pop_size=200,Iteration=100)
    label=['NSGA','MOEA/D']
    title='NSGA CPU(S):'+str(cpu_t[0])+'  '+'MOEA/D CPU(s)'+str(cpu_t[1])
    Sched_Result(EP,label,title)
    Iterate_curve(data=C, label=label, xlabel='Iteration', ylabel='makespan', title='Iteration curve')
    Iterate_curve(data=T, label=label, xlabel='Iteration', ylabel='Total tardiness', title='Iteration curve')

#分批策略对比
elif test=='method_compare':
    sf = SF_env('shang_Data.xlsx')
    sf.reset()
    Initial_Pop1 = Pop_ConsSublot(Pop_size=100, Job_Shop=sf, max_SpiltNum=10).Initial()
    # Initial_Pop3 = Pop_ConsSublot_Improved(Pop_size=100, Job_Shop=sf, max_SpiltNum=10).Initial()
    Initial_Pop2 = Pop_NotSpilt(Pop_size=100, Job_Shop=sf).Initial_Random()
    Initial_Pop=[Initial_Pop2,Initial_Pop1]
    Evolution_method=[Evolution_NotSpilt,Evolution_consistent]
    EP, cpu_t,C,T= method_test(NSGA, Initial_Pop,Evolution_method, Pop_size=100, Iteration=100)
    label = ['batching is not considered','batching is considered']
    title = 'batching is considered CPU(S):' + str(cpu_t[0]) + '  ' + 'batching is not considered CPU(s)' + str(cpu_t[1])
    Sched_Result(EP, label, title)
    Iterate_curve(data=C, label=label, xlabel='Iteration', ylabel='makespan', title='Iteration curve')
    Iterate_curve(data=T, label=label, xlabel='Iteration', ylabel='Total tardiness', title='Iteration curve')
    # Result_Output(EP[1])
