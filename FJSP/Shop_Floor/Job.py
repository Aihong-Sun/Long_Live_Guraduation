'''
Code Time: 2022/11/22 15:36
by: Aihong-Sun
use for: Job describe
'''

class Job:
    def __init__(self,idx,processing_machine,processing_time,color=None,Energy_Consumption=None):
        '''
        :param idx: 工件编号
        :param processing_machine: 加工机器list
        :param processing_time: 加工时间list
        '''
        self.idx=idx
        self.processing_machine=processing_machine
        self.processing_time=processing_time
        self.O_num=len(self.processing_time)
        self.end=0
        self.cur_op=0
        self.been_op=0
        self.Gantt_color=color  #用于绘制Gantt图
        self.using_time=[]
        self._on=[]     #在哪个机器上加工
        self.EC=Energy_Consumption
        self.Energy_using=0

    def get_next_info(self,Machine):
        m_idx=self.processing_machine[self.cur_op][Machine]
        return self.processing_time[self.cur_op][Machine],m_idx

    def update(self,s,e,m_idx):
        M_site= self.processing_machine[self.cur_op].index(m_idx+1)
        self.end=e
        if self.EC:
            self.Energy_using += self.EC[self.cur_op][M_site] * (e - s)
        self.cur_op+=1
        self.using_time.append([s,e])
        self._on.append(M_site)
