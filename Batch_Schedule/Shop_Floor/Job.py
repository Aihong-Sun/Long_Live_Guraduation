

class Job:
    def __init__(self,orderid,Subbatch_idx,Subbatch_num,ProModel,ots,SB_num=1,Gantt_colors=None):
        self.orderID=orderid
        self.Subbatch=Subbatch_idx
        self.ProModel=ProModel
        self.Subbatch_num=Subbatch_num
        # print(self.orderID,self.Subbatch_num)
        self.ots=ots
        self.cur_op=0
        self.SB_num=SB_num
        if SB_num==1:
            self.end=0
        else:
            self.end=[0 for _ in range(SB_num)]
        self.last_opt=0     #工件上道工序加工时间
        self.Gantt_color=Gantt_colors

    def Initial_Batch(self,Bat_num):
        self.Bat_num=Bat_num

    #不考单件流的工件更新方法
    def update(self,end):
        self.cur_op+=1
        self.end=end

    #考虑分批的工件更新方法
    def update_consistent(self,end_lis,Batch_i):
        self.end[Batch_i]=end_lis

    #阶段更新
    def update_op(self):
        self.cur_op+=1

