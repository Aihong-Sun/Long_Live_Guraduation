
import random
import numpy as np
import copy
from Batch_Schedule.Algo.Individual import Popi

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

#针对批次分割矩阵的交叉
def Batch_Crossover(p1,p2):
    lis=[_ for _ in range(len(p1))]
    r=random.randint(1,int(len(p1)/2)-1)
    lis1=random.sample(lis,r)
    for i in range(len(lis1)):
        p1[lis1[i]],p2[lis1[i]]=p2[lis1[i]],p1[lis1[i]]
    return p1,p2

#针对批次分割矩阵的变异操作
def Batch_Mutation(p1):
    p=[]
    for Lis in p1:
        for j in range(int(len(Lis) / 2)):
            r = random.randint(0, Lis[j])
            Lis[j] -= r
            Lis[int(len(Lis) / 2) + j] += r
        p.append(Lis)
    return p

#不考虑分批的进化操作
def Evolution_NotSpilt(p1,p2):
    chs11,chs12,chs13=p1.chs2,p1.chs3,p1.chs4
    chs21, chs22, chs23 = p2.chs2, p2.chs3, p2.chs4
    #对编码段chs2进行交叉
    cross_method=[SPC,TPC,UC]
    CM1,CM2=random.choice(cross_method),random.choice(cross_method)
    chs111,chs211=CM1(chs11,chs21)      #对工艺选择层进行交叉
    chs131, chs231 = CM2(chs13, chs23)  #对机器选择层进行交叉
    cross_method = [POX,Job_Crossover]
    CM = random.choice(cross_method)
    chs121,chs221=CM(chs12,chs22,p1.n)      #对工序选择层进行交叉

    #变异
    chs111,chs211=swap_mutation(chs111),swap_mutation(chs211)
    chs121, chs221 = swap_mutation(chs121), swap_mutation(chs221)

    new_pop1=Popi(copy.deepcopy(p1.JS),chs2=chs111,chs3=chs121,chs4=chs131,Op_site=p1.Op_site)
    new_pop2=Popi(copy.deepcopy(p1.JS), chs2=chs211, chs3=chs221, chs4=chs231, Op_site=p1.Op_site)
    return new_pop1,new_pop2

#考虑分批的进化操作
def Evolution_consistent(p1,p2):
    chs11, chs12, chs13 = p1.chs1, p1.chs2, p1.chs3
    chs21, chs22, chs23 = p2.chs1, p2.chs2, p2.chs3
    # 对编码段chs2进行交叉
    cross_method = [SPC, TPC, UC]
    CM1, CM2 = random.choice(cross_method), random.choice(cross_method)
    chs121, chs221 = CM1(chs12, chs22)  # 对工艺选择层进行交叉
    chs111, chs211 = Batch_Crossover(chs11, chs21)  # 对批次分割层进行交叉
    cross_method = [POX, Job_Crossover]
    CM = random.choice(cross_method)
    chs131, chs231 = CM(chs13, chs23, p1.n)  # 对工序选择层进行交叉

    # 变异
    chs111, chs211 = Batch_Mutation(chs111), Batch_Mutation(chs211)
    chs121, chs221 = swap_mutation(chs121), swap_mutation(chs221)
    chs131,chs231 = swap_mutation(chs131), swap_mutation(chs231)

    new_pop1 = Popi(copy.deepcopy(p1.JS), chs1=chs111, chs2=chs121, chs3=chs131)
    new_pop2 = Popi(copy.deepcopy(p1.JS), chs1=chs211, chs2=chs221, chs3=chs231)
    return new_pop1, new_pop2

#考虑改进分批的进化操作
def Evolution_consistent_Improved(p1,p2):
    chs11, chs12, chs13 = p1.chs1, p1.chs2, p1.chs3
    chs21, chs22, chs23 = p2.chs1, p2.chs2, p2.chs3
    chs12_new,chs22_new=[],[]
    c_len=len(chs12[0])
    for ci in range(len(chs12)):
        chs12_new.extend(chs12[ci])
        chs22_new.extend(chs22[ci])
    chs12,chs22=chs12_new,chs22_new

    # 对编码段chs2进行交叉
    cross_method = [SPC, TPC, UC]
    CM1, CM2 = random.choice(cross_method), random.choice(cross_method)
    chs121, chs221 = CM1(chs12, chs22)  # 对工艺选择层进行交叉
    chs111, chs211 = Batch_Crossover(chs11, chs21)  # 对批次分割层进行交叉
    cross_method = [POX, Job_Crossover]
    CM = random.choice(cross_method)
    chs131, chs231 = CM(chs13, chs23, p1.n)  # 对工序选择层进行交叉

    # 变异
    chs111, chs211 = Batch_Mutation(chs111), Batch_Mutation(chs211)
    chs121, chs221 = swap_mutation(chs121), swap_mutation(chs221)
    chs131,chs231 = swap_mutation(chs131), swap_mutation(chs231)

    chs121_new,chs221_new=[],[]
    k1,k2=0,c_len
    for i in range(int(len(chs121)/c_len)):
        chs121_new.append(chs121[k1:k2])
        chs221_new.append(chs221[k1:k2])
        k1+=c_len
        k2+=c_len
    chs121,chs221= chs121_new,chs221_new
    new_pop1 = Popi(copy.deepcopy(p1.JS), chs1=chs111, chs2=chs121, chs3=chs131)
    new_pop2 = Popi(copy.deepcopy(p1.JS), chs1=chs211, chs2=chs221, chs3=chs231)
    return new_pop1, new_pop2
