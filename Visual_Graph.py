import matplotlib.pyplot as plt
import pickle
import numpy as np
import seaborn as sns; sns.set()
from tsmoothie.smoother import LowessSmoother

# 默认设置
plt.figure(figsize=(18, 6))
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# 绘制调度Gantt图
def Gantt(Machines,AGVs=None,save_fig=None,makespan=None,):
    k = 0
    y_ticks=[[],[]]
    if AGVs:
        #AGV上的调度Gantt图
        for agv in AGVs:
            j=0
            for ui in agv.using_time:
                if ui[1] - ui[0] != 0:
                    plt.barh(k, width=ui[1] - ui[0],
                             height=0.8, left=ui[0],
                             color=agv.Gantt_Info[j],
                             edgecolor='black', label=agv._on[j])
                j += 1
            y_ticks[0].append(k)
            y_ticks[1].append('AGV'+str(agv.idx+1))
            k+=1
        plt.hlines(k - 0.4, xmin=0, xmax=100, color="black")  # 横线
    # 机器上的加工Gantt图
    for Mi in Machines:
        j=0
        for ui in Mi.using_time:
            if ui[1] - ui[0] != 0:
                plt.barh(k, width=ui[1] - ui[0],
                         height=0.8, left=ui[0],
                         color=Mi.Gantt_Info[j],
                         edgecolor='black',label=Mi._on[j])
            j+=1
            y_ticks[0].append(k)
            y_ticks[1].append('M' + str(Mi.idx + 1))
            k += 1
    plt.yticks(y_ticks[0],y_ticks[1])
    plt.xlabel('Time(s)')
    if makespan:
        plt.title('makespam:',makespan)
    if save_fig:
        with open(save_fig,'wb') as fb:
            plt.savefig(fb)
    else:
        plt.show()

# bi-objective pareto front
def Plot_NonDominatedSet(EP,shape,G_label,xlable,ylable,title=None):

    x = []
    y = []
    for i in range(len(EP)):
        x.append(EP[i].fitness[0])
        y.append(EP[i].fitness[1])
    plt.plot(x, y, shape,label=G_label)
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.title(title)
    plt.legend()

# 3-objective pareto front
def TriPlot_NonDominatedSet(ax,color,EP,Instance,Algo_name,cpu_t):
    x = []
    y = []
    z=[]
    for i in range(len(EP)):
        x.append(EP[i].fitness[0])
        y.append(EP[i].fitness[1])
        z.append(EP[i].fitness[2])

    # 绘制散点图
    ax.scatter(x, y, z,color=color,label=str(Algo_name))
    # 添加坐标轴(顺序是Z, Y, X)
    ax.set_zlabel('Max Machine Load', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('Total Machine Load', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('Makespan', fontdict={'size': 15, 'color': 'red'})
    plt.title('Instance: '+Instance+' '+'Algo_name: '+Algo_name+' '+'CPU(s): '+str(cpu_t))
    plt.show()

#迭代曲线
def Iterate_curve(data,label,xlabel,ylabel,title):
    x=[_ for _ in range(len(data[0]))]
    for i in range(len(data)):
        plt.subplot(1, 2, i+1)
        plt.plot(x,data[i])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(label[i])
    plt.show()

#绘制误差带阴影图
def Plot_Error_band_shaded(Data_file,title):
    with open(Data_file, "rb") as fb:
        K = pickle.load(fb)
        d = np.array(K)
        data = []
        for di in d:
            data.append(sum(di) / len(di))
        x = [_ for _ in range(len(data))]
        smoother = LowessSmoother(smooth_fraction=0.03, iterations=2)
        smoother1 = LowessSmoother(smooth_fraction=0.03, iterations=2)
        smoother.smooth(data)
        low, up = smoother.get_intervals('prediction_interval')
        smoother1.smooth(data)
        # plt.plot(x,smoother.data[0], '.',linewidth=0.1)
        plt.plot(x, smoother1.smooth_data[0], linewidth=2, label=title)
        plt.xlabel('Training step(*10)', fontdict={'family': 'Times New Roman', 'size': 14})
        plt.fill_between(range(len(smoother.data[0])), low[0], up[0], alpha=0.3)

# 绘制箱型图
def Box_plot(Data,best,mean,colums,xticks=None):
    Data = np.array(Data)
    x = [_  for _ in range(len(Data))]
    plt.boxplot(x=Data,
                patch_artist=True,
                labels=colums,  # 添加具体的标签名称
                showmeans=True,
                showfliers=True,
                whis=0.5,
                widths=0.2,
                boxprops={'color': 'black', 'facecolor': '#9999ff'},
                flierprops={'marker': 'o', 'markerfacecolor': 'red', 'color': 'black'},
                meanprops={'marker': 'D', 'markerfacecolor': 'indianred'},
                medianprops={'linestyle': '--', 'color': 'orange'},
                zorder=1,
                notch=True)
    plt.hlines(0, xmin=0, xmax=5, linestyles="dashdot", zorder=2)
    plt.hlines(best, xmin=0, xmax=5, linestyles="dashed", color='green', zorder=2)
    plt.text(y=-3, x=3.5, s="baseline", fontsize=14, rotation=90)
    plt.ylabel('Standardize performance(SP)', fontdict={'family': 'Times New Roman', 'size': 14})
    plt.plot(x, mean, "--", color='#e17701')
    if xticks:
        plt.xticks(x,xticks)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.show()

