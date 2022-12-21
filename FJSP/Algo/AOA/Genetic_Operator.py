import math
import random
import numpy as np
from FJSP.Algo.AOA.FJSP_problem import *
import copy

# POX:precedence preserving order-based crossover
def POX(p1, p2,n):
    jobsRange = range(0, n)
    sizeJobset1 = random.randint(1, n)
    jobset1 = random.sample(jobsRange, sizeJobset1)
    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
        else:
            o1.append(-1)
            p1kept.append(e)
    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset1:
            o2.append(e)
        else:
            o2.append(-1)
            p2kept.append(e)
    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)
    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)
    return o1, o2

def Job_Crossover(p1 ,p2,n):
    jobsRange = range(0, n)
    sizeJobset1 = random.randint(0, n)
    jobset1 = random.sample(jobsRange, sizeJobset1)
    jobset2 = [item for item in jobsRange if item not in jobset1]
    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
            p1kept.append(e)
        else:
            o1.append(-1)
    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset2:
            o2.append(e)
            p2kept.append(e)
        else:
            o2.append(-1)
    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)
    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)
    return o1 ,o2

def swap_mutation(p):
    pos1 = random.randint(0, len(p) - 1)
    pos2 = random.randint(0, len(p) - 1)
    if pos1 == pos2:
        return p
    if pos1 > pos2:
        pos1, pos2 = pos2, pos1
    offspring = p[:pos1] + [p[pos2]] + \
                p[pos1 + 1:pos2] + [p[pos1]] + \
                p[pos2 + 1:]
    return offspring

def MB_mutation(p1):
    D = len(p1)
    c1 = p1.copy()
    r = np.random.uniform(size=D)
    for idx1, val in enumerate(p1):
        if r[idx1] <= 0.05:
            idx2 = np.random.choice(np.delete(np.arange(D), idx1))
            c1[idx1], c1[idx2] = c1[idx2], c1[idx1]
    return c1

def Mac_mutation(p1,min_pt):
    site=[_ for _ in range(len(p1))]
    for i in range(3):
        s=random.choice(site)
        del site[site.index(s)]
        p1[s]=min_pt[s]
    return p1

#[1]张超勇. 基于自然启发式算法的作业车间调度问题理论与应用研究[D].华中科技大学,2007.
def OS_mutation(OS,MS,JS,J_site,SJS=None):
    new_OS=None
    best_score=None
    chs1=OS
    chs2=MS
    os_list=[_ for _ in range(len(chs1))]
    for i in range(5):
        random.shuffle(os_list)
        r=random.randint(1,len(os_list)-1)
        os_set=os_list[0:r]
        os_had=[]
        os_site=[]
        for i in os_set:
            if chs1[i] not in os_had:
                os_had.append(chs1[i])
                os_site.append(i)
        old_os_site=copy.deepcopy(os_site)
        random.shuffle(os_site)
        c1=copy.deepcopy(chs1)
        for j in range(len(old_os_site)):
            c1[os_site[j]]=chs1[old_os_site[j]]
        js=decode(c1, chs2, copy.deepcopy(JS), J_site)
        score=Get_Score(js,SJS)
        if new_OS!=None:
            if Dominate(score,best_score):
                new_OS=c1
                best_score=score
        else:
            new_OS=c1
            best_score=score
    return new_OS,chs2

#单点交叉：Single-point crossover
def SPC(p1,p2):
    site=random.randint(1,len(p1)-1)
    c1,c2=p1[:site],p2[:site]
    p1[:site]=c2
    p2[:site]=c1
    return p1,p2

#双点交叉：Two-point crossover
def TPC(p1,p2):
    site = [_ + 1 for _ in range(len(p1) - 2)]
    site = random.sample(site, 2)
    c1, c2 = p1[site[0]:site[1]], p2[site[0]:site[1]]
    p1[site[0]:site[1]] = c2
    p2[site[0]:site[1]] = c1
    return p1,p2

#均匀交叉(Unifrom crossover)
def UC(p1,p2):
    for i in range(len(p1)):
        if random.random()<0.5:
            p1[i],p2[i]=p2[i],p1[i]
    return p1,p2

#进化操作
def cross_operator(OS1,OS2,MS1,MS2,JS,J_site,SJS=None):
    chs11,chs12=OS1,MS1
    chs21,chs22=OS2,MS2
    #对编码段chs2进行交叉
    cross_method=[TPC]
    CM1,CM2=random.choice(cross_method),random.choice(cross_method)
    chs121, chs221 = CM2(chs12, chs22)  #对机器选择层进行交叉
    cross_method = [POX]
    CM = random.choice(cross_method)
    chs111,chs211=CM(chs11,chs21,JS.n)      #对工序选择层进行交叉
    js1 = decode(chs111,chs121, copy.deepcopy(JS), J_site)
    score1 = Get_Score(js1, SJS)
    js2 = decode(chs211, chs221, copy.deepcopy(JS), J_site)
    score2 = Get_Score(js2, SJS)
    if Dominate(score1,score2):
        return chs111,chs121
    else:
        return chs211, chs221



