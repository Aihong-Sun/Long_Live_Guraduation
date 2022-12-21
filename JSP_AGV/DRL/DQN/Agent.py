from JSP_AGV.DRL.DQN.Network.CNN import *
from JSP_AGV.DRL.DQN.Memory_choice.Prioritized_Memory import PrioritizedBuffer as PRE_Memory
from JSP_AGV.DRL.DQN.Memory_choice.Uniform_Memory  import Memory as uniform_Memory
from JSP_AGV.DRL.DQN.Network.CNN_dueling import Net as Net1
import numpy as np
import random
import os


def huber_loss(x, y):
    z = torch.abs(x-y).squeeze()
    return torch.where(z < 1., 0.5*z**2, z-0.5)

class DQN():
    """docstring for DQN"""
    def __init__(self,args):
        super(DQN, self).__init__()
        self.n=args.n
        self.NUM_ACTIONS=args.NUM_ACTIONS
        self.max_o_len=args.max_o_len
        self.W=args.W
        self.H=args.H
        self.episodes=args.episodes
        if args.Network_type=='CNN_DNN':
            self.eval_net, self.target_net = Net(self.W,self.H,self.NUM_ACTIONS,args.feature_len), Net(self.W,self.H,
                                                                                   self.NUM_ACTIONS,args.feature_len)
        if args.Network_type=='CNN_duelling':
            self.eval_net, self.target_net = Net1(self.W, self.H, self.NUM_ACTIONS,args.feature_len), Net1(self.W,self.H,
                                                                                   self.NUM_ACTIONS,args.feature_len)
        self.pre = args.PRE
        if self.pre:
            self.memory = PRE_Memory(args.MEMORY_CAPACITY)
        else:
            self.memory = uniform_Memory(args.MEMORY_CAPACITY)

        self.ddqn=args.DDQN
        self.epsilon=0.8
        self.max_exploration_step=args.max_exploration_step
        self.step=0
        self.learn_step_counter = 0
        self.memory_counter = 0
        self.MAX_EPSILON=args.MAX_EPSILON
        self.MIN_EPSILON= args.MIN_EPSILON
        self.BATCH_SIZE=args.BATCH_SIZE
        self.GAMMA=args.GAMMA
        self.Q_NETWORK_ITERATION=args.Q_NETWORK_ITERATION
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=args.LR)
        self.loss_func = nn.MSELoss()

    def choose_action(self, S,epsilon):
        X = np.reshape(S[0], (-1, 4, self.W,self.H))
        X = torch.FloatTensor(X)
        Y = torch.unsqueeze(torch.FloatTensor(S[1]),0)
        if random.random()>=epsilon:# greedy policy
            action_value = self.eval_net.forward(X,Y)
            action = torch.max(action_value, 1)[1].data.numpy()[0]
        else: # random policy
            action = np.random.randint(0,self.NUM_ACTIONS)
        return action

    def test_action(self,S):
        X = np.reshape(S[0], (-1, 4, self.W,self.H))
        X= torch.FloatTensor(X)
        Y = torch.unsqueeze(torch.FloatTensor(S[1]), 0)
        action_value = self.eval_net.forward(X,Y)
        action = torch.max(action_value, 1)[1].data.numpy()[0]
        return action

    def store_transition(self, state, action, reward, next_state,done):
        if self.pre:    #priority exprience memory remember
            self.memory.push(state, action, reward, next_state,done)
        else:
            self.memory.remember((state, action, reward, next_state,done))
        self.memory_counter+=1

    def learn(self):
        #update the parameters
        if self.learn_step_counter % self.Q_NETWORK_ITERATION ==0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter+=1
        if self.pre:
            idx, IS_weights, states, actions, rewards, next_states,dones=self.memory.sample(self.BATCH_SIZE)
            IS_weights = torch.FloatTensor(IS_weights)
            batch_state_X = np.array([o[0] for o in states])
            batch_state_Y = np.array([o[1] for o in states])
            batch_next_state_X = np.array([o[0] for o in next_states])
            batch_next_state_Y = np.array([o[1] for o in next_states])
            batch_action = np.array(actions)
            batch_reward = np.array(rewards)
            batch_done = np.array(dones)
        else:
            batch = self.memory.sample(self.BATCH_SIZE)

            # sample batch from memory
            batch_state_X = np.array([o[0][0] for o in batch])
            batch_state_Y = np.array([o[0][1] for o in batch])
            batch_next_state_X = np.array([o[3][0] for o in batch])
            batch_next_state_Y = np.array([o[3][1] for o in batch])
            batch_action = np.array([o[1] for o in batch])
            batch_reward = np.array([o[2] for o in batch])
            batch_done= np.array([o[4] for o in batch])
        batch_action = torch.LongTensor(np.reshape(batch_action, (-1, len(batch_action)))).detach()
        batch_reward = torch.FloatTensor(np.reshape(batch_reward, (-1, len(batch_reward))))
        batch_done=torch.FloatTensor(batch_done)
        batch_state_X = torch.FloatTensor(np.reshape(batch_state_X, (-1, 4, self.W,self.H)))
        batch_next_state_X = torch.FloatTensor(np.reshape(batch_next_state_X, (-1, 4, self.W,self.H)))
        batch_state_Y = torch.FloatTensor(batch_state_Y)
        batch_next_state_Y = torch.FloatTensor(batch_next_state_Y )

        #q_eval
        q_eval = self.eval_net(batch_state_X,batch_state_Y).gather(1, batch_action)
        # q_next = self.target_net(batch_next_state_X,batch_next_state_Y)

        if self.ddqn:
            max_actions = self.eval_net(batch_next_state_X,batch_next_state_Y).max(1)[1].view(-1,1)
            Q_next = self.target_net(batch_next_state_X,batch_next_state_Y).gather(1, max_actions).view(-1)
        else:
            Q_next = self.target_net(batch_next_state_X,batch_next_state_Y).max(1)[0].view(-1)
        q_target = batch_reward + self.GAMMA * Q_next*(1-batch_done)

        if self.pre:
            TD_errors = huber_loss(q_eval, q_target.detach())
            loss = torch.mean(TD_errors * IS_weights)
        else:
            loss = self.loss_func(q_eval, q_target.detach())

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        if self.pre:
            self.memory.update_priority(idx, TD_errors.detach().numpy())

    def save_model(self,file,step):
        f = file + '/' + 'step' + str(step)
        if not os.path.exists(f):
            os.makedirs(f)
        torch.save(self.eval_net.state_dict(), f +'/' + 'eval_net.pkl')
        torch.save(self.target_net.state_dict(), f + '/' + 'target_net.pkl')

    def load_model(self,model_path):
        if os.path.exists(model_path + '/eval_net.pkl'):
            self.eval_net.load_state_dict(torch.load(model_path + '/eval_net.pkl'))
            self.target_net.load_state_dict(torch.load(model_path + '/target_net.pkl'))
            print('loading success...')
        else:
            print('loading defeat...')
