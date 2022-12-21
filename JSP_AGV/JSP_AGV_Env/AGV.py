class AGV:
    def __init__(self,idx,L_U):
        self.idx=idx
        self.cur_site=L_U
        self.using_time=[]
        self._on=[]
        self._to=[]
        self.end=0
        self.total=0
        self.total_trans=0

    def ST(self,s,t1,t2):
        start=max(s,self.end+t1)
        return start-t1,start+t2

    def update(self,s,trans1,trans2,J_site,J_m,_on=None):
        self.using_time.append([s,s+trans1])
        self.using_time.append([s + trans1, s+trans1 + trans2])
        self._on.append(None)
        self._on.append(_on)
        self._to.extend([J_site,J_m])
        self.end=s+trans1+trans2
        self.cur_site=J_m
        self.total=self.total+trans2
        self.total_trans=self.total_trans+trans1+trans2