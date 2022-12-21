
from FJSP.Shop_Floor.Job_Shop import Job_shop
from  FJSP.Algo.AOA.object import Fitness, Limit
import copy
import pickle
from FJSP.Shop_Floor.utils import *

def Equal_parts(lb,ub,n):
    unit=round((ub-lb)/n,3)
    list=[]
    k=lb+unit
    for i in range(n):
        list.append(round(k,3))
        k+=unit
    return list

def decode(OS,MS,JS,J_site):
    for i in OS:  # 依次读取工序编码进行解码
        O_n = JS.Jobs[i].cur_op  # 获取当前解码工件已解码工序
        m_idx = J_site.index((i, O_n))  # 获取对应工序的机器索引
        JS.decode(i, MS[m_idx])  # 解码
    return JS

#转换机制
def Change_Code(X,M_option,OS):
    # 获得工序编码序列
    O_len = len(OS)
    OS_value = X[:O_len]
    OS_dict = zip(OS, OS_value)
    OS_new = sorted(OS_dict, key=lambda x: x[1])
    OS_True = [_[0] for _ in OS_new]
    # 获得机器编码序列
    MS_value = X[O_len:]
    # print('----')
    # print(MS_value)
    MS_True = []
    for i in range(len(MS_value)):
        Ep = Equal_parts(-10, 10, M_option[i])
        Mi = None
        for pi in range(len(Ep)):
            if MS_value[i] < Ep[pi]:
                Mi = pi
                break
        if Mi == None:
            Mi = M_option[i] - 1
        MS_True.append(Mi)
    return OS_True,MS_True

def mainFunction(X,JS,J_site,M_option,OS,SJS=None):
    OS_True, MS_True=Change_Code(X,M_option,OS)
    JS=decode(OS_True, MS_True,JS,J_site)
    return Get_Score(JS,SJS)

def Get_Score(JS,SJS):
    if SJS:     #双目标
        num_Dp=JS.Scheme_Comparison(SJS)
        return JS.C_max,num_Dp
    elif JS.Energy_Consumption!=None and SJS!=None:     #三目标
        num_Dp = JS.Scheme_Comparison(SJS)
        T_ec=JS.Total_Energy_Comsumption()
        return JS.C_max, num_Dp,T_ec
    elif  JS.Energy_Consumption!=None and SJS==None:
        T_ec = JS.Total_Energy_Comsumption()
        return JS.C_max,  T_ec
    else:   #单目标
        return JS.C_max

def Get_JS(X,JS,J_site,M_option,OS):
    OS_True, MS_True = Change_Code(X, M_option, OS)
    JS = decode(OS_True, MS_True, JS, J_site)
    return JS




def Static_FJSP_Info(n, m, PT, MT, ni,numofObj,lowerBound,upperBound,maximumIteration,C1,C2,C3,C4,EC=None,ESPC=None):
    '''
    :param file: 算例文件名
    :param numofObj: 种群规模
    :param lowerBound: 上界
    :param upperBound: 下界
    :param maximumIteration: 最大迭代次数
    :param C1:
    :param C2:
    :param C3:
    :param C4:
    :return:
    '''

    JS = Job_shop(n, m, ni, MT, PT,EC,ESPC)
    JS.reset()
    os_list = []  # 工序序列
    ms_list,J_site = [], []  # 机器序列和工序对应的位置
    for i in range(JS.n):
        os_list.extend([i for _ in range(JS.Jobs[i].O_num)][JS.Jobs[i].cur_op:])
        ms_list.extend([len(pi) for pi in JS.Jobs[i].processing_machine][JS.Jobs[i].cur_op:])
        J_site.extend([(i, j) for j in range(JS.Jobs[i].O_num)][JS.Jobs[i].cur_op:])
    limitFunction = None
    limitInputs = []
    dimention = int(2*len(os_list))
    if EC:
        fitness = Fitness.Multi_obj
    else:
        fitness = Fitness.Single_obj
    for count in range(dimention):
        limitInputs.append(Limit(lowerBound,upperBound))
    return numofObj, limitInputs[0].lowerBound,limitInputs[0].upperBound,\
           maximumIteration, C1, C2, C3, C4, mainFunction, dimention,\
           limitInputs,limitFunction,fitness, JS, J_site, ms_list, os_list


def Dynamic_FJSP_Info(file,resched_t,MT,PT, numofObj, lowerBound, upperBound, maximumIteration, C1, C2, C3, C4,EC=None,ESPC=None):
    '''

    :param JS: 原调度方案
    :param resched_t: 重调度时刻
    :param PM: 重调度工件的机器信息
    :param PT: 重调度工件的加工时间信息
    :param numofObj: 种群规模
    :param lowerBound:
    :param upperBound:
    :param maximumIteration:
    :param C1:
    :param C2:
    :param C3:
    :param C4:
    :return:
    '''
    with open(file, "rb") as fb:
        I = pickle.load(fb)
    JS = I['job_shop_env']
    Gantt(JS.Machines)
    SJS = copy.deepcopy(JS)
    SJS.resched(resched_t, MT, PT,EC)
    os_list = []  # 工序序列
    ms_list, J_site = [], []  # 机器序列和工序对应的位置
    for i in range(  SJS.n):
        os_list.extend([i for _ in range(  SJS.Jobs[i].O_num)][  SJS.Jobs[i].cur_op:])
        ms_list.extend([len(pi) for pi in   SJS.Jobs[i].processing_machine][  SJS.Jobs[i].cur_op:])
        J_site.extend([(i, j) for j in range(  SJS.Jobs[i].O_num)][  SJS.Jobs[i].cur_op:])
    limitFunction = None
    limitInputs = []
    dimention = int(2 * len(os_list))
    fitness = Fitness.Multi_obj
    for count in range(dimention):
        limitInputs.append(Limit(lowerBound, upperBound))
    return numofObj, limitInputs[0].lowerBound,limitInputs[0].upperBound,\
           maximumIteration, C1, C2, C3, C4, mainFunction, dimention,\
           limitInputs,limitFunction,fitness, SJS, J_site, ms_list, os_list,JS

