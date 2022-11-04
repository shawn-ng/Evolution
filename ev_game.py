import pygame
import random 
import time

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

pygame.init()

width, height = 500, 500
game_screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("The Evolution Game")

while True:
    pass

pygame.quit()