"""
This is the agent class
- need to able to update coordination, able to move 
- health bar 
    - update health bar function 
- Vision of the agent 

"""

import numpy as np 

class agentClass():

    def __init__(self, agent_id, init_loc, sources, map):

        # checking agent_id >= 2
        if agent_id < 2:
            raise SyntaxError('agent_id must be bigger or equal to 2')

        """
        map and source information
        """
        self.map = map
        self.sources = sources
        """
        agent attributes and functionality
        """
        self.agent_id = int(agent_id)
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

        Every move of the agent cause one health and eat source add 1 health (initial)

        Problem
        - Need more context of building the environment rule in order to compute.
        - Agent on the same grid as the health bar
        """
        if self.agent_health == 100:
            self.agent_health = self.agent_health

        if self.detect_source:
            self.agent_health += 1
        else:
            self.agent_health -= 1

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
            self.upd_health()
        elif int(direction) == 1: #up 
            self.agent_curr_location[0] += self.action_direction[0]
            self.agent_curr_location[1] += self.action_direction[1]
            self.upd_health()
        elif int(direction) == 2: #left
            self.agent_curr_location[0] += self.action_direction[0]
            self.agent_curr_location[1] += self.action_direction[1]
            self.upd_health()
        elif int(direction) == 3: #down
            self.agent_curr_location[0] += self.action_direction[0]
            self.agent_curr_location[1] += self.action_direction[1]
            self.upd_health()

    def detect_source(self): 
        """
        The parameter source is the dictionary of source that contain the coordinates and the status of source 

        Output: True means that the source is in the same grid as the agent. 
        """   
        # source that yet to be eaten 
        sources_list = []
   
        for source in self.sources:
            if self.sources[source]['digest'] == False:
                sources_list.appen(self.sources[source]['coor'])
         
        # things to consider -> detecting object infront behind and sides
        if self.agent_curr_location in sources_list:
            return True
        else:
            return False