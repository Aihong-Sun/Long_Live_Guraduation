import matplotlib.pyplot as plt
plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
from matplotlib.ticker import MaxNLocator


def Gantt(Machines):
    #对工件批分配甘特图颜色
    k=0
    y_label=[]
    y_ticks=[]
    for Mi in Machines:
        y_label.append('M'+str(Mi.idx))
        k+=1
        i=0
        for usi in Mi.using_time:
            plt.barh(k, width=usi[1] -usi[0],
                     height=0.6,
                     left=usi[0],
                     color=Mi._on[i],
                     edgecolor='black')
            plt.text(x=usi[0]+0.1,
                     y=k-0.1,
                     s=Mi.PJ_Info[i],
                     fontsize=12,fontproperties='Times New Roman')
            i+=1
        y_ticks.append(k)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    # plt.yticks(y_ticks,y_label,fontproperties='SimSun')
    plt.ylabel('机器',fontproperties='SimSun',fontsize=13)
    plt.xlabel('时间', fontproperties='SimSun',fontsize=13)
    plt.show()
