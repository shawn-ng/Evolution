"""
This is the agent class
- need to able to update coordination, able to move 
- health bar 
    - update health bar function 
- Vision of the agent 

"""
import pygame

class CreateAgent():

    def __init__(self, id, home_location , init_location):

        # Identifier
        self.Id = id
        self.colour = (255,255,102)
        self.size = 10
        self.speed = 15
        self.step = 10

        # agent location 
        self.x_loc_home = home_location[0]
        self.y_loc_home = home_location[1]
        self.x_loc = init_location[0]
        self.y_loc = init_location[1]
        
        # activity
        self.activity = {
            "eat": 1,
            "rest": 2, 
            "move": 3
        }

        # agent energy level
        self.energy = 100
        self.max_energy = 100 
        self.food_eaten = 0
        self.food_energy = 5
        self.drainRate = 0.5

        # state 
        self.die = False 
        
        
    def displayAgent(self, display):
        pygame.draw.rect(display, self.colour, [self.x_loc, self.y_loc, self.size, self.size])

    def eat(self):

        self.food_eaten += 1

        self.updateEnergy(activity=1)

    def updateEnergy(self, activity):

        if self.energy <= self.max_energy:
            if activity == self.activity["eat"]:
                self.energy += self.food_energy
            elif activity == self.activity["rest"]:
                self.energy -= self.drainRate * 0.09
            elif activity == self.activity["move"]:
                self.energy -= self.drainRate
            
        if self.energy > self.max_energy:
            self.energy == self.max_energy

    def move(self, width, height, foods_dict):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x_loc >= self.step and self.x_loc <= width - self.step:
                self.x_loc -= self.step 
                self.updateEnergy(activity=3)
                self.detectFood(foods_dict)
        elif keys[pygame.K_RIGHT]:
            if self.x_loc >= 0 and self.x_loc <= width - self.step * 2:
                self.x_loc+= self.step
                self.updateEnergy(activity=3)
                self.detectFood(foods_dict)
        elif keys[pygame.K_DOWN]:
            if self.y_loc >= 0 and self.y_loc <= height - self.step * 2:
                self.y_loc += self.step
                self.updateEnergy(activity=3)
                self.detectFood(foods_dict)
        elif keys[pygame.K_UP]:
            if self.y_loc >= self.step and self.y_loc <= height:
                self.y_loc -= self.step
                self.updateEnergy(activity=3)
                self.detectFood(foods_dict)
        elif keys[pygame.K_1]:
            print(f"energy: {self.energy} \tfood eaten: {self.food_eaten}")
        else:
            self.updateEnergy(activity=2)
        
        
    def detectFood(self, foods_dict):

        for key in foods_dict.keys():
            item = foods_dict[key]
            if [self.x_loc, self.y_loc] == [item.x_loc, item.y_loc]:
                self.eat()
                item.eaten = True
                break
