import pandas as pd
import datetime
import matplotlib.pyplot as plt

#绘图颜色
colors=['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen', 'lightgray', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内

#read data
def read_data(file):
    Machine_data=pd.read_excel(file,sheet_name='data_pro_op_machine')
    op_data=pd.read_excel(file,sheet_name='data_pro_op')
    order=pd.read_excel(file, sheet_name='order')
    Machine_List=[]
    for i in range(len(Machine_data['Machine'])):
        Machine_List.append((Machine_data['Machine'][i],Machine_data['ProcessNo'][i],Machine_data['Process'][i],
                             Machine_data['ProcessTime(ms)'][i],Machine_data['pipetime(min)'][i],))
    K=pd.DataFrame(list(set(Machine_List)),columns=['Machine','ProcessNo','Process','ProcessTime(ms)','pipetime(min)'])
    Op_list=[]
    for i in range(len(op_data)):
        Op_list.append((op_data['Process'][i],op_data['ProcessNo'][i],op_data['prevno'][i],
                        op_data['Changeover(min)'][i],op_data['StandingTime(min)'][i]))
    D=pd.DataFrame(list(set(Op_list)),columns=['Process','ProcessNo','prevno','Changeover(min)','StandingTime(min)'])
    DK={}
    for i in range(len(D['Process'])):
        DK[D['ProcessNo'][i]]={'Process':D['Process'][i],'prevno':D['prevno'][i],
                               'Changeover(min)':D['Changeover(min)'][i],'StandingTime(min)':D['StandingTime(min)'][i]}
    return K,DK,order

#判断是否超出交货期
def Judge_Ots(ots,end):
    start='2022/2/15 00:00:00'
    ots=str(ots)
    d1 = datetime.datetime.strptime(start, '%Y/%m/%d %H:%M:%S')
    d2 = datetime.datetime.strptime(ots, '%Y-%m-%d %H:%M:%S')
    d = (d2 - d1).total_seconds()
    if end-d>0:
        return end-d
    else:
        return False

def Gantt(Machines):
    #对工件批分配甘特图颜色
    k=0
    y_label=[]
    y_ticks=[]
    for MS in Machines:
        for Mi in MS:
            y_label.append(Mi.Mac_name)
            k+=1
            i=0
            for usi in Mi.using_time:
                plt.barh(k, width=usi[1] -usi[0],
                         height=0.6,
                         left=usi[0],
                         color=Mi._on[i],
                         edgecolor='black')
                i+=1
            y_ticks.append(k)
    plt.yticks(y_ticks,y_label,fontproperties='SimSun')
    plt.show()

def Tard_barh(Jobs):
    T_ard=[]
    T_x=[]
    x=0
    for Ji in Jobs:
        end=Ji.end
        if isinstance(end,list):
            end=max(Ji.end)
        Tard=Judge_Ots(Ji.ots,end)
        if Tard:
            T_ard.append(Tard)
            T_x.append(x)
        x+=1
    plt.scatter(T_x,T_ard)
    plt.show()


