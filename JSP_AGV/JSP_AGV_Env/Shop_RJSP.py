from JSP_AGV.JSP_AGV_Env.AGV import AGV
from JSP_AGV.JSP_AGV_Env.machine import Machine
from JSP_AGV.JSP_AGV_Env.Job import Job

#绘图颜色
colors=[ 'yellow','purple','orange', 'green', 'rosybrown','papayawhip', 'aqua', 'lightblue','aquamarine',
         'azure', 'beige', 'bisque', 'blanchedalmond', 'blue',
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


class RJSP:
    def __init__(self,n,m,agv_num,PT,MT,TT,L_U):
        self.n,self.m,self.agv_num=n,m,agv_num
        self.PT=PT
        self.MT=MT
        self.TT=TT
        self.L_U=L_U
        self.Jobs=[]
        self.C_max=0

    def reset(self):
        self.Jobs = []
        for i in range(self.n):
            Ji = Job(i,colors[i],self.PT[i], self.MT[i], self.L_U)
            self.Jobs.append(Ji)
        self.Machines = []
        for j in range(self.m+1):
            Mi = Machine(j)
            self.Machines.append(Mi)
        self.AGVs = []
        for k in range(self.agv_num):
            agv = AGV(k, self.L_U)
            self.AGVs.append(agv)

    def decode(self,Ji,agv):
        trans1 = self.TT[agv.cur_site][Ji.cur_site]
        trans2 = self.TT[Ji.cur_site][Ji.cur_op]
        J_end, J_site, op_t, op_m = Ji.get_info()
        s, end = agv.ST(Ji.end, trans1, trans2)
        J_m = self.Machines[op_m]
        agv.update(s,  trans1, trans2, Ji.cur_site,op_m, Ji.idx)
        start = max(end, J_m.end)
        J_m.update(start, op_t, Ji.idx, Ji.G_color)
        Jend = start + op_t
        Ji.update(Jend, agv, J_m)
        if Jend > self.C_max:
            self.C_max = Jend