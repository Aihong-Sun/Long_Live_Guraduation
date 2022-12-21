

class Machine:
    def __init__(self,Mac_name,ProcessNo,Process,PT,Piptime):
        self.Mac_name=Mac_name
        self.ProcessNo=ProcessNo
        self.Process=Process
        self.PT=PT*0.0001
        self.Piptime=Piptime*60
        self.using_time=[]
        self._on=[]
        self.PJ_Info=[]
        self.last_jobtype=None
        self.end=self.Piptime

    #不考虑分批：加工job的下一道工序，其中op_info为当前工序的加工信息
    def processing(self,Ji,op_info):
        Ji_end=Ji.end
        changeoverT=0
        if self.last_jobtype!=Ji.ProModel and self.last_jobtype!=None:
            changeoverT=op_info['Changeover(min)']*60   #换型时间
        if Ji.end!=0:
            Ji_end=Ji.end+op_info['StandingTime(min)']*60   #静置时间
        pt=changeoverT+self.PT*Ji.Subbatch_num
        J_s = max(self.end, Ji_end)
        ET = J_s + pt
        self.using_time.append([J_s, ET])
        self._on.append(Ji.Gantt_color)
        Ji.update(ET)
        self.PJ_Info.append(Ji.orderID)
        self.end = ET
        self.last_jobtype = Ji.ProModel

    #一致分批在机器上的解码
    def processing_consistent(self,Ji,Batch_i,op_info):
        changeoverT = 0
        Ji_end=Ji.end[Batch_i]
        if self.last_jobtype != Ji.ProModel:
            changeoverT = op_info['Changeover(min)'] * 60  # 换型时间
        if Ji.end[Batch_i] != 0:
            Ji_end = Ji.end[Batch_i] + op_info['StandingTime(min)'] * 60  # 静置时间
        pt = changeoverT + self.PT * Ji.Subbatch_num[Batch_i]
        J_s = max(self.end, Ji_end)
        ET = J_s + pt
        self.using_time.append([J_s, ET])
        self._on.append(Ji.Gantt_color)
        Ji.update_consistent(ET, Batch_i)
        self.PJ_Info.append(str(Ji.orderID)+'_'+str(Batch_i)+'_'+str(Ji.Subbatch_num[Batch_i]))
        self.end = ET
        self.last_jobtype=Ji.ProModel