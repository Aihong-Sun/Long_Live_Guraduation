class Job:
    def __init__(self,idx,G_color,PT,MT,L_U):
        self.idx=idx
        self.G_color=G_color
        self.PT=PT
        self.MT=MT
        self.cur_site=L_U
        self.L_U=L_U
        self.end=0
        self.cur_op=0
        self.Finished=False
        self.PRE_AGV=None
        self.PRE_Machine=None
        self._onAGV=[]

    def get_info(self):
        return self.end,self.cur_site,self.PT[self.cur_op],self.MT[self.cur_op]

    def update(self,e,AGV,Machine):
        self.end=e
        self.cur_op+=1
        self.cur_site=self.MT[self.cur_op-1]
        if self.cur_op==len(self.PT):
            self.Finished=True
        self.PRE_AGV = AGV
        self.PRE_Machine = Machine
        self._onAGV.append(self.PRE_AGV.idx)