"""
Requirements of the environment:
1. Adjustable grid 
    - grid size
    - food 
    - positioning of the foods 
"""
import numpy as np

class gridEnvs():

    label = {
        'grid': 0, 
        'source': 1,
        'agent': 2,
    }

    def __init__(self, size=10, source_num = 2):

        self.size = size
        self.source_num = source_num 


    """
    Need modification into the correct purpose

    def rand_position (self):
        try1[1:9, 1:9] = np.random.randint(low=2, size=(8,8))

        init_sum = int(np.count_nonzero(try1==1))

        if init_sum > 20:
            row_list = np.nonzero(try1)[0]
            column_list = np.nonzero(try1)[1]
            diff_sum = init_sum - 20

            alist = list(range(len(row_list)))
            list_del = random.sample(alist, k = diff_sum)

            for i in list_del:
                try1[row_list[i]][column_list[i]] = 0
    """



    def map_display(self):

        map = np.zeros(self.size, self.size)



