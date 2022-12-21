import copy

from FJSP.Algo.AOA.object import Object, Fitness
from FJSP.Algo.AOA.FJSP_problem import *
from numpy import random
import math
from FJSP.Algo.AOA.Genetic_Operator import *
from FJSP.Algo.utils import *

def AOA(numOfObj,lowerBound,upperBound,maximumIteration,C1,C2,C3,C4, mainFunction,dim,positionLimit,limitFunction,fitness,Job_shop,J_site,M_option,OS,SJS=None,Grate=0.5,Lrate=0.4):
    best_val=[]
    # 1 : initialieze objects population using (4),(5), and (6)
    population = generatePopulation(numOfObj,lowerBound,upperBound,mainFunction,dim,positionLimit,limitFunction,copy.deepcopy(Job_shop),J_site,M_option,OS,copy.deepcopy(SJS),Grate=0.5,Lrate=0.4)
    
    # 1.2 get object with miminum scores atributes and set it as bestObject
    bestObject = ''
    if fitness == Fitness.Multi_obj :
        bestObj = getBestObjectByMinScore_Multi_obj(population)
    else :
        bestObj = getBestObjectByMinScore(population)
    Best_Op=bestObj
    # 1.3 update every object in maximumIteration times
    iteration = 1
    while iteration <= maximumIteration:
        population1=copy.deepcopy(population)
        for obj in population1:
            if isinstance(bestObj,list):
                bestObject = random.choice(bestObj)

            else:
                bestObject=bestObj
            # 2 : update density and volume using (7)
            obj.density = obj.density + random.random() * (bestObject.density - obj.density)
            obj.volume = obj.volume + random.random() * (bestObject.volume - obj.volume)

            # 3 : Transfer operator and density factor using (8) and (9)
            TF = math.exp((iteration - maximumIteration)/maximumIteration)
            denDecFactor = math.exp((maximumIteration-iteration)/maximumIteration) - (iteration/maximumIteration)

            randomObject = population1[int(random.random()*len(population1))]
            minAcceleration, maxAcceleration = getMinMaxAcceleration(population1)
            if TF <= 0.45:
                # 4.1 : Exploration phase (collision occure) using (10)
                obj.acceleration = (randomObject.density + randomObject.volume * randomObject.acceleration)/(obj.density * obj.volume)

                #  4.3 : Normalize acceleration using (12)  ### TODO: not test yet
                # u and l are range of normalization and set to 0.9 and 0.1 respectively
                u = 0.9
                l = 0.1
                accNorm = u * (obj.acceleration - minAcceleration) / (maxAcceleration - minAcceleration) +l

                # 5 : update position using (13) # TODO : not test yet
                if dim > 0 :
                    for count in range(dim):
                        obj.position[count]= obj.position[count] + C1 * random.random() * accNorm * denDecFactor * abs(randomObject.position[count] - obj.position[count])
                else:
                    obj.position = obj.position + C1 * random.random() * accNorm * denDecFactor * (randomObject.position - obj.position)

            else :
            # Exploitation Phase # TODO: not test yet
            # 4.2 : Exploitation Phase ( no collision between objects) using (11)
                obj.acceleration = (bestObject.density + bestObject.volume * bestObject.acceleration)/(obj.density + obj.volume)

                #  4.3 : Normalize acceleration using (12)  ### TODO: not test yet
                # u and l are range of normalization and set to 0.9 and 0.1 respectively
                u = 0.9
                l = 0.1
                accNorm = u * (obj.acceleration - minAcceleration) / (maxAcceleration - minAcceleration) +l

                # 5 : Update ddiraction flag F using(15) # TODO : not test yet
                T = C3 * TF
                P = 2 * random.random() - C4
                F = 1 if P <= 0.5  else -1
                # 5 : Update position using (14)
                if dim >0 :
                    for count in range(dim):
                        bestPosition = bestObject.position[count]
                        objPosition = obj.position[count]
                        obj.position[count] = bestPosition + F * C2 * random.random() * accNorm * denDecFactor * (T * bestPosition - objPosition)
                else :
                    obj.position = bestObject.position + F * C2 * random.random() * accNorm * denDecFactor * (T * bestObject.position - obj.position)

            # end of if

            # update object score
            # obj.setScore(mainFunction(obj.position)) # it can be run , but not give an impact for all

        # end of for

        # check position and make sure position in range 
        # and update score of each object
        # printAllPopulation(population,"before Check Position")
        population1 = checkPosition(dim,population1,lowerBound,upperBound,mainFunction,positionLimit,copy.deepcopy(Job_shop),J_site,M_option,OS,copy.deepcopy(SJS))
        population= population1
        # Evaluate each object and select the one with the best fitness value
        if fitness == Fitness.Multi_obj :
            bestObj = getBestObjectByMinScore_Multi_obj(population)
        else :
            bestObj = getBestObjectByMinScore(population)
        if isinstance(bestObj, list):
            Best_Op.extend(bestObj)
            NDSet=fast_non_dominated_sort(Best_Op)
            Best_Op=NDSet[0]
        else:
            if bestObject.fitness <Best_Op.fitness:
                Best_Op=bestObject
        iteration  = iteration + 1
        best_val.append(bestObject.fitness)
    #  return object with the best fitness value
    return Best_Op, population,best_val


def IAOA(numOfObj, lowerBound, upperBound, maximumIteration, C1, C2, C3, C4, mainFunction, dim, positionLimit,
        limitFunction, fitness, Job_shop, J_site, M_option, OS, SJS=None, Grate=0.5, Lrate=0.4):
    best_val = []
    # 1 : initialieze objects population using (4),(5), and (6)
    population = generatePopulation(numOfObj, lowerBound, upperBound, mainFunction, dim, positionLimit, limitFunction,
                                    copy.deepcopy(Job_shop), J_site, M_option, OS, copy.deepcopy(SJS), Grate=0.5,
                                    Lrate=0.4)

    # 1.2 get object with miminum scores atributes and set it as bestObject
    bestObject = ''
    if fitness == Fitness.Multi_obj:
        bestObj = getBestObjectByMinScore_Multi_obj(population)
    else:
        bestObj = getBestObjectByMinScore(population)
    Best_Op = bestObj
    # 1.3 update every object in maximumIteration times
    iteration = 1
    while iteration <= maximumIteration:
        population1 = copy.deepcopy(population)
        for obj in population1:
            if isinstance(bestObj, list):
                bestObject = random.choice(bestObj)

            else:
                bestObject = bestObj
            # 2 : update density and volume using (7)
            obj.density = obj.density + random.random() * (bestObject.density - obj.density)
            obj.volume = obj.volume + random.random() * (bestObject.volume - obj.volume)

            # 3 : Transfer operator and density factor using (8) and (9)
            TF = math.exp((iteration - maximumIteration) / maximumIteration)
            denDecFactor = math.exp((maximumIteration - iteration) / maximumIteration) - (iteration / maximumIteration)

            randomObject = population1[int(random.random() * len(population1))]
            minAcceleration, maxAcceleration = getMinMaxAcceleration(population1)
            if TF <= 0.45:
                # 4.1 : Exploration phase (collision occure) using (10)
                obj.acceleration = (randomObject.density + randomObject.volume * randomObject.acceleration) / (
                            obj.density * obj.volume)

                #  4.3 : Normalize acceleration using (12)  ### TODO: not test yet
                # u and l are range of normalization and set to 0.9 and 0.1 respectively
                u = 0.9
                l = 0.1
                accNorm = u * (obj.acceleration - minAcceleration) / (maxAcceleration - minAcceleration) + l

                # 5 : update position using (13) # TODO : not test yet
                if dim > 0:
                    for count in range(dim):
                        import time
                        t1=time.time()
                        obj.position=Genetic_Operator(obj.position, randomObject.position, lowerBound, upperBound, Job_shop, J_site, M_option, OS, SJS=None)
                        t2=time.time()
                        # obj.position[count] = obj.position[count] + C1 * random.random() * accNorm * denDecFactor * abs(
                        #     randomObject.position[count] - obj.position[count])
                else:
                    obj.position = obj.position + C1 * random.random() * accNorm * denDecFactor * (
                                randomObject.position - obj.position)

            else:
                # Exploitation Phase # TODO: not test yet
                # 4.2 : Exploitation Phase ( no collision between objects) using (11)
                obj.acceleration = (bestObject.density + bestObject.volume * bestObject.acceleration) / (
                            obj.density + obj.volume)

                #  4.3 : Normalize acceleration using (12)  ### TODO: not test yet
                # u and l are range of normalization and set to 0.9 and 0.1 respectively
                u = 0.9
                l = 0.1
                accNorm = u * (obj.acceleration - minAcceleration) / (maxAcceleration - minAcceleration) + l

                # 5 : Update ddiraction flag F using(15) # TODO : not test yet
                T = C3 * TF
                P = 2 * random.random() - C4
                F = 1 if P <= 0.5 else -1
                # 5 : Update position using (14)
                if dim > 0:
                    for count in range(dim):
                        bestPosition = bestObject.position[count]
                        objPosition = obj.position[count]
                        obj.position[count] = bestPosition + F * C2 * random.random() * accNorm * denDecFactor * (
                                    T * bestPosition - objPosition)
                else:
                    obj.position = bestObject.position + F * C2 * random.random() * accNorm * denDecFactor * (
                                T * bestObject.position - obj.position)

            # end of if

            # update object score
            # obj.setScore(mainFunction(obj.position)) # it can be run , but not give an impact for all

        # end of for

        # check position and make sure position in range
        # and update score of each object
        # printAllPopulation(population,"before Check Position")
        population1 = checkPosition(dim, population1, lowerBound, upperBound, mainFunction, positionLimit,
                                    copy.deepcopy(Job_shop), J_site, M_option, OS, copy.deepcopy(SJS))
        population = population1
        # Evaluate each object and select the one with the best fitness value
        if fitness == Fitness.Multi_obj:
            bestObj = getBestObjectByMinScore_Multi_obj(population)
        else:
            bestObj = getBestObjectByMinScore(population)
        if isinstance(bestObj, list):
            Best_Op.extend(bestObj)
            NDSet = fast_non_dominated_sort(Best_Op)
            Best_Op = NDSet[0]
        else:
            if bestObject.fitness < Best_Op.fitness:
                Best_Op = bestObject
        iteration = iteration + 1
        best_val.append(bestObject.fitness)
    #  return object with the best fitness value
    return Best_Op, population, best_val

def Position_Get(X,Y,lb,ub,M_option):
    unit = round((ub - lb) /len(X), 3)
    k = lb
    va=[]
    for i in range(len(X)):
        vai = round(random.uniform(k, k + unit), 3)
        va.append(vai)
        k += unit
    os_va=zip(X,va)
    OS_new = sorted(os_va, key=lambda x: x[0])
    OS_True = [_[1] for _ in OS_new]
    for i in range(len(Y)):
        l=Machine_parts(lb,ub,M_option[i],Y[i])
        OS_True.append(l)
    return OS_True

def Genetic_Operator(X1,X2,lowerBound, upperBound, Job_shop, J_site, M_option, OS, SJS=None):
    OS1,MS1=Change_Code(X1,M_option,OS)
    OS2, MS2 = Change_Code(X2, M_option, OS)
    JS=copy.deepcopy(Job_shop)
    OS3,MS3=cross_operator(OS1, OS2, MS1, MS2,  JS, J_site, SJS)
    if random.random()<0.05:
        JS = copy.deepcopy(Job_shop)
        OS3,MS3=OS_mutation(OS3, MS3, JS, J_site, SJS)
    position=Position_Get(OS3,MS3,lowerBound, upperBound,M_option)
    return position
# end of procedure AOA

def Machine_parts(lb,ub,n,idx):
    unit=round((ub-lb)/n,3)
    k=lb
    for i in range(n):
        if i==idx:
            L=round(random.uniform(k,k+unit),3)
            break
        k+=unit
    return L


#全局生成初始种群
def GS_Position(lowerBound,upperBound,dim,positionLimit,Job_shop,J_site,M_option,OS,):
    objPosition = []
    for count in range(int(dim / 2)):
        objPosition.append(positionLimit[count].lowerBound + random.random() * (
                    positionLimit[count].upperBound - positionLimit[count].lowerBound))
    OS_dict = zip(OS, objPosition)
    OS_new = sorted(OS_dict, key=lambda x: x[1])
    OS_True = [_[0] for _ in OS_new]
    m_load = [0 for _ in range(Job_shop.m)]
    chs2 = [0 for _ in range(len(M_option))]
    op = [_.cur_op for _ in Job_shop.Jobs]
    MS_True=[0 for _ in range(len(M_option))]
    for ci in OS_True:
        m_l = []
        for i in range(len(Job_shop.Jobs[ci].processing_machine[op[ci]])):
            k = Job_shop.Jobs[ci].processing_machine[op[ci]][i]
            load = m_load[k - 1]
            pt = Job_shop.Jobs[ci].processing_time[op[ci]][i]
            m_l.append(load + pt)
        min_ml = min(m_l)
        m_idx = m_l.index(min_ml)
        o_idx = J_site.index((ci, op[ci]))
        value=Machine_parts(lowerBound,upperBound,M_option[o_idx],m_idx)
        chs2[o_idx] =  value
        MS_True[o_idx]=m_idx
        m_load[Job_shop.Jobs[ci].processing_machine[op[ci]][m_idx] - 1] = min_ml
        op[ci] += 1
    # print(MS_True)
    # print(chs2)
    objPosition.extend(chs2)
    return objPosition

#局部初始化种群
def LS_Position(lowerBound,upperBound,dim,positionLimit,Job_shop,J_site,M_option,OS):
    ms_minpt = []
    for i in range(Job_shop.n):
        ms_minpt.extend([pi.index(min(pi)) for pi in Job_shop.Jobs[i].processing_time][Job_shop.Jobs[i].cur_op:])
    objPosition = []
    for count in range(int(dim / 2)):
        objPosition.append(positionLimit[count].lowerBound + random.random() * (
                positionLimit[count].upperBound - positionLimit[count].lowerBound))
    for m_idx in range(len(ms_minpt)):
        value = Machine_parts(lowerBound, upperBound, M_option[m_idx], ms_minpt[m_idx])
        objPosition.append(value)
    return objPosition

#随机初始化种群
def RS_Position(lowerBound,upperBound,dim,positionLimit,Job_shop,J_site,M_option,OS):
    objPosition = []
    for count in range(dim):
        objPosition.append(positionLimit[count].lowerBound + random.random() * (
                    positionLimit[count].upperBound - positionLimit[count].lowerBound))
    return objPosition


def generatePopulation(numOfObj,lowerBound,upperBound,mainFunction,dim,positionLimit,limitFunction,Job_shop,J_site,M_option,OS,SJS=None,Grate=0.5,Lrate=0.4):
    population = []
    for i in range(numOfObj):
        if i<int(Grate*numOfObj):
            objPosition=GS_Position(lowerBound,upperBound,dim,positionLimit,copy.deepcopy(Job_shop),J_site,M_option,OS,)
        elif i<int((Grate+Lrate)*numOfObj):
            objPosition=LS_Position(lowerBound, upperBound, dim, positionLimit, copy.deepcopy(Job_shop), J_site, M_option, OS)
        else:
            objPosition = RS_Position(lowerBound, upperBound, dim, positionLimit, copy.deepcopy(Job_shop), J_site, M_option, OS)
        # TODO : What if position is not an array
        objAcceleration = lowerBound + random.random() * (upperBound - lowerBound)
        anObject = Object(copy.deepcopy(objPosition), copy.deepcopy(objAcceleration))
        score=mainFunction(anObject.position,copy.deepcopy(Job_shop),J_site,M_option,OS,copy.deepcopy(SJS))
        anObject.setScore(copy.deepcopy(score))
        population.append(copy.deepcopy(anObject))
    return population

def getBestObjectByMaxScore(population): 
    minPosition = minAcceleration = minVolume = -math.inf
    minDensity = minScore = -math.inf
    
    for anObject in population:
        if anObject.fitness > minScore:
            minPosition = anObject.position
            minAcceleration = anObject.acceleration
            minVolume = anObject.volume
            minDensity = anObject.density
            minScore = anObject.fitness
        
    bestOne = Object(minPosition,minAcceleration)
    bestOne.setDensity(minDensity)
    bestOne.setVolume(minVolume)
    bestOne.setScore(minScore)
    return bestOne

def getBestObjectByMinScore(population,):
    minScore = math.inf
    bestOne=population[0]
    for anObject in population:
        if anObject.fitness < minScore:
            bestOne=copy.copy(anObject)
            minScore=bestOne.fitness
    return bestOne


def getBestObjectByMinScore_Multi_obj(population):
    NDSet=fast_non_dominated_sort(population)
    return NDSet[0]

def getMinMaxAcceleration(population):
    minAcceleration = 9999
    maxAcceleration = -9999

    for obj in population:
        minAcceleration = obj.acceleration if obj.acceleration < minAcceleration else minAcceleration
        maxAcceleration = obj.acceleration if obj.acceleration > maxAcceleration else maxAcceleration

    # TODO : bagaimana cara menghindari pembagian dengan nol
    while minAcceleration == maxAcceleration :
        tempAcc = random.random()
        if tempAcc > minAcceleration:
            maxAcceleration = tempAcc
        else :
            minAcceleration = tempAcc

    return minAcceleration, maxAcceleration

def checkPosition(dim,population,lowerBound,upperBound,mainFunction,positionLimit,Job_shop,J_site,M_option,OS,SJS=None):
    updatePopulation = []
    for obj in population :
        for count in range(dim):
            obj.position[count] = positionLimit[count].lowerBound if obj.position[count] < positionLimit[count].lowerBound else obj.position[count]
            obj.position[count] = positionLimit[count].upperBound if obj.position[count] > positionLimit[count].upperBound else obj.position[count]
        
        # TODO : make condition for obj that only has one position alias position is not array   
        obj.setScore(mainFunction(obj.position,copy.deepcopy(Job_shop),J_site,M_option,OS,copy.deepcopy(SJS)))
        updatePopulation.append(obj)

    return updatePopulation

def printAllPopulation(population,message):
    print(message)
    count = 1
    for obj in population:
        print (f"objek ke-{count} : {obj.position}")
    print("\n")