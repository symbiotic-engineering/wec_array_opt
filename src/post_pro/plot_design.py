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
#x =np.array([9.99992319805342,0.10000141275443655,6.29665416651116,35.2553311085241,-47.23848856922516,6.3156648226237255,35.13284647724411,43.61632163749309,6.353502594175767,70.94483065027279,-0.4074111725847307,6.451506386779879])
#x =np.array([2.0001,0.10397832340819038,5.116361100746302,14.037805604014116,-0.09705234903568005,4.968466082392987,7.021016122797809,7.2600758951825295,4.967302814506727,7.07106781,-7.303507084576809,5.301374065918128])
#index 10 is cluster1. 
#index 200 is cluster2
#index 225 is cluster3
#index 241 is cluster4
#index 245 is cluster5
x = [2.000028346374051,0.10013448362444206,5.109433334932386,14.322144189749588,0.0,5.021456029824595,7.128059299166645,7.586125186422013,5.120965893666736,7.072909120014476,-11.160580885499542,5.070070298180154]



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
ax.set_xlim([-40,120])
ax.set_ylim([-80,80])
ax.set_aspect('equal', adjustable='box')
#plt.show()
plt.savefig('post_pro/plots/cluster5_design.pdf')
