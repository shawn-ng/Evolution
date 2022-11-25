"""
Mind 
- Need to build nn model 
    - have to use relu for activation function  
    - what the node does it need to think 
        1. vision available from that position
        2. 
"""
import torch as T
from torch import nn 
import torch.nn.functional as F
import torch.optim as optim 
import numpy as np 
import random
"""
is a offpolicy method and let the agent to figure how to play the game. 
is a bootstrap 
"""
# A simple DQN (replay)
class DeepQNetwork(nn.Module):
    def __init__(self, lr, input_dims, fc1_dims, fc2_dims, n_actions):
        super(DeepQNetwork, self).__init__()
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss() # This is because q-learning is like a straight line. Where we have alpha as our parameter to minimize the lost
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, states):
        x = F.relu(self.fc1(states))
        x = F.relu(self.fc2(x))

        action = self.fc3(x)

        return action 

class AgentThink:

    def __init__(self, lr, gamma, epsilon, input_dims, batch_size, n_actions, max_men_size = 100000,  eps_end=0.05, eps_dec=5e-4):
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon # times where you choose random action or policy action
        self.eps_min = eps_end
        self.eps_dec = eps_dec
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = max_men_size
        self.batch_size = batch_size
        self.mem_cntr = 0
        self.iter_cntr = 0

        self.Q_eval = DeepQNetwork(self.lr, n_actions = n_actions, input_dims = input_dims, fc1_dims = 250, fc2_dims = 250)

        self.state_memory = np.zeros((self.mem_size, *input_dims),
                                     dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims),
                                         dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)

    def store_transitions(self, state, state_, reward, action, terminal):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = terminal

        self.mem_cntr += 1

    def choose_actions(self, observation):
        if np.random.random() > self.epsilon:
            state = T.tensor([observation]).to(self.Q_eval.device)
            state = state.to(T.float32)
            actions = self.Q_eval.forward(state)

            action = T.argmax(actions).item()

            if action >= 250:
                action = np.random.choice(self.action_space)
        else:
            action = np.random.choice(self.action_space)

        return action

    def learn(self):

        if self.mem_cntr < self.batch_size:
            return 

        self.Q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_cntr, self.mem_size)

        batch = np.random.choice(max_mem, self.batch_size, replace = False)
        batch_index = np.arange(self.batch_size, dtype = np.int32)

        state_batch = T.tensor(self.state_memory[batch]).to(self.Q_eval.device)
        new_state_batch = T.tensor(
                self.new_state_memory[batch]).to(self.Q_eval.device)
        action_batch = self.action_memory[batch]
        reward_batch = T.tensor(
                self.reward_memory[batch]).to(self.Q_eval.device)
        terminal_batch = T.tensor(
                self.terminal_memory[batch]).to(self.Q_eval.device)
        q_eval = self.Q_eval.forward(state_batch)[batch_index, action_batch]
        q_next = self.Q_eval.forward(new_state_batch)
        q_next[terminal_batch] = 0.0

        q_target = self.gamma*T.max(q_next, dim=1)[0] + T.tensor(np.resize(reward_batch.detach().numpy(), (64,5)))

        loss = self.Q_eval.loss(q_target, q_eval).to(self.Q_eval.device)
        loss.backward()
        self.Q_eval.optimizer.step()

        self.iter_cntr += 1
        self.epsilon = self.epsilon - self.eps_dec \
            if self.epsilon > self.eps_min else self.eps_min
