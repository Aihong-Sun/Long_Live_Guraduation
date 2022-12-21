import seaborn as sns; sns.set()
import numpy as np
import pandas as pd
from JSP_AGV.RL_Env.RJSP_rlenv import Env
from JSP_AGV.PDR import *
from utils import *
from params import *
from JSP_AGV.Instance.GS_Instance import Instance
from JSP_AGV.DRL.DQN.Agent import DQN
from JSP_AGV.DRL.PPO_discrete.ppo_discrete import PPO_discrete

# 模型保存的路径
model_path=r'C:\Users\Aihong\PycharmProjects\Long_Live_Guraduation\JSP_AGV\model_save_min1\prTrue\CNN_duelling\ddqnTrue\128_0.0001_50_100000_0.98\step4400'   #模型保存位置

# 验证算例
Insi=[4, 6, 22]
name = 'n' + str(Insi[0]) + '_m' + str(Insi[1]) + '_agv' + str(Insi[2])
n, m, agv_num, PT, MT, agv_trans = Instance(name)

#初始化调度环境
args1 = get_args(n, m, agv_num, PT, MT, agv_trans, W=10, H=14, per=True, Network_type='CNN_duelling', DDQN=True,
                GAMMA=0.98, BATCH_SIZE=128, LR=0.0001, Q_NETWORK_ITERATION=50)
env = Env(args1)
env.reset()


parser = argparse.ArgumentParser("Hyperparameter Setting for PPO_discrete")
max_o_len = max([len(Pi) for Pi in PT])
# Environment parameter
parser.add_argument('--NUM_ACTIONS', default=14, type=int, help='Processing Machine Matrix')
parser.add_argument('--W', default=2*(n+1), type=int, help='wigth Matrix')
parser.add_argument('--H', default=2*(m+1), type=int, help='Processing Machine Matrix')
parser.add_argument('--feature_len', default=4 + m + agv_num, type=int, help='the length of artificial features')

# Job Shop parameter
parser.add_argument('--n', default=n, type=int, help='job numbers')
parser.add_argument('--m', default=m, type=int, help='machine numbers')
parser.add_argument('--max_o_len', default=max_o_len, type=int, help='max operation length')
parser.add_argument('--PT', default=PT, type=int, help='processing time')
parser.add_argument('--MT', default=MT, type=int, help='processing machines')
parser.add_argument('--TT', default=agv_trans, type=int, help='transportation time bewteen machines')
parser.add_argument('--agv_num', default=agv_num, type=int, help='agv number')
parser.add_argument('--action_dim', default=14, type=int, help='agv number')
parser.add_argument("--max_train_steps", type=int, default=5000*24, help=" Maximum number of training steps")
parser.add_argument("--evaluate_freq", type=float, default=10, help="Evaluate the policy every 'evaluate_freq' steps")
parser.add_argument("--save_freq", type=int, default=20, help="Save frequency")
parser.add_argument("--batch_size", type=int, default=64, help="Batch size")
parser.add_argument("--mini_batch_size", type=int, default=64, help="Minibatch size")
parser.add_argument("--hidden_width", type=int, default=64, help="The number of neurons in hidden layers of the neural network")
parser.add_argument("--lr_a", type=float, default=1e-4, help="Learning rate of actor")
parser.add_argument("--lr_c", type=float, default=1e-4, help="Learning rate of critic")
parser.add_argument("--gamma", type=float, default=0.99, help="Discount factor")
parser.add_argument("--lamda", type=float, default=0.95, help="GAE parameter")
parser.add_argument("--epsilon", type=float, default=0.2, help="PPO clip parameter")
parser.add_argument("--K_epochs", type=int, default=10, help="PPO parameter")
parser.add_argument("--use_adv_norm", type=bool, default=True, help="Trick 1:advantage normalization")
parser.add_argument("--use_state_norm", type=bool, default=True, help="Trick 2:state normalization")
parser.add_argument("--use_reward_norm", type=bool, default=False, help="Trick 3:reward normalization")
parser.add_argument("--use_reward_scaling", type=bool, default=True, help="Trick 4:reward scaling")
parser.add_argument("--entropy_coef", type=float, default=0.01, help="Trick 5: policy entropy")
parser.add_argument("--use_lr_decay", type=bool, default=True, help="Trick 6:learning rate Decay")
parser.add_argument("--use_grad_clip", type=bool, default=True, help="Trick 7: Gradient clip")
parser.add_argument("--use_orthogonal_init", type=bool, default=True, help="Trick 8: orthogonal initialization")
parser.add_argument("--set_adam_eps", type=float, default=True, help="Trick 9: set Adam epsilon=1e-5")
parser.add_argument("--use_tanh", type=float, default=True, help="Trick 10: tanh activation function")
args2 = parser.parse_args()

# test DRL
#建立 Agent,并将参数赋予Agent
Agent1 = DQN(args1)
Agent1.load_model(model_path)
Agent1 = DQN(args1)

Agent2=PPO_discrete(args2)
model_path=r'C:\Users\Aihong\PycharmProjects\Long_Live_Guraduation\JSP_AGV\Experiment\Experiment_result\PPO\model_save4_6_20\step350'
Agent2.load_model(model_path)
res_dqn=test_model(Agent1, env,100)
print('result of DQN',np.mean(res_dqn))
res_PPO=test_model(Agent2, env,100)
print('result of PPO',np.mean(res_PPO))



# test rule
for i in range(14):
    res_pdr=dispatching_rule(env,i,100)
    print('rule',i,'--result:',  np.mean(res_pdr))

