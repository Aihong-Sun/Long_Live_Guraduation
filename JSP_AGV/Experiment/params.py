
import argparse

parser = argparse.ArgumentParser()

def get_args(n,m,agv_num,PT,MT,TT,W,H,per,Network_type,DDQN,GAMMA,BATCH_SIZE,LR,Q_NETWORK_ITERATION,MEMORY_CAPACITY=100000,max_exploration_step=400000,episode=5000):
    max_o_len = max([len(Pi) for Pi in PT])
    #params for RL agent:
    parser.add_argument('--PRE',default=per,type=bool,help='wether choose prioritized experience replay')
    parser.add_argument('--Network_type',default=Network_type,type=str,help='choose which type of network,Candidate:CNN_duelling,CNN_DNN')
    parser.add_argument('--DDQN',default=DDQN,type=bool,help='wether choose DDQN')

    #Environment parameter
    parser.add_argument('--NUM_ACTIONS',default=14,type=int,help='Processing Machine Matrix')
    parser.add_argument('--W', default=W, type=int, help='wigth Matrix')
    parser.add_argument('--H', default=H, type=int, help='Processing Machine Matrix')
    parser.add_argument('--feature_len', default=4 + m + agv_num, type=int, help='the length of artificial features')

    #Hyperparameter
    parser.add_argument('--LR',default=LR,type=float,help='learning rate')
    parser.add_argument('--MEMORY_CAPACITY',default=MEMORY_CAPACITY,type=int,help='memory capacity')
    parser.add_argument('--MIN_EPSILON',default=0.05,type=float,help='min epsilon')
    parser.add_argument('--MAX_EPSILON',default=0.8,type=float,help='max epsilon')
    parser.add_argument('--BATCH_SIZE',default=BATCH_SIZE,type=float,help='batch size')
    parser.add_argument('--GAMMA',default=GAMMA,type=float,help='GAMMA')
    parser.add_argument('--Q_NETWORK_ITERATION',default=Q_NETWORK_ITERATION,type=int,help='network iteration')
    parser.add_argument('--max_exploration_step',default=max_exploration_step,type=int,help='network iteration')
    parser.add_argument('--episodes',default=episode,type=int,help='network iteration')


    # Job Shop parameter
    parser.add_argument('--n', default=n, type=int, help='job numbers')
    parser.add_argument('--m', default=m, type=int, help='machine numbers')
    parser.add_argument('--max_o_len', default=max_o_len, type=int, help='max operation length')
    parser.add_argument('--PT', default=PT, type=int, help='processing time')
    parser.add_argument('--MT', default=MT, type=int, help='processing machines')
    parser.add_argument('--TT', default=TT, type=int, help='transportation time bewteen machines')
    parser.add_argument('--agv_num', default=agv_num, type=int, help='agv number')
    args = parser.parse_args()
    return args

def change_Envargs(args,n,m,agv_num,PT,MT,TT):
    args.n=n
    args.m=m
    args.agv_num=agv_num
    args.PT=PT
    args.MT=MT
    args.TT=TT
    return args

def change_RLargs(args,per,Network_type,DDQN,GAMMA,BATCH_SIZE,LR,Q_NETWORK_ITERATION,MEMORY_CAPACITY=100000,max_exploration_step=200000,episode=5000):
    args.PRE=per
    args.Network_type=Network_type
    args.DDQN=DDQN
    args.GAMMA=GAMMA
    args.BATCH_SIZE=BATCH_SIZE
    args.LR=LR
    args.Q_NETWORK_ITERATION=Q_NETWORK_ITERATION
    args.MEMORY_CAPACITY=MEMORY_CAPACITY
    args.max_exploration_step =max_exploration_step
    args.episodes = episode
    return args