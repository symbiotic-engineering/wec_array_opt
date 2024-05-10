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
x = [8.0,0.10000176846656803,5.581093837920735,25.099245914231062,57.349730490385554,5.591793670279263,35.566394383063724,18.715676400728057,5.544893817794155,-11.407404511152668,39.45913157871826,5.54611649142049]

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
plt.savefig('post_pro/plots/design_minSPACE.pdf')
