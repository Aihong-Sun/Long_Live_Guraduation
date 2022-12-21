import random

# Job selection
#选择最早到达机器的工件
def FCFS(SF):
    Jobs = [Job for Job in SF.Jobs if not Job.Finished]     #choose not finished jobs
    finish_t = [Ji.end for Ji in Jobs]  # get jobs' last finished time
    min_finish=min(finish_t)    # min finish time
    Job_idx = [Jobs[i] for i, x in enumerate(finish_t) if x == min_finish]  # choose Jobs with min last finish time
    return random.choice(Job_idx)

#选择工序加工时间最短的工件
def SOPT(SF):
    Jobs = [Job for Job in SF.Jobs if not Job.Finished] #choose not finished jobs
    pt = [Ji.PT[Ji.cur_op] for Ji in Jobs]
    min_pt = min(pt)
    srtp = [Jobs[i] for i, x in enumerate(pt) if x == min_pt]   # choose Jobs with min last finish time
    return random.choice(srtp)

#选择工件加工时间最短的工件
def SJPT(SF):
    Jobs = [Job for Job in SF.Jobs if not Job.Finished] #choose not finished jobs
    pt = [sum(Ji.PT) for Ji in Jobs]
    min_pt = min(pt)
    srtp = [Jobs[i] for i, x in enumerate(pt) if x == min_pt]   # choose Jobs with min last finish time
    return random.choice(srtp)

#选择剩余工时最短的工件
def SRW(SF):
    Jobs = [Job for Job in SF.Jobs if not Job.Finished]  # choose not finished jobs
    pt = [sum(Ji.PT[Ji.cur_op:]) for Ji in Jobs]
    min_pt = min(pt)
    srtp = [Jobs[i] for i, x in enumerate(pt) if x == min_pt]  # choose Jobs with min last finish time
    return random.choice(srtp)  #由于采用随机取的方式可能造成一定的不稳定性，因而，选择第一个

#选择工序加工时间与工件总加工时间和之比最小的工件
def PDJT(SF):
    Jobs = [Job for Job in SF.Jobs if not Job.Finished]  # choose not finished jobs
    pt = [Ji.PT[Ji.cur_op]/sum(Ji.PT) for Ji in Jobs]
    min_pt = min(pt)
    srtp = [Jobs[i] for i, x in enumerate(pt) if x == min_pt]  # choose Jobs with min last finish time
    return random.choice(srtp)  #由于采用随机取的方式可能造成一定的不稳定性，因而，选择第一个

#选择具有通过将工序加工时间乘以工件总加工时间获得的最小值对应的工件。
def PMJT(SF):
    Jobs = [Job for Job in SF.Jobs if not Job.Finished]  # choose not finished jobs
    pt = [Ji.PT[Ji.cur_op]*sum(Ji.PT) for Ji in Jobs]
    min_pt = min(pt)
    srtp = [Jobs[i] for i, x in enumerate(pt) if x == min_pt]  # choose Jobs with min last finish time
    return random.choice(srtp)  #由于采用随机取的方式可能造成一定的不稳定性，因而，选择第一个

#选择工序加工时间与剩余工时之比最小的工件
def PDRW(SF):
    Jobs = [Job for Job in SF.Jobs if not Job.Finished]  # choose not finished jobs
    pt = [Ji.PT[Ji.cur_op]/sum(Ji.PT[Ji.cur_op:]) for Ji in Jobs if Ji.PT[Ji.cur_op]!=0]
    try:
        min_pt = min(pt)
        srtp = [Jobs[i] for i, x in enumerate(pt) if x == min_pt]  # choose Jobs with min last finish time
    except:
        srtp =Jobs
    return random.choice(srtp)  #由于采用随机取的方式可能造成一定的不稳定性，因而，选择第一个

# AGV selection
# 选择最早到达工件所在位置的AGV
def FCFSA(SF,Ji):
    AGVs=SF.AGVs
    trans_Matrix=SF.TT
    arrive_t=[agv.end+trans_Matrix[agv.cur_site][Ji.cur_site] for agv in AGVs]
    min_arrive_t=min(arrive_t)
    srtp = [AGVs[i] for i, x in enumerate(arrive_t) if x == min_arrive_t]  # choose Jobs with min last finish time
    return random.choice(srtp)  #由于采用随机取的方式可能造成一定的不稳定性，因而，选择第一个

#选择取件时间最短的AGV
def STD(SF, Ji):
    AGVs = SF.AGVs
    trans_Matrix = SF.TT
    arrive_t = [trans_Matrix[agv.cur_site][Ji.cur_site] for agv in AGVs]
    min_arrive_t = min(arrive_t)
    srtp = [AGVs[i] for i, x in enumerate(arrive_t) if x == min_arrive_t]  # choose Jobs with min last finish time
    return random.choice(srtp)  #由于采用随机取的方式可能造成一定的不稳定性，因而，选择第一个

JS_set=[FCFS, SOPT, SJPT, SRW, PDJT, PDRW, PMJT, PDRW]
VS_set=[FCFSA,STD]