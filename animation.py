import numpy as np
import matplotlib.pyplot as plt 

"""
Animation: Vizualising the agent movement.

Integration:
- need to store sources into a list and store it in a dictionary 
- have the path of the agent in a list after every loop
- maybe incorporate in real time visualizing if possible? 
- finding optimize way to store the lists?

x_data = []
y_data = []

x_data_1 = []
y_data_2 = []

sources = {
    0 :[[1,2],[2,3],[4,5]],
    1 :[[1,2],[2,3]]
}

fig, ax = plt.subplots(figsize=(5,5))

ax.set_xlim(0,10)
ax.set_ylim(0,10)
ax.set_xticks(np.arange(11))
ax.set_yticks(np.arange(11))
ax.grid()
scat = ax.scatter(x_data, y_data)
scat_ = ax.scatter(x_data_1, y_data_2)



def animation_frame(i):
    x_data.append([i])
    y_data.append([i])
    data = np.hstack((x_data[len(x_data) - 1],y_data[len(y_data) - 1]))
    scat.set_offsets(data)
    if i >= 4:
        scat_.set_offsets(sources[1])
    else:
        scat_.set_offsets(sources[0])
    return scat, scat_

animation = FuncAnimation(fig, animation_frame, frames=np.arange(0,10,1),interval=10)
HTML(animation.to_jshtml())
"""
