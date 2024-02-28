import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
grandparent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append("/".join((grandparent_folder,'sea-lab-utils')))
import matplotlib.pyplot as plt
import modules.model_nWECs as model
import numpy as np
import pyplotutilities.colors as colors
# Design to plot
x =np.array([6.299197279076497,0.10007673575582875,5.939685563058021,49.182921347145985,7.320310446259552,5.885220747485372,35.81817865532949,-21.72754886674548,5.972333841463968,19.11948545539301,25.042376603446414,5.880815678820527])

# get x and y
r, L, x, y, d, N = model.unpack_x(x)
print(d)

# plot
colors.get_colors()     # create the color variables
plt.rcParams.update({'font.size': 12})  # Increase font size
fig,ax = plt.subplots(1,figsize=(7,7))
ax.plot(x,y, linestyle = 'none', marker = 'o', color = colors.black, markersize = 6*r)
for ii in range(len(x)):
    ax.text(x[ii],y[ii],f'{ii+1}',horizontalalignment = 'center', verticalalignment = 'center',color = 'w')
ax.set_xlabel('X location [m]')
ax.set_ylabel('Y location [m]')
#ax.set_xlim([-125,175])
#ax.set_ylim([-75,225])
#ax.axis('equal')
#plt.show()
plt.savefig('design.png')
