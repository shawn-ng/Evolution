import pygame
import random 
import time
from Agent.agent import CreateAgent as CA
from food import Food as F
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
class Game():

    def __init__(self, width, height, number_agent = 1 , number_food = 10):

        self.dis_width = width
        self.dis_height = height

        # Creating agent
        self.number_agent = number_agent
        self.agents_dict = {}
        self.populateAgent()

        # Creating food 
        self.food_count = 10
        self.foods_dict = {}
        self.populateFood()

        # game state
        self.game_over = False
        self.fps = 10
        self.round = 0

    def startGame(self):
        dis = pygame.display.set_mode((self.dis_width,self.dis_height))
        pygame.display.update()
        pygame.display.set_caption("The Evolution Game")
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()

        while not self.game_over:

            seconds = round((pygame.time.get_ticks() - start_ticks)/1000)
            print(seconds)
            # check time on condition
            if seconds%5 == 0:
                # is agent home else dead 
                self.agents_dict["agent-1"].checkIsHome()
                
       
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
                    self.agents_dict[agent].move(width = self.dis_width, height = self.dis_height, foods_dict = self.foods_dict)
                    self.agents_dict[agent].displayAgent(display = dis)   
                else:
                    self.game_over = True
            
            pygame.display.update()
            
            clock.tick(self.fps)

    def quitGame(self):
        pygame.quit()

    def populateAgent(self):
        
        for i in range(self.number_agent):
            self.agents_dict[f"agent-{i + 1}"] = CA(id=i + 1, home_location=[10 + (i + 1) * 10, (i) * 10], init_location=[10 + (i + 1) * 10, (i) * 10])

    def populateFood(self):

        for i in range(self.food_count):
            foodx = round(random.randrange(20, self.dis_width - 10)/ 10) * 10 
            foody = round(random.randrange(20, self.dis_width - 10)/ 10) * 10
            
            self.foods_dict[f"food-{i + 1}"] = F(id = i + 1, location = [foodx, foody]) 


pygame.init()

Game = Game(width=500, height=500, number_agent=1)

Game.startGame()

Game.quitGame()