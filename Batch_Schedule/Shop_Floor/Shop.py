from Batch_Schedule.Shop_Floor.Job import Job
from Batch_Schedule.Shop_Floor.Machine import Machine
from Batch_Schedule.Shop_Floor.ultis import *

#绘图颜色
colors=['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen', 'lightgray', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']


class SF_env:
    def __init__(self,file):
        self.Mac_List, self.Proc_Path, self.Ord_Lis=read_data(file)
        self.Ord_num=len(self.Ord_Lis['orderId'])
        self.Op_num=len(self.Proc_Path)

    #重置机器
    def reset(self):
        #完工时间
        self.C_max=0
        #总拖期
        self.T_tard=0
        #未达到交货期的工件个数
        self.tard_num=0
        #初始化机器
        self.Mac_Lis=[[] for i in range(7)]
        for i in range(len(self.Mac_List['Machine'])):
            self.Mac_Lis[int(self.Mac_List['ProcessNo'][i])-1].append(Machine(self.Mac_List['Machine'][i],
                self.Mac_List['ProcessNo'][i], self.Mac_List['Process'][i], self.Mac_List['ProcessTime(ms)'][i],
                self.Mac_List['pipetime(min)'][i]))

    #不考单件流的批量分割的订单初始化方法
    def order_spilt(self,Batch_lis):
        self.Ord_Set = []
        k=1
        for i in range(len(self.Ord_Lis['orderId'])):
            self.Ord_Set.append(Job(self.Ord_Lis['orderId'][i], k+ 1, Batch_lis[i], self.Ord_Lis['ProdModel'][i],
                                    self.Ord_Lis['ots'][i],SB_num=len(Batch_lis[i]),Gantt_colors=colors[i]))
            k+=1

    # 基于单件流的批量分割订单初始化方法
    def order_reset(self,):
        self.Ord_Set=[]
        for i in range(len(self.Ord_Lis['orderId'])):
            self.Ord_Set.append(
                Job(self.Ord_Lis['orderId'][i], i + 1, self.Ord_Lis['count'][i], self.Ord_Lis['ProdModel'][i],
                    self.Ord_Lis['ots'][i],Gantt_colors=colors[i]))

    #基于工件批的普通前插式解码
    def decode(self,Job_idx,Mac,Opath):
        '''
        :param Job_idx: int
        :param Mac: int
        :param Opath: 0-1 binary
        '''
        Ji=self.Ord_Set[Job_idx]
        O_num=Ji.cur_op      # 当前加工工序
        Op = self.Proc_Path[O_num + 1]
        if Opath==1:
            if O_num==1:
                Op=self.Proc_Path[3]
                Mach = self.Mac_Lis[2][Mac]
            elif O_num==2:
                Op = self.Proc_Path[2]
                Mach = self.Mac_Lis[1][Mac]
            else:
                Mach = self.Mac_Lis[O_num][Mac]
        else:
            Mach = self.Mac_Lis[O_num][Mac]
        # processing
        Mach.processing(Ji,Op)
        # 计算交货期
        if Ji.cur_op>=7:
            Tard=Judge_Ots(Ji.ots, Ji.end)  #判断是否超过交货期
            if  Tard:
                self.T_tard+= Tard
                self.tard_num+=1
        #计算完工时间
        if self.C_max<Ji.end:
            self.C_max=Ji.end

    #机器安排规则:最先可用最先加工
    def Machine_Assign(self,Ji,O_num,Op):
        Mac=self.Mac_Lis[O_num]
        M_e = [Mi.end for Mi in Mac]
        mach = Mac[M_e.index(min(M_e))]
        for Bi in range(Ji.SB_num):
            if Ji.Subbatch_num[Bi]!=0:
                mach.processing_consistent(Ji,Bi,Op)
        ft=max(Ji.end)
        Ji.update_op()
        return ft

    #基于单件流+工序重叠操作的前插式解码
    def decode_Consistent(self,Job_idx,Opath):
        Ji=self.Ord_Set[Job_idx]
        O_num=Ji.cur_op
        if Opath == 1:
            if O_num == 1:
                Op = self.Proc_Path[3]
                ft=self.Machine_Assign(Ji,O_num+1,Op)
            elif O_num == 2:
                Op = self.Proc_Path[2]
                ft=self.Machine_Assign(Ji,O_num-1,Op)
            else:
                Op = self.Proc_Path[O_num + 1]
                ft= self.Machine_Assign(Ji, O_num ,Op)
        else:
            Op = self.Proc_Path[O_num + 1]
            ft= self.Machine_Assign(Ji, O_num, Op)

        # 计算交货期
        if Ji.cur_op >= 7:
            Tard = Judge_Ots(Ji.ots, ft)  # 判断是否超过交货期
            if Tard:
                self.T_tard += Tard
                self.tard_num += 1
        # 计算完工时间
        if self.C_max < ft:
            self.C_max = ft
        return ft


    def decode_Consistent_Improved(self,Job_idx,Opath):
        Ji = self.Ord_Set[Job_idx]
        O_num = Ji.cur_op
        real_O=O_num
        Op = self.Proc_Path[O_num + 1]
        for i in range(len(Opath)):
            if Opath[i] == 1:
                if O_num == 1:
                    real_O=O_num + 1
                    Op = self.Proc_Path[3]
                elif O_num == 2:
                    real_O = O_num -1
                    Op = self.Proc_Path[2]

            #采用规则选择机器
            Mac = self.Mac_Lis[real_O]
            M=[Mi for Mi in Mac if Mi.last_jobtype==Ji.ProModel]
            if M!=[]:
                M_e = [Mi.end for Mi in M]
            else:
                M_e = [Mi.end for Mi in Mac]
            mach = Mac[M_e.index(min(M_e))]

            if Ji.Subbatch_num[i] != 0:
                mach.processing_consistent(Ji, i, Op)
        ft = max(Ji.end)
        Ji.update_op()

        # 计算交货期
        if Ji.cur_op >= 7:
            Tard = Judge_Ots(Ji.ots, ft)  # 判断是否超过交货期
            if Tard:
                self.T_tard += Tard
                self.tard_num += 1
        # 计算完工时间
        if self.C_max < ft:
            self.C_max = ft
        return ft
