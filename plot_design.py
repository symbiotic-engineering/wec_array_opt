import matplotlib.pyplot as plt
import modules.model_nWECs as model
import numpy as np

# Design to plot
N = 10

# get x and y
#r, L, x, y, d  = model.unpack_x(x,N)

wecX, wecY = np.meshgrid(np.linspace(0,50,2),np.linspace(0,50,2))
x = wecX.flatten()
y = wecY.flatten()

#x = np.zeros(4)
#y = np.linspace(0,200,4)

#x = np.array([0,30,10,-30])
#y = np.array([0,30,-40,20])

# plot
plt.rcParams.update({'font.size': 16})  # Increase font size
fig,ax = plt.subplots(1,figsize=(10,10))
ax.plot(x,y, linestyle = 'none', marker = 'o', color = (0/256, 158/256, 115/256), markersize = 20)
for ii in range(len(x)):
    ax.text(x[ii],y[ii],f'{ii+1}',horizontalalignment = 'center', verticalalignment = 'center')
ax.axis('equal')
ax.set_xlabel('X location [m]')
ax.set_ylabel('Y location [m]')
plt.savefig('experiments_interaction_1/grid_layout.pdf')