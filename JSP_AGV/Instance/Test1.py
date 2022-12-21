'''
start date: 2021/9/14
from thesis:
    Arviv,,Kfir等.Collaborative reinforcement learning for a two-robot job transfer flow-shop scheduling problem[J].
    INTERNATIONAL JOURNAL OF PRODUCTION RESEARCH,2016,54(4):1196-1209.
'''

import random
import numpy as np
import copy

random.seed(64)

Matrix6_6=[[0,0],[0,2],[0,4],[4,0],[4,2],[4,4],[2,2]]
Matrix8_8=[[0,0],[0,2],[0,4],[0,8],[2,3],[4,0],[4,2],[4,4],[4,8]]
Matrix10_10=[[0,2],[0,4],[0,6],[2,0],[2,2],[2,4],[2,6],[2,8],[4,2],[4,4],[4,6]]

def G_travel_matrix(Matrix):
    TT=[]
    for Mi in Matrix:
        TTi=[]
        for Mj in Matrix:
            TTi.append(abs(Mi[0]-Mj[0])+abs(Mi[1]-Mj[1]))
        TT.append(TTi)
    return TT

MM=G_travel_matrix(Matrix6_6)
print(len(MM))
def trans_Matrix(trans,m):
    T=np.zeros((m,m))
    for i in range(len(T)):
        for j in range(len(T[i])):
            if i==j:
                T[i][j]=0
            elif i!=j and T[i][j]==0:
                T[i][j]=sum(trans[i:j])
                T[j][i]=T[i][j]
    return T



def Generate(n,m):
    Mch_speed=[[10,20],[25,45]]
    Ms=Mch_speed[0]
    PT=[]
    MT=[]
    for i in range(n):
        PT_i=[random.randint(Ms[0],Ms[1]) for i in range(m)]
        MT_i=[_ for _ in range(m)]
        random.shuffle(MT_i)
        PT.append(PT_i)
        MT.append(copy.copy(MT_i))
    return PT,MT

file=r'./10_6_test'

import os
import pickle

# files=os.listdir(file)
# print(len(files))

Ni=[10,10,10,10,10,10,10,10,10,10]
AGV_num=[2,2,2,2,2,2,2,2,2,2]
k=0
for i in range(len(Ni)):
    PT,MT=Generate(Ni[i],6)
    file1 = file + '/' + 'n' + str(Ni[i]) + '_m6' + '_agv' + str(AGV_num[i])+str(k)+'.pkl'
    Ins={'n':Ni[i],'m':6,'agv_num':AGV_num[i],'processing_time':PT,'Processing_machine':MT,'travle_Matrix':MM}
    with open(file1, "wb") as f:
        pickle.dump(Ins, f, pickle.HIGHEST_PROTOCOL)
    k+=1









