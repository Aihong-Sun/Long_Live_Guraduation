import os

import seaborn as sns; sns.set()


PR_False_DNN_DQN=[r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prFalse\CNN_DNN\ddqnFalse\5_0.0001_200_500000_0.9',]

PR_False_DNN_DDQN=[r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prFalse\CNN_DNN\ddqnTrue\5_0.0001_100_100000_0.9',
                   r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prFalse\CNN_DNN\ddqnTrue\5_0.0001_100_500000_0.9']

PR_False_Duelling_DQN=[r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prFalse\CNN_duelling\ddqnFalse\5_0.0001_200_100000_0.9']
PR_False_Duelling_DDQN=[r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prFalse\CNN_duelling\ddqnTrue\5_0.0001_150_500000_0.9']

PR_True_DNN_DQN=[r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prTrue\CNN_DNN\ddqnFalse\5_0.0001_200_500000_0.9',
                 r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prTrue\CNN_DNN\ddqnFalse\5_0.0001_150_100000_0.9']

PR_True_DNN_DDQN=[r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prTrue\CNN_DNN\ddqnTrue\5_0.0001_100_100000_0.9',
                  r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prTrue\CNN_DNN\ddqnTrue\5_0.0001_100_500000_0.9']

PR_True_Duelling_DQN=[r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prTrue\CNN_duelling\ddqnFalse\5_0.0001_100_500000_0.9']
PR_True_Duelling_DDQN=[r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\Draw_Result1\prTrue\CNN_duelling\ddqnTrue\5_0.0001_200_500000_0.9']


F000=PR_False_DNN_DQN[0]+'\Reward.pkl'
F001=PR_False_DNN_DDQN[0]+'\Reward.pkl'
F010=PR_False_Duelling_DQN[0]+'\Reward.pkl'
F011=PR_False_Duelling_DDQN[0]+'\Reward.pkl'
F100=PR_True_DNN_DQN[0]+'\Reward.pkl'
F101=PR_True_DNN_DDQN[1]+'\Reward.pkl'
F110=PR_True_Duelling_DQN[0]+'\Reward.pkl'
F111=PR_True_Duelling_DDQN[0]+'\Reward.pkl'


from tsmoothie.smoother import LowessSmoother


def draw_f(F,i,title):
    with open(F, "rb") as fb:
        K = pickle.load(fb)
        d=np.array(K)
        data=[]
        for di in d:
            data.append(sum(di)/len(di))
        x=[_ for _ in range(len(data))]
        smoother = LowessSmoother(smooth_fraction=0.03, iterations=2)
        smoother1 = LowessSmoother(smooth_fraction=0.03, iterations=2)
        smoother.smooth(data)
        low, up = smoother.get_intervals('prediction_interval')
        smoother1.smooth(data)
        # plt.plot(x,smoother.data[0], '.',linewidth=0.1)
        plt.plot(x,smoother1.smooth_data[0], linewidth=2,label=title)
        plt.xlabel('Training step(*10)',fontdict={'family' : 'Times New Roman', 'size': 14})
        plt.fill_between(range(len(smoother.data[0])), low[0], up[0], alpha=0.3)
        # if i==0:
            # plt.ylabel('reward')


import seaborn as sns
import random
import numpy as np
import matplotlib.pyplot as plt
from JS_Env.operator_choose_rule import action_translator
import pandas as pd
import os
import pickle
from RL_Env.Agent_Env2 import Env
sns.set_style("white")

# df.columns=['D3QN',"DDQN+PER","DDQN",]
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
# plt.figure(figsize=(10,5))



def test_model(Agent,env,model_path):
    C=[]
    Agent.load_model(model_path)
    for i in range(100):
        state, done = env.reset()
        ep_reward = 0
        while True:
            action = Agent.test_action(state)
            Job_i = action_translator(action, env)
            next_state, reward, done = env.step(Job_i)
            ep_reward += reward
            if done == True:
                fitness = env.SF.C_max
                C.append(fitness)
                break
    return C
plt.subplot(1,2,1)
# plt.subplot2grid((2,5), (0,0))
draw_f(F100,0,"D3QN")

# plt.subplot2grid((2,5), (0,1))
draw_f(F101,2,'DDQN+PER')
# plt.yticks([],[])
# plt.subplot2grid((2,5), (0,2))
draw_f(F001,1,"DDQN")
# plt.yticks([],[])
# plt.subplot2grid((2,5), (0,3))
draw_f(F110,2,'DQN+PER')
# plt.yticks([],[])
# plt.subplot2grid((2,5), (0,4))
draw_f(F000,2,'DQN')
# plt.yticks([],[])
plt.legend(loc=0)
plt.ylabel("Total Reward of Episode",fontdict={'family' : 'Times New Roman', 'size': 14})

plt.subplot(1,2,2)
# plt.subplot2grid((2,5), (1,0))

F000=PR_False_DNN_DQN[0]+'\C_max.pkl'
F001=PR_False_DNN_DDQN[0]+'\C_max.pkl'
F010=PR_False_Duelling_DQN[0]+'\C_max.pkl'
F011=PR_False_Duelling_DDQN[0]+'\C_max.pkl'
F100=PR_True_DNN_DQN[0]+'\C_max.pkl'
F101=PR_True_DNN_DDQN[1]+'\C_max.pkl'
F110=PR_True_Duelling_DQN[0]+'\C_max.pkl'
F111=PR_True_Duelling_DDQN[0]+'\C_max.pkl'
draw_f(F100,0,"D3QN")
# plt.subplot2grid((2,5), (1,1))
# plt.yticks([],[])
draw_f(F101,2,'DDQN+PER')
# plt.subplot2grid((2,5), (1,2))
# plt.yticks([],[])
draw_f(F001,1,"DDQN")
# plt.subplot2grid((2,5), (1,3))
# plt.yticks([],[])
draw_f(F110,2,'DQN+PER')
# plt.subplot2grid((2,5), (1,4))
draw_f(F000,2,'DQN')
# plt.yticks([],[])
plt.legend(loc=0)
plt.ylabel("Makespan",fontdict={'family' : 'Times New Roman', 'size'   : 1})

plt.show()
from Instance.Text_extract import data
from Single_RL.DQN_series.DQN import DQN
from Single_RL.Params import args

model_path = r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\model_save2\prFalse\CNN_DNN\ddqnFalse\128_0.0001_50_500000_0.95\step3500'
Ci = "C1"
Ki = '11'   # 11,12,13,14 是同一种工件的不同类型       '1/2/5'
f = r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL/Instance/Bilge_Ulusoy' + '/' + Ci + '/' + 'E' + Ki + '.pkl'
n, m, PT, agv_trans, MT, agv_num = data(f)
env = Env(n, m, agv_num,PT,MT,agv_trans,m)
env.reset()
args.max_o_len = env.max_o_len
args.n=n
# args.NUM_ACTIONS=4

args.PRE =False
args.Network_type ='CNN_DNN'
args.DDQN = False
args.GAMMA = 0.9
args.BATCH_SIZE = 128
args.LR = 0.0001
args.Q_NETWORK_ITERATION = 50
args.MEMORY_CAPACITY = 100000
Agent = DQN(args)
C1 = test_model(Agent, env, model_path)

model_path = r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\model_save2\prFalse\CNN_DNN\ddqnTrue\5_0.0001_100_100000_0.9\step4000'
args.PRE =False
args.Network_type ='CNN_DNN'
args.DDQN = True
args.GAMMA = 0.9
args.BATCH_SIZE = 5
args.LR = 0.0001
args.Q_NETWORK_ITERATION = 100
args.MEMORY_CAPACITY = 100000
Agent = DQN(args)
C2 = test_model(Agent, env, model_path)

model_path = r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\model_save2\prTrue\CNN_DNN\ddqnTrue\5_0.0001_100_100000_0.9\step4000'
args.PRE =True
args.Network_type ='CNN_DNN'
args.DDQN = True
args.GAMMA = 0.9
args.BATCH_SIZE = 5
args.LR = 0.0001
args.Q_NETWORK_ITERATION = 100
args.MEMORY_CAPACITY = 100000
Agent = DQN(args)
C3 = test_model(Agent, env, model_path)

model_path = r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL\Single_RL\model_save2\prFalse\CNN_DNN\ddqnFalse\5_0.0001_200_500000_0.9\step4000'
args.PRE =False
args.Network_type ='CNN_DNN'
args.DDQN = False
args.GAMMA = 0.9
args.BATCH_SIZE = 5
args.LR = 0.0001
args.Q_NETWORK_ITERATION = 200
args.MEMORY_CAPACITY = 500000
Agent = DQN(args)
C4 = test_model(Agent, env, model_path)

C=[C1,C2,C4,C3]
NP=[]
Y_mean=[]
for i in range(len(C)-1):
    ni=[]
    for j in range(len(C[i])):
        ni.append(((C3[j]-C[i][j])/C3[j])*100)
    Y_mean.append(sum(ni) / len(ni))
    NP.append(ni)
print(len(NP))
print(min(C1),min(C2),min(C4),min(C3))
C1m=sum(NP[0])/len(C1)
NP=np.array(NP)
x=[_+1 for _ in range(3)]
# plt.subplot(122)
NP=NP.T
df = pd.DataFrame(NP)
df.columns=['D3QN',"DDQN+PER","DDQN",]
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.boxplot(x =NP,
            patch_artist=True,
            labels = ['D3QN',"DDQN","DQN+PER",], # 添加具体的标签名称
            showmeans=True,
            showfliers=True,
            whis=0.5,
            widths=0.2,
            boxprops = {'color':'black','facecolor':'#9999ff'},
            flierprops = {'marker':'o','markerfacecolor':'red','color':'black'},
            meanprops = {'marker':'D','markerfacecolor':'indianred'},
            medianprops = {'linestyle':'--','color':'orange'},
            zorder=1,
            notch=True)
plt.hlines(0,xmin=0,xmax=5,linestyles="dashdot",zorder=2)
plt.hlines(C1m,xmin=0,xmax=5,linestyles="dashed",color='green',zorder=2)
plt.text(y=-3,x=3.5,s="baseline",fontsize=14,rotation=90)
plt.ylabel('Standardize performance(SP)',fontdict={'family' : 'Times New Roman', 'size': 14})
plt.plot(x,Y_mean,"--",color='#e17701')
# plt.xlabel('DRL algorithms')
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.show()

