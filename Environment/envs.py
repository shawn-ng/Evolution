"""
Requirements of the environment:
1. Adjustable grid 
    - grid size
    - food 
    - positioning of the foods 
"""
import numpy as np

class gridEnvs():

    """
    label = {
        'grid': 0, 
        'source': 1,
        'agent': 2,
    }
    """

    def __init__(self, size = 10, source_num = 20):

        self.size = int(size)
        self.source_num = int(source_num) 
        self.map = self.map_create()
        self.source = self.source_position()

    def map_create(self):
        """
        Creating the map with required size 
        - maybe the refresh of the map?
        """
        map = np.zeros((self.size, self.size))       
        map_ = self.source_create(map)
        return map_

    def source_create(self, map):
        """
        Randomly alocating sources in the map where is not the habitat of the agent
        """
        init_sum = 0
        """
        Ensure the number of source are correct number 
        """
        while init_sum != self.source_num:
            map[1:self.size - 1, 1: self.size - 1] = np.random.randint(low=2,size=(self.size - 2, self.size - 2))
            init_sum = int(np.count_nonzero(map==1))
        return map

    def source_position(self):
        """
        The coordinates of the souces and stored in a dictionary and the status of the food

        Dictionary structure:
        {
            0: {
                'coor': [0,1],
                'digest': False
            }
        }
        """
        y_axis = np.where(self.map == 1)[0]
        x_axis = np.where(self.map == 1)[1]

        dict = {}
        init_list = []

        #loop
        for i in range(len(y_axis)):
            init_list.append(y_axis[i])
            init_list.append(x_axis[i])

            dict[i] = {
                'coor': init_list,
                'digest': False
            }

            init_list = []

        return dict  
    
    def available_source(self):
        
        source_list = []

        for i in range(len(self.source)):

            if self.source[i]['digest'] == False:
                source_list.append(self.source[i]['coor'])

        return source_list 


