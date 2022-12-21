import xlrd

xlsx=xlrd.open_workbook(r'C:\Users\Administrator\PycharmProjects\RJSP_singleRL/result_makespan.xlsx')
sheet1 = xlsx.sheets()[0]
sheet1_cols = sheet1.ncols
X=[]
for i in range(sheet1_cols):
    X.append(sheet1.col_values(i))


del X[1]
del X[-4]
X0=X[4]
del X[4]
NP=[]
Y_mean=[]
for i in range(len(X)):
    ni=[]
    for j in range(len(X[i])):
        ni.append(((X0[j]-X[i][j])/X0[j])*100)
    Y_mean.append(sum(ni)/len(ni))
    NP.append(ni)

import matplotlib.pyplot as plt

# import seaborn as sns; sns.set()
x=[_+1 for _ in range(6)]
# plt.plot(x,SP1,label="GA")
# plt.plot(x,SP2,label="LMS")
# plt.plot(x,SP3,label="drl_BEST")
# plt.plot(x,SP4,label="drl_aVE")
# plt.legend()
# 绘图
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.boxplot(x = NP,
            patch_artist=True,
            labels = ["LOR+FAFS",'LRPT+FAFS','FIFO+ST','LOR+ST','LRPT +ST','D3QN'], # 添加具体的标签名称
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
plt.yticks(fontsize=14)
plt.xticks([1,2,3,4,5,6], ["LOR+FAFS",'LRPT+FAFS','FIFO+ST','LOR+ST','LRPT +ST','D3QN'],fontsize=14,)
plt.hlines(0,xmin=0,xmax=6.5,linestyles="dashdot",zorder=2)
plt.text(y=-3,x=6.3,s="baseline",fontsize=14,rotation=90)
plt.plot(x,Y_mean,"--",color='#e17701')
# plt.xlabel('approaches',fontsize=12)
plt.hlines(Y_mean[-1],xmin=0,xmax=6.5,linestyles="dashed",color='green',zorder=2)
plt.ylabel('SP',fontdict={'family' : 'Times New Roman', 'size': 14})
# 显示图形
plt.show()
