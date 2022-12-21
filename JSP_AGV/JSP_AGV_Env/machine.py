class Machine:
    def __init__(self,idx):
        self.idx=idx
        self.using_time=[]
        self._on=[]
        self.Gantt_Info=[]
        self.end=0
        self.total=0

    def update(self,s,pt,_on,G_color):
        e=s+pt
        self.using_time.append([s,e])
        self._on.append(_on)
        self.Gantt_Info.append(G_color)
        self.end=e
        self.total+=pt