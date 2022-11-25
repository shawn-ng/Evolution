import numpy as np 
import pygame 

from ev_game import Game as G
from mind import AgentThink
import constants as const



if __name__ == '__main__':

    lr = 0.001
    episodes = const.EPISODES

    env_game = G(width=const.WIDTH, height=const.HEIGHT)
    agent = AgentThink(gamma= 0.99, epsilon = 1.0, lr=lr,
                         input_dims=[const.WIDTH,const.HEIGHT], n_actions=len(env_game.actions) ,
                         batch_size=64, eps_end = 0.01)
    scores, eps_history = [], []

    for i in range(episodes):
        score = 0 
        done = False
        env_game.reset()

        env_game.initGame()
        env_game.startGame()
        
        observation = env_game.game_state_array

        while done == False:
            
            action = str(agent.choose_actions(observation))
    
            observation_, reward, done, info = env_game.step(action)
            for key in reward.keys():
                score += reward[key]
        
            agent.store_transitions(observation, observation_,  reward["agent-1"] , action,  done)

            agent.learn
            observation = observation_

        scores.append(score)
        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])
        print(agent.action_memory)
        print('episode ', i, 'score %.2f' % score,
                'average score %.2f' % avg_score,
                'epsilon %.2f' % agent.epsilon)
            