import pygame 

class Food():

    def __init__(self, id,  location):

        # identifier 
        self.Id = id
        self.size = 10
        self.colour = (0,0,255)

        # location 
        self.x_loc = location[0]
        self.y_loc = location[1]

        # state
        self.eaten = False

    def displayFood(self, display):

        if self.eaten != True:
            pygame.draw.rect(display, self.colour, [self.x_loc, self.y_loc, self.size, self.size])
        else:
            pass
