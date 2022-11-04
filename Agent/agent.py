"""
This is the agent class
- need to able to update coordination, able to move 
- health bar 
    - update health bar function 
- Vision of the agent 

"""

import numpy as np 

class agentClass():
    
    def __init__(self, agent_id, init_loc):

        # checking agent_id >= 2
        if agent_id < 2:
            raise SyntaxError('agent_id must be bigger or equal to 2')

        """
        agent attributes and functionality
        """
        self.agent_id = int(agent_id)
        self.energy = 100
        self.action_direction = {
            0: np.array([1,0]), # right
            1: np.array([0,1]), # up
            2: np.array([-1,0]), # left 
            3: np.array([0,-1]), # down
        }

        """
        Location
        """
        # agent passed location stored in the list
        self.agent_tiles = [init_loc]
        self.agent_curr_location = init_loc
        self.agent_habitat = init_loc
        self.vision = []
        # invoking initial update of the agent into the map
        # self.upd_location()

    def eat_source(self):
        """
        This will update the health bar of the agent.

        Every move of the agent cause one health and eat source add 1 health (initial)

        Problem
        - Need more context of building the environment rule in order to compute.
        - Agent on the same grid as the health bar
        """
        if self.energy < 100:
            self.energy += 1

    def move_energy(self):

        self.energy -= 1

    def agent_move(self, direction):
        """
        This will allow the agent to move and update the current location as well.

        Addition
        - I need to add detecting forward object 
        - I need to detect 'habitat'
        """
        last_index = len(self.agent_tiles) - 1
        curr_loc = self.agent_tiles[last_index]
        new_loc = []

        if int(direction) == 0: #right 
            new_loc.append(curr_loc[0] + self.action_direction[0][0])
            new_loc.append(curr_loc[1] + self.action_direction[0][1])
        elif int(direction) == 1: #up 
            new_loc.append(curr_loc[0] + self.action_direction[1][0])
            new_loc.append(curr_loc[1] + self.action_direction[1][1])
        elif int(direction) == 2: #left
            new_loc.append(curr_loc[0] + self.action_direction[2][0])
            new_loc.append(curr_loc[1] + self.action_direction[2][1])
        elif int(direction) == 3: #down
            new_loc.append(curr_loc[0] + self.action_direction[3][0])
            new_loc.append(curr_loc[1] + self.action_direction[3][1])
        
        self.move_energy()
        self.agent_tiles.append(new_loc)
        self.agent_curr_location = new_loc
        self.get_vision()

        #self.upd_location()

    def get_vision(self, distance = 2):
        """
        Each agent will have ther own vision space. 

        Setting on 2 box vision in four direction but doesn't include the diagonal box

        thoughts 
        - I have my current location
        - Then I can use this to calculate my vision 
        - since I have vision means that i will have to allow the agent to detect where is the food
        """

        visionTemp = []
        
        for i in range(4):
            loc = [self.agent_curr_location[0] ,self.agent_curr_location[1]]
            for k in range(distance):

                loc[0] += self.action_direction[i][0]
                loc[1] += self.action_direction[i][1]

                visionTemp.append([loc[0], loc[1]])
        
        self.vision = visionTemp

    
    """
    # Update on the physical map
    def upd_location(self):
        
        last_index = len(self.agent_tiles) - 1
        self.agent_curr_location = self.agent_tiles[last_index]

        if len(self.agent_tiles) != 1:
            prev_location = self.agent_tiles[last_index - 1]

        y_axis = self.agent_curr_location[0]
        x_axis = self.agent_curr_location[1]
        
        if len(self.agent_tiles) != 1:
            self.map[y_axis][x_axis] = self.agent_id
            self.map[prev_location[0]][prev_location[1]] = 0
        else:
            self.map[y_axis][x_axis] = self.agent_id

    def curr_location(self):
        Finding the location of the agent from the map .
        
        Problem:
        - How do I identify which agent am I refering. 

        Things that dont have to include:
        - I do not need to assign the initial location because I can do it through the game loop. 
        
        # initial thoughts 
        curr_loc = np.where(map == self.agent_id)

        curr_loc_list = []

        for i in curr_loc:
            curr_loc_list.append(i)

        return curr_loc_list

    def on_source(self,): 
        
        The parameter source is the dictionary of source that contain the coordinates and the status of source 

        Output: True means that the source is in the same grid as the agent. 
        
        # source that yet to be eaten 
        sources_list = []
   
        for source in self.sources:
            if self.sources[source]['digest'] == False:
                sources_list.append(self.sources[source]['coor'])
         
        # things to consider -> detecting object infront behind and sides
        if self.agent_curr_location in sources_list:
            return True
        else:
            return False
    """
