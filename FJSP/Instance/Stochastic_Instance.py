import random
import pickle
import os



def Generate_Instance(n,m):
    PT=[]
    MT=[]
    ni=[]
    for i in range(n):
        PTi=[]
        MTi=[]
        Oi=random.randint(2,6)
        ni.append(Oi)
        for j in range(Oi):
            m_num=random.randint(1,m-1) #可加工机器数
            PTii=[random.randint(5,15) for i in range(m_num)]
            MTii=[random.randint(1,m) for i in range(m_num)]
            PTi.append(PTii)
            MTi.append(MTii)
        PT.append(PTi)
        MT.append(MTi)
    return n, m, PT, MT, ni

n, m, PT, MT, ni =Generate_Instance(20,8)

result_path = r'C:\Users\Administrator\PycharmProjects\Long_live_graduation\FJSP\Instance\Stochastic_Ins'
dic = {'n': n, 'm': m,'processing_time':PT,'Processing machine':MT,'Jobs_Onum':ni}
with open(os.path.join(result_path, str(n)+'_'+str(m) + ".pkl"), "wb") as f:
    pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)



