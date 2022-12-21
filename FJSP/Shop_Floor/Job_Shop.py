from FJSP.Shop_Floor.Job import Job
from FJSP.Shop_Floor.Machine import Machine

#绘图颜色
colors=[ 'yellow','purple','orange', 'green', 'rosybrown','papayawhip', 'aqua', 'lightblue','aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blue',
        'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
        'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen',
        'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon',
        'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink',
        'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia',
        'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'honeydew',
        'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
        'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen',
        'lightgray', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray',
        'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine',
        'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
        'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite',
        'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen',
        'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple',
        'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna',
        'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle',
        'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']

class Job_shop:
    def __init__(self,n,m,O_num,pro_Mac,pro_t,Energy_Consumption=None,ESPC=None):
        '''
        :param n: 工件数
        :param m: 机器数
        :param O_num: 工序数
        :param pro_Mac: 加工机器矩阵
        :param pro_t:   加工时间矩阵
        :param Energy_Consumption: 负载能耗
        :param ESPC: 空载能耗
        '''
        self.n= len(pro_Mac)
        self.m=m
        self.O_num=O_num
        self.PM = pro_Mac
        self.PT = pro_t
        self.Energy_Consumption=Energy_Consumption
        self.ESPC=ESPC

    # 车间重置
    def reset(self):
        self.C_max = 0
        self.Jobs=[]    #工件集
        for i in range(self.n):
            if self.Energy_Consumption:
                Ji = Job(i, self.PM[i], self.PT[i], colors[i],self.Energy_Consumption[i])
            else:
                Ji=Job(i,self.PM[i],self.PT[i],colors[i])
            self.Jobs.append(Ji)
        self.Machines=[]    #机器集
        for j in range(self.m):
            Mi=Machine(j)
            self.Machines.append(Mi)

    def resched(self,t,PM=None,PT=None,EC=None):
        for Ji in self.Jobs:
            idx=0
            for us in Ji.using_time:
                if us[0]<t:
                    idx+=1
                else:
                    Ji.using_time=Ji.using_time[:idx]
                    Ji._on=Ji._on[:idx]
                    Ji.cur_op=idx
                    Ji.been_op=idx
                    if Ji.using_time!=[]:
                        Ji.end=max(Ji.using_time[-1][1],t)
                    else:
                        Ji.end =t
                    break
        for Mi in self.Machines:
            idx=0
            for us in Mi.using_time:
                if us[0]<t:
                    idx+=1
                else:
                    Mi.using_time = Mi.using_time[:idx]
                    # Mi.end=Mi.using_time[idx][1]
                    Mi._on=Mi._on[:idx]
                    Mi.PJ_Info=Mi.PJ_Info[:idx]
                    if Mi.using_time!=[]:
                        Mi.end = max(Mi.using_time[-1][1],t)
                    else:
                        Mi.end=t
                    break
        print(len(PM))
        for i in range(len(PM)):
            if EC:
                Ji=Job(i+self.n,PM[i],PT[i],colors[i+self.n+1],EC[i])
            else:
                Ji = Job(i + self.n, PM[i], PT[i], colors[i + self.n + 1])
            Ji.end = t
            self.Jobs.append(Ji)

        self.n+=len(PM)
        print(self.n)

    # 对比原始方案和当前方案
    def Scheme_Comparison(self,SJS):
        Num_Dp=0    #设备更换次数: Number of device replacements
        for i in range(len(SJS.Jobs)):
            J1,J2=self.Jobs[i],SJS.Jobs[i]
            for j in range(len(J1._on)):
                if J1._on[j]!=J2._on[j]:
                    Num_Dp+=1
        return Num_Dp

    #总能耗
    def Total_Energy_Comsumption(self):
        Tec=0   #总能耗
        for Ji in self.Jobs:
            Tec+=Ji.Energy_using
        for Mi in self.Machines:
            gap = [Mi.using_time[_][1]-Mi.using_time[_ + 1][0] for _ in range(len(Mi.using_time) - 1)
                   if Mi.using_time[_ + 1][0] - Mi.using_time[_][1] > 0]  # 机器空隙
            if Mi.using_time !=[]:
                gap.append(Mi.using_time[0][0])
            Tec+=sum(gap)*self.ESPC[Mi.idx]
        return Tec

    # 解码
    def decode(self,Job,Machine):
        Ji=self.Jobs[Job]
        o_pt,M_idx = Ji.get_next_info(Machine)
        Mi=self.Machines[M_idx-1]
        end=Mi.decode(Ji,o_pt)
        if end>self.C_max:
            self.C_max=end
