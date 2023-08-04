import matplotlib.pyplot as plt
import modules.model_nWECs as model
import numpy as np

# Design to plot
N = 10

# get x and y
#r, L, x, y, d  = model.unpack_x(x,N)

wecX, wecY = np.meshgrid(np.linspace(0,50,2),np.linspace(0,250,5))
x = wecX.flatten()
y = wecY.flatten()

x = np.zeros(10)
y = np.linspace(0,500,10)

x = np.array([0,4383,2091,2630,3775,3172,2314,1967,717,3129])*(50/324) #scale down factor for matching with other layouts
y = np.array([0,3262,1414,3180,-1199,2199,3250,4197,3123,2870])*(50/324)

# plot
plt.rcParams.update({'font.size': 16})  # Increase font size
fig,ax = plt.subplots(1,figsize=(10,10))
ax.plot(x,y, linestyle = 'none', marker = 'o', color = (0/256, 158/256, 115/256), markersize = 20)
ax.axis('equal')
ax.set_xlabel('X location [m]')
ax.set_ylabel('Y location [m]')
plt.savefig('experiments_interaction_3/rand_layout.pdf')