
class Machine:
    def __init__(self,idx):
        self.idx=idx
        self.using_time=[]  #机器加工时间
        self.end=0      #机器完工时间
        self._on=[]     #在机器上加工的工件：用于记录，绘制Gantt图
        self.PJ_Info=[]        #用于记录加工工件的相关信息

    #解码
    def decode(self,Ji,o_pt):
        J_end=Ji.end
        if self.end<=J_end or self.using_time==[]: #后插
            self.using_time.append([J_end,J_end+o_pt])
            self.end=J_end+o_pt
            self._on.append(Ji.Gantt_color)
            self.PJ_Info.append((Ji.idx+1,Ji.cur_op+1))
            Ji.update(J_end, self.end, self.idx)
        else:       #前插
            J_s=max(self.end,Ji.end)
            gap=[[self.using_time[_][1],self.using_time[_+1][0]] for _ in range(len(self.using_time)-1)
                 if self.using_time[_+1][0]-self.using_time[_][1]>0]        #机器空隙
            if self.using_time[0][0]>=o_pt and J_end<self.using_time[0][0]:
                gap.append([0,self.using_time[0][0]])
            for gi in gap:
                if gi[0]>=J_end and gi[1]-gi[0]>=o_pt:
                    J_s=gi[0]
                elif gi[0]<J_end and gi[1]-J_end>=o_pt:
                    J_s = J_end
            J_e=J_s+o_pt
            self.using_time.append([J_s,J_e])
            self.using_time=sorted(self.using_time,key=lambda x:x[0])

            idx=self.using_time.index([J_s,J_e])
            self._on.insert(idx,Ji.Gantt_color)
            self.PJ_Info.insert(idx,(Ji.idx+1,Ji.cur_op+1))
            Ji.update(J_s,J_e,self.idx)
            self.end=max(J_e,self.end)
        return self.end
