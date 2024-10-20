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
import scienceplots
plt.style.use(['science','no-latex','notebook'])

# Design to plot
def get_design(file_path, x):
    # Read the file
    data = np.genfromtxt(file_path, delimiter=',')
    # Get the line x
    line_x = data[x]
    return line_x
x = get_design('../data/paretos/designs_filtered.csv',113)
# get x and y
r, L, x, y, d, N = model.unpack_x(x)
print(d)

# plot
colors.get_colors()     # create the color variables
plt.rcParams.update({'font.size': 16})  # Increase font size
fig,ax = plt.subplots(1,figsize=(7,7))
ax.plot(x,y, linestyle = 'none', marker = 'o', color = colors.black, markersize = 6*r)
for ii in range(len(x)):
    ax.text(x[ii],y[ii],f'{ii+1}',horizontalalignment = 'center', verticalalignment = 'center',color = 'w',weight='bold')
ax.set_xlabel('X location [m]')
ax.set_ylabel('Y location [m]')

#ax.axis('equal')
ax.set_xlim([-40,80])
ax.set_ylim([-40,80])
ax.set_aspect('equal', adjustable='box')
#plt.show()
#plt.savefig('post_pro/plots/design_space.pdf')


### Grid layout
grid_x = [6.00000000e+00 , 1.00005783e-01,  5.11150016,  2.12436944e+02, -4.22189966e+02,  5.11171228e+00,  2.21193671e+01 ,-3.59575494e+02, 5.11097006e+00 , 1.68654060e+01 , 3.45798347e+02,  5.11277117e+00]
r, L, x, y, d, N = model.unpack_x(x)

# plot
colors.get_colors()     # create the color variables
plt.rcParams.update({'font.size': 16})  # Increase font size
fig,ax = plt.subplots(1,figsize=(7,7))
ax.plot(x,y, linestyle = 'none', marker = 'o', color = colors.black, markersize = 6*r)
for ii in range(len(x)):
    ax.text(x[ii],y[ii],f'{ii+1}',horizontalalignment = 'center', verticalalignment = 'center',color = 'w',weight='bold')
ax.set_xlabel('X location [m]')
ax.set_ylabel('Y location [m]')

#ax.axis('equal')
ax.set_xlim([-40,80])
ax.set_ylim([-40,80])
ax.set_aspect('equal', adjustable='box')

### line layout

