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
N = 4
x =np.array([5.325203438444657,0.14353262885406554,1.2530055440922019,-589.4684883771776,351.18125657271526,4.426026020185715,-674.6244906553854,-108.97963359757523,3.899335279090678,-115.35450094492194,-62.74147042703967,3.3221155388429606])

# get x and y
r, L, x, y, d  = model.unpack_x(x,N)
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
