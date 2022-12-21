import pickle
import numpy as np

def Instance(name,file_name='10_6_test'):
    file=r'C:\Users\Aihong\PycharmProjects\Long_Live_Guraduation\JSP_AGV\Instance'+'/'+file_name
    f=file+'/'+name+'.pkl'
    with open(f, "rb") as fb:
        Ins= pickle.load(fb)
    n,m,agv_num,PT,MT,TT=Ins['n'],Ins['m'],Ins['agv_num'],Ins['processing_time'],Ins['Processing_machine'],Ins['travle_Matrix']
    return  n,m,agv_num,PT,MT,TT
