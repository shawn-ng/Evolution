import pygame
import random 
import time
import numpy as np
from Agent.agent import CreateAgent as CA
from food import Food as F
import constants as const 
from mind import AgentThink 
"""
Game Logic.

Might be using pygame to build the logic of the game (dont think of implementing RL. Build a human playable game first.)

Rules of the game
1. Agent will be place in initial location of the habitat 
2. We need to fix the habitat of that agent 
3. Agent will eat the sources to gain health 
4. Agent will continue to explore the environment 
5. Agent will have little vision hence harder to get resources 
6. Each day will last 60 seconds and if agent not back at the habitat the agent will die
7. The goal of the game is to survive as many iteration of 60 seconds as possible 
"""

episodes = const.EPISODES
class Game():

    def __init__(self, width = const.WIDTH , height = const.HEIGHT , number_agent = 1 , number_food = 150, max_episode_len = 200):

        self.dis_width = width
        self.dis_height = height

        # Creating agent
        self.number_agent = number_agent
        self.agents_dict = {}
        self.agents_reward = {}
        self.agents_home_list = []
        self.populateAgent()

        # Creating food 
        self.food_count = number_food
        self.foods_dict = {}
        self.foods_list = []
        self.populateFood()

        # game state
        self.game_over = False
        self.fps = 10
        self.round = 0
        self.episode_len = 0 
        self.max_episode_len = max_episode_len

        #game env in array format
        self.game_state_array = []

        # agent action
        self.actions = [0.0,1.0,2.0,3.0,4.0] # rest, left, right, down , up
        self.action = 0

        # agent reward
        self.agents_reward = {}

    def startGame(self):
        dis = pygame.display.set_mode((self.dis_width,self.dis_height))
        pygame.display.update()
        pygame.display.set_caption("The Evolution Game")
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()

        # think
        lr = 0.001
        agentThink = AgentThink(gamma= 0.99, epsilon = 1.0, lr=lr,
                         input_dims=[const.WIDTH,const.HEIGHT], n_actions=len(self.actions) ,
                         batch_size=64, eps_end = 0.01)
        scores, eps_history = [], []

        for i in range(episodes):
            
            score = 0
            score_list = []
            self.reset()
        
            observation = self.twoD_map(dis)

            while not self.game_over:                

                seconds = round((pygame.time.get_ticks() - start_ticks)/1000)
                
                # check time on condition
                if seconds%20 == 0 and seconds != 0: 
                    self.round += 1
                    # Resetting timer to 0 
                    start_ticks = pygame.time.get_ticks()

                    for agent in self.agents_dict.keys():
                        self.agents_dict[agent].checkIsHome()
                        self.agents_dict[agent].updateEnergy(activity=4)
                        # the reward depend on how many day did the agent survive
                        if self.agents_dict[agent].die == False:
                            self.agents_dict[agent].survive_day += 1
                        else: 
                            self.game_over == True
            

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_over = True
            
                dis.fill((0,0,0))

                # check food
                for key in self.foods_dict.keys():
                    if self.foods_dict[key].eaten == False:
                        self.foods_dict[key].displayFood(display = dis)

                # agent home 
                for agent in self.agents_dict.keys():
                    self.agents_dict[agent].displayHome(display = dis)

                # check agent whether izit alive
                for agent in self.agents_dict.keys():
                    if self.agents_dict[agent].die == False:
                        self.agents_dict[agent].move(width = self.dis_width, height = self.dis_height, foods_dict = self.foods_dict, action = self.action)
                        self.agents_dict[agent].displayAgent(display = dis ,foods_list = self.foods_list ,vision_dis = True)   
                    else:
                        self.game_over = True
                
                pygame.display.update()
                
                self.game_state_array = np.array(self.twoD_map(pygame.display.get_surface()))

                self.action = agentThink.choose_actions(observation)

                observation_, reward, done , info = self.step()

                for key in reward.keys():
                    score += reward[key]

                agentThink.store_transitions(observation, observation_,  reward["agent-1"] , self.action,  done)
                agentThink.learn()
                observation = observation_

                clock.tick(self.fps)

            score_list.append(score)
            scores.append(score_list)
            eps_history.append(agentThink.epsilon)

            avg_score = np.mean(score_list)
            print('episode ', i, 'score %.2f' % score,
                    'average score %.2f' % avg_score,
                    'epsilon %.2f' % agentThink.epsilon)
            
                

    def step(self):

        self.agents_reward = self.get_reward()
        self.agents_dict = self.agents_dict
        self.episode_len += 1

        if self.episode_len > self.max_episode_len:
            self.game_over = True
        
        return self.game_state_array, self.agents_reward, self.game_over, self.episode_len

    def reset(self):
        self.game_over = False

        # resetting agent location and home 
        self.agents_dict = {}
        self.agents_home_list = []
        self.agents_reward = {}
        self.populateAgent()
    
        self.foods_dict = {}
        self.foods_list = []
        self.populateFood()

        self.game_state_array = []
        
        self.round = 0

        self.episode_len = 0

    def action_space(self):
        return self.actions

    def get_reward(self):
        
        # reward every round they survive with good health
        for key in self.agents_dict.keys():

            health = self.agents_dict[key].energy
            round =  self.agents_dict[key].survive_day
            foodcount = self.agents_dict[key].food_eaten

            if self.agents_dict[key].die == False:
                
                # reward = energy x 0.6 + round x 0.2 + food count x 0.2

                self.agents_reward[key] = self.agents_reward[key] + (health * 0.6) + (round * 0.2) + (foodcount * 0.2)

            elif self.agents_dict[key].die == True:
                
                self.agents_reward[key] -= 100 

        return self.agents_reward

    def initGame(self):
        pygame.init()

    def quitGame(self):
        pygame.quit()

    def populateAgent(self):
        
        for i in range(self.number_agent):
            self.agents_dict[f"agent-{i + 1}"] = CA(id=i + 1, home_location=[10 + (i + 1) * 10, (i) * 10], init_location=[10 + (i + 1) * 10, (i) * 10])
            self.agents_reward[f"agent-{i+1}"] = 0
            self.agents_home_list.append([10 + (i + 1) * 10, (i) * 10])

    def populateFood(self):

        for i in range(self.food_count):
            foodx = round(random.randrange(20, self.dis_width - 10)/ 10) * 10 
            foody = round(random.randrange(20, self.dis_width - 10)/ 10) * 10
            
            self.foods_dict[f"food-{i + 1}"] = F(id = i + 1, location = [foodx, foody]) 

            # Putting into the list of food
            self.foods_list.append([foodx, foody])

    def twoD_map(self, surface): 
        return pygame.surfarray.array2d(surface)

pygame.init()

Game = Game()

Game.startGame()

Game.quitGame()