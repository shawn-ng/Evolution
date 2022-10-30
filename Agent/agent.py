"""
This is the agent class
- need to able to update coordination, able to move 
- health bar 
    - update health bar function 

"""

import numpy as np 

class agentClass():

    def __init__(self, agent_id, map, init_loc):

        # checking agent_id >= 2
        if agent_id < 2:
            raise SyntaxError('agent_id must be bigger or equal to 2')

        self.agent_id = int(agent_id)
        self.map = map
        self.agent_health = 100
        self.action_direction = {
            0: np.array([1,0]), # right
            1: np.array([0,1]), # up
            2: np.array([-1,0]), # left 
            3: np.array([0,-1]), # down
        }
        self.agent_curr_location = init_loc

    def upd_health(self):
        """
        This will update the health bar of the agent.

        Problem
        - Need more context of building the environment rule in order to compute.
        """

    def curr_location(self):
        """
        Finding the location of the agent from the map .
        
        Problem:
        - How do I identify which agent am I refering. 

        Things that dont have to include:
        - I do not need to assign the initial location because I can do it through the game loop. 
        """

        # initial thoughts 
        curr_loc = np.where(map == self.agent_id)

        curr_loc_list = []

        for i in curr_loc:
            curr_loc_list.append(i)

        return curr_loc_list

    def agent_move(self, direction):
        """
        This will allow the agent to move and update the current location as well.

        Addition
        - I need to add detecting forward object 
        - I need to detect 'habitat'
        """
        if int(direction) == 0: #right 
            self.agent_curr_location[0] += self.action_direction[0]
            self.agent_curr_location[1] += self.action_direction[1]
        elif int(direction) == 1: #up 
            self.agent_curr_location[0] += self.action_direction[0]
            self.agent_curr_location[1] += self.action_direction[1]
        elif int(direction) == 2: #left
            self.agent_curr_location[0] += self.action_direction[0]
            self.agent_curr_location[1] += self.action_direction[1]
        elif int(direction) == 3: #down
            self.agent_curr_location[0] += self.action_direction[0]
            self.agent_curr_location[1] += self.action_direction[1]