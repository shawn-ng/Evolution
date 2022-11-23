import pygame
from ev_game import Game 
from mind import AgentThink


pygame.init()

if __name__ == '__main__':

    lr = 0.0001
    n_games = 500
    learning = AgentThink(gamma=0.99, epsilon=1.0, lr=lr, 
                input_dims=env.observation_space.shape,
                n_actions=env.action_space.n, mem_size=1000000, batch_size=64,
                epsilon_end=0.01)
