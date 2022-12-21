import torch
import numpy as np
from torch.utils.tensorboard import SummaryWriter
import argparse
from normalization import Normalization, RewardScaling
from replaybuffer import ReplayBuffer
from ppo_discrete import PPO_discrete
import matplotlib.pyplot as plt

def evaluate_policy(args, env, agent):
    times = 3
    evaluate_reward = 0
    for _ in range(times):
        s,_ = env.reset()
        done = False
        episode_reward = 0
        while not done:
            a = agent.test_action(s)  # We use the deterministic policy during the evaluating
            s_, r, done= env.step(a)
            episode_reward += r
            s = s_
        evaluate_reward += episode_reward

    return evaluate_reward / times


def main(args, env):
    args.action_dim = 14
    args.max_episode_steps = 24  # Maximum number of steps per episode
    args.state_dim=(10,14)

    evaluate_num = 0  # Record the number of evaluations
    evaluate_rewards = []  # Record the rewards during the evaluating
    total_steps = 0  # Record the total steps during the training

    replay_buffer = ReplayBuffer(args)
    agent = PPO_discrete(args)
    episode_step=0
    while total_steps < args.max_train_steps:
        episode_step+=1
        s,done = env.reset()
        done=False
        episode_steps = 0
        while not done:
            episode_steps += 1
            a, a_logprob = agent.choose_action(s)  # Action and the corresponding log probability
            s_, r, done, = env.step(a)

            # When dead or win or reaching the max_episode_steps, done will be Ture, we need to distinguish them;
            # dw means dead or win,there is no next state s';
            # but when reaching the max_episode_steps,there is a next state s' actually.
            if done :
                dw = True
                break
            else:
                dw = False

            replay_buffer.store(s, a, a_logprob, r, s_, dw, done)
            s = s_
            total_steps += 1

            # When the number of transitions in buffer reaches batch_size,then update
            if replay_buffer.count == args.batch_size:
                agent.update(replay_buffer, total_steps)
                replay_buffer.count = 0

        # Evaluate the policy every 'evaluate_freq' steps
        if episode_step % args.evaluate_freq == 0 :
            evaluate_num += 1
            evaluate_reward = evaluate_policy(args, env, agent)
            evaluate_rewards.append(evaluate_reward)
            print("evaluate_num:{} \t evaluate_reward:{} \t".format(evaluate_num, evaluate_reward))

    x=[_ for _ in range(len(evaluate_rewards))]
    plt.plot(x,evaluate_rewards)
    plt.show()

if __name__ == '__main__':
    from JSP_AGV.Instance.GS_Instance import Instance
    from JSP_AGV.RL_Env.RJSP_rlenv import Env

    Insi = [4, 6, 20]
    name = 'n' + str(Insi[0]) + '_m' + str(Insi[1]) + '_agv' + str(Insi[2])
    n, m, agv_num, PT, MT, agv_trans = Instance(name)
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

    parser.add_argument("--max_train_steps", type=int, default=5000*24, help=" Maximum number of training steps")
    parser.add_argument("--evaluate_freq", type=float, default=20, help="Evaluate the policy every 'evaluate_freq' steps")
    parser.add_argument("--save_freq", type=int, default=20, help="Save frequency")
    parser.add_argument("--batch_size", type=int, default=612, help="Batch size")
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
    args = parser.parse_args()
    env = Env(args)
    main(args, env,)
