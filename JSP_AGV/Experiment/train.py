import matplotlib.pyplot as plt
from JSP_AGV.RL_Env.action import action_translator
import os
import pickle
from JSP_AGV.RL_Env.RJSP_rlenv import Env

def main(Agent,env,file,result_path,model_path):
    Reward_total = []
    C_total = []
    rewards_list = []
    E=[]
    C = []
    dqn = Agent
    print("Collecting Experience....")
    for i in range(dqn.episodes):
        print("\r", end="")
        print("training progress: {}%: ".format((i/dqn.episodes)*100), "▋" * (i//100), end="")
        state,done = env.reset()
        ep_reward = 0
        while True:
            action,e = dqn.choose_action(state)
            E.append(dqn.epsilon)
            next_state, reward, done = env.step(action)
            dqn.store_transition(state, action, reward, next_state)
            ep_reward += reward
            if dqn.memory_counter >=Agent.BATCH_SIZE:
                dqn.learn()
                if done and i%10==0:
                    ret, f, C1, R1 = test(env,i,dqn,e)
                    Reward_total.append(R1)
                    C_total.append(C1)
                    rewards_list.append( ret)
                    C.append(f)
            if done:
                if i%200==0 and i>3000 or i==5000:
                    dqn.save_model(model_path,i)
                break
            state = next_state
    x = [_ for _ in range(len(C))]
    if not os.path.exists(file):
        os.makedirs(file)
    plt.plot(x, rewards_list)
    plt.savefig(file+'/'+'Reward.png')
    plt.close()
    plt.plot(x, C)
    plt.savefig(file+'/'+'Cmax.png')
    plt.close()

    if not os.path.exists(result_path):
        os.makedirs(result_path)
    with open(os.path.join(result_path, 'C_max' + ".pkl"), "wb") as f:
        pickle.dump(C_total, f, pickle.HIGHEST_PROTOCOL)
    with open(os.path.join(result_path, 'Reward' + ".pkl"), "wb") as f:
        pickle.dump(Reward_total, f, pickle.HIGHEST_PROTOCOL)

def test(env,i,dqn,e):
    returns = []
    C=[]
    for  total_step in range(10):
        state, done = env.reset()
        ep_reward = 0
        while True:
            action = dqn.test_action(state)
            next_state, reward, done = env.step(action)
            ep_reward += reward
            if done == True:
                fitness = env.SF.C_max
                C.append(fitness)
                break
        returns.append(ep_reward)
    print('----------------------------->>>>','time step:',i,'','Reward ：',sum(returns)/10 ,'','C_max:',sum(C) /10,'explore rate:', e)
    return sum(returns) / 10,sum(C) /10,C,returns

if __name__ == '__main__':

    from JSP_AGV.DRL.DQN.Agent import DQN
    from JSP_AGV.Instance.GS_Instance import Instance
    from JSP_AGV.Experiment.params import get_args, change_Envargs, change_RLargs
    Insi=[10, 6, 2]
    name = 'n' + str(Insi[0]) + '_m' + str(Insi[1]) + '_agv' + str(Insi[2])
    n, m, agv_num, PT, MT, agv_trans = Instance(name)
    args = get_args(n, m, agv_num, PT, MT, agv_trans, W=10, H=14, per=False, Network_type='CNN_DNN', DDQN=False,
                    GAMMA=0.95, BATCH_SIZE=128, LR=0.0001, Q_NETWORK_ITERATION=50)
    env = Env(args)
    GM = [0.95,0.97, 0.98, 0.99]
    BZ=[128,]
    Lr=[0.0001,]
    Q_N=[50,150]
    MC=[100000]
    pre = [True,False]
    Network = ['CNN_duelling','CNN_DNN']
    DDQN = [ False,True]

    for GAMMA in GM:
        for BATCH_SIZE in BZ:
            for LR in Lr:
                for Q_NETWORK_ITERATION in Q_N:
                    for MEMORY_CAPACITY in MC:
                        for pr in pre:
                            for net in Network:
                                for ddqn in DDQN:
                                    print()
                                    print('<<<<------------开始训练------------>>>>')
                                    print('pr' + str(pr) + '/' + str(net) + '/' + 'ddqn' + str(
                                        ddqn) + '/' + str(BATCH_SIZE) + '_' + str(LR) + '_' + str(
                                        Q_NETWORK_ITERATION) + '_' + str(MEMORY_CAPACITY) + '_' + str(GAMMA))
                                    file = "../Result_min1/" + 'pr' + str(pr) + '/' + str(net) + '/' + 'ddqn' + str(
                                        ddqn) + '/' + str(BATCH_SIZE) + '_' + str(LR) + '_' + str(
                                        Q_NETWORK_ITERATION) + '_' + str(MEMORY_CAPACITY) + '_' + str(GAMMA)
                                    result_path = "../Draw_Result_min1/" + 'pr' + str(pr) + '/' + str(
                                        net) + '/' + 'ddqn' + str(ddqn) + '/' + str(BATCH_SIZE) + '_' + str(
                                        LR) + '_' + str(Q_NETWORK_ITERATION) + '_' + str(MEMORY_CAPACITY) + '_' + str(
                                        GAMMA) + '/'
                                    model_path = "../model_save_min1/" + 'pr' + str(pr) + '/' + str(
                                        net) + '/' + 'ddqn' + str(ddqn) + '/' + str(BATCH_SIZE) + '_' + str(
                                        LR) + '_' + str(Q_NETWORK_ITERATION) + '_' + str(MEMORY_CAPACITY) + '_' + str(
                                        GAMMA) + '/'
                                    args = change_RLargs(args, per=pr, Network_type=net, DDQN=ddqn, GAMMA=0.95,
                                                         BATCH_SIZE=BATCH_SIZE, LR=LR,
                                                         Q_NETWORK_ITERATION=Q_NETWORK_ITERATION,episode=5000)
                                    Agent=DQN(args)
                                    main(Agent,env,file,result_path,model_path)
                                    break
                                break
                            break
                        break
                    break
                break
            break
        break
