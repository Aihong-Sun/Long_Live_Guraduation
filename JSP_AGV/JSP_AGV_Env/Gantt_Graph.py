import copy

import matplotlib.pyplot as plt
import numpy as np

#注：此处的Machine和AGV分别表示Machine类列表和AGV类列表
def Gantt(Machines,agvs=None,file=None,name=None,C_max=None):
    plt.figure(figsize=(18,6))
    plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus'] = False  # 显示负号
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite','navy', 'sandybrown', 'moccasin','chartreuse','darkslateblue','hotpink','lemonchiffon',
         'mediumvioletred','mintcream','mistyrose','oldlace','olivedrab',]

    Job_text=['J'+str(i+1) for i in range(100)]
    Machine_text=['M'+str(i+1) for i in range(50)]
    t = 0
    k=0
    Le=[]
    Job_c=[]
    if agvs!=None:
        for k in range(len(agvs)):
            for m in range(len(agvs[k].using_time)):
                if agvs[k].using_time[m][1] - agvs[k].using_time[m][0] != 0:
                    if agvs[k]._on[m]!=None:
                        plt.barh(k, width= agvs[k].using_time[m][1]- agvs[k].using_time[m][0],
                                        height=0.6,
                                        left=agvs[k].using_time[m][0],
                                        color=M[agvs[k]._on[m]],
                                        edgecolor='black')
                    else:
                        plt.barh(k, width=agvs[k].using_time[m][1] - agvs[k].using_time[m][0],
                                 height=0.6,
                                 left=agvs[k].using_time[m][0],
                                 color='white',
                                 edgecolor='black',)
                    # plt.text(x=agvs[k].using_time[m][0]+(agvs[k].using_time[m][1] - agvs[k].using_time[m][0])/2-2,
                    #          y=k-0.05,
                    #          # s=Machine_text[agvs[k].trace[m]]+'-'+Machine_text[agvs[k].trace[m+1]],
                    #          fontsize=5)
                if  agvs[k].using_time[m][1]>t:
                    t=agvs[k].using_time[m][1]

    for i in range(len(Machines)):
        for j in range(len(Machines[i].using_time)):
            if Machines[i].using_time[j][1] - Machines[i].using_time[j][0] != 0:
                li=plt.barh(i+k+1, width=Machines[i].using_time[j][1] - Machines[i].using_time[j][0],
                         height=0.8, left=Machines[i].using_time[j][0],
                         color=M[Machines[i]._on[j]],
                         edgecolor='black',label=Job_text[Machines[i]._on[j]])
                if Machines[i]._on[j] not in Job_c:
                    Job_c.append(Machines[i]._on[j])
                    Le.append(li)
            if Machines[i].using_time[j][1]>t:
                t=Machines[i].using_time[j][1]
    if agvs!=None:
        lis=['AGV1','AGV2','AGV3','AGV4','AGV5','AGV6','AGV7']
        list1=['M'+str(_+1) for _ in range(len(Machines)-1)]
        lis=copy.copy(lis[:len(agvs)])
        lis.extend(list1)
        plt.xlim(0,t)
        plt.hlines(k + 0.4,xmin=0,xmax=t, color="black")  # 横线
        plt.yticks(np.arange(i + k + 1), lis,size=13,)
        plt.title('Instance:'+name+' and makespan:'+str(C_max))
        plt.xlabel('Time(s)')
        dictionary = dict(zip(Le,Job_c))
        d_order = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=False))
        Le=list(d_order.keys())
        Job_t=Job_text[:len(Le)]
        plt.legend(Le,Job_t,ncol=2,frameon=False,bbox_to_anchor=(1.01, 1),fontsize="medium")
    if file!=None:
        with open(file,'wb') as fb:
            plt.savefig(fb)
    plt.close()
