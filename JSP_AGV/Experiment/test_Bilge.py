list1=[96,102,99,112,87,118,115,161,118,147,82,76,85,88,69,98,79,151,104,136,84,86,86,89,74,104,86,153,106,141,103,108,111,126,96,120,127,163,122,159]
Basline = [130, 143, 142, 198, 130, 153, 129, 196, 178, 188, 98, 86, 114, 129, 98, 123, 92, 172, 123, 154, 109, 98, 103,
           155, 109, 128, 93, 172, 119, 158, 168, 169, 167, 242, 168, 189, 156, 251, 181, 246]
list2=[96,82,84,103,100,76,86,108,99,85,86,111,112,87,89,121,87,69,74,96,118,98,103,120,111,79,83,126,161,151,153,163,116,102,105,120,146,135,139,157]

list4=[138.5,39.2,145.1,510.2,282.4,100.5,96.6,475.9,27.7,44.9,617.3,414.9,255.4,268.7,216.5,452.0,18.4,98.7,139.4,223.2,74.7,66.6,902.2,370.2,549.3,2303.3,2403.3,3598.0,1300.6,2.7,9.3,295.8,57,284.0,54.1,1266.5,115.5,3252.9,66.6,822.2]
K = ['11','21','31','41', '51', '61', '71', '81', '91', '101', "12", '22', '32', '42', '52', '62', '72', '82',
         '92', '102',
         "13", '23', '33', '43', '53', '63', '73', '83', '93', '103', "14", '24', '34', '44', '54', '64', '74', '84',
         '94', '104']
name=[]
# print(len(list4))
for i in range(10):
    name.extend([str(i+1)+str(1),str(i+1)+str(2),str(i+1)+str(3),str(i+1)+str(4)])
list3=[]
list5=[]
for Ki in K:
    list3.append(list2[name.index(Ki)])
    list5.append(list4[name.index(Ki)])

LL=[100,118,113,132,89,142,118,173,133,170,87,94,92,107,77,119,85,151,116,161,87,98,94,104,76,126,90,155,118,164,110,126,123,144,105,152,136,193,131,172]
lm=[111.16,131.28,120.65,148.54,108.67,158.23,125.28,206,146.68,186.25,90.96,109.78,94,122.13,86.98,136.87,94.2,175,120.74,195.08,94.24,119.76,96,127.91,93.28,138.96,92.5,177,122.74,199,123.04,147.3,129.63,168.05,120.08,164.9,140.56,222.47,148.04,197.36]
SP1=[]
SP2=[]
SP3=[]
SP4=[]
for i in range(len(list3)):
    SP1.append(((Basline[i]-list1[i])/Basline[i])*100)
    SP2.append(((Basline[i] - list3[i]) / Basline[i]) * 100)
    SP3.append(((Basline[i] - LL[i]) / Basline[i]) * 100)
    SP4.append(((Basline[i] - lm[i]) / Basline[i]) * 100)

import matplotlib.pyplot as plt

# import seaborn as sns; sns.set()
x=[_+1 for _ in range(2)]
Y=[SP3,SP4]
meansY=[]
for Yi in Y:
    meansY.append(sum(Yi)/40)
print(meansY)
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

plt.boxplot(x = Y,
            patch_artist=True,
            labels = ['DRL_best',"DRL_Ave"], # 添加具体的标签名称
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
plt.yticks(fontsize=14,)
plt.xticks([1,2],['Best',"Ave."],fontsize=14,)
plt.hlines(0,xmin=0,xmax=5,linestyles="dashdot",zorder=2)
plt.text(y=-3,x=2.3,s="baseline",fontsize=14,rotation=90)
plt.plot(x,meansY,"--",color='#e17701')
# plt.xlabel('approaches',fontsize=12)
plt.ylabel('SP',fontdict={'family' : 'Times New Roman', 'size': 14})
# 显示图形
plt.show()
