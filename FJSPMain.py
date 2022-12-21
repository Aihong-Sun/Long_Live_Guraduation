import numpy as np
from gurobipy import Model, GRB, quicksum
import time
import os

from DataRead import getdata
from FJSPMIPModel import MIPModel

filename=r'C:\Users\Aihong\PycharmProjects\Long_Live_Guraduation\FJSSPinstances/1_Brandimarte/BrandimarteMk5.fjs'
Data=getdata(filename)
print('data_j',Data['J'],Data['OJ'])
print('DATA_operations_machines',Data['operations_machines'])
print('DATA_operations_machines',Data['operations_times'])
model=MIPModel(Data)
nSolution = model.SolCount

# Print number of solution stored
print('number of solution stored:' + str(nSolution))

# Print objective values of solutions
for e in range (nSolution):
    model.setParam(GRB.Param.SolutionNumber, e)
    print ('%g' % model.PoolObjVal, end=' ')
    if (e + 1) % 5 == 0:
        print('')
